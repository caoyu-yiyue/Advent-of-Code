"""
Advent of Code 2022 / Day 23
url: https://adventofcode.com/2022/day/23
"""

# %%
from collections import deque, Counter
from operator import itemgetter
from itertools import product

from matplotlib import pyplot as plt

# %%


class Elf:
    DIRECTIONS = deque(['N', 'S', 'W', 'E'])
    OFFSETS = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1),
               'NW': (-1, -1), 'NE': (-1, 1), 'SW': (1, -1), 'SE': (1, 1)}

    def __init__(self, position) -> None:
        self.position = position
        self.willing_pos = None

    def __repr__(self) -> str:
        return f'{self.position}'

    @staticmethod
    def _add_coord(coord, offset) -> tuple[int, int]:
        return tuple([sum(pair) for pair in zip(coord, offset)])

    @classmethod
    def shift_directions(cls) -> None:
        cls.DIRECTIONS.rotate(-1)

    @classmethod
    def reset_directions(cls) -> None:
        cls.DIRECTIONS = deque(['N', 'S', 'W', 'E'])

    def decide_direction(self, current_poses) -> tuple[int, int]:
        # In the order of directions, decide the direction it can move.
        for direc in self.DIRECTIONS:
            if (willing_pos :=
                    self._check_direction(direc, current_poses)) is not None:
                self.willing_pos = willing_pos
                return self.willing_pos

    def _check_direction(self, direction: str, current_poses: set):
        neighbors = [self._add_coord(self.position, offset)
                     for offset in self.OFFSETS.values()]

        # Don't move if the point is not crowed.
        if not (set(neighbors) & current_poses):
            return None

        match direction:
            case 'N':
                if not set(itemgetter(0, 4, 5)(neighbors)) & current_poses:
                    return neighbors[0]
            case 'S':
                if not set(itemgetter(1, 6, 7)(neighbors)) & current_poses:
                    return neighbors[1]
            case 'W':
                if not set(itemgetter(2, 4, 6)(neighbors)) & current_poses:
                    return neighbors[2]
            case 'E':
                if not set(itemgetter(3, 5, 7)(neighbors)) & current_poses:
                    return neighbors[3]

    def move(self, willings_counter: Counter):
        # If no willing poses same, move.
        if self.willing_pos is not None:
            if willings_counter[self.willing_pos] == 1:
                self.position = self.willing_pos
            self.willing_pos = None

        return self.position


class Ground:

    def __init__(self, path) -> None:
        self.current_positions = set()
        self.elves = set()
        self.round = 0
        self._load_input(path)

    def _load_input(self, path) -> None:
        with open(path) as f:
            lines = f.read().splitlines()

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '#':
                    self.current_positions.add((row, col))
                    elf = Elf(position=(row, col))
                    self.elves.add(elf)

    def _collect_willings(self) -> Counter:
        willings = [elf.decide_direction(
            self.current_positions) for elf in self.elves]
        willings_counter = Counter(willings)

        return willings_counter

    def _move_elves(self, willings_counter) -> None:
        new_positions = {elf.move(willings_counter) for elf in self.elves}
        self.current_positions = new_positions
        self.round += 1

    def start_a_round(self) -> None:
        willings_counter = self._collect_willings()
        if set(willings_counter.keys()) == set([None]):
            print(f'stable at the {self.round + 1} round.')
            return self.round + 1
        self._move_elves(willings_counter)

    def cal_rectangle(self) -> int:
        min_row_col = map(min, zip(*self.current_positions))
        max_row_col = map(max, zip(*self.current_positions))

        ranges = map(lambda min_max: range(
            min_max[0], min_max[1] + 1), zip(min_row_col, max_row_col))

        all_idxes = set(product(*ranges))
        return len(all_idxes - self.current_positions)

    def plot_elves(self) -> None:
        fig, ax = plt.subplots(1, 1)
        x_y = list(zip(*self.current_positions))
        ax.scatter(x=x_y[1], y=x_y[0], marker='s', s=128)
        ax.invert_yaxis()
        plt.show()


# %%
ground = Ground(path='data/day23.txt')
Elf.reset_directions()

# %%
for i in range(10):
    print(i)
    ground.start_a_round()
    # ground.plot_elves()
    Elf.shift_directions()
ground.cal_rectangle()

# Too high: 3844

# %%
# Part 2
ground2 = Ground(path='data/day23.txt')
Elf.reset_directions()

stop_round = None
while stop_round is None:
    stop_round = ground2.start_a_round()
    Elf.shift_directions()
