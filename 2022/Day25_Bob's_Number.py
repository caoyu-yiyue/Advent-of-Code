"""
Advent of Code 2022 / Day 25
url: https://adventofcode.com/2022/day/25
"""

# %%
value_map = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}


def SNAFU2norm(SNAFU: str) -> int:
    result = 0
    for i, char in enumerate(SNAFU[::-1]):
        digit = value_map[char]
        result += 5 ** i * digit

    return result


# %%
def norm2SNAFU(num: int) -> str:
    first_divider = 0
    i = 0
    while first_divider < num:
        i += 1
        first_divider = 5 ** i
    i -= 1

    quotients = []
    mod = num
    while mod > 5:
        num, mod = divmod(mod, 5**i)
        quotients.append(num)
        i -= 1
    quotients.extend([0] * i + [mod])

    mapping = {0: '0', 1: '1', 2: '2', 3: '1=', 4: '1-', 5: '10'}
    result = ''
    for i, num in enumerate(quotients[::-1]):
        if len(result) > i:
            num += int(result[-(i + 1)])
            result = result[-i:]
        result = mapping[num] + result
    return result


# 1-0---0
# norm2SNAFU(20)

# %%
norm2SNAFU(201)

# %%
with open('data/day25.txt') as f:
    ipt_lines = f.read().splitlines()


total = 0
for line in ipt_lines:
    total += SNAFU2norm(line)
# print(total)

print(norm2SNAFU(total))
# Wrong: 20===-20-020=0001-2
