"""
Data loading utilities. Downloads from GitHub Releases when running in Colab
or when local files aren't present.
"""

from pathlib import Path

import pandas as pd

RELEASE_BASE = "https://github.com/jsdrews/coffee-data/releases/download/v0.1.0-data"

GITHUB_RAW = "https://raw.githubusercontent.com/jldbc/coffee-quality-database/master/data"

DATA_FILES = {
    "cqi": "arabica_data_cleaned.csv",
    "coe": "cup_of_excellence.csv",
    "nasa": "nasa_power_example.csv",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCAL_DATA = PROJECT_ROOT / "data" / "raw"


def _resolve_path(name: str) -> str:
    """Return local path if it exists, otherwise a remote URL."""
    local = LOCAL_DATA / DATA_FILES[name]
    if local.exists():
        return str(local)
    if name == "cqi":
        return f"{GITHUB_RAW}/{DATA_FILES[name]}"
    return f"{RELEASE_BASE}/{DATA_FILES[name]}"


def load_cqi() -> pd.DataFrame:
    """Load and clean the full CQI Arabica dataset (~1,300 samples)."""
    df = pd.read_csv(_resolve_path("cqi"))
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(".", "_", regex=False)
        .str.replace(" ", "_")
    )
    cupping_cols = [
        "aroma", "flavor", "aftertaste", "acidity", "body",
        "balance", "uniformity", "clean_cup", "sweetness",
    ]
    existing = [c for c in cupping_cols if c in df.columns]
    df = df.dropna(subset=existing, how="all")
    return df


def load_coe() -> pd.DataFrame:
    """Load Cup of Excellence data."""
    return pd.read_csv(_resolve_path("coe"))


def load_nasa() -> pd.DataFrame:
    """Load NASA POWER example data."""
    return pd.read_csv(_resolve_path("nasa"))
