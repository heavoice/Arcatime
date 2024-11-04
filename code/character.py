import pygame
import os

class Character():
    def __init__(self, x, y):
        # Correct the path to the idle image
        image_path = os.path.join("D:\\", "Hworld", "Python", "Arcatime", "assets", "images", "sprites", "jake", "idle.png")
        
        # Load the idle image
        self.idle_image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.idle_image.get_rect(topleft=(x, y))
        
        # Other attributes
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        self.target_health = 100
        self.attack_cooldown = 0

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 5
        GRAVITY = 2
        dx = 0
        dy = 0

        # Key press
        key = pygame.key.get_pressed()

        # Perform actions only if not currently attacking or on cooldown
        if not self.attacking and self.attack_cooldown == 0:
            # Movement
            if key[pygame.K_a]:  # Move left
                dx = -SPEED
            if key[pygame.K_d]:  # Move right
                dx = SPEED

            # Attack
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attacking = True
                self.attack(surface, target)

                # Skill 1
                if key[pygame.K_r]:
                    self.attack_type = 1
                # Skill 2
                if key[pygame.K_t]:
                    self.attack_type = 2

        # Jump
        if key[pygame.K_w] and not self.jump:  # Jump
            self.vel_y = -25
            self.jump = True

        # Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Character stays within screen boundaries
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 40:  # Assume a ground level at 40 pixels from the bottom
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 40 - self.rect.bottom

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        # Update health gradually
        self.update_health()

        # Reduce cooldown timer
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def attack(self, surface, target):
        # Create an attacking rectangle area to detect collision
        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, self.rect.width, self.rect.height)

        # Only decrease target's health if attack collides with target
        if attacking_rect.colliderect(target.rect):
            target.target_health -= 10  # Reduce target health only on hit

        # Draw the attack rectangle for visual feedback
        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

        # Set cooldown after each attack
        self.attack_cooldown = 20  # Adjust cooldown time as needed
        self.attacking = False  # Reset attacking state immediately

    def update_health(self):
        # Gradually decrease health until it reaches target_health
        if self.health > self.target_health:
            self.health -= 0.5  # Adjust speed of decrease as needed

    def draw(self, surface):
        scale_factor = 2  # Adjust this value to increase/decrease size while keeping position constant
        new_width = int(self.idle_image.get_width() * scale_factor)  # Scale width
        new_height = int(self.idle_image.get_height() * scale_factor)  # Scale height
        
        # Create a scaled version of the image
        scaled_image = pygame.transform.scale(self.idle_image, (new_width, new_height))
        
        # Calculate the new position to keep the character centered
        new_x = self.rect.x - (new_width - self.rect.width) // 2
        new_y = self.rect.y - (new_height - self.rect.height) // 2
        
        # Draw the scaled image at the new position
        surface.blit(scaled_image, (new_x, new_y))
        
        # Update rect to the new scaled dimensions for collision detection
        self.rect = scaled_image.get_rect(center=(new_x + new_width // 2, new_y + new_height // 2))
