import numba as nb

import constants


def get_ray(x, direction, plane, width):
    """Construct a ray that is perpendicular to plane in the given direction
    for given screen position on screen x-axis."""
    (direction_x, direction_y) = direction
    (plane_x, plane_y) = plane
    camera_x = ((2 * x) / width) - 1
    ray_dir = (
        direction_x + (plane_x * camera_x),
        direction_y + (plane_y * camera_x),
    )
    return ray_dir


def run_along_ray(start, direction_ray, grid_dict) -> tuple:
    """Apply the DDA from <start> along <direction_ray> until
    a valid tile is encountered in <grid_dict> or max_iterations if reached.
    The DDA algorithm decomposes <direction_ray> into side side distances
    and takes integer steps along <direction_ray>. The algorithm
    runs along the minimum x, y combination."""
    # grid of integers
    # start may be floats
    # get the int values of the start xy
    (start_x, start_y) = start
    int_map = (int(start_x), int(start_y))
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
    element = grid_dict[int(int_map[0])][
        int(int_map[1])
    ]  # grid_dict.get(tuple(int_map))
    perp_wall_dist = calculate_wall_distance(tuple(side_dist), tuple(delta_dist), side)
    # wall_x = calculate_wall_x()
    return perp_wall_dist, side, tuple(int_map)


def construct_deltas(ray_dir, pos, int_map) -> tuple:
    """Construct <step>, <side_dist>, and <dist> delta pairs.
    <step> represents an integer step along x/y.
    <side_dist> represents the total distance along x/y.
    <delta_dist> represents the distance along x/y that moves a
    whole integer step."""
    # ||ray_dir|| = 1 since ray_dir is normalized
    # delta_dist = abs(||ray_dir||/ray_dir_x, ||ray_dir||/ray_dir_y)
    # delta_dist = abs(1/ray_dir_x, 1/ray_dir_y)
    # handle division by 0
    INF_VAL = 1e20
    (ray_dir_x, ray_dir_y) = ray_dir
    (pos_x, pos_y) = pos
    (int_x, int_y) = int_map
    if ray_dir_x == 0 or ray_dir_y == 0:
        if ray_dir_x == 0:
            delta_dist = (INF_VAL, abs(1 / ray_dir_y))
        else:
            delta_dist = (abs(1 / ray_dir_x), INF_VAL)
    else:
        # no division by 0
        delta_dist = (abs(1 / ray_dir_x), abs(1 / ray_dir_y))
    (delta_dist_x, delta_dist_y) = delta_dist
    # calculate step and initial side dist
    if ray_dir_x < 0:
        step_x = -1
        side_dist_x = (pos_x - int_map[0]) * delta_dist_x
    else:
        step_x = 1
        side_dist_x = (int_map[0] + 1.0 - pos_x) * delta_dist_x
    if ray_dir_y < 0:
        step_y = -1
        side_dist_y = (pos_y - int_map[1]) * delta_dist_y
    else:
        step_y = 1
        side_dist_y = (int_map[1] + 1.0 - pos_y) * delta_dist_y
    side_dist = (side_dist_x, side_dist_y)
    step = (step_x, step_y)
    delta_dist = (delta_dist_x, delta_dist_y)
    return step, side_dist, delta_dist


def hit_wall(int_map, grid_dict, max_iterations) -> bool:
    """Check if a valid tile has been hit by ray or run
    has iterated max_iterations times."""
    element = grid_dict[int_map[0]][
        int_map[1]
    ]  # grid_dict.setdefault(tuple(int_map), -1)
    if element > 0 or max_iterations == 0:
        # collision or max_iterations has been met
        return True
    return False


def calculate_wall_distance(side_dist, delta_dist, side) -> float:
    """Calculates euclidean distance of <start> to intersection point.
    Handles which side of a cube is hit. If no wall is hit returns infinity."""
    if side == 0:
        # side is vertical
        perp_wall_dist = side_dist[0] - delta_dist[0]
    else:
        # side == 1
        # side is horizontal
        perp_wall_dist = side_dist[1] - delta_dist[1]
    return perp_wall_dist


def walk_along_ray(int_map, step, side_dist, delta_dist) -> tuple:
    """Take a <step> along a given ray by following a <delta_dist>.
    Returns new <side_dist>, new <int_map>, and <side>."""
    (int_x, int_y) = int_map
    (step_x, step_y) = step
    (side_dist_x, side_dist_y) = side_dist
    (delta_dist_x, delta_dist_y) = delta_dist
    if side_dist_x < side_dist_y:
        # add to our x dist tracker
        side_dist_x += delta_dist_x
        # take a step along x
        int_x += step_x
        side = 0
    else:
        side_dist_y += delta_dist_y
        int_y += step_y
        side = 1
    return (side_dist_x, side_dist_y), (int_x, int_y), side


# compile entire file as jit
nb.jit_module(nopython=True, fastmath=True, cache=True)
