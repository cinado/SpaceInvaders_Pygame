import os
import pygame
from enum import Enum
import random

HEIGHT = 750
WIDTH = 700

player_velocity = 5
ENEMY_VELOCITY = 1
ENEMY_WIDTH = 50

PLAYER_SPACE_SHIP_UNSCALED_IMG = pygame.image.load(os.path.join("images", "playerspaceship.png"))
PLAYER_SPACE_SHIP = pygame.transform.scale_by(PLAYER_SPACE_SHIP_UNSCALED_IMG, 0.4)

BLUE_ENEMY_UNSCALED_IMG = pygame.image.load(os.path.join("images", "blueenemy.png"))
PINK_ENEMY_UNSCALED_IMG = pygame.image.load(os.path.join("images", "pinkenemy.png"))
GREEN_ENEMY_UNSCALED_IMG = pygame.image.load(os.path.join("images", "greenenemy.png"))

BLUE_ENEMY = pygame.transform.scale(BLUE_ENEMY_UNSCALED_IMG, (
    ENEMY_WIDTH, BLUE_ENEMY_UNSCALED_IMG.get_height() * (ENEMY_WIDTH / BLUE_ENEMY_UNSCALED_IMG.get_width())))
PINK_ENEMY = pygame.transform.scale(PINK_ENEMY_UNSCALED_IMG, (
    ENEMY_WIDTH, PINK_ENEMY_UNSCALED_IMG.get_height() * (ENEMY_WIDTH / PINK_ENEMY_UNSCALED_IMG.get_width())))
GREEN_ENEMY = pygame.transform.scale(GREEN_ENEMY_UNSCALED_IMG, (
    ENEMY_WIDTH, GREEN_ENEMY_UNSCALED_IMG.get_height() * (ENEMY_WIDTH / GREEN_ENEMY_UNSCALED_IMG.get_width())))

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


class LaserBullet:
    def __init__(self, position_x, position_y, laser_bullet_image):
        self.position_x = position_x
        self.position_y = position_y
        self.laser_bullet_image = laser_bullet_image


class Weapon:
    def __init__(self, laser_bullet_image):
        self.laser_bullet_image = laser_bullet_image

    def shoot_laser_bullet(self, position_x, position_y):
        return LaserBullet(position_x, position_y, self.laser_bullet_image)


class DefaultEnemyWeapon(Weapon):
    ENEMY_LASER = [BLUE_LASER, GREEN_LASER]

    def __init__(self):
        super().__init__(random.choice(self.ENEMY_LASER))


class DefaultPlayerWeapon(Weapon):
    def __init__(self):
        super().__init__(RED_LASER)


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


class Enemy(Ship):
    ENEMY_IMAGES = [BLUE_ENEMY, PINK_ENEMY, GREEN_ENEMY]

    def __init__(self, position_x, position_y, health=100):
        super().__init__(position_x, position_y, health)
        self.spaceship_image = random.choice(self.ENEMY_IMAGES)

    def move(self, velocity):
        self.positionY += velocity


def main():
    def update_window():
        WINDOW.blit(BACKGROUND, (0, 0))

        for enemy in alive_enemies:
            enemy.draw(WINDOW)

        player_ship.draw(WINDOW)
        pygame.display.update()

    running_game = True
    max_fps = 60
    clock = pygame.time.Clock()
    player_ship = PlayerShip(WIDTH // 2, 400)
    alive_enemies = []
    level = 0
    enemies_for_each_wave = 0

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

        if len(alive_enemies) == 0:
            level += 1
            enemies_for_each_wave += 5
            for i in range(enemies_for_each_wave):
                new_enemy = Enemy(random.randrange(25, WIDTH - BLUE_ENEMY.get_width()), random.randrange(-1500, -50))
                alive_enemies.append(new_enemy)

        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running_game = False
                pygame.quit()

        pressed_keys = pygame.key.get_pressed()
        for key, action in keys_actions.items():
            if pressed_keys[key]:
                action()

        for enemy in alive_enemies:
            enemy.move(ENEMY_VELOCITY)


main()
