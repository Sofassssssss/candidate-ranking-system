import os
import time
import matplotlib.pyplot as plt
from typing import List

from src.utils import read_data_from_csv
from src.ranking import get_pareto_orderings, exact_minimal_family_optimized


def run_algorithm_pipeline(filepath: str):
    data = read_data_from_csv(filepath)
    if not data:
        return

    elements, orderings = get_pareto_orderings(data)

    exact_minimal_family_optimized(elements, orderings)
    pass


def measure_average_time(filepath: str, num_runs: int = 10) -> float:
    if not os.path.exists(filepath):
        print(f"Файл {filepath} не найден!")
        return 0.0

    times = []
    for _ in range(num_runs):
        start_time = time.perf_counter()
        run_algorithm_pipeline(filepath)
        end_time = time.perf_counter()
        times.append(end_time - start_time)

    avg_time = sum(times) / len(times)
    return avg_time


def plot_and_save(x_values: List[int], y_times: List[float], x_label: str, title: str, filename: str):
    plt.figure(figsize=(8, 5))

    plt.plot(x_values, y_times, marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=8)

    plt.title(title, fontsize=14, fontweight='bold', pad=15)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel("Время выполнения (секунды)", fontsize=12)

    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"График сохранен: {filename}")


def main():
    base_dir = "research_data"

    print("Начинаем профилирование алгоритма (это может занять некоторое время)...\n")

    print("Эксперимент 1: Зависимость от числа кандидатов...")
    cands_x = [5, 6, 7, 8, 9, 10, 11]
    times_exp1 = []
    for c in cands_x:
        path = os.path.join(base_dir, f"exp1_cands_{c}.csv")
        t = measure_average_time(path, num_runs=10)
        times_exp1.append(t)
        print(f"  Кандидатов: {c:2d} -> Среднее время: {t:.5f} сек")

    plot_and_save(
        x_values=cands_x,
        y_times=times_exp1,
        x_label="Количество альтернатив (кандидатов)",
        title="Зависимость времени работы от числа кандидатов\n(при фиксированном числе критериев M=5)",
        filename="statistics/graph_1_candidates.png"
    )

    print("\nЭксперимент 2: Зависимость от числа критериев...")
    crits_x = [5, 10, 15, 25, 50, 75, 100]
    times_exp2 = []
    for c in crits_x:
        path = os.path.join(base_dir, f"exp2_crits_{c}.csv")
        t = measure_average_time(path, num_runs=10)
        times_exp2.append(t)
        print(f"  Критериев: {c:3d} -> Среднее время: {t:.5f} сек")

    plot_and_save(
        x_values=crits_x,
        y_times=times_exp2,
        x_label="Количество критериев",
        title="Зависимость времени работы от числа критериев\n(при фиксированном числе кандидатов N=7)",
        filename="statistics/graph_2_criteria.png"
    )

    print("\nЭксперимент 3: Синхронный рост (Кандидаты = Критерии)...")
    sq_x = [5, 6, 7, 8, 9, 10, 11]
    times_exp3 = []
    for s in sq_x:
        path = os.path.join(base_dir, f"exp3_sq_{s}.csv")
        t = measure_average_time(path, num_runs=10)
        times_exp3.append(t)
        print(f"  Размерность (N=M): {s:2d} -> Среднее время: {t:.5f} сек")

    plot_and_save(
        x_values=sq_x,
        y_times=times_exp3,
        x_label="Размерность задачи (N = M)",
        title="Рост времени при одновременном увеличении\nчисла альтернатив и критериев",
        filename="statistics/graph_3_candidates_and_criteria.png"
    )

    print("\nПрофилирование завершено!")


if __name__ == "__main__":
    main()