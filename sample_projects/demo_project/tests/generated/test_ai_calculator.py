# Generated test: test_add
# Target function: add

import pytest
from calculator import add

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0.5, 0.5) == 1.0


# Generated test: test_divide_success
# Target function: divide

import pytest
from calculator import divide

def test_divide_success():
    assert divide(6, 3) == 2.0
    assert divide(-6, 2) == -3.0


# Generated test: test_divide_by_zero
# Target function: divide

import pytest
from calculator import divide

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)


# Generated test: test_multiply
# Target function: multiply

import pytest
from calculator import multiply

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0


# Generated test: test_subtract
# Target function: subtract

import pytest
from calculator import subtract

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    assert subtract(0, 0) == 0
