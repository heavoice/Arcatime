import pygame
import os
print("Current Working Directory:", os.getcwd())
from logic.movement import movement
from logic.jump import jump  
from interface.screen import screen

# Initialize Pygame
pygame.init()

# Window size
win = pygame.display.set_mode((700, 600))

# Set the window title
pygame.display.set_caption("Arcatime")

# Initialize variables
x, y, width, height, vel = 50, 440, 40, 60, 10
isJump = False
jump_count = 10  # Height of the jump

# Main game loop
running = True
while running:
    # Frame rate control
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Call the screen function to update character and background
    x, y = screen(win, x, y, vel, width, height)

    # Handle jumping mechanics
    isJump, jump_count, y = jump(isJump, jump_count, y)

# Quit Pygame
pygame.quit()
