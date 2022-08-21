import numpy as np

import constants



def get_color(
    unsigned int side,
    unsigned int[:, :]texture,
    unsigned int tex_x,
    int tex_y
):
    cdef unsigned int color = texture[tex_x - 1][int(tex_y)]
    if side == 0:
        # darken color using bitwise operators
        return (color >> 1) & 8355711
    return color


VECTORIZED = np.vectorize(get_color)


def get_pixel_column(
    unsigned int side,
    unsigned int y_start,
    unsigned int y_end,
    unsigned int[:] y_vals,
    unsigned int[:, :] texture,
    unsigned int tex_x
):
    """Draw section of a wall encountered by ray."""
    assert all(isinstance(val, int) for val in (side, y_start, y_end, tex_x)), "Not int!"
    # How much to increase the texture coordinate per screen pixel
    cdef long double step_y = 64.0 / (y_end - y_start)
    cdef int offset = int(y_start - (((constants.SIZE[1] + y_end - y_start)/ 2)))
    # collect colors

    def elementwise(int y):
        #assert y >= 0, f"val={y} < 0!"
        return get_color(side, texture, tex_x, y)
    # print(split(np.multiply(step_y, np.add(y_vals, offset))))
    return np.vectorize(elementwise)(np.multiply(step_y, np.add(y_vals, offset)))

'''
def split(array):
    groups = []
    last_list = None
    for i in range(len(array)):
        current = array[i]
        if last_list is None:
            last_list = [current]
        else:
            if last_list[0] == current:
                last_list.append(current)
            else:
                groups.append((last_list))
                last_list = [current]
    return groups
'''
