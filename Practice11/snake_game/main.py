import pygame
import sys
import os
from snakeee import Snake, Food, WIDTH, HEIGHT, BLOCK_SIZE

pygame.init()
pygame.mixer.init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

eat_sound = pygame.mixer.Sound("eat_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")

BG_COLOR = (255, 245, 238)
SNAKE_COLOR = (147, 197, 114)
TEXT_COLOR = (105, 105, 105)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11")
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

snake = Snake()
food = Food(snake.body)
speed = 10

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

    # Check if food expired (timer)
    if food.is_expired():
        food.spawn(snake.body)

    # Check if food eaten
    if snake.body[0] == food.pos:
        # Play eat sound
        eat_sound.play()
        
        snake.score += food.weight
        speed = 10 + (snake.score // 2)
        food.spawn(snake.body)
    else:
        snake.body.pop()

    # Collision check
    if snake.check_collision():
        # Play game over sound
        game_over_sound.play()
        
        # Delay to hear the sound
        pygame.time.delay(1000)
        
        pygame.quit()
        sys.exit()

    SCREEN.fill(BG_COLOR)

    #Food
    pygame.draw.rect(SCREEN, food.color, (food.pos[0], food.pos[1], BLOCK_SIZE, BLOCK_SIZE))

    #Snake
    for block in snake.body:
        pygame.draw.rect(SCREEN, SNAKE_COLOR, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

    #Score
    score_text = font.render(f"Score: {snake.score}  Speed: {speed}", True, TEXT_COLOR)
    SCREEN.blit(score_text, (10, 10))

    pygame.display.flip()
    CLOCK.tick(speed)