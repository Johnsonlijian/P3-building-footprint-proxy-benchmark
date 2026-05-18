"""Create a lightweight Shenzhen full-vs-sample summary figure.

The full event-level table is not redistributed. This script creates a compact
derived-bar figure from the public aggregate summary table included here.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "outputs" / "derived_tables" / "shenzhen_full_vs_hash_sample_mc_summary.csv"
OUT = ROOT / "outputs" / "figures" / "figure_4b_shenzhen_full_vs_hash_sample_from_summary.png"


def main() -> None:
    rows = list(csv.DictReader(SUMMARY.open(newline="", encoding="utf-8")))
    xs = [r["label"].replace("_", " ") for r in rows]
    ys = [float(r["mean_tCO2e"]) for r in rows]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.bar(xs, ys, color=["#2f5597", "#70ad47"])
    ax.set_ylabel("Conditional mean tCO2e")
    ax.set_title("Shenzhen full proxy inventory and hash sample")
    ax.grid(axis="y", linestyle=":", alpha=0.45)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300)
    print(OUT)


if __name__ == "__main__":
    main()
