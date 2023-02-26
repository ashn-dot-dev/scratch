from argparse import ArgumentParser
from cProfile import Profile
from dataclasses import dataclass, field
from math import inf
from pstats import Stats
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
    reachable: Set["Square"] = field(default_factory=set)
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
                screen.addch(y, x, "<")
                continue
            if previous.position.x == position.x + 1 and previous.position.y == position.y:
                screen.addch(y, x, ">")
                continue
            if previous.position.x == position.x and previous.position.y == position.y - 1:
                screen.addch(y, x, "^")
                continue
            if previous.position.x == position.x and previous.position.y == position.y + 1:
                screen.addch(y, x, "v")
                continue
            assert False, "unreachable"
    screen.refresh()

def shortest_path(squares: Dict[Position, Square], e: Square, screen = None):
    """
    Dijkstra's shortest path algorithm, implemented to find the distance from
    each square in `squares` to the end square `e`.
    """
    # All unvisited squares.
    unvisited: Set[Square] = {x for x in squares.values()}
    # All unvisited squares that have had their distance updated.
    #
    # This set contains redundant information that *could* be calculated purely
    # from the unvisited set. However the performance gains from caching this
    # information separately is worth the redundancy cost.
    visitable: Set[Square] = {x for x in unvisited if x.distance is not None}

    def visit(square: Square):
        assert square.distance is not None
        for x in filter(lambda s: s in unvisited, square.reachable):
            if x.distance is None:
                x.distance = square.distance + 1
                x.previous = square
                visitable.add(x)
        unvisited.discard(square)
        visitable.discard(square)

    e.distance = 0
    visit(e)

    max_x = max(map(lambda position: position.x, squares.keys()))
    max_y = max(map(lambda position: position.y, squares.keys()))

    while True:
        ordered = sorted(visitable, key=lambda x: cast(int, x.distance))
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
    squares: Dict[Position, Square] = dict()

    # Initialize all squares with a position and elevation.
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

    # Calculate reachable neighbors for each square.
    for square in squares.values():
        def neighbors(square: Square) -> Set[Square]:
            position = square.position
            adjacent = [
                Position(position.x - 1, position.y),
                Position(position.x + 1, position.y),
                Position(position.x, position.y - 1),
                Position(position.x, position.y + 1),
            ]
            return {squares[p] for p in adjacent if p in squares}

        def reachable(square: Square):
            position = square.position
            return {
                n for n in neighbors(square)
                if n.elevation + 1 >= square.elevation
            }

        square.reachable = reachable(square)

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
    parser.add_argument("-p", "--profile", action="store_true")
    args = parser.parse_args()

    if args.profile:
        profile = Profile()
        profile.runcall(main, None)
        stats = Stats(profile)
        stats.sort_stats("tottime")
        stats.print_stats()
        sys.exit(0)

    part1, part2 = curses.wrapper(main) if args.display else main(None)
    print(f"PART 1: {part1}")
    print(f"PART 2: {part2}")
