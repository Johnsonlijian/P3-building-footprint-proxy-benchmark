# Reproducible Runbook

## Environment

Python 3.10+ is recommended.

No third-party package is required for the validation script. The optional plotting helper requires `matplotlib`.

## Validate Derived Outputs

```bash
python scripts/validate_derived_outputs.py
```

Expected summary:

- Full Shenzhen proxy rows: 76,042.
- Full conditional mean: 2,181,482 tCO2e.
- Hash-sample rows: 8,000.
- Hash-sample conditional mean: 267,095 tCO2e.

## Data Boundary

Raw third-party geospatial data are not redistributed. Source links are provided in `DATASETS_AND_LINKS.csv`; derived non-sensitive summaries and manuscript figures are included for auditability.

## Optional Derived Figure Regeneration

```bash
pip install matplotlib
python scripts/make_shenzhen_histogram.py
```

This regenerates `outputs/figures/figure_4b_shenzhen_full_vs_hash_sample_from_summary.png` from the public aggregate summary table.


## v22 Derived Tables

- `outputs/derived_tables/shenzhen_full_vs_hash_sample_mc_summary.csv`
- `outputs/derived_tables/shenzhen_full_inventory_type_summary.csv`
- `outputs/derived_tables/lca_coefficient_table_v21.csv`

These tables report only derived summaries, not event-level Overture rows.


## v24 Interval Validation

- `outputs/derived_tables/interval_validation_by_city_year.csv`
- `outputs/derived_tables/interval_validation_summary.csv`
- `outputs/derived_tables/interval_validation_bootstrap_ci.csv`
- `outputs/figures/figure_s1_interval_validation.png`

These outputs are derived from the synthetic benchmark only and do not imply Shenzhen event validation.
