import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1050, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load background image
background_image = pygame.image.load("Img/bg.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load bird image
bird_image = pygame.image.load("Img/birds11.png")
bird_image = pygame.transform.scale(bird_image, (50, 50))  # Resize as needed

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (70, 200, 250)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game variables
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 15
bird_velocity = 0
gravity = 0.5
jump_strength = -10
pipe_width = 60
pipe_gap = 150
pipe_velocity = 4
pipes = []
score = 0

high_score = 0
lives = 3
distance = 0
running = True
game_over = False
current_screen = "start"  # Start with the starting screen

# Function to read the high score from the file
def read_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            content = file.read().strip()  # Strip any extra whitespace or newline characters
            return int(content) if content else 0  # Return 0 if the file is empty
    else:
        return 0   # Default to 0 if no file exists

# Function to save the high score to the file
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Function to reset the game
def reset_game():
    global bird_y, bird_velocity, pipes, score, distance, lives, game_over
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    distance = 0
    lives = 3
    game_over = False

# Function to spawn a new pipe
def spawn_pipe():
    pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
    pipes.append({"x": WIDTH, "top": pipe_height, "bottom": pipe_height + pipe_gap})

# Function to draw a button
def draw_button(screen, text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Change color if hovered
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    # Add text to the button
    font = pygame.font.Font(None, 40)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Function to display the starting screen
def start_screen():
    global current_screen, high_score
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 80)
    title_text = font.render("Flappy Bird", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - 200, HEIGHT // 2 - 250))

    # Display the high score
    font = pygame.font.Font(None, 50)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH // 2 - 150, HEIGHT // 2 - 180))

    # Draw buttons
    draw_button(screen, "Start", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GRAY, GREEN, lambda: set_screen("game"))
    draw_button(screen, "Settings", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, GRAY, GREEN, lambda: set_screen("settings"))
    draw_button(screen, "About Us", WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, GRAY, GREEN, lambda: set_screen("about"))
    draw_button(screen, "Quit", WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 50, GRAY, RED, quit_game)
    pygame.display.flip()

# Function to display the settings screen
def settings_screen():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Settings", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))

    # Add a back button
    draw_button(screen, "Back", 10, 10, 100, 50, GRAY, RED, lambda: set_screen("start"))
    pygame.display.flip()

# Function to display the about us screen
def about_screen():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 40)
    title_text = font.render("About the Developer", True, WHITE)
    dev_text = font.render("Tushar Albert Burney", True, WHITE)
    desc_text = font.render("Passionate developer & game designer.", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - 200, HEIGHT // 2 - 150))
    screen.blit(dev_text, (WIDTH // 2 - 200, HEIGHT // 2 - 80))
    screen.blit(desc_text, (WIDTH // 2 - 200, HEIGHT // 2 - 30))

    # Add a back button
    draw_button(screen, "Back", 10, 10, 100, 50, GRAY, RED, lambda: set_screen("start"))
    pygame.display.flip()

# Function to set the current screen
def set_screen(screen_name):
    global current_screen
    current_screen = screen_name

# Function to quit the game
def quit_game():
    global running
    running = False

# Main game loop
high_score = read_high_score()  # Read high score at the start
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over and current_screen == "game":
            bird_velocity = jump_strength

    if current_screen == "start":
        start_screen()
        continue
    elif current_screen == "settings":
        settings_screen()
        continue
    elif current_screen == "about":
        about_screen()
        continue

    # Game logic (only when the game screen is active)
    if current_screen == "game":
        # Game over logic
        if game_over:
            if score > high_score:
                high_score = score
                save_high_score(high_score)  # Save new high score to the file

            screen.blit(background_image, (0, 0))
            font = pygame.font.Font(None, 50)
            text = font.render(f"Game Over! Score: {score} Distance: {distance}m", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 250, HEIGHT // 2 - 100))
            draw_button(screen, "Retry", WIDTH // 2 - 150, HEIGHT // 2, 150, 50, GRAY, GREEN, reset_game)
            draw_button(screen, "Home", WIDTH // 2 + 20, HEIGHT // 2, 150, 50, GRAY, RED, lambda: set_screen("start"))
            pygame.display.flip()
            continue

        # Update bird
        bird_velocity += gravity
        bird_y += bird_velocity

        # Create a rectangle around the bird for collision detection
        bird_rect = pygame.Rect(bird_x - 25, int(bird_y) - 25, 50, 50)

        # Update pipes and check for collisions
        for pipe in pipes:
            pipe["x"] -= pipe_velocity
            top_pipe_rect = pygame.Rect(pipe["x"], 0, pipe_width, pipe["top"])
            bottom_pipe_rect = pygame.Rect(pipe["x"], pipe["bottom"], pipe_width, HEIGHT - pipe["bottom"])

            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    bird_y = HEIGHT // 2
                    bird_velocity = 0
                break

            if pipe["x"] + pipe_width < 0:
                pipes.remove(pipe)
                score += 1

        # Check if bird hits the ground
        if bird_y + 25 > HEIGHT or bird_y - 25 < 0:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                bird_y = HEIGHT // 2
                bird_velocity = 0

        # Spawn new pipes
        if len(pipes) == 0 or pipes[-1]["x"] < WIDTH // 2:
            spawn_pipe()

        distance += pipe_velocity // 4

        screen.blit(background_image, (0, 0))

        screen.blit(bird_image, (bird_x - 25, int(bird_y) - 25))

        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))  # Top pipe
            pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], pipe_width, HEIGHT - pipe["bottom"]))  # Bottom pipe

        # Draw score, lives, and distance
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        distance_text = font.render(f"Distance: {distance}m", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(distance_text, (10, 90))

        pygame.display.flip()
        clock.tick(30)

# Quit the game
pygame.quit()
