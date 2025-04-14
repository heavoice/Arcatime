# timer.py
import pygame
from settings import WHITE

class Timer:
    def __init__(self, total_time):
        self.total_time = total_time  # Total time in seconds
        self.start_ticks = pygame.time.get_ticks()  # Start time

    def get_time_left(self):
        # Calculate time left in seconds
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        time_left = max(self.total_time - int(elapsed_time), 0)
        return time_left

    def draw(self, screen, x, y):
        font = pygame.font.SysFont("Arial", 24)
        time_left = self.get_time_left()
        timer_text = font.render(f"{time_left}", True, WHITE)
        screen.blit(timer_text, (x, y))
