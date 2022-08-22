import math

import pygame as pg

import numba as nb
from numba import jit

import numpy as np

import constants
import dda
import functions


CACHE = False

# TODO: paralle=True
@jit(fastmath=True, nopython=True, cache=CACHE, nogil=True)
def cast_rays(
    screen_size,
    origin,
    direction,
    plane,
    grid,
    pixel_buffer,
    images,
    step=constants.STEP,
    slow=False,
):
    """Cast rays perpendicular to <plane> in the direction of <direction> from <origin>.
    A ray is casted for every <step> taken from 0 to <width>.
    If a valid tile is hit by a row then the wall is drawn as a line.
    If slow is True, the screen is drawn after every step."""
    assert step >= 1, "Step must be greater than 0"
    assert step == 1 or step % 2 == 0, "Step must be 1 or even"
    # init vars
    (width, height) = screen_size
    # begin raycasting
    x = 0
    for x in nb.prange(width):
        ray = dda.get_ray(x, direction, plane, width)
        distance, side, index = dda.run_along_ray(origin, ray, grid)[:]
        element = grid[index[0]][index[1]]
        distance = abs(distance)
        if side == -1 or distance < 0.2:
            # ray did not collide with anything, so move to next x coordinate
            minor_step = step
            continue
        else:
            # minor_step = step + int(distance // constants.INTERVAL)
            minor_step = step
            pixel_buffer = fill_wrapper(
                screen_size,
                pixel_buffer,
                origin,
                x,
                ray,
                distance,
                side,
                element,
                minor_step,
                images,
            )
    return pixel_buffer


@jit(fastmath=True, nopython=True, cache=CACHE)
def get_y_limits(line_height, height) -> tuple:
    """Get the start values of walls to be drawn along y-axis."""
    y_start = int((-line_height + height) / 2)
    if y_start < 0:
        y_start = 0
    y_end = int((line_height + height) / 2)
    if y_end >= height:
        y_end = height - 1
    return (y_start, y_end)


@jit(fastmath=True, nopython=True, cache=CACHE)
def calculate_wall_x(side, start, distance, ray) -> float:
    assert distance >= 0
    if side == 0:
        x = start[1] + distance * ray[1]
    else:
        # side == 1
        x = start[0] + distance * ray[0]
    # float val
    return x - math.floor(x)


"int32(float32[:,:], float32[:,:], float32, int32)"


@jit(fastmath=True, nopython=True, cache=CACHE)
def calculate_texture_x(origin, ray, distance: float, side: int) -> int:
    wall_x = calculate_wall_x(side, origin, distance, ray)
    x = int(wall_x * constants.TEX_WIDTH)
    if side == 0 and ray[0] > 0:
        x = constants.TEX_WIDTH - x - 1
    if side == 1 and ray[1] < 0:
        x = constants.TEX_WIDTH - x - 1
    return x


@jit(fastmath=True, nopython=True, cache=CACHE)
def get_color(distance, side, element):
    """Get the color for given element and darken color
    depending on side hit and distance from start."""
    COLORS = [
        255,
        4278190335,
        16711935,
        65535,
        4294902015,
        4278255615,
        16777215,
        4294967295,
        4288348415,
    ]
    color = COLORS[element]
    ratio = 1 - (1 / (distance + 1))
    if side == 0:
        # darken color using bitwise operators
        color = (color >> 1) & 8355711
    reduce_color(color, ratio * 10)
    return color


"""
    color = constants.INT_TO_COLOR.get(element)
    # dist -> depth -> darker
    ratio = 1 - (1 / (distance + 1))
    if side == 0:
        # darken color
        color = functions.darken_rgb(color, 50)
    color = functions.darken_rgb(color, ratio * 150)
    return pg.Color(color)
"""


@jit(fastmath=True, nopython=True, cache=CACHE, nogil=True)
def fill_wrapper(
    screen_size,
    pixel_buffer,
    origin,
    x,
    ray,
    distance,
    side,
    element,
    step,
    images,
) -> np.ndarray:
    """Wraps fill_slice to test parallelization."""
    (width, height) = screen_size
    line_height = int(height / distance)
    y_limits = get_y_limits(line_height, height)
    tex_x = calculate_texture_x(origin, ray, distance, side)
    if element < 100:
        color = int(get_color(distance, side, element))
        texture = np.zeros((64, 64), dtype="uint32")
    else:
        # element >= 100
        texture = images[element - 101]
        color = 0
    return fill_slice(
        screen_size,
        pixel_buffer,
        x,
        y_limits,
        line_height,
        side,
        step,
        element,
        texture,
        tex_x,
        color,
    )


@jit(fastmath=True, nopython=True, cache=CACHE, nogil=True)
def reduce_color(color, factor) -> int:
    return color
    # TODO: implement correctly 
    R = int(((color >> 24) & 0xFF) / factor)
    G = int(((color >> 16) & 0xFF) / factor)
    B = int(((color >> 8) & 0xFF) / factor)
    A = int(((color) & 0xFF) / factor)
    return (R & 0xFF) << 24 | (G & 0xFF) << 16 | (B & 0xFF) << 8 | (A & 0xFF)


@jit(fastmath=True, nopython=True, parallel=True, cache=CACHE, nogil=True)
def fill_slice(
    screen_size,
    pixel_buffer,
    x,
    y_limits,
    line_height,
    side,
    step,
    element,
    texture,
    tex_x,
    color,
) -> np.ndarray:
    (width, height) = screen_size
    (y_start, y_end) = y_limits
    if element > 100:
        col = np.zeros((int(y_end - y_start),), dtype="int64")
        step_y = 64.0 / (line_height)
        offset = y_start - (((constants.SIZE[1] + line_height) / 2))
        # collect colors
        for i in nb.prange(y_end - y_start):
            # explicitly make color an int for numba
            tex_y = int(step_y * (i + offset)) & (constants.TEX_HEIGHT - 1)
            if tex_y == 0:
                # TODO: figure out why this happens
                # subtracting by 1 removes texture repeating at bottom of wall
                tex_y -= 1
            color = int(texture[tex_x - 1][tex_y])
            if side == 0:
                # darken color using bitwise operators
                color = (color >> 1) & 8355711
            col[i] = color
    else:
        col = np.full((y_end - y_start,), color)
    for i in nb.prange(step):
        j = x + i
        if j < width:
            pixel_buffer[j][y_start:y_end] = col
    return pixel_buffer


"""UNOPTIMIZED CODE"""
'''
@jit(fastmath=True, nopython=True, parallel=True)
def fill_slice(screen_size, pixel_buffer, x, y_limits, side, step, element, texture, tex_x, color) -> np.ndarray:
    (width, height) = screen_size
    (y_start, y_end) = y_limits
    if element > 100:
        col = get_pixel_column(side, y_start, y_end, np.arange(y_end - y_start), texture, tex_x, step)
    else:
        col = np.full((y_end - y_start,), color)
    for i in nb.prange(step):
        j = x + i
        if j < width - 1:
            pixel_buffer[j][y_start : y_end] = col
    return pixel_buffer


@jit(fastmath=True, nopython=True, parallel=True, cache=CACHE, nogil=True)
def get_pixel_column(
    side: int,
    y_start: int,
    y_end: int,
    y_vals: np.ndarray,
    texture: np.ndarray,
    tex_x: int,
    steps: int
) -> np.ndarray:
    # How much to increase the texture coordinate per screen pixel
    step_y = 64.0 / (y_end - y_start)
    offset = y_start - (((constants.SIZE[1] + y_end - y_start) / 2))
    # collect colors
    y_vals = step_y * (y_vals + offset)
    for i in nb.prange(len(y_vals)):
        color = texture[tex_x - 1][int(y_vals[i])]
        if side == 0:
            # darken color using bitwise operators
            color = (color >> 1) & 8355711
        y_vals[i] = color
    return y_vals


@jit(fastmath=True, forceobj=True, cache=CACHE)
def cast_rays(
    screen,
    origin,
    direction,
    plane,
    grid_dict,
    pixel_buffer,
    images,
    step=constants.STEP,
    slow=False,
):
    """Cast rays perpendicular to <plane> in the direction of <direction> from <origin>.
    A ray is casted for every <step> taken from 0 to <width>.
    If a valid tile is hit by a row then the wall is drawn as a line.
    If slow is True, the screen is drawn after every step."""
    assert step >= 1, "Step must be greater than 0"
    assert step == 1 or step % 2 == 0, "Step must be 1 or even"
    # init vars
    (width, height) = screen_size = screen.get_rect().size
    # begin raycasting
    x = 0
    while x < width:
        ray = dda.get_ray(x, direction, plane, width)
        distance, side, element = dda.run_along_ray(origin, ray, grid_dict)[:]
        distance = abs(distance)
        if side == -1 or distance < 0.2:
            # ray did not collide with anything, so move to next x coordinate
            minor_step = step
            continue
        else:
            minor_step = step + int(distance // constants.INTERVAL)
            pixel_buffer = fill_wrapper(
                screen,
                screen_size,
                pixel_buffer,
                origin,
                x,
                ray,
                distance,
                side,
                element,
                minor_step,
                images,
            )
        x += minor_step
    return pixel_buffer
'''
