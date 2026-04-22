import pygame
from ball import Ball # Импортируем твой новый класс

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

# Создаем объект мяча
# Параметры: x, y, radius, color, screen_width, screen_height
my_ball = Ball(WIDTH // 2, HEIGHT // 2, 25, (255, 0, 0), WIDTH, HEIGHT)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка нажатий (Задание 3.3.2)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                my_ball.move(0, -20)
            if event.key == pygame.K_DOWN:
                my_ball.move(0, 20)
            if event.key == pygame.K_LEFT:
                my_ball.move(-20, 0)
            if event.key == pygame.K_RIGHT:
                my_ball.move(20, 0)

    screen.fill((255, 255, 255)) # Белый фон (Задание 3.3.1)
    
    my_ball.draw(screen) # Отрисовка через метод класса
    
    pygame.display.flip()
    clock.tick(60) # Контроль FPS для плавности

pygame.quit()