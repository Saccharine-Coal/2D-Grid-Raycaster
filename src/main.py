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
import buffer


def main() -> None:
    """Run the game. Initializes pygame and game objects.
    Handles user input, updates game objects, and draws to the screen."""

    def handle_events():
        """Abstracted function: Handle all game events"""
        running = True
        # get events
        events = pg.event.get()
        # get pressed keys
        pressed = pg.key.get_pressed()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
        player.handle_event(events, pressed)
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
    font = pg.font.SysFont(pg.font.get_default_font(), 24)  # create font object
    clock = pg.time.Clock()  # create clock object
    # Set up the drawing window
    size = (width, height) = constants.SIZE
    screen = pg.display.set_mode(size)
    sur_copy = screen.copy()
    rect = pg.Rect((0, int(height / 2)), (width, int(height / 2)))
    pg.draw.rect(sur_copy, constants.FLOOR, rect)
    rect = pg.Rect((0, 0), (width, int(height / 2)))
    pg.draw.rect(sur_copy, constants.CEILING, rect)
    pixel_buffer = buffer.construct_pixel_buffer(sur_copy)
    empty_buffer = np.copy(pixel_buffer)
    arr_1 = buffer.load_as_array("../img/bluestone.png")
    arr_2 = buffer.load_as_array("../img/redbrick.png")
    arr_3 = buffer.load_as_array("../img/wood.png")
    arr_4 = buffer.load_as_array("../img/colorstone.png")
    arr_5 = buffer.load_as_array("../img/mossy.png")
    arr_6 = buffer.load_as_array("../img/purplestone.png")
    arr_7 = buffer.load_as_array("../img/eagle.png")
    arr_8 = buffer.load_as_array("../img/greystone.png")
    arr_9 = buffer.load_as_array("../img/greenlight.png")
    arr_10 = buffer.load_as_array("../img/barrel.png")
    arr_11 = buffer.load_as_array("../img/pillar.png")
    images = (
        arr_1,
        arr_2,
        arr_3,
        arr_4,
        arr_5,
        arr_6,
        arr_7,
        arr_8,
        arr_9,
        arr_10,
        arr_11,
    )
    # Main game LOOP
    running = True
    while running:
        clock.tick(constants.FPS)
        # HANDLE EVENTS
        running = handle_events()  # Run until the user asks to quit
        # DRAW
        clear_screen()
        pixel_buffer = np.copy(empty_buffer)
        # cast rays and draw walls
        cast_rays(
            screen,
            player.xy,
            player.direction,
            player.plane,
            grid,
            width,
            height,
            pixel_buffer,
            images,
            step=constants.STEP,
            slow=constants.SLOW,
        )
        # draw the minimap
        mini_map.draw(screen, grid, player)
        # draw fps
        draw_text()
        update_display()


def cast_rays(
    screen,
    origin,
    direction,
    plane,
    grid_dict,
    width,
    height,
    pixel_buffer,
    images,
    step=1,
    slow=False,
):
    """Cast rays perpendicular to <plane> in the direction of <direction> from <origin>.
    A ray is casted for every <step> taken from 0 to <width>.
    If a valid tile is hit by a row then the wall is drawn as a line.
    If slow is True, the screen is drawn after every step."""

    def get_ray(x, direction, plane, width):
        """Construct a ray that is perpendicular to plane in the given direction
        for given screen position on screen x-axis."""
        camera_x = ((2 * x) / width) - 1
        ray_dir = constants.Point2(
            direction.x + (plane.x * camera_x),
            direction.y + (plane.y * camera_x),
        )
        return ray_dir

    def get_color(distance, side, element):
        """Get the color for given element and darken color
        depending on side hit and distance from start."""
        color = constants.INT_TO_COLOR.get(element)
        # dist -> depth -> darker
        ratio = 1 - (1 / (distance + 1))
        if side == 0:
            # darken color
            color = functions.darken_rgb(color, 50)
        color = functions.darken_rgb(color, ratio * 150)
        return color

    def get_y_limits(distance, height):
        """Get the start values of walls to be drawn along y-axis."""
        line_height = height / distance
        y_start = int((-line_height + height) / 2)
        if y_start < 0:
            y_start = 0
        y_end = int((line_height + height) / 2)
        if y_end >= height:
            y_end = height - 1
        return (y_start, y_end)

    def draw_wall(screen, color, x, y_limits, step, slow, pixel_buffer, tex_x):
        """Draw section of a wall encountered by ray."""
        (y_start, y_end) = y_limits
        for i in range(step):
            pg.draw.aaline(screen, color, (x + i, y_start), (x + i, y_end))
        # for y in range(y_start, y_end+1):
        #    for i in range(step):
        #        pixel_buffer = buffer.change_color(pixel_buffer, x + i, y, color)
        return pixel_buffer

    def draw_textured_wall(
        screen, side, x, y_limits, slow, pixel_buffer, tex_x, texture
    ):
        """Draw section of a wall encountered by ray."""

        def wrapper(tex_y):
            """Get color of texture at (tex_x, tex_y) and darken by certain side."""
            color = texture[tex_x - 1][tex_y]
            if side == 0:
                # darken color using bitwise operators
                return (color >> 1) & 8355711
            return color

        (y_start, y_end) = y_limits
        height = y_end - y_start
        # How much to increase the texture coordinate per screen pixel
        step = 64 / height
        # collect colors
        numbers = (
            min(
                int(
                    (y_start - (constants.SIZE[1] / 2) + (height / 2)) * step
                    + (step * y)
                ),
                63,
            )
            for y in range(height + 1)
        )
        colors = np.fromiter(map(wrapper, numbers), dtype=texture.dtype)
        # colors = np.frompyfunc(wrapper, 1, 1)(numbers)
        # print(colors.shape)
        return buffer.change_column(pixel_buffer, x, colors, y_start=y_start)

    def calculate_wall_x(start, distance, ray) -> float:
        if side == 0:
            x = start.y + distance * ray.y
        elif side == 1:
            x = start.x + distance * ray.x
        else:
            x = float("inf")
        # float val
        return x - math.floor(x)

    def calculate_texture_x(side, wall_x, ray) -> int:
        x = math.floor(wall_x * constants.TEX_WIDTH) - 1
        if side == 0 and ray.x > 0:
            x = constants.TEX_WIDTH - x - 1
        if side == 1 and ray.y < 0:
            x = constants.TEX_WIDTH - x - 1
        return x

    assert step >= 1, "Step must be greater than 0"
    local_sur = screen.copy()
    local_sur.set_colorkey((0, 0, 0))
    # begin raycasting
    for x in range(0, width, step):
        ray = get_ray(x, direction, plane, width)
        dist, side, element = run_along_ray(origin, ray, grid_dict)[:]
        if side == -1:
            # ray did not collide with anything, so move to next x coordinate
            continue
        y_limits = get_y_limits(dist, height)
        tex_x = calculate_texture_x(side, calculate_wall_x(origin, dist, ray), ray)
        if element >= 100:
            pixel_buffer = draw_textured_wall(
                screen,
                side,
                x,
                y_limits,
                slow,
                pixel_buffer,
                tex_x,
                images[constants.INT_TO_INDEX[element]],
            )
        else:
            color = get_color(dist, side, element)
            pixel_buffer = draw_wall(
                local_sur, color, x, y_limits, step, slow, pixel_buffer, tex_x
            )
    buffer.draw_buffer(pixel_buffer, screen, screen)
    screen.blit(local_sur, (0, 0))


def run_along_ray(start, direction_ray, grid_dict):
    """Apply the DDA from <start> along <direction_ray> until
    a valid tile is encountered in <grid_dict> or max_iterations if reached.
    The DDA algorithm decomposes <direction_ray> into side side distances
    and takes integer steps along <direction_ray>. The algorithm
    runs along the minimum x, y combination."""

    def construct_deltas(ray_dir, pos, int_map):
        """Construct <step>, <side_dist>, and <dist> delta pairs.
        <step> represents an integer step along x/y.
        <side_dist> represents the total distance along x/y.
        <delta_dist> represents the distance along x/y that moves a
        whole integer step."""
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

    def hit_wall(int_map, grid_dict, max_iterations) -> bool:
        """Check if a valid tile has been hit by ray or run
        has iterated max_iterations times."""
        element = grid_dict.setdefault(tuple(int_map), -1)
        if element > 0 or max_iterations == 0:
            # collision or max_iterations has been met
            return True
        return False

    def calculate_wall_distance(side_dist, delta_dist, side) -> float:
        """Calculates euclidean distance of <start> to intersection point.
        Handles which side of a cube is hit. If no wall is hit returns infinity."""
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
    # wall_x = calculate_wall_x()
    return perp_wall_dist, side, element


def walk_along_ray(int_map, step, side_dist, delta_dist):
    """Take a <step> along a given ray by following a <delta_dist>.
    Returns new <side_dist>, new <int_map>, and <side>."""
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
