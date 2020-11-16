from pygame import constants
import pymunk
from pygame import gfxdraw

class Bumper:
    def __init__(self, space, position):
        self.body = pymunk.Body(1, body_type=pymunk.Body.STATIC)
        self.body.position = position[0], position[1]
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.elasticity = 2
        self.shape.collision_type = 1
        space.add(self.body, self.shape)

    def draw(self, screen):
        gfxdraw.filled_circle(screen, int(self.body.position.x), int(self.body.position.y), 10, (0,255,0))