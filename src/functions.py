import math


def rotate_by_step(xy, rad) -> tuple:
    x, y = xy[:]
    cos, sin = math.cos(rad), math.sin(rad)
    nx = (x * cos) - (y * sin)
    ny = (x * sin) + (y * cos)
    return (nx, ny)


def darken_rgb(rgb, sub) -> tuple:
    def sub_and_limit(val, sub, ceil=255, floor=0):
        subtracted = val - sub
        return min(max(subtracted, floor), 255)

    r = sub_and_limit(rgb[0], sub)
    g = sub_and_limit(rgb[1], sub)
    b = sub_and_limit(rgb[2], sub)
    return (r, g, b)
