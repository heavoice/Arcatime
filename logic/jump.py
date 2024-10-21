import pygame

def jump(isJump, jump_count, y):
    keys = pygame.key.get_pressed()

    # If the SPACE key is pressed, set isJump to True
    if keys[pygame.K_SPACE]:
        isJump = True

    # Handle jumping logic
    if isJump:
        if jump_count >= -10:  # Jumping logic
            neg = 1
            if jump_count < 0:
                neg = -1
            y -= (jump_count ** 2) * 0.5 * neg  # Quadratic function for jump height
            jump_count -= 1
        else:
            isJump = False
            jump_count = 10  # Reset jump count after jump

    return isJump, jump_count, y  # Return updated values
