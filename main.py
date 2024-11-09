SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024



# Initialize Pygame
pygame.init()


# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Width: 800, Height: 600
pygame.display.set_caption("Basic Pygame Window")


# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

        
if __name__ == '__main__':
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()
