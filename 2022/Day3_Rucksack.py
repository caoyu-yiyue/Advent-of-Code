"""
Advent of Code 2022 / Day 3
url: https://adventofcode.com/2022/day/3
"""

# %%
import string

# %%
with open('data/day3.txt', 'r') as f:
    rucksacks = f.read().splitlines()

# %%
priority_list = string.ascii_letters

# %%
score = 0

for items in rucksacks:

    # Get length of item in a rucksack
    item_len = len(items)

    # Split to two parts.
    first_part = set(items[:item_len // 2])
    second_part = items[item_len // 2:]

    # Find same item.
    common_type = first_part.intersection(second_part).pop()
    score += priority_list.index(common_type) + 1

print(score)

# %%
# Problem 2
score_2 = 0

for i in range(0, len(rucksacks) - 1, 3):
    first, second, third = rucksacks[i:i + 3]

    # Common of three rucksacks.
    common_type = set(first).intersection(second).intersection(third).pop()

    # Add score
    score_2 += priority_list.index(common_type) + 1

print(score_2)
