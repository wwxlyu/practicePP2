import pygame
import sys
from snakeee import Snake, Food, WIDTH, HEIGHT, BLOCK_SIZE

pygame.init()

BG_COLOR = (255, 245, 238)    # Cream
SNAKE_COLOR = (147, 197, 114) # Pastel Green
FOOD_COLOR = (255, 105, 180)  # Pink
TEXT_COLOR = (105, 105, 105)  # Gray

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

snake = Snake()
food = Food(snake.body)
speed = 8

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN and snake.direction != "UP":
                snake.direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction = "RIGHT"

    snake.move()

    # Check if food eaten
    if snake.body[0] == food.pos:
        snake.score += 1
        food = Food(snake.body)
        if snake.score % 3 == 0:
            snake.level += 1
            speed += 2
    else:
        snake.body.pop()

    if snake.check_collision():
        pygame.quit()
        sys.exit()

    SCREEN.fill(BG_COLOR)

    # Draw Food
    pygame.draw.rect(SCREEN, FOOD_COLOR, (food.pos[0], food.pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw Snake
    for block in snake.body:
        pygame.draw.rect(SCREEN, SNAKE_COLOR, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw Score and Level
    score_text = font.render(f"Score: {snake.score}  Level: {snake.level}", True, TEXT_COLOR)
    SCREEN.blit(score_text, (10, 10))

    pygame.display.flip()
    CLOCK.tick(speed)