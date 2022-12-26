"""
Advent of Code 2022 / Day 7
url: https://adventofcode.com/2022/day/7
"""

# %%
from typing import Dict, Literal, Optional

# %%
with open('data/day7.txt', 'r') as f:
    commands = f.read().splitlines()

# %%
filtered_dirs = []


# %%
class Node:

    def __init__(self,
                 name: str,
                 type: Literal['dir', 'file'],
                 size: Optional[int] = None,
                 parent=None) -> None:
        self.name = name
        self.type = type
        self.size = size
        self.parent = parent
        self.children: Dict[str, Node] = {}

    def add_child(self, child) -> None:
        child.parent = self
        self.children.update({child.name: child})

    def cal_size(self) -> None:
        if self.type == 'dir':
            if self.children == {}:
                self.size = 0
            else:
                self.size = sum(
                    map(lambda child: child.cal_size(),
                        self.children.values()))
                # If size < 100000, append it to result.
                if self.size <= 100000:
                    filtered_dirs.append(self)

        return self.size

    def go_to_child(self, name):
        return self.children[name]

    def go_to_parent(self):
        return self.parent

    def back_to_root(self):
        root = self
        while root.parent is not None:
            root = root.parent

        return root

    def travel_over_dirs(self):
        dirs_under = []

        for child in self.children.values():
            if child.type == 'file':
                continue

            dirs_under.append(child)
            child_dirs = child.travel_over_dirs()
            dirs_under = dirs_under + child_dirs

        return dirs_under


# %%
CURRENT_NODE = Node(name='/', type='dir')


def change_current_node(to: str) -> Node:
    global CURRENT_NODE
    if to == '..':
        CURRENT_NODE = CURRENT_NODE.go_to_parent()
    else:
        CURRENT_NODE = CURRENT_NODE.go_to_child(to)


def create_dir_child(name: str) -> None:
    child_node = Node(name=name, type='dir')
    CURRENT_NODE.add_child(child_node)


def create_file_child(name: str, size: int):
    child_node = Node(name=name, type='file', size=size)
    CURRENT_NODE.add_child(child_node)


def parse_input(input_line):
    line_parts = input_line.split(' ')
    indicator = line_parts[0]

    if indicator == "$":
        command = line_parts[1]
        if command == 'cd':
            change_current_node(to=line_parts[2])
        if command == 'ls':
            pass
    elif indicator == 'dir':
        create_dir_child(name=line_parts[1])
    elif indicator.isdigit():
        create_file_child(name=line_parts[1], size=int(indicator))


# %%
for line in commands[1:]:
    parse_input(line)

root_node = CURRENT_NODE.back_to_root()
root_node.cal_size()

# %%
sum([filtered_dir.size for filtered_dir in filtered_dirs])

# %%
# ================================================================================
# Part 2
# ================================================================================
all_dirs = root_node.travel_over_dirs()

# Test if all dirs
set([dir.type for dir in all_dirs])

# %%
size_list = [dir.size for dir in all_dirs]
size_list.sort()

space_free = 70000000 - root_node.size
space_needed = 30000000 - space_free

for size in size_list:
    if size < space_needed:
        continue
    else:
        print(size)
        break
