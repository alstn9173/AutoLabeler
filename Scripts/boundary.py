class Boundary:
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def set_coordinate(self, x, y):
        self.x = x
        self.y = y

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_coordinate(self):
        return [self.x, self.y]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height