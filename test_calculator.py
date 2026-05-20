import pytest
from calculator import add, subtract, multiply, divide, is_even


class TestCalculator:

    def test_add_positive(self):
        assert add(1, 2) == 3

    def test_add_negative(self):
        assert add(-1, -2) == -3

    def test_subtract(self):
        assert subtract(5, 3) == 2

    def test_multiply(self):
        assert multiply(4, 3) == 12

    def test_multiply_zero(self):
        assert multiply(100, 0) == 0

    def test_divide(self):
        assert divide(10, 2) == 5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_is_even_true(self):
        assert is_even(4) is True

    def test_is_even_false(self):
        assert is_even(5) is False

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ])
    def test_add_parametrize(self, a, b, expected):
        assert add(a, b) == expected
