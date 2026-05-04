import os
from typing import Dict, Tuple
from src.utils import read_data_from_csv
from src.ranking import get_pareto_orderings, exact_minimal_family_optimized


def main():
    filepath = os.path.join('data', 'data1.csv')
    data = read_data_from_csv(filepath)
    elements, orderings = get_pareto_orderings(data)
    result = exact_minimal_family_optimized(elements, orderings)

    print(result)


if __name__ == "__main__":
    main()
