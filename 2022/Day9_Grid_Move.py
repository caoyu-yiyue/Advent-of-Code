"""
Advent of Code 2022 / Day 9
url: https://adventofcode.com/2022/day/9
"""

# %%
import matplotlib.pyplot as plt

# %%
with open('data/day9.txt', 'r') as f:
    commands = f.read().splitlines()


# %%
def move_head(start_coord: list[int, int], command: str) -> list[int, int]:
    direction, steps = command.split(' ')
    steps = int(steps)

    if not isinstance(start_coord, list):
        start_coord = list(start_coord)

    if direction == 'L':
        start_coord[0] -= steps
    elif direction == 'R':
        start_coord[0] += steps
    elif direction == 'U':
        start_coord[1] += steps
    elif direction == 'D':
        start_coord[1] -= steps

    return tuple(start_coord)


# %%
def track_head(current_tail_coord: tuple[int, int], head_coord: tuple[int,
                                                                      int]):

    tail_tracks = []

    tail_tracks.append(current_tail_coord)

    x_head, y_head = head_coord
    x_tail, y_tail = current_tail_coord

    x_move_direction = 1 if x_head >= x_tail else -1
    y_move_direction = 1 if y_head >= y_tail else -1

    while abs(x_head - x_tail) > 1 or abs(y_head - y_tail) > 1:
        if abs(x_head - x_tail) > 0:
            x_tail += x_move_direction
        if abs(y_head - y_tail) > 0:
            y_tail += y_move_direction

        tail_tracks.append((x_tail, y_tail))

    return tail_tracks, (x_tail, y_tail)


# assert track_head((0, 0), head_coord=(0, 2)) == {(0, 0), (0, 1)}
track_head((0, 0), head_coord=(1, 3))

# %%
head_coord = (0, 0)
tail_coord = (0, 0)
all_tail_tracks = []

for command in commands:
    head_coord = move_head(head_coord, command)
    tracks_1_command, tail_coord = track_head(tail_coord, head_coord)
    all_tail_tracks += (tracks_1_command)

len(all_tail_tracks)


# %%
# Part 2
def move_long_rope(commands) -> int:
    # knots_per_command = []
    knots = [(0, 0)] * 10
    all_tracks_of_last = set()

    for command in commands:
        # Get the head coordinate after command
        knots[0] = move_head(knots[0], command)

        # Calculate the second knot's track.
        second_tracks, second_knot_coord = track_head(
            current_tail_coord=knots[1], head_coord=knots[0])
        forward_tracks = second_tracks
        knots[1] = second_knot_coord

        for i in range(1, len(knots) - 1):
            # Get the knot coord of the backward one.
            backward_coord = knots[i + 1]

            # The backward knot will track the forward's every step.
            backward_tracks = []
            for forward_coord in forward_tracks:
                _, backward_coord = track_head(
                    current_tail_coord=backward_coord,
                    head_coord=forward_coord)
                backward_tracks.append(backward_coord)

                # If new backward_coord didn't change,
                # then not need to track more.
                if backward_tracks and backward_coord == backward_coord[-1]:
                    break

            # Update coord of backward_knot.
            knots[i + 1] = backward_coord
            forward_tracks = backward_tracks

            if i == len(knots) - 2:
                # Add record to the result when we get to the last pair.
                all_tracks_of_last.update(backward_tracks)
                # knots_per_command.append(knots.copy())

            if backward_coord == knots[i]:
                # Means if the new calculated backward coordinate didn't
                # update, then the follows will not update too.
                break

        # print(command, knots)

    return all_tracks_of_last


last_tracks = move_long_rope(commands)
len(last_tracks)

# %%
plt.scatter(*zip(*last_tracks))
plt.grid()
