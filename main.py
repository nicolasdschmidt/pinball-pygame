import pygame, pymunk, sys, random
from pymunk import pygame_util
from pygame.locals import *

from ball import Ball
from obstacle import Obstacle
from flipper import Flipper
from bumper import Bumper

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

font_big = pygame.font.SysFont("monospace", 24, bold=True)
font_small = pygame.font.SysFont("monospace", 16, bold=True)

draw_options = pygame_util.DrawOptions(SCREEN)

score = 0
total_attempts = 5
attempts = total_attempts

game_running = True
pause_rendered = False

launch_ready = True
game_over = False

ACTIVE_COLOR = (0,255,0)
INACTIVE_COLOR = (0,100,0)

ACTIVE_TEXT = (0,255,255)
INACTIVE_TEXT = (0,100,100)

ACTIVE_SCORE = (255,255,255)
INACTIVE_SCORE = (100,100,100)

CUR_COLOR = ACTIVE_COLOR
CUR_TEXT = ACTIVE_TEXT
CUR_SCORE = ACTIVE_SCORE

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

ball = Ball(space, START_POS)

flipper_l = Flipper(space, (LAUNCHER_OFFSET/3, HEIGHT-40), (70,10), -1)
flipper_r = Flipper(space, (LAUNCHER_OFFSET/3*2, HEIGHT-40), (70,10), 1)

bumpers = []
bumpers.append(Bumper(space, (34, 40)))
bumpers.append(Bumper(space, (129, 155)))
bumpers.append(Bumper(space, (216, 151)))
bumpers.append(Bumper(space, (175, 187)))
bumpers.append(Bumper(space, (121, 303)))
bumpers.append(Bumper(space, (216, 390)))
bumpers.append(Bumper(space, (250, 267)))
bumpers.append(Bumper(space, (350, 60)))

# limites físicos da tela
boundaries = []
boundaries.append(Obstacle(space, (WIDTH/2, 0), (WIDTH, 10)))       # norte
boundaries.append(Obstacle(space, (LAUNCHER_OFFSET/4-100, HEIGHT), (LAUNCHER_OFFSET/2, 10)))  # sul
boundaries.append(Obstacle(space, (LAUNCHER_OFFSET/2+LAUNCHER_OFFSET/4+100, HEIGHT), (LAUNCHER_OFFSET/2, 10)))  # sul2
boundaries.append(Obstacle(space, (WIDTH, HEIGHT/2), (10, HEIGHT))) # leste
boundaries.append(Obstacle(space, (0, HEIGHT/2), (10, HEIGHT)))     # oeste
boundaries.append(Obstacle(space, (WIDTH-CORNER_OFFSET, CORNER_OFFSET), (WIDTH/2, 10), 45))   # nordeste
boundaries.append(Obstacle(space, (CORNER_OFFSET, CORNER_OFFSET), (WIDTH/2, 10), -45))   # noroeste
boundaries.append(Obstacle(space, (LAUNCHER_OFFSET, HEIGHT/2+50), (5, HEIGHT)))

# obstáculos
obstacles = []
obstacles.append(Obstacle(space, (LAUNCHER_OFFSET-60, HEIGHT-70), (WIDTH/6, 2), -40))
obstacles.append(Obstacle(space, (0+60, HEIGHT-70), (WIDTH/6, 2), 40))
obstacles.append(Obstacle(space, (LAUNCHER_OFFSET-60, HEIGHT-20), (WIDTH/3+20, 2), -40))
obstacles.append(Obstacle(space, (0+60, HEIGHT-20), (WIDTH/3+8, 2), 40))
obstacles.append(Obstacle(space, (LAUNCHER_OFFSET-70, HEIGHT-120), (WIDTH/6, 2), -70))
obstacles.append(Obstacle(space, (0+70, HEIGHT-120), (WIDTH/6, 2), 70))
obstacles.append(Obstacle(space, (LAUNCHER_OFFSET-70+(WIDTH/12+17), HEIGHT-330), (WIDTH/6, 2), -65))
obstacles.append(Obstacle(space, (0+70-(WIDTH/12+17), HEIGHT-330), (WIDTH/6, 2), 65))

obstacles.append(Obstacle(space, (LAUNCHER_OFFSET-60+(WIDTH/12-7), HEIGHT-125), (WIDTH/6, 2), 90))
obstacles.append(Obstacle(space, (0+60-(WIDTH/12-7), HEIGHT-125), (WIDTH/6, 2), 90))
obstacles.append(Obstacle(space, (LAUNCHER_OFFSET-60+(WIDTH/12-7), HEIGHT-250), (WIDTH/4, 2), 90))
obstacles.append(Obstacle(space, (0+60-(WIDTH/12-7), HEIGHT-250), (WIDTH/4, 2), 90))

obstacles.append(Obstacle(space, (333, 46), (WIDTH/6, 5), 10))
obstacles.append(Obstacle(space, (267, 43), (WIDTH/6, 5), -3))
obstacles.append(Obstacle(space, (107, 91), (WIDTH/6, 5), -70))
obstacles.append(Obstacle(space, (129, 91), (WIDTH/6, 5), 70))
obstacles.append(Obstacle(space, (), (WIDTH/9-2, 5), 0))

obstacles.append(Obstacle(space, (59, 205), (WIDTH/4, 5), 75))
obstacles.append(Obstacle(space, (50, 112), (WIDTH/4, 5), -85))
obstacles.append(Obstacle(space, (311, 217), (WIDTH/8, 5), -70))
obstacles.append(Obstacle(space, (322, 168), (WIDTH/8, 5), -85))
obstacles.append(Obstacle(space, (317, 120), (WIDTH/8, 5), 70))
obstacles.append(Obstacle(space, (289, 87), (WIDTH/8, 5), 30))
obstacles.append(Obstacle(space, (262, 75), (WIDTH/12, 5), 10))

#boundaries.append(Obstacle(space, (WIDTH/2+FLIPPER_OFFSET, HEIGHT/2+100), (5, HEIGHT/2)))

def decrease_attempt():
    global attempts, game_over
    attempts -= 1
    if attempts <= 0:
        game_over = True

def bumper_collision(space, arbiter, d1):
    global score
    score += 55
    return True

c_handler = space.add_collision_handler(1, 1)
c_handler.begin = bumper_collision

# loop principal
while True:
    if game_running:
        for event in pygame.event.get():
            # se o usuário clicar para sair, obedecer
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # input do teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_running = False
                    CUR_COLOR = INACTIVE_COLOR
                    CUR_TEXT = INACTIVE_TEXT
                    CUR_SCORE = INACTIVE_SCORE
                if event.key == pygame.K_f:
                    flipper_l.move()
                if event.key == pygame.K_j:
                    flipper_r.move()
                if event.key == pygame.K_SPACE and launch_ready:
                    if not game_over:
                        launch_ready = False
                        ball.launch(random.randint(900, 1400))
                    else:
                        score = 0
                        attempts = total_attempts
                        game_over = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        # preencher a tela com preto (para esconder o frame anterior)
        SCREEN.fill((0,0,0))

        ball.draw(SCREEN, CUR_COLOR)
        flipper_l.draw(SCREEN, CUR_COLOR)
        flipper_r.draw(SCREEN, CUR_COLOR)

        for bumper in bumpers:
            bumper.draw(SCREEN, CUR_COLOR)

        for boundary in boundaries:
            boundary.draw(SCREEN, CUR_COLOR)

        for obstacle in obstacles:
            obstacle.draw(SCREEN, CUR_COLOR)

        scoreText = font_big.render(str(score).zfill(5), 1, CUR_SCORE)
        if (attempts > 0):
            attemptsText = font_big.render((attempts) * '#' + (total_attempts - attempts) * '-', 1, CUR_TEXT)
        else:
            attemptsText = font_big.render('game over', 1, CUR_TEXT)
        score_rect = scoreText.get_rect(center=(int(WIDTH/2), 40))
        attempts_rect = attemptsText.get_rect(center=(int(WIDTH/2), 60))

        pauseText = font_small.render('<P> para pausa/sobre/ajuda', 1, CUR_SCORE)
        pause_rect = pauseText.get_rect(center=(int(WIDTH/2), HEIGHT - 10))

        SCREEN.blit(scoreText, score_rect)
        SCREEN.blit(attemptsText, attempts_rect)
        SCREEN.blit(pauseText, pause_rect)

        launch_ready = START_POS[0] - ball.radius < ball.body.position.x and ball.body.position.x < START_POS[0] + ball.radius and START_POS[1] - ball.radius/2 < ball.body.position.y and ball.body.position.y < START_POS[1] + ball.radius/2

        if (ball.body.position.y > HEIGHT or ball.body.position.y < 0):
            ball.recycle(START_POS)
            decrease_attempt()
            launch_ready = True

        # atualizar espaço físico
        space.step(1/FPS)
    else:
        for event in pygame.event.get():
            # se o usuário clicar para sair, obedecer
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # input do teclado
            if event.type == pygame.KEYDOWN:
                CUR_COLOR = ACTIVE_COLOR
                CUR_TEXT = ACTIVE_TEXT
                CUR_SCORE = ACTIVE_SCORE
                game_running = True
                pause_rendered = False

        if not pause_rendered and not game_running:
            pause_rendered = True

            pauseText = font_big.render('PAUSED', 1, (255,255,255))
            pause_rect = pauseText.get_rect(center=(int(WIDTH/2), 120))

            keyText = font_small.render('pressione qualquer tecla para retornar', 1, (255,255,255))
            key_rect = keyText.get_rect(center=(int(WIDTH/2), 140))

            spaceText = font_small.render('lançar bola: espaço', 1, (255,255,255))
            space_rect = spaceText.get_rect(center=(int(WIDTH/2), 220))

            flipperText = font_small.render('flippers: F e J', 1, (255,255,255))
            flipper_rect = flipperText.get_rect(center=(int(WIDTH/2), 240))

            aboutText = font_small.render('Pinball por:', 1, (255,255,255))
            about_rect = aboutText.get_rect(center=(int(WIDTH/2), 340))

            enzoText = font_small.render('Enzo Spinella (19168)', 1, (255,255,255))
            enzo_rect = enzoText.get_rect(center=(int(WIDTH/2), 380))

            nicolasText = font_small.render('Nícolas Schmidt (19191)', 1, (255,255,255))
            nicolas_rect = nicolasText.get_rect(center=(int(WIDTH/2), 420))

            SCREEN.blit(pauseText, pause_rect)
            SCREEN.blit(keyText, key_rect)
            SCREEN.blit(spaceText, space_rect)
            SCREEN.blit(flipperText, flipper_rect)
            SCREEN.blit(aboutText, about_rect)
            SCREEN.blit(enzoText, enzo_rect)
            SCREEN.blit(nicolasText, nicolas_rect)

    # atualizar tela e avançar o clock
    pygame.display.update()
    clock.tick(FPS)