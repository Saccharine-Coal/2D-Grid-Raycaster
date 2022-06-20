"""Simple program to create 3D perspective from a 2D grid map.
Algorithm is adapted from: 
    https://lodev.org/cgtutor/raycasting.html#The_Basic_Idea_
With supplemental resource: 
    https://www.youtube.com/watch?v=NbSee-XM7WA
"""
import math

from collections import namedtuple

import numpy as np

import pygame as pg

import numerical


# use this to simplify tuple attribute access
Point2 = namedtuple("Point2", "x y")


def scaled_distance(num, denom) -> float:
    # Lx = sqrt(1^2 + (dy/dx)^2)
    # Ly = sqrt(1^2 + (dx/dy)^2)
    if numerical.is_close(denom, 0):
        # div by 0
        if denom == 0:
            return float("inf")
    # dx is not 0
    return math.sqrt(1 + (num/denom)**2)


def normalize(vector) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
       return vector
    return vector / norm


def run(start, direction_ray, grid_dict):
    # grid of integers
    pos = Point2(start[0], start[1])
    ray_dir = Point2(*normalize(direction_ray))
    int_map = [int(pos.x), int(pos.y)]
    delta_dist = Point2(
        scaled_distance(ray_dir.y, ray_dir.x),
        scaled_distance(ray_dir.x, ray_dir.y)
    )
    INF = float("inf")
    #print(int_map, ray_dir, delta_dist)
    if delta_dist.x == INF or delta_dist.y == INF:
        if delta_dist.x == INF:
            delta_dist = Point2(1e100, delta_dist.y)
        if delta_dist.y == INF:
            delta_dist = Point2(delta_dist.x, 1e100)
        #return 0, -1, -1
    #   step_x, step_y
    # side_dist_x, side_dist_y = 0.0, 0.0
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
    step = Point2(step_x, step_y)
    # perform DDA
    hit = False
    MAX_ITERATIONS = 1e2
    iterations = 0
    # initialize default vals
    perp_wall_dist = 1e20
    side = -1
    element = -1
    while not hit:
        iterations += 1
        if side_dist_x < side_dist_y:
            side_dist_x += delta_dist.x
            int_map[0] += step.x
            side = 0
        else:
            side_dist_y += delta_dist.y
            int_map[1] += step.y
            side = 1
        # check if tile collision
        index = (int_map[0], int_map[1])
        element = grid_dict.setdefault(index, -1)
        if element > 0:
            # collision
            hit = True
        # set upper limit to prevent infinite loop
        if iterations == MAX_ITERATIONS:
            return 0, -1, -1
    if side == 0:
        # side is vertical
        perp_wall_dist = (side_dist_x - delta_dist.x)
    else:
        # side is horizontal
        perp_wall_dist = (side_dist_y - delta_dist.y)
    return perp_wall_dist, side, element


def floor_ray(start, stepsize, width) -> int:
    floor = math.floor(start)
    is_negative = stepsize < 0
    if is_negative:
        # moving in negative direction
        return (start - floor)*stepsize
    else:
        # moving in positive direction
        return ((floor+width) - start)*stepsize


def tile_collidepoint(point, grid):
    for rect in grid:
        if rect.collidepoint(point):
            return True
    return False
    for x, row in enumerate(grid):
        for y, element in enumerate(row):
            index = (x, y)
            if element == 1:
                # is a filled tile
                print(index, point)
                if numerical.is_array_close(index, point):
                    return True
    return False


def rotate(rad) -> tuple:
    # x = cos(phi) - sin(phi)
    # y = sin(phi) - cos(phi)
    rad = rad % 2*math.pi
    cos, sin = math.cos(rad), math.sin(rad)
    return (cos-sin, sin+cos)


GRID = [
  [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,7,7,7,7,7,7,7,7],
  [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,7],
  [4,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
  [4,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
  [4,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,7],
  [4,0,4,0,0,0,0,5,5,5,5,5,5,5,5,5,7,7,0,7,7,7,7,7],
  [4,0,5,0,0,0,0,5,0,5,0,5,0,5,0,5,7,0,0,0,7,7,7,1],
  [4,0,6,0,0,0,0,5,0,0,0,0,0,0,0,5,7,0,0,0,0,0,0,8],
  [4,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,1],
  [4,0,8,0,0,0,0,5,0,0,0,0,0,0,0,5,7,0,0,0,0,0,0,8],
  [4,0,0,0,0,0,0,5,0,0,0,0,0,0,0,5,7,0,0,0,7,7,7,1],
  [4,0,0,0,0,0,0,5,5,5,5,0,5,5,5,5,7,7,7,7,7,7,7,1],
  [6,6,6,6,6,6,6,6,6,6,6,0,6,6,6,6,6,6,6,6,6,6,6,6],
  [8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
  [6,6,6,6,6,6,0,6,6,6,6,0,6,6,6,6,6,6,6,6,6,6,6,6],
  [4,4,4,4,4,4,0,4,4,4,6,0,6,2,2,2,2,2,2,2,3,3,3,3],
  [4,0,0,0,0,0,0,0,0,4,6,0,6,2,0,0,0,0,0,2,0,0,0,2],
  [4,0,0,0,0,0,0,0,0,0,0,0,6,2,0,0,5,0,0,2,0,0,0,2],
  [4,0,0,0,0,0,0,0,0,4,6,0,6,2,0,0,0,0,0,2,2,0,2,2],
  [4,0,6,0,6,0,0,0,0,4,6,0,0,0,0,0,5,0,0,0,0,0,0,2],
  [4,0,0,5,0,0,0,0,0,4,6,0,6,2,0,0,0,0,0,2,2,0,2,2],
  [4,0,6,0,6,0,0,0,0,4,6,0,6,2,0,0,5,0,0,2,0,0,0,2],
  [4,0,0,0,0,0,0,0,0,4,6,0,6,2,0,0,0,0,0,2,0,0,0,2],
  [4,4,4,4,4,4,4,4,4,4,1,1,1,2,2,2,2,2,2,3,3,3,3,3]
]

INT_TO_COLOR = {
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (255, 255, 0),
    5: (255, 0, 255),
    6: (0, 255, 255),
    7: (255, 255, 255),
    8: (255, 155, 0)
}


def darken_rgb(rgb, sub) -> tuple:
    def sub_and_limit(val, sub, ceil=255, floor=0):
        subtracted = val - sub
        return min(max(subtracted, floor), 255)
    r = sub_and_limit(rgb[0], sub)
    g = sub_and_limit(rgb[1], sub)
    b = sub_and_limit(rgb[2], sub)
    return (r, g, b)


def rotate_by_step(xy, rad) -> tuple:
    x, y = xy[:]
    cos, sin = math.cos(rad), math.sin(rad)
    nx = (x*cos) - (y*sin)
    ny = (x*sin) + (y*cos)
    return (nx, ny)


def main():

    grid = {}
    for x, row in enumerate(GRID):
        for y, element in enumerate(row):
            grid[(x, y)] = element

    pg.init()
    clock = pg.time.Clock()
    # Set up the drawing window
    size = (width, height) = [600, 600]
    screen = pg.display.set_mode(size)

    # Run until the user asks to quit
    running = True
    direction = Point2(1, 0)
    rad = -.75
    plane = Point2(0, 0.66)
    origin = np.array((3.0, 10.0))
    RAD_STEP = 2*math.pi/32
    STEPSIZE = .25

    # MINIMAP
    window_scale = 6
    w, h = len(GRID), len(GRID[0])
    subwindow = pg.Surface((w*window_scale, h*window_scale))
    while running:
        clock.tick(30)
        print(f'fps={clock.get_fps():.0f}')
        # Did the user click the window close button?
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    direction = Point2(*rotate_by_step(direction, -RAD_STEP))
                    plane = Point2(*rotate_by_step(plane, -RAD_STEP))
                if event.key == pg.K_RIGHT:
                    direction = Point2(*rotate_by_step(direction, RAD_STEP))
                    plane = Point2(*rotate_by_step(plane, RAD_STEP))
                if event.key == pg.K_DOWN:
                    origin[0] -= STEPSIZE*direction.x
                    origin[1] -= STEPSIZE*direction.y
                if event.key == pg.K_UP:
                    origin[0] += STEPSIZE*direction.x
                    origin[1] += STEPSIZE*direction.y
        # Fill the background with black
        screen.fill((0, 0, 0))

        for x in range(width):
            camera_x = ((2*x) / width) - 1
            ray_dir = (direction.x + (plane.x*camera_x), direction.y + (plane.y*camera_x))
            dist, side, element = run(origin, ray_dir, grid)[:]
            if side == -1:
                # ray did not collide with anything
                continue
            color = INT_TO_COLOR.get(element)
            if side == 0:
                # darken color
                color = darken_rgb(color, 50)
            scale = dist
            line_height = height/scale
            if dist == 0:
                line_height = height
            y_start = (-line_height + height)/2
            if y_start < 0:
                y_start = 0
            y_end = (line_height + height)/2
            if y_end >= height:
                y_end = height-1
            # dist -> depth -> darker
            ratio = (1-(1/(dist+1)))
            color = darken_rgb(color, ratio*150)
            pg.draw.aaline(screen, color, (x, y_start), (x, y_end))
        # clear subwindow
        subwindow.fill((25, 25, 25))
        for index, element in grid.items():
            x, y = index[:]
            if element > 0:
                color = INT_TO_COLOR.get(element)
                pg.draw.rect(subwindow, color,
                             pg.Rect((x*window_scale, y*window_scale), (window_scale, window_scale))
                            )
        scaled_pos = (origin[0]*window_scale, origin[1]*window_scale)
        scaled_dir = ((origin[0]+direction.x*3)*window_scale, (origin[1]+direction.y*3)*window_scale)
        pg.draw.circle(subwindow, (255, 0, 0), scaled_pos, 5)
        pg.draw.line(subwindow, (0, 255, 0), scaled_pos, scaled_dir, 5)
        screen.blit(subwindow, (0, 0))
        # Flip the display
        pg.display.flip()
main()
