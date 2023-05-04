from argparse import ArgumentParser
from itertools import count
from enum import Enum


class TokenKind(Enum):
    EOI = "end-of-input"
    COMMA = ","
    INTEGER = "integer"
    LBRACKET = "["
    RBRACKET = "]"


class Token:
    def __init__(self, kind, text):
        self.kind = kind
        self.text = text

    def __str__(self):
        if self.kind == TokenKind.INTEGER:
            return f"{self.kind.value}({self.text})"
        return f"{self.kind.value}"


class Lexer:
    EOI = ""

    def __init__(self, source):
        self.source = source
        self.position = 0

    def is_eoi(self):
        return self.position >= len(self.source)

    def current_character(self):
        if self.is_eoi():
            return Lexer.EOI
        return self.source[self.position]

    def next_token(self):
        start = self.position

        if self.is_eoi():
            return Token(TokenKind.EOI, Lexer.EOI)

        if self.current_character() == TokenKind.COMMA.value:
            self.position += len(TokenKind.COMMA.value)
            return Token(TokenKind.COMMA, self.source[start : self.position])

        if self.current_character() == TokenKind.LBRACKET.value:
            self.position += len(TokenKind.LBRACKET.value)
            return Token(TokenKind.LBRACKET, self.source[start : self.position])

        if self.current_character() == TokenKind.RBRACKET.value:
            self.position += len(TokenKind.RBRACKET.value)
            return Token(TokenKind.RBRACKET, self.source[start : self.position])

        if self.current_character().isdigit():
            while self.current_character().isdigit():
                self.position += 1
            return Token(TokenKind.INTEGER, self.source[start : self.position])

        raise Exception(f"invalid character `{self.current_character()}`")


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = lexer.next_token()

    def parse_packet(self):
        value = self.parse_list()
        if self.current.kind != TokenKind.EOI:
            raise Exception(f"expected {TokenKind.EOI.value} (found `{self.current}`)")
        return value

    def parse_value(self):
        if self.current.kind == TokenKind.LBRACKET:
            return self.parse_list()

        if self.current.kind == TokenKind.INTEGER:
            return self.parse_integer()

        raise Exception(f"expected value (found `{self.current}`)")

    def parse_list(self):
        if self.current.kind != TokenKind.LBRACKET:
            raise Exception(f"expected `{TokenKind.LBRACKET.value}` (found `{self.current}`)")
        self.current = self.lexer.next_token()

        result = []
        while self.current.kind != TokenKind.RBRACKET:
            if len(result) != 0:
                if self.current.kind != TokenKind.COMMA:
                    raise Exception(f"expected `{TokenKind.COMMA.value}` (found `{self.current}`)")
                self.current = self.lexer.next_token()
            result.append(self.parse_value())

        if self.current.kind != TokenKind.RBRACKET:
            raise Exception(f"expected `{TokenKind.RBRACKET.value}` (found `{self.current}`)")
        self.current = self.lexer.next_token()
        return result

    def parse_integer(self):
        if self.current.kind != TokenKind.INTEGER:
            raise Exception(f"expected {TokenKind.INTEGER.value} (found `{self.current}`)")
        result = int(self.current.text)
        self.current = self.lexer.next_token()
        return result


def parse_packet(line):
    lexer = Lexer(line)
    parser = Parser(lexer)
    return parser.parse_packet()


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


def part1(input, debug=False):
    pairs = [tuple(x.split("\n")) for x in input.split("\n\n")]
    pairs = [(parse_packet(p[0]), parse_packet(p[1])) for p in pairs]

    sum = 0
    for i in range(len(pairs)):
        cmp = compare(*pairs[i], debug)
        if debug:
            print(cmp)
        if cmp == Order.INORDER:
            sum += i + 1

    print(f"PART 1: {sum}")


def part2(input, debug=False):
    packets = [parse_packet(p) for p in input.split("\n") if len(p) != 0]
    packets.append([[2]])
    packets.append([[6]])

    # Bubble sort the packets. Slow, but simple to implement.
    for i in range(len(packets)):
        for j in range(len(packets) - i - 1):
            cmp = compare(packets[j], packets[j + 1])
            if cmp == Order.UNORDER:
                packets[j], packets[j + 1] = packets[j + 1], packets[j]

    # Find the divider packets.
    def is_divider(packet, num):
        assert isinstance(packet, list)
        if len(packet) != 1:
            return False
        if not isinstance(packet[0], list):
            return False
        if len(packet[0]) != 1:
            return False
        return packet[0][0] == num

    divider_2 = None
    divider_6 = None
    for i in range(len(packets)):
        packet = packets[i]
        if is_divider(packet, 2):
            assert divider_2 is None
            divider_2 = i + 1
        if is_divider(packet, 6):
            assert divider_6 is None
            divider_6 = i + 1

    print(f"PART 2: {divider_2 * divider_6}")


def main(args):
    with open("day-13.input") as f:
        input = f.read()

    part1(input, args.debug)
    part2(input, args.debug)


if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument("-d", "--debug", action="store_true")
    main(ap.parse_args())
