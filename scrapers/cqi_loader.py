"""
Loader for the Coffee Quality Institute (CQI) dataset.

Download the CSV from Kaggle first:
https://www.kaggle.com/datasets/fatihb/coffee-quality-data-cqi

Place the file(s) in data/raw/ and use this script to load and clean them.
"""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = str(PROJECT_ROOT / "data" / "raw" / "df_arabica_clean.csv")


def load_cqi_data(path: str = RAW_PATH) -> pd.DataFrame:
    """Load and lightly clean the CQI Arabica dataset."""
    df = pd.read_csv(path)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Cupping score columns (for quick reference)
    cupping_cols = [
        "aroma", "flavor", "aftertaste", "acidity", "body",
        "balance", "uniformity", "clean_cup", "sweetness",
    ]

    # Drop rows missing all cupping scores
    existing_cupping = [c for c in cupping_cols if c in df.columns]
    df = df.dropna(subset=existing_cupping, how="all")

    return df


def summarize(df: pd.DataFrame) -> None:
    """Print a quick summary of the dataset."""
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nCountries: {df['country_of_origin'].nunique()}")
    print(df["country_of_origin"].value_counts().head(10))
    print(f"\nProcessing methods:")
    print(df["processing_method"].value_counts())


if __name__ == "__main__":
    df = load_cqi_data()
    summarize(df)
