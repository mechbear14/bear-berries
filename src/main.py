import pygame
from pygame.locals import *
from game import Game

"""
Bear and Berries, by Gabe Lyu
Created on 31MAR20(BST)
Starting point of the game. Run this file to start the game.
This is a simple game example for extension. Suggestions (especially on architecture) are welcome.
Contact via GitHub only

This module creates a screen and a clock, initialises the game and registers event listeners with PyGame main loop.

Avoid touching this file unless you want to:
- Add new event listener
- Prepare files needed for creating a *game* object
For creating a *scene* from file, or adding listener for an existing event to a new class, please do that in Game class.
"""

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 360))
    pygame.display.set_caption("Bear and berries")
    clock = pygame.time.Clock()
    game = Game(screen)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                game.on_key_down(pressed_keys)
            elif event.type == KEYUP:
                pressed_keys = pygame.key.get_pressed()
                game.on_key_up(pressed_keys)
        clock.tick(30)
        game.update(pygame.time.get_ticks())
        screen.fill(Color(0, 0, 128))
        game.render()
        pygame.display.update()
