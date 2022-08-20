# TODO: docstring
import os

import pygame as pg
import numpy as np


def load_as_array(path, colorkey=None) -> np.ndarray:
    # TODO: docstring
    assert os.path.exists(path), "Not a valid path!"
    if colorkey:
        surface = pg.image.load(path, ".png").convert_alpha()
        surface.set_colorkey(colorkey)
        return pg.surfarray.pixels2d(surface)
    return pg.surfarray.pixels2d(pg.image.load(path, ".png").convert_alpha())


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
    # TODO: docstring
    if colorkey:
        # TODO: doesn't work
        for i in range(len(pixel_buffer)):
            for j in range(len(pixel_buffer[i])):
                pixel_buffer[i][j] = original_surface.unmap_rgb(pixel_buffer[i][j])
        sur = pg.surfarray.make_surface(pixel_buffer)
        sur.set_colorkey(colorkey)
        surface.blit(sur, (0, 0))
    else:
        pg.surfarray.blit_array(surface, pixel_buffer)
