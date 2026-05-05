from rich.console import Console
from typing import List, Tuple
from rich.align import Align
from rich.table import Table
from rich import box


def visualize_result(linearizations: List[Tuple[str, ...]]):
    console = Console()

    print(
        "\nРАНЖИРОВАННЫЙ СПИСОК КАНДИДАТОВ.\n"
        "Кандидаты располагаются сверху вниз от лучшего к худшему.\n"
        "Может быть представлено несколько вариантов ранжирований.\n"
    )

    table = Table(box=box.ROUNDED, expand=False, border_style="bright_blue")

    for i in range(1, len(linearizations) + 1):
        table.add_column(str(i), justify="center", header_style="bold magenta", min_width=5)

    reversed_lins = [list(reversed(lin)) for lin in linearizations]
    num_elements = len(reversed_lins[0])

    for i in range(num_elements):
        candidate_row = []
        for j in range(len(linearizations)):
            color = "bold green" if i == 0 else "white"
            candidate_row.append(f"[{color}]{reversed_lins[j][i]}[/{color}]")

        table.add_row(*candidate_row)

        if i < num_elements - 1:
            arrow_row = ["[dim yellow]↓[/dim yellow]" for _ in range(len(linearizations))]
            table.add_row(*arrow_row)

    console.print(Align.left(table))
    console.print()