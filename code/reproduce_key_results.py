from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import pandas as pd

from config import DERIVED_DIR, FIGURE_SOURCE_DIR, OUTPUT_DIR


def as_float(value):
    if pd.isna(value):
        return None
    return float(value)


def as_int(value):
    if pd.isna(value):
        return None
    return int(value)


def incidence_rate_residual_summary() -> dict:
    df = pd.read_csv(FIGURE_SOURCE_DIR / "figure1_profile_counts_2023.csv")
    df = df[df["outcome"].eq("Incidence")].set_index("age_group")
    out = {}
    for age in ["u5", "70p"]:
        row = df.loc[age]
        out[age] = {
            "n_locations": as_int(row["n_locations"]),
            "high_rate_and_large_positive_residual": as_int(row["double_high"]),
            "high_rate_only": as_int(row["benchmark_aligned_high_burden"]),
            "large_positive_residual_only": as_int(row["excess_only"]),
            "neither": as_int(row["neither"]),
            "spearman_rate_vs_residual": as_float(row["observed_vs_residual_spearman"]),
            "jaccard_upper_tertile_sets": as_float(row["high_observed_vs_high_excess_jaccard"]),
        }
    return out


def incidence_mortality_overlap_summary() -> list[dict]:
    df = pd.read_csv(FIGURE_SOURCE_DIR / "figure2_overlap_and_jaccard.csv")
    records = []
    for _, row in df.iterrows():
        records.append(
            {
                "age_group": row["age_group"],
                "mortality_related_outcome": row["severe_outcome"],
                "shared": as_int(row["shared_n"]),
                "incidence_only": as_int(row["incidence_only_n"]),
                "mortality_related_only": as_int(row["severe_only_n"]),
                "jaccard": as_float(row["jaccard"]),
            }
        )
    return records


def alternative_model_summary() -> dict:
    s9 = pd.read_csv(DERIVED_DIR / "table_s9_benchmark_variant_sensitivity_under5_incidence.csv")
    s10 = pd.read_csv(DERIVED_DIR / "table_s10_country_benchmark_stability_under5_2023.csv")
    primary = s10[s10["primary_high_deviation"].astype(bool)].copy()
    return {
        "model_variants": [
            {
                "benchmark_variant": row["benchmark_variant"],
                "n_locations": as_int(row["n_locations"]),
                "high_estimated_rate_n": as_int(row["high_estimated_rate_n"]),
                "large_positive_residual_n": as_int(row["large_positive_residual_n"]),
                "high_rate_and_large_positive_residual_n": as_int(row["double_high_n"]),
            }
            for _, row in s9.iterrows()
        ],
        "primary_large_positive_residual_n": int(len(primary)),
        "retained_in_at_least_6_of_8_models": int((primary["n_large_positive_residual_across_benchmarks"] >= 6).sum()),
        "retained_in_all_8_models": int((primary["n_large_positive_residual_across_benchmarks"] == 8).sum()),
    }


def population_and_support_summary() -> list[dict]:
    df = pd.read_csv(DERIVED_DIR / "table_s12_population_scale_endpoint_consistency_classification_support.csv")
    records = []
    for _, row in df.sort_values(["age_group", "outcome"]).iterrows():
        records.append(
            {
                "age_group": row["age_group"],
                "outcome": row["outcome"],
                "high_residual_countries": as_int(row["high_deviation_countries"]),
                "estimated_minus_fitted_number": as_float(row["benchmark_relative_number_difference"]),
                "same_group_2000_2023_share": as_float(row["same_endpoint_profile_share"]),
                "simulation_support_ge_0_8_share": as_float(row["p_high_deviation_ge_0_8_share"]),
            }
        )
    return records


def restricted_sample_summary() -> list[dict]:
    df = pd.read_csv(DERIVED_DIR / "table_s20_under5_incidence_support_sensitivity.csv")
    wanted = [
        ("full_sample", "fixed full-sample benchmark"),
        ("population_500k", "restricted-refit benchmark"),
        ("ui80", "restricted-refit benchmark"),
        ("joint_pop500_ui80", "restricted-refit benchmark"),
    ]
    records = []
    for scenario_id, mode in wanted:
        hit = df[df["scenario_id"].eq(scenario_id) & df["benchmark_mode"].eq(mode)]
        if hit.empty:
            continue
        row = hit.iloc[0]
        records.append(
            {
                "scenario_id": scenario_id,
                "scenario": row["scenario"],
                "benchmark_mode": mode,
                "eligible_n": as_int(row["eligible_n"]),
                "spearman_rate_vs_residual": as_float(row["spearman_rho_observed_vs_deviation"]),
                "jaccard_rate_vs_residual": as_float(row["jaccard_observed_vs_deviation"]),
                "eligible_retention": as_float(row["eligible_retention_proportion"]),
                "overall_retention": as_float(row["overall_retention_proportion"]),
            }
        )
    return records


def hap_sdi_summary() -> list[dict]:
    df = pd.read_csv(DERIVED_DIR / "table_s21_hap_sdi_model_diagnostics.csv")
    wanted = df[
        df["Model"].isin(["HAP only", "+ year fixed effects", "+ linear SDI", "Official M3 spline"])
    ].copy()
    return wanted.to_dict(orient="records")


def build_summary() -> dict:
    return {
        "incidence_rate_residual_2023": incidence_rate_residual_summary(),
        "incidence_mortality_related_overlap_2023": incidence_mortality_overlap_summary(),
        "alternative_sdi_year_models": alternative_model_summary(),
        "population_and_support": population_and_support_summary(),
        "under5_incidence_restricted_samples": restricted_sample_summary(),
        "hap_sdi_diagnostics": hap_sdi_summary(),
    }


def write_markdown(summary: dict, path: Path) -> None:
    u5 = summary["incidence_rate_residual_2023"]["u5"]
    old = summary["incidence_rate_residual_2023"]["70p"]
    alt = summary["alternative_sdi_year_models"]
    lines = [
        "# Reproduced key results",
        "",
        "## Estimated incidence rate and SDI–year residual",
        "",
        f"- Under-5: Spearman rho = {u5['spearman_rate_vs_residual']:.3f}; Jaccard = {u5['jaccard_upper_tertile_sets']:.3f}; groups = {u5['high_rate_and_large_positive_residual']}/{u5['high_rate_only']}/{u5['large_positive_residual_only']}/{u5['neither']}.",
        f"- Age 70+: Spearman rho = {old['spearman_rate_vs_residual']:.3f}; Jaccard = {old['jaccard_upper_tertile_sets']:.3f}; groups = {old['high_rate_and_large_positive_residual']}/{old['high_rate_only']}/{old['large_positive_residual_only']}/{old['neither']}.",
        "",
        "## Alternative SDI–year models",
        "",
        f"- Primary large-positive-residual countries: {alt['primary_large_positive_residual_n']}.",
        f"- Retained in at least 6 of 8 model variants: {alt['retained_in_at_least_6_of_8_models']}.",
        f"- Retained in all 8 model variants: {alt['retained_in_all_8_models']}.",
        "",
        "## Restricted-sample under-5 incidence results",
        "",
    ]
    for row in summary["under5_incidence_restricted_samples"]:
        lines.append(
            f"- {row['scenario']} ({row['benchmark_mode']}): rho = {row['spearman_rate_vs_residual']:.3f}, Jaccard = {row['jaccard_rate_vs_residual']:.3f}, eligible retention = {row['eligible_retention']:.3f}."
        )
    lines += [
        "",
        "The complete machine-readable values are in `key_results_summary.json` and the source CSV files.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    summary = build_summary()
    json_path = OUTPUT_DIR / "key_results_summary.json"
    md_path = OUTPUT_DIR / "key_results_summary.md"
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(summary, md_path)
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
