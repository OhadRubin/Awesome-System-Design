import pytest

from foobar import Foo


@pytest.fixture
def foo():
    return Foo()


def test_run(foo):
    assert foo.run() == 'foo'


def test_inc(foo):
    assert foo.inc(1) == 2


def test_add(foo):
    assert foo.add(1, 2) == 3
