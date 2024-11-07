# projectile.py
import pygame
import os

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.width = 10
        self.height = 5
        self.active = True
        self.image = pygame.Surface((self.width, self.height))  # Dummy projectile image
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        # Move the projectile depending on direction
        SPEED = 10
        self.x += SPEED * self.direction
        self.rect.x = self.x
        if self.x < 0 or self.x > 800:  # Arbitrary screen width
            self.active = False  # Deactivate if out of bounds

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Red colored projectile
