import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump Clone")
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 255))  # Blue color
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150)
        self.vel_y = 0
        self.score = 0

    def update(self):
        # Apply gravity
        self.vel_y += 0.5

        # Move vertically
        self.rect.y += self.vel_y

        # Move horizontally
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Wrap around the screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((70, 10))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create initial platforms
for i in range(7):
    p = Platform(random.randint(0, SCREEN_WIDTH - 70), i * 100)
    all_sprites.add(p)
    platforms.add(p)

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update()

    # Check for collision with platforms
    if player.vel_y > 0:
        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits:
            player.rect.bottom = hits[0].rect.top
            player.vel_y = -10  # Make the player jump

    # If player reaches top quarter of the screen, move platforms down
    if player.rect.top <= SCREEN_HEIGHT / 4:
        player.rect.top = SCREEN_HEIGHT / 4
        for platform in platforms:
            platform.rect.y += abs(player.vel_y)

            # Remove platforms that are off the screen
            if platform.rect.top >= SCREEN_HEIGHT:
                platform.kill()
                player.score += 1
                # Create new platform
                new_platform = Platform(random.randint(0, SCREEN_WIDTH - 70), random.randint(-50, 0))
                all_sprites.add(new_platform)
                platforms.add(new_platform)

    # Game over condition
    if player.rect.top > SCREEN_HEIGHT:
        running = False

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display the score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(player.score), True, BLACK)
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

pygame.quit()