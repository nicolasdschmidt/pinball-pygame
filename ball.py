import pymunk
from pygame import gfxdraw

class Ball:
    def __init__(self, space, position):
        self.space = space
        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = position
        self.radius = 10
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.6
        self.shape.collision_type = 1
        self.space.add(self.body,self.shape)

    def launch(self, impulse):
        self.body.apply_impulse_at_local_point((0,-impulse), (0,0))

    def recycle(self, position):
        #self.space.remove([self.body, self.shape])
        self.body.position = position
        self.body.velocity = (0, 0)

    def draw(self, screen, color):
        gfxdraw.aacircle(screen, int(self.body.position.x), int(self.body.position.y), self.radius, (color))
        gfxdraw.filled_circle(screen, int(self.body.position.x), int(self.body.position.y), self.radius, (color))