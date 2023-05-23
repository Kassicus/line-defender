import pygame

import lib

class ToggleUnitButton(pygame.sprite.Sprite):
    def __init__(
            self,
            x: int,
            y: int,
            title: str,
            unit: str,
            count: int
    ):
        super().__init__()
        
        self.pos = pygame.math.Vector2(x, y)

        self.font = pygame.font.SysFont("Courier", 16)
        self.title = title
        self.title_surface = self.font.render(self.title, True, lib.color.green)

        self.unit = unit
        self.unit_count = count

        self.image = pygame.Surface([125, 50])
        self.image.fill(lib.color.gray)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def draw_label(self, surface: pygame.Surface):
        surface.blit(
            self.title_surface,
            (self.pos.x + (self.rect.width / 2) - (self.title_surface.get_width() / 2), self.pos.y + (self.rect.height / 2) - (self.title_surface.get_height() / 2))
        )

    def update(self):
        self.mouse_interact()

    def mouse_interact(self):
        x, y = pygame.mouse.get_pos()

        if self.pos.x < x < self.pos.x + self.rect.width:
            if self.pos.y < y < self.pos.y + self.rect.height:
                self.mouse_hover = True
                self.image.fill(lib.color.light_gray)
            else:
                self.mouse_hover = False
                self.image.fill(lib.color.gray)
        else:
            self.mouse_hover = False
            self.image.fill(lib.color.gray)

        if self.mouse_hover:
            if pygame.mouse.get_pressed()[0]:
                lib.current_friend_unit = self.unit
                lib.spawn_friend_count = self.unit_count

class UnitInterface():
    def __init__(self):
        self.button_group = pygame.sprite.Group()

        self.rifle_button = ToggleUnitButton(10, 940, "RifleMan", "rifle", 5)
        self.auto_rifle_button = ToggleUnitButton(145, 940, "AutoRifle", "autorifle", 4)

        self.button_group.add(
            self.rifle_button,
            self.auto_rifle_button
        )

    def draw(self, surface: pygame.Surface):
        self.button_group.draw(surface)

        for button in self.button_group:
            button.draw_label(surface)

    def update(self):
        self.button_group.update()