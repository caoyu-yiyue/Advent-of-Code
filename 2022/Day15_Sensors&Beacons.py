"""
Advent of Code 2022 / Day 15
url: https://adventofcode.com/2022/day/15
"""

# %%
# from collections import defaultdict
import re
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# %%
with open('data/day15.txt', 'r') as f:
    INPUT_LINES = f.read().splitlines()


# %%
def parse_input(lines) -> list:
    pairs = []

    for line in lines:
        coord_regex = re.compile(r'(-*\d+)')
        coord = list(map(int, coord_regex.findall(line)))
        pairs.append([(coord[0], coord[1]), (coord[2], coord[3])])

    return pairs


# %%
def man_distance(s: tuple, b: tuple) -> tuple:
    return abs(s[0] - b[0]) + abs(s[1] - b[1])


# %%
def same_dis_in_line(sensor: tuple, line: int, distance: int) -> set[int]:
    abs_x = distance - abs(sensor[1] - line)
    if abs_x >= 0:
        return set(range(sensor[0] - abs_x, sensor[0] + abs_x + 1, 1))
    else:
        return set()


# %%
# def beacons_x_in_line(pairs: list, line: int) -> set[int]:
#     return {pair[1][0] for pair in pairs if pair[1][1] == line}

# %%
if __name__ == '__main__':
    sensor_beacon_pairs = parse_input(INPUT_LINES)

    line = 2000000
    no_beacons = set()
    beacons_x_in_line = set()
    for pair in sensor_beacon_pairs:
        dist = man_distance(*pair)
        no_beacon = same_dis_in_line(sensor=pair[0], line=line, distance=dist)
        no_beacons.update(no_beacon)

        if pair[1][1] == line:
            beacons_x_in_line.add(pair[1][0])

    print(len(no_beacons - beacons_x_in_line))


# %%
# Part 2
# ================================================================================
# Code for examples, can handle samll amount of points and visualize it.
# ================================================================================
def sensor_area(sensor: tuple, beacon: tuple, largest: int):
    dist = man_distance(sensor, beacon)
    # x_range = range(sensor[0] - dist, sensor[0] + dist + 1, 1)
    y_range = range(max(sensor[1] - dist, 0),
                    min(sensor[1] + dist, largest) + 1, 1)

    area = set()
    for y in y_range:
        x_set = same_dis_in_line(sensor=sensor, line=y, distance=dist)
        pnts = {(x, y) for x in x_set if x >= 0 and x <= largest}
        area.update(pnts)

    return area


# # %%
# def sensor_area2(sensor: tuple, beacon: tuple, largest: int):
#     dist = man_distance(sensor, beacon)
#     # x_range = range(sensor[0] - dist, sensor[0] + dist + 1, 1)
#     y_range = range(max(sensor[1] - dist, 0),
#                     min(sensor[1] + dist, largest) + 1, 1)

#     area = defaultdict(lambda: set(range(largest + 1)))
#     for y in y_range:
#         x_set = same_dis_in_line(sensor=sensor, line=y, distance=dist)
#         area[y] = area[y] - x_set

#     return area

# %%
largest = 20

detected_areas = set()
for pair in sensor_beacon_pairs:
    detected_area = sensor_area(pair[0], pair[1], largest=largest)
    detected_areas.update(detected_area)

# %%
# Visualization
fig, ax = plt.subplots(1, 1)
ax.scatter(*zip(*detected_areas))
ax.invert_yaxis()
ticks = range(0, largest)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.grid(alpha=0.5)

# ================================================================================
# Code for Large Input.
# ================================================================================
# %%
largest = 4000000

pairs_num = len(sensor_beacon_pairs)

# Calculate the manhatten distance, the highest and lowset line a scanner can
# reach, and bind them to an array of sensor/beacon pairs.
dists = np.array([man_distance(s, b) for s, b in sensor_beacon_pairs])
pair_array = np.array(sensor_beacon_pairs).reshape(len(sensor_beacon_pairs), 4)
pair_array = np.hstack((pair_array, dists.reshape(pairs_num, 1),
                        (pair_array[:, 1] - dists).reshape(pairs_num, 1),
                        (pair_array[:, 1] + dists).reshape(pairs_num, 1)))


# %%
def cal_x_range(row: np.ndarray, line: int) -> tuple[int, int]:
    """Min and Max of a range for a scanner targetting to the line."""
    abs_x = row[4] - abs(row[1] - line)
    return row[0] - abs_x, row[0] + abs_x


def merge_range(left, right):
    if min(left) <= min(right) and max(left) >= max(right):
        return left
    else:
        return (min(left), max(right))


# %%
stop = False
for line_idx in tqdm(range(largest + 1)):
    respect_pairs: np.ndarray = pair_array[(pair_array[:, -2] <= line_idx)
                                           & (pair_array[:, -1] >= line_idx)]
    min_maxs = np.apply_along_axis(cal_x_range,
                                   axis=1,
                                   arr=respect_pairs,
                                   line=line_idx)
    # Sort the ranges by min value.
    min_maxs_sorted = min_maxs[min_maxs[:, 0].argsort()]

    # merge the ranges gradually.
    covered_range = min_maxs_sorted[0]
    for row_idx in range(1, min_maxs_sorted.shape[0]):

        # Stop if right value ge than largest.
        if covered_range[1] >= largest:
            break

        next_range = min_maxs_sorted[row_idx]

        if next_range[0] > (covered_range[1] + 1):
            # If next range left value - current covered > 1, there's empty.
            empty_pnt = (covered_range[1] + 1, line_idx)
            stop = True
            break

        if next_range[1] >= covered_range[1]:
            # When come here, next range left - current covered next <= 1
            # If next range value right >= covered range, then extend covered
            # range.
            covered_range[1] = next_range[1]

    if stop:
        break

print(empty_pnt)

# %%
empty_pnt[0] * 4000000 + empty_pnt[1]
