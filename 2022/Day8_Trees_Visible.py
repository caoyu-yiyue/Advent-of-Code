"""
Advent of Code 2022 / Day 8
url: https://adventofcode.com/2022/day/8
"""

# %%
import numpy as np


# %%
tree_array = np.genfromtxt('data/day8.txt', delimiter=1, dtype='int8')

# %%
grid_shape = tree_array.shape
edge_count = grid_shape[0] * 2 + (grid_shape[1] - 2) * 2

# %%
inter_visible_count = 0
for i in range(1, grid_shape[0] - 1):
    for j in range(1, grid_shape[1] - 1):
        tree = tree_array[i, j]

        # Left
        if tree_array[i, 0:j].max() < tree:
            inter_visible_count += 1
            continue
        # Right
        if tree_array[i, (j + 1):].max() < tree:
            inter_visible_count += 1
            continue
        # Up
        if tree_array[0:i, j].max() < tree:
            inter_visible_count += 1
            continue
        # Bottom
        if tree_array[(i + 1):, j].max() < tree:
            inter_visible_count += 1
            continue

# %%
print(edge_count + inter_visible_count)

# %%
# Part 2

# %%
MAX_SCORE = 0


def update_max(score):
    global MAX_SCORE
    if score > MAX_SCORE:
        MAX_SCORE = score


def half_search(array: np.array, target, side='left'):
    if side == 'right':
        array = np.flip(array)

    searching_array = array

    # if searching_array.max() < target:
    # return searching_array.size

    while searching_array.size > 0:
        max_val = searching_array.max()
        if max_val < target:
            # If have sliced the array, the last tree has been cutted.
            # If didn't, then all the trees can be seen.
            return searching_array.size + (searching_array.size != array.size)

        max_idx = searching_array.argmax()
        searching_array = searching_array[:max_idx]

    # If the last one is also greater or equal target, can see it.
    return 1


# half_search(np.array([2, 2, 2]), target=3, side='left')

# %%
for i in range(1, grid_shape[0] - 1):
    for j in range(1, grid_shape[1] - 1):
        tree = tree_array[i, j]

        # Left
        left = half_search(tree_array[i, 0:j], target=tree, side='right')

        # Right
        right = half_search(tree_array[i, (j + 1):], target=tree, side='left')

        # Up
        up = half_search(tree_array[0:i, j], target=tree, side='right')

        # Bottom
        bottom = half_search(tree_array[(i + 1):, j], target=tree, side='left')

        tree_score = left * right * up * bottom

        update_max(tree_score)

# %%
# half_search(np.array([1, 2, 3, 1, 2, 2, 1]), target=3, side='right')
print(MAX_SCORE)
