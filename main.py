import pygame

import lib
import friends
import enemies

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
            lib.friend_group.add(f)

        if key == pygame.K_b:
            x, y = pygame.mouse.get_pos()
            b = enemies.RifleEnemy(x, y)
            lib.enemy_group.add(b)

    def collide_projectiles(self):
        for f in lib.friend_group:
            for e in lib.enemy_bullets:
                if f.rect.colliderect(e.rect):
                    f.health -= e.damage
                    e.destroy()

        for e in lib.enemy_group:
            for f in lib.friend_bullets:
                if e.rect.colliderect(f.rect):
                    e.health -= f.damage
                    f.destroy()

    def draw(self):
        self.screen.fill(lib.color.black)

        lib.friend_group.draw(self.screen)
        lib.enemy_group.draw(self.screen)

        lib.friend_bullets.draw(self.screen)
        lib.enemy_bullets.draw(self.screen)

    def update(self):
        lib.friend_group.update(lib.enemy_group)
        lib.enemy_group.update(lib.friend_group)

        lib.friend_bullets.update()
        lib.enemy_bullets.update()

        self.collide_projectiles()

        pygame.display.update()
        lib.delta_time = self.clock.tick(lib.frame_limit) / 1000

if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()
