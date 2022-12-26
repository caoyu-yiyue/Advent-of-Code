"""
Advent of Code 2022 / Day 21
url: https://adventofcode.com/2022/day/21
"""

# %%
with open('data/day21.txt', 'r') as f:
    input_lines = f.read().splitlines()


# %%
class Monkey:

    def __init__(self, name, job: str) -> None:
        self.name: str = name
        self.job: str = job
        self.value: int = None
        self.parent = None
        self.children = []

    def __repr__(self) -> str:
        return f"""
        Name: {self.name},
        Value: {self.value},
        Parent: {self.parent.name}
        """

    def parse_job(self):
        if self.job.isnumeric():
            self.value = int(self.job)
            return self.value

        m1_name, sign, m2_name = self.job.split()
        m1 = ALL_MONKEYS[m1_name]
        m1.parent = self
        m2 = ALL_MONKEYS[m2_name]
        m2.parent = self
        self.children.extend([m1, m2])

        if sign == '+':
            self.value = m1.parse_job() + m2.parse_job()
            return self.value
        elif sign == '-':
            self.value = m1.parse_job() - m2.parse_job()
            return self.value
        elif sign == '*':
            self.value = m1.parse_job() * m2.parse_job()
            return self.value
        elif sign == '/':
            self.value = m1.parse_job() / m2.parse_job()
            return self.value


# %%
ALL_MONKEYS = {}
for line in input_lines:
    name, job = line.split(': ')
    ALL_MONKEYS[name] = Monkey(name, job)

# %%
root_m = ALL_MONKEYS['root']
root_m.parse_job()

# %%
# Part 2
trackback = []
m = ALL_MONKEYS['humn']
while m.parent is not None:
    trackback.insert(0, m.name)
    m = m.parent


def reverse_job(target, knowed_num, knowed_idx, job):
    _, sign, _ = job.split()

    if sign == '+':
        return target - knowed_num
    elif sign == '-' and knowed_idx == 0:
        return knowed_num - target
    elif sign == '-' and knowed_idx == 1:
        return knowed_num + target
    elif sign == '*':
        return target / knowed_num
    elif sign == '/' and knowed_idx == 0:
        return knowed_num / target
    elif sign == '/' and knowed_idx == 1:
        return target * knowed_num


for node in trackback:
    human_tree_start = ALL_MONKEYS[node]
    common_parent = human_tree_start.parent

    human_tree_idx = common_parent.children.index(human_tree_start)
    # another_tree_start = next(
    #     filter(lambda monkey: monkey.name not in trackback,
    #            common_parent.children))
    another_tree_idx = 0 if human_tree_idx == 1 else 1
    another_tree_start = common_parent.children[another_tree_idx]

    if common_parent.name == 'root':
        target_value = another_tree_start.value
    else:
        target_value = reverse_job(target=target_value,
                                   knowed_num=another_tree_start.value,
                                   knowed_idx=another_tree_idx,
                                   job=common_parent.job)

print(target_value)
