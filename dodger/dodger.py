# -8- coding: utf-8 -*-

import sys
import random
import pygame

from pygame.locals import *


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 40
BADDIE_MIN_SIZE = 10
BADDIE_MAX_SIZE = 20
BADDIE_MIN_SPEED = 1
BADDIE_MAX_SPEED = 5
ADD_NEW_BADDIE_RATE = 10
PLAYER_MOVE_RETE = 5

# Set up levels data.
LEVEL1 = [
    ADD_NEW_BADDIE_RATE,
    BADDIE_MIN_SIZE,
    BADDIE_MAX_SIZE,
    BADDIE_MIN_SPEED,
    BADDIE_MAX_SPEED,
    FPS
]
LEVEL2 = [LEVEL1[0] - 1, LEVEL1[1], LEVEL1[2], LEVEL1[3], LEVEL1[4], LEVEL1[5]]
LEVEL3 = [LEVEL1[0] - 2, LEVEL1[1], LEVEL1[2], LEVEL1[3], LEVEL1[4], LEVEL1[5]]
LEVEL4 = [LEVEL1[0] - 3, LEVEL1[1], LEVEL1[2], LEVEL1[3], LEVEL1[4], LEVEL1[5]]
LEVEL5 = [LEVEL1[0] - 4, LEVEL1[1], LEVEL1[2], LEVEL1[3], LEVEL1[4], LEVEL1[5]]
LEVEL6 = [LEVEL1[0] - 5, LEVEL1[1], LEVEL1[2], LEVEL1[3], LEVEL1[4], LEVEL1[5]]


def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


def player_has_hit_baddie(player_rect, baddies):
    for baddie in baddies:
        if player_rect.colliderect(baddie['rect']):
            return True
    return False


def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def read_top_score():
    try: 
        with open(r'.\config.ini') as conf:
            score = int(conf.readline().strip())
            return score
    except(FileNotFoundError, ValueError):
        return 0


def write_top_score(score):
    try:
        with open(r'.\config.ini', 'w') as conf:
            conf.write(str(score))
    except(OSError):
        pass


def terminate():
    window_surface.fill(BACKGROUND_COLOR)
    draw_text('GOOD BYE', font, window_surface,
              WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2)
    pygame.display.update()
    main_clock.tick(0.8)
    pygame.quit()
    sys.exit()


# Set up pygame, the window, and the mouse cursor.
pygame.init()
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
game_over_sound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.
player_image = pygame.image.load('player.png')
player_rect = player_image.get_rect()
baddie_image = pygame.image.load('baddie.png')

# Show the "Start" screen.
draw_text('Dodger', font, window_surface, WINDOW_WIDTH / 2 - 60, WINDOW_HEIGHT // 3)
draw_text('Press a key to start.', font, window_surface, WINDOW_WIDTH / 2 - 150,
          WINDOW_HEIGHT / 3 + 150)
pygame.display.update()
wait_for_player_to_press_key()

top_score = read_top_score()


while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    level = 1
    player_rect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
    move_left, move_right, move_up, move_down = False, False, False, False
    reverse_cheat = False
    slow_cheat = False
    baddie_add_counter = 0
    pygame.mixer.music.play(-1, 0.0)
    
    while True:
        # The game loop runs while the game part is playing.
        score += 1  # Increase score.
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            
            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverse_cheat = True
                if event.key == ord('x'):
                    slow_cheat = True
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
                if event.key == ord('z'):
                    reverse_cheat = False
                    #score = 0
                if event.key == ord('x'):
                    slow_cheat = False
                    #score = 0
                if event.key == K_ESCAPE:
                    terminate()
                
                if event.key == K_LEFT or event.key == ord('a'):
                    move_left = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    move_right = False
                if event.key == K_UP or event.key == ord('w'):
                    move_up = False
                if event.key == K_DOWN or event.key == ord('s'):
                    move_down = False
            
            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                player_rect.move_ip(event.pos[0] - player_rect.centerx,
                                    event.pos[1] - player_rect.centery)
        
        # Add new baddies at the top of the screen, if needed.
        if not reverse_cheat and not slow_cheat:
            baddie_add_counter += 1
        if baddie_add_counter == ADD_NEW_BADDIE_RATE:
            baddie_add_counter = 0
            baddie_size = random.randint(BADDIE_MIN_SIZE, BADDIE_MAX_SIZE)
            new_baddie = {
                'rect': pygame.Rect(
                    random.randint(0, WINDOW_WIDTH - baddie_size),
                    0 - baddie_size, baddie_size, baddie_size
                ),
                'speed': random.randint(BADDIE_MIN_SPEED, BADDIE_MAX_SPEED),
                'surface': pygame.transform.scale(baddie_image, (baddie_size, baddie_size))
            }
            baddies.append(new_baddie)
        
        # Move the player around.
        if move_left and player_rect.left > 0:
            player_rect.move_ip(-1 * PLAYER_MOVE_RETE, 0)
        if move_right and player_rect.right < WINDOW_WIDTH:
            player_rect.move_ip(PLAYER_MOVE_RETE, 0)
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0, -1 * PLAYER_MOVE_RETE)
        if move_down and player_rect.bottom < WINDOW_HEIGHT:
            player_rect.move_ip(0, PLAYER_MOVE_RETE)
            
        # Move the mouse cursor to match player.
        pygame.mouse.set_pos(player_rect.centerx, player_rect.centery)
        
        # Move the baddies down.
        for baddie in baddies:
            if not reverse_cheat and not slow_cheat:
                baddie['rect'].move_ip(0, baddie['speed'])
            elif reverse_cheat:
                baddie['rect'].move_ip(0, -5)
            elif slow_cheat:
                baddie['rect'].move_ip(0, 1)
        
        # Delete baddies that have fallen past the bottom.
        for baddie in baddies[:]:
            if baddie['rect'].top > WINDOW_HEIGHT:
                baddies.remove(baddie)
        
        # Draw the game world on the window.
        window_surface.fill(BACKGROUND_COLOR)
        
        # Draw the score and top score.
        draw_text('Score: %s' % (score), font, window_surface, 10, 0)
        draw_text('Top score: %s' % (top_score), font, window_surface, 10, 40)
        
        # Draw the level text.
        draw_text('LEVEL: %s' % (level), font, window_surface, 450, 0)
        
        # Draw the player's rectangle.
        window_surface.blit(player_image, player_rect)
        
        # Draw each baddie.
        for baddie in baddies:
            window_surface.blit(baddie['surface'], baddie['rect'])
        
        pygame.display.update()
        
        # Check if any of the baddies have hit the player.
        if player_has_hit_baddie(player_rect, baddies):
            if score > top_score:
                # Set new top score.
                top_score = score
                write_top_score(top_score)
            break
        
        # Check if the player have reached next level.
        if score > 0 and score < 2000:
            ADD_NEW_BADDIE_RATE = LEVEL1[0]
            BADDIE_MIN_SIZE = LEVEL1[1]
            BADDIE_MAX_SIZE = LEVEL1[2]
            BADDIE_MIN_SPEED = LEVEL1[3]
            BADDIE_MAX_SPEED = LEVEL1[4]
            FPS = LEVEL1[5]
            level = 1
        elif score >= 2000 and score < 4000:
            ADD_NEW_BADDIE_RATE = LEVEL2[0]
            BADDIE_MIN_SIZE = LEVEL2[1]
            BADDIE_MAX_SIZE = LEVEL2[2]
            BADDIE_MIN_SPEED = LEVEL2[3]
            BADDIE_MAX_SPEED = LEVEL2[4]
            FPS = LEVEL2[5]
            level = 2
        elif score >= 4000 and score < 6000:
            ADD_NEW_BADDIE_RATE = LEVEL3[0]
            BADDIE_MIN_SIZE = LEVEL3[1]
            BADDIE_MAX_SIZE = LEVEL3[2]
            BADDIE_MIN_SPEED = LEVEL3[3]
            BADDIE_MAX_SPEED = LEVEL3[4]
            FPS = LEVEL3[5]
            level = 3
        elif score >= 6000 and score < 8000:
            ADD_NEW_BADDIE_RATE = LEVEL4[0]
            BADDIE_MIN_SIZE = LEVEL4[1]
            BADDIE_MAX_SIZE = LEVEL4[2]
            BADDIE_MIN_SPEED = LEVEL4[3]
            BADDIE_MAX_SPEED = LEVEL4[4]
            FPS = LEVEL4[5]
            level = 4
        elif score >= 8000 and score < 10000:
            ADD_NEW_BADDIE_RATE = LEVEL5[0]
            BADDIE_MIN_SIZE = LEVEL5[1]
            BADDIE_MAX_SIZE = LEVEL5[2]
            BADDIE_MIN_SPEED = LEVEL5[3]
            BADDIE_MAX_SPEED = LEVEL5[4]
            FPS = LEVEL5[5]
            level = 5
        
        main_clock.tick(FPS)
    
    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    game_over_sound.play()
    
    draw_text('GAME OVER', font, window_surface, WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3)
    draw_text('Press a key to play again.', font, window_surface,
              WINDOW_WIDTH / 3 - 100, WINDOW_HEIGHT / 3 + 120)
    pygame.display.update()
    wait_for_player_to_press_key()
    game_over_sound.stop()
