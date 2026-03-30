"""
Data loading utilities. Downloads from GitHub Releases when running in Colab
or when local files aren't present.
"""

from pathlib import Path

import pandas as pd

RELEASE_BASE = "https://github.com/jsdrews/coffee-data/releases/download/v0.1.0-data"

DATA_FILES = {
    "cqi": "df_arabica_clean.csv",
    "coe": "cup_of_excellence.csv",
    "nasa": "nasa_power_example.csv",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCAL_DATA = PROJECT_ROOT / "data" / "raw"


def _resolve_path(name: str) -> str:
    """Return local path if it exists, otherwise the GitHub release URL."""
    local = LOCAL_DATA / DATA_FILES[name]
    if local.exists():
        return str(local)
    return f"{RELEASE_BASE}/{DATA_FILES[name]}"


def load_cqi() -> pd.DataFrame:
    """Load and clean the CQI Arabica dataset."""
    df = pd.read_csv(_resolve_path("cqi"))
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
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
