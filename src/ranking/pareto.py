from typing import List, Dict, Tuple, Set
from ..ordering import Ordering


def dominates(x: Tuple[int, ...], y: Tuple[int, ...]) -> bool:
    """
    Проверка доминирования вектора x над вектором y по Парето.
    Правило: x доминирует над y, если для всех i: x_i >= y_i, и хотя бы для одного j: x_j > y_j.
    """
    strictly_greater = False
    for xi, yi in zip(x, y):
        if xi < yi:
            return False
        if xi > yi:
            strictly_greater = True

    return strictly_greater


def get_pareto_orderings(data: Dict[str, Tuple[int, ...]]) -> Tuple[List[str], List[Ordering]]:
    """
    Представление диаграммы Хассе на основе отношения непосредственного доминирования по Парето.
    """
    elements = sorted(list(data.keys()))
    all_edges: Set[Tuple[str, str]] = set()

    # Шаг 1: Находим все возможные отношения доминирования (полный граф)
    for lesser_cand in elements:
        for bigger_cand in elements:
            if lesser_cand != bigger_cand:
                if dominates(data[bigger_cand], data[lesser_cand]):
                    all_edges.add((lesser_cand, bigger_cand))

    # Шаг 2: Осуществляем транзитивную редукцию
    # Если есть путь A -> B и B -> C, то ребро A -> C нужно удалить
    direct_edges = set(all_edges)

    for (lesser, bigger) in all_edges:
        for intermediate in elements:
            if (lesser, intermediate) in all_edges and (intermediate, bigger) in all_edges:
                if (lesser, bigger) in direct_edges:
                    direct_edges.remove((lesser, bigger))

    orderings = [Ordering(lesser, bigger) for lesser, bigger in sorted(list(direct_edges))]

    return elements, orderings