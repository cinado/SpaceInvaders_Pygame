import os
import pygame

HEIGHT = 750
WIDTH = 700

PLAYER_SPACE_SHIP = pygame.image.load(os.path.join("images", "playerspaceship.png"))

BLUE_ENEMY = pygame.image.load(os.path.join("images", "blueenemy.png"))
PINK_ENEMY = pygame.image.load(os.path.join("images", "pinkenemy.png"))
GREEN_ENEMY = pygame.image.load(os.path.join("images", "greenenemy.png"))

BLUE_LASER = pygame.image.load(os.path.join("images", "bluelaser.png"))
RED_LASER = pygame.image.load(os.path.join("images", "redlaser.png"))
GREEN_LASER = pygame.image.load(os.path.join("images", "greenlaser.png"))

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Space Invaders")
pygame.display.set_icon(pygame.image.load(os.path.join("images", "logo.png")))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background.png")), (WIDTH, HEIGHT))


class Ship:
    def __init__(self, position_x, position_y, health=100):
        self.positionX = position_x
        self.positionY = position_y
        self.health = health
        self.spaceship_image = None

    def draw(self, window):
        window.blit(self.spaceship_image, (self.positionX, self.positionY))


class PlayerShip(Ship):
    def __init__(self, position_x, position_y, health=100):
        super().__init__(position_x, position_y, health)
        self.spaceship_image = PLAYER_SPACE_SHIP



def main():
    def update_window():
        WINDOW.blit(BACKGROUND, (0, 0))
        player_ship.draw(WINDOW)
        pygame.display.update()

    running_game = True
    max_fps = 60
    clock = pygame.time.Clock()
    player_ship = PlayerShip(WIDTH // 2, 400)

    while running_game:
        # Limits the framerate to max_fps
        clock.tick(max_fps)
        update_window()
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running_game = False
                pygame.quit()


main()
