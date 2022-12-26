"""
Advent of Code 2022 / Day 19
url: https://adventofcode.com/2022/day/19
"""

# %%
import re
import copy


# %%
def parse_input(path='data/day19ex.txt') -> list:
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    blueprints = []
    for line in lines:
        nums = re.findall(r'\d+', line)
        blueprint = {
            'ore': {
                'ore': int(nums[1])
            },
            'clay': {
                'ore': int(nums[2])
            },
            'obs': {
                'ore': int(nums[3]),
                'clay': int(nums[4])
            },
            'geode': {
                'ore': int(nums[5]),
                'obs': int(nums[6])
            }
        }
        blueprints.append(blueprint)

    return blueprints


def check_geode_rob(state, blueprint) -> bool:
    inv = state['inventory']
    if blueprint['geode']['ore'] <= inv[0] and blueprint['geode'][
            'obs'] <= inv[2] and state['bots'][2] > 0:
        return True
    else:
        return False


def check_obs_rob(state, blueprint) -> bool:
    inv = state['inventory']
    if blueprint['obs']['ore'] <= inv[0] and blueprint['obs'][
            'clay'] <= inv[1] and state['bots'][1] > 0:
        return True
    else:
        return False


def check_clay_rob(state, blueprint) -> bool:
    inv = state['inventory']
    if blueprint['clay']['ore'] <= inv[0]:
        return True
    else:
        return False


def check_ore_rob(state, blueprint) -> bool:
    inv = state['inventory']
    if blueprint['ore']['ore'] <= inv[0]:
        return True
    else:
        return False


def create_new_state(state: dict, type: str | None, blueprint: dict):
    # types = {'ore': 0, 'clay': 1, 'obs': 2, 'geode': 3}
    types = ['ore', 'clay', 'obs', 'geode']

    new_state = copy.deepcopy(state)
    new_state['time'] += 1

    new_state['mines'] = [
        pair[0] + pair[1] for pair in zip(state['mines'], state['bots'])
    ]
    new_state['inventory'] = [
        pair[0] + pair[1] for pair in zip(state['inventory'], state['bots'])
    ]

    if type is not None:
        type_num = types.index(type)
        new_state['bots'][type_num] += 1
        new_state['inventory'][0] -= blueprint[type]['ore']
        if type_num >= 2:
            material_name = types[type_num - 1]
            new_state['inventory'][type_num -
                                   1] -= blueprint[type][material_name]

    if any([mine < 0 for mine in state['inventory']]):
        raise ValueError('出现了负值')

    return new_state


def prune_func(state):
    return sum([[1, 10, 100, 1000][i] * state['mines'][i] for i in range(4)])


def bfs_search(blueprint_num, time_limit, max_depth):
    blueprint = BLUEPIRNTS[blueprint_num]
    depth = 0
    queue = [{'time': 0, 'bots': [1, 0, 0, 0],
              'inventory': [0, 0, 0, 0], 'mines': [0, 0, 0, 0]}]
    max_geode = 0

    while queue:
        c_state = queue.pop(0)
        # print(c_state)

        if depth < c_state['time']:
            queue.sort(key=prune_func, reverse=True)
            queue = queue[:max_depth]
            depth = c_state['time']

        if c_state['time'] == time_limit:
            max_geode = max(max_geode, c_state['mines'][-1])
            continue

        nothing_state = create_new_state(
            state=c_state, type=None, blueprint=blueprint)
        queue.append(nothing_state)

        if check_geode_rob(state=c_state, blueprint=blueprint):
            queue.append(create_new_state(c_state, 'geode', blueprint))
            continue

        if check_obs_rob(c_state, blueprint):
            queue.append(create_new_state(c_state, 'obs', blueprint))
        if check_clay_rob(c_state, blueprint):
            queue.append(create_new_state(c_state, 'clay', blueprint))
        if check_ore_rob(c_state, blueprint):
            queue.append(create_new_state(c_state, 'ore', blueprint))

    return max_geode


# %%
BLUEPIRNTS = parse_input('data/day19.txt')

result = 0
for i in range(len(BLUEPIRNTS)):
    max_geo = bfs_search(i, 24, 1000)
    print('No.', i, ': ', max_geo)
    result += (i + 1) * max_geo

# %%
# Part 2
BLUEPIRNTS = parse_input('data/day19.txt')
# bfs_search(1, 32, 10000)

result = 1
for i in range(3):
    max_geo = bfs_search(i, 32, 10000)
    print('No.', i, ': ', max_geo)
    result *= max_geo
