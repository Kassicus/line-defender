import pygame
import random

import lib
import friends
import enemies
import ui

pygame.init()

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode([lib.screen_width, lib.screen_height])
        pygame.display.set_caption("Line Defender")

        self.running = True
        self.clock = pygame.time.Clock()
        lib.events = pygame.event.get()

        self.debug_interface = ui.DebugInterface()
        self.info_interface = ui.InfoInterface()

        self.unit_interface = ui.UnitInterface()
        self.place_unit_cursor = pygame.image.load("assets/down_arrow.png").convert_alpha()

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_events(event.button)

    def mouse_events(self, button):
        if lib.mouse_mode == "spawn":
            if button == pygame.BUTTON_LEFT:
                x, y = pygame.mouse.get_pos()

                match lib.current_friend_unit:
                    case "rifle":
                        for f in range(lib.spawn_friend_count):
                            f = friends.RifleFriend(x + random.randint(-50, 50), y + random.randint(-100, 100))
                            lib.friend_group.add(f)
                    case "autorifle":
                        for f in range(lib.spawn_friend_count):
                            f = friends.AutoRifleFriend(x + random.randint(-50, 50), y + random.randint(-100, 100))
                            lib.friend_group.add(f)

                lib.cash -= lib.current_cost
                lib.mouse_mode = "normal"
                pygame.mouse.set_visible(True)

    def events_keyboard(self, key: pygame.key):
        if key == pygame.K_q:
            self.running = False

        if key == pygame.K_w:
            self.spawn_enemy_wave()

    def spawn_enemy_wave(self):
        for x in range(8):
            x = random.choice((enemies.RifleEnemy, enemies.SMGEnemy))
            e = x(random.randint(1600, 1700), random.randint(25, 975))
            lib.enemy_group.add(e)

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

        self.unit_interface.draw(self.screen)
        self.debug_interface.draw(self.screen)
        self.info_interface.draw(self.screen)

        if lib.mouse_mode == "spawn":
            x, y = pygame.mouse.get_pos()
            self.screen.blit(self.place_unit_cursor, (x - self.place_unit_cursor.get_width() / 2, y - self.place_unit_cursor.get_height()))

    def update(self):
        lib.friend_group.update(lib.enemy_group)
        lib.enemy_group.update(lib.friend_group)

        lib.friend_bullets.update()
        lib.enemy_bullets.update()

        self.collide_projectiles()

        self.unit_interface.update()
        self.debug_interface.update(self.clock)
        self.info_interface.update()

        pygame.display.update()
        lib.delta_time = self.clock.tick(lib.frame_limit) / 1000

if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()
