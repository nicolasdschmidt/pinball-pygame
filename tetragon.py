from line import Line

class Tetragon:
    def __init__(self, c1, c2, c3, c4):
        self.corners = [c1, c2, c3, c4]
        self.lines = [Line(c1, c2), Line(c2, c3), Line(c3, c4), Line(c4, c1)]

    def draw(self):
        for line in self.lines:
            line.draw()