"""
Advent of Code 2022 / Day 11
url: https://adventofcode.com/2022/day/11
"""

# %%
import re
import math

# %%
DATA_PATH = 'data/day11.txt'


# %%
class Monkey:
    REGEX_DESC = re.compile(
        (r'Monkey (\d+):\n.+?:\s(.+)\n.+?new = (.+)\n.+?(\d+)\n.+?(\d+)\n.+?'
         r'(\d+)'))

    def __init__(self, input_str) -> None:
        matched_groups = self.REGEX_DESC.match(input_str).groups()
        self.id = matched_groups[0]
        self.items = list(map(int, matched_groups[1].split(', ')))
        self.operation_str = matched_groups[2]
        self.test_divider = int(matched_groups[3])
        self.true_target = int(matched_groups[4])
        self.false_target = int(matched_groups[5])

        self.inspect_times = 0

    def __repr__(self) -> str:
        return f"""id: {self.id}
        items: {self.items}
        operation_str: {self.operation_str}
        test_divider: {self.test_divider}
        true_target: {self.true_target}
        false_target: {self.false_target}
        """

    def _find_receiver(self, item: int) -> int:
        if item % self.test_divider == 0:
            return self.true_target
        else:
            return self.false_target

    def _inspect_item(self, all_monkeys: list) -> None:
        item = self.items.pop(0)

        level_opreated = self._oprate_value(item)
        level_reliefed = self._manage_value(level_opreated)
        target = self._find_receiver(item=level_reliefed)
        self.inspect_times += 1

        target_monkey: Monkey = all_monkeys[target]
        target_monkey.receive_item(level_reliefed)

    def _manage_value(self, item) -> int:
        return item // 3

    def _oprate_value(self, item) -> int:
        return eval(self.operation_str.replace('old', str(item)))

    def process_turn(self, all_monkeys: list) -> None:
        while self.items:
            self._inspect_item(all_monkeys)

    def receive_item(self, item: int) -> None:
        self.items.append(item)


# %%
def read_input(input_path) -> list[str]:
    with open(input_path, 'r') as f:
        monkey_descs = f.read().split('\n\n')
    return monkey_descs


def monkey_play(monkey_descs, monkey_class, rounds=20) -> int:

    # Create monkeys.
    monkeys = []
    for desc in monkey_descs:
        monkey: Monkey = monkey_class(desc)
        monkeys.append(monkey)

    # Playing
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.process_turn(all_monkeys=monkeys)

    # Monkey business
    inspect_times_all = [m.inspect_times for m in monkeys]
    inspect_times_all.sort(reverse=True)
    return inspect_times_all[0] * inspect_times_all[1]


# %%
monkey_descs = read_input(DATA_PATH)
monkey_play(monkey_descs, monkey_class=Monkey)


# %%
# Part 2
def get_dividers(path) -> list[int]:

    with open(path, 'r') as f:
        input_str = f.read()

    divider_strs = re.findall(r'Test.+?(\d+)', input_str)
    return [int(divider_str) for divider_str in divider_strs]


dividers = get_dividers(DATA_PATH)


# %%
class Monkey2(Monkey):

    def _manage_value(self, item) -> int:
        return item % math.lcm(*dividers)


monkey_play(monkey_descs=monkey_descs, monkey_class=Monkey2, rounds=10000)
