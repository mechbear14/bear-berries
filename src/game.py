import os
from typing import List
from random import randint
from pygame.locals import *
from pygame import Surface, Vector2, image
from pygame.sprite import Group, spritecollide
from sprites import Bear, Berry, World
from utils import Camera, TextUI


class Game:
    """
    Class representing the game.
    @note Since this example has only one scene, all the timing and sprite sheets are managed in this class.
    If there's a requirement for multiple scenes, you might want to create a Scene class separately, and decide which
    objects are shared between scenes (for example, player's backpack) and which are in one specific scene only
    (for example, timer).
    """
    def __init__(self, screen: Surface):
        """
        Creates the game
        @param screen: The screen surface (created with pygame.display.set_mode) to draw on. This screen is used both
        for drawing and for creating the camera.
        @note To pave our way to Rust projects, this project uses type hints in function signatures.
        """

        # Load sprite sheets (aka costumes)
        assets_path = os.path.dirname(os.path.realpath(__file__))
        bear_spritesheet = image.load(os.path.join(
            assets_path, "..", "assets", "bears.png"))
        berry_spritesheet = image.load(os.path.join(
            assets_path, "..", "assets", "berry.png"))

        # Definition of game objects
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

        # Gameplay-related data
        self.score = 0
        self.remaining = 100
        self.timer = 0

        # State management. You might want to use a state machine for complex games.
        self.running = True

    def update(self, ticks: int):
        """
        Updates game state with timing information provided by PyGame
        @param ticks: number of milliseconds passed since pygame.init() was called
        (obtained with pygame.time.get_ticks())
        @return: None
        """
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
        """
        Event listener for pygame.KEYDOWN event. All key press checks should be done in this function and on_key_up().
        @bug Only checks the first pressed key in the list. Not able to handle multiple keys pressed at a same time
        @param keys: a list of key status obtained with pygame.key.get_pressed().
        @return: None
        """
        directions = [Vector2(0, -1), Vector2(-1, 0),
                      Vector2(0, 1), Vector2(1, 0)]
        accepted_keys = [K_UP, K_LEFT, K_DOWN, K_RIGHT, K_w, K_a, K_s, K_d]
        for index, key in enumerate(accepted_keys):
            if keys[key]:
                self.bear.set_direction(directions[index % 4])
                self.bear.set_walking(True)

    def on_key_up(self, keys: List[bool]):
        """
        Event listener for pygame.KEYDOWN event. All key press checks should be done in this function and on_key_down().
        @note As required by Python syntax, the position argument keys must present even if it's not used anywhere in
        the function.
        @param keys: a list of key status obtained with pygame.key.get_pressed().
        @return: None
        """
        self.bear.set_walking(False)

    def render(self):
        """
        Draws all game objects onto the screen based on camera position.
        @note Order matters.
        @return: None
        """
        self.world.draw(self.screen, self.camera)
        for berry in self.berry_group:
            if berry.rect.colliderect(self.camera.rect):
                berry.draw(self.screen, self.camera)
        self.bear.draw(self.screen, self.camera)
        self.text.render(self.screen)
