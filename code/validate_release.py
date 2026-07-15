from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import pandas as pd

from config import DERIVED_DIR, FIGURE_SOURCE_DIR, FIGURES_DIR, OUTPUT_DIR, REPOSITORY_ROOT

EXPECTED_DERIVED = 21
EXPECTED_FIGURE_SOURCE = 14
EXPECTED_MAIN_FIGURES = {
    "Figure1_final.jpeg",
    "Figure2_final.jpeg",
    "Figure3_final.jpeg",
    "Figure4_final.jpeg",
}
EXPECTED_SUPPLEMENTARY = {
    "SupplementaryFigureS1_corrected.jpeg",
    "SupplementaryFigureS1_corrected.pdf",
    "SupplementaryFigureS1_corrected.svg",
    "SupplementaryFigureS2_final.jpeg",
    "SupplementaryFigureS3_final.jpeg",
    "SupplementaryFigureS4_final.jpeg",
}
EXPECTED_EDITABLE = {"Figure1.ai", "Figure2.ai", "Figure3.ai", "Figure4.ai"}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".yml", ".yaml", ".cff", ".json", ".csv"}
FORBIDDEN_NAMES = {"__pycache__", ".pytest_cache", ".ipynb_checkpoints"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".docx", ".doc", ".tmp"}
ABSOLUTE_PATH_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    errors = []
    for encoding in ["utf-8-sig", "utf-8", "cp1252", "latin1"]:
        try:
            return pd.read_csv(path, encoding=encoding)
        except Exception as exc:  # pragma: no cover - used for release QA
            errors.append(f"{encoding}: {exc}")
    raise RuntimeError(f"Could not read {path}: {' | '.join(errors)}")


def scan_paths() -> dict:
    bad_names = []
    bad_suffixes = []
    local_paths = []
    for path in REPOSITORY_ROOT.rglob("*"):
        rel = path.relative_to(REPOSITORY_ROOT).as_posix()
        if any(part in FORBIDDEN_NAMES for part in path.parts):
            bad_names.append(rel)
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            bad_suffixes.append(rel)
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if rel in {"outputs/validation_summary.json", "outputs/release_manifest_sha256.csv"}:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            text = path.read_text(encoding="latin1")
        if ABSOLUTE_PATH_RE.search(text):
            local_paths.append(rel)
    return {
        "forbidden_directory_hits": sorted(set(bad_names)),
        "forbidden_file_hits": sorted(set(bad_suffixes)),
        "absolute_path_hits": sorted(set(local_paths)),
    }


def validate_corrected_tables() -> dict:
    s9 = read_csv(DERIVED_DIR / "table_s9_benchmark_variant_sensitivity_under5_incidence.csv")
    s10 = read_csv(DERIVED_DIR / "table_s10_country_benchmark_stability_under5_2023.csv")
    lowess = s9.loc[s9["benchmark_variant"].eq("lowess_year_frac035")].iloc[0]
    quintile = s9.loc[s9["benchmark_variant"].eq("sdi_quintile_year_median")].iloc[0]
    primary = s10[s10["primary_high_deviation"].astype(bool)]
    return {
        "all_s9_models_use_203_locations": bool(s9["n_locations"].eq(203).all()),
        "all_s9_models_have_68_high_estimated_rate": bool(s9["high_estimated_rate_n"].eq(68).all()),
        "all_s9_models_have_68_large_positive_residual": bool(s9["large_positive_residual_n"].eq(68).all()),
        "lowess_double_high_n": int(lowess["double_high_n"]),
        "sdi_quintile_double_high_n": int(quintile["double_high_n"]),
        "primary_large_positive_residual_n": int(len(primary)),
        "primary_retained_at_least_6_of_8": int((primary["n_large_positive_residual_across_benchmarks"] >= 6).sum()),
        "primary_retained_all_8": int((primary["n_large_positive_residual_across_benchmarks"] == 8).sum()),
    }


def build_manifest() -> list[dict]:
    records = []
    for path in sorted(p for p in REPOSITORY_ROOT.rglob("*") if p.is_file()):
        rel = path.relative_to(REPOSITORY_ROOT).as_posix()
        if rel in {"outputs/validation_summary.json", "outputs/release_manifest_sha256.csv"}:
            continue
        records.append(
            {
                "path": rel,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return records


def main() -> None:
    derived = sorted(DERIVED_DIR.glob("*.csv"))
    figure_source = sorted(FIGURE_SOURCE_DIR.glob("*.csv"))
    csv_results = {}
    for path in derived + figure_source:
        df = read_csv(path)
        csv_results[path.relative_to(REPOSITORY_ROOT).as_posix()] = {
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
        }

    main_figures = {p.name for p in (FIGURES_DIR / "main").iterdir() if p.is_file()}
    supplementary = {p.name for p in (FIGURES_DIR / "supplementary").iterdir() if p.is_file()}
    editable = {p.name for p in (FIGURES_DIR / "editable").iterdir() if p.is_file()}
    scans = scan_paths()
    corrected = validate_corrected_tables()

    checks = {
        "derived_csv_count_21": len(derived) == EXPECTED_DERIVED,
        "figure_source_csv_count_14": len(figure_source) == EXPECTED_FIGURE_SOURCE,
        "all_csv_files_readable": len(csv_results) == EXPECTED_DERIVED + EXPECTED_FIGURE_SOURCE,
        "main_figures_complete": EXPECTED_MAIN_FIGURES.issubset(main_figures),
        "supplementary_figures_complete": EXPECTED_SUPPLEMENTARY.issubset(supplementary),
        "editable_figures_complete": EXPECTED_EDITABLE.issubset(editable),
        "all_figure_files_nonempty": all(
            p.stat().st_size > 0
            for folder in [FIGURES_DIR / "main", FIGURES_DIR / "supplementary", FIGURES_DIR / "editable"]
            for p in folder.iterdir()
            if p.is_file()
        ),
        "no_forbidden_directories": not scans["forbidden_directory_hits"],
        "no_forbidden_files": not scans["forbidden_file_hits"],
        "no_local_absolute_paths": not scans["absolute_path_hits"],
        "s9_uses_common_203_location_scope": corrected["all_s9_models_use_203_locations"],
        "s9_all_rate_sets_n68": corrected["all_s9_models_have_68_high_estimated_rate"],
        "s9_all_residual_sets_n68": corrected["all_s9_models_have_68_large_positive_residual"],
        "s9_lowess_double_high_n43": corrected["lowess_double_high_n"] == 43,
        "s9_quintile_double_high_n37": corrected["sdi_quintile_double_high_n"] == 37,
        "s10_primary_n68": corrected["primary_large_positive_residual_n"] == 68,
        "s10_retained_ge6_n66": corrected["primary_retained_at_least_6_of_8"] == 66,
        "s10_retained_all8_n43": corrected["primary_retained_all_8"] == 43,
    }
    checks["all_checks_pass"] = all(checks.values())

    manifest = build_manifest()
    manifest_path = OUTPUT_DIR / "release_manifest_sha256.csv"
    with manifest_path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=["path", "size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(manifest)

    summary = {
        "repository_root": ".",
        "checks": checks,
        "counts": {
            "derived_csv": len(derived),
            "figure_source_csv": len(figure_source),
            "main_figure_files": len(main_figures),
            "supplementary_figure_files": len(supplementary),
            "editable_figure_files": len(editable),
            "manifest_files": len(manifest),
        },
        "corrected_benchmark_results": corrected,
        "scan_results": scans,
        "csv_dimensions": csv_results,
    }
    out = OUTPUT_DIR / "validation_summary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not checks["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
