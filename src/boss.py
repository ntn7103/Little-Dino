import pygame
from spritesheet import SpriteSheet
from constant import *
from utils import *


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # super().__init__()

        self.is_death = False
        self.is_completely_death = False

        self.sprites_sheet_idle = SpriteSheet(f"images/boss/cat/Idle.png")
        self.sprites_sheet_walk = SpriteSheet(f"images/boss/cat/Walk.png")
        self.sprites_sheet_death = SpriteSheet(f"images/boss/cat/Death.png")
        self.scale = 2

        self.num_idle_sprites = 4
        self.idle_sprites = [
            self.sprites_sheet_idle.get_sprite(48 * i, 0, 48, 48, self.scale)
            for i in range(self.num_idle_sprites)
        ]

        self.frame = 0

        self.num_walking_sprites = 6
        self.flying_sprites = [
            self.sprites_sheet_walk.get_sprite(48 * i, 0, 48, 48, self.scale)
            for i in range(self.num_walking_sprites)
        ]

        self.idle_sprites += self.flying_sprites
        self.num_idle_sprites += self.num_walking_sprites
        self.num_death_sprites = 4
        self.death_sprites = [
            self.sprites_sheet_death.get_sprite(48 * i, 0, 48, 48, self.scale)
            for i in range(self.num_death_sprites)
        ]

        self.image = self.idle_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.top = 10

        self.speed_x = 10
        self.speed_y = 0

        self.current_time = pygame.time.get_ticks()
        self.last_time = 0
        self.skill = None
        self.last_skill_time = 0
        self.max_hp = 3
        self.hp = self.max_hp

    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.is_death:
            self.speed_x = 0
            self.speed_y = 0
            self.image = self.get_death_frame()
            return
        self.rect.x += self.speed_x
        if self.rect.x <= -100 or self.rect.x >= WIDTH + 50:
            self.speed_x = -self.speed_x
        self.image = self.get_frame()
        if self.speed_x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def get_death_frame(self):
        image = self.death_sprites[self.frame]
        if self.current_time - self.last_time >= ANIM_COOLDOWN * 4:
            self.frame = self.frame + 1
            if self.frame >= self.num_death_sprites:
                self.is_completely_death = True
                self.kill()
            self.last_time = self.current_time
        return image

    def get_frame(self):
        image = self.idle_sprites[self.frame]
        if self.current_time - self.last_time >= ANIM_COOLDOWN:
            self.frame = self.frame + 1
            if self.frame >= self.num_idle_sprites:
                self.frame = 0
            self.last_time = self.current_time
        return image

    def hurt(self):
        if self.hp > 0:
            self.hp -= 1
        else:
            self.is_death = True
            self.frame = 0
