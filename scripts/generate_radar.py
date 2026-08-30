"""Generate placeholder dark-theme skill radar charts for the profile README."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets"
CATEGORIES = ["Python", "FastAPI", "React", "LLM/AI", "Databases", "Git"]
VALUES = [7, 7, 5, 8, 5, 7]
GREEN = "#39D353"
GRID = "#30363D"
TEXT = "#C9D1D9"


def make_chart(output: Path, title: str) -> None:
    """Render a transparent SVG radar chart with the supplied placeholder values."""
    angles = np.linspace(0, 2 * np.pi, len(CATEGORIES), endpoint=False).tolist()
    chart_values = VALUES + VALUES[:1]
    chart_angles = angles + angles[:1]

    fig, axis = plt.subplots(figsize=(6, 6), subplot_kw={"polar": True})
    fig.patch.set_alpha(0)
    axis.set_facecolor("none")
    axis.set_theta_offset(np.pi / 2)
    axis.set_theta_direction(-1)
    axis.set_ylim(0, 10)
    axis.set_xticks(angles)
    axis.set_xticklabels(CATEGORIES, color=TEXT, fontsize=10)
    axis.set_yticks([2, 4, 6, 8, 10])
    axis.set_yticklabels(["2", "4", "6", "8", "10"], color=TEXT, fontsize=8)
    axis.grid(color=GRID, linewidth=0.8)
    axis.spines["polar"].set_color(GREEN)
    axis.plot(chart_angles, chart_values, color=GREEN, linewidth=2)
    axis.fill(chart_angles, chart_values, color=GREEN, alpha=0.22)
    axis.set_title(title, color=GREEN, fontsize=14, fontweight="bold", pad=20)
    fig.savefig(output, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    make_chart(OUTPUT_DIR / "radar-dark.svg", "Skill Radar")
    # A matching second chart keeps the README's two-column presentation balanced.
    make_chart(OUTPUT_DIR / "radar-dark-secondary.svg", "Skill Snapshot")


if __name__ == "__main__":
    main()
