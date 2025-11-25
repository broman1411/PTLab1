# -*- coding: utf-8 -*-
import argparse
import sys
import os
from src.TextDataReader import TextDataReader
from src.JsonDataReader import JsonDataReader
from src.DebtCalculation import DebtCalculation

# Добавляем путь к src в sys.path для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


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

    # Расчет задолженностей
    debt_calculator = DebtCalculation(students)
    debt_count = debt_calculator.count_students_with_debts()
    print(f"Количество студентов с академическими "
          f"задолженностями: {debt_count}")


if __name__ == "__main__":
    main()
