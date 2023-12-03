"""
Advent of Code 2023 / Day 2
url: https://adventofcode.com/2023/day/2
"""
# %%
import re

# %%
# CUBE_NUMS = {'red': 12, 'green': 13, 'blue': 14}
CUBE_NUMS = [12, 13, 14]

# Part 1
with open('data/day2.txt', 'r') as f:
    games = f.readlines()

# %%
red_regex = re.compile(r'(\d+) red')
green_regex = re.compile(r'(\d+) green')
blue_regex = re.compile(r'(\d+) blue')
color_regexes = [red_regex, green_regex, blue_regex]

# %%
possible_games: set = set(range(1, len(games) + 1))

# %%
# For every game, test if the game is possible.
for game_order, game_str in enumerate(games, start=1):
    # For every color, find the counts encoured in this game.
    for color_order, color_regex in enumerate(color_regexes):
        color_counts_str = color_regex.findall(game_str)
        # If any of the number larger than the stocks, drop the game order in
        # the game.
        if any(
                map(lambda count_str: int(count_str) > CUBE_NUMS[color_order],
                    color_counts_str)):
            possible_games.remove(game_order)
            break
    continue
# ================================================================================
# Part 2

# %%
power_sum = 0
for game_str in games:
    power = 1
    for color_regex in color_regexes:
        color_counts_str = color_regex.findall(game_str)

        # If any color found 0, then the power is 0, and don't need to add it
        # to sum.
        if len(color_counts_str) == 0:
            continue

        # the max of one color is the min of the needed.
        color_needed = max(
            map(lambda count_str: int(count_str), color_counts_str))
        power *= color_needed

    power_sum += power

print('Part 2 Answer: power_sum.')
# 86400 too high.
