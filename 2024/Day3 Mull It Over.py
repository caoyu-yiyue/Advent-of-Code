# %%
import re

# %%
with open("2024/data/Day3.txt") as f:
    INPUT = f.read()

# %%
num_pairs = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", INPUT)

# %%
result_1 = 0
for num_pair in num_pairs:
    num_pair = [int(num) for num in num_pair]
    result_1 += num_pair[0] * num_pair[1]

print(result_1)

# %%
# ================================================================================
# https://www.reddit.com/r/adventofcode/comments/1h5frsp/comment/m2wdvoo/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

toggle = True
result_2 = 0
for x in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\)", INPUT):
    match x[0]:
        case "do()":
            toggle = True
        case "don't()":
            toggle = False
        case _:
            if toggle:
                result_2 += int(x[1]) * int(x[2])

print(result_2)

# 80710398 Too Low
# 107516772 Incorrect
