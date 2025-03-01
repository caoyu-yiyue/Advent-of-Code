# %%
from functools import cmp_to_key

# %%
with open('2024/data/Day5.txt', 'r') as f:
    input_str = f.read().strip()

# %%
rules_str = input_str.split('\n\n')[0].split('\n')
pages_str = input_str.split('\n\n')[1].split('\n')

# %%
pages = [[int(num) for num in page.split(',')] for page in pages_str]
RULES_HASH = set(rules_str)


# %%
# For the num a and b, if a|b is in RULES_HASH, a is before b,
# else a is after b.
def cmp_(a, b) -> int:
    compare_key = f'{a}|{b}'
    if compare_key in RULES_HASH:
        return 1
    else:
        return -1


# %%
sum_of_middle = 0
for page in pages:
    sorted_page = sorted(page, key=cmp_to_key(cmp_), reverse=True)
    if page == sorted_page:
        sum_of_middle += page[len(page) // 2]

print(sum_of_middle)

# %%
# ================================================================================
# Part 2
sum_of_incorrect_middle = 0
for page in pages:
    sorted_page = sorted(page, key=cmp_to_key(cmp_), reverse=True)
    if page != sorted_page:
        sum_of_incorrect_middle += sorted_page[len(sorted_page) // 2]

print(sum_of_incorrect_middle)
