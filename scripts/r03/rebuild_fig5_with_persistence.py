from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TABLE_R02 = ROOT / "outputs" / "derived_tables" / "r02"
TABLE_R03 = ROOT / "outputs" / "derived_tables" / "r03"
SVG = ROOT / "outputs" / "figures" / "r02_svg"
PDF = ROOT / "outputs" / "figures" / "r02_pdf"
PNG = ROOT / "outputs" / "figures" / "r02_png"

PALETTE = {
    "blue": "#2F5597",
    "teal": "#0F766E",
    "green": "#4E8F4A",
    "orange": "#D4872C",
    "red": "#B94A48",
    "gray": "#5B6470",
    "light_gray": "#E8ECF2",
}


def style_axes(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", linestyle=":", alpha=0.35)
    ax.tick_params(labelsize=8)


def savefig(fig: plt.Figure, stem: str) -> None:
    for directory in [SVG, PDF, PNG]:
        directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(SVG / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(PDF / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(PNG / f"{stem}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    summary = pd.read_csv(TABLE_R02 / "table_r02_shenzhen_proxy_summary.csv")
    types = pd.read_csv(TABLE_R02 / "table_r02_shenzhen_type_skew.csv")
    triage = pd.read_csv(TABLE_R02 / "inputs" / "validation_machine_triage_summary.csv").sort_values("n", ascending=False)
    persistence = pd.read_csv(TABLE_R03 / "table_r03_shenzhen_overture_persistence_summary.csv")

    fig, axes = plt.subplots(1, 4, figsize=(15.2, 4.2), gridspec_kw={"width_ratios": [1.05, 1.05, 1.08, 1.0]})

    ax = axes[0]
    x = np.arange(len(summary))
    y = summary["mean_tCO2e"] / 1e6
    yerr = np.vstack([(summary["mean_tCO2e"] - summary["p05_tCO2e"]) / 1e6, (summary["p95_tCO2e"] - summary["mean_tCO2e"]) / 1e6])
    ax.bar(x, y, yerr=yerr, capsize=4, color=[PALETTE["blue"], PALETTE["orange"]], edgecolor="#263238", linewidth=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(["Full proxy\ninventory", "Hash sample\n8,000"])
    ax.set_ylabel("Conditional screening total (Mt CO2e)")
    ax.set_title("a  Conditional totals")
    style_axes(ax)

    ax = axes[1]
    type_rows = types.sort_values("n_rows", ascending=False)
    labels = type_rows["building_type"].str.replace("_", " ")
    shares = 100 * type_rows["n_rows"] / type_rows["n_rows"].sum()
    ax.barh(labels, shares, color=PALETTE["teal"], edgecolor="#263238", linewidth=0.7)
    ax.set_xlabel("Share of disappeared-ID rows (%)")
    ax.set_title("b  Overture type skew")
    ax.grid(True, axis="x", linestyle=":", alpha=0.35)
    ax.grid(False, axis="y")
    for i, v in enumerate(shares):
        ax.text(v + 0.2, i, f"{v:.2f}%", va="center", fontsize=7.5)

    ax = axes[2]
    p = persistence.set_index("persistence_status")
    statuses = ["persistent_absent_in_check_release", "reappeared_in_check_release"]
    counts = [int(p.loc[s, "n_rows"]) if s in p.index else 0 for s in statuses]
    ax.bar(["Persistent\nabsent", "Reappeared"], counts, color=[PALETTE["green"], PALETTE["red"]], edgecolor="#263238", linewidth=0.7)
    ax.set_yscale("log")
    ax.set_ylim(8, 350000)
    ax.set_ylabel("Rows, log scale")
    ax.set_title("c  Third-release check")
    style_axes(ax)
    for i, v in enumerate(counts):
        pct = 100 * v / sum(counts)
        ax.text(i, v * (1.15 if v > 100 else 1.7), f"{v:,}\n({pct:.2f}%)", ha="center", va="bottom", fontsize=7.5)
    ax.text(0.5, 0.18, "2026-05-20.0 check\nreduces single-release churn", transform=ax.transAxes, ha="center", va="center", fontsize=7.5, bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=PALETTE["light_gray"]))

    ax = axes[3]
    labels = ["New-release\ncontrol", "Tiny proxy\ngeometry", "No new\noverlap"]
    ax.bar(labels[: len(triage)], triage["n"], color=[PALETTE["green"], PALETTE["gray"], PALETTE["red"]], edgecolor="#263238", linewidth=0.7)
    ax.set_ylabel("Validation-packet rows")
    ax.set_title("d  Machine triage only")
    style_axes(ax)
    for i, v in enumerate(triage["n"]):
        ax.text(i, int(v) + 4, str(int(v)), ha="center", va="bottom", fontsize=7.5)
    ax.text(0.5, 0.54, "Not human labels\nNot detector accuracy", transform=ax.transAxes, ha="center", va="center", fontsize=7.5, bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=PALETTE["light_gray"]))

    fig.suptitle("Figure 5. Shenzhen proxy screening is strengthened by persistence checks but remains unverified", fontsize=13, fontweight="bold", y=1.04)
    fig.tight_layout()
    savefig(fig, "fig5_shenzhen_proxy_boundary")


if __name__ == "__main__":
    main()
