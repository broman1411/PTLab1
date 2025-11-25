# -*- coding: utf-8 -*-
import argparse
import sys

from .CalcRating import CalcRating
from .TextDataReader import TextDataReader
from .JsonDataReader import JsonDataReader
from .DebtCalculation import DebtCalculation


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    path = get_path_from_arguments(sys.argv[1:])

    # Определяем тип reader на основе расширения файла
    if path.endswith('.json'):
        reader = JsonDataReader()
    else:
        reader = TextDataReader()

    students = reader.read(path)
    print("Students: ", students)

    # Расчет рейтинга
    rating = CalcRating(students).calc()
    print("Rating: ", rating)

    # Расчет задолженностей
    debt_calculator = DebtCalculation(students)
    debt_count = debt_calculator.count_students_with_debts()
    print(f"Количество студентов с академическими задолженностями: {debt_count}")


if __name__ == "__main__":
    main()