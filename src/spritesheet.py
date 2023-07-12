import pygame


class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.sprite_sheet.set_colorkey((0, 0, 0))

    def get_sprite(self, x, y, width, height, scale=4):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        new_sprite = pygame.transform.scale(
            sprite, (int(width * scale), int(height * scale))
        )
        return new_sprite
