import pygame, sys
import os
from paint_logic import get_distance, get_equilateral_triangle, get_rhombus

pygame.init()
# Fixing paths for assets if needed
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SCREEN = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Paint Practice 11")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN.fill(WHITE)

# Drawing states
current_color = BLACK
mode = 'rect' 
start_pos = None
drawing = False

font = pygame.font.SysFont("Arial", 14, bold=True)

while True:
    # UPDATED MENU STRING
    msg = "Modes: [R]ect, [S]quare, [C]ircle, [T]riangle, [U]Equi, [H]Rhombus, [E]raser | Colors: [1]Red, [2]Green, [3]Blue, [4]Black"
    text_surf = font.render(msg, True, (50, 50, 50))
    pygame.draw.rect(SCREEN, (230, 230, 230), (0, 0, 900, 35))
    SCREEN.blit(text_surf, (10, 8))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Mode selection
            if event.key == pygame.K_r: mode = 'rect'
            elif event.key == pygame.K_s: mode = 'square'
            elif event.key == pygame.K_c: mode = 'circle'
            elif event.key == pygame.K_t: mode = 'right_triangle'
            elif event.key == pygame.K_u: mode = 'equilateral_triangle'
            elif event.key == pygame.K_h: mode = 'rhombus'
            elif event.key == pygame.K_e: mode = 'eraser'
            # Color selection
            elif event.key == pygame.K_1: current_color = RED
            elif event.key == pygame.K_2: current_color = GREEN
            elif event.key == pygame.K_3: current_color = BLUE
            elif event.key == pygame.K_4: current_color = BLACK

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                
                if mode == 'rect':
                    width = end_pos[0] - start_pos[0]
                    height = end_pos[1] - start_pos[1]
                    pygame.draw.rect(SCREEN, current_color, (start_pos[0], start_pos[1], width, height), 2)
                
                elif mode == 'square':
                    side = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(SCREEN, current_color, (start_pos[0], start_pos[1], side, side), 2)

                elif mode == 'circle':
                    radius = int(get_distance(start_pos, end_pos))
                    pygame.draw.circle(SCREEN, current_color, start_pos, radius, 2)

                elif mode == 'right_triangle':
                    points = [start_pos, end_pos, (start_pos[0], end_pos[1])]
                    pygame.draw.polygon(SCREEN, current_color, points, 2)

                elif mode == 'equilateral_triangle':
                    points = get_equilateral_triangle(start_pos, end_pos)
                    pygame.draw.polygon(SCREEN, current_color, points, 2)

                elif mode == 'rhombus':
                    points = get_rhombus(start_pos, end_pos)
                    pygame.draw.polygon(SCREEN, current_color, points, 2)
                
                drawing = False

        if event.type == pygame.MOUSEMOTION:
            if drawing and mode == 'eraser':
                # Eraser just draws white circles
                pygame.draw.circle(SCREEN, WHITE, event.pos, 20)

    pygame.display.flip()