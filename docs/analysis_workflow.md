# Analysis workflow

## 1. Outcomes and population groups

The analysis used GBD 2023 estimates for lower respiratory infection incidence, deaths, disability-adjusted life-years (DALYs), and years of life lost (YLLs) from 1990 to 2023. The primary age groups were children younger than 5 years and adults aged 70 years or older.

## 2. SDI–year model

For each age group and outcome, country-year rates were modelled as a nonlinear function of Socio-demographic Index (SDI) with calendar-year effects. The primary specification used a cubic B-spline for SDI and year fixed effects.

The SDI–year residual was calculated as:

> GBD-estimated rate minus fitted SDI–year rate.

## 3. Country groups

Within each age-outcome-year stratum:

- high estimated rate: upper tertile of GBD-estimated rates;
- large positive residual: positive residual in the upper tertile of residuals;
- high estimated rate plus large positive residual;
- high estimated rate only;
- large positive residual only; and
- neither.

The country groups are descriptive. They do not define national performance or preventable burden.

## 4. Incidence and mortality-related comparisons

Incidence large-positive-residual sets were compared with corresponding death, DALY, and YLL sets. Overlap was summarised with country counts and the Jaccard index. Rank agreement was summarised with Spearman correlation.

## 5. Population and uncertainty analyses

Interpretation of under-5 incidence groups was examined using:

- population-at-risk thresholds;
- agreement of country groups between 2000 and 2023;
- simulations based on marginal GBD uncertainty intervals;
- uncertainty-interval width restrictions; and
- fixed versus restricted-sample refitting of the SDI–year model.

Exclusion by an eligibility rule was separated from reclassification among countries that remained eligible.

## 6. Alternative SDI–year models

Alternative specifications included polynomial, spline, LOWESS, and SDI-quintile median models. The final corrected analysis applied the same 203-country upper-tertile classification rule to all model variants.

## 7. Contextual profiles

Environmental and health-system indicators were analysed after the country groups were defined. The contextual profiles are descriptive post-classification comparisons. They were not used to define the SDI–year residual or country groups.

## 8. HAP-PM and SDI diagnostics

The household-air-pollution PM2.5 (HAP-PM) analysis assessed why the coefficient changed sign after SDI adjustment. Diagnostics included:

- HAP-PM–SDI correlations;
- common-sample M1–M3 comparisons;
- alternative SDI functions;
- residualisation;
- collinearity diagnostics; and
- leave-one-country-out models.

The M3 estimate was interpreted as specification-dependent rather than as an independent or causal HAP-PM effect.

## 9. Figure production

The numerical results were produced in Python. Final multi-panel layouts were adjusted in Adobe Illustrator. The repository therefore contains:

- final manuscript figures;
- editable Illustrator files; and
- source tables underlying the figures.
