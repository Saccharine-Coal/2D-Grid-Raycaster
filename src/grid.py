"""Separate file to hold the grid array. Also checks the structure of the grid."""
import random

import numpy as np

import constants

"""
Feel free to modify the preceding GRID definition as you'd like.
For simplicity the grid should be square and only contain integer elements.

Each integer determines whether a wall exists and the color of said wall.
DEFAULT INTEGER MAPPINGS
    Integer |   Effect
    0:          No wall,
    1:          Wall with color=(255, 0, 0),
    2:          Wall with color=(0, 255, 0),
    3:          Wall with color=(0, 0, 255),
    4:          Wall with color=(255, 255, 0),
    5:          Wall with color=(255, 0, 255),
    6:          Wall with color=(0, 255, 255),
    7:          Wall with color=(255, 255, 255),
    8:          Wall with color=(255, 155, 0)
"""

GRID = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7],
    [4, 0, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [4, 0, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [4, 0, 103, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7],
    [4, 0, 104, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 0, 7, 7, 7, 7, 7],
    [4, 0, 105, 0, 0, 0, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 7, 0, 0, 0, 7, 7, 7, 1],
    [4, 0, 106, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0, 0, 0, 0, 0, 8],
    [4, 0, 107, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 1],
    [4, 0, 108, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0, 0, 0, 0, 0, 8],
    [4, 0, 106, 0, 101, 104, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0, 0, 7, 7, 7, 1],
    [4, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, 1],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 6, 0, 6, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 0, 0, 5, 0, 0, 2, 0, 0, 0, 2],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2],
    [4, 0, 6, 0, 6, 0, 0, 0, 0, 4, 6, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 2],
    [4, 0, 0, 5, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2],
    [4, 0, 6, 0, 6, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 5, 0, 0, 2, 0, 0, 0, 2],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
]
# generate a random grid
if constants.RANDOM:
    assert 0 < constants.EMPTY_CHANCE < 1
    n = constants.DIM
    vals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 101, 102, 103, 104, 105, 106, 107, 108]
    n_sub = len(vals) - 1
    p_dist = [constants.EMPTY_CHANCE] + n_sub*[(1-constants.EMPTY_CHANCE)/n_sub]
    assert len(vals) == len(p_dist)
    assert 1 - sum(p_dist) < 1e-2, f"sum(p_dist) is not 1!"
    f = lambda i, j: 1 if (i==0 or j==0 or i==n or j==n) else random.choices(population=vals, weights=p_dist, k=1)[0]
    GRID = list(list(f(i, j) for j in range(n+1)) for i in range(n+1))

# PLEASE DO NOT MODIFY THE FOLLOWING LINES
# set (1-2, 1-2) to be empty. always place player here
for i in range(2):
    for j in range(2):
        GRID[1+i][1+j] = 0

# convert grid to array for numba
GRID = np.array(GRID, dtype="int64")

# check structure and data of grid
assert all(len(GRID) == len(row) for row in GRID), "Grid should be square!"
# element wise assertions
for row in GRID:
    for val in row:
        assert isinstance(val, np.int64), "Non integer element in grid!"
        valid = (val == 0 or val in constants.INT_TO_COLOR or val in constants.INT_TO_INDEX)
        assert valid, f"Element, {val}, defined in GRID not defined in constants.INT_TO_COLOR or constants.INT_TO_INDEX"
