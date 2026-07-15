# Data contents

## `derived/`

This folder contains the machine-readable Supplementary Tables S1–S21 used in the manuscript and supplement.

Key groups are:

- S1–S3: contextual indicators, ERA5 derivation, and domain construction;
- S4–S7: wetness-score robustness and model sensitivity;
- S8–S10: threshold and alternative SDI–year model sensitivity;
- S11–S18: population scale, country groups, contextual patterns, and representative country profiles;
- S19–S20: uncertainty-width and restricted-sample sensitivity for under-5 incidence;
- S21: HAP-PM and SDI model diagnostics.

The files use the final threshold-corrected S9 and S10 results. For 2023 under-5 incidence, each alternative SDI–year model uses the same 203-country upper-tertile rules for the estimated-rate and positive-residual sets.

## `figure_source/`

This folder contains the data used to assemble Figures 1–4 and Supplementary Figures S3–S4. The final figures were adjusted in Adobe Illustrator; therefore, display labels may differ from legacy internal column names retained in some source CSVs.

Examples:

- `double_high` means high estimated rate plus a large positive SDI–year residual;
- `benchmark_aligned_high_burden` means high estimated rate only;
- `excess_only` in legacy source columns means large positive residual only;
- `severe_only_n` in legacy source columns means mortality-related-only.

These legacy names are retained only to preserve source-data lineage. Manuscript text and final figures use the current residual terminology.

## Units and definitions

- Rates are generally reported per 100,000 population.
- Population and estimated event numbers are in their native count units.
- SDI ranges from 0 to 1.
- The SDI–year residual is the GBD-estimated rate minus the fitted SDI–year rate.
- A large positive residual is positive and in the upper tertile of residuals within the relevant age-outcome-year stratum.
- High estimated rate is the upper tertile of GBD-estimated rates within the relevant stratum.
- Empty simulation fields for YLLs indicate that corresponding simulation outputs were unavailable, not zero.

## Original data

The repository does not redistribute the full original datasets. Obtain original inputs from their providers, including IHME/GBD, Copernicus/ERA5, WorldPop, World Bank, WHO, and Natural Earth. See `../docs/data_sources.md`.
