"""
Advent of Code 2022 / Day 5
url: https://adventofcode.com/2022/day/5
"""

# %%
import re
from collections import deque

# %%
with open('data/day5.txt', 'r') as f:
    input_str = f.read()

# %%
stacks_str, steps = input_str.split(sep='\n\n')

MOVEMENT_REGEX = re.compile(r'move (\d+) from (\d+) to (\d+)')

# %%
row_lines = stacks_str.splitlines()
line_idx = row_lines.pop(-1)


# %%
# The value index in stacks is the index of line_idx which is not space.
def parse_value_index(line_idx: str) -> range:
    for char in line_idx[::-1]:
        if char != ' ':
            lastest_col = int(char)
            return range(1, lastest_col * 4, 4)


value_idx = parse_value_index(line_idx)

# value_idx = list(
#     filter(lambda idx: line_idx[idx] != ' ', range(0, len(line_idx))))

# %%
# O(n) method: transport matrix first, loop through the value_idx,
# slice the row of values.
row_lines.reverse()
stack_tuples = [list(zip(*row_lines))[idx] for idx in value_idx]

# O(n*n) method: find the column index first, then transport the matrix.
# parsed_rows = list(map(lambda row: [row[idx] for idx in value_idx],
# row_lines))
# parsed_rows.reverse()

# list(zip(*parsed_rows))


# %%
# Convert stack data type to LifoQueue, and drop spaces.
def to_stacks(tuple: tuple) -> deque:
    stack = deque()
    for char in tuple:
        if not char.isalpha():
            break
        else:
            stack.append(char)

    return stack


stacks = list(map(to_stacks, stack_tuples))


# %%
def parse_step(step_line: str) -> tuple:
    count, start, end = MOVEMENT_REGEX.findall(step_line)[0]
    return tuple(map(int, [count, start, end]))


# %%
movements = steps.splitlines()

for movement in movements:
    count, start, end = parse_step(movement)

    for i in range(0, count):
        item = stacks[start - 1].pop()
        stacks[end - 1].append(item)

# Show result.
''.join(list(map(lambda x: x[-1], stacks)))

# %%
# Problem 2
stacks = list(map(to_stacks, stack_tuples))

for movement in movements:
    count, start, end = parse_step(movement)
    start_stack = stacks[start - 1]
    end_stack = stacks[end - 1]

    temp_stack = deque()

    # Pop the items to temp_stack, so first poped is at last.
    for i in range(0, count):
        item = start_stack.pop()
        temp_stack.append(item)

    # Pop the items to target stack, so last poped from start at last again.
    while temp_stack:
        item = temp_stack.pop()
        end_stack.append(item)

# Show result.
''.join(list(map(lambda x: x[-1], stacks)))
