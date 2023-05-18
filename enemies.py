import pygame
import random

import lib
import bullets

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(
            self,
            x: int,
            y: int,
            health: int,
            accuracy: int,
            max_shot_cooldown: int,
            mag_capacity: int,
            max_reload_timer: int,
            bullet_type: pygame.sprite.Sprite
            ):

        super().__init__()

        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(20, 30)
        self.velocity = pygame.math.Vector2()

        self.health = health
        self.accuracy = accuracy
        self.target = None

        self.bullet_type = bullet_type
        self.max_shot_cooldown = max_shot_cooldown
        self.shot_cooldown = random.randint(0, self.max_shot_cooldown)
        self.mag_capacity = mag_capacity
        self.rounds_remaining = self.mag_capacity
        self.reloading = False
        self.max_reload_timer = max_reload_timer
        self.reload_timer = self.max_reload_timer

        self.image = pygame.Surface([self.size.x, self.size.y])
        self.image.fill(lib.color.red)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, enemies: pygame.sprite.Group):
        self.pos += self.velocity * lib.delta_time
        self.rect.center = self.pos

        if self.target == None:
            self.target = self.get_target(enemies)
        else:
            self.engage_target()

        if self.health <= 0:
            self.kill()

    def get_target(self, enemies: pygame.sprite.Group) -> pygame.sprite.Sprite:
        if len(enemies.sprites()) > 0:
            target = min([e for e in enemies], key = lambda e: self.pos.distance_to(e.pos))
            return target

    def engage_target(self):
        if self.reloading == False:
            self.shot_cooldown -= 1
        else:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.reloading = False
                self.reload_timer = self.max_reload_timer
                self.rounds_remaining = self.mag_capacity

        if self.target.alive():
            if self.shot_cooldown < 0:
                self.shoot()
                self.shot_cooldown = self.max_shot_cooldown
            else:
                self.target = None

    def shoot(self):
        b = self.bullet_type(
                self.pos.x,
                self.pos.y,
                random.randint(int(self.target.pos.x) - self.accuracy, int(self.target.pos.x) + self.accuracy),
                random.randint(int(self.target.pos.y) - self.accuracy, int(self.target.pos.y) + self.accuracy)
                )

        lib.enemy_bullets.add(b)

        self.rounds_remaining -= 1

        if self.rounds_remaining <= 0:
            self.reloading = True

class RifleEnemy(BaseEnemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 10, 20, 5, 5, 120, bullets.HandgunBullet) 