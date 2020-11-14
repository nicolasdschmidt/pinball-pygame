from flipper import Flipper
import pygame, pymunk, sys, random, math
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

CORNER_OFFSET = 20
WALL_SIZE = 10
BALL_RADIUS = 10
FLIPPER_OFFSET = 100

FLIPPER_L = 0

FLIPPER_MAX = 45

START_POS = (int(WIDTH - WALL_SIZE/2 - BALL_RADIUS), int(HEIGHT - WALL_SIZE/2 - BALL_RADIUS))

# espaço físico pymunk
space = pymunk.Space()
space.gravity = (0, 500)

ball = Ball(space, START_POS, random.randint(750, 1200))
#ball = Ball(space, (WIDTH/2.5, 0))


flipper_l = Flipper(space, (WIDTH/2, HEIGHT/2), (50,10), 0)

'''
r_flipper_body = pymunk.Body(1, 100)
r_flipper_body.position = 450, 100
r_flipper_shape = pymunk.Poly.create_box(r_flipper_body, (450, 100))
space.add(r_flipper_body, r_flipper_shape)

r_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
r_flipper_joint_body.position = r_flipper_body.position 
j = pymunk.PinJoint(r_flipper_body, r_flipper_joint_body, (0,0), (0,0))
#todo: tweak values of spring better
s = pymunk.DampedRotarySpring(r_flipper_body, r_flipper_joint_body, 0.15, 20000000,900000)
space.add(j, s)
'''

# limites físicos da tela
boundaries = []
boundaries.append(Obstacle(space, (WIDTH/2, 0), (WIDTH, 10)))       # norte
boundaries.append(Obstacle(space, (WIDTH/2, HEIGHT), (WIDTH, 10)))  # sul
boundaries.append(Obstacle(space, (WIDTH, HEIGHT/2), (10, HEIGHT))) # leste
boundaries.append(Obstacle(space, (0, HEIGHT/2), (10, HEIGHT)))     # oeste
boundaries.append(Obstacle(space, (WIDTH-CORNER_OFFSET, CORNER_OFFSET), (WIDTH/2, 10), 45))   # nordeste
boundaries.append(Obstacle(space, (CORNER_OFFSET, CORNER_OFFSET), (WIDTH/2, 10), -45))   # noroeste
boundaries.append(Obstacle(space, (WIDTH - WALL_SIZE/2 - BALL_RADIUS*2 - 10, HEIGHT/2+100), (5, HEIGHT)))
#boundaries.append(Obstacle(space, (WIDTH/2+FLIPPER_OFFSET, HEIGHT/2+100), (5, HEIGHT/2)))

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
    flipper_l.draw(SCREEN)

    for boundary in boundaries:
        boundary.draw(SCREEN)

    keys=pygame.key.get_pressed()

    if keys[K_z]:
        if FLIPPER_L < FLIPPER_MAX:
            FLIPPER_L += 10
    else:
        FLIPPER_L = 0
    flipper_l.body.angle = math.radians(FLIPPER_L)

    # atualizar espaço físico
    space.step(1/FPS)

    # atualizar tela e avançar o clock
    pygame.display.update()
    clock.tick(FPS)