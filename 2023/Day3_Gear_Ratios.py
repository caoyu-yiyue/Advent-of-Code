"""
Advent of Code 2023 / Day 3
url: https://adventofcode.com/2023/day/3
"""

# %%
import numpy as np

# %%
with open('data/day3.txt', 'r') as f:
    # Remain the \n for avoiding numbers through lines.
    lines = f.readlines()

matrix = [[*line] for line in lines]

# %%
schematic_array: np.array = np.array(matrix)

# %%
VALID_NUMS = []
CURRENT_NUM = ''
height = schematic_array.shape[0]
width = schematic_array.shape[1]
for i in range(height):
    for j in range(width):
        current_char = schematic_array[i, j]

        if schematic_array[i, j].isnumeric():
            # If the item is a digit.
            CURRENT_NUM += current_char
        else:
            if CURRENT_NUM == '':
                # Continue if there's no number
                continue
            else:
                # Test if the number is valid, if is then append to the
                # VALID_NUMS
                i_up = max(i - 1, 0)
                i_down = min(i + 1, schematic_array.shape[0] - 1)

                j_left = max(j - len(CURRENT_NUM) - 1, 0)
                # j_right = j + 1 if j != 0 else width
                around_chars: np.array = schematic_array[i_up:(i_down + 1),
                                                         j_left:j + 1]

                flatten_list = list(around_chars.flatten())
                symbols = list(
                    filter(
                        lambda s:
                        (not s.isnumeric()) and (s != '.') and (s != '\n'),
                        flatten_list))
                if len(symbols) >= 1:
                    VALID_NUMS.append(int(CURRENT_NUM))

            CURRENT_NUM = ''

# %%
sum(VALID_NUMS)

# 542316 Too low
# 548507 Too high
# 548874 Too high
