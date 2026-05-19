"""Validate derived outputs shipped with the public package.

This script uses only the non-sensitive derived tables included in the repo.
It does not download or redistribute raw third-party data.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "outputs" / "derived_tables" / "shenzhen_full_vs_hash_sample_mc_summary.csv"
TYPE_SUMMARY = ROOT / "outputs" / "derived_tables" / "shenzhen_full_inventory_type_summary.csv"
COEFFICIENTS = ROOT / "outputs" / "derived_tables" / "lca_coefficient_table_v21.csv"
INTERVAL_SUMMARY = ROOT / "outputs" / "derived_tables" / "interval_validation_summary.csv"


def read_first(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as f:
        return next(csv.DictReader(f))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(SUMMARY)
    by_label = {row["label"]: row for row in rows}
    required = {
        "full_inventory": (76042, 2181482),
        "hash_sample_8000": (8000, 267095),
    }
    for label, (expected_rows, expected_mean) in required.items():
        if label not in by_label:
            raise SystemExit(f"Missing row: {label}")
        row = by_label[label]
        observed_rows = int(float(row["n_rows"]))
        observed_mean = round(float(row["mean_tCO2e"]))
        if observed_rows != expected_rows:
            raise SystemExit(f"{label} n_rows: expected {expected_rows}, observed {observed_rows}")
        if observed_mean != expected_mean:
            raise SystemExit(f"{label} mean_tCO2e: expected rounded {expected_mean}, observed {observed_mean}")
    for path in [TYPE_SUMMARY, COEFFICIENTS, INTERVAL_SUMMARY]:
        if not path.exists():
            raise SystemExit(f"Missing derived table: {path}")
    interval = read_first(INTERVAL_SUMMARY)
    if int(float(interval["covered_count"])) != 53:
        raise SystemExit("Interval coverage count changed unexpectedly")
    if round(float(interval["coverage_90"]), 3) != 0.707:
        raise SystemExit("Interval coverage changed unexpectedly")
    print("Derived output validation passed.")
    full = by_label["full_inventory"]
    sample = by_label["hash_sample_8000"]
    print(f"Full Shenzhen proxy rows: {int(float(full['n_rows'])):,}")
    print(f"Full conditional mean tCO2e: {float(full['mean_tCO2e']):,.0f}")
    print(f"Hash-sample rows: {int(float(sample['n_rows'])):,}")
    print(f"Hash-sample conditional mean tCO2e: {float(sample['mean_tCO2e']):,.0f}")
    print(f"Synthetic 90% interval coverage: {float(interval['coverage_90']):.3f}")


if __name__ == "__main__":
    main()
