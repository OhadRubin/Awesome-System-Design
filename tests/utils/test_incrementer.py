import pytest

from foobar.utils import Incrementer


@pytest.fixture
def i():
    return Incrementer(1)


def test_attributes(i):
    assert i.x == 1


def test_repr(i):
    assert repr(i) == 'Incrementer(x=1)'


def test_compute(i):
    assert i.compute() == 2
