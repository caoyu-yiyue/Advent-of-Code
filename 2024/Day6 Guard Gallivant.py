# %%
# import numpy as np

# %%
with open("2024/data/day6.txt", "r") as f:
    map_str = f.read().splitlines()

MAP = [list(line) for line in map_str]

# np.genfromtxt("2024/data/day6_ex.txt", delimiter=1, dtype='<U1',
# comments=None)

# %%
# Find the Guard
for idx, line in enumerate(MAP):
    if '^' in line:
        guard_idx = (idx, line.index('^'))
        break


# %%
def turn_right(current_dir_calculator) -> tuple:
    direction_calculator_order = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_calculator_idx = direction_calculator_order.index(
        current_dir_calculator)
    direction_calculator_idx = (direction_calculator_idx + 1) % 4

    return direction_calculator_order[direction_calculator_idx]


# %%
# MAP[guard_idx[0]][guard_idx[1]] = '.'
tracks = set([guard_idx])
direction_calculator = (-1, 0)
while True:
    next_x = guard_idx[0] + direction_calculator[0]
    next_y = guard_idx[1] + direction_calculator[1]
    if next_x < 0 or next_x >= len(MAP) or next_y < 0 or next_y >= len(MAP[0]):
        break

    next_item = MAP[next_x][next_y]

    if next_item == '#':
        direction_calculator = turn_right(direction_calculator)
    elif next_item == '.' or next_item == '^':
        guard_idx = (next_x, next_y)
        tracks.add(guard_idx)

    # print(guard_idx, direction_calculator)

print(len(tracks))
