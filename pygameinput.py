# coding: utf-8

import sys
import pygame
import random

from pygame.locals import *


# Set up a game.
pygame.init()
main_clock = pygame.time.Clock()

# Set up the window.
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

windows_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Input')

# Set up movements variables.
move_left = False
move_right = False
move_up = False
move_down = False

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
player = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH),
                                     random.randint(0, WINDOW_HEIGHT),
                                     BOUNCER_WIDTH, BOUNCER_HEIGHT),
                'color': WHITE
                }

food_counter = 0
NEWFOOD = 40
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
    # Check for events.
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # Change the keyboard variables.
            if event.key == K_LEFT or event.key == ord('a'):
                move_right = False
                move_left = True
            if event.key == K_RIGHT or event.key == ord('d'):
                move_left = False
                move_right = True
            if event.key == K_UP or event.key == ord('w'):
                move_down = False
                move_up = True
            if event.key == K_DOWN or event.key == ord('s'):
                move_up = False
                move_down = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                move_left = False
            if event.key == K_RIGHT or event.key == ord('d'):
                move_right = False
            if event.key == K_UP or event.key == ord('w'):
                move_up = False
            if event.key == K_DOWN or event.key == ord('s'):
                move_down = False
            if event.key == ord('x'):
                player['rect'].top = random.randint(0, WINDOW_HEIGHT-player['rect'].height)
                player['rect'].left = random.randint(0, WINDOW_WIDTH-player['rect'].width)
        if event.type == MOUSEBUTTONUP:
            foods.append(
                {
                    'food': pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE),
                    'color': random.choice(COLORS)
                }
            )
    
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
    
    # Move the player.
    if move_down and player['rect'].bottom < WINDOW_HEIGHT:
        player['rect'].top += MOVESPEED
    if move_up and player['rect'].top > 0:
        player['rect'].top -= MOVESPEED
    if move_left and player['rect'].left > 0:
        player['rect'].left -= MOVESPEED
    if move_right and player['rect'].right < WINDOW_WIDTH:
        player['rect'].left += MOVESPEED
    
    # Draw the player onto the surface.
    pygame.draw.rect(windows_surface, player['color'], player['rect'])

    # Check if the bouncer has intersected with any food squares.
    for food in foods[:]:
        if player['rect'].colliderect(food['food']):
            foods.remove(food)
    
    # Draw the foods.
    for i in range(len(foods)):
        pygame.draw.rect(windows_surface, foods[i]['color'], foods[i]['food'])
    
    # Draw the window onto the screen.
    pygame.display.update()
    main_clock.tick(40)
