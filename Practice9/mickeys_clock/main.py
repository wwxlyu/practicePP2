import pygame
import os
from clock import ClockLogic

#Initialization
pygame.init()
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

base_path = os.path.dirname(__file__)
img_dir = os.path.join(base_path, "images")

#Load images
face_img = pygame.image.load(os.path.join(img_dir, "clock1.png")).convert_alpha()
face_rect = face_img.get_rect(center=(WIDTH//2, HEIGHT//2))
min_hand = pygame.image.load(os.path.join(img_dir, "minutes.png")).convert_alpha()
sec_hand = pygame.image.load(os.path.join(img_dir, "second.png")).convert_alpha()

def rotate_center(image, angle):
    """Helper to rotate image around center."""
    rotated_image = pygame.transform.rotate(image, -angle)
    new_rect = rotated_image.get_rect(center=(WIDTH//2, HEIGHT//2))
    return rotated_image, new_rect

clock_engine = ClockLogic()
clock_fps = pygame.time.Clock()

running = True 

while running:
    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update logic
    clock_engine.update_time()
    sec_angle, min_angle = clock_engine.calculate_angles()

    #Drawing
    screen.fill((255, 255, 255))
    screen.blit(face_img, face_rect)

    #Minutes
    rot_min, rect_min = rotate_center(min_hand, min_angle)
    screen.blit(rot_min, rect_min)

    #Seconds
    rot_sec, rect_sec = rotate_center(sec_hand, sec_angle)
    screen.blit(rot_sec, rect_sec)

    pygame.display.flip()
    clock_fps.tick(60)

pygame.quit()