import argparse
import sys
from typing import TextIO, List
import statistics


MOVE_LIMIT = 20


def read_nums_file(f: TextIO) -> List[int]:
    result = []
    try:
        for num, line in enumerate(f):
            s = line.strip()
            if not s:
                continue
            result.append(int(s))
    except ValueError:
        raise ValueError(f"Файл должен состоять из целых чисел. На строке с номером {num + 1} прочитано: {line}")
    if not result:
        raise ValueError(f"Файл не содержит целых чисел")
    return result


def count_moves(nums: List[int]) -> int | None:
    median = statistics.median_low(nums)
    result = 0
    for x in nums:
        result += abs(x - median)
        if result > MOVE_LIMIT:
            return None

    return result


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Расчет минимального количества ходов, требуемых для приведения всех элементов массива к одному числу",
        epilog=(
            "Пример запуска:\n"
            "  python task4.py путь/до/файла_с_элементами_массива \n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("file", type=argparse.FileType("r", encoding="utf-8"),
                        help="Файл с элементами массива")

    return parser.parse_args()


def main():
    try:
        args = parse_arguments()

        with args.file as file:
            nums = read_nums_file(file)

        res = count_moves(nums)
        if res is not None:
            print(res)
        else:
            print(f"{MOVE_LIMIT} ходов недостаточно для приведения всех элементов массива к одному числу")

    except Exception as e:
        print(f"Ошибка выполнения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
