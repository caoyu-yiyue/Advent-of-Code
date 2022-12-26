"""
Advent of Code 2022 / Day 22
url: https://adventofcode.com/2022/day/22
"""

# %%
import re
from collections import defaultdict

import numpy as np

# %%
with open('data/day22.txt', 'r') as f:
    input = f.read()

map_str, commands_str = input.split('\n\n')

# %%
board_map = defaultdict(lambda: None)
board_lines = map_str.splitlines()

# %%
width = max(map(len, board_lines))
height = len(board_lines)

lines_padding = list(map(lambda str: list(str.ljust(width)), board_lines))
board_map = np.array(lines_padding)


# %%
class Person():

    def __init__(self, board_map) -> None:
        # 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
        self.facing = 0
        self.position = None
        self.find_start_position(board_map)

    def find_start_position(self, board_map: np.ndarray) -> None:
        first_line = board_map[0]
        pos = np.where(first_line == '.')
        self.position = np.array([0, pos[0][0]])

    def cal_result(self):
        return (self.position[0] + 1) * 1000 + (self.position[1] + 1) * 4 + \
            self.facing

    def turn(self, order: str) -> None:
        if order == 'R':
            self.facing = (self.facing + 1) % 4
        if order == 'L':
            self.facing = (self.facing - 1) % 4

    def go_to_next_position(self, board_map, steps):
        map_shape = board_map.shape
        row_range = range(0, map_shape[0])
        col_range = range(0, map_shape[1])

        adders = {0: [0, 1], 1: [1, 0], 2: [0, -1], 3: [-1, 0]}
        adder = adders[self.facing]

        for s in range(steps):
            nxt_pos = self.position + adder
            # If outranged.
            if nxt_pos[1] not in col_range or nxt_pos[0] not in row_range or \
               board_map[*nxt_pos] == ' ':
                # horizentaly out.
                current_row_idx = self.position[0]
                current_row = board_map[current_row_idx]
                solid_items = np.where(current_row != ' ')
                if self.facing == 0:
                    # Facing right.
                    nxt_pos = np.array([current_row_idx, solid_items[0][0]])
                if self.facing == 2:
                    # Facing left.
                    nxt_pos = np.array([current_row_idx, solid_items[0][-1]])

                # Vertically out.
                current_col_idx = self.position[1]
                current_col = board_map[:, current_col_idx]
                solid_items = np.where(current_col != ' ')
                if self.facing == 1:
                    # Facing down.
                    nxt_pos = np.array([solid_items[0][0], current_col_idx])
                if self.facing == 3:
                    # Facing up.
                    nxt_pos = np.array([solid_items[0][-1], current_col_idx])

            # If is wall.
            if board_map[*nxt_pos] == '#':
                break

            # If all tile.
            self.position = nxt_pos

            # print(self.position)


# %%
person = Person(board_map=board_map)
# person.go_to_next_position(board_map, steps=10)

# %%
commands = re.findall(r'\d+|[RL]', commands_str)

# for command in commands:
#     if command.isdigit():
#         # print('Moving: ', command)
#         person.go_to_next_position(board_map, steps=int(command))
#     elif command.isalpha():
#         # print('Truning: ', command)
#         person.turn(command)

# %%
print(person.cal_result())

# %%
# Part 2


class PersonCube(Person):
    def find_section(self):
        if self.position[0] in range(0, 50):
            if self.position[1] in range(50, 100):
                return 1
            if self.position[1] in range(100, 150):
                return 2

        if self.position[0] in range(50, 100):
            return 3

        if self.position[0] in range(100, 150):
            if self.position[1] in range(0, 50):
                return 4
            if self.position[1] in range(50, 100):
                return 5

        if self.position[0] in range(150, 200):
            return 6

        raise ValueError('Did not find section.')

    def go_cublic(self, board_map, steps):
        map_shape = board_map.shape
        row_range = range(0, map_shape[0])
        col_range = range(0, map_shape[1])

        adders = {0: [0, 1], 1: [1, 0], 2: [0, -1], 3: [-1, 0]}

        for s in range(steps):
            adder = adders[self.facing]
            nxt_pos = self.position + adder
            # If outranged.
            if nxt_pos[1] not in col_range or nxt_pos[0] not in row_range or \
               board_map[*nxt_pos] == ' ':
                nxt_pos = self._change_pos_through_edge2(board_map)
            # If is wall.
            if board_map[*nxt_pos] == '#':
                break

            if board_map[*nxt_pos] == ' ':
                raise ValueError('Going to move out range')

            # If all tile.
            self.position = nxt_pos

            # print(self.position)

    def _change_pos_through_edge(self):
        current_pos = self.position
        section = self.find_section()

        # 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
        if section == 1:
            if current_pos[1] == 50 and self.facing == 2:
                # From section 1 Left to the section 4.
                self.facing = 0
                nxt_pos = np.array([100 + (49 - current_pos[0]), 0])
            if current_pos[0] == 0 and self.facing == 3:
                # From section 1 Up to section 6
                self.facing = 0
                nxt_pos = np.array([current_pos[1] - 50 + 150, 0])
        if section == 2:
            if current_pos[0] == 0 and self.facing == 3:
                # From section 2 Up to section 6
                nxt_pos = current_pos + [150, -100]
            if current_pos[0] == 49 and self.facing == 1:
                # From section 2 Down to section 3
                self.facing = 2
                nxt_pos = np.array([50 + (current_pos[1] - 100), 99])
            if current_pos[1] == 149 and self.facing == 0:
                # From section 2 Right to section 5.
                self.facing = 2
                nxt_pos = np.array([(49 - current_pos[0]) + 100, 99])
        if section == 3:
            if current_pos[1] == 50 and self.facing == 2:
                # From section 3 Left to section 4
                self.facing = 1
                nxt_pos = np.array([100, 99 - current_pos[0]])
            if current_pos[1] == 99 and self.facing == 0:
                # From section 3 Right to section 2
                self.facing = 3
                nxt_pos = np.array([49, 100 + (current_pos[0] - 50)])
        if section == 4:
            if current_pos[1] == 0 and self.facing == 2:
                # From section 4 Left to section 1
                self.facing = 0
                nxt_pos = np.array([149 - current_pos[0], 50])
            if current_pos[0] == 100 and self.facing == 3:
                # From 4 Up to 3
                self.facing = 0
                nxt_pos = np.array([50 + current_pos[1], 50])
        if section == 5:
            if current_pos[1] == 99 and self.facing == 0:
                # From 5 Right to 2
                self.facing = 2
                nxt_pos = np.array([149 - current_pos[0], 149])
            if current_pos[0] == 149 and self.facing == 1:
                # From 5 Down to 6
                self.facing = 2
                nxt_pos = np.array([150 + (current_pos[1] - 50), 49])
        if section == 6:
            if current_pos[1] == 0 and self.facing == 2:
                # From 6 Left to 1
                self.facing = 1
                nxt_pos = np.array([0, 50 + (current_pos[0] - 150)])
            if current_pos[1] == 49 and self.facing == 0:
                # From 6 Right to 5
                self.facing = 3
                nxt_pos = np.array([149, 50 + (current_pos[0] - 150)])
            if current_pos[0] == 199 and self.facing == 1:
                # From 6 Down to 2
                nxt_pos = np.array([0, 100 + current_pos[1]])

        return nxt_pos

    def _change_pos_through_edge2(self, board_map):
        current_pos = self.position
        section = self.find_section()

        # 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
        match section:
            case 1:
                if current_pos[1] == 50 and self.facing == 2:
                    # From section 1 Left to the section 4.
                    facing, nxt_pos = self.cross_edge(current_pos, start='1L')
                if current_pos[0] == 0 and self.facing == 3:
                    # From section 1 Up to section 6
                    facing, nxt_pos = self.cross_edge(current_pos, start='1U')
            case 2:
                if current_pos[0] == 0 and self.facing == 3:
                    # From section 2 Up to section 6
                    facing, nxt_pos = self.cross_edge(current_pos, start='2U')
                if current_pos[0] == 49 and self.facing == 1:
                    # From section 2 Down to section 3
                    facing, nxt_pos = self.cross_edge(current_pos, start='2D')
                if current_pos[1] == 149 and self.facing == 0:
                    # From section 2 Right to section 5.
                    facing, nxt_pos = self.cross_edge(current_pos, start='2R')
            case 3:
                if current_pos[1] == 50 and self.facing == 2:
                    # From section 3 Left to section 4
                    facing, nxt_pos = self.cross_edge(current_pos, start='3L')
                if current_pos[1] == 99 and self.facing == 0:
                    # From section 3 Right to section 2
                    facing, nxt_pos = self.cross_edge(current_pos, start='3R')
            case 4:
                if current_pos[1] == 0 and self.facing == 2:
                    # From section 4 Left to section 1
                    facing, nxt_pos = self.cross_edge(current_pos, start='4L')
                if current_pos[0] == 100 and self.facing == 3:
                    # From 4 Up to 3
                    facing, nxt_pos = self.cross_edge(current_pos, start='4U')
            case 5:
                if current_pos[1] == 99 and self.facing == 0:
                    # From 5 Right to 2
                    facing, nxt_pos = self.cross_edge(current_pos, start='5R')
                if current_pos[0] == 149 and self.facing == 1:
                    # From 5 Down to 6
                    facing, nxt_pos = self.cross_edge(current_pos, start='5D')
            case 6:
                if current_pos[1] == 0 and self.facing == 2:
                    # From 6 Left to 1
                    facing, nxt_pos = self.cross_edge(current_pos, start='6L')
                if current_pos[1] == 49 and self.facing == 0:
                    # From 6 Right to 5
                    facing, nxt_pos = self.cross_edge(current_pos, start='6R')
                if current_pos[0] == 199 and self.facing == 1:
                    # From 6 Down to 2
                    facing, nxt_pos = self.cross_edge(current_pos, start='6D')

        if board_map[*nxt_pos] != '#':
            self.facing = facing
        return nxt_pos

    EDGE_LINK = {'1L': {'con': '4L', 'facing': 0, 'direction': 'reverse'},
                 '1U': {'con': '6L', 'facing': 0, 'direction': 'same'},
                 '2U': {'con': '6D', 'facing': 3, 'direction': 'same'},
                 '2R': {'con': '5R', 'facing': 2, 'direction': 'reverse'},
                 '2D': {'con': '3R', 'facing': 2, 'direction': 'same'},
                 '3L': {'con': '4U', 'facing': 1, 'direction': 'same'},
                 '3R': {'con': '2D', 'facing': 3, 'direction': 'same'},
                 '4L': {'con': '1L', 'facing': 0, 'direction': 'reverse'},
                 '4U': {'con': '3L', 'facing': 0, 'direction': 'same'},
                 '5R': {'con': '2R', 'facing': 2, 'direction': 'reverse'},
                 '5D': {'con': '6R', 'facing': 2, 'direction': 'same'},
                 '6L': {'con': '1U', 'facing': 1, 'direction': 'same'},
                 '6D': {'con': '2U', 'facing': 1, 'direction': 'same'},
                 '6R': {'con': '5D', 'facing': 3, 'direction': 'same'}
                 }

    START_PNTS = {1: [0, 50], 2: [0, 100], 3: [50, 50],
                  4: [100, 0], 5: [100, 50], 6: [150, 0]}

    def _cal_len_in_section(self, section: int, edge: str, pnt: np.ndarray):
        standard_pnt = pnt - self.START_PNTS[section]
        match edge:
            case 'L' | 'R':
                return standard_pnt[0]
            case 'U' | 'D':
                return standard_pnt[1]

    def _convert_face_coord(self, to: str, length: int, direction: str):
        section = int(to[0])
        edge = to[1]
        offset = self.START_PNTS[section]

        if direction == 'reverse':
            length = 49 - length

        match edge:
            case 'L':
                return np.array([length, 0]) + offset
            case 'R':
                return np.array([length, 49]) + offset
            case 'U':
                return np.array([0, length]) + offset
            case 'D':
                return np.array([49, length]) + offset

    def cross_edge(self, pnt, start: str):
        target = self.EDGE_LINK[start]
        length = self._cal_len_in_section(
            section=int(start[0]), edge=start[1], pnt=pnt)
        to = self._convert_face_coord(
            target['con'], length, target['direction'])
        print(f'From {pnt} to {to}.')
        return target['facing'], to


# %%
person2 = PersonCube(board_map)

for command in commands:
    if command.isdigit():
        # print('Moving: ', command)
        person2.go_cublic(board_map, steps=int(command))
    elif command.isalpha():
        # print('Truning: ', command)
        person2.turn(command)

print(person2.cal_result())

# Too high: 147140
# Too high: 11562
# Wrong: 5257
