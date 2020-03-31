import pygame
from pygame.locals import *
from game import Game


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
