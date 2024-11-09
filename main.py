import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Window Example")

# Set up colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with blue color
    screen.fill(BLUE)

    # Update the display
    pygame.display.flip()

# Clean up and close the window
pygame.quit()
sys.exit()
