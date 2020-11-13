import pymunk
from pygame import gfxdraw

class Ball:
    def __init__(self, space, position):
        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = position
        self.radius = 10
        self.shape = pymunk.Circle(self.body, self.radius)
        space.add(self.body,self.shape)

    def draw(self, screen):
        gfxdraw.aacircle(screen, int(self.body.position.x), int(self.body.position.y), self.radius, (0,255,0))
        gfxdraw.filled_circle(screen, int(self.body.position.x), int(self.body.position.y), self.radius, (0,255,0))