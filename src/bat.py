import pygame
from spritesheet import SpriteSheet
from constant import *
import numpy as np


class Bat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name="Standard", is_death=False):
        pygame.sprite.Sprite.__init__(self)

        self.is_death = is_death

        self.sprites_sheet = SpriteSheet(f"images/bats/Bat{name}_Sheet.png")
        self.scale = 2

        self.num_attack_sprites = 4
        self.attack_sprites = [
            self.sprites_sheet.get_sprite(32 * i, 0, 32, 32, self.scale)
            for i in range(self.num_attack_sprites)
        ]

        self.frame = 0

        self.num_flying_sprites = 4
        self.flying_sprites = [
            self.sprites_sheet.get_sprite(32 * i, 32, 32, 32, self.scale)
            for i in range(self.num_flying_sprites)
        ]

        self.attack_sprites += self.flying_sprites
        self.num_attack_sprites += self.num_flying_sprites
        self.num_death_sprites = 6
        self.death_sprites = [
            self.sprites_sheet.get_sprite(32 * i, 96, 32, 32, self.scale)
            for i in range(self.num_death_sprites)
        ]

        self.image = self.attack_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.bottom = pos_y

        self.speed_x = np.random.randint(-BAT_SPEED, BAT_SPEED)
        self.speed_y = np.random.randint(-BAT_SPEED, BAT_SPEED)

        self.current_time = pygame.time.get_ticks()
        self.last_time = 0


    def update(self):
        if self.is_death:
            self.speed_x = 0
            self.speed_y = 0
            self.current_time = pygame.time.get_ticks()
            self.image = self.get_death_frame()
            return
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y
        self.current_time = pygame.time.get_ticks()
        self.image = self.get_frame()
        if self.speed_x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def collide(self):
        self.speed_x = -self.speed_x
        self.speed_y = -self.speed_y

    def get_death_frame(self):
        image = self.death_sprites[self.frame]
        if self.current_time - self.last_time >= ANIM_COOLDOWN:
            self.frame = self.frame + 1
            if self.frame >= self.num_death_sprites:
                self.kill()
            self.last_time = self.current_time
        return image

    def get_frame(self):
        image = self.attack_sprites[self.frame]
        if self.current_time - self.last_time >= ANIM_COOLDOWN:
            self.frame = self.frame + 1
            if self.frame >= self.num_attack_sprites:
                self.frame = 0
            self.last_time = self.current_time
        return image
