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
        self.level = 1

    def move(self):
        head = list(self.body[0])
        if self.direction == "RIGHT": head[0] += BLOCK_SIZE
        elif self.direction == "LEFT": head[0] -= BLOCK_SIZE
        elif self.direction == "UP": head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN": head[1] += BLOCK_SIZE
        
        self.body.insert(0, head)

    def check_collision(self):
        head = self.body[0]
        # Wall collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        # Self collision
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.pos = self.generate_random_pos(snake_body)

    def generate_random_pos(self, snake_body):
        while True:
            pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                   random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
            if pos not in snake_body:
                return pos