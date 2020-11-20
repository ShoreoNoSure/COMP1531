from divisors import divisors
from hypothesis import given, strategies
import pytest

def test_12():
    assert divisors(12) == {1,2,3,4,6,12}

def test_negative():
    with pytest.raises(ValueError):
        divisors(-3)

def test_0():
    assert divisors(0) == {0}

def test_1():
    assert divisors(1) == {1}

def test_2():
    assert divisors(2) == {1,2}

def test_30():
    assert divisors(30) == {1,2,3,5,6,10,15,30}
