# coding: utf-8

import sys
import pygame
import random

from pygame.locals import *


def do_rects_overlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b.
        if is_point_inside_rect(a.left, a.top, b) or is_point_inside_rect(a.left, a.bottom, b) or \
           is_point_inside_rect(a.right, a.top, b) or is_point_inside_rect(a.right, a.bottom, b):
            return True
    
    return False


def is_point_inside_rect(x, y, rect):
    if x > rect.left and x < rect.right and y > rect.top and y < rect.bottom:
        return True
    else:
        return False


# Set up a game.
pygame.init()
main_clock = pygame.time.Clock()

# Set up the window.
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

windows_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Collision Detection')

# Set up direction variables.
DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9
DIRECTIONS = [DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT]

MOVESPEED = 6

# Set up the colors.
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
WHEAT = (245, 222, 179)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
DEEPSKYBLUE = (0, 191, 255)
LAVENDER = (230, 230, 250)
WHITE = (255, 255, 255)
COLORS = [RED, GREEN, BLUE, GRAY, PURPLE, TEAL, YELLOW,
          ORANGE, BROWN, DEEPSKYBLUE, LAVENDER, WHITE]

# Set up the bouncer and food data structures.
BOUNCER_WIDTH = 50
BOUNCER_HEIGHT = 50
white_bouncer = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH),
                                     random.randint(0, WINDOW_HEIGHT),
                                     BOUNCER_WIDTH, BOUNCER_HEIGHT),
                'dir': random.choice(DIRECTIONS),
                'color': WHITE
                }
green_bouncer = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH),
                                     random.randint(0, WINDOW_HEIGHT),
                                     BOUNCER_WIDTH, BOUNCER_HEIGHT),
                'dir': random.choice(DIRECTIONS),
                'color': GREEN
                }

bouncers = [white_bouncer, green_bouncer]
food_counter = 0
NEWFOOD = 40 // len(bouncers)
FOODSIZE = 20

foods = []
foods_color = []
for i in range(20):
    foods.append(
            {'food': pygame.Rect(
            random.randint(0, WINDOW_WIDTH-FOODSIZE), random.randint(0, WINDOW_HEIGHT-FOODSIZE),
            FOODSIZE, FOODSIZE) ,
             'color': random.choice(COLORS)
             }
    )

# Run the game loop.
while True:
    # Check for the QUIT event:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    food_counter += 1
    if food_counter >= NEWFOOD:
        # Add new food
        food_counter = 0
        foods.append(
            {'food': pygame.Rect(
            random.randint(0, WINDOW_WIDTH-FOODSIZE), random.randint(0, WINDOW_HEIGHT-FOODSIZE),
            FOODSIZE, FOODSIZE) ,
             'color': random.choice(COLORS)
             }
        )
    
    # Draw the black background onto the surface.
    windows_surface.fill(BLACK)
    
    for bouncer in bouncers:
        # Move the bouncer data structure.
        if bouncer['dir'] == DOWNLEFT:
            bouncer['rect'].left -= MOVESPEED
            bouncer['rect'].top += MOVESPEED
        if bouncer['dir'] == DOWNRIGHT:
            bouncer['rect'].left += MOVESPEED
            bouncer['rect'].top += MOVESPEED
        if bouncer['dir'] == UPLEFT:
            bouncer['rect'].left -= MOVESPEED
            bouncer['rect'].top -= MOVESPEED
        if bouncer['dir'] == UPRIGHT:
            bouncer['rect'].left += MOVESPEED
            bouncer['rect'].top -= MOVESPEED
        
        # Check if the bouncer has move out of the window
        if bouncer['rect'].top < 0:
            if bouncer['dir'] == UPLEFT:
                bouncer['dir'] = DOWNLEFT
            if bouncer['dir'] == UPRIGHT:
                bouncer['dir'] = DOWNRIGHT
        if bouncer['rect'].bottom > WINDOW_HEIGHT:
            if bouncer['dir'] == DOWNLEFT:
                bouncer['dir'] = UPLEFT
            if bouncer['dir'] == DOWNRIGHT:
                bouncer['dir'] = UPRIGHT
        if bouncer['rect'].left < 0:
            if bouncer['dir'] == DOWNLEFT:
                bouncer['dir'] = DOWNRIGHT
            if bouncer['dir'] == UPLEFT:
                bouncer['dir'] = UPRIGHT
        if bouncer['rect'].right > WINDOW_WIDTH:
            if bouncer['dir'] == DOWNRIGHT:
                bouncer['dir'] = DOWNLEFT
            if bouncer['dir'] == UPRIGHT:
                bouncer['dir'] = UPLEFT
        
        # Draw the bouncer onto the surface.
        pygame.draw.rect(windows_surface, bouncer['color'], bouncer['rect'])
    
        # Check if the bouncer has intersected with any food squares.
        for food in foods[:]:
            if do_rects_overlap(bouncer['rect'], food['food']):
                foods.remove(food)
    
    # Draw the foods.
    for i in range(len(foods)):
        pygame.draw.rect(windows_surface, foods[i]['color'], foods[i]['food'])
    
    # Draw the window onto the screen.
    pygame.display.update()
    main_clock.tick(40)
