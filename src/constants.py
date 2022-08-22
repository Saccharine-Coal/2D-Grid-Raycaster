"""Holds settings for program and constant values."""
from collections import namedtuple

# use this to simplify tuple attribute access
Point2 = namedtuple("Point2", "x y")

# GAME SETTINGS
SIZE = (600, 600)               # game window size
FPS = 60                        # max fps of game

# WORLD SETTINGS
SLOW = False                    # show raycasting drawing process
RANDOM = True
EMPTY_CHANCE = 0.8
DIM = 40
# RGBA -> int
# (R & 0xff) << 24 | (G & 0xff) << 16 | (B & 0xff) << 8 | (A & 0xff)
INT_TO_COLOR = {
    # maps grid elements to colors
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (255, 255, 0),
    5: (255, 0, 255),
    6: (0, 255, 255),
    7: (255, 255, 255),
    8: (255, 155, 0),
}
# maps grid elements to textures, start with 100+
INT_TO_INDEX = {
    101: 0,
    102: 1,
    103: 2,
    104: 3,
    105: 4,
    106: 5,
    107: 6,
    108: 7,
    109: 8,
    110: 9,
    111: 10
}
FLOOR = (150, 150, 150)            # color of floor
CEILING = (20, 20, 20)       # color of ceiling


# PLAYER SETTINGS
STEPSIZE = 0.0035                # move player by size steps on keypress
DEG_STEP = 0.3                    # rotate player by size steps on keypress
if SLOW:
    DEG_STEP = 3 * DEG_STEP     # increase step size if SLOW=True

# MINIMAP SETTINGS
SCALE = 4                       # scaling of minimap

# TEXTURE SETTINGS
STEP = 1                        # how many steps to take when casting rays
TEX_WIDTH = TEX_HEIGHT = 64
INTERVAL = 3        # controls quality of textures as a function of distance
