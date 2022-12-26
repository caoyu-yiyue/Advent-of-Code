"""
Advent of Code 2022 / Day 4
url: https://adventofcode.com/2022/day/4
"""

# %%
import re

# %%
with open('data/day4.txt', 'r') as f:
    section_pairs = f.read().splitlines()

# %%
pair_regex = re.compile(r'(\d+)\-(\d+)\,(\d+)\-(\d+)')

# %%
# Part 1
fully_conver_counts = 0

for pair in section_pairs:
    first_start, first_end, second_start, second_end = map(
        int,
        pair_regex.match(pair).groups())

    if first_start <= second_start and first_end >= second_end:
        fully_conver_counts += 1
    elif first_start >= second_start and first_end <= second_end:
        fully_conver_counts += 1

print(fully_conver_counts)

# %%
# Part 2
has_overlap_count = 0
for pair in section_pairs:
    # Parse numbers
    first_start, first_end, second_start, second_end = map(
        int,
        pair_regex.match(pair).groups())

    if first_end < second_start or second_end < first_start:
        continue
    else:
        has_overlap_count += 1

print(has_overlap_count)
