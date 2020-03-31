from pygame.sprite import Sprite, Group
from pygame import Vector2, Color, image, Surface, Rect
import os


class Bear(Sprite):
    def __init__(self, x: int, y: int):
        Sprite.__init__(self)
        self.position = Vector2(x, y)
        self.speed = 25
        self.directions = [
            Vector2(0, -1), Vector2(-1, 0), Vector2(1, 0), Vector2(0, 1)]
        self.direction = Vector2(0, -1)
        self.walking = False

        assets_path = os.path.dirname(os.path.realpath(__file__))
        spritesheet = image.load(os.path.join(
            assets_path, "..", "assets", "bears.png"))
        spritesheet = spritesheet.convert()
        spritesheet.set_colorkey(Color(128, 51, 0))
        self.costumes = []
        for i in range(12):
            row, column = divmod(i, 3)
            surface = Surface((50, 50)).convert_alpha()
            surface.fill(Color(0, 0, 0, 0))
            surface.blit(spritesheet, surface.get_rect(),
                         area=Rect(column * 50, row * 50, 50, 50))
            self.costumes.append(surface)

        self.direction_number = 0
        self.costume_number = 0
        self.image = self.costumes[self.costume_number]
        self.rect = self.image.get_rect(center=self.position)
        self.timer = 0
        self.walking_start_time = 0

    def set_direction(self, direction: Vector2):
        self.direction = direction
        self.direction_number = self.directions.index(direction)

    def set_walking(self, walking: bool):
        self.walking = walking

    def update(self, ticks: int):
        if self.walking:
            eta = ticks - self.walking_start_time
            frame = eta // 250
            dt = ticks - self.timer
            self.rect = self.rect.move(
                self.speed * dt / 100.0 * self.direction)
            self.costume_number = self.direction_number * 3 + frame % 2 + 1
        else:
            self.walking_start_time = ticks
            self.costume_number = self.direction_number * 3
        self.timer = ticks

    def draw(self, surface: Surface):
        self.image = self.costumes[self.costume_number]
        surface.blit(self.image, self.rect)


class Berry(Sprite):
    def __init__(self, x: int, y: int):
        Sprite.__init__(self)
        self.position = Vector2(x, y)

        assets_path = os.path.dirname(os.path.realpath(__file__))
        spritesheet = image.load(os.path.join(
            assets_path, "..", "assets", "berry.png"))
        spritesheet.convert()
        spritesheet.set_colorkey(Color(128, 51, 0))
        self.image = spritesheet
        self.rect = self.image.get_rect().move(self.position)

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)
