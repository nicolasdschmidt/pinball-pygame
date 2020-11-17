import pymunk
from pymunk import Vec2d
from pygame import gfxdraw

class Flipper:
    def __init__(self, space, position, dimension, invert):
        self.width = dimension[0]
        self.height = dimension[1]
        self.invert = invert
        self.body = pymunk.Body(100, 200000)
        self.body.position = position[0], position[1]
        self.shape = pymunk.Poly.create_box(self.body, (self.width,self.height))
        space.add(self.body, self.shape)
        self.joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.joint_body.position = self.body.position
        j = pymunk.PinJoint(self.body, self.joint_body, (self.invert * 30, 0), (self.invert * 30, 0))
        s = pymunk.DampedRotarySpring(self.body, self.joint_body, 0.15, 20000000,900000)
        space.add(j, s)
        self.forceDelay = 0
        self.shape.group = 1
        self.shape.elasticity = 0#2.0

    def move(self):
        self.shape.elasticity = 1.4
        self.forceDelay = 20
        self.body.apply_impulse_at_local_point(Vec2d.unit() * -30000, (self.invert * -50,20))

    def draw(self, screen):
        if (self.forceDelay <= 0):
            self.shape.elasticity = 0
        else:
            self.forceDelay -= 1
        vertices = []
        for v in self.shape.get_vertices():
            x,y = v.rotated(self.shape.body.angle) + self.shape.body.position
            vertices.append((x,y))
        gfxdraw.aapolygon(screen, vertices, (0,255,0))
        gfxdraw.filled_polygon(screen, vertices, (0,255,0))
        #gfxdraw.filled_circle(screen, int(self.invert * -50 + self.body.position.x), int(20 + self.body.position.y), 5, (255,255,255))