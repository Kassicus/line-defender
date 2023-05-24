import pygame

import lib

class DebugInterface():
    def __init__(self):
        self.active = True

        self.font = pygame.font.SysFont("Courier", 16)
        
        self.fps_text = pygame.Surface([0, 0])
        self.mouse_text = pygame.Surface([0, 0])

        self.fps_offset = 0
        self.mouse_offset = 0

    def get_fps(self, clock: pygame.time.Clock) -> list [pygame.Surface, int]:
        fps_string = "FPS: " + str(int(clock.get_fps()))
        fps_text = self.font.render(fps_string, True, lib.color.cyan)

        fps_offset = int(lib.screen_width - fps_text.get_width() - 10)

        return fps_text, fps_offset
    
    def get_mouse(self) -> list [pygame.Surface, int]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_string = "Mouse: " + str(mouse_x) + " | " + str(mouse_y)
        mouse_text = self.font.render(mouse_string, True, lib.color.cyan)

        mouse_offset = int(lib.screen_width - mouse_text.get_width() - 10)

        return mouse_text, mouse_offset
    
    def toggle_active(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def draw(self, display_surface: pygame.Surface):
        display_surface.blit(self.fps_text, (self.fps_offset, 10))
        display_surface.blit(self.mouse_text, (self.mouse_offset, 30))

    def update(self, clock: pygame.time.Clock):
        self.fps_text, self.fps_offset = self.get_fps(clock)
        self.mouse_text, self.mouse_offset = self.get_mouse()

class ToggleUnitButton(pygame.sprite.Sprite):
    def __init__(
            self,
            x: int,
            y: int,
            title: str,
            unit: str,
            count: int,
            cost: int
    ):
        super().__init__()
        
        self.pos = pygame.math.Vector2(x, y)

        self.font = pygame.font.SysFont("Courier", 16)
        self.title = title
        self.title_surface = self.font.render(self.title, True, lib.color.green)

        self.unit = unit
        self.unit_count = count

        self.cost = cost

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
                if lib.cash >= self.cost:
                    lib.current_friend_unit = self.unit
                    lib.spawn_friend_count = self.unit_count
                    lib.mouse_mode = "spawn"
                    pygame.mouse.set_visible(False)
                    lib.current_cost = self.cost

class UnitInterface():
    def __init__(self):
        self.button_group = pygame.sprite.Group()

        self.rifle_button = ToggleUnitButton(10, 940, "RifleMan", "rifle", 5, 100)
        self.auto_rifle_button = ToggleUnitButton(145, 940, "AutoRifle", "autorifle", 4, 200)

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

class InfoInterface():
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 24)

        self.cash_text = pygame.Surface([0, 0])
        
        self.cash_offset = 0

    def get_cash(self) -> list [pygame.Surface, int]:
        cash_string = "Cash: " + str(lib.cash)
        cash_text = self.font.render(cash_string, True, lib.color.green)

        cash_offset = 10

        return cash_text, cash_offset
    
    def draw(self, display_surface: pygame.Surface):
        display_surface.blit(self.cash_text, (self.cash_offset, 10))

    def update(self):
        self.cash_text, self.cash_offset = self.get_cash()