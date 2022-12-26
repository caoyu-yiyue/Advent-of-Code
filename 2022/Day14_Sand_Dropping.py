"""
Advent of Code 2022 / Day 14
url: https://adventofcode.com/2022/day/14
"""

# %%
import re

import numpy as np
import matplotlib.pyplot as plt

# %%
# Read input
with open('data/day14.txt', 'r') as f:
    INPUT_LINES = f.read().splitlines()


# %%
# Parse Input
def _parse_endpoints(line: str) -> np.array:
    """Input a line and return a array of endpoints."""
    coord_regex = re.compile(r'(\d+),(\d+)')
    endpoints = coord_regex.findall(line)
    endpoints_array = np.array(endpoints, dtype='int16')

    return endpoints_array


# %%
# Parse Path
def _fill_line(pnt1: np.array, pnt2: np.array) -> np.array:
    num = abs((pnt1 - pnt2)).max() + 1
    return np.linspace(pnt1, pnt2, num=num, endpoint=True, dtype='int16')


def _find_rocks_in_path(endpoints: np.array) -> np.array:
    lines = []
    for idx in range(len(endpoints) - 1):
        line = _fill_line(endpoints[idx], endpoints[idx + 1])
        lines.append(line)

    return np.unique(np.concatenate(lines), axis=0)


# %%
# Parse Map
def find_all_rocks(input_lines):
    paths = []
    for line in input_lines:
        endpoints = _parse_endpoints(line)
        one_path = _find_rocks_in_path(endpoints=endpoints)
        paths.append(one_path)

    return np.unique(np.concatenate(paths), axis=0)


all_rocks = find_all_rocks(INPUT_LINES)

# %%
# Visilization.
plt.scatter(*zip(*all_rocks))
plt.gca().invert_yaxis()


# %%
# Find outline.
def find_two_bottom(rocks: np.array):
    min_x = rocks[:, 0].min()

    # left_top = np.array([min_x, 0])
    right_bottom = rocks.max(axis=0)
    left_bottom = np.array([min_x, right_bottom[1]])

    return left_bottom, right_bottom


left_bottom, right_bottom = find_two_bottom(all_rocks)


# %%
def in_range(pnt: list, lb, rb):
    if not isinstance(pnt, np.ndarray):
        pnt = np.array(pnt)

    if pnt[0] < lb[0] and pnt[1] > lb[1]:
        print('Out of left bottom.')
        return False

    if (pnt > rb).all():
        print('Out of right bottom.')
        return False

    return True


# %%
# Simulate the Sand.
# A list for checking blocks.
blocks = all_rocks.tolist()
START_PNT = [500, 0]

pnt = START_PNT
set_count = 0

while in_range(pnt, left_bottom, right_bottom):
    next_pnt = [pnt[0], pnt[1] + 1]

    if next_pnt in blocks:
        next_pnt = [pnt[0] - 1, pnt[1] + 1]

    if next_pnt in blocks:
        next_pnt = [pnt[0] + 1, pnt[1] + 1]

    if next_pnt in blocks:
        # Set it
        set_count += 1
        blocks.append(pnt)
        pnt = START_PNT
        continue

    pnt = next_pnt

# %%
# Visualization.
plt.scatter(*zip(*all_rocks))
plt.gca().invert_yaxis()

plt.scatter(*zip(*blocks[all_rocks.shape[0]:]))

# %%
# ================================================================================
# Part 2
# ================================================================================
floor_y = left_bottom[1] + 2
BLOCKS = set(map(tuple, all_rocks))
START_PNT = np.array([500, 0])


def is_floor(pnt, floor_y):
    if pnt[1] == floor_y:
        return True

    return False


def is_block(pnt: np.ndarray) -> bool:
    global BLOCKS
    if tuple(pnt) in BLOCKS:
        return True


def add_to_blocks(pnt: np.ndarray) -> bool:
    global BLOCKS
    BLOCKS.add(tuple(pnt))


# %%
pnt = START_PNT
set_count = 0
while True:
    next_pnt = pnt + [0, 1]

    if is_floor(next_pnt, floor_y):
        # Set it
        set_count += 1
        add_to_blocks(pnt)
        pnt = START_PNT
        continue

    if is_block(next_pnt):
        next_pnt = pnt + [-1, 1]

    if is_block(next_pnt):
        next_pnt = pnt + [1, 1]

    if is_block(next_pnt):
        # Set it
        set_count += 1
        add_to_blocks(pnt)

        # If it is setted and the pnt is the Start Pnt, stop.
        if (pnt == START_PNT).all():
            break

        pnt = START_PNT
        continue

    pnt = next_pnt

print(set_count)

print(len(BLOCKS) - len(all_rocks))

# %%
# Visualization.
plt.scatter(*zip(*BLOCKS))
plt.scatter(*zip(*all_rocks))
plt.gca().invert_yaxis()
