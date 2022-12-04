with open("day-01.input") as f:
    input = f.read();

elves = input.split("\n\n")
totals = [sum([int(calories) for calories in x.split()]) for x in elves]
sorted = list(reversed(sorted(totals)))

print(f"PART 1: {sorted[0]}")
print(f"PART 2: {sorted[0] + sorted[1] + sorted[2]}")
