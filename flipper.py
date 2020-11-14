import pymunk, math
from pygame import gfxdraw

class Flipper:
    def __init__(self, space, position, dimension, angle=0):
        self.body = pymunk.Body(1, body_type=pymunk.Body.KINEMATIC)
        self.width = dimension[0]
        self.height = dimension[1]
        self.body.position = position
        self.body.angle = math.radians(angle)
        self.body.center_of_gravity = (self.width/2.5, self.height/2)
        self.shape = pymunk.Poly.create_box(self.body, size=(self.width, self.height))
        space.add(self.body,self.shape)


    def draw(self, screen):
        vertices = []
        for v in self.shape.get_vertices():
            x,y = v.rotated(self.shape.body.angle) + self.shape.body.position
            vertices.append((x,y))
        gfxdraw.aapolygon(screen, vertices, (0,255,0))
        gfxdraw.filled_polygon(screen, vertices, (0,255,0))