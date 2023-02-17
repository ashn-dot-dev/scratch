from argparse import ArgumentParser
from dataclasses import dataclass
from math import inf
from string import ascii_lowercase
from typing import Dict, List, Optional, Set, Tuple, cast
import curses
import sys

@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

@dataclass
class Square:
    position: Position
    elevation: int
    # Distance from this square to the end square. None if the end square
    # cannot be reached from this square.
    distance: Optional[int] = None
    # The previous visited square with a path that reaches this square. None if
    # this square has not been touched by a visited square.
    previous: Optional["Square"] = None

    def __hash__(self):
        return hash(self.position)

def display(squares: Dict[Position, Square], max_x: int, max_y: int, screen):
    for y in range(max_y):
        for x in range(max_x):
            position = Position(x, y)
            if squares[position].distance == 0:
                screen.addch(y, x, "E")
                continue
            previous = squares[position].previous
            if previous is None:
                elevation = squares[position].elevation
                screen.addch(y, x, ascii_lowercase[elevation])
                continue
            if previous.position.x == position.x - 1 and previous.position.y == position.y:
                screen.addch(y, x, chr(0xFFE9))
                continue
            if previous.position.x == position.x + 1 and previous.position.y == position.y:
                screen.addch(y, x, chr(0xFFEB))
                continue
            if previous.position.x == position.x and previous.position.y == position.y - 1:
                screen.addch(y, x, chr(0xFFEA))
                continue
            if previous.position.x == position.x and previous.position.y == position.y + 1:
                screen.addch(y, x, chr(0xFFEC))
                continue
            assert False, "unreachable"
    screen.refresh()

def shortest_path(squares: Dict[Position, Square], e: Square, screen = None):
    """
    Dijkstra's shortest path algorithm, implemented to find the distance from
    each square in `squares` to the end square `e`. Edges from each square to
    other squares are calculated on the fly via the `candidates` subroutine.
    """
    visited: Set[Square] = set()
    unvisited: Set[Square] = {x for x in squares.values()}

    def neighbors(square: Square) -> Set[Square]:
        position = square.position
        adjacent = [
            Position(position.x - 1, position.y),
            Position(position.x + 1, position.y),
            Position(position.x, position.y - 1),
            Position(position.x, position.y + 1),
        ]
        return {squares[p] for p in adjacent if p in squares}

    def candidates(square: Square):
        position = square.position
        return {
            n for n in neighbors(square)
            if n in unvisited and n.elevation + 1 >= square.elevation
        }

    def visit(square: Square):
        assert(square.distance is not None)
        for x in candidates(square):
            if x.distance is None:
                x.distance = square.distance + 1
                x.previous = square
        unvisited.discard(square)
        visited.add(square)

    e.distance = 0
    visit(e)

    max_x = max(map(lambda position: position.x, squares.keys()))
    max_y = max(map(lambda position: position.y, squares.keys()))

    while True:
        ordered = sorted(
            {x for x in unvisited if x.distance is not None},
            key=lambda x: cast(int, x.distance)
        )
        if len(ordered) == 0:
            return # no more visitable squares
        visit(ordered[0])
        if screen is not None:
            display(squares, max_x, max_y, screen)

def main(stdscr):
    with open("day-12.input") as f:
        input = [s.strip() for s in f.readlines()];

    S: Optional[Square] = None
    E: Optional[Square] = None
    squares: Dict[Tuple[int, int], Square] = dict()

    for y in range(len(input)):
        for x in range(len(input[y])):
            position = Position(x, y)
            if input[y][x] == "S":
                assert S is None
                S = Square(position, ascii_lowercase.find("a"))
                squares[position] = S
                continue
            if input[y][x] == "E":
                assert E is None
                E = Square(position, ascii_lowercase.find("z"))
                squares[position] = E
                continue
            squares[position] = Square(position, ascii_lowercase.find(input[y][x]))

    assert(S is not None)
    assert(E is not None)

    shortest_path(squares, E, stdscr)
    if stdscr is not None:
        # Accept final keyboard input before quitting.
        stdscr.getch()

    shortest_start = sorted(
        [s for s in squares.values() if s.elevation == 0],
        key=lambda x: x.distance or inf
    )[0]
    return (S.distance, shortest_start.distance)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--display", action="store_true")
    args = parser.parse_args()

    part1, part2 = curses.wrapper(main) if args.display else main(None)
    print(f"PART 1: {part1}")
    print(f"PART 2: {part2}")
