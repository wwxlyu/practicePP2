import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((35, 60))
        self.image.fill(color)
        # Add white stripe
        pygame.draw.rect(self.image, (255, 255, 255), (12, 0, 10, 60))
        self.rect = self.image.get_rect(center=(200, 500))
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 50:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < 350:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((35, 60))
        self.image.fill((255, 50, 80))  # Red color
        pygame.draw.rect(self.image, (150, 0, 0), (0, 0, 35, 60), 2)  # Border
        self.rect = self.image.get_rect(midtop=(random.randint(60, 340), -60))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed