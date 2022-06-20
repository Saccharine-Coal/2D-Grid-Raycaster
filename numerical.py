from __future__ import annotations

import math

# default is 1e-9
# lower the rel tol since pygame uses integers for pixel representation.
# Extra precision on float is pointless otherwise.
# precision is not needed
REL_TOL = 1e-3
# for values near 0
ABS_TOL = 1e-3


def is_close(a, b) -> bool:
    """Basically float == float. But float == float should not be used!"""
    if b == 0 and isinstance(b, int):
        # b is 0
        return math.isclose(a, b, rel_tol=REL_TOL, abs_tol=ABS_TOL)
    return math.isclose(a, b, rel_tol=REL_TOL, )


def is_above_or_eq(a, b) -> bool:
    """a >= b"""
    return is_close(a, b) or a > b


def is_below_or_eq(a, b) -> bool:
    """a < b"""
    return is_close(a, b) or a < b


def is_above(a, b) -> bool:
    """a > b"""
    return not is_close(a, b) and a > b


def is_below(a, b) -> bool:
    """a < b"""
    return not is_close(a, b) and a < b


def is_in(val, lower, upper, inclusive=True) -> bool:
    """If a float/int is contained within a boundary [lower, upper].
    @param: inclusive=False => val in (lower, upper) not including bounds"""
    if inclusive:
        # lower <= val <= upper
        return is_above_or_eq(val, lower) and is_below_or_eq(val, upper)
    # lower < val < upper
    return is_above(val, lower) and is_below(val, upper)


def is_array_close(arr_1: tuple[float], arr_2: tuple[float]) -> bool:
    """Determine if an array of floats are close.
    @return bool: True if all floats are close, False otherwise.
    """
    if len(arr_1) != len(arr_2):
        # not equivalent nor close if the size is different
        return False
    return all(is_close(a, b) for a, b in zip(arr_1, arr_2))


def is_array_in(arr, iter_of_arr) -> bool:
    """Determine if an array is an iterable of arrays."""
    if len(iter_of_arr) == 0:
        # empty list
        return False
    return any(is_array_close(arr, val) for val in iter_of_arr)


def distance(start, end) -> float:
    """Euclidean distance for any dimension."""
    diff_sq = tuple(pow(b-a, 2) for a, b in zip(start, end))
    return math.sqrt(sum(diff_sq))


if __name__ == "__main__":
    x = 0.3333
    y = 0.3233
    print(is_above(x, y))
    print(is_above_or_eq(x, y))
