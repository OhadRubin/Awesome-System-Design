import pytest

from foobar.utils import Adder


@pytest.fixture
def a():
    return Adder(1, 2)


def test_attributes(a):
    assert a.x == 1
    assert a.y == 2


def test_repr(a):
    assert repr(a) == 'Adder(x=1, y=2)'


def test_compute(a):
    assert a.compute() == 3
