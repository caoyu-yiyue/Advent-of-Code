"""
Advent of Code 2022 / Day 12
url: https://adventofcode.com/2022/day/12
"""

# %%
import string
from queue import Queue

import numpy as np
import seaborn as sns

# %%
INPUT: np.array = np.genfromtxt('data/day12.txt', delimiter=1, dtype='<U2')

lowercase_letters = string.ascii_lowercase
letter_map = dict(zip(lowercase_letters, range(len(lowercase_letters))))
letter_map.update({'S': 0, 'E': 25})

INPUT_INTS = np.copy(INPUT)
for k, v in letter_map.items():
    INPUT_INTS[INPUT_INTS == k] = v
INPUT_INTS = INPUT_INTS.astype('int')

# %%
START_COORD = np.array(zip(*np.where(INPUT == 'S')).__next__())
END_COORD = np.array(zip(*np.where(INPUT == 'E')).__next__())

# %%
sns.heatmap(data=INPUT_INTS)


# %%
class Point:

    NEIGHBOR_OFFSETS = np.array([[0, -1], [0, 1], [-1, 0], [1, 0]])

    def __init__(self,
                 coord: tuple[int, int],
                 elevation: int,
                 target=None,
                 cost: int = np.nan) -> None:
        self.coord = np.array(coord)
        self.elevation = elevation
        self.cost = cost
        self.target = target
        self.neighbors = []

    def __repr__(self) -> str:
        return f"""Point: {self.coord},
        value: {self.elevation},
        cost: {self.cost}"""

    @staticmethod
    def _is_inside(coord) -> bool:
        return (coord >= [0, 0]).all() and (coord < INPUT_INTS.shape).all()

    def _dfs_search(self, pnts_array) -> None:
        self._add_direct_neighbors(pnts_array)

        for neighbor_pnt in self.neighbors:
            neighbor_pnt._dfs_search(pnts_array=pnts_array)

    def _add_direct_neighbors(self, pnts_array):
        neighbors_using = []
        for offset in self.NEIGHBOR_OFFSETS:
            # Find neighbors
            neighbor_coord = self.coord + offset
            if not self._is_inside(neighbor_coord):
                # Check if index in range.
                continue
            neighbor_pnt = pnts_array[*neighbor_coord]

            # Checking if is validate road.
            if neighbor_pnt._check_validate(target=self):
                # Add cost and find neighbors.
                neighbor_pnt.target = self
                neighbor_pnt.cost = self.cost + 1
                neighbors_using.append(neighbor_pnt)

        self.neighbors = neighbors_using

    def _bfs_search(self, pnts_array) -> None:
        # queue for processing.
        queue = Queue(maxsize=0)

        # Add direct neighbors.
        self._add_direct_neighbors(pnts_array)

        # fill the queue with direct neighbors.
        for neighbor in self.neighbors:
            queue.put(neighbor)

        # Loop until queue is empty.
        while not queue.empty():
            # for every neighbor, find direct neighbor and add them to queue.
            for neighbor in self.neighbors:
                neighbor = queue.get()
                neighbor._add_direct_neighbors(pnts_array)

                for neighbor_in_neighbor in neighbor.neighbors:
                    queue.put(neighbor_in_neighbor)

    def _is_road(self, target) -> bool:
        return target.elevation - self.elevation <= 1

    def _have_cost(self) -> bool:
        return not np.isnan(self.cost)

    def _check_validate(self, target) -> bool:
        return not self._have_cost() and self._is_road(target)


# %%
# DFS Search
pnts = []

for idx, value in np.ndenumerate(INPUT_INTS):
    pnts.append(Point(coord=idx, elevation=value))

pnts_array = np.array(pnts).reshape(INPUT_INTS.shape)

# %%
end_point = pnts_array[*END_COORD]
end_point.target = end_point
end_point.cost = 0
end_point._dfs_search(pnts_array=pnts_array)

start_pnt = pnts_array[*START_COORD]


# %%
# BFS Search
def search_path(how='bfs', end_coord=END_COORD) -> Point:
    pnts = []

    for idx, value in np.ndenumerate(INPUT_INTS):
        pnts.append(Point(coord=idx, elevation=value))

    pnts_array = np.array(pnts).reshape(INPUT_INTS.shape)

    # Get the end point
    end_point: Point = pnts_array[*end_coord]
    end_point.target = end_point
    end_point.cost = 0

    # Search the path
    if how == 'bfs':
        end_point._bfs_search(pnts_array=pnts_array)
    elif how == 'dfs':
        end_point._dfs_search(pnts_array=pnts_array)

    # Get the start Point
    # start_pnt = pnts_array[*start_coord]

    return pnts_array


pnts_array = search_path(how='bfs')


# %%
def draw_path(start_pnt, start_coord=START_COORD,
              end_coord=END_COORD):
    tracks = []
    pnt = start_pnt
    while pnt.cost > 0:
        tracks.append(pnt.coord)
        pnt = pnt.target

    # costs = []
    # for row in pnts_array:
    #     for pnt in row:
    #         costs.append(pnt.cost)
    # cost_array = np.array(costs).reshape(INPUT_INTS.shape)

    sns.heatmap(INPUT_INTS)
    x, y = list(zip(*tracks))
    sns.scatterplot(x=y, y=x)
    sns.scatterplot(x=[start_coord[1]], y=[start_coord[0]], color='red')
    sns.scatterplot(x=[end_coord[1]], y=[end_coord[0]], color='green')


# %%
start_pnt = pnts_array[*START_COORD]
draw_path(start_pnt=start_pnt)

# %%
# Part 2
lowest_coord = list(zip(*np.where(INPUT_INTS == 0)))

lowest_cost = np.Inf
for coord in lowest_coord:
    pnt: Point = pnts_array[*coord]
    if pnt.cost < lowest_cost:
        lowest_cost = pnt.cost

print(lowest_cost)
