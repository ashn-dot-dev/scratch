from argparse import ArgumentParser
from itertools import count
from enum import Enum

Order = Enum("Order", ["NEITHER", "INORDER", "UNORDER"])

def compare(lhs, rhs, debug=False) -> Order:
    if debug:
        print(f"COMPARE {lhs} vs {rhs}")

    # If both values are integers, the lower integer should come first. If the
    # left integer is lower than the right integer, the inputs are in the right
    # order. If the left integer is higher than the right integer, the inputs
    # are not in the right order. Otherwise, the inputs are the same integer;
    # continue checking the next part of the input.
    if isinstance(lhs, int) and isinstance(rhs, int):
        if lhs < rhs:
            return Order.INORDER
        if lhs > rhs:
            return Order.UNORDER
        return Order.NEITHER

    # If both values are lists, compare the first value of each list, then the
    # second value, and so on. If the left list runs out of items first, the
    # inputs are in the right order. If the right list runs out of items first,
    # the inputs are not in the right order. If the lists are the same length
    # and no comparison makes a decision about the order, continue checking the
    # next part of the input.
    if isinstance(lhs, list) and isinstance(rhs, list):
        for i in count():
            if i == len(lhs) and i == len(rhs):
                return Order.NEITHER
            if i == len(lhs):
                return Order.INORDER
            if i == len(rhs):
                return Order.UNORDER
            cmp = compare(lhs[i], rhs[i])
            if cmp != Order.NEITHER:
                return cmp

    # If exactly one value is an integer, convert the integer to a list which
    # contains that integer as its only value, then retry the comparison. For
    # example, if comparing [0,0,0] and 2, convert the right value to [2] (a
    # list containing 2); the result is then found by instead comparing [0,0,0]
    # and [2].
    if isinstance(lhs, int) and isinstance(rhs, list):
        return compare([lhs], rhs)
    if isinstance(lhs, list) and isinstance(rhs, int):
        return compare(lhs, [rhs])

    assert False, "unreachable"

def main(args):
    with open("day-13.input") as f:
        input = f.read();

    pairs = [tuple(x.split("\n")) for x in input.split("\n\n")]
    pairs = [(eval(p[0]), eval(p[1])) for p in pairs]

    sum = 0
    for i in range(len(pairs)):
        cmp = compare(*pairs[i], debug=args.debug)
        if args.debug:
            print(cmp)
        if cmp == Order.INORDER:
            sum += i + 1

    print(f"PART 1: {sum}")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    main(parser.parse_args())
