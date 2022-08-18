from collections import namedtuple
import math

import pygame as pg

# use this to simplify tuple attribute access
Point2 = namedtuple("Point2", "x y")

# GAME SETTINGS
SIZE = (600, 600)
FPS = 60

# WORLD SETTINGS
STEP = 1
SLOW = False
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
FLOOR = (50, 50, 50)
CEILING = (25, 25, 25)


# PLAYER SETTINGS
STEPSIZE = 0.25
RAD_STEP = 2 * math.pi / 32

# MINIMAP SETTINGS
scale = 6
