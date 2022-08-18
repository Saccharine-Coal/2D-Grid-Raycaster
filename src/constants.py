"""Holds settings for program and constant values."""
from collections import namedtuple

# use this to simplify tuple attribute access
Point2 = namedtuple("Point2", "x y")

# GAME SETTINGS
SIZE = (600, 600)               # game window size
FPS = 60                        # max fps of game

# WORLD SETTINGS
STEP = 1                        # how many steps to take when casting rays
SLOW = False                    # show raycasting drawing process
# maps grid elements to colors
INT_TO_COLOR = {
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (255, 255, 0),
    5: (255, 0, 255),
    6: (0, 255, 255),
    7: (255, 255, 255),
    8: (255, 155, 0),
}
FLOOR = (50, 50, 50)            # color of floor
CEILING = (25, 25, 25)          # color of ceiling


# PLAYER SETTINGS
STEPSIZE = 0.035                # move player by size steps on keypress
DEG_STEP = 1                    # rotate player by size steps on keypress

# MINIMAP SETTINGS
SCALE = 6                       # scaling of minimap
