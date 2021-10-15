import pygame
from game.game import Game


def main():
    running = True
    W, H = 600, 600
    pygame.init()
    pygame.font.init()
    game = Game(W,H)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.mouse_pressed(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP:
                game.mouse_released(pygame.mouse.get_pos())
            
            if event.type == pygame.MOUSEMOTION:
                game.mouse_moved(pygame.mouse.get_pos())

            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        game.update()
        game.draw()

if __name__ == '__main__':
    main()
