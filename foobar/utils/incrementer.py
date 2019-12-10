class Incrementer:

    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x!r})'

    def compute(self):
        return self.x + 1
