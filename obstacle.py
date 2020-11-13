import pymunk
from pygame import gfxdraw, Rect

class Obstacle:
    def __init__(self, space, position, dimension):
        self.body = pymunk.Body(1, body_type=pymunk.Body.STATIC)
        self.width = dimension[0]
        self.height = dimension[1]
        self.body.position = position
        self.shape = pymunk.Poly.create_box(self.body, size=(self.width, self.height))
        space.add(self.body,self.shape)

    def draw(self, screen):
        gfxdraw.box(screen, Rect(self.body.position.x - self.width/2, self.body.position.y - self.height/2, self.width, self.height), (0,255,0))