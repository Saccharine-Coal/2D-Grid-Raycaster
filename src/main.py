"""Simple program to create 3D perspective from a 2D grid map.
Algorithm is adapted from:
    https://lodev.org/cgtutor/raycasting.html#The_Basic_Idea_
With supplemental resource:
    https://www.youtube.com/watch?v=NbSee-XM7WA
Much of the code has been abstracted and compartmentalized to reduce boiler plate code.
This abstraction is intended for beginner programmers to focus
on the DDA algorithm in this program and skip pygame boilerplate code.
The DDA algorithm is contained in the fuctions run_along_ray, and walk_along_ray.
cast_rays handles drawing the world from the distances generated in the DDA algorithm.
"""
import math
from collections import namedtuple
import time

import numpy as np
import pygame as pg

import game_objects
import numerical
import constants
import functions


def main():
    """Run the game. Initializes pygame and game objects.
    Handles user input, updates game objects, and draws to the screen."""

    def handle_events():
        """Abstracted function: Handle all game events"""
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            player.handle_event(event)
        return running

    def clear_screen():
        """Abstracted function: Clear the game screen"""
        screen.fill((0, 0, 0))

    def draw_floor():
        """Abstracted function: Draw game world floor"""
        rect = pg.Rect((0, int(height / 2)), (width, int(height / 2)))
        pg.draw.rect(screen, constants.FLOOR, rect)

    def draw_celing():
        """Abstracted function: Draw game world ceiling"""
        rect = pg.Rect((0, 0), (width, int(height / 2)))
        pg.draw.rect(screen, constants.CEILING, rect)

    def draw_text():
        """Abstracted function: Draw game performance statistics"""
        text = font.render(f"fps={int(clock.get_fps())}", False, (0, 255, 0))
        screen.blit(text, (screen.get_rect().centerx, 0))

    def update_display():
        """Abstracted function: Update game screen"""
        # Flip the display
        pg.display.flip()

    # Construct game objects
    player = game_objects.Player((3, 10))
    grid = game_objects.Grid
    mini_map = game_objects.MiniMap()
    pg.init()
    font = pg.font.SysFont(pg.font.get_default_font(), 24)
    clock = pg.time.Clock()
    # Set up the drawing window
    size = (width, height) = constants.SIZE
    screen = pg.display.set_mode(size)
    # Main game LOOP
    running = True
    while running:
        clock.tick(constants.FPS)
        print(f"fps={clock.get_fps():.0f}")
        # HANDLE EVENTS
        running = handle_events()  # Run until the user asks to quit
        # DRAW
        clear_screen()
        draw_floor()
        draw_celing()
        # cast rays and draw walls
        cast_rays(
            screen,
            player.xy,
            player.direction,
            player.plane,
            grid,
            width,
            height,
            step=constants.STEP,
            slow=constants.SLOW,
        )
        # draw the minimap
        mini_map.draw(screen, grid, player)
        # draw fps
        draw_text()
        update_display()


def cast_rays(
    screen, origin, direction, plane, grid_dict, width, height, step=1, slow=False
):
    # TODO: DOCSTRING

    def get_ray(x, direction, plane, width):
        # TODO: DOCSTRING
        camera_x = ((2 * x) / width) - 1
        ray_dir = constants.Point2(
            direction.x + (plane.x * camera_x),
            direction.y + (plane.y * camera_x),
        )
        return ray_dir

    def get_color(distance, side, element):
        # TODO: DOCSTRING
        color = constants.INT_TO_COLOR.get(element)
        # dist -> depth -> darker
        ratio = 1 - (1 / (distance + 1))
        if side == 0:
            # darken color
            color = functions.darken_rgb(color, 50)
        color = functions.darken_rgb(color, ratio * 150)
        return color

    def get_y_limits(distance, height):
        # TODO: DOCSTRING
        line_height = height / distance
        y_start = (-line_height + height) / 2
        if y_start < 0:
            y_start = 0
        y_end = (line_height + height) / 2
        if y_end >= height:
            y_end = height - 1
        return (y_start, y_end)

    def draw_wall(screen, color, x, y_limits, step, slow):
        # TODO: DOCSTRING
        (y_start, y_end) = y_limits
        for i in range(step):
            pg.draw.aaline(screen, color, (x + i, y_start), (x + i, y_end))
            if slow:
                time.sleep(0.002)
                pg.display.flip()

    assert step >= 1, "Step must be greater than 0"
    # begin raycasting
    for x in range(0, width, step):
        ray = get_ray(x, direction, plane, width)
        dist, side, element = run_along_ray(origin, ray, grid_dict)[:]
        if side == -1:
            # ray did not collide with anything, so move to next x coordinate
            continue
        color = get_color(dist, side, element)
        y_limits = get_y_limits(dist, height)
        draw_wall(screen, color, x, y_limits, step, slow)


def run_along_ray(start, direction_ray, grid_dict):
    # TODO: DOCSTRING

    def construct_deltas(ray_dir, pos, int_map):
        # TODO: DOCSTRING
        # ||ray_dir|| = 1 since ray_dir is normalized
        # delta_dist = abs(||ray_dir||/ray_dir.x, ||ray_dir||/ray_dir.y)
        # delta_dist = abs(1/ray_dir.x, 1/ray_dir.y)
        # handle division by 0
        INF_VAL = float("inf")
        if ray_dir.x == 0 or ray_dir.y == 0:
            if ray_dir.x == 0:
                delta_dist = constants.Point2(INF_VAL, abs(1 / ray_dir.y))
            else:
                delta_dist = constants.Point2(abs(1 / ray_dir.x), INF_VAL)
        else:
            # no division by 0
            delta_dist = constants.Point2(abs(1 / ray_dir.x), abs(1 / ray_dir.y))
        # calculate step and initial side dist
        if numerical.is_below(ray_dir.x, 0):
            step_x = -1
            side_dist_x = (pos.x - int_map[0]) * delta_dist.x
        else:
            step_x = 1
            side_dist_x = (int_map[0] + 1.0 - pos.x) * delta_dist.x
        if numerical.is_below(ray_dir.y, 0):
            step_y = -1
            side_dist_y = (pos.y - int_map[1]) * delta_dist.y
        else:
            step_y = 1
            side_dist_y = (int_map[1] + 1.0 - pos.y) * delta_dist.y
        side_dist = [side_dist_x, side_dist_y]
        step = constants.Point2(step_x, step_y)
        return step, side_dist, delta_dist

    def hit_wall(int_map, grid_dict, max_iterations):
        # TODO: DOCSTRING
        element = grid_dict.setdefault(tuple(int_map), -1)
        if element > 0 or max_iterations == 0:
            # collision or max_iterations has been met
            return True
        return False

    def calculate_wall_distance(side_dist, delta_dist, side):
        # TODO: DOCSTRING
        if side == 0:
            # side is vertical
            perp_wall_dist = side_dist[0] - delta_dist.x
        elif side == 1:
            # side is horizontal
            perp_wall_dist = side_dist[1] - delta_dist.y
        else:
            # side == -1
            perp_wall_dist = float("inf")
        return perp_wall_dist

    # TODO: DOCSTRING
    # grid of integers
    # start may be floats
    # get the int values of the start xy
    int_map = [int(start.x), int(start.y)]
    (step, side_dist, delta_dist) = construct_deltas(direction_ray, start, int_map)
    # perform DDA
    max_iterations = 1e2
    running = True
    while running:
        max_iterations -= 1
        (side_dist, int_map, side) = walk_along_ray(
            int_map, step, side_dist, delta_dist
        )
        if hit_wall(int_map, grid_dict, max_iterations):
            running = False
    element = grid_dict.get(tuple(int_map))
    perp_wall_dist = calculate_wall_distance(side_dist, delta_dist, side)
    return perp_wall_dist, side, element


def walk_along_ray(int_map, step, side_dist, delta_dist):
    # TODO: DOCSTRING
    """Take a step along a given ray by following a delta dist.
    Return SIDE if a wall is hit or max iterations is hit."""
    assert isinstance(int_map, list) and isinstance(
        side_dist, list
    ), "Must be a mutable (list) iterable!"
    if numerical.is_below(side_dist[0], side_dist[1]):
        # add to our x dist tracker
        side_dist[0] += delta_dist.x
        # take a step along x
        int_map[0] += step.x
        side = 0
    else:
        side_dist[1] += delta_dist.y
        int_map[1] += step.y
        side = 1
    return side_dist, int_map, side


main()
