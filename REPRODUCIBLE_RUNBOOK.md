# Reproducible Runbook

## Environment

Python 3.10+ is recommended.

```bash
pip install matplotlib
```

## Validate Derived Outputs

```bash
python scripts/validate_derived_outputs.py
```

Expected summary:

- Shenzhen capped rows: 8,000 / 76,042.
- Conditional mean: 181,208 tCO2e.
- Conditional p05-p95 interval: 173,744-189,388 tCO2e.

## Regenerate a Derived Figure

```bash
python scripts/make_shenzhen_histogram.py
```

## Data Boundary

Raw third-party geospatial data are not redistributed. Source links are provided in `DATASETS_AND_LINKS.csv`; derived non-sensitive summaries and manuscript figures are included for auditability.
