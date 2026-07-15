# Data sources

The repository contains derived analysis tables. Original datasets should be obtained from their providers under the applicable access and licensing terms.

## IHME Global Burden of Disease 2023

Used for:

- LRI incidence;
- deaths;
- DALYs;
- YLLs;
- uncertainty intervals;
- Socio-demographic Index;
- household-air-pollution PM2.5 and other selected risk/context indicators.

The country-level GBD estimates are modelled outputs assembled from heterogeneous source data. They are not uniformly observed surveillance counts.

## ERA5

Copernicus Climate Change Service ERA5 reanalysis was used for temperature, dewpoint temperature, precipitation, and derived humidity and threshold-day indicators. Supplementary Table S2 records the climate-variable derivations.

## WorldPop

Gridded population data were used to aggregate climate indicators and describe population at risk. The full raster products are not redistributed in this repository.

## World Bank World Development Indicators

Used for selected country-level socioeconomic, service, and infrastructure indicators.

## World Health Organization

Used for selected vaccination, health-system, WASH, and disease-context indicators where applicable.

## Natural Earth

Country boundary data were used for map rendering. Boundary files are not redistributed here; plotting software can obtain them from Natural Earth or through supported geospatial libraries.

## Version and variable details

The detailed source, transformation, direction, and coverage for each contextual indicator are provided in:

- `data/derived/table_s1_contextual_indicator_dictionary.csv`
- `data/derived/table_s2_era5_climate_derivation.csv`
- `data/derived/table_s3_contextual_domain_construction.csv`

## Redistribution boundary

Only derived, analysis-ready tables needed to check the manuscript results are included. Users reconstructing the full pipeline must download the original data independently and comply with the providers' terms.
