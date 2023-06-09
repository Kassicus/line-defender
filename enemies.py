import pygame
import random
import math

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
            bullet_type: pygame.sprite.Sprite,
            engage_distance: int,
            kill_value: int
    ):

        super().__init__()

        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(20, 30)
        self.velocity = pygame.math.Vector2()
        self.waypoint = self.get_waypoint()

        self.health = health
        self.speed = 100
        self.accuracy = accuracy
        self.target = None
        self.engage_distance = engage_distance
        self.kill_value = kill_value
        self.is_current_target = False

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
            new_target = self.get_target(enemies)

            if new_target == None:
                self.move_to_waypoint()
            else:
                self.target = new_target

        else:
            self.engage_target()

        if self.health <= 0:
            lib.cash += self.kill_value
            self.kill()

    def get_target(self, enemies: pygame.sprite.Group) -> pygame.sprite.Sprite:
        if len(enemies.sprites()) > 0:
            target = min([e for e in enemies], key = lambda e: self.pos.distance_to(e.pos))
            if self.pos.distance_to(target.pos) < self.engage_distance:
                return target
            else:
                return None

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
            self.velocity = pygame.math.Vector2(0, 0)
            if self.shot_cooldown < 0:
                self.shoot()
                self.shot_cooldown = self.max_shot_cooldown
        elif self.target == None:
            self.move_to_waypoint()
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

    def get_vectors(self) -> pygame.math.Vector2:
        distance = [self.waypoint.x - self.pos.x, self.waypoint.y - self.pos.y]
        normal = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / normal, distance[1] / normal]
        vectors = pygame.math.Vector2(direction[0] * self.speed, direction[1] * self.speed)

        return vectors

    def move_to_waypoint(self):
        self.velocity = self.get_vectors()
        self.check_waypoint()

    def check_waypoint(self):
        if self.pos.distance_to(self.waypoint) < 5:
            self.velocity.x, self.velocity.y = 0, 0
            self.waypoint = self.get_waypoint()

    def get_waypoint(self) -> pygame.math.Vector2:
        x = random.randint(int(self.pos.x - 400), int(self.pos.x - 50))
        y = random.randint(25, 975)

        waypoint = pygame.math.Vector2(x, y)

        return waypoint

class SMGEnemy(BaseEnemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 10, 120, 10, 30, 350, bullets.HandgunBullet, 450, 6)

class RifleEnemy(BaseEnemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 10, 20, 50, 5, 250, bullets.ARBullet, 600, 4) 
