import io
from decimal import Decimal
import pytest
from task2 import Ellipse, read_ellipse_params, read_points, EPS


@pytest.mark.parametrize(
    "text, expected, expect_error",
    [
        ("0 0\n5 3\n", (Decimal("0"), Decimal("0"), Decimal("5"), Decimal("3")), False),
        ("1 -1 – координаты центра\n1 3 – координаты радиуса  \n",
         (Decimal("1"), Decimal("-1"), Decimal("1"), Decimal("3")), False),
        ("1 2\n-3 5\n", None, True),
    ],
)
def test_read_ellipse_params(text, expected, expect_error):
    f = io.StringIO(text)
    if expect_error:
        with pytest.raises(ValueError):
            read_ellipse_params(f)
    else:
        e = read_ellipse_params(f)
        assert (e.x0, e.y0, e.a, e.b) == expected


def test_read_points():
    f = io.StringIO("\n0 3\n  \n0 0\n6 0   \n")
    pts = read_points(f)
    assert pts == [
        (Decimal("0"), Decimal("3")),
        (Decimal("0"), Decimal("0")),
        (Decimal("6"), Decimal("0")),
    ]


@pytest.mark.parametrize(
    "ellipse_params, point, expected",
    [

        ({"a": Decimal("5"), "b": Decimal("3"), "x0": Decimal("0"), "y0": Decimal("0")},
         (Decimal("0"), Decimal("3")), 0),
        ({"a": Decimal("5"), "b": Decimal("3"), "x0": Decimal("0"), "y0": Decimal("0")},
         (Decimal("0"), Decimal("0")), 1),
        ({"a": Decimal("5"), "b": Decimal("3"), "x0": Decimal("0"), "y0": Decimal("0")},
         (Decimal("6"), Decimal("0")), 2),
        ({"a": Decimal("5"), "b": Decimal("3"), "x0": Decimal("0"), "y0": Decimal("0")},
         (Decimal("0"), Decimal("3") + (EPS / Decimal("10"))), 0)
    ])
def test_check_dot_parametrized(ellipse_params, point, expected):
    e = Ellipse(**ellipse_params)
    assert e.check_dot(*point) == expected
