def nice1(s):
    vowels = 0
    double = False
    for i in range(len(s)):
        if s[i] in "aeiou":
            vowels += 1
        if i != 0 and s[i] == s[i - 1]:
            double = True;
    return vowels >= 3 and double and \
        not "ab" in s and \
        not "cd" in s and \
        not "pq" in s and \
        not "xy" in s

def nice2(s):
    repeats = False
    for i in range(len(s) - 2):
        if s[i] == s[i + 2]:
            repeats = True

    double_pair = False
    pairs = dict()
    for i in range(len(s) - 1):
        pair = s[i : i + 2]
        if pair in pairs:
            if i >= pairs[pair] + 2:
                double_pair = True
        else:
            pairs[pair] = i

    return repeats and double_pair

nice1_count = 0;
nice2_count = 0;
with open("day-05.input") as f:
    for line in f:
        nice1_count += nice1(line)
        nice2_count += nice2(line)

print(f"PART 1: {nice1_count}")
print(f"PART 2: {nice2_count}")
