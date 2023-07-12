import pygame
import sys
from constant import *
from spritesheet import SpriteSheet


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites_sheet = SpriteSheet("images/Small_Fireball_10x26.png")
        self.scale = 4
        self.num_sprites = 10 # 10x26
        self.sprites = [self.sprites_sheet.get_sprite(10*i, 26, 10, 26, self.scale) 
                        for i in range(self.num_sprites)]
        
        self.image = self.sprites[0]
        self.frame = 0
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.current_time = 0
        self.last_time = 0

    def update(self):
        self.rect.y += self.speedy
        self.current_time =  pygame.time.get_ticks()
        self.image = self.get_frame()
        if self.rect.bottom < 0:
            self.kill()
    def get_frame(self):
        image = self.sprites[self.frame]
        if self.current_time - self.last_time >= ANIM_COOLDOWN:
            self.frame = self.frame + 1
            if self.frame >= self.num_sprites:
                self.frame = 0
            self.last_time = self.current_time
        image = pygame.transform.flip(image, False, True)
        return image