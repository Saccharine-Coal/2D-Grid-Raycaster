"""Holds simple game classes."""
import pygame as pg

import functions
import constants
import grid


# construct dictionary from a nested array to simplify grid indexing
Grid = {}
for x, row in enumerate(grid.GRID):
    for y, element in enumerate(row):
        Grid[(x, y)] = element


class Player:
    """Game object that represents a player.
    Position is represented by a cartesian pair (x, y).
    Each player has a direction vector and plane vector.
    Player movement is handled by Player.move() and Player.rotate()."""

    def __init__(self, xy) -> None:
        (self.x, self.y) = xy
        self.direction = constants.Point2(1, 0)
        self.plane = constants.Point2(0, 0.66)
        self.grid = Grid

    @property
    def xy(self) -> constants.Point2:
        return constants.Point2(self.x, self.y)

    def move(self, dx=0, dy=0) -> None:
        x = self.x + dx * constants.STEPSIZE * self.direction.x
        y = self.y + dy * constants.STEPSIZE * self.direction.y
        if self.is_colliding(x, y):
            return
        self.x, self.y = x, y

    def rotate(self, degrees) -> None:
        """Rotate the plane and direction ray."""
        rads = (degrees / 36) * constants.DEG_STEP
        self.direction = constants.Point2(
            *functions.rotate_by_step(self.direction, rads)
        )
        self.plane = constants.Point2(*functions.rotate_by_step(self.plane, rads))

    def handle_event(self, events, pressed, dt) -> None:
        # check pressed keys
        if pressed[pg.K_LEFT]:
            self.rotate(-constants.DEG_STEP * dt)
        if pressed[pg.K_RIGHT]:
            self.rotate(constants.DEG_STEP * dt)
        if pressed[pg.K_DOWN]:
            self.move(-1 * dt, -1 * dt)
        if pressed[pg.K_UP]:
            self.move(1 * dt, 1 * dt)

    def is_colliding(self, x, y) -> bool:
        return False
        # TODO: implement a working function
        pos = (int(round(x)), int(round(y)))
        if pos in self.grid and self.grid[pos] != 0:
            return True
        return False


class MiniMap:
    """Game object that represents a small 2D top down view of the map."""

    def __init__(self):
        self.scale = constants.SCALE
        self.w, self.h = len(grid.GRID), len(grid.GRID[0])
        self.subwindow = pg.Surface((self.w * self.scale, self.h * self.scale))

    def draw(self, surface, grid, player):
        self.subwindow.fill((25, 25, 25))
        for index, element in grid.items():
            x, y = index[:]
            if element > 0:
                if element >= 100:
                    # is referencing a texture element
                    color = (100, 100, 100)
                else:
                    color = constants.INT_TO_COLOR.get(element)
                pg.draw.rect(
                    self.subwindow,
                    color,
                    pg.Rect(
                        (x * self.scale, y * self.scale),
                        (self.scale, self.scale),
                    ),
                )
        scaled_pos = (player.x * self.scale, player.y * self.scale)
        scaled_dir = (
            (player.x + player.direction.x * 3) * self.scale,
            (player.y + player.direction.y * 3) * self.scale,
        )
        pg.draw.circle(self.subwindow, (255, 0, 0), scaled_pos, 5)
        pg.draw.line(self.subwindow, (0, 255, 0), scaled_pos, scaled_dir, 5)
        surface.blit(self.subwindow, (0, 0))
