import time
from os import path
import pygame
import sys
import numpy as np
from player import Player
from bat import Bat
from bullet import Bullet
from boss import Boss
from spritesheet import SpriteSheet
from utils import *
from constant import *
import pygame.mixer 

# SETUP
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()

# Game Screen
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BLACK)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Little Dino")
pygame.mouse.set_visible(False)


#Background
img_dir = path.join(path.dirname(__file__), 'background')
background = pygame.image.load(path.join(img_dir, "forest.png")).convert()
background2 = pygame.image.load(path.join(img_dir, "background2.png")).convert()
background_rect = background.get_rect()

snd_dir = path.join(path.dirname(__file__), 'background')
pygame.mixer.music.load(path.join(snd_dir, 'background.mp3'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

hurt_sound = pygame.mixer.Sound(path.join(snd_dir, 'meow.wav'))
win_sound = pygame.mixer.Sound(path.join(snd_dir, 'win.mp3'))
# END_SETUP

# GAME STATE PARAMETERS
game_over = False
new_game = True
win_game = False
current_level = 1

# RESTART to replay game.
# Restart aka setup object for game.
def restart():
    # Use global keyword that defines variables for whole game.
    # variable scope: local, global
    # local = in function, in class, in method (function of class)
    # global = all system.
    global list_players, mini_players, list_bats, change_player, game_over, last_player_position_x, change_player, player
    # Game initialization
    all_sprites.empty()
    bats.empty()
    bullets.empty()

    # Init players
    list_players = [Player("doux"), Player("mort"), Player("tard"), Player("vita")]
    mini_players = [Player("doux"), Player("mort"), Player("tard"), Player("vita")]

    # Change icon of player (mini player) to top right screen.
    for i, mini in enumerate(mini_players):
        mini.change_mini()
        mini.rect.centerx = WIDTH - 20 * i - 10
        mini.rect.centery = 100
        all_sprites.add(mini)

    # setup enemy for first stage.
    list_bats = [Bat(100, 100), Bat(200, 100), Bat(300, 100)]
    for bat in list_bats:
        all_sprites.add(bat)
        bats.add(bat)

    change_player = False
    player = list_players[-1]
    all_sprites.add(player)
    game_over = False
    win_game = False
    current_level = 1
    last_player_position_x = -1

def level2():
    global list_bats, change_player, game_over, last_player_position_x, change_player, player

    # 8 bats in two rows
    list_bats = [Bat(100, 100), Bat(200, 100), Bat(300, 100), Bat(400, 100),
                 Bat(100, 200), Bat(200, 200), Bat(300, 200), Bat(400, 200)]
    for bat in list_bats:
        all_sprites.add(bat)
        bats.add(bat)

    change_player = False
    player = list_players[-1]
    all_sprites.add(player)
    game_over = False
    win_game = False

    # Add boss to the game.
    global boss
    boss = Boss()
    all_sprites.add(boss)

    # change background
    global background
    background = background2

# MAIN
while True:
    # Setup for game.
    clock.tick(FPS)
    screen.blit(background, background_rect)

    # CHECK GAME STATES
    if win_game:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("YOU WIN", 1, WHITE)
        textpos = text.get_rect(centerx=WIDTH / 2, centery=HEIGHT / 2)
        screen.blit(text, textpos)
        pygame.display.flip()
        win_sound.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    restart()
                    continue
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        continue

    if new_game:
        new_game = False
        restart()

    if game_over:
        # Because I don't want game over screen appear too fast.
        time.sleep(1)
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("GAME OVER", 1, WHITE)
        textpos = text.get_rect(centerx=WIDTH / 2, centery=HEIGHT / 2)
        screen.blit(text, textpos)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    game_over = False
                    restart()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        continue
    # END OF CHECK STATES
    
    # Game over condition.
    if len(bats) == 0:
        # Not too smart
        current_level += 1
        if current_level == 2:
            # Render next level screen
            screen.fill(BLACK)
            font = pygame.font.Font(None, 36)
            text = font.render("NEXT LEVEL", 1, WHITE)
            # center the text on the screen
            textpos = text.get_rect(centerx=WIDTH / 2, centery=HEIGHT / 2)
            screen.blit(text, textpos)
            pygame.display.flip()
            time.sleep(2)
            if current_level == 2:
                level2()
                continue
        else:
            if boss.is_completely_death:
                win_game = True
                continue
    # end of game over condition

    # process change player.
    if change_player:
        list_players.pop()
        mini_players.pop()
        if len(list_players) == 0: # out of life
            game_over = True
            continue
        player = list_players[-1]
        player.rect.centerx = last_player_position_x
        all_sprites.add(player)
        change_player = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()



    # check to see if a bullet hit a bat
    hits = pygame.sprite.groupcollide(bullets, bats, True, True, pygame.sprite.collide_rect_ratio(0.5))
    
    for hit in hits:
        # after bat and bullet touch each other, death animation of bat appears 
        bat = Bat(hit.rect.centerx, hit.rect.centery, is_death=True)
        all_sprites.add(bat)

    # check if a bat hit the player
    if pygame.time.get_ticks() - last_bat_touched > IMMORTAL_TIME:
        # The bat must not be gone, but it killed by the collide.
        # Because when a sprite (player) and a group of bat (bats) collide, I don't know what exactly bat hit.
        # So I decide to kill the bat first.
        hits = pygame.sprite.spritecollide(player, bats, True, pygame.sprite.collide_rect_ratio(0.6))
        
        for hit in hits:
            # Hurt animation and kill player after hurt animation done.
            player.is_hurt()
            mini_players[-1].is_hurt()

            change_player = True

            # Now, add a new bat and make some change...
            new_bat = Bat(hit.rect.centerx, hit.rect.centery)
            new_bat.collide()

            all_sprites.add(new_bat)
            bats.add(new_bat)
            last_bat_touched = pygame.time.get_ticks()

            # save current postion of player.
            last_player_position_x = player.rect.centerx

    all_sprites.update()
    
    # Check special params if at level 2.
    if current_level >= 2:
        # print("level 2")
        # draw boss health bar
        hits = pygame.sprite.spritecollide(boss, bullets, True, pygame.sprite.collide_rect_ratio(0.7))
        
        if hits:
            boss.hurt()
            hurt_sound.play()

        # draw health bar
        if not boss.is_completely_death:
            pygame.draw.rect(screen, GREEN, (WIDTH / 2 - 100, 10, 70 * boss.hp, 20))
            pygame.draw.rect(screen, RED, (WIDTH / 2 - 100 + 70 * boss.hp, 10, 70 * (boss.max_hp - boss.hp), 20))

    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()