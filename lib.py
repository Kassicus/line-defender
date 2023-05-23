import pygame
import random

screen_width = 1500
screen_height = 1000

class Colors():
    def __init__(self):
        self.black = pygame.Color(0, 0, 0, 255)
        self.white = pygame.Color(255, 255, 255, 255)
        self.red = pygame.Color(255, 0, 0, 255)
        self.green = pygame.Color(0, 255, 0, 255)
        self.blue = pygame.Color(0, 0, 255, 255)
        self.yellow = pygame.Color(255, 255, 0, 255)
        self.magenta = pygame.Color(255, 0, 255, 255)
        self.cyan = pygame.Color(0, 255, 255, 255)
        self.gray = pygame.Color(80, 80, 80, 255)
        self.light_gray = pygame.Color(140, 140, 140, 255)

    def get_random(self) -> pygame.Color:
        color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return color

color = Colors()

delta_time = 0
frame_limit = 120

events = None

friend_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

friend_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

current_friend_unit = "rifle"
spawn_friend_count = 5