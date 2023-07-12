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

# General setup
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')

clock = pygame.time.Clock()
sprites_sheet = SpriteSheet("images/Small_Fireball_10x26.png")
num_sprites = 10
sprites = [
    [sprites_sheet.get_sprite(10*i, 26*j, 10, 26, 1) 
                        for i in range(num_sprites)]
    for j in range(6)
]
image = sprites[0][0]
last = 0
current = pygame.time.get_ticks()
frame_i = 0
frame_j = 0
bul = Bullet(200, 200)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    # if current % 10 == 0:
    #     frame_i = (frame_i + 1) % 10
    current = pygame.time.get_ticks()
    if current - last > ANIM_COOLDOWN:
        frame_j = frame_j + 1
        frame_j %= 6
        last = current
    gameDisplay.fill((0, 0, 0))
    gameDisplay.blit(sprites[frame_j][frame_i], (400,400))
    bul.update()
    gameDisplay.blit(bul.image, (200, 200))
    # for i in range(6):
    #     gameDisplay.blit(sprites[i][0], (100*i, 400))
    pygame.display.update()

    # pygame.display.flip()

pygame.quit()