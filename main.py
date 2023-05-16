import pygame

import lib

pygame.init()

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode([lib.screen_width, lib.screen_height])
        pygame.display.set_caption("Line Defender")

        self.running = True
        self.clock = pygame.time.Clock()
        lib.events = pygame.event.get()

    def start(self):
        while self.running:
            self.events()
            self.draw()
            self.update()

    def events(self):
        lib.events = pygame.event.get()

        for event in lib.events:
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.fill(lib.color.black)

    def update(self):
        pygame.display.update()
        lib.delta_time = self.clock.tick(lib.frame_limit) / 1000

if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()

