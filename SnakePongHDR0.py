import pygame
import random
from array import array

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Set screen dimensions
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SnakePong with Sound")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Snake properties
snake_block_size = 10
snake_speed = 15

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font for displaying score
font_style = pygame.font.SysFont(None, 25)

def display_score(score):
    """Renders the score on the screen."""
    value = font_style.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

def draw_snake(snake_block_size, snake_list):
    """Draws the snake on the screen."""
    for x, y in snake_list:
        pygame.draw.rect(screen, white, [x, y, snake_block_size, snake_block_size])

def generate_beep_sound(frequency=440, duration=0.1):
    """Generates a beep sound with varying frequencies."""
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

def game_loop():
    """Main game loop."""
    game_over = False
    game_close = False

    # Initial snake position
    x1 = screen_width / 2
    y1 = screen_height / 2
    x1_change = 0
    y1_change = 0

    # Snake properties
    snake_list = []
    snake_length = 1

    # Ball properties
    ball_x = random.randrange(0, screen_width - snake_block_size, 10)
    ball_y = 0
    ball_speed = 5

    # Sound properties
    catch_sound = generate_beep_sound(440, 0.1)
    game_over_sound = generate_beep_sound(220, 0.5)

    while not game_over:
        while game_close:
            # Display game over message and options
            screen.fill(black)
            message = font_style.render("You Lost! Press Q-Quit or C-Play Again", True, white)
            screen.blit(message, [screen_width / 6, screen_height / 3])
            display_score(snake_length - 1)
            pygame.display.update()

            # Event handling for game over options
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Event handling for snake movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block_size
                    y1_change = 0

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for collision with walls
        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_over_sound.play()
            game_close = True

        # Update ball position
        ball_y += ball_speed

        # Check for collision with snake
        for x, y in snake_list:
            if x == ball_x and y == ball_y:
                catch_sound.play()
                snake_length += 1
                ball_x = random.randrange(0, screen_width - snake_block_size, 10)
                ball_y = 0

        # Check if ball goes out of bounds
        if ball_y >= screen_height:
            game_over_sound.play()
            game_close = True

        # Draw game objects
        screen.fill(black)
        pygame.draw.rect(screen, white, [ball_x, ball_y, snake_block_size, snake_block_size])
        draw_snake(snake_block_size, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
