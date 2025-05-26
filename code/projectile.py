# projectile.py
import pygame
import os

class Projectile:
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y
        self.direction = direction
        self.width = 10
        self.height = 5
        self.active = True
        if owner == "character1":
            self.image = pygame.image.load(os.path.join("assets", "images", "projectile", "projectile01.png")).convert_alpha()
        elif owner == "character2":
            self.image = pygame.image.load(os.path.join("assets", "images", "projectile", "projectile02.png")).convert_alpha()
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
            surface.blit(self.image, self.rect)
