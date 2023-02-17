import os
import pygame

HEIGHT = 750
WIDTH = 700

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Space Invaders")
pygame.display.set_icon(pygame.image.load(os.path.join("images", "logo.png")))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background.png")), (WIDTH, HEIGHT))


def main():
    running_game = True

    while running_game:
        WINDOW.blit(BACKGROUND, (0, 0))
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running_game = False
                pygame.quit()


main()
