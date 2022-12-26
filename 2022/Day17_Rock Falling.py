"""
Advent of Code 2022 / Day 17
url: https://adventofcode.com/2022/day/17
"""

# %%
import numpy as np

# import matplotlib.pyplot as plt


# %%
class Rock:
    # 0: horizontal, 1: cross, 2: L, 3: vertical: 4: square.

    def __init__(self, type: int, left: int, bottom: int) -> None:
        self.type = type
        creator = self.rock_creator(type)
        self.entity = np.array(creator(left, bottom))

    @staticmethod
    def horizontal_rock(left, bottom) -> list[list]:
        return [[left + x, bottom] for x in range(4)]

    @staticmethod
    def cross_rock(left, bottom) -> list[list]:
        return [[left, bottom + 1], [left + 1, bottom], [left + 1, bottom + 1],
                [left + 1, bottom + 2], [left + 2, bottom + 1]]

    @staticmethod
    def l_rock(left, bottom) -> list[list]:
        return [[left, bottom], [left + 1, bottom], [left + 2, bottom],
                [left + 2, bottom + 1], [left + 2, bottom + 2]]

    @staticmethod
    def vertical_rock(left, bottom) -> list[list]:
        return [[left, bottom + x] for x in range(4)]

    @staticmethod
    def square_rock(left, bottom) -> list[list]:
        return [[left, bottom], [left, bottom + 1], [left + 1, bottom],
                [left + 1, bottom + 1]]

    def __repr__(self) -> str:
        return f"{self.entity}"

    def rock_creator(self, type: int):
        creators = {
            0: self.horizontal_rock,
            1: self.cross_rock,
            2: self.l_rock,
            3: self.vertical_rock,
            4: self.square_rock
        }
        return creators[type]

    @staticmethod
    def _is_itercect(arr1, arr2) -> bool:
        # https://stackoverflow.com/questions/8317022/get-intersecting-rows-across-two-2d-numpy-arrays
        _, ncols = arr1.shape
        dtype = {
            'names': ['f{}'.format(i) for i in range(ncols)],
            'formats': ncols * [arr1.dtype]
        }
        C = np.intersect1d(arr1.view(dtype), arr2.view(dtype))

        if C.shape == (0, ):
            return False
        else:
            return True

    def move_left(self, blocks) -> None:
        # print('left')
        left_edge = self.entity[:, 0].min()
        if left_edge <= 0:
            return

        entity_plan = self.entity + [-1, 0]
        if not self._is_itercect(entity_plan, blocks):
            self.entity = entity_plan

    def move_right(self, blocks) -> None:
        # print('right')
        right_edge = self.entity[:, 0].max()
        if right_edge >= 6:
            return
        entity_plan = self.entity + [1, 0]
        if not self._is_itercect(entity_plan, blocks):
            self.entity = entity_plan

    def _move_down(self, floor: np.ndarray, blocks: np.ndarray) -> None:
        # Subtract coord first.
        entity_plan = self.entity + [0, -1]

        # Find the floor under the rock entity.
        entity_h_positions = self.entity[:, 0]
        floor_under = floor[entity_h_positions]

        # If the bottom of the entity less or equal the floor under it?
        if (entity_plan[:, 1] > floor_under).all():
            self.entity = entity_plan
            # print('down')
            return None
        else:
            # floor higher than the rock, settlement, update blocks.
            # print('settle')

            # x_unique, y_maxes = group_max(id=self.entity[:, 0],
            #                               data=self.entity[:, 1])
            # floor[x_unique] = y_maxes

            blocks = np.concatenate([blocks, self.entity])
            return blocks

    def move_down(self, blocks):
        entity_plan = self.entity + [0, -1]
        if not self._is_itercect(entity_plan, blocks):
            self.entity = entity_plan
        else:
            blocks = np.concatenate([blocks, self.entity])
            return blocks


def group_max(id: np.ndarray, data: np.ndarray):
    # https://stackoverflow.com/questions/8623047/group-by-max-or-min-in-a-numpy-array
    ndx = np.lexsort(keys=(data, id))
    id, data = id[ndx], data[ndx]
    y_maxes = data[np.r_[np.diff(id), True].astype(bool)]
    return np.unique(id), y_maxes


def cal_floor(blocks) -> np.ndarray:
    _, floor = group_max(blocks[:, 0], blocks[:, 1])
    return floor


def clear_blocks(blocks):
    max_per_col = cal_floor(blocks)
    min_line = max_per_col.min()

    new_blocks = blocks[blocks[:, 1] >= min_line - 3]

    return new_blocks


# def is_pattern(blocks):
#     height = blocks[:, 1].max()
#     first_half: np.ndarray = blocks[:(height / 2)]
#     second_half: np.ndarray = blocks[(height / 2) + 1] - [0, height / 2]

#     return np.array_equal(first_half, second_half)


# def is_pattern_for0()


# %%
def part1():
    rocks_types = list(range(5))
    with open('data/day17_ex.txt') as f:
        jets = f.read().strip()

    blocks = np.array([[x, -1] for x in range(7)])
    # floor = np.array([-1] * 7)
    jet_count = 0
    for i in range(2022):
        # if i % 5 == 5 and is_pattern(blocks):
        #     print('find_parten')
        #     return i, blocks[:, 1].max() + 1

        # floor = cal_floor(blocks)
        # print(floor)
        type = rocks_types[i % 5]
        rock = Rock(type=type, left=2, bottom=blocks[:, 1].max() + 4)

        new_blocks = None
        # move_count = 0
        while new_blocks is None:
            # move_count += 1
            jet = jets[jet_count % len(jets)]
            if jet == '<':
                rock.move_left(blocks)
            elif jet == '>':
                rock.move_right(blocks)
            jet_count += 1

            new_blocks = rock.move_down(blocks=blocks)
            # print('Loop End.', i, move_count)

        blocks = clear_blocks(new_blocks)
        print(i)

    # print('Final: ', blocks)
    return blocks


blocks = part1()
print(blocks[:, 1].max() + 1)

# Too High: 3169
# Right: 3147

# %%
# plt.scatter(*zip(*blocks))


# %%
# Part 2
def cal_tops(blocks):
    max_per_col = cal_floor(blocks)
    min_line = max_per_col.min()

    return max_per_col - min_line


def part2():
    rocks_types = list(range(5))
    with open('data/day17.txt') as f:
        jets = f.read().strip()

    blocks = np.array([[x, -1] for x in range(7)])
    heights = []
    # floor = np.array([-1] * 7)
    jet_count = 0
    key_set = {}
    for i in range(1000000000000):
        (rock_idx) = i % 5

        # floor = cal_floor(blocks)
        # print(floor)
        type = rocks_types[(rock_idx)]
        rock = Rock(type=type, left=2, bottom=blocks[:, 1].max() + 4)

        new_blocks = None
        # move_count = 0
        while new_blocks is None:
            # move_count += 1
            jet_idx = jet_count % len(jets)
            start_state = (rock_idx, jet_idx, *cal_tops(blocks))
            if start_state in key_set.keys():
                print('repeat_key at:', key_set[start_state])
                return i, key_set[start_state], blocks[:, 1].max() + 1, heights
            else:
                key_set[start_state] = i

            jet = jets[jet_idx]
            if jet == '<':
                rock.move_left(blocks)
            elif jet == '>':
                rock.move_right(blocks)
            jet_count += 1

            new_blocks = rock.move_down(blocks=blocks)
            # print('Loop End.', i, move_count)

        blocks = clear_blocks(new_blocks)
        blocks = new_blocks
        heights.append(blocks[:, 1].max() + 1)
        print(i)

    # print('Final: ', blocks)
    return blocks


rock, start_turn, height, heights_record = part2()
# part2()

# %%
start = start_turn
rocks = 1000000000000
cycle_len = rock - start  # How many rocks in one cycle?

initial, cycle_part = heights_record[:start], heights_record[start:]

cycles = (rocks - start) // cycle_len  # How many cycles in all the rocks.
cycle_height = height - heights_record[start - 1]

remain_length = rocks - cycles * cycle_len - (start - 1)
height_deltas = np.diff(heights_record)

cycles * cycle_height + heights_record[start - 1] + (
    heights_record[start + remain_length - 1] - heights_record[start - 1]) - 1
# sum(height_deltas[start + 1:remain_length + 1])
