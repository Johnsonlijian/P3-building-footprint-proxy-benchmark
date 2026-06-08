# Building-footprint proxy audit for urban carbon screening

This repository contains the public no-raw-data reproducibility package for the manuscript:

**Auditing open footprint proxies for urban carbon screening**

## What Is Included

- Source registry and dataset links.
- Derived Shenzhen demonstrator summary tables, including the full 76,042-row proxy-inventory aggregate and a deterministic hash-ordered 8,000-row sample aggregate.
- Manuscript figures generated from non-sensitive outputs.
- Small validation and plotting scripts.
- R02 vector figure outputs for the npj Urban Sustainability target revision: SVG/PDF/PNG for Figures 1-5.
- R02 derived benchmark, interval, stress-test, and Shenzhen proxy-summary tables.
- Runbook, citation metadata, and licence.

## Evidence Boundary

Open footprint disappearance is treated as a proxy signal. This repository does not provide field-verified removal labels, performance metrics, official inventory correction, or city-level carbon accounting.

## Quick Start

```bash
python scripts/validate_derived_outputs.py
```

## Repository URL

https://github.com/Johnsonlijian/P3-building-footprint-proxy-benchmark


## v22 Update

The package includes a full 76,042-row Shenzhen proxy inventory summary and a deterministic hash-ordered 8,000-row sample summary. Event-level proxy rows are not redistributed.


## v24 Update

The package now includes synthetic interval-validation diagnostics: 90% interval coverage, interval width, and interval score for 75 synthetic city-year aggregates.

## R02 npj Urban Sustainability Update

This local package adds the strongest current no-raw-data reproducibility layer for the target-journal revision:

- `scripts/r02/build_r02_figures_and_tables.py`
- `outputs/figures/r02_svg/`
- `outputs/figures/r02_pdf/`
- `outputs/figures/r02_png/`
- `outputs/derived_tables/r02/`

Active submission manuscripts, internal rejection-risk reviews, cover letters, response drafts, raw third-party data, and event-level Overture proxy rows are intentionally excluded.

The intended public remote remains:

https://github.com/Johnsonlijian/P3-building-footprint-proxy-benchmark

Pushing or publishing the refreshed package requires explicit author approval.
