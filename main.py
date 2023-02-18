import os
import pygame
from enum import Enum
import random

HEIGHT = 750
WIDTH = 700

pygame.font.init()

player_velocity = 5
ENEMY_VELOCITY = 1
LASER_VELOCITY = 4
ENEMY_WIDTH = 50
LASER_WIDTH = 30

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

BLUE_LASER_UNSCALED_IMG = pygame.image.load(os.path.join("images", "bluelaser.png"))
RED_LASER_UNSCALED_IMG = pygame.image.load(os.path.join("images", "redlaser.png"))
GREEN_LASER_UNSCALED_IMG = pygame.image.load(os.path.join("images", "greenlaser.png"))

BLUE_LASER = pygame.transform.scale(BLUE_LASER_UNSCALED_IMG, (
    LASER_WIDTH, BLUE_LASER_UNSCALED_IMG.get_height() * (LASER_WIDTH / BLUE_LASER_UNSCALED_IMG.get_width())))
RED_LASER = pygame.transform.scale(RED_LASER_UNSCALED_IMG, (
    LASER_WIDTH, RED_LASER_UNSCALED_IMG.get_height() * (LASER_WIDTH / RED_LASER_UNSCALED_IMG.get_width())))
GREEN_LASER = pygame.transform.scale(GREEN_LASER_UNSCALED_IMG, (
    LASER_WIDTH, GREEN_LASER_UNSCALED_IMG.get_height() * (LASER_WIDTH / GREEN_LASER_UNSCALED_IMG.get_width())))

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
        self.mask = pygame.mask.from_surface(self.laser_bullet_image)

    def move(self, velocity):
        self.position_y += velocity

    def draw(self, window):
        window.blit(self.laser_bullet_image, (self.position_x, self.position_y))

    def check_if_outside_window(self):
        return not (0 <= self.position_y <= HEIGHT)

    def check_collision(self, obj):
        return check_if_objects_collide(self, obj)


def check_if_objects_collide(first_object, second_object):
    x_difference = second_object.position_x - first_object.position_x
    y_difference = second_object.position_y - first_object.position_y
    return first_object.mask.overlap(second_object.mask, (x_difference, y_difference)) is not None


class Weapon:
    def __init__(self, laser_bullet_image, cooldown=700):
        self.laser_bullet_image = laser_bullet_image
        self.cooldown = cooldown
        self.last_shot = 0

    def shoot_laser_bullet(self, position_x, position_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.cooldown:
            self.last_shot = current_time
            return LaserBullet(position_x, position_y, self.laser_bullet_image)
        else:
            return None


class DefaultEnemyWeapon(Weapon):
    ENEMY_LASER = [BLUE_LASER, GREEN_LASER]

    def __init__(self):
        super().__init__(random.choice(self.ENEMY_LASER))


class DefaultPlayerWeapon(Weapon):
    def __init__(self):
        super().__init__(RED_LASER)


class Ship:
    def __init__(self, position_x, position_y, health=100):
        self.position_x = position_x
        self.position_y = position_y
        self.health = health
        self.spaceship_image = None
        self.weapon = None
        self.shot_laser_bullets = list()

    def get_width(self):
        return self.spaceship_image.get_width()

    def get_height(self):
        return self.spaceship_image.get_height()

    def draw(self, window):
        window.blit(self.spaceship_image, (self.position_x, self.position_y))
        for laser in self.shot_laser_bullets:
            laser.draw(window)

    def shoot(self):
        lasers = self.weapon.shoot_laser_bullet(self.position_x + (self.get_width()//2.9), self.position_y)
        if lasers is not None:
            self.shot_laser_bullets.append(lasers)

    def move_shot_laser_bullets(self, velocity):
        for laser_bullet in self.shot_laser_bullets:
            laser_bullet.move(velocity)
            if laser_bullet.check_if_outside_window():
                self.shot_laser_bullets.remove(laser_bullet)


class PlayerShip(Ship):
    def __init__(self, position_x, position_y, health=100):
        super().__init__(position_x, position_y, health)
        self.spaceship_image = PLAYER_SPACE_SHIP
        self.weapon = DefaultPlayerWeapon()
        self.mask = pygame.mask.from_surface(self.spaceship_image)
        self.healthbar = Healthbar(self.health, self.position_x, self.position_y, self.get_height(),
                                   self.get_width())

    def check_if_in_window(self, direction):
        if direction.name == "RIGHT":
            return (self.position_x + self.get_width() + direction.value[1]) < WIDTH
        elif direction.name == "LEFT":
            return (self.position_x + direction.value[1]) > 0
        elif direction.name == "DOWN":
            return (self.position_y + self.get_height() + direction.value[1]) < HEIGHT
        elif direction.name == "UP":
            return (self.position_y + direction.value[1]) > 0

    def move(self, direction):
        if self.check_if_in_window(direction):
            match direction.name:
                case "RIGHT":
                    self.position_x += direction.value[1]
                case "LEFT":
                    self.position_x += direction.value[1]
                case "DOWN":
                    self.position_y += direction.value[1]
                case "UP":
                    self.position_y += direction.value[1]

    def move_shot_laser_bullets(self, velocity, enemies):
        super().move_shot_laser_bullets(velocity)
        for shot_laser in self.shot_laser_bullets:
            for enemy in enemies:
                if shot_laser.check_collision(enemy):
                    enemies.remove(enemy)
                    self.shot_laser_bullets.remove(shot_laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar.update_position(self.position_x, self.position_y)
        self.healthbar.draw(window)

class Healthbar:
    def __init__(self, current_health, position_x, position_y, space_ship_height, width, height=10, max_health = 100):
        self.current_health = current_health
        self.position_x = position_x
        self.position_y = position_y + space_ship_height
        self.max_health = max_health
        self.width = width
        self.height = height
        self.space_ship_height = space_ship_height

    def update_health(self, current_health):
        self.current_health = current_health

    def update_position(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y + self.space_ship_height

    def draw(self, window):
        current_health_ration = self.current_health / self.max_health
        healthbar_width = int(self.width * current_health_ration)

        bar_surface = pygame.Surface((self.width, self.height))
        bar_surface.fill((255, 0, 0))
        bar_surface.set_alpha(128)

        pygame.draw.rect(bar_surface, (0, 255, 0), (0, 0, healthbar_width, self.height))
        window.blit(bar_surface, (self.position_x, self.position_y))


class Enemy(Ship):
    ENEMY_IMAGES = [BLUE_ENEMY, PINK_ENEMY, GREEN_ENEMY]

    def __init__(self, position_x, position_y, health=100):
        super().__init__(position_x, position_y, health)
        self.spaceship_image = random.choice(self.ENEMY_IMAGES)
        self.weapon = DefaultEnemyWeapon()
        self.mask = pygame.mask.from_surface(self.spaceship_image)

    def move(self, velocity):
        self.position_y += velocity

    def move_shot_laser_bullets(self, velocity, player):
        super().move_shot_laser_bullets(velocity)
        for shot_laser in self.shot_laser_bullets:
            if shot_laser.check_collision(player):
                player.health -= 10
                player.healthbar.update_health(player.health)
                self.shot_laser_bullets.remove(shot_laser)


def main():
    def update_window():
        WINDOW.blit(BACKGROUND, (0, 0))

        level_text = information_bar_font.render(f"Level: {level}", True, (255, 255, 255))
        lives_text = information_bar_font.render(f"Lives: {lives}", True, (255, 255, 255))

        WINDOW.blit(lives_text, (10, 5))
        WINDOW.blit(level_text, (WIDTH - level_text.get_width() - 10, 5))

        for each_enemy in alive_enemies:
            each_enemy.draw(WINDOW)

        player_ship.draw(WINDOW)
        pygame.display.update()

    running_game = True
    max_fps = 60
    clock = pygame.time.Clock()
    player_ship = PlayerShip(WIDTH // 2, 400)
    alive_enemies = []
    level = 0
    lives = 5
    enemies_for_each_wave = 0
    information_bar_font = pygame.font.SysFont("source_sans_pro", 40)

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
                new_enemy = Enemy(random.randrange(25, WIDTH - (int(1.25*BLUE_ENEMY.get_width()))),
                                  random.randrange(-1500, -50))
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
            enemy.move_shot_laser_bullets(LASER_VELOCITY, player_ship)
            if random.randrange(0, 2 * max_fps) == 7:
                enemy.shoot()

            if check_if_objects_collide(player_ship, enemy):
                player_ship.health -= 10
                player_ship.healthbar.update_health(player_ship.health)
                alive_enemies.remove(enemy)
            elif (enemy.position_y + enemy.get_height()) > HEIGHT:
                alive_enemies.remove(enemy)
                lives -= 1

        player_ship.move_shot_laser_bullets(-LASER_VELOCITY, alive_enemies)


main()
