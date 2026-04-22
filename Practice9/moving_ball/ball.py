import pygame

class Ball:
    def __init__(self, x, y, radius, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 20

    def draw(self, screen):
        # Рисуем мяч на указанном экране
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        # Проверяем границы перед тем, как изменить координаты (Задание 3.3.4)
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверка по горизонтали
        if self.radius <= new_x <= self.screen_width - self.radius:
            self.x = new_x
            
        # Проверка по вертикали
        if self.radius <= new_y <= self.screen_height - self.radius:
            self.y = new_y