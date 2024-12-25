import pygame
import random
import os
import webbrowser  # Import the webbrowser module

pygame.init()

WIDTH, HEIGHT = 1050, 600   # This will decide how big the screen is.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Sparow")  # Display the Name on the home Screen.

# Default settings
selected_difficulty = "Medium"
selected_theme = "Day"
selected_bird_skin = "Default"

background_image = pygame.image.load("Img/bg.png")  # BG Img ( Change as per you need!!)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
bird_image = pygame.image.load("Img/birds11.png")   # Birds Img .
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
current_screen = "start"  # Defaulte Screen to start with.

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))
def read_high_score():
    if os.path.exists("high_score.txt"):  # Store the best highe score in the .txt file 
        with open("high_score.txt", "r") as file:
            content = file.read().strip()  
            return int(content) if content else 0  
    else:
        return 0   # Default to 0 if no file exists

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
    draw_button(screen, "Start", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GRAY, GREEN, lambda: set_screen("Game"))  
    draw_button(screen, "Settings", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, GRAY, GREEN, lambda: set_screen("settings"))
    draw_button(screen, "About Us", WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, GRAY, GREEN, lambda: set_screen("about"))
    draw_button(screen, "Quit", WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 50, GRAY, RED, quit_game)
    pygame.display.flip()


def settings_screen():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Settings", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))

    # Add a back button
    draw_button(screen, "Back", 10, 10, 100, 50, GRAY, RED, lambda: set_screen("start"))
    pygame.display.flip()

# def settings_screen():
#     running = True
#     global selected_difficulty, selected_theme, selected_bird_skin

#     while running:
#         screen.fill(BLACK)  # Settings background color

#         # Title
#         font_title = pygame.font.Font(None, 60)
#         title_text = font_title.render("Settings", True, WHITE)
#         title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
#         screen.blit(title_text, title_rect)

#         # Difficulty Setting
#         font_option = pygame.font.Font(None, 40)
#         difficulty_text = font_option.render(f"Difficulty: {selected_difficulty}", True, WHITE)
#         difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2, 150))
#         screen.blit(difficulty_text, difficulty_rect)

#         draw_button(screen, "Easy", WIDTH // 2 - 150, 200, 100, 50, GRAY, GREEN, lambda: change_difficulty("Easy"))
#         draw_button(screen, "Medium", WIDTH // 2 - 50, 200, 100, 50, GRAY, GREEN, lambda: change_difficulty("Medium"))
#         draw_button(screen, "Hard", WIDTH // 2 + 50, 200, 100, 50, GRAY, GREEN, lambda: change_difficulty("Hard"))

#         # Theme Setting
#         theme_text = font_option.render(f"Theme: {selected_theme}", True, WHITE)
#         theme_rect = theme_text.get_rect(center=(WIDTH // 2, 300))
#         screen.blit(theme_text, theme_rect)

#         draw_button(screen, "Day", WIDTH // 2 - 150, 350, 100, 50, GRAY, GREEN, lambda: change_theme("Day"))
#         draw_button(screen, "Night", WIDTH // 2 - 50, 350, 100, 50, GRAY, GREEN, lambda: change_theme("Night"))
#         draw_button(screen, "Winter", WIDTH // 2 + 50, 350, 100, 50, GRAY, GREEN, lambda: change_theme("Winter"))

#         # Bird Skin Setting
#         bird_skin_text = font_option.render(f"Bird Skin: {selected_bird_skin}", True, WHITE)
#         bird_skin_rect = bird_skin_text.get_rect(center=(WIDTH // 2, 450))
#         screen.blit(bird_skin_text, bird_skin_rect)

#         draw_button(screen, "Default", WIDTH // 2 - 150, 500, 100, 50, GRAY, GREEN, lambda: change_bird_skin("Default"))
#         draw_button(screen, "Red", WIDTH // 2 - 50, 500, 100, 50, GRAY, GREEN, lambda: change_bird_skin("Red"))
#         draw_button(screen, "Blue", WIDTH // 2 + 50, 500, 100, 50, GRAY, GREEN, lambda: change_bird_skin("Blue"))

#         # Back Button (Repositioned slightly higher)
#         draw_button(screen, "Back", WIDTH // 2 - 50, HEIGHT - 150, 100, 50, GRAY, RED, lambda:())

#         pygame.display.flip()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()

# # Debug Back Button Function
# # def debug_back_button():                              
# #    print("Back button clicked!")  # Debugging output
# #    set_screen("start")  # Ensure this function switches back to the start screen

# # Updated draw_button Function
# def draw_button(screen, text, x, y, width, height, color, hover_color, action):
#     mouse = pygame.mouse.get_pos()
#     click = pygame.mouse.get_pressed()

#     # Check if mouse is over the button
#     if x + width > mouse[0] > x and y + height > mouse[1] > y:
#         pygame.dra

# # Helper functions for changing settings
# def change_difficulty(level):
#     global selected_difficulty
#     selected_difficulty = level

# def change_theme(theme):
#     global selected_theme
#     selected_theme = theme
#     apply_theme(theme)

# def change_bird_skin(skin):
#     global selected_bird_skin
#     selected_bird_skin = skin
#     apply_bird_skin(skin)

# def apply_theme(theme):
#     global background_image
#     if theme == "Day":
#         background_image = pygame.image.load("Img/bg.png")
#     elif theme == "Night":
#         background_image = pygame.image.load("Img/bg.png")
#     elif theme == "Winter":
#         background_image = pygame.image.load("Img/bg.png")

# def apply_bird_skin(skin):
#     global bird_image
#     if skin == "Default":
#         bird_image = pygame.image.load("Img/bird_blue (2).png")
#     elif skin == "Red":
#         bird_image = pygame.image.load("Img/birds11.png")
#     elif skin == "Blue":
#         bird_image = pygame.image.load("Img/bird_blue (1).png")


# Function to display the about us screen
def about_screen():
    screen.blit(background_image, (0, 0))

    # Box dimensions and position
    box_width, box_height = 750, 400
    box_x, box_y = (WIDTH - box_width) // 2, (HEIGHT - box_height) // 2

    # Draw the box
    pygame.draw.rect(screen, GRAY, (box_x, box_y, box_width, box_height), border_radius=15)
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 5, border_radius=15)  # Border

    # Draw the title
    font_title = pygame.font.Font(None, 50)
    title_text = font_title.render("Dev Note", True, BLACK)
    title_rect = title_text.get_rect(center=(box_x + box_width // 2, box_y + 40))
    screen.blit(title_text, title_rect)

    # Draw the developer's image (placeholder)
    image_size = 100
    dev_image = pygame.image.load("Img/OIP.jpeg")  # Replace with your developer image path
    dev_image = pygame.transform.scale(dev_image, (image_size, image_size))
    image_rect = dev_image.get_rect(center=(box_x + 100, box_y + 150))
    screen.blit(dev_image, image_rect)

    # Write a paragraph about the developer with dynamic wrapping
    font_text = pygame.font.Font(None, 30)
    paragraph = (
        "Hey there, "
        "I’m Tushar Albert Burney, the developer behind this project. "
        "This is my twist on the classic, with smooth mechanics and the familiar challenge we all love. "
        "I’m actively working on updates to enhance the experience—stay tuned for what’s next! "
        "If you like this project, follow me on GitHub for more updates: /SergentGhost. "
        "Thanks for playing, and keep flapping! 🐦"
    )

    text_x = box_x + 180  # Start text to the right of the image
    text_y = box_y + 100  # Start the paragraph below the title
    text_width = box_width - 200  # Allow margin for text
    render_text_wrapped(screen, paragraph, font_text, BLACK, text_x, text_y, text_width)

    # Add a Linktree button
    link_button_x = box_x + box_width // 2 - 100
    link_button_y = box_y + box_height - 60
    draw_button(
        screen,
        "More About Me",
        link_button_x,
        link_button_y,
        200,
        40,
        GRAY,
        GREEN,
        lambda: open_link("https://linktr.ee/TusharAlbertBurney")  # Replace with your Linktree URL
    )

    # Add a Back button
    back_button_x = 10
    back_button_y = 10
    draw_button(
        screen,
        "Back",
        back_button_x,
        back_button_y,
        100,
        50,
        GRAY,
        RED,
        lambda: set_screen("start")
    )
    pygame.display.flip()


# Helper function to open a link in the default web browser
def open_link(url):
    import webbrowser
    webbrowser.open(url)


# Helper function to render wrapped text
def render_text_wrapped(surface, text, font, color, x, y, max_width):
    """Render text within a specific width, wrapping lines if necessary."""
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)  # Add the last line

    line_spacing = 10
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y + i * (font.size(line)[1] + line_spacing)))


# Helper function to draw buttons
def draw_button(screen, text, x, y, width, height, color, hover_color, action):
    """Draw a button and handle click events."""
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)

    # Change color on hover
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
        if click[0]:  # Check if mouse is clicked
            action()
    else:
        pygame.draw.rect(screen, color, button_rect)

    # Draw button text
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

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
