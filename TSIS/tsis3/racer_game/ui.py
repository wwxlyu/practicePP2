import pygame

# Color palette
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
DARK_BLUE = (10, 10, 30)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
GRAY = (100, 100, 100)

class Button:
    def __init__(self, text, x, y, w, h, color, action_id):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.action_id = action_id

    def draw(self, screen, font):
        # Draw button background
        pygame.draw.rect(screen, DARK_BLUE, self.rect, 0, border_radius=8)
        pygame.draw.rect(screen, self.color, self.rect, 3, border_radius=8)
        
        # Draw text
        text_surf = font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_gradient_background(screen):
    for y in range(600):
        # Dark blue to purple gradient
        r = 10 + y // 30
        g = 10 + y // 40
        b = 30 + y // 20
        if b > 150:
            b = 150
        pygame.draw.line(screen, (r, g, b), (0, y), (400, y))