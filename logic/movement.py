import pygame

def movement(x, y, vel, width, height):
    keys = pygame.key.get_pressed()

    # Handle left/right movement
    if keys[pygame.K_a] and x > vel:  # Using 'A' for left movement
        x -= vel
    if keys[pygame.K_d] and x < 700 - width - vel:  # Using 'D' for right movement
        x += vel

    # Handle up/down movement (optional)
    if keys[pygame.K_w] and y > vel:  # Using 'W' for up movement
        y -= vel
    if keys[pygame.K_s] and y < 500 - height - vel:  # Using 'S' for down movement
        y += vel

    return x, y  # Return updated x and y coordinates
