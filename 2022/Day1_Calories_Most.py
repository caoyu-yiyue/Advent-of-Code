"""
Advent of Code 2022 / Day 1
url: https://adventofcode.com/2022/day/1
"""

# %%
import re

# %%
with open('data/day1.txt', 'r') as f:
    input = f.read().strip()

# %%
# Split data by blank line.
chuncks = re.split(r'\n\n', input)


# %%
# Split every item.
def split_item(txt) -> None:
    txt_items = re.split(r'\n', txt)
    return list(map(int, txt_items))


int_chuncks = list(map(split_item, chuncks))

# %%
# Sum every chunck.
value_sums = list(map(sum, int_chuncks))
max(value_sums)

# %%
# Sum of top 3.
value_sums.sort(reverse=True)

sum(value_sums[:3])
