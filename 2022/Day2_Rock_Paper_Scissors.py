"""
Advent of Code 2022 / Day 2
url: https://adventofcode.com/2022/day/2
"""

# %%
with open('data/day2.txt', 'r') as f:
    strategies = f.read().splitlines()

# %%
elf_mark = {'A': 'Rock', 'B': 'Paper', 'C': 'Scissors'}
response_mark = {'X': 'Rock', 'Y': 'Paper', 'Z': 'Scissors'}

# %%
result_kinds = list(elf_mark.keys())
STRA_LEN = len(result_kinds)

# %%
# First Part
score = 0

for round in strategies:
    # Parse result.
    elf_result, resp_result = round.split(' ')

    # Parse index in strategies.
    elf_idx = result_kinds.index(elf_result)
    resp_idx = result_kinds.index(resp_result)

    if resp_idx == elf_idx:
        # print('Draw')
        score += 3
    elif (elf_idx + 1) % STRA_LEN == resp_idx:
        # Elf Lose.
        score += 6
    # elif (elf_idx + 2) % STRA_LEN == resp_idx:
    # Elf Win, do noting.
    # score += 0

    score += resp_idx + 1

# %%
print(score)

# %%
# Second Part
score = 0

for round in strategies:
    # Parse result.
    elf_result, round_end = round.split(' ')

    elf_idx = result_kinds.index(elf_result)

    if round_end == 'X':
        # Need to lose, means Elf win.
        resp_idx = (elf_idx + 2) % STRA_LEN
    elif round_end == 'Y':
        # Need to draw
        resp_idx = elf_idx
        score += 3
    elif round_end == 'Z':
        # Need to win, means Elf lose.
        resp_idx = (elf_idx + 1) % STRA_LEN
        score += 6

    score += resp_idx + 1

print(score)
