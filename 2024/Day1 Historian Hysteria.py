"""
https://adventofcode.com/2024/day/1
"""
# %%
from collections import Counter

# %%
with open('2024/data/day1.txt', 'r') as f:
    locations_txt: list = f.read().splitlines()

locations: list = zip(*map(lambda x: list(map(int, x.split())), locations_txt))

# %%
location_sorted: list = list(map(lambda x: sorted(list(x)), locations))

# %%
distances = []
for idx in range(0, len(location_sorted[0])):
    distance_per = abs(location_sorted[0][idx] - location_sorted[1][idx])
    distances.append(distance_per)

# %%
result_1 = sum(distances)
print(result_1)

# ================================================================================
# %%
count_map: Counter = Counter(location_sorted[1])

result_2 = 0
for loc in location_sorted[0]:
    result_2 += loc * count_map[loc]

print(result_2)
