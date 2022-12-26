"""
Advent of Code 2022 / Day 24
url: https://adventofcode.com/2022/day/24
"""

# %%
import copy
from collections import Counter, deque

import numpy as np


def _add_coord(coord, offset) -> tuple[int, int]:
    return tuple([sum(pair) for pair in zip(coord, offset)])
# %%


class Blizzard:

    def __init__(self, direction, position) -> None:
        self.direction = direction
        self.position = position

    def move_1step(self, valley) -> tuple[int, int]:
        offsets = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}
        nxt_pnt = _add_coord(self.position, offsets[self.direction])

        if nxt_pnt[0] in {0, (valley.height - 1)}:
            nxt_pnt = (valley.height - 1 - self.position[0], nxt_pnt[1])
        if nxt_pnt[1] in {0, (valley.width - 1)}:
            nxt_pnt = (nxt_pnt[0], valley.width - 1 - self.position[1])

        self.position = nxt_pnt
        return nxt_pnt


class Valley:

    def __init__(self, input_path) -> None:
        self.blizzards = []
        self.blz_poses = []
        self.width = None
        self.height = None
        self.read_input(input_path)
        self.entrance = (0, 1)
        self.exit = (self.height - 1, self.width - 2)

    def read_input(self, input_path) -> None:
        with open(input_path) as f:
            input_lines = f.read().splitlines()

        self.height = len(input_lines)
        self.width = len(input_lines[0])
        for row, line in enumerate(input_lines[1:-1]):
            for col, char in enumerate(line):
                if char in {'>', '<', 'v', '^'}:
                    self.blz_poses.append((row + 1, col))
                    blizzard = Blizzard(char, (row + 1, col))
                    self.blizzards.append(blizzard)

    def update(self) -> None:
        self.blz_poses.clear()
        for blizzard in self.blizzards:
            blz_pos = blizzard.move_1step(valley=self)
            self.blz_poses.append(blz_pos)

    def plot_valley(self, travler=None):

        map_a = np.full((self.height, self.width), '.')
        for slice in [np.s_[0], np.s_[-1], np.s_[:, 0], np.s_[:, -1]]:
            map_a[slice] = '#'
        map_a[*self.entrance] = '.'
        map_a[*self.exit] = '.'

        pos_counters = Counter(self.blz_poses)
        for bliz in self.blizzards:
            pos = bliz.position
            if pos_counters[pos] >= 2:
                map_a[*pos] = pos_counters[pos]
            else:
                map_a[*pos] = bliz.direction

        if travler is not None:
            if map_a[*travler.position] != '.':
                raise ValueError('Travler on blizzard.')

            map_a[*travler.position] = 'E'

        print('\n'.join(''.join(row) for row in map_a))


class Travler:

    def __init__(self) -> None:
        self.position = (0, 1)
        self.step = 0

    def move(self, next_time_valley: Valley):
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        potential_pnts = []
        for offset in offsets:
            nxt_pnt = _add_coord(self.position, offset)
            if self._in_range(nxt_pnt, next_time_valley) and \
                    nxt_pnt not in set(next_time_valley.blz_poses):
                new_travler = copy.deepcopy(self)
                new_travler.step += 1
                new_travler.position = nxt_pnt
                potential_pnts.append(new_travler)
        if not potential_pnts:
            self.step += 1
            potential_pnts.append(self)

        return potential_pnts

    def _in_range(self, pnt, valley):
        row_range = range(1, valley.height - 1)
        col_range = range(1, valley.width - 1)

        return (pnt[0] in row_range) and (pnt[1] in col_range) or \
            pnt == valley.exit or pnt == valley.entrance

    def deaded(self, valley):
        if self.position in set(valley.blz_poses):
            return True
        else:
            return False


# %%
def cal_distance(valley_tralver):
    valley, travler = valley_tralver
    return (valley.exit[0] - travler.position[0]) + \
        (valley.exit[1] - travler.position[1])


def process_state(valley, travler):
    process_queue = [travler]
    min_steps = np.inf
    visited = set()
    max_dist = -1

    stop = False
    while process_queue and not stop:
        travler = process_queue.pop(0)

        if travler.step > max_dist:
            max_dist = travler.step
            valley.update()

        travlers = travler.move(valley)

        for travler in travlers:
            # print('=====================')
            # print('time: ', travler.step)

            # Check if key is in visited.
            key = (*travler.position, travler.step)
            if key in visited:
                continue
            else:
                visited.add(key)

            if travler.deaded(valley):
                continue
            print(cal_distance((valley, travler)))
            # valley.plot_valley(travler)
            if travler.position == valley.exit or travler.step > min_steps:
                min_steps = min(travler.step, min_steps)
                stop = True
            else:
                process_queue.append(travler)

            # process_queue.sort(key=cal_distance)
            # process_queue = process_queue[:1000]

    return min_steps


def process_state2(valley, start_pnt, end_pnt):
    visited = set()
    max_dist = -1

    # pnt = (0, 1)
    time = 0
    process_queue = deque([(start_pnt, time)])

    while process_queue:
        pnt, time = process_queue.popleft()

        if time % 50 == 0:
            print(pnt, time)

        # print(cal_distance(pnt, valley.exit))
        if pnt == end_pnt:
            print(time)
            return time, valley

        key = (*pnt, time)
        if key in visited:
            continue

        if time > max_dist:
            max_dist = time
            valley.update()

        for offset in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)):
            nx = _add_coord(pnt, offset)
            if nx not in set(valley.blz_poses) and \
                    nx[0] in range(1, valley.height - 1) and \
                    nx[1] in range(1, valley.width - 1) or \
                    nx == valley.exit or nx == valley.entrance:
                visited.add((*pnt, time))
                process_queue.append((nx, time + 1))


# %%
valley = Valley('data/day24ex.txt')
travler = Travler()

time1, valley_1 = process_state2(
    valley, start_pnt=(0, 1), end_pnt=valley.exit)

# Too high: 548
# Too high: 495

# %%
# Part 2
time2, valley_2 = process_state2(
    valley_1, start_pnt=valley.exit, end_pnt=valley.entrance)
time3, _ = process_state2(valley_2, start_pnt=(0, 1), end_pnt=valley.exit)
print(time1 + time2 + time3 + 2)

# %%
# valley = Valley('data/day24ex.txt')
# travler = Travler()
# valley.plot_valley(travler)
# print('===================')

# for i in range(18):
#     print('time: ', i + 1)
#     valley.update()
#     travler.move(valley)
#     valley.plot_valley(travler)
#     print('===================')
