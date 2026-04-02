"""
Pull PubChem bioassay data for key coffee bioactive compounds.
https://pubchem.ncbi.nlm.nih.gov

Uses PUG REST API to fetch:
  1. Compound properties (molecular weight, formula, LogP, etc.)
  2. Bioassay summaries (activity outcomes, assay descriptions)

Target compounds:
  - Chlorogenic acid (CID 1794427)
  - Cafestol (CID 108052)
  - Kahweol (CID 114778)
  - Trigonelline (CID 5570)
  - Caffeine (CID 2519)
"""

import time
from pathlib import Path

import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
PROPERTIES_PATH = OUTPUT_DIR / "pubchem_properties.csv"
BIOASSAYS_PATH = OUTPUT_DIR / "pubchem_coffee_bioassays.csv"

PUG_REST = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

HEADERS = {
    "User-Agent": "CoffeeDataResearch/0.1 (academic research project)"
}

COMPOUNDS = {
    "chlorogenic_acid": 1794427,
    "cafestol": 108052,
    "kahweol": 114778,
    "trigonelline": 5570,
    "caffeine": 2519,
}

# Properties to fetch for each compound
PROPERTY_LIST = (
    "IUPACName,MolecularFormula,MolecularWeight,XLogP,TPSA,"
    "HBondDonorCount,HBondAcceptorCount,RotatableBondCount,"
    "ExactMass,MonoisotopicMass"
)

# Bioassay column headers (from PubChem API)
BIOASSAY_COLUMNS = [
    "aid", "panel_member_id", "sid", "cid", "activity_outcome",
    "activity_score", "activity_url", "assay_url", "target_name",
    "assay_name", "assay_type", "target_gi", "target_gene_id",
]


def fetch_properties() -> pd.DataFrame:
    """Fetch molecular properties for all target compounds."""
    cids = ",".join(str(cid) for cid in COMPOUNDS.values())
    url = f"{PUG_REST}/compound/cid/{cids}/property/{PROPERTY_LIST}/JSON"

    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    props = r.json()["PropertyTable"]["Properties"]
    df = pd.DataFrame(props)

    # Add compound name column
    cid_to_name = {cid: name for name, cid in COMPOUNDS.items()}
    df["compound_name"] = df["CID"].map(cid_to_name)

    # Reorder columns
    cols = ["compound_name", "CID"] + [c for c in df.columns if c not in ("compound_name", "CID")]
    return df[cols]


def fetch_bioassays(cid: int, compound_name: str) -> pd.DataFrame:
    """Fetch bioassay summary for a single compound."""
    url = f"{PUG_REST}/compound/cid/{cid}/assaysummary/JSON"
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()

    table = r.json().get("Table", {})
    columns = table.get("Columns", {}).get("Column", [])
    rows_raw = table.get("Row", [])

    rows = []
    for row in rows_raw:
        cells = row.get("Cell", [])
        # Pad/truncate to match expected columns
        if len(cells) < len(columns):
            cells.extend([""] * (len(columns) - len(cells)))
        elif len(cells) > len(columns):
            cells = cells[:len(columns)]
        rows.append(cells)

    df = pd.DataFrame(rows, columns=BIOASSAY_COLUMNS[:len(columns)])
    df["compound_name"] = compound_name
    return df


def scrape_all():
    """Fetch properties and bioassays for all target compounds."""
    print("Fetching compound properties...")
    props_df = fetch_properties()
    print(f"  → {len(props_df)} compounds")

    print("\nFetching bioassay summaries...")
    bioassay_dfs = []
    for name, cid in COMPOUNDS.items():
        print(f"  {name} (CID {cid})...")
        df = fetch_bioassays(cid, name)
        print(f"    → {len(df)} assay results")
        bioassay_dfs.append(df)
        time.sleep(0.5)  # respect rate limits

    bioassays_df = pd.concat(bioassay_dfs, ignore_index=True)

    # Filter to active results for a more useful dataset
    active_df = bioassays_df[bioassays_df["activity_outcome"] == "Active"].copy()
    print(f"\n  Total: {len(bioassays_df)} results ({len(active_df)} active)")

    return props_df, bioassays_df


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    props_df, bioassays_df = scrape_all()

    props_df.to_csv(PROPERTIES_PATH, index=False)
    print(f"\nSaved properties to {PROPERTIES_PATH}")

    bioassays_df.to_csv(BIOASSAYS_PATH, index=False)
    print(f"Saved {len(bioassays_df)} bioassay rows to {BIOASSAYS_PATH}")

    print("\nActive results per compound:")
    active = bioassays_df[bioassays_df["activity_outcome"] == "Active"]
    print(active.groupby("compound_name").size().to_string())
