"""Create a lightweight summary figure from derived quantiles.

The full event-level table is not redistributed. This script creates a compact
derived-bar figure from the quantile table included in the repository.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
QUANTILES = ROOT / "outputs" / "derived_tables" / "shenzhen_event_quantiles.csv"
OUT = ROOT / "outputs" / "figures" / "figure_4b_shenzhen_quantile_summary.png"


def main() -> None:
    rows = list(csv.DictReader(QUANTILES.open(newline="", encoding="utf-8")))
    xs = [r["quantile"] for r in rows]
    ys = [float(r["embodied_mean_tCO2e"]) for r in rows]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.plot(xs, ys, marker="o", color="#2f5597")
    ax.set_xlabel("Quantile")
    ax.set_ylabel("Event-level mean tCO2e")
    ax.set_title("Shenzhen capped proxy rows: derived quantile summary")
    ax.grid(axis="y", linestyle=":", alpha=0.45)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300)
    print(OUT)


if __name__ == "__main__":
    main()
