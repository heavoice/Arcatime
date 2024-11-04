import pygame
from character import Character
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, YELLOW, RED, BACKGROUND_IMAGE_PATH

pygame.init()

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Arcatime')

# Set frame rate
clock = pygame.time.Clock()

# Load background image
bg_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha()

# Function to draw background
def background():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function to draw health bar
def health(current_health, target_health, x, y):
    max_width = 200  # Maximum width of the health bar
    health_width = int(max_width * (current_health / 100))  
    target_width = int(max_width * (target_health / 100))  

    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, max_width + 4, 34), 2)  # Draw white outline
    pygame.draw.rect(screen, YELLOW, (x, y, max_width, 30))  # Full bar in yellow
    pygame.draw.rect(screen, RED, (x, y, health_width, 30))  # Health amount in red

    # Gradually decrease health to target
    if current_health > target_health:
        current_health -= 0.1  # Adjust rate as needed
    return current_health

# Create instances of Character
character_1 = Character(150, 310)
character_2 = Character(525, 310)  # Set y coordinate same as character_1

# Game loop
run = True
while run:
    clock.tick(FPS)

    # Draw background
    background()

    # Show health and update character health gradually
    character_1.health = health(character_1.health, character_1.target_health, 30, 20)
    character_2.health = health(character_2.health, character_2.target_health, 470, 20)

    # Move characters
    character_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_2)
    character_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_1)

    # Draw characters
    character_1.draw(screen)
    character_2.draw(screen)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update display
    pygame.display.update()

# Exit
pygame.quit()
