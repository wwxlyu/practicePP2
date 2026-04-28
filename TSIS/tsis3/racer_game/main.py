import pygame, sys
from pygame.locals import *
from racer import Player, Enemy, Coin
import os
pygame.init()
pygame.mixer.init()



os.chdir(os.path.dirname(os.path.abspath(__file__)))
coin_sound = pygame.mixer.Sound("coin_sound.mp3")
crash_sound = pygame.mixer.Sound("crash_sound.mp3")

# pygame.mixer.music.load("background_music.mp3")
# pygame.mixer.music.play(-1) # -1 means play in a loop

FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer Practice 11")

font = pygame.font.SysFont("Verdana", 20)

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

COIN_SCORE = 0
CURRENT_SPEED = 5
N = 5 

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    SCREEN.fill((255, 255, 255))
    
    scores = font.render(f"Coins: {COIN_SCORE} Speed: {CURRENT_SPEED}", True, (0, 0, 0))
    SCREEN.blit(scores, (10, 10))

    for entity in all_sprites:
        SCREEN.blit(entity.image, entity.rect)
        if isinstance(entity, Player):
            entity.move()
        else:
            entity.move(CURRENT_SPEED)

    # Collision with enemy (Crash)
    if pygame.sprite.spritecollideany(P1, enemies):
        # Play crash sound
        crash_sound.play()
        
        # Give a small delay so the user can hear the sound before the window closes
        pygame.time.delay(1000)
        
        pygame.quit()
        sys.exit()

    # Collision with coins (Score)
    collided_coin = pygame.sprite.spritecollideany(P1, coins)
    if collided_coin:
        # Play coin sound
        coin_sound.play()
        
        COIN_SCORE += collided_coin.weight
        CURRENT_SPEED = 5 + (COIN_SCORE // N)
        collided_coin.spawn()

    pygame.display.update()
    FramePerSec.tick(FPS)