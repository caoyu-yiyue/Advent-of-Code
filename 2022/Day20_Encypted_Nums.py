"""
Advent of Code 2022 / Day 20
url: https://adventofcode.com/2022/day/20
"""

# %%
from copy import deepcopy

# %%
with open('data/day20.txt') as f:
    input = [int(n) for n in f.read().splitlines()]

# %%
# [1, 2, -3, 3, -2, 0, 4]
# [1, 2, -3, 4, 0, 3, -2]


def decrypt(input) -> list:
    counts = len(input)
    moving_list = deepcopy(input)
    active_flags = [True] * counts

    for i in range(len(input)):
        current_moving_idx = active_flags.index(True)
        print(moving_list)
        print('moving: ', moving_list[current_moving_idx])

        item = moving_list.pop(current_moving_idx)

        if item == 0:
            moving_list.insert(current_moving_idx, item)
            continue

        new_position = (current_moving_idx + item) % (counts - 1)
        if new_position == 0:
            new_position = counts
        elif new_position == counts:
            new_position = 0

        moving_list.insert(new_position, item)

        _ = active_flags.pop(current_moving_idx)
        active_flags.insert(new_position, False)

    return moving_list


# decrypt_list = decrypt(input)


# %%
def cal_coord(decrypt_list) -> int:
    zero_pos = decrypt_list.index(0)
    fisrt = decrypt_list[(1000 + zero_pos) % len(decrypt_list)]
    second = decrypt_list[(2000 + zero_pos) % len(decrypt_list)]
    third = decrypt_list[(3000 + zero_pos) % len(decrypt_list)]

    return fisrt + second + third


# cal_coord(decrypt_list)

# %%
# Part 2
decryption_key = 811589153


def find_first_idx_after(start_idx, value, list):
    for idx in range(start_idx, len(list)):
        if list[idx] == value:
            return idx


def decrypt2(input: list, times: int) -> list:
    counts = len(input)
    moving_list = deepcopy(input)
    order_list = list(range(counts))

    for time in reversed(range(1, times + 1)):
        # current_moving_idx = 0

        for i in range(len(input)):
            # current_moving_idx = find_first_idx_after(0, i, order_list)
            current_moving_idx = order_list.index(i)
            # print(moving_list)
            # print('moving: ', moving_list[current_moving_idx])

            item = moving_list.pop(current_moving_idx)

            if item == 0:
                moving_list.insert(current_moving_idx, item)
                continue

            new_position = (current_moving_idx + item) % (counts - 1)
            if new_position == 0:
                new_position = counts
            elif new_position == counts:
                new_position = 0

            moving_list.insert(new_position, item)

            o = order_list.pop(current_moving_idx)
            order_list.insert(new_position, o)

        # print('Current list: ', time, moving_list)

    return moving_list


input_multed = [num * decryption_key for num in input]
dec_list2 = decrypt2(input_multed, 10)

# %%
cal_coord(dec_list2)
