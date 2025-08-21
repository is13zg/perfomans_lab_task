from math import gcd
import argparse
import sys


def positive_int(value: str) -> int:
    try:
        result = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} не является числом")

    if result < 1:
        raise argparse.ArgumentTypeError(f"Значение должно быть ≥ 1, получено {result}")
    return result


def get_path(n: int, m: int) -> str:
    steps = n // gcd(n, m - 1)
    return "".join(str(i * (m - 1) % n + 1) for i in range(steps))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Вывод пути по круговым массивам [1..n] при обходе интервалами m", epilog=(
            "Примеры:\n"
            "  python task1.py 6 3 5 4   -> 13514253\n"
            "  python task2.py 4 2 6 4   -> 123414\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("n1", type=positive_int, help="Размер 1-го массива (n1 ≥ 1)")
    parser.add_argument("m1", type=positive_int, help="Длина интервала 1-го массива (m1 ≥ 1)")
    parser.add_argument("n2", type=positive_int, help="Размер 2-го массива (n2 ≥ 1)")
    parser.add_argument("m2", type=positive_int, help="Длина интервала 2-го массива (m2 ≥ 1)")

    return parser.parse_args()


def main():
    try:
        args = parse_arguments()
        out = get_path(args.n1, args.m1) + get_path(args.n2, args.m2)
        print(out)
    except Exception as e:
        print(f"Ошибка выполнения : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
