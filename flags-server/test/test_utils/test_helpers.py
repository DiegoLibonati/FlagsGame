from src.utils.helpers import is_positive_integer


class TestIsPositiveInteger:
    def test_positive_integer_returns_true(self) -> None:
        assert is_positive_integer(1) is True
        assert is_positive_integer(100) is True
        assert is_positive_integer(999999) is True

    def test_zero_returns_false(self) -> None:
        assert is_positive_integer(0) is False

    def test_negative_integer_returns_false(self) -> None:
        assert is_positive_integer(-1) is False
        assert is_positive_integer(-100) is False

    def test_positive_string_number_returns_true(self) -> None:
        assert is_positive_integer("1") is True
        assert is_positive_integer("100") is True

    def test_zero_string_returns_false(self) -> None:
        assert is_positive_integer("0") is False

        assert is_positive_integer("abc") is False
        assert is_positive_integer("1.5") is False
        assert is_positive_integer("-1") is False

    def test_boolean_returns_false(self) -> None:
        assert is_positive_integer(True) is False
        assert is_positive_integer(False) is False

    def test_float_returns_false(self) -> None:
        assert is_positive_integer(1.0) is False
        assert is_positive_integer(1.5) is False

    def test_none_returns_false(self) -> None:
        assert is_positive_integer(None) is False

    def test_list_returns_false(self) -> None:
        assert is_positive_integer([1]) is False
        assert is_positive_integer([]) is False
