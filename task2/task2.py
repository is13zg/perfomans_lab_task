import argparse
import sys
from typing import TextIO, Tuple, List
from dataclasses import dataclass
from decimal import Decimal, getcontext

getcontext().prec = 80
EPS = Decimal('1e-25')


@dataclass
class Ellipse:
    a: Decimal
    b: Decimal
    x0: Decimal
    y0: Decimal

    def check_dot(self, x: Decimal, y: Decimal) -> int:
        calc = (x - self.x0) ** 2 / self.a ** 2 + (y - self.y0) ** 2 / self.b ** 2

        if (calc - Decimal(1)).copy_abs() <= EPS:
            return 0
        elif calc > Decimal(1):
            return 2
        else:
            return 1

    def __str__(self):
        return f"{self.a=},{ self.b=},{  self.x0=},{ self.y0=} "


def read_ellipse_params(f: TextIO) -> Ellipse:
    x, y = map(Decimal, f.readline().strip().split()[:2])
    a, b = map(Decimal, f.readline().strip().split()[:2])
    if a <= 0 or b <= 0:
        raise ValueError(f"Радиусы эллипса должны быть положительными, прочитано {a=} {b=}")
    return Ellipse(a, b, x, y)


def read_points(f: TextIO) -> List[Tuple[Decimal, Decimal]]:
    result = []
    for line in f:
        s = line.strip()
        if not s:
            continue
        x, y = map(Decimal, s.split())
        result.append((x, y))
    return result


def check_pos(ellipse: Ellipse, dots: List[Tuple[Decimal, Decimal]]) -> List[int]:
    return [ellipse.check_dot(x, y) for x, y in dots]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Расчет положения точек относительно эллипса", epilog=(
            "Пример запуска:\n"
            "  python task2.py путь/до/файла_с_параметрами_эллипса  путь/до/файла_с_точками \n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("file1", type=argparse.FileType("r", encoding="utf-8"),
                        help="Файл с координатами и радиусом эллипса")
    parser.add_argument("file2", type=argparse.FileType("r", encoding="utf-8"), help="Файл с координатами точек")

    return parser.parse_args()


def main():
    try:
        args = parse_arguments()

        with args.file1 as f1:
            ellipse = read_ellipse_params(f1)

        with args.file2 as f2:
            dots = read_points(f2)

        results = check_pos(ellipse, dots)
        print("\n".join(map(str, results)) + "\n")

    except Exception as e:
        print(f"Ошибка выполнения : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
