import os
import matplotlib.pyplot as plt
from typing import List, Tuple


def visualize_result(linearizations: List[Tuple[str, ...]], output_filename: str = "ranking.png"):
    output_dir = "result"
    os.makedirs(output_dir, exist_ok=True)

    reversed_lins = [list(reversed(lin)) for lin in linearizations]
    num_cols = len(reversed_lins)
    num_rows = len(reversed_lins[0])

    fig_width = max(6, num_cols * 2.5)
    fig_height = max(5, num_rows * 1.5 + 2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    fig.text(0.5, 0.95, "Ранжированный список кандидатов",
             ha='center', va='center', fontsize=25, fontweight='bold', family='monospace')

    subtext = ("Кандидаты располагаются сверху вниз от лучшего к худшему.\n"
               "Может быть представлено несколько вариантов ранжирований.")
    fig.text(0.5, 0.85, subtext,
             ha='center', va='center', fontsize=20, color='#555555', family='monospace')

    if num_cols > 1:
        x_positions = [0.1 + 0.8 * i / (num_cols - 1) for i in range(num_cols)]
    else:
        x_positions = [0.5]

    if num_rows > 1:
        y_positions = [0.8 - 0.7 * i / (num_rows - 1) for i in range(num_rows)]
    else:
        y_positions = [0.5]

    for col_idx, lin in enumerate(reversed_lins):
        x = x_positions[col_idx]

        ax.text(x, 0.85, f"Вариант {col_idx + 1}",
                ha='center', va='center', fontsize=16, fontweight='bold', color='#6c757d')

        for row_idx, candidate in enumerate(lin):
            y = y_positions[row_idx]

            bg_color = "#d4edda" if row_idx == 0 else "#ffffff"
            border_color = "#28a745" if row_idx == 0 else "#343a40"

            bbox_props = dict(boxstyle="round,pad=0.6", facecolor=bg_color,
                              edgecolor=border_color, linewidth=2)

            ax.text(x, y, str(candidate), ha="center", va="center",
                    size=14, fontweight='bold', bbox=bbox_props, zorder=3)

            if row_idx < num_rows - 1:
                y_next = y_positions[row_idx + 1]

                ax.annotate("",
                            xy=(x, y_next), xycoords='data',
                            xytext=(x, y), textcoords='data',
                            arrowprops=dict(arrowstyle="->", color="#adb5bd",
                                            linewidth=2, shrinkA=22, shrinkB=22),
                            zorder=2)

    filepath = os.path.join(output_dir, output_filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"\nРанжированный список кандидатов успешно сохранен в файл: {filepath}")
