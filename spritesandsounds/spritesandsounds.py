# -*- coding: utf-8 -*-

import sys
import time
import random
import pygame

from pygame.locals import *


# Set up pygame.
pygame.init()
main_clock = pygame.time.Clock()

# Set up the window.
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Sprites and Sound')

# Set up the colors.
LACK = (0, 0, 0)
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
BLACK = (0, 0, 0)
COLORS = [RED, GREEN, BLUE, GRAY, PURPLE, TEAL, YELLOW,
          ORANGE, BROWN, DEEPSKYBLUE, LAVENDER, WHITE]

# Set up the block data structure.
player = pygame.Rect(300, 100, 50, 50)
player_image = pygame.image.load('player.png')
player_stretched_image = pygame.transform.scale(player_image, (50, 50))
food_image = pygame.image.load('cherry.png')
foods = []
for i in range(20):
    foods.append(
        pygame.Rect(random.randint(0, WINDOW_WIDTH-20),random.randint(0, WINDOW_HEIGHT-20),20, 20)
    )

food_counter = 0
NEWFOOD = 40

# Set up keyboard variables.
move_left = False
move_right = False
move_up = False
move_down = False

MOVESPEED = 6

# Set up music.
pick_up_sound = pygame.mixer.Sound('pickup.wav')
pygame.mixer.music.load('background.mid')
pygame.mixer.music.play(-1, 0.0)
music_playing = True

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
                player.top = random.randint(0, abs(WINDOW_HEIGHT-player.height))
                player.left = random.randint(0, abs(WINDOW_WIDTH-player.width))
            if event.key == ord('m'):
                if music_playing:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                music_playing = not music_playing
        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0]-10, event.pos[1]-10, 20, 20))
    
    food_counter += 1
    if food_counter >= NEWFOOD:
        # Add new food.
        food_counter = 0
        foods.append(
            pygame.Rect(
                random.randint(0, WINDOW_WIDTH - 20), random.randint(0, WINDOW_HEIGHT - 20), 20, 20)
        )
    
    # Draw the black background onto the surface.
    window_surface.fill(BLACK)
    
    # Move the player.
    if move_down and player.bottom < WINDOW_HEIGHT:
        player.top += MOVESPEED
    if move_up and player.top > 0:
        player.top -= MOVESPEED
    if move_left and player.left > 0:
        player.left -= MOVESPEED
    if move_right and player.right < WINDOW_WIDTH:
        player.right += MOVESPEED
    
    # Draw the block onto the surface.
    window_surface.blit(player_stretched_image, player)
    
    # Check if the block has intersected with any food squares.
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
            player_stretched_image = pygame.transform.scale(player_image,
                (player.width, player.height))
            if music_playing:
                pick_up_sound.play()
                
    # Draw the food.
    for food in foods:
        window_surface.blit(food_image, food)
    
    # Draw the window onto the screen.
    pygame.display.update()
    main_clock.tick(40)
