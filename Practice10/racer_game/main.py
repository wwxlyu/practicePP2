import pygame, sys
from pygame.locals import *
from racer import Player, Enemy, Coin

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer")

font = pygame.font.SysFont("Verdana", 20)

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

COIN_SCORE = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    SCREEN.fill((255, 255, 255))
    
    # Render and display the coin counter
    scores = font.render(f"Coins: {COIN_SCORE}", True, (0, 0, 0))
    SCREEN.blit(scores, (300, 10))

    for entity in all_sprites:
        SCREEN.blit(entity.image, entity.rect)
        entity.move()

    # Collision detection with the enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.quit()
        sys.exit()

    # Collision detection with coins
    collided_coin = pygame.sprite.spritecollideany(P1, coins)
    if collided_coin:
        COIN_SCORE += 1
        collided_coin.spawn()

    pygame.display.update()
    FramePerSec.tick(FPS)