import pytest

from foobar import Bar


@pytest.fixture
def bar():
    return Bar()


def test_run(bar):
    assert bar.run() == 'bar'


def test_inc(bar):
    assert bar.inc(1) == 2


def test_add(bar):
    assert bar.add(1, 2) == 3
