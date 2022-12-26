"""
Advent of Code 2022 / Day 16
url: https://adventofcode.com/2022/day/16
"""

# %%
import re
from collections import deque
import copy

# %%
with open('data/day16.txt', 'r') as f:
    INPUT_LINES = f.read().splitlines()

FINAL_SCORE = 0
DISTS_DICT = {}
PATH = ['AA']


# %%
def parse_node(str_line):
    node_name_regex = re.compile(r'([A-Z]{2})')
    rate_regex = re.compile(r'[0-9]+')

    nodes = node_name_regex.findall(str_line)
    rate = int(rate_regex.search(str_line).group(0))

    return {nodes[0]: {'adjacents': nodes[1:], 'rate': rate}}


def parse_nodes(input_str: str) -> dict:
    nodes = {}
    for line in input_str:
        nodes.update(parse_node(line))

    return nodes


def cal_distances(start_node):
    distances = {start_node: 0}

    visited_nodes = {start_node}
    processing_queue = deque([(start_node, node)
                              for node in NODES[start_node]['adjacents']])

    while len(processing_queue) > 0:
        adjacent = processing_queue.popleft()
        # if not in the visited node.
        if (processing := adjacent[1]) not in visited_nodes:
            # Add the processing node to the visited.
            visited_nodes.add(processing)

            # Calculate distance.
            dist = distances[adjacent[0]] + 1

            # Update record.
            distances[processing] = dist

            # Extend the processing queue for next research.
            processing_queue.extend([
                (processing, node) for node in NODES[processing]['adjacents']
            ])

    DISTS_DICT[start_node] = distances

    return distances


def ending_settlement(open_valves: dict) -> int:
    return sum(
        [NODES[valve]['rate'] * time for valve, time in
         open_valves.items()])


def bfs_all_path(time_limit, stop_inverval=False):

    DP = {}

    time = time_limit
    root_state = {'node': 'AA', 'time': time, 'open_valves': {}}

    process_queue = deque([])
    process_queue.append(root_state)

    max_flow = 0
    path_record = []

    while len(process_queue) > 0:
        state = process_queue.popleft()
        # print(state)

        if stop_inverval:
            flow = ending_settlement(state['open_valves'])
            path_record.append((set(state['open_valves'].keys()), flow))

        key = state['node'] + str(state['time']) + \
            ''.join(state['open_valves'].keys())

        if key in DP:
            max_flow = max(max_flow, DP[key])

        if state['time'] <= 0:
            # flows_record.append(state['flow'])
            # return state['flow']
            raise ValueError('Wrong time.')

        options = dict(
            filter(
                lambda itm: itm[1]['rate'] > 0 and itm[0] not in state[
                    'open_valves'].keys(), NODES.items()))
        if len(options) == 0 and not stop_inverval:
            # ending_flow = state['flow'] + state['time'] * add_flow(
            #     state['open_valves'])
            ending_flow = ending_settlement(state['open_valves'])
            max_flow = max(max_flow, ending_flow)
            DP[key] = max_flow

            # state['ending_flow'] = ending_flow
            path_record.append((set(state['open_valves'].keys()), ending_flow))

        for node in options.keys():
            steps = DISTS_DICT[state['node']][node] + 1

            if state['time'] - steps <= 0:
                # ending_flow = state['flow'] + state['time'] * add_flow(
                #     state['open_valves'])

                ending_flow = ending_settlement(state['open_valves'])
                max_flow = max(max_flow, ending_flow)
                DP[key] = max_flow

                # state['ending_flow'] = ending_flow
                path_record.append(
                    (set(state['open_valves'].keys()), ending_flow))
            else:
                current_open_valves = copy.deepcopy(state['open_valves'])
                current_open_valves[node] = state['time'] - steps
                new_state = {
                    'node': node,
                    'time': state['time'] - steps,
                    # 'flow':
                    # state['flow'] + steps * add_flow(state['open_valves']),
                    'open_valves': current_open_valves
                }
                process_queue.append(new_state)

    return max_flow, path_record


# %%
# Part 1
NODES = parse_nodes(INPUT_LINES)
for node in NODES.keys():
    cal_distances(node)

# %%
max_flow, _ = bfs_all_path(30)

# %%
# Part 2
max_flow, path_record = bfs_all_path(26, stop_inverval=True)


# %%
def max_flow_dual_paths(path_record):
    ranked_path = sorted(path_record, key=lambda p: p[1], reverse=True)
    max_flow = 0

    for (path_i, flow_i) in ranked_path:
        for (path_j, flow_j) in ranked_path:
            if flow_i + flow_j <= max_flow:
                break
            if len(path_i & path_j) == 0:
                if flow_j + flow_j > max_flow:
                    max_flow = flow_i + flow_j

    return max_flow
    # max_path


max_flow_dual_paths(path_record)
