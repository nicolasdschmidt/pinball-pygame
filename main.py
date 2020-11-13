import pygame, pymunk, sys
from pygame.locals import *

from ball import Ball
from obstacle import Obstacle

# inicializar biblioteca PyGame
pygame.init()

# taxa de FPS do jogo
FPS = 60
clock = pygame.time.Clock()

# tamanho da tela
WIDTH = 400
HEIGHT = 600

# espaço físico pymunk
space = pymunk.Space()
space.gravity = (0, 500)

ball = Ball(space, (WIDTH/2, 0))

# limites físicos da tela
boundaries = []
boundaries.append(Obstacle(space, (WIDTH/2, 0), (WIDTH, 10)))       # norte
boundaries.append(Obstacle(space, (WIDTH/2, HEIGHT), (WIDTH, 10)))  # sul
boundaries.append(Obstacle(space, (WIDTH, HEIGHT/2), (10, HEIGHT))) # leste
boundaries.append(Obstacle(space, (0, HEIGHT/2), (10, HEIGHT)))     # oeste

# instanciar janela
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
SCREEN.fill((0,0,0))
pygame.display.set_caption("Pinball")

# loop principal
while True:
    # se o usuário clicar para sair, obedecer
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # preencher a tela com preto (para esconder o frame anterior)
    SCREEN.fill((0,0,0))

    ball.draw(SCREEN)

    for boundary in boundaries:
        boundary.draw(SCREEN)

    # atualizar espaço físico
    space.step(1/FPS)

    # atualizar tela e avançar o clock
    pygame.display.update()
    clock.tick(FPS)