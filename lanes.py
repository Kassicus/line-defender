import pygame

import lib

class Lane(pygame.sprite.Sprite):
    def __init__(self, y: int):
        super().__init__()

        self.pos = pygame.math.Vector2(0, y)
        self.size = pygame.math.Vector2(1500, 25)

        self.image = pygame.Surface([self.size.x, self.size.y])
        self.image.fill(lib.color.black)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self):
        pass
