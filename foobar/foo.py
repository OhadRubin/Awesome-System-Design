from .utils import Adder, Incrementer


class Foo:

    def run(self):
        return 'foo'

    def inc(self, x):
        incrementer = Incrementer(x)
        return incrementer.compute()

    def add(self, x, y):
        adder = Adder(x, y)
        return adder.compute()
