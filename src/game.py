import os
from typing import List
from random import randint
from pygame.locals import *
from pygame import Surface, Vector2, image
from pygame.sprite import Group, spritecollide
from sprites import Bear, Berry, World
from utils import Camera, TextUI


class Game:
    def __init__(self, screen: Surface):
        assets_path = os.path.dirname(os.path.realpath(__file__))
        bear_spritesheet = image.load(os.path.join(
            assets_path, "..", "assets", "bears.png"))
        berry_spritesheet = image.load(os.path.join(
            assets_path, "..", "assets", "berry.png"))

        self.world = World()
        self.bear = Bear(320, 180, bear_spritesheet)
        self.berry_group = Group()
        for _ in range(100):
            x, y = randint(0, 1000), randint(0, 1000)
            berry = Berry(x, y, berry_spritesheet)
            berry.rect = berry.rect.clamp(self.world.rect)
            self.berry_group.add(berry)
        self.screen = screen
        self.camera = Camera(320, 180, screen)
        self.text = TextUI(0, 0)

        self.score = 0
        self.remaining = 100
        self.timer = 0

        self.running = True

    def update(self, ticks: int):
        self.bear.update(ticks)
        self.bear.clamp(self.world.rect)
        self.camera.move_to(self.bear.position)
        self.camera.clamp(self.world.rect)
        collide_list = spritecollide(self.bear, self.berry_group, True)
        for _ in collide_list:
            self.score += 1
            self.remaining = len(self.berry_group)
            if self.remaining == 0:
                self.running = False
        if self.running:
            self.timer = ticks
            self.text.set_text(
                "Collected: {0}. Remaining: {1}. Elapsed time: {2:.1f} s".format(self.score, self.remaining, self.timer / 1000.0))
        else:
            self.text.set_text(
                "You collected all berries in {0:.1f} seconds".format(self.timer / 1000.0))

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

    def render(self):
        self.world.draw(self.screen, self.camera)
        for berry in self.berry_group:
            if berry.rect.colliderect(self.camera.rect):
                berry.draw(self.screen, self.camera)
        self.bear.draw(self.screen, self.camera)
        self.text.render(self.screen)
