import pygame
import math

from resources import *
class Bullet():
    def __init__(self, x, y, direction):
        self.image = pygame.image.load('assets/bullet.png').convert_alpha()
        self.x = x
        self.y = y
        self.radius = 4
        self.speed = 3
        self.direction = pygame.Vector2(math.cos(direction), math.sin(direction))

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        # Move the bullet
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

        self.rect.center = (self.x, self.y)

    def draw(self):
        base_surface.blit(self.image,self.rect.center)

    def col(self, player):
        if player.rect.collidepoint(self.x, self.y):
            player.damage()
            return True

        return False

class PlayerProjectile():
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.radius = 3
        self.speed = 10
        self.direction = pygame.Vector2(direction).normalize()  # Normalize the direction vector

    def update(self):
        # Move the projectile
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self):
        # Draw the projectile
        projectile = pygame.image.load('assets/player_bullets.png')
        base_surface.blit(projectile, (self.x, self.y))

    def col(self, boss):
        # Check if projectile collides with the boss
        if boss.rect.collidepoint(self.x, self.y):
            boss.health -= 10  # Deal damage to the boss
            return True
        return False


bullets = []  # List to store BOSS projectiles
projectiles = []