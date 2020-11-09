import pygame

def draw_line(screen, start, end):
    pygame.draw.line(screen, (255,255,255), start.int().tuple(), end.int().tuple())