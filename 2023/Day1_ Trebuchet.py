"""
Advent of Code 2023 / Day 1
url: https://adventofcode.com/2023/day/1
"""

# %%
import re

# %%
FIRST_NUM_REGEX = re.compile(r"^.*?(\d)", flags=re.MULTILINE)
LAST_NUM_REGEX = re.compile(r".*(\d).*$", flags=re.MULTILINE)

# %%
with open("data/day1.txt", "r") as f:
    input_txt = f.read()


# %%
def cal_calibration_sum(input_txt) -> int:
    first_nums = FIRST_NUM_REGEX.findall(input_txt)
    last_nums = LAST_NUM_REGEX.findall(input_txt)

    calibration_nums = [
        pair[0] * 10 + pair[1]
        for pair in zip(map(int, first_nums), map(int, last_nums))
    ]

    return sum(calibration_nums)


# %%
cal_calibration_sum(input_txt)

# Result: 55621

# %%
# ================================================================================
# Part 2
num_str_dict = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
num_str_regex = "|".join(num_str_dict.keys())

# %%
first_num_or_num_str_regex = re.compile(r"^.*?(\d|{})".format(num_str_regex),
                                        flags=re.MULTILINE)
last_num_or_num_str_regex = re.compile(r".*(\d|{}).*$".format(num_str_regex),
                                       flags=re.MULTILINE)

# %%
first_num_or_str = first_num_or_num_str_regex.findall(input_txt)
last_num_or_str = last_num_or_num_str_regex.findall(input_txt)


def parse_num(num_or_str: str) -> int:
    # If length of the number or str in greater than 1, it's a string,
    # else is a number.
    if len(num_or_str) > 1:
        return num_str_dict[num_or_str]
    else:
        return int(num_or_str)


calibration_nums_part2 = [
    pair[0] * 10 + pair[1] for pair in zip(map(parse_num, first_num_or_str),
                                           map(parse_num, last_num_or_str))
]

# %%
print(sum(calibration_nums_part2))

# 53592
