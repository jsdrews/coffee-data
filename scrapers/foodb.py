"""
Extract coffee compound data from FooDB bulk CSV download.
https://foodb.ca

The FooDB CSV dump (foodb_2020_4_7_csv.tar.gz) contains:
  - Food.csv: food entries with IDs
  - Compound.csv: compound identities, properties, and classifications
  - Content.csv: compound-food concentration measurements

This script downloads the dump (if not cached), extracts the three needed
files, filters for coffee entries, and joins compound names to content records.

Coffee food entries:
  - 58: Coffee (general)
  - 59: Arabica coffee
  - 60: Robusta coffee
  - 768: Coffee mocha
"""

import tarfile
from pathlib import Path

import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "foodb_coffee.csv"

DUMP_URL = "https://foodb.ca/public/system/downloads/foodb_2020_4_7_csv.tar.gz"
CACHE_PATH = Path("/tmp/foodb_csv.tar.gz")
EXTRACT_DIR = Path("/tmp/foodb_2020_04_07_csv")

HEADERS = {
    "User-Agent": "CoffeeDataResearch/0.1 (academic research project)"
}

COFFEE_FOOD_IDS = [58, 59, 60, 768]

NEEDED_FILES = [
    "foodb_2020_04_07_csv/Food.csv",
    "foodb_2020_04_07_csv/Compound.csv",
    "foodb_2020_04_07_csv/Content.csv",
]


def _download_dump():
    """Download the FooDB CSV dump if not already cached."""
    if CACHE_PATH.exists() and CACHE_PATH.stat().st_size > 500_000_000:
        print(f"  Using cached dump at {CACHE_PATH}")
        return

    print(f"  Downloading FooDB dump ({DUMP_URL})...")
    r = requests.get(DUMP_URL, headers=HEADERS, stream=True, timeout=300)
    r.raise_for_status()

    with open(CACHE_PATH, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"  Downloaded {CACHE_PATH.stat().st_size / 1e6:.0f} MB")


def _extract_files():
    """Extract needed CSV files from the tar.gz dump."""
    all_exist = all(
        (Path("/tmp") / name).exists() for name in NEEDED_FILES
    )
    if all_exist:
        print("  CSV files already extracted")
        return

    print("  Extracting CSV files...")
    with tarfile.open(CACHE_PATH, "r:gz") as tar:
        for name in NEEDED_FILES:
            try:
                tar.extract(name, path="/tmp")
            except KeyError:
                print(f"    Warning: {name} not found in archive")


def scrape_all() -> pd.DataFrame:
    """Extract coffee compound-concentration data from FooDB dump."""
    _download_dump()
    _extract_files()

    # Load food names
    foods = pd.read_csv(EXTRACT_DIR / "Food.csv", low_memory=False)
    food_names = dict(zip(foods["id"], foods["name"]))

    # Load compounds (only columns we need — full file is 49MB)
    compounds = pd.read_csv(
        EXTRACT_DIR / "Compound.csv",
        usecols=["id", "name", "moldb_mono_mass", "state",
                 "kingdom", "superklass", "klass", "subklass"],
        low_memory=False,
    )

    # Load content, filtering for coffee foods
    print("  Loading content (this takes a moment)...")
    chunks = pd.read_csv(EXTRACT_DIR / "Content.csv", chunksize=100_000, low_memory=False)
    coffee_content = []
    for chunk in chunks:
        matches = chunk[chunk["food_id"].isin(COFFEE_FOOD_IDS)]
        if len(matches):
            coffee_content.append(matches)

    content = pd.concat(coffee_content, ignore_index=True)
    print(f"  → {len(content)} coffee content records")

    # Join compound names
    content = content.merge(
        compounds.rename(columns={"id": "source_id", "name": "compound_name"}),
        on="source_id",
        how="left",
    )

    # Add food names
    content["food_name"] = content["food_id"].map(food_names)

    # Select and rename columns
    result = content[[
        "food_id", "food_name", "source_id", "compound_name",
        "orig_content", "orig_min", "orig_max", "orig_unit",
        "standard_content", "preparation_type",
        "kingdom", "superklass", "klass", "subklass",
        "orig_citation", "citation", "citation_type",
    ]].copy()

    result = result.rename(columns={
        "source_id": "compound_id",
        "orig_content": "content",
        "orig_min": "content_min",
        "orig_max": "content_max",
        "orig_unit": "unit",
    })

    # Convert numeric columns
    for col in ("content", "content_min", "content_max", "standard_content"):
        result[col] = pd.to_numeric(result[col], errors="coerce")

    return result


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    print("Extracting FooDB coffee data...")
    df = scrape_all()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved {len(df)} rows to {OUTPUT_PATH}")

    print(f"\nRecords per coffee type:")
    print(df.groupby("food_name").size().to_string())

    print(f"\nTop 15 compounds by record count:")
    print(df.groupby("compound_name").size().sort_values(ascending=False).head(15).to_string())

    print(f"\nCompound classes:")
    print(df["klass"].value_counts().head(10).to_string())
