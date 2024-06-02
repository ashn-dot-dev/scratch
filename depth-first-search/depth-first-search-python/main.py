from dataclasses import dataclass, field
import sys

@dataclass
class Node:
    name: str
    children: set = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return self.name

@dataclass
class Graph:
    nodes: set[Node] = field(default_factory=set)


def dfs(graph: Graph) -> list[Node]:
    visited = set()
    sorted = list()

    def visit(node: Node):
        if node in visited:
            return
        visited.add(node)
        for child in node.children:
            visit(child)
        sorted.insert(0, node)

    for node in graph.nodes:
        visit(node)
    return sorted


def dfs_cycle_detecting(graph: Graph) -> list[Node]:
    visiting = set()
    visited = set()
    sorted = list()

    def visit(node: Node):
        if node in visited:
            return
        if node in visiting:
            raise Exception(f"cycle detected in graph {graph}")
        visiting.add(node)
        for child in node.children:
            visit(child)
        visited.add(node)
        sorted.insert(0, node)

    for node in graph.nodes:
        visit(node)
    return sorted


def main():
    # B-->E-->A--+
    # |   |   |  |
    # |   v   |  |
    # +-->C<--+  |
    #      |     v
    #      +---->D

    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Node("D")
    e = Node("E")

    a.children.add(c)
    a.children.add(d)

    b.children.add(c)
    b.children.add(e)

    c.children.add(d)

    e.children.add(a)
    e.children.add(c)

    sorted = dfs(Graph((a, b, c, d, e)))
    print([node.name for node in sorted])

    # +->W-->X--+
    # |  |   |  |
    # |  |   v  v
    # |  +-->Y->Z
    # |         |
    # +---------+

    w = Node("W")
    x = Node("X")
    y = Node("Y")
    z = Node("Z")

    w.children.add(x)
    w.children.add(y)

    x.children.add(y)
    x.children.add(z)

    y.children.add(z)

    z.children.add(w)

    sorted = dfs_cycle_detecting(Graph((a, b, c, d, e)))
    print([node.name for node in sorted])
    try:
        sorted = dfs_cycle_detecting(Graph((w, x, y, z)))
    except Exception as e:
        print("error:", e, file=sys.stderr)
    print([node.name for node in sorted])


if __name__ == "__main__":
    main()
