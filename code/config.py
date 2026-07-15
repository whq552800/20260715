from __future__ import annotations

from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPOSITORY_ROOT / "data"
DERIVED_DIR = DATA_DIR / "derived"
FIGURE_SOURCE_DIR = DATA_DIR / "figure_source"
FIGURES_DIR = REPOSITORY_ROOT / "figures"
OUTPUT_DIR = REPOSITORY_ROOT / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
