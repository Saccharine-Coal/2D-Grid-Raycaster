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
import raycast


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
        player.handle_event(events, pressed, dt)
        return running

    def clear_screen():
        """Abstracted function: Clear the game screen"""
        screen.fill((0, 0, 0))

    def draw_textures():
        """Abstracted function: Draw textured tiles"""
        buffer.draw_buffer(pixel_buffer, screen, screen)

    def draw_floor():
        rect = pg.Rect((0, int(height / 2)), (width, int(height / 2)))
        pg.draw.rect(screen, constants.FLOOR, rect)

    def draw_celing():
        """Abstracted function: Draw game world ceiling"""
        rect = pg.Rect((0, 0), (width, int(height / 2)))
        pg.draw.rect(screen, constants.CEILING, rect)

    def draw_text():
        """Abstracted function: Draw game performance statistics"""
        text = font.render(f"fps={int(fps)}", False, (0, 255, 0))
        screen.blit(text, (screen.get_rect().centerx, 0))

    def update_display():
        """Abstracted function: Update game screen"""
        # Flip the display
        pg.display.flip()

    # Construct game objects
    player = game_objects.Player((2, 2))
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
    empty_buffer = np.copy(
        pixel_buffer
    )  # np.tile(np.arange(constants.SIZE[1]), (constants.SIZE[0], 1))
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
    local_surface = screen.copy()
    local_surface.set_colorkey((0, 0, 0))
    # Main game LOOP
    running = True
    while running:
        dt = clock.tick(constants.FPS)
        fps = clock.get_fps()
        # print(f"fps={fps}")
        # HANDLE EVENTS
        running = handle_events()  # Run until the user asks to quit
        # DRAW
        clear_screen()
        pixel_buffer = np.copy(empty_buffer)
        # cast rays and draw walls
        local_surface.fill((0, 0, 0))
        pixel_buffer = raycast.cast_rays(
            screen.get_rect().size,
            player.xy,
            player.direction,
            player.plane,
            game_objects.GRID,
            np.copy(empty_buffer),
            images,
            step=1,
            slow=False,
        )
        # draw texture
        draw_textures()
        # draw the minimap
        mini_map.draw(screen, grid, player)
        # draw fps
        draw_text()
        update_display()


main()
