import os
import csv
import random


def generate_smart_scores(num_candidates: int, num_criteria: int) -> list[list[int]]:
    candidates_scores = []

    for i in range(num_candidates):
        if num_candidates > 1:
            latent_skill = i / (num_candidates - 1)
        else:
            latent_skill = 0.5

        base_score = 2 + latent_skill * 7

        scores = []
        for _ in range(num_criteria):
            noise = random.gauss(mu=0.0, sigma=0.6)
            final_score = round(base_score + noise)

            final_score = max(1, min(10, final_score))
            scores.append(final_score)

        candidates_scores.append(scores)

    random.shuffle(candidates_scores)
    return candidates_scores


def create_dataset(filepath: str, num_candidates: int, num_criteria: int):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        header = ["candidate"] + [f"c{i}" for i in range(1, num_criteria + 1)]
        writer.writerow(header)

        smart_scores = generate_smart_scores(num_candidates, num_criteria)

        for i in range(num_candidates):
            cand_name = f"cand_{i + 1}"
            writer.writerow([cand_name] + smart_scores[i])

def generate_data():
    base_dir = "research_data"
    os.makedirs(base_dir, exist_ok=True)

    candidates_list_exp1 = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    fixed_criteria = 5
    print("Генерация данных для Эксперимента 1...")
    for cands in candidates_list_exp1:
        filepath = os.path.join(base_dir, f"exp1_cands_{cands}.csv")
        create_dataset(filepath, cands, fixed_criteria)
        print(f"  Создан: {filepath}")

    fixed_candidates = 8
    criteria_list_exp2 = [5, 10, 15, 25, 50, 75, 100]
    print("\nГенерация данных для Эксперимента 2...")
    for crits in criteria_list_exp2:
        filepath = os.path.join(base_dir, f"exp2_crits_{crits}.csv")
        create_dataset(filepath, fixed_candidates, crits)
        print(f"  Создан: {filepath}")

    square_list_exp3 = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    print("\nГенерация данных для Эксперимента 3...")
    for size in square_list_exp3:
        filepath = os.path.join(base_dir, f"exp3_sq_{size}.csv")
        create_dataset(filepath, size, size)
        print(f"  Создан: {filepath}")

    print("\nВсе тестовые данные успешно сгенерированы в папку 'research/research_data'!")


if __name__ == "__main__":
    generate_data()