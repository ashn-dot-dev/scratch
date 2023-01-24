from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

with open("day-11.input") as f:
    input = f.read().strip();

class Part(Enum):
    PART1 = 1
    PART2 = 2

@dataclass
class Monkey:
    items: List[int]
    operator: str
    lhs_operand: Optional[int]  # None => old
    rhs_operand: Optional[int]  # None => old
    test_divisible: int
    test_t_target: int
    test_f_target: int
    total_inspections: int

    def take_turn(self, monkeys: List["Monkey"], monkeys_test_product: int, part: Part) -> None:
        if len(self.items) == 0:
            return

        def operation(operator, lhs, rhs):
            if operator == "+":
                return lhs + rhs
            if operator == "*":
                return lhs * rhs
            Exception("unknown operator")

        while len(self.items) != 0:
            self.total_inspections += 1
            lhs = self.lhs_operand or self.items[0]
            rhs = self.rhs_operand or self.items[0]
            self.items[0] = operation(self.operator, lhs, rhs)
            if part == Part.PART1:
                self.items[0] //= 3

            # All monkey test divisible numbers in the day 11 input are prime.
            # If the item is divisible by the product of all the test divisible
            # numbers, then the test for "is this divisible by <number>" will
            # produce the same result for the item modulo that product as it
            # would for that item itself. By performing this modulo reduction
            # every turn, we prevent the worry level for the items from
            # ballooning to huge integers that would otherwise slow down the
            # computation beyond any reasonable amount of time.
            self.items[0] %= monkeys_test_product

            divisible = self.items[0] % self.test_divisible == 0
            target = self.test_t_target if divisible else self.test_f_target
            monkeys[target].items.append(self.items.pop(0))


def parse_monkey(s: str) -> Monkey:
    def parse_operation(line):
        fields = line.split(" = ")[1].split()
        operator = fields[1]
        lhs = None
        if fields[0] != "old":
            lhs = int(fields[0])
        rhs = None
        if fields[2] != "old":
            rhs = int(fields[2])
        return operator, lhs, rhs

    lines = list([x.strip() for x in s.split("\n")])
    items = [int(x) for x in lines[1].split(": ")[1].split(", ")]
    operation_line = lines[2]
    operator, lhs_operand, rhs_operand = parse_operation(operation_line)
    test_divisible = int(lines[3].split()[-1])
    test_t_target = int(lines[4].split()[-1])
    test_f_target = int(lines[5].split()[-1])

    return Monkey(items, operator, lhs_operand, rhs_operand, test_divisible, test_t_target, test_f_target, 0)

monkeys = list(map(parse_monkey, input.split("\n\n")))
monkeys_test_product = 1
for m in monkeys:
    monkeys_test_product *= m.test_divisible

def part1(monkeys, monkeys_test_product):
    for _ in range(20):
        for m in monkeys:
            m.take_turn(monkeys, monkeys_test_product, Part.PART1)
    active = list(reversed(sorted(monkeys, key = lambda m: m.total_inspections)))
    print(f"PART 1: {active[0].total_inspections * active[1].total_inspections}")

def part2(monkeys, monkeys_test_product):
    monkeys = list(map(parse_monkey, input.split("\n\n")))
    for _ in range(10000):
        for m in monkeys:
            m.take_turn(monkeys, monkeys_test_product, Part.PART2)
    active = list(reversed(sorted(monkeys, key = lambda m: m.total_inspections)))
    print(f"PART 2: {active[0].total_inspections * active[1].total_inspections}")

part1(deepcopy(monkeys), monkeys_test_product)
part2(deepcopy(monkeys), monkeys_test_product)
