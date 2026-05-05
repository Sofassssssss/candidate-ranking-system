from src.ranking import get_pareto_orderings, exact_minimal_family_optimized
from src.cli.cli import get_data_from_user_input
from src.utils import visualize_result

def main():
    data = get_data_from_user_input()
    if data is None:
        return
    elements, orderings = get_pareto_orderings(data)
    result = exact_minimal_family_optimized(elements, orderings)
    visualize_result(result)

if __name__ == "__main__":
    main()
