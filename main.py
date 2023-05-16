import pygame

import lib
import friends

pygame.init()

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode([lib.screen_width, lib.screen_height])
        pygame.display.set_caption("Line Defender")

        self.running = True
        self.clock = pygame.time.Clock()
        lib.events = pygame.event.get()

        self.friend_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

    def start(self):
        while self.running:
            self.events_master()
            self.draw()
            self.update()

    def events_master(self):
        lib.events = pygame.event.get()

        for event in lib.events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                self.events_keyboard(event.key)

    def events_keyboard(self, key: pygame.key):
        if key == pygame.K_q:
            self.running = False

        if key == pygame.K_f:
            x, y = pygame.mouse.get_pos()
            f = friends.RifleFriend(x, y)
            self.friend_group.add(f)

    def draw(self):
        self.screen.fill(lib.color.black)

        self.friend_group.draw(self.screen)
        self.enemy_group.draw(self.screen)

    def update(self):
        self.friend_group.update(self.enemy_group)
        self.enemy_group.update(self.friend_group)

        pygame.display.update()
        lib.delta_time = self.clock.tick(lib.frame_limit) / 1000

if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()

