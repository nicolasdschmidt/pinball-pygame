from draw import draw_line

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def draw(self, screen):
        draw_line(screen, self.start, self.end)