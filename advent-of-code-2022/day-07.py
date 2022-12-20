class Entry:
    def __init__(self, parent, name, size=0):
        self.name = name
        self.size = size
        self.parent = parent
        self.children = dict()

    def __repr__(self):
        return f"{str(self.__class__.__name__)}(name={repr(self.name)}, size={self.size})"

    def __str__(self):
        result = [f"- {str(self.name)} (size={str(self.size)})"]
        for c in sorted(self.children.values(), key = lambda x: x.name):
            result.append("\n".join(["  " + x for x in str(c).split("\n")]))
        return "\n".join(result)

    def is_directory(self):
        return len(self.children) != 0

    def insert(self, node):
        self.children[node.name] = node
        while self != None:
            self.size += node.size
            self = self.parent

with open("day-07.input") as f:
    input = [s.strip() for s in f.readlines()];

root = Entry(None, "/");
current_directory = root

for line in input:
    if line.startswith("$ cd"):
        name = line[len("$ cd "):]
        if name == "/":
            current_directory = root
            continue
        if name == "..":
            current_directory = current_directory.parent;
            continue;
        current_directory = current_directory.children[name]
        continue

    if line.startswith("$ ls"):
        # A line with ls is always followed by lines listing files in the
        # current directory.
        continue;

    # Line from ls listing files in the current directory.
    fields = line.split(" ")
    name = fields[1]
    if name in current_directory.children:
        continue # Already added.
    if fields[0] == "dir":
        current_directory.insert(Entry(current_directory, name))
        continue;
    current_directory.insert(Entry(current_directory, name, int(fields[0])))

def directories(node):
    result = []
    if node.is_directory():
        result.append(node)
    for c in node.children.values():
        result += directories(c)
    return result

print(root)

# PART 1
candidates = filter(lambda d: d.size < 100000, directories(root))
print(f"PART 1: {sum(map(lambda d: d.size, candidates))}")

# PART 2
need = 30000000 - (70000000 - root.size);
candidates = filter(lambda d: d.size >= need, directories(root))
smallest = sorted(candidates, key=lambda d: d.size)[0].size
print(f"PART 2: {smallest}")
