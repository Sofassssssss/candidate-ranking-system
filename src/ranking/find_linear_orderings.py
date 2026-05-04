from typing import List, Tuple, Set
from itertools import combinations
from collections import defaultdict
from ..ordering import Ordering



def find_linear_orderings_optimized(elements: List[str], orderings: List[Ordering]) -> List[Tuple[str, ...]]:
    """
    Нахождение линеаризаций упорядоченного множества.
    Процесс оптимизирован с помощью поиска с возвратом (backtracking).
    """
    adj = defaultdict(list)
    in_degree = {el: 0 for el in elements}

    for o in orderings:
        adj[o.lesser].append(o.bigger)
        in_degree[o.bigger] += 1

    result_permutations = []
    path = []

    def backtrack():
        if len(path) == len(elements):
            result_permutations.append(tuple(path))
            return

        available = [node for node in elements if in_degree[node] == 0 and node not in path]

        for node in available:
            path.append(node)
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1

            backtrack()

            path.pop()
            for neighbor in adj[node]:
                in_degree[neighbor] += 1

    backtrack()
    return result_permutations


def get_incomparable_pairs_optimized(elements: List[str], orderings: List[Ordering]) -> List[Tuple[str, str]]:
    """
    Нахождение несравнимых пар в упорядоченном множестве с помощью обхода графа (DFS).
    """
    adj = defaultdict(list)
    for o in orderings:
        adj[o.lesser].append(o.bigger)

    def get_reachable(start_node) -> Set[str]:
        visited = set()
        stack = [start_node]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(adj[node])
        return visited

    comparable = set()
    for el in elements:
        reachable = get_reachable(el)
        for r in reachable:
            if el != r:
                comparable.add((el, r))

    incomparable = []
    for a, b in combinations(elements, 2):
        if (a, b) not in comparable and (b, a) not in comparable:
            incomparable.append((a, b))

    return incomparable


def exact_minimal_family_optimized(elements: List[str], orderings: List[Ordering]) -> List[Tuple[str, ...]]:
    """
    Поиск минимального полного семейства линеаризаций.
    """
    linear_orders = find_linear_orderings_optimized(elements, orderings)
    incomparable_pairs = get_incomparable_pairs_optimized(elements, orderings)

    if not incomparable_pairs:
        return [linear_orders[0]]

    lo_covers_direct = []
    lo_covers_reverse = []

    for lo in linear_orders:
        lo_index_map = {el: idx for idx, el in enumerate(lo)}
        covered_direct = set()
        covered_reverse = set()

        for a, b in incomparable_pairs:
            if lo_index_map[a] < lo_index_map[b]:
                covered_direct.add((a, b))
            else:
                covered_reverse.add((a, b))

        lo_covers_direct.append(covered_direct)
        lo_covers_reverse.append(covered_reverse)

    total_incomparable = set(incomparable_pairs)

    for r in range(1, len(linear_orders) + 1):
        for comb_indices in combinations(range(len(linear_orders)), r):

            current_direct = set()
            current_reverse = set()

            for idx in comb_indices:
                current_direct.update(lo_covers_direct[idx])
                current_reverse.update(lo_covers_reverse[idx])

            if current_direct == total_incomparable and current_reverse == total_incomparable:
                return [linear_orders[i] for i in comb_indices]

    return []