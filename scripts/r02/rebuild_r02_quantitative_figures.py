from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TABLE = ROOT / "outputs" / "derived_tables" / "r02"
INPUT = TABLE / "inputs"
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
    "text": "#17212B",
}


def style_axes(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", linestyle=":", alpha=0.35)
    ax.tick_params(labelsize=9)


def savefig(fig: plt.Figure, stem: str) -> None:
    for directory in [SVG, PDF, PNG]:
        directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(SVG / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(PDF / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(PNG / f"{stem}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def make_fig2() -> None:
    base = pd.read_csv(TABLE / "table_r02_point_estimator_benchmarks.csv")
    city = pd.read_csv(INPUT / "city_year_summary.csv")
    base["label"] = base["method"].map(
        {
            "MC_posterior_mean": "MC mean",
            "global_mean_prior_coeff": "Global mean",
            "global_median_coeff": "Global median",
            "typology_mean_prior_coeff": "Typology mean",
            "typology_median_coeff": "Typology median",
        }
    )
    order = ["MC mean", "Typology mean", "Typology median", "Global mean", "Global median"]
    colors = [PALETTE["blue"], PALETTE["teal"], PALETTE["orange"], PALETTE["gray"], "#9AA2AF"]
    b = base.set_index("label").loc[order].reset_index()
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.2))
    ax = axes[0]
    ax.bar(b["label"], b["mean_abs_pct_error"], color=colors, edgecolor="#263238", linewidth=0.7)
    ax.set_ylabel("Mean absolute percent error (%)")
    ax.set_title("a  Point estimates")
    ax.tick_params(axis="x", rotation=30)
    style_axes(ax)
    for i, row in b.iterrows():
        ax.text(i, row["mean_abs_pct_error"] + 0.18, f"{row['mean_abs_pct_error']:.2f}", ha="center", fontsize=8)
    ax = axes[1]
    x = city["embodied_GT_tCO2e"] / 1e6
    y = city["embodied_mean_tCO2e"] / 1e6
    ax.scatter(x, y, s=28, color=PALETTE["blue"], alpha=0.78, edgecolor="white", linewidth=0.3)
    lim = max(float(x.max()), float(y.max())) * 1.05
    ax.plot([0, lim], [0, lim], linestyle="--", color=PALETTE["gray"], linewidth=1.0)
    ax.set_xlabel("Synthetic truth (Mt CO2e)")
    ax.set_ylabel("MC posterior mean (Mt CO2e)")
    ax.set_title("b  Controlled recovery")
    style_axes(ax)
    fig.suptitle("Figure 2. Monte Carlo is an uncertainty layer, not a better point estimator", fontsize=13, fontweight="bold", y=1.03)
    fig.tight_layout()
    savefig(fig, "fig2_point_estimate_negative_benchmark")


def make_fig3() -> None:
    by = pd.read_csv(INPUT / "interval_validation_by_city_year.csv").sort_values("normalized_interval_score_90", ascending=False).reset_index(drop=True)
    summary = pd.read_csv(TABLE / "table_r02_interval_summary.csv").iloc[0]
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.2))
    ax = axes[0]
    colors = by["covered_90"].map({1: PALETTE["blue"], 0: PALETTE["red"]})
    ax.scatter(np.arange(len(by)), by["normalized_interval_score_90"], c=colors, s=28, edgecolor="white", linewidth=0.3)
    ax.axhline(float(by["normalized_interval_score_90"].median()), color=PALETTE["gray"], linestyle="--", linewidth=1.0)
    ax.set_xlabel("City-year aggregates sorted by interval score")
    ax.set_ylabel("Normalized 90% interval score")
    ax.set_title("a  Interval penalties")
    style_axes(ax)
    ax = axes[1]
    vals = [int(summary["covered_count"]), int(summary["n_city_year"] - summary["covered_count"])]
    ax.bar(["Covered", "Missed"], vals, color=[PALETTE["blue"], PALETTE["red"]], edgecolor="#263238", linewidth=0.7)
    ax.set_ylabel("City-year aggregates")
    ax.set_title("b  Nominal 90% coverage")
    style_axes(ax)
    ax.text(0.5, max(vals) * 0.76, "Coverage = 70.7%\nWilson 95% CI 59.6%-79.8%", ha="center", va="center", fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=PALETTE["light_gray"]))
    fig.suptitle("Figure 3. Coefficient-only intervals under-cover total uncertainty", fontsize=13, fontweight="bold", y=1.03)
    fig.tight_layout()
    savefig(fig, "fig3_interval_undercoverage")


def make_fig4() -> None:
    stress = pd.read_csv(INPUT / "stress_test_results.csv").sort_values("abs_pct_error", ascending=False)
    top = stress.head(12).copy()
    top["scenario"] = top.apply(lambda r: f"C {float(r['coeff_scale']):.2g}\nA {float(r['area_scale']):.2g}", axis=1)
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.4))
    ax = axes[0]
    ax.bar(top["scenario"], top["abs_pct_error"], color=PALETTE["orange"], edgecolor="#263238", linewidth=0.7)
    ax.set_ylabel("Absolute percent error (%)")
    ax.set_title("a  Largest stress cases")
    style_axes(ax)
    ax.text(0.02, 0.95, f"Max = {float(top['abs_pct_error'].iloc[0]):.2f}%", transform=ax.transAxes, ha="left", va="top", fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=PALETTE["light_gray"]))
    ax = axes[1]
    sizes = 35 + stress["abs_pct_error"].to_numpy() * 8
    sc = ax.scatter(stress["area_scale"], stress["coeff_scale"], c=stress["abs_pct_error"], s=sizes, cmap="YlOrRd", edgecolor="#263238", linewidth=0.7)
    ax.set_xlabel("Area scale")
    ax.set_ylabel("Coefficient scale")
    ax.set_title("b  Observed stress combinations")
    ax.set_xlim(0.74, 1.24)
    ax.set_ylim(0.66, 1.34)
    ax.set_xticks([0.8, 1.0, 1.2])
    ax.set_yticks([0.7, 0.8, 0.9, 1.1, 1.2, 1.3])
    ax.grid(True, linestyle=":", alpha=0.35)
    for _, r in stress.iterrows():
        ax.text(float(r["area_scale"]), float(r["coeff_scale"]), f"{float(r['abs_pct_error']):.0f}", ha="center", va="center", fontsize=7)
    cbar = fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Absolute percent error (%)", fontsize=9)
    fig.suptitle("Figure 4. Stress tests define the boundary of interpretable carbon totals", fontsize=13, fontweight="bold", y=1.03)
    fig.tight_layout()
    savefig(fig, "fig4_assumption_stress_boundary")


def make_fig5() -> None:
    summary = pd.read_csv(TABLE / "table_r02_shenzhen_proxy_summary.csv")
    types = pd.read_csv(TABLE / "table_r02_shenzhen_type_skew.csv")
    triage = pd.read_csv(INPUT / "validation_machine_triage_summary.csv").sort_values("n", ascending=False)
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.2), gridspec_kw={"width_ratios": [1.1, 1.05, 1.0]})
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
    rows = types.sort_values("n_rows", ascending=False)
    labels = rows["building_type"].str.replace("_", " ")
    shares = 100 * rows["n_rows"] / rows["n_rows"].sum()
    ax.barh(labels, shares, color=PALETTE["teal"], edgecolor="#263238", linewidth=0.7)
    ax.set_xlabel("Share of disappeared-ID rows (%)")
    ax.set_title("b  Overture type skew")
    ax.grid(True, axis="x", linestyle=":", alpha=0.35)
    ax.grid(False, axis="y")
    for i, v in enumerate(shares):
        ax.text(v + 0.2, i, f"{v:.2f}%", va="center", fontsize=8)
    ax = axes[2]
    labels = ["New-release\ncontrol", "Tiny proxy\ngeometry", "No new\noverlap"]
    ax.bar(labels[: len(triage)], triage["n"], color=[PALETTE["green"], PALETTE["gray"], PALETTE["red"]], edgecolor="#263238", linewidth=0.7)
    ax.set_ylabel("Validation-packet rows")
    ax.set_title("c  Machine triage only")
    style_axes(ax)
    ax.text(0.5, 0.58, "Not human labels\nNot detector accuracy", transform=ax.transAxes, ha="center", va="center", fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=PALETTE["light_gray"]))
    fig.suptitle("Figure 5. Shenzhen is a proxy-screening demonstration, not verified demolition accounting", fontsize=13, fontweight="bold", y=1.03)
    fig.tight_layout()
    savefig(fig, "fig5_shenzhen_proxy_boundary")


def main() -> None:
    plt.rcParams.update({"font.family": "Arial", "savefig.facecolor": "white"})
    make_fig2()
    make_fig3()
    make_fig4()
    make_fig5()


if __name__ == "__main__":
    main()
