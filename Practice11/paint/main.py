import pygame
import sys
from paint_logic import get_distance

pygame.init()

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Paint Practice")

# Initial background setup
BG_COLOR = (255, 255, 255) 
SCREEN.fill(BG_COLOR)

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Default state
current_color = BLACK
mode = 'rect' # Options: 'rect', 'circle', 'eraser'
start_pos = None
drawing = False

font = pygame.font.SysFont("Arial", 16)

def show_instructions():
    # Simple UI text for user instructions
    msg = "Modes: [R]ect, [C]ircle, [E]raser | Colors: [1]Red, [2]Green, [3]Blue, [4]Black"
    text_surf = font.render(msg, True, (100, 100, 100))
    # Clear top area for text
    pygame.draw.rect(SCREEN, (240, 240, 240), (0, 0, SCREEN_WIDTH, 30))
    SCREEN.blit(text_surf, (10, 5))

while True:
    show_instructions()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard event handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: mode = 'rect'
            elif event.key == pygame.K_c: mode = 'circle'
            elif event.key == pygame.K_e: mode = 'eraser'
            elif event.key == pygame.K_1: current_color = RED
            elif event.key == pygame.K_2: current_color = GREEN
            elif event.key == pygame.K_3: current_color = BLUE
            elif event.key == pygame.K_4: current_color = BLACK

        # Mouse event handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos # Store the point where user clicked

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                
                if mode == 'rect':
                    # Calculate width and height relative to start_pos
                    width = end_pos[0] - start_pos[0]
                    height = end_pos[1] - start_pos[1]
                    pygame.draw.rect(SCREEN, current_color, (start_pos[0], start_pos[1], width, height), 2)
                
                elif mode == 'circle':
                    # Radius is the distance between start and end of the drag
                    radius = int(get_distance(start_pos, end_pos))
                    pygame.draw.circle(SCREEN, current_color, start_pos, radius, 2)
                
                drawing = False

        if event.type == pygame.MOUSEMOTION:
            # Eraser works continuously while holding mouse button
            if drawing and mode == 'eraser':
                pygame.draw.circle(SCREEN, BG_COLOR, event.pos, 20)

    pygame.display.flip()