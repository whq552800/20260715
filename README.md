# GBD-estimated LRI rates and SDI–year residuals

This repository contains the code, derived tables, figure source data, and final figure files for the manuscript:

**GBD-estimated rates and SDI–year residuals provide complementary views of national lower respiratory infection estimates: an ecological analysis of 203 countries and territories**

## Study scope

The analysis compares four related but non-equivalent views of lower respiratory infection (LRI) burden:

1. GBD-estimated rates;
2. residuals from a fitted SDI–year model;
3. incidence versus mortality-related outcomes; and
4. population size and sensitivity of country-group assignments.

The primary age groups are children younger than 5 years and adults aged 70 years or older. Outcomes include incidence, deaths, disability-adjusted life-years (DALYs), and years of life lost (YLLs), covering 1990–2023.

The SDI–year residual is defined as:

> GBD-estimated rate minus the rate fitted from SDI and calendar year.

It is a descriptive model residual. It is not a measure of national performance, preventable burden, attributable burden, or a causal counterfactual.

## Repository contents

```text
.
├── README.md
├── CITATION.cff
├── requirements.txt
├── environment.yml
├── code/
│   ├── README.md
│   ├── config.py
│   ├── reproduce_key_results.py
│   └── validate_release.py
├── data/
│   ├── README.md
│   ├── derived/
│   └── figure_source/
├── figures/
│   ├── main/
│   ├── supplementary/
│   └── editable/
└── docs/
    ├── analysis_workflow.md
    └── data_sources.md
```

## Reproducibility levels

### Level 1: verify the public release

```powershell
python code\validate_release.py
```

This checks the expected folder structure, reads all CSV files, verifies the final figures, scans the repository for local absolute paths and cache files, and creates `outputs/validation_summary.json`.

### Level 2: reproduce the main reported summary values from derived data

```powershell
python code\reproduce_key_results.py
```

This reads the machine-readable Supplementary Tables and figure source tables and creates `outputs/key_results_summary.json` and `outputs/key_results_summary.md`. The `outputs/` directory is generated locally and is not committed to the repository.

### Full upstream reconstruction

The repository provides analysis-ready derived data and portable verification scripts. Reconstructing the complete workflow from original source data requires downloading the relevant datasets from their providers and implementing the processing steps documented in `docs/analysis_workflow.md` and `docs/data_sources.md`.

## Data availability

The repository contains analysis-ready derived tables and figure source data. It does not redistribute the complete original GBD, ERA5, WorldPop, World Bank, WHO, or Natural Earth source datasets. Original data should be obtained from the relevant providers under their access and licensing terms.

See:

- `data/README.md`
- `docs/data_sources.md`
- Supplementary Table S1 in `data/derived/`

## Figures

- `figures/main/` contains the four final main-figure JPEG files used in the manuscript.
- `figures/supplementary/` contains the final supplementary figures.
- `figures/editable/` contains the Illustrator source files used for final layout.

The final Illustrator layout may differ slightly from direct Python rendering, while the underlying country classifications and numerical values are provided in `data/figure_source/`.

## Software

The analysis was developed in Python. The main dependencies are listed in `requirements.txt` and `environment.yml`.

## Citation

A citation template is provided in `CITATION.cff`. The article DOI and repository archive DOI should be added after publication and release archiving.

## Contact

Haiqing Wang  
University of Chinese Academy of Sciences / Northeast Institute of Geography and Agroecology, Chinese Academy of Sciences  
Email: wanghaiqing25@mails.ucas.ac.cn

## Release status

This directory contains the files intended for the public GitHub repository. Manuscript working files, local build scripts, provenance-only scripts, release-preparation checklists, and workstation-specific inventories are excluded from the public Git layer.
