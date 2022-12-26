"""
Advent of Code 2022 / Day 6
url: https://adventofcode.com/2022/day/6
"""

# %%
with open('data/day6.txt', 'r') as f:
    data_stream = f.read().strip()

# %%
for i in range(len(data_stream)):
    potiential_marker = set(data_stream[i:i + 4])
    if len(potiential_marker) == 4:
        break

print(i + 4)

# %%
test = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'


# %%
def count_preprocess(data_stream, diff_num: int) -> int:
    for i in range(len(data_stream)):
        potiential_marker = set(data_stream[i:i + diff_num])
        if len(potiential_marker) == diff_num:
            break

    return i + diff_num


count_preprocess(data_stream, 14)
