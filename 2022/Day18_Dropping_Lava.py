"""
Advent of Code 2022 / Day 18
url: https://adventofcode.com/2022/day/18
"""

# %%
from itertools import product
from collections import deque, defaultdict

# %%
with open('data/day18.txt') as f:
    INPUT_LINES = f.read().splitlines()


# %%
# Part 1
def part1():
    space_record = defaultdict(lambda: False)
    total_sides = 0

    offsets = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1),
               (0, 0, 1)]
    for line in INPUT_LINES:
        idx = tuple(map(int, line.split(',')))
        space_record[idx] = True
        total_sides += 6
        for offset in offsets:
            adjacent_idx = tuple(sum(x) for x in zip(idx, offset))
            if space_record[adjacent_idx]:
                total_sides -= 2
            else:
                continue

    print('Total Sides:', total_sides)
    return total_sides, space_record


total_sides, space_record = part1()


# Another Method
def find_neighbors(idx):
    x, y, z = idx
    return {(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z),
            (x, y, z - 1), (x, y, z + 1)}


lava_idxs = set(map(lambda line: eval(line), INPUT_LINES))

# 面积就是空着的临近数量。
# Area is the empty neighbors' number
sum(len(find_neighbors(lava) - lava_idxs) for lava in lava_idxs)

# %%
# Part 2
coord_mins = tuple(map(min, zip(*lava_idxs)))
coord_maxs = tuple(map(max, zip(*lava_idxs)))

xyz_ranges = list(
    map(lambda min_max: range(min_max[0] - 1, min_max[1] + 2),
        zip(coord_mins, coord_maxs)))

all_idxs = set(product(*xyz_ranges))
air_idxs: set = all_idxs - lava_idxs

# %%
steam = set()
processing_queue = deque([(coord_mins[0] - 1, coord_mins[1] - 1,
                           coord_mins[2] - 1)])

# processing_queue = deque([coord_mins])
while processing_queue:
    node = processing_queue.pop()
    steam.add(node)
    # Find neighbors who are air.
    neighbors = find_neighbors(node) & air_idxs
    # Add air neighbor into the processing_queue to wait processing.
    processing_queue.extend(neighbors - steam)

# 因为从第一个界外的空气（蒸汽）开始，寻找是空气的临近值，所以不会穿过实体方块（即熔岩块儿）到达
# 内部的空气块儿。故而可以便利所有能联通的外部空气。

# Now we have the steam blocks.
sides = 0
for lava in lava_idxs:
    # For every lava's neighbor, find the steam
    sides += len(find_neighbors(lava) & steam)
# Same As:
sum(len(find_neighbors(lava) & steam) for lava in lava_idxs)

# 因为外露面的面积就是空临近块儿的个数，而蒸汽块儿包裹着所有实体块儿的外部，即蒸汽块儿的外面积 = 所有实体块儿的外面积。
# 计算蒸汽块儿的外面积即可得到所有实体块儿的外面积。

print(sides)

# %%
cubes = lava_idxs
block = {(a, b, c)
         for a in range(-1, 21) for b in range(-1, 21)
         for c in range(-1, 21)} - cubes
delta = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
def sides(x, y, z): return {(x + a, y + b, c + z) for a, b, c in delta} & block


steam = set()
nodes = deque([(-1, -1, -1)])
while nodes:
    n = nodes.pop()
    steam.add(n)
    nodes.extend(sides(*n) - steam)
print('part1', sum(len(sides(*c) - cubes) for c in cubes))
print('part2', sum(len(sides(*c) & steam) for c in cubes))
