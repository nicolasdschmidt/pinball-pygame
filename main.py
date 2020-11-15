import pygame, pymunk, sys, random
from pymunk import pygame_util
from pygame.locals import *

from ball import Ball
from obstacle import Obstacle
from flipper import Flipper

# inicializar biblioteca PyGame
pygame.init()

# taxa de FPS do jogo
FPS = 60
clock = pygame.time.Clock()

# tamanho da tela
WIDTH = 400
HEIGHT = 600

# instanciar janela
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
SCREEN.fill((0,0,0))
pygame.display.set_caption("Pinball")

draw_options = pygame_util.DrawOptions(SCREEN)

CORNER_OFFSET = 20
WALL_SIZE = 10
BALL_RADIUS = 10
FLIPPER_OFFSET = 100

FLIPPER_L = 0

FLIPPER_MAX = 45

START_POS = (int(WIDTH - WALL_SIZE/2 - BALL_RADIUS), int(HEIGHT - WALL_SIZE/2 - BALL_RADIUS))
LAUNCHER_OFFSET = WIDTH - WALL_SIZE/2 - BALL_RADIUS*2 - 10

# espaço físico pymunk
space = pymunk.Space()
space.gravity = (0, 500)

ball = Ball(space, START_POS, random.randint(750, 1200))

flipper_l = Flipper(space, (LAUNCHER_OFFSET/3, HEIGHT*3/4), (70,10), -1)
flipper_r = Flipper(space, (LAUNCHER_OFFSET/3*2, HEIGHT*3/4), (70,10), 1)

# limites físicos da tela
boundaries = []
boundaries.append(Obstacle(space, (WIDTH/2, 0), (WIDTH, 10)))       # norte
boundaries.append(Obstacle(space, (WIDTH/2, HEIGHT), (WIDTH, 10)))  # sul
boundaries.append(Obstacle(space, (WIDTH, HEIGHT/2), (10, HEIGHT))) # leste
boundaries.append(Obstacle(space, (0, HEIGHT/2), (10, HEIGHT)))     # oeste
boundaries.append(Obstacle(space, (WIDTH-CORNER_OFFSET, CORNER_OFFSET), (WIDTH/2, 10), 45))   # nordeste
boundaries.append(Obstacle(space, (CORNER_OFFSET, CORNER_OFFSET), (WIDTH/2, 10), -45))   # noroeste
boundaries.append(Obstacle(space, (LAUNCHER_OFFSET, HEIGHT/2+100), (5, HEIGHT)))
#boundaries.append(Obstacle(space, (WIDTH/2+FLIPPER_OFFSET, HEIGHT/2+100), (5, HEIGHT/2)))

# loop principal
while True:
    for event in pygame.event.get():
        # se o usuário clicar para sair, obedecer
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # input do teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                flipper_l.move()
            if event.key == pygame.K_j:
                flipper_r.move()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

    # preencher a tela com preto (para esconder o frame anterior)
    SCREEN.fill((0,0,0))

    ball.draw(SCREEN)
    flipper_l.draw(SCREEN)
    flipper_r.draw(SCREEN)

    for boundary in boundaries:
        boundary.draw(SCREEN)

    #space.debug_draw(draw_options)

    # atualizar espaço físico
    space.step(1/FPS)

    # atualizar tela e avançar o clock
    pygame.display.update()
    clock.tick(FPS)