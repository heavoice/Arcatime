import pygame
from logic.movement import movement  # Import the movement function

# Load character walking sprites
walkRight = [
    pygame.image.load('assets/character/R1.png'),
    pygame.image.load('assets/character/R2.png'),
    pygame.image.load('assets/character/R3.png'),
    pygame.image.load('assets/character/R4.png'),
    pygame.image.load('assets/character/R5.png'),
    pygame.image.load('assets/character/R6.png')
]

# Resize the sprites to a new size (e.g., 80x120 pixels)
scaled_walkRight = [pygame.transform.scale(sprite, (80, 120)) for sprite in walkRight]

bg = [pygame.image.load('assets/background/bg.jpg')]

# Initialize global variables
walkCount = 0


def screen(win, x, y, vel, width, height):
    global walkCount
    win.fill((0, 0, 0))  # Clear the window before drawing anything

    # Draw the background first
    win.blit(bg[0], (0, 0))  # Draw the background image

    # Update x and y positions based on movement
    x, y = movement(x, y, vel, width, height)

    # Determine which frame to display based on walkCount
    if walkCount + 1 >= len(scaled_walkRight):  # Loop back to the first frame after the last one
        walkCount = 0
    else:
        walkCount += 1

    # Draw the character walking animation (use scaled sprites)
    win.blit(scaled_walkRight[walkCount], (x, y))

    # Update the display
    pygame.display.update()

    return x, y
