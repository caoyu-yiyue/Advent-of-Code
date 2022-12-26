"""
Advent of Code 2022 / Day 10
url: https://adventofcode.com/2022/day/10
"""

# %%
import numpy as np


# %%
def parse_instruction(instruction: str):
    if instruction == 'noop':
        return [0]
    else:
        v = instruction.split(' ')[1]
        return [0, int(v)]


# %%
with open('data/day10.txt', 'r') as f:
    instructions = f.read().splitlines()

value_at_cycle_end = [1]

for instruction in instructions:
    value_at_cycle_end += parse_instruction(instruction)

# %%
values_array = np.array(value_at_cycle_end)
x_during = values_array.cumsum()[:-1]
idx_array = np.arange(1, len(x_during) + 1)

# %%
signal_strengths = x_during * idx_array
interesting_signals = []
for i in range(19, 220, 40):
    # print(signal_strengths[i])
    interesting_signals.append(signal_strengths[i])

print(sum(interesting_signals))

# %%
# Part 2
crt_marks = []
for idx, x_val in enumerate(x_during):
    # Index in current row.
    idx_in_row = idx % 40

    if idx_in_row >= (x_val - 1) and idx_in_row <= (x_val + 1):
        crt_marks.append('🌚')
    else:
        crt_marks.append('🌕')

marks_grid = np.array(crt_marks).reshape((6, 40))
np.apply_along_axis(lambda x: ''.join(x), axis=1, arr=marks_grid)
