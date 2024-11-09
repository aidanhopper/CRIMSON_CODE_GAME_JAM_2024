import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player properties
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5
PLAYER_JUMP_VELOCITY = -15
GRAVITY = 0.8

# Platform properties
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 10
PLATFORM_COLOR = GREEN
INITIAL_PLATFORMS = 10
PLATFORM_VERTICAL_DISTANCE = 80  # Max distance between platforms vertically

# Fonts
FONT_NAME = pygame.font.match_font('arial')

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump Clone")
clock = pygame.time.Clock()

# Helper functions
def draw_text(surface, text, size, color, x, y, align="topleft"):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    setattr(text_rect, align, (x, y))
    surface.blit(text_surface, text_rect)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
        self.vel_y = 0
        self.score = 0

    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY

        # Move vertically
        self.rect.y += self.vel_y

        # Move horizontally
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Wrap around the screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH

    def jump(self):
        self.vel_y = PLAYER_JUMP_VELOCITY

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Game functions
def generate_platforms(platforms, all_sprites):
    while len(platforms) < INITIAL_PLATFORMS:
        last_platform = max(platforms, key=lambda p: p.rect.y)
        new_y = last_platform.rect.y - random.randint(50, PLATFORM_VERTICAL_DISTANCE)
        new_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        new_platform = Platform(new_x, new_y)
        platforms.add(new_platform)
        all_sprites.add(new_platform)

def show_menu():
    screen.fill(WHITE)
    draw_text(screen, "Doodle Jump Clone", 48, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, align="center")
    draw_text(screen, "Press any key to start", 36, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, align="center")
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def show_game_over(score):
    screen.fill(WHITE)
    draw_text(screen, "Game Over", 48, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, align="center")
    draw_text(screen, f"Score: {score}", 36, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, align="center")
    draw_text(screen, "Press R to Restart or Q to Quit", 24, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4, align="center")
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main_game():
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # Create the player
    player = Player()
    all_sprites.add(player)

    # Create initial platforms
    for i in range(INITIAL_PLATFORMS):
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        y = SCREEN_HEIGHT - i * 80
        p = Platform(x, y)
        all_sprites.add(p)
        platforms.add(p)

    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        all_sprites.update()

        # Check for collision with platforms
        if player.vel_y > 0:
            hits = pygame.sprite.spritecollide(player, platforms, False)
            if hits:
                # Check if player is above the platform
                if player.rect.bottom <= hits[0].rect.bottom + player.vel_y:
                    player.rect.bottom = hits[0].rect.top
                    player.jump()
        
        # Scroll the screen
        if player.rect.top <= SCREEN_HEIGHT / 4:
            player.rect.top = SCREEN_HEIGHT / 4
            for platform in platforms:
                platform.rect.y += abs(player.vel_y)
                if platform.rect.top >= SCREEN_HEIGHT:
                    platform.kill()
                    player.score += 1
                    # Generate new platform based on the last platform
                    if len(platforms) > 0:
                        last_platform = min(platforms, key=lambda p: p.rect.y)
                        new_y = last_platform.rect.y - random.randint(50, PLATFORM_VERTICAL_DISTANCE)
                        new_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
                        new_platform = Platform(new_x, new_y)
                        platforms.add(new_platform)
                        all_sprites.add(new_platform)
        
        # Generate more platforms if needed
        generate_platforms(platforms, all_sprites)

        # Game over condition
        if player.rect.top > SCREEN_HEIGHT:
            running = False

        # Draw everything
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # Display the score
        draw_text(screen, f"Score: {player.score}", 24, BLACK, 10, 10)

        # Update the display
        pygame.display.flip()

    show_game_over(player.score)

# Start the game with the menu
show_menu()
main_game()