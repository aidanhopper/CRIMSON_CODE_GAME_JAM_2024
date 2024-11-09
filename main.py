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

# Player properties
PLAYER_SPEED = 5
PLAYER_JUMP_VELOCITY = -15
GRAVITY = 0.8

# Platform properties
PLATFORM_VERTICAL_DISTANCE = 80  # Max distance between platforms vertically

# Fonts
FONT_NAME = pygame.font.match_font('arial')

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump Clone with Sprites")
clock = pygame.time.Clock()

# Load Images
try:
    player_image = pygame.image.load('assets/player.png').convert_alpha()
    platform_image = pygame.image.load('assets/platform.png').convert_alpha()
    background_image = pygame.image.load('assets/background.png').convert()
    game_over_image = pygame.image.load('assets/game_over.png').convert_alpha()  # Load Game Over Image
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

# Scale images as needed
player_image = pygame.transform.scale(player_image, (50, 50))
platform_image = pygame.transform.scale(platform_image, (70, 10))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit screen

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
        self.image = player_image
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
        self.image = platform_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Game functions
def generate_platforms(platforms, all_sprites):
    while len(platforms) < 10:
        last_platform = max(platforms, key=lambda p: p.rect.y)
        new_y = last_platform.rect.y - random.randint(50, PLATFORM_VERTICAL_DISTANCE)
        new_x = random.randint(0, SCREEN_WIDTH - platform_image.get_width())
        new_platform = Platform(new_x, new_y)
        platforms.add(new_platform)
        all_sprites.add(new_platform)

def show_menu():
    screen.blit(background_image, (0, 0))
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
    # Blit the Game Over image to cover the entire screen
    screen.blit(game_over_image, (0, 0))  # Position at top-left corner

    # Overlay the score on the Game Over image
    draw_text(screen, f"Score: {score}", 36, (255, 255, 255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50, align="center")
    draw_text(screen, "Press R to Restart or Q to Quit", 24, (255, 255, 255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10, align="center")
    
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
    for i in range(10):
        x = random.randint(0, SCREEN_WIDTH - platform_image.get_width())
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
                        new_x = random.randint(0, SCREEN_WIDTH - platform_image.get_width())
                        new_platform = Platform(new_x, new_y)
                        platforms.add(new_platform)
                        all_sprites.add(new_platform)

        # Generate more platforms if needed
        generate_platforms(platforms, all_sprites)

        # Game over condition
        if player.rect.top > SCREEN_HEIGHT:
            running = False

        # Draw everything
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        # Optionally, draw additional elements (e.g., sun, clouds)
        pygame.draw.circle(screen, (255, 255, 0), (50, 50), 20)  # Sun

        # Display the score
        draw_text(screen, f"Score: {player.score}", 24, BLACK, 10, 10)

        # Update the display
        pygame.display.flip()

    show_game_over(player.score)

# Start the game with the menu
show_menu()
main_game()
