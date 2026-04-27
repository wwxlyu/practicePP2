import pygame
import random

WIDTH = 400
HEIGHT = 400
BLOCK_SIZE = 20

class Snake:
    def __init__(self):
        self.body = [[200, 200], [180, 200], [160, 200]]
        self.direction = "RIGHT"
        self.score = 0

    def move(self):
        head = list(self.body[0])
        if self.direction == "RIGHT": head[0] += BLOCK_SIZE
        elif self.direction == "LEFT": head[0] -= BLOCK_SIZE
        elif self.direction == "UP": head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN": head[1] += BLOCK_SIZE
        self.body.insert(0, head)

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.spawn(snake_body)

    def spawn(self, snake_body):
        # Random weight (1 or 3)
        self.weight = random.choice([1, 1, 1, 3])
        self.color = (255, 105, 180) if self.weight == 1 else (255, 215, 0) # Pink or Gold
        
        # Timer for disappearing (5000 ms = 5 seconds)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000 
        
        while True:
            self.pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                        random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
            if self.pos not in snake_body:
                break

    def is_expired(self):
        # Check if 5 seconds have passed
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.lifetime