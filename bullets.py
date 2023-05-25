import pygame
import math

import lib

class BaseBullet(pygame.sprite.Sprite):
    def __init__(self, sx: int, sy: int, tx: int, ty: int, speed: int, damage: int):
        super().__init__()

        self.pos = pygame.math.Vector2(sx, sy)
        self.target_pos = pygame.math.Vector2(tx, ty)
        self.velocity = pygame.math.Vector2()

        self.speed = speed
        self.damage = damage
        self.lifetime = 8000

        self.image = pygame.Surface([3, 3])
        self.image.fill(lib.color.yellow)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.velocity = self.get_vectors()

    def get_vectors(self) -> pygame.math.Vector2:
        distance = [self.target_pos.x - self.pos.x, self.target_pos.y - self.pos.y]
        normal = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / normal, distance[1] / normal]
        vectors = pygame.math.Vector2(direction[0] * self.speed, direction[1] * self.speed)

        return vectors

    def update(self):
        self.pos += self.velocity * lib.delta_time
        self.rect.center = self.pos

        self.lifetime -= 1

        if self.lifetime < 0:
            self.kill()

    def destroy(self):
        self.kill()

class HandgunBullet(BaseBullet):
    def __init__(self, sx: int, sy: int, tx: int, ty: int):
        super().__init__(sx, sy, tx, ty, 650, 1)

class RifleBullet(BaseBullet):
    def __init__(self, sx: int, sy: int, tx: int, ty: int):
        super().__init__(sx, sy, tx, ty, 1200, 5)

class ARBullet(BaseBullet):
    def __init__(self, sx: int, sy: int, tx: int, ty: int):
        super().__init__(sx, sy, tx, ty, 1000, 3)
