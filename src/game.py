from typing import List
from random import randint
from pygame.locals import *
from pygame import Surface, Vector2
from pygame.sprite import Group, spritecollide
from sprites import Bear, Berry


class Game:
    def __init__(self):
        self.bear = Bear(320, 180)
        self.berry_group = Group()
        for _ in range(10):
            x, y = randint(0, 640), randint(0, 360)
            berry = Berry(x, y)
            self.berry_group.add(berry)

        self.score = 0
        self.remaining = 10

    def update(self, ticks: int):
        self.bear.update(ticks)
        collide_list = spritecollide(self.bear, self.berry_group, True)
        for _ in collide_list:
            self.score += 1
            self.remaining = len(self.berry_group)

    def on_key_down(self, keys: List[bool]):
        directions = [Vector2(0, -1), Vector2(-1, 0),
                      Vector2(0, 1), Vector2(1, 0)]
        accepted_keys = [K_UP, K_LEFT, K_DOWN, K_RIGHT, K_w, K_a, K_s, K_d]
        for index, key in enumerate(accepted_keys):
            if keys[key]:
                self.bear.set_direction(directions[index % 4])
                self.bear.set_walking(True)

    def on_key_up(self, keys: List[bool]):
        self.bear.set_walking(False)

    def render(self, screen: Surface):
        self.berry_group.draw(screen)
        self.bear.draw(screen)
