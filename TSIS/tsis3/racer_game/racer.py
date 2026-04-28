import pygame
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Global speed variable we will increase in main
INITIAL_SPEED = 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, current_speed):
        self.rect.move_ip(0, current_speed)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[pygame.K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[pygame.K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spawn()

    def spawn(self):
        # Extra task: Randomly generating coins with different weights
        self.weight = random.choice([1, 1, 1, 3]) # 1 is common, 3 is rare
        
        # Change appearance based on weight
        size = 20 if self.weight == 1 else 30
        self.image = pygame.Surface((size, size))
        color = (255, 215, 0) if self.weight == 1 else (150, 0, 255) # Gold or Purple
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), random.randint(-100, -30))

    def move(self, current_speed):
        self.rect.move_ip(0, current_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()