import json
import argparse
import sys
import os
from typing import Any


def validate_file_path(path: str) -> str:
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        return path
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Ошибка создания пути: {e}")


def set_value(test: dict[str, Any], res: dict[str, Any]) -> list:
    current_id = None if test.get("id") is None else str(test.get("id"))
    if current_id in res:
        test['value'] = res.get(current_id)

    for x in test.get("values", []):
        set_value(x, res)

    for x in test.get("tests", []):
        set_value(x, res)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Создание файла report.json с заполненными полями value для структуры tests.json на основании values.json",
        epilog=(
            "Пример запуска:\n"
            "  python task3.py values.json tests.json report.json \n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("values_file", type=argparse.FileType("r", encoding="utf-8"),
                        help="Файл содержит результаты прохождения тестов с уникальными id")
    parser.add_argument("tests_file", type=argparse.FileType("r", encoding="utf-8"),
                        help="Файл содержит структуру для построения отчета на основе прошедших тестов")
    parser.add_argument("report_file", type=validate_file_path,
                        help="В этот файл записывается результат")

    return parser.parse_args()


def main():
    try:
        args = parse_arguments()

        try:
            with args.values_file as values_file:
                values_data = json.load(values_file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON в values_file: {e}")

        values_dict = {str(x['id']): x['value'] for x in values_data["values"]}
        try:
            with args.tests_file as tests_file:
                tests_data = json.load(tests_file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON в tests_file: {e}")

        set_value(tests_data, values_dict)

        with open(args.report_file, "w", encoding="utf-8") as report_file:
            json.dump(tests_data, report_file, ensure_ascii=False, indent=2)


    except Exception as e:
        print(f"Ошибка выполнения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
