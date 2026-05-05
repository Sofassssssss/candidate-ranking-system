import os
from typing import Dict, Tuple
from ..utils.csv_reader import read_data_from_csv

CANDIDATES_FILE = 'candidates'


def get_data_file_number() -> int | None:
    print(
        "Введите номер файла с данными о кандидатах\n"
        "(доступные файлы можно посмотреть в папке data/).\n"
        "Для выхода просто нажмите Enter!")

    while True:
        user_input = input().strip()

        if user_input == "":
            print("Выход из программы.")
            return None

        if not user_input.isdigit():
            print("Ошибка: пожалуйста, введите целое число.")
            continue

        file_number = int(user_input)
        file_path = f'data/{CANDIDATES_FILE}{file_number}.csv'

        if not os.path.isfile(file_path):
            print(f"Файл '{file_path}' не найден. Введите существующий номер.")
            continue

        return file_number


def get_data_from_user_input() -> Dict[str, Tuple[int, ...]] | None:
    print("Эта программа предназначена для получения ранжированного списка кандидатов.\n"
          "Каждый кандидат оценивается по нескольким критериям c1,...,cn.\n"
          "Примеры файлов с данными о кандидатах можно найти в папке data/\n\n")
    file_number = get_data_file_number()
    if file_number is None:
        return None
    data = read_data_from_csv(os.path.join('data', f'candidates{file_number}.csv'))
    return data
