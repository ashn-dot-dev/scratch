struct Board[Rows: Int, Cols: Int]:
    var data: Pointer[Bool]

    fn __init__(inout self):
        var data = Pointer[Bool].alloc(Rows * Cols)
        memset_zero(data, Rows * Cols)
        self.data = data

    fn __moveinit__(inout self, owned other: Self):
        self.data = other.data

    fn __del__(owned self):
        Pointer[Bool].free(self.data)

    fn __getitem__(self, row: Int, col: Int) -> Bool:
        return self.data[row * Cols + col]

    fn __setitem__(self, row: Int, col: Int, value: Bool):
        self.data[row * Cols + col] = value

    fn __str__(self) -> String:
        var result = String()
        result += String("+") + String("-") * Cols + "+\n"
        for row in range(Rows):
            result += "|"
            for col in range(Cols):
                var value = self[row, col]
                result += "#" if self[row, col] else " "
            result += "|\n"
        result += String("+") + String("-") * Cols + "+"
        return result

    fn rows(self) -> Int:
        return Rows

    fn cols(self) -> Int:
        return Cols

    fn next(self) -> Board[Rows, Cols]:
        var new = Self()
        for row in range(Rows):
            for col in range(Cols):
                var neighbors = 0
                var coordinates = List(
                    (row-1, col-1),
                    (row-1, col+0),
                    (row-1, col+1),

                    (row+0, col-1),
                    (row+0, col+1),

                    (row+1, col-1),
                    (row+1, col+0),
                    (row+1, col+1),
                )
                for rc in coordinates:
                    var r = rc[].get[0, Int]()
                    var c = rc[].get[1, Int]()
                    if r < 0 or r >= Rows:
                        continue
                    if c < 0 or c >= Cols:
                        continue
                    neighbors += 1 if self[r, c] else 0
                # Any live cell with fewer than two live neighbors dies, as if
                # by underpopulation.
                if self[row, col] and neighbors < 2:
                    new[row, col] = False
                # Any live cell with two or three live neighbors lives on to
                # the next generation.
                elif self[row, col] and neighbors == 2 or neighbors == 3:
                    new[row, col] = True
                # Any live cell with more than three live neighbors dies, as if
                # by overpopulation.
                elif self[row, col] and neighbors > 3:
                    new[row, col] = False
                # Any dead cell with exactly three live neighbors becomes a
                # live cell, as if by reproduction.
                elif not self[row, col] and neighbors == 3:
                    new[row, col] = True
        return new^

    fn advance(inout self):
        self = self.next()


fn glider[Rows: Int, Cols: Int]() raises -> Board[Rows, Cols]:
    if Rows < 3 or Cols < 3:
        raise Error("[glider] invalid board size")
    var board = Board[Rows, Cols]()
    board[0, 1] = True
    board[1, 2] = True
    board[2, 0] = True
    board[2, 1] = True
    board[2, 2] = True
    return board^


fn random[Rows: Int, Cols: Int]() -> Board[Rows, Cols]:
    from random import seed, random_ui64
    seed()
    var board = Board[Rows, Cols]()
    for row in range(board.rows()):
        for col in range(board.cols()):
            board[row, col] = Bool(random_ui64(0, 1))
    return board^


fn animate[Rows: Int, Cols: Int, SleepSec: Float64 = 0.10](owned board: Board[Rows, Cols], generations: Optional[Int]):
    from time import sleep
    var HOME  = "\x1B[1;1H" # ANSI Escape - Move cursor row=1, col=1.
    var CLEAR = "\x1B[2J"   # ANSI Escape - Erase entire screen.
    # XXX: At the time of writing, it looks like Mojo is not catching keyboard
    # interrupts as an exception, so there is no good way to set the cursor to
    # be invisible, and then reset the cursor to be visible after an interrupt.
    #var MKINV = "\x1B[?25l" # ANSI Escape - Make cursor invisible.
    #var MKVIS = "\x1B[?25h" # ANSI Escape - Make cursor visible.

    print(CLEAR, sep="", end="")
    var generation = 0
    while generation < generations.or_else(generation + 1):
        print(HOME, board, sep="", end="")
        board.advance()
        sleep(SleepSec)
    print(HOME, board, sep="", end="")


def main():
    # XXX: I would love to use Python's ArgumentParser to parse command line
    # arguments, but I hit so many snags during development that I am avoiding
    # integrating Python argument parsing for now. It looks like I could use
    # the Mojo's `sys.arg.argv` function[1] to parse arguments manually, but I
    # would rather use Python's more ergonomic builtin library. Issues I ran
    # into include...
    #
    # (1) At the time of writing, compiling life.mojo on macOS with:
    #
    #   mojo build life.mojo
    #
    # creates a binary that will produce this error and then segfault:
    #
    #   $ ./life
    #   Mojo/Python interoperability error: Unable to locate a suitable libpython, please set `MOJO_PYTHON_LIBRARY`
    #   Segmentation fault: 11
    #
    # This is a known issue with Python imports, and can be fixed by running
    # the executable as:
    #
    #   $ MOJO_PYTHON_LIBRARY=$(modular config mojo.python_lib) ./life
    #
    # See Mojo issue #551[2] for more information.
    #
    # (2) When the compiled Mojo program from (1) is run, keyboard interrupts
    # are not handled, so stopping an infinite animation requires killing the
    # process from another terminal or sending the process to the background
    # and killing the background job. Note that when the Python import and
    # ArgumentParser code was removed, keyboard interrupts did register in
    # compiled programs. Not sure what part of the Mojo<->Python interactions
    # were causing the unexpected behavior.
    #
    # (3) At the time of writing, attempting to specify the type of an
    # ArgumentParser argument as `int` fails to compile with the error:
    #
    #   error: cannot convert function to non-function type 'PythonObject'
    #       parser.add_argument("-g", "--generations", nargs="?", type=int)
    #
    # since `int` is a type in Python, but is a function in Mojo.
    #
    # (4) Mojo seems to eat command line arguments that I would expect to be
    # handled by the argument parser. Providing `-h` or `--help` as a command
    # line argument is ignored (no help text printed), and providing an
    # optional argument (i.e. "--generations=10") produces a `None` object for
    # `args.generations` when `args` is created and assigned with:
    #
    #    var args = parser.parse_args()
    #
    # Not sure if this is something I am not aware of in Python, or whether it
    # is a specific Mojo<->Python interaction.
    #
    # [1]: https://docs.modular.com/mojo/stdlib/sys/arg/argv
    # [2]: https://github.com/modularml/mojo/issues/551

    alias ROWS = 28
    alias COLS = 80

    # Test animation spawning a glider.
    #animate(glider[ROWS, COLS](), 32)

    # Default behavior - generate and advance a random board.
    animate(random[ROWS, COLS](), None)
