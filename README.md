# Building-footprint proxy benchmark for carbon-stock screening

This repository contains the public no-raw-data reproducibility package for the manuscript:

**A source-audited uncertainty benchmark for urban carbon-stock screening with open building-footprint change proxies**

## What Is Included

- Source registry and dataset links.
- Derived Shenzhen demonstrator summary tables, including the full 76,042-row proxy-inventory aggregate and a deterministic hash-ordered 8,000-row sample aggregate.
- Manuscript figures generated from non-sensitive outputs.
- Small validation and plotting scripts.
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
