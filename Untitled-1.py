import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Save the Ball Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Ball setup
ball_radius = 20
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_velocity = 4
ball_direction = [random.choice([-1, 1]), random.choice([-1, 1])]

# Player (paddle) setup
paddle_width, paddle_height = 100, 10
paddle_x = SCREEN_WIDTH // 2 - paddle_width // 2
paddle_y = SCREEN_HEIGHT - 50
paddle_speed = 8

# Spikes setup
spike_width, spike_height = 20, 40
spikes = []
for i in range(0, SCREEN_WIDTH, spike_width):
    spikes.append(pygame.Rect(i, SCREEN_HEIGHT - spike_height, spike_width, spike_height))

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game states
game_over = False

def draw_ball():
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)

def draw_paddle():
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))

def draw_spikes():
    for spike in spikes:
        pygame.draw.polygon(screen, RED, [(spike.x, spike.y), (spike.x + spike_width, spike.y), (spike.x + spike_width // 2, spike.y - spike_height)])

def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def show_game_over():
    over_text = font.render("GAME OVER! Tap R to Restart", True, RED)
    screen.blit(over_text, (SCREEN_WIDTH // 10, SCREEN_HEIGHT // 2))

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Restart the game
                ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                ball_direction = [random.choice([-1, 1]), random.choice([-1, 1])]
                score = 0
                game_over = False

    if not game_over:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - paddle_width:
            paddle_x += paddle_speed

        # Ball movement
        ball_x += ball_velocity * ball_direction[0]
        ball_y += ball_velocity * ball_direction[1]

        # Ball collision with walls
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= SCREEN_WIDTH:
            ball_direction[0] *= -1
        if ball_y - ball_radius <= 0:
            ball_direction[1] *= -1

        # Ball collision with paddle
        if (paddle_x <= ball_x <= paddle_x + paddle_width) and (paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height):
            ball_direction[1] *= -1
            score += 1

        # Ball collision with spikes
        for spike in spikes:
            if spike.collidepoint(ball_x, ball_y + ball_radius):
                game_over = True

        # Draw elements
        draw_ball()
        draw_paddle()
        draw_spikes()
        show_score()
    else:
        show_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
