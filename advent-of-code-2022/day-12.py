# Solved using Dijkstra's Shortest Path Algorithm implemented based on the
# explanation from [1].
#
# [1]: https://youtu.be/bZkzH5x0SKU
from dataclasses import dataclass
from string import ascii_lowercase
from typing import Dict, List, Optional, Set, Tuple, cast

@dataclass
class Square:
    position: Tuple[int, int]
    elevation: int
    distance: Optional[int] = None
    previous: Optional["Square"] = None

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

def shortest_path(squares: Dict[Tuple[int, int], Square], s: Square, e: Square):
    def neighbors(square: Square) -> Set[Square]:
        position = square.position
        adjacent = [
            (position[0] - 1, position[1]),
            (position[0] + 1, position[1]),
            (position[0], position[1] - 1),
            (position[0], position[1] + 1),
        ]
        return {squares[p] for p in adjacent if p in squares}

    visited: Set[Square] = set()
    unvisited: Set[Square] = {x for x in squares.values()}

    def visit(square: Square):
        assert(square.distance is not None)
        candidates = {n for n in neighbors(square) if n in unvisited and n.elevation <= square.elevation + 1}
        for x in candidates:
            x.distance = square.distance + 1
            x.previous = square
        unvisited.discard(square)
        visited.add(square)

    s.distance = 0
    visit(s)

    def next():
        return sorted({x for x in unvisited if x.distance is not None}, key=lambda x: x.distance or -1)[0]

    while e not in visited:
        visit(next())


def parsed(input: List[str]):
    S: Optional[Square] = None
    E: Optional[Square] = None
    squares: Dict[Tuple[int, int], Square] = dict()

    for y in range(len(input)):
        for x in range(len(input[y])):
            position = (x + 1, y + 1)
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
    S.distance = 0
    return squares, S, E

with open("day-12.input") as f:
    input = [s.strip() for s in f.readlines()];

squares, S, E = parsed(input)
shortest_path(squares, S, E)
print(f"PART 1: {E.distance}")
