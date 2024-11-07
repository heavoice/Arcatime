# main.py
import pygame
from character import Character
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, YELLOW, RED, BACKGROUND_IMAGE_PATH

pygame.init()

# Define control schemes for Character 1 and Character 2
controls_player1 = {
    "move_left": pygame.K_a,
    "move_right": pygame.K_d,
    "jump": pygame.K_w,
    "attack1": pygame.K_r,
    "attack2": pygame.K_t
}

controls_player2 = {
    "move_left": pygame.K_LEFT,
    "move_right": pygame.K_RIGHT,
    "jump": pygame.K_UP,
    "attack1": pygame.K_KP1,  # Example for number pad attack 1
    "attack2": pygame.K_KP2   # Example for number pad attack 2
}

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

# Create instances of Character with respective controls
character_1 = Character(150, 310, character_name="character1", controls=controls_player1)
character_2 = Character(525, 310, character_name="character2", controls=controls_player2)

# Game loop
run = True
while run:
    clock.tick(FPS)

    # Draw background
    background()

    # Draw projectiles after updating
    character_1.draw_projectiles(screen)
    character_2.draw_projectiles(screen)

    # Update health and characters
    character_1.health = health(character_1.health, character_1.target_health, 30, 20)
    character_2.health = health(character_2.health, character_2.target_health, 470, 20)

    # Pass correct arguments to move function
    character_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_2)
    character_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_1)

    # Draw projectiles
    character_1.draw_projectiles(screen)
    character_2.draw_projectiles(screen)

    # Check for game over
    if character_1.is_dead():
        font = pygame.font.SysFont("Arial", 30)
        game_over_text = font.render("Game Over - Character 2 Wins!", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        run = False
    elif character_2.is_dead():
        font = pygame.font.SysFont("Arial", 30)
        game_over_text = font.render("Game Over - Character 1 Wins!", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        run = False

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == controls_player1["attack1"]:
                character_1.attack(screen, character_2)  # Pass arguments
            elif event.key == controls_player2["attack1"]:
                character_2.attack(screen, character_1)  # Pass arguments

    # Draw characters
    character_1.draw(screen)
    character_2.draw(screen)

    # Update display
    pygame.display.update()

# Exit
pygame.quit()
