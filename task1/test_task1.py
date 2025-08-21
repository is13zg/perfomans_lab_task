import pytest
from task1 import get_path


@pytest.mark.parametrize(
    "n, m, expected",
    [
        (6, 3, "135"),
        (5, 4, "14253"),
        (4, 2, "1234"),
        (6, 4, "14"),
        (1, 1, "1"),
        (7, 7, "1765432"),
        (10, 1, "1"),
        (20, 13, "1135179"),
        (3, 5, "123"),

    ]
)
def test_examples(n, m, expected):
    assert get_path(n, m) == expected
