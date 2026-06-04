import matplotlib.pyplot as plt
from typing import List, Tuple
import os

TITLE_FONT = 50
SUBTITLE_FONT = 40
COL_HEADER_FONT = 40
CANDIDATE_FONT = 35


def visualize_result(linearizations: List[Tuple[str, ...]], output_filename: str = "ranking.png"):
    output_dir = "result"
    os.makedirs(output_dir, exist_ok=True)

    reversed_lins = [list(reversed(lin)) for lin in linearizations]
    num_cols = len(reversed_lins)
    num_rows = len(reversed_lins[0])

    fig_width = max(14, num_cols * 6)
    fig_height = max(10, num_rows * 3.0 + 4)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    fig.text(0.5, 0.97, "Ранжированный список кандидатов",
             ha='center', va='center', fontsize=TITLE_FONT, fontweight='bold', family='monospace')

    subtext = ("Кандидаты располагаются сверху вниз от лучшего к худшему.\n"
               "Может быть представлено несколько вариантов ранжирований.")
    fig.text(0.5, 0.87, subtext,
             ha='center', va='center', fontsize=SUBTITLE_FONT, color='#555555', family='monospace')

    if num_cols > 1:
        x_positions = [0.05 + 0.9 * i / (num_cols - 1) for i in range(num_cols)]
    else:
        x_positions = [0.5]

    if num_rows > 1:
        y_positions = [0.78 - 0.72 * i / (num_rows - 1) for i in range(num_rows)]
    else:
        y_positions = [0.5]

    for col_idx, lin in enumerate(reversed_lins):
        x = x_positions[col_idx]

        ax.text(x, 0.88, f"Вариант {col_idx + 1}",
                ha='center', va='center', fontsize=COL_HEADER_FONT, fontweight='bold', color='#6c757d')

        for row_idx, candidate in enumerate(lin):
            y = y_positions[row_idx]

            is_best = (row_idx == 0)

            bg_color = "#d4edda" if is_best else "#ffffff"
            border_color = "#28a745" if is_best else "#343a40"

            bbox_props = dict(boxstyle="round,pad=1.0", facecolor=bg_color,
                              edgecolor=border_color, linewidth=4)

            ax.text(x, y, str(candidate), ha="center", va="center",
                    size=CANDIDATE_FONT, fontweight='bold', bbox=bbox_props, zorder=3)

            if row_idx < num_rows - 1:
                y_next = y_positions[row_idx + 1]

                ax.annotate("",
                            xy=(x, y_next), xycoords='data',
                            xytext=(x, y), textcoords='data',
                            arrowprops=dict(arrowstyle="->", color="#adb5bd",
                                            linewidth=6,
                                            shrinkA=60,
                                            shrinkB=60),
                            zorder=2)

    filepath = os.path.join(output_dir, output_filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"\nРанжированный список успешно сохранен: {filepath}")
