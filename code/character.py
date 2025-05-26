#character.py
import pygame
import os
from projectile import Projectile

class Character:
    def __init__(self, x, y, character_name, controls, facing_left):
        super().__init__()
        self.x = x
        self.y = y
        self.character_name = character_name
        self.controls = controls
        self.projectiles = []
        

        # Load idle and walking images
        self.idle_l_image = self.load_image("idle-l.png")
        self.idle_r_image = self.load_image("idle-r.png")
        self.walk_r_images = [self.load_image(f"walk-r-{i}.png") for i in range(1, 7)]
        self.walk_l_images = [self.load_image(f"walk-l-{i}.png") for i in range(1, 7)]
        self.current_image = self.idle_l_image if facing_left else self.idle_r_image
        self.rect = self.current_image.get_rect(topleft=(x, y))

        # Initialize other attributes
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        self.target_health = 100
        self.attack_cooldown = 0
        self.anim_index = 0
        self.anim_cooldown = 5
        self.anim_timer = 0
        self.direction = 1  # Default direction (right)
        self.facing_left = facing_left

    def load_image(self, filename):
        """ Helper method to load images with path construction """
        path = os.path.join("assets", "images", "character", self.character_name, filename)
        return pygame.image.load(path).convert_alpha()

    def take_damage(self, amount=5):
        """ Decrease health by a specified amount """
        self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def move(self, screen_width, screen_height, surface, target):
        """ Handle movement, jumping, gravity, and attacking logic """
        SPEED = 5
        GRAVITY = 2
        dx, dy = 0, 0

        key = pygame.key.get_pressed()

        # Handle movement regardless of attack state
        if key[self.controls["move_left"]]:
            dx = -SPEED
            self.direction = -1  # Set direction to left
        if key[self.controls["move_right"]]:
            dx = SPEED
            self.direction = 1  # Set direction to right

        if key[self.controls["jump"]] and not self.jump:
            self.vel_y = -25
            self.jump = True

        # Gravity and vertical movement
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Keep the character within screen boundaries
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 40:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 40 - self.rect.bottom

        # Update the character's position
        self.rect.x += dx
        self.rect.y += dy

        # Update health and attack cooldown
        self.update_health()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update animation frame based on movement
        if dx != 0:
            self.facing_left = self.direction == -1  # Update arah pandang berdasarkan arah gerak
            self.anim_timer += 1
            if self.anim_timer >= self.anim_cooldown:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(self.walk_l_images)

            if self.direction == -1:  # Moving left
                self.current_image = self.walk_l_images[self.anim_index]
            else:  # Moving right
                self.current_image = self.walk_r_images[self.anim_index]
        else:
            if self.direction == -1:
                self.current_image = self.idle_l_image
            else:
                self.current_image = self.idle_r_image



        # Handle projectile movement and collisions
        for projectile in self.projectiles:
            projectile.move()
            projectile.draw(surface)
            if projectile.rect.colliderect(target.rect):
                target.take_damage()  # Handle damage to the target
                projectile.active = False

        # Remove inactive projectiles
        self.projectiles = [p for p in self.projectiles if p.active]

    def draw_projectiles(self, surface):
        """ Draw all active projectiles """
        for projectile in self.projectiles:
            projectile.draw(surface)

    def attack(self, surface, target):
        """ Handle the attack logic and projectiles """
        self.direction = -1 if self.facing_left else 1
        if self.attack_cooldown == 0:
            offset_x = 30 if self.direction == 1 else -30
            projectile = Projectile(
                self.rect.centerx + offset_x,
                self.rect.centery + 10,
                self.direction,
                self.character_name
            )
            self.projectiles.append(projectile)
            self.attack_cooldown = 20

        for projectile in self.projectiles:
            projectile.move()
            projectile.draw(surface)
            if projectile.rect.colliderect(target.rect):
                target.take_damage()  # Handle damage to the target
                projectile.active = False

        self.projectiles = [p for p in self.projectiles if p.active]

    def update_health(self):
        """ Gradually decrease health towards target health """
        if self.health > self.target_health:
            self.health -= 0.5
        if self.target_health <= 0:
            self.health = 0

    def draw(self, screen):
        """ Draw the character on the screen """
        scale_factor = 2
        new_width = int(self.current_image.get_width() * scale_factor)
        new_height = int(self.current_image.get_height() * scale_factor)

        # Tentukan apakah perlu di-flip
        flip = self.direction == -1
        if self.facing_left:
            flip = not flip  # Balik logika jika default menghadap kiri

        # Flip horizontal jika perlu
        image_to_draw = pygame.transform.flip(self.current_image, flip, False)

        # Scale dan gambar
        scaled_image = pygame.transform.scale(image_to_draw, (new_width, new_height))
        new_x = self.rect.x - (new_width - self.rect.width) // 2
        new_y = self.rect.y - (new_height - self.rect.height) // 2
        screen.blit(scaled_image, (new_x, new_y))

        # Update rect
        self.rect = scaled_image.get_rect(center=(new_x + new_width // 2, new_y + new_height // 2))

    def is_dead(self):
        """ Check if the character is dead """
        return self.health <= 0
