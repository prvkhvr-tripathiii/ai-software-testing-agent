# Generated test: test_add
# Target function: add

from calculator import add

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


# Generated test: test_divide_success
# Target function: divide

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

from calculator import multiply

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0


# Generated test: test_subtract
# Target function: subtract

from calculator import subtract

def test_subtract():
    assert subtract(5, 2) == 3
    assert subtract(0, 5) == -5
    assert subtract(-2, -3) == 1
