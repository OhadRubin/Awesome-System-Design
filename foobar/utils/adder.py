class Adder:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x!r}, y={self.y!r})'

    def compute(self):
        return self.x + self.y
