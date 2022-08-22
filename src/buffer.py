# TODO: docstring
import os

import pygame as pg
import numpy as np


def load_as_array(path, scale=1) -> np.ndarray:
    # TODO: docstring
    assert os.path.exists(path), "Not a valid path!"
    surface = pg.image.load(path, ".png").convert_alpha()
    rgb_array = pg.surfarray.pixels3d(surface)#.astype("uint32")
    int_array = np.zeros((64, 64)).astype("uint32")
    for i in range(len(rgb_array)):
        for j in range(len(rgb_array[i])):
            # convert to int 
            int_array[i][j]= int(pg.Color(rgb_array[i][j]))
    return int_array

def construct_pixel_buffer(surface) -> np.ndarray:
    # TODO: docstring
    return pg.surfarray.pixels2d(surface)


def clear_buffer(pixel_buffer) -> np.ndarray:
    return np.full((pixel_buffer.shape), (0, 0, 0))


def change_color(pixel_buffer, x, y, color) -> np.ndarray:
    # TODO: docstring
    pixel_buffer[x][y] = color
    return pixel_buffer

def change_column(pixel_buffer, x, y_vals, y_start=0) -> np.ndarray:
    # TODO: docstring
    pixel_buffer[x][y_start:y_start + len(y_vals)] = y_vals
    return pixel_buffer

def draw_buffer(pixel_buffer, surface, original_surface, colorkey=None) -> None:
    rgb_array = pg.surfarray.array3d(surface).copy()
    #rgb_array = int_to_rgb(pixel_buffer, rgb_array, pixel_buffer.shape)
    pg.surfarray.blit_array(surface, pixel_buffer >> 8)

import numba as nb


@nb.jit(nopython=True, parallel=True, nogil=True)
def int_to_rgb(int_array, rgb_array, shape):
    for i in nb.prange(shape[0]):
        for j in nb.prange((shape[1])):
            color = int_array[i][j]
            R = (color >> 24) & 0xFF
            G = (color >> 16) & 0xFF
            B = (color >> 8) & 0xFF
            A = (color) & 0xFF
            rgb_array[i][j] = (R, G, B)
    return rgb_array

