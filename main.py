import pygame, sys
from pygame.locals import *
from pygame import gfxdraw

from vector import Vector
from line import Line

# inicializar biblioteca PyGame
pygame.init()

# taxa de FPS do jogo
FPS = 60
clock = pygame.time.Clock()

# tamanho da tela
WIDTH = 400
HEIGHT = 600

p1 = Vector(10, 20)
p2 = Vector(90, 70)
line = Line(p1, p2)

# instanciar janela
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
SCREEN.fill((0,0,0))
pygame.display.set_caption("Pinball")

# função para desenhar um círculo com anti-aliasing, uma técnica para reduzir
# aquelas bordas "pixeladas" de figuras arredondads adicionando mais detalhe
def draw_circle(surface, color, x, y, radius):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

# loop principal
while True:
    # se o usuário clicar para sair, obedecer
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # preencher a tela com preto (para esconder o frame anterior)
    SCREEN.fill((0,0,0))
    
    line.draw(SCREEN)

    # atualizar tela e avançar o clock
    pygame.display.update()
    clock.tick(FPS)