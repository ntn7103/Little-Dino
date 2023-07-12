import pygame
import spritesheet
from constant import *
from bullet import Bullet
from utils import *
from os import path
import pygame.mixer 

pygame.mixer.init()
snd_dir = path.join(path.dirname(__file__), 'background')
shooting_sound = pygame.mixer.Sound(path.join(snd_dir, 'shoot.wav'))
ouch_sound = pygame.mixer.Sound(path.join(snd_dir, 'ouch.wav'))

shooting_sound.set_volume(0.2)

class Player(pygame.sprite.Sprite):
    def __init__(self, name="vita"):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.sprites = spritesheet.SpriteSheet(f"images/dinos/DinoSprites_{name}.png")
        self.scale = PLAYER_SCALE

        self.animation_steps = [4, 6, 3, 4]
        self.action = 0
        self.num_stay_sprites = 10
        self.list_sprites = []
        num_sprites = 0
        for i in range(len(self.animation_steps)):
            self.list_sprites.append(
                [
                    self.sprites.get_sprite(24 * j + num_sprites, 0, 24, 24, self.scale)
                    for j in range(self.animation_steps[i])
                ]
            )
            num_sprites += self.animation_steps[i] * 24
        self.frame = 0

        self.image = self.list_sprites[0][0]

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10

        self.speed_x = 0

        self.current_time = pygame.time.get_ticks()
        self.last_time = 0
        self.last_shot = pygame.time.get_ticks()
        self.hurt = False

        self.is_mini = False

    def change_mini(self):
        self.scale = MINI_PLAYER_SCALE
        self.is_mini = True

    def get_frame(self, flip=False):

        if self.frame >= self.animation_steps[self.action]:
            self.frame = 0
        if flip:
            image = pygame.transform.flip(
                self.list_sprites[self.action][self.frame], True, False
            )
        else:
            image = self.list_sprites[self.action][self.frame]
        if self.current_time - self.last_time >= ANIM_COOLDOWN:
            self.frame = self.frame + 1
            if self.frame >= self.animation_steps[self.action]:
                self.frame = 0
            self.last_time = self.current_time
        if self.is_mini:
            # print(image.get_size())
            image = pygame.transform.scale(
                image, (int(24 * self.scale), int(24 * self.scale))
            )
        return image

    def is_hurt(self):
        self.hurt = True
        self.frame = 0
        ouch_sound.play()

    def update(self):

        self.speed_x = 0
        self.current_time = pygame.time.get_ticks()
        key_state = pygame.key.get_pressed()
        if self.hurt:
            self.action = 3
            if self.frame == self.animation_steps[self.action] - 1:
                self.kill()
            self.image = self.get_frame()
            return
        else:
            self.action = 0

        if self.is_mini:
            self.image = self.get_frame()
            return

        if key_state[pygame.K_LEFT]:
            self.speed_x = -8
            if self.action != 1:
                self.action = 1
            self.image = self.get_frame(flip=True)
        elif key_state[pygame.K_RIGHT]:
            self.speed_x = 8
            if self.action != 1:
                self.action = 1
            self.image = self.get_frame()

        elif key_state[pygame.K_SPACE] or key_state[pygame.K_c]:
            self.shoot()
            shooting_sound.play()

        else:
            self.image = self.get_frame()
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_shot > SKILL_COOLDOWN:
            self.last_shot = self.current_time

            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


#             play sound
