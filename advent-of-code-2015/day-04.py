import hashlib
import itertools

INPUT = "bgvyzdsv"

def md5_that_starts_with_zeros(zeros):
    for n in itertools.count(start=0):
        hash = hashlib.md5(INPUT.encode() + str(n).encode()).hexdigest()
        if hash.startswith("0" * zeros):
            return n

print(f"PART 1: {md5_that_starts_with_zeros(5)}")
print(f"PART 2: {md5_that_starts_with_zeros(6)}")
