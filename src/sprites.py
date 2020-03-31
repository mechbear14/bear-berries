from pygame.sprite import Sprite, Group
from pygame import Vector2, Color, image, Surface, Rect
from pygame.font import Font
from utils import Camera
import os


class Bear(Sprite):
    def __init__(self, x: int, y: int, spritesheet: Surface):
        Sprite.__init__(self)
        self.position = Vector2(x, y)
        self.speed = 25
        self.directions = [
            Vector2(0, -1), Vector2(-1, 0), Vector2(1, 0), Vector2(0, 1)]
        self.direction = Vector2(0, -1)
        self.walking = False

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
            ds = self.speed * dt / 100.0 * self.direction
            self.position = self.position + ds
            self.rect = self.rect.move(ds)
            self.costume_number = self.direction_number * 3 + frame % 2 + 1
        else:
            self.walking_start_time = ticks
            self.costume_number = self.direction_number * 3
        self.timer = ticks

    def clamp(self, area: Rect):
        self.rect = self.rect.clamp(area)
        self.position = Vector2(self.rect.center)

    def draw(self, surface: Surface, camera: Camera = None):
        self.image = self.costumes[self.costume_number]
        if camera is None:
            surface.blit(self.image, self.rect)
        else:
            position_in_camera = camera.from_world(self.position)
            rect = self.image.get_rect(center=position_in_camera)
            surface.blit(self.image, rect)


class Berry(Sprite):
    def __init__(self, x: int, y: int, spritesheet: Surface):
        Sprite.__init__(self)
        self.position = Vector2(x, y)

        spritesheet.convert()
        spritesheet.set_colorkey(Color(128, 51, 0))
        self.image = spritesheet
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface: Surface, camera: Camera = None):
        if camera is None:
            surface.blit(self.image, self.rect)
        else:
            position_in_camera = camera.from_world(self.position)
            rect = self.image.get_rect(center=position_in_camera)
            surface.blit(self.image, rect)


class World(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.columns, self.rows = 10, 10
        self.colour1 = Color(200, 128, 0)
        self.colour2 = Color(200, 64, 0)
        self.font = Font(None, 60)
        self.image = Surface((self.columns * 100, self.rows * 100))
        for y in range(self.rows):
            for x in range(self.columns):
                surface = Surface((100, 100))
                rect = Rect(x * 100, y * 100, 100, 100)
                number = x + y * self.columns + 1
                colour = self.colour1 if (x + y) % 2 == 1 else self.colour2
                surface.fill(colour)
                font_surface = self.font.render(
                    str(number), True, Color(255, 200, 200))
                font_rect = font_surface.get_rect(center=Vector2(50, 50))
                surface.blit(font_surface, font_rect)
                self.image.blit(surface, rect)
        self.rect = self.image.get_rect()

    def draw(self, surface: Surface, camera: Camera = None):
        if camera is None:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(self.image, self.rect, area=camera.rect)
