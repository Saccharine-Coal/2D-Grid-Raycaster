import numpy as np

import constants



def get_color(side, texture, tex_x, tex_y):
    if tex_y == 0:
        return 0
    color = texture[tex_x - 1][int(tex_y)]
    if side == 0:
        # darken color using bitwise operators
        return (color >> 1) & 8355711
    return color


VECTORIZED = np.vectorize(get_color)


def get_pixel_column(side, y_start, y_end, y_vals, texture, tex_x):
    """Draw section of a wall encountered by ray."""
    assert all(isinstance(val, int) for val in (side, y_start, y_end, tex_x)), "Not int!"
    height_y = y_end - y_start
    # How much to increase the texture coordinate per screen pixel
    step_y = 64 / height_y
    offset = int(y_start - (constants.SIZE[1] / 2) + (height_y / 2))
    # collect colors

    def elementwise(y):
        return get_color(side, texture, tex_x, y)

    return np.vectorize(elementwise)(step_y * (y_vals + offset))


'''
def get_pixel_array(array, side, y_start, y_end, row, texture, tex_x):
    def rowwise(row):
        return get_pixel_column(side, y_start, y_end, row, texture, tex_x)
    return np.array(map(rowwise, array))
'''
