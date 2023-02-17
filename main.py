import os
import pygame
from enum import Enum

HEIGHT = 750
WIDTH = 700

player_velocity = 5
enemy_velocity = 1

PLAYER_SPACE_SHIP_UNSCALED_IMG = pygame.image.load(os.path.join("images", "playerspaceship.png"))
PLAYER_SPACE_SHIP = pygame.transform.scale_by(PLAYER_SPACE_SHIP_UNSCALED_IMG, 0.4)

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


class Direction(Enum):
    LEFT = ("LEFT", -player_velocity)
    RIGHT = ("RIGHT", player_velocity)
    UP = ("UP", -player_velocity)
    DOWN = ("DOWN", player_velocity)


class Ship:
    def __init__(self, position_x, position_y, health=100):
        self.positionX = position_x
        self.positionY = position_y
        self.health = health
        self.spaceship_image = None

    def get_width(self):
        return self.spaceship_image.get_width()

    def get_height(self):
        return self.spaceship_image.get_height()

    def draw(self, window):
        window.blit(self.spaceship_image, (self.positionX, self.positionY))

    def shoot(self):
        None
        # TODO: to be implemented


class PlayerShip(Ship):
    def __init__(self, position_x, position_y, health=100):
        super().__init__(position_x, position_y, health)
        self.spaceship_image = PLAYER_SPACE_SHIP

    def check_if_in_window(self, direction):
        if direction.name == "RIGHT":
            return (self.positionX + self.get_width() + direction.value[1]) < WIDTH
        elif direction.name == "LEFT":
            return (self.positionX + direction.value[1]) > 0
        elif direction.name == "DOWN":
            return (self.positionY + self.get_height() + direction.value[1]) < HEIGHT
        elif direction.name == "UP":
            return (self.positionY + direction.value[1]) > 0

    def move(self, direction):
        if self.check_if_in_window(direction):
            match direction.name:
                case "RIGHT":
                    self.positionX += direction.value[1]
                case "LEFT":
                    self.positionX += direction.value[1]
                case "DOWN":
                    self.positionY += direction.value[1]
                case "UP":
                    self.positionY += direction.value[1]


def main():
    def update_window():
        WINDOW.blit(BACKGROUND, (0, 0))
        player_ship.draw(WINDOW)
        pygame.display.update()

    running_game = True
    max_fps = 60
    clock = pygame.time.Clock()
    player_ship = PlayerShip(WIDTH // 2, 400)

    keys_actions = {
        pygame.K_a: lambda: player_ship.move(Direction.LEFT),
        pygame.K_d: lambda: player_ship.move(Direction.RIGHT),
        pygame.K_w: lambda: player_ship.move(Direction.UP),
        pygame.K_s: lambda: player_ship.move(Direction.DOWN),
        pygame.K_SPACE: lambda: player_ship.shoot()
    }

    while running_game:
        # Limits the framerate to max_fps
        clock.tick(max_fps)
        update_window()

        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running_game = False
                pygame.quit()

        pressed_keys = pygame.key.get_pressed()
        for key, action in keys_actions.items():
            if pressed_keys[key]:
                action()


main()
