"""Validate derived outputs shipped with the public package.

This script uses only the non-sensitive derived tables included in the repo.
It does not download or redistribute raw third-party data.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "outputs" / "derived_tables" / "shenzhen_proxy_demonstrator_summary.csv"
QUANTILES = ROOT / "outputs" / "derived_tables" / "shenzhen_event_quantiles.csv"


def read_first(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as f:
        return next(csv.DictReader(f))


def main() -> None:
    row = read_first(SUMMARY)
    required_counts = {
        "removed_id_count_full": 76042,
        "rows_written_export_cap": 8000,
    }
    for key, expected in required_counts.items():
        observed = int(float(row.get(key, "nan")))
        if observed != expected:
            raise SystemExit(f"{key}: expected {expected}, observed {observed}")
    mean = float(row["conditional_embodied_mean_tCO2e"])
    if round(mean) != 181208:
        raise SystemExit(f"conditional_embodied_mean_tCO2e: expected rounded 181208, observed {mean}")
    if not QUANTILES.exists():
        raise SystemExit(f"Missing quantile table: {QUANTILES}")
    print("Derived output validation passed.")
    print(f"Shenzhen capped rows: {row['rows_written_export_cap']} / {row['removed_id_count_full']}")
    print(f"Conditional mean tCO2e: {float(row['conditional_embodied_mean_tCO2e']):,.0f}")
    print(
        "Conditional p05-p95 tCO2e: "
        f"{float(row['conditional_embodied_p05_tCO2e']):,.0f}-"
        f"{float(row['conditional_embodied_p95_tCO2e']):,.0f}"
    )


if __name__ == "__main__":
    main()
