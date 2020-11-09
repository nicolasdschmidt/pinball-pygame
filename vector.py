class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def int(self):
        return Vector(int(self.x), int(self.y))

    def tuple(self):
        return self.x, self.y