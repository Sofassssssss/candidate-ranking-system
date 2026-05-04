import csv
from typing import Dict, Tuple


def read_data_from_csv(filepath: str) -> Dict[str, Tuple[int, ...]]:
    """
    Считывает данные из CSV файла.

    Ожидается формат:
    c1,c2,c3,... (строка заголовков будет пропущена)
    a,3,3,3,...  (имя кандидата и его оценки по критериям)

    :param filepath: Путь к csv файлу.
    :return: Словарь, где ключ - имя кандидата, а значение - кортеж его оценок.
    """
    candidates_data: Dict[str, Tuple[int, ...]] = {}

    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)

            next(reader, None)

            for row_number, row in enumerate(reader, start=2):
                if not row:
                    continue

                candidate_name = row[0].strip()

                try:
                    scores = tuple(int(value.strip()) for value in row[1:])
                    candidates_data[candidate_name] = scores
                except ValueError as e:
                    print(
                        f"Предупреждение: Ошибка преобразования данных в строке {row_number} для кандидата '{candidate_name}'. Пропускаем. Ошибка: {e}")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filepath}' не найден.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при чтении файла: {e}")

    return candidates_data