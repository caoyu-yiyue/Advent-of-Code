"""
Advent of Code 2022 / Day 13
url: https://adventofcode.com/2022/day/13
"""

# %%
import json
from collections import deque
from functools import cmp_to_key
from typing import Literal
# import numpy as np

# %%
with open('data/day13.txt', 'r') as f:
    INPUT = f.read().split('\n\n')


# %%
def compare_simple_list(left: list, right: list) -> bool | None:
    """Compare two list without nest list."""

    left = deque(left)
    right = deque(right)

    while len(left) > 0 or len(right) > 0:
        # guard if who is run out.
        if len(left) == 0:
            return True
        if len(right) == 0:
            return False

        left_1st = left.popleft()
        right_1st = right.popleft()

        if left_1st < right_1st:
            return True
        elif left_1st > right_1st:
            return False

    return None


# %%
def compare_nested_lists(left: list, right: list) -> bool | None:
    """Compare two list without nest list."""

    left = [left] if isinstance(left, int) else left
    right = [right] if isinstance(right, int) else right

    left = deque(left)
    right = deque(right)

    result = None
    while result is None and (len(left) > 0 or len(right) > 0):
        check_result = check_and_pop(left, right)
        if isinstance(check_result, bool):
            return check_result
        else:
            left_1st, right_1st = check_result

        while isinstance(left_1st, list) or isinstance(right_1st, list):
            result = compare_nested_lists(left_1st, right_1st)

            # If find result, then return it.
            if result is not None:
                return result
            else:
                # If didn't, continue for the two queues.
                check_result = check_and_pop(left, right)
                if isinstance(check_result, bool):
                    return check_result
                else:
                    left_1st, right_1st = check_result

        if left_1st < right_1st:
            result = True
        elif left_1st > right_1st:
            result = False
        else:
            continue

    return result


def check_and_pop(left, right):
    # guard if who is run out.
    if len(left) == 0:
        return True
    if len(right) == 0:
        return False

    left_1st = left.popleft()
    right_1st = right.popleft()

    return left_1st, right_1st


# %%
# compare_nested_lists([1], [1])
l, r = [eval(line) for line in INPUT[1].splitlines()]
compare_nested_lists(l, r)

# %%
results = []
sum_of_indices = 0
for idx, packet in enumerate(INPUT):
    l, r = [eval(line) for line in packet.splitlines()]
    is_inorder = compare_nested_lists(l, r)
    if is_inorder:
        sum_of_indices += idx + 1
    results.append(is_inorder)


# %%
# Part 2
def comparator(left, right) -> Literal[-1, 1]:
    result = compare_nested_lists(left, right)
    if result:
        return -1
    else:
        return 1


# %%
with open('data/day13.txt', 'r') as f:
    INPUT_LINES = f.read().splitlines()

# %%
item_lines = [eval(line) for line in INPUT_LINES if line != '']
item_lines.extend([[[2]], [[6]]])
item_lines.sort(key=cmp_to_key(comparator))

(item_lines.index([[2]]) + 1) * (item_lines.index([[6]]) + 1)

# %%
item_lines = [json.loads(line) for line in INPUT_LINES if line != '']


# %%
# Answer from Reddit:
def in_order(l1, l2):
    if isinstance(l1, int) and isinstance(l2, int):
        if l1 == l2:
            return None
        return l1 < l2

    if isinstance(l1, list) and isinstance(l2, list):
        for e1, e2 in zip(l1, l2):
            if (comparison := in_order(e1, e2)) is not None:
                return comparison
        return in_order(len(l1), len(l2))

    if isinstance(l1, int):
        return in_order([l1], l2)
    return in_order(l1, [l2])


text = open("inputs/13", "r").read()
pairs = [[eval(l) for l in pair.splitlines()]
         for pair in text.strip().split("\n\n")]
print(
    sum(i for i, (left, right) in enumerate(pairs, 1)
        if in_order(left, right)))

packets = [p for pair in pairs for p in pair]
position_1 = 1 + sum(1 for p in packets if in_order(p, [[2]]))
position_2 = 2 + sum(1 for p in packets if in_order(p, [[6]]))
print(position_1 * position_2)
