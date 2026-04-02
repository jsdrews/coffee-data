"""
Pull bioactivity data from ChEMBL for key coffee compounds.
https://www.ebi.ac.uk/chembl/

Uses the ChEMBL REST API to fetch activity measurements (IC50, EC50, Ki, etc.)
for target compounds against protein targets.

Target compounds:
  - Chlorogenic acid (CHEMBL284616)
  - Cafestol (CHEMBL1407645)
  - Kahweol (CHEMBL1494598)
  - Trigonelline (CHEMBL350675)
  - Caffeine (CHEMBL113)
"""

import time
from pathlib import Path

import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "chembl_coffee_bioactivity.csv"

API_BASE = "https://www.ebi.ac.uk/chembl/api/data"

HEADERS = {
    "User-Agent": "CoffeeDataResearch/0.1 (academic research project)"
}

COMPOUNDS = {
    "chlorogenic_acid": "CHEMBL284616",
    "cafestol": "CHEMBL1407645",
    "kahweol": "CHEMBL1494598",
    "trigonelline": "CHEMBL350675",
    "caffeine": "CHEMBL113",
}

# Fields to extract from each activity record
ACTIVITY_FIELDS = [
    "activity_id",
    "molecule_chembl_id",
    "target_chembl_id",
    "target_pref_name",
    "target_organism",
    "type",
    "value",
    "units",
    "relation",
    "standard_type",
    "standard_value",
    "standard_units",
    "standard_relation",
    "pchembl_value",
    "assay_chembl_id",
    "assay_type",
    "assay_description",
    "document_chembl_id",
]

PAGE_SIZE = 500


def fetch_activities(chembl_id: str, compound_name: str) -> list[dict]:
    """Fetch all bioactivity records for a compound, paginating through results."""
    all_activities = []
    offset = 0

    while True:
        url = (
            f"{API_BASE}/activity?"
            f"molecule_chembl_id={chembl_id}&format=json"
            f"&limit={PAGE_SIZE}&offset={offset}"
        )
        r = requests.get(url, headers=HEADERS, timeout=60)
        if r.status_code != 200:
            print(f"    Error {r.status_code} at offset {offset}")
            break

        data = r.json()
        activities = data.get("activities", [])
        if not activities:
            break

        for act in activities:
            row = {field: act.get(field) for field in ACTIVITY_FIELDS}
            row["compound_name"] = compound_name
            all_activities.append(row)

        total = data.get("page_meta", {}).get("total_count", 0)
        offset += PAGE_SIZE

        if offset >= total:
            break

        time.sleep(0.3)

    return all_activities


def scrape_all() -> pd.DataFrame:
    """Fetch bioactivity data for all target compounds."""
    all_rows: list[dict] = []

    for name, chembl_id in COMPOUNDS.items():
        print(f"  {name} ({chembl_id})...")
        activities = fetch_activities(chembl_id, name)
        print(f"    → {len(activities)} activity records")
        all_rows.extend(activities)
        time.sleep(0.5)

    df = pd.DataFrame(all_rows)

    if not df.empty:
        for col in ("value", "standard_value", "pchembl_value"):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    print("Fetching ChEMBL bioactivity data...")
    df = scrape_all()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved {len(df)} rows to {OUTPUT_PATH}")

    print("\nRecords per compound:")
    print(df.groupby("compound_name").size().to_string())

    if "standard_type" in df.columns:
        print("\nTop activity types:")
        print(df["standard_type"].value_counts().head(10).to_string())
