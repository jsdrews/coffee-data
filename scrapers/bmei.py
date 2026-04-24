"""
Pull reference data for the BMEI bioinput program at Nogales.

Fetches three datasets:
  1. SoilGrids soil properties for Bruselas, Huila (1.85°N, 76.08°W)
  2. NASA POWER monthly climate for Bruselas (2018–2025)
  3. PubChem compound properties for key Bacillus lipopeptides
     (surfactin, iturin A, fengycin, beauvericin)
"""

import time
from pathlib import Path

import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"

# Output files
SOIL_PATH = OUTPUT_DIR / "bmei_bruselas_soil.csv"
CLIMATE_PATH = OUTPUT_DIR / "bmei_bruselas_climate.csv"
LIPOPEPTIDES_PATH = OUTPUT_DIR / "bmei_lipopeptide_properties.csv"

# ── Bruselas coordinates ────────────────────────────────────────────────────
LAT = 1.85
LON = -76.08

# ── SoilGrids ───────────────────────────────────────────────────────────────
SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"

SOIL_PROPERTIES = ["phh2o", "ocd", "clay", "sand", "silt", "nitrogen", "cec", "soc"]
SOIL_DEPTHS = ["0-5cm", "5-15cm", "15-30cm", "30-60cm"]

HEADERS = {
    "User-Agent": "CoffeeDataResearch/0.1 (academic research project)"
}


def fetch_bruselas_soil() -> pd.DataFrame:
    """Fetch SoilGrids soil data for Bruselas coordinates."""
    # Fetch each property individually for reliability
    all_records = []
    for prop in SOIL_PROPERTIES:
        params = [
            ("lon", LON),
            ("lat", LAT),
            ("value", "mean"),
            ("property", prop),
        ]
        for depth in SOIL_DEPTHS:
            params.append(("depth", depth))

        print(f"  Fetching {prop}...")
        for attempt in range(3):
            try:
                resp = requests.get(
                    SOILGRIDS_URL, params=params, headers=HEADERS, timeout=30
                )
                resp.raise_for_status()
                data = resp.json()
                for layer in data["properties"]["layers"]:
                    unit = layer.get("unit_measure", {}).get("mapped_units", "")
                    for depth_info in layer["depths"]:
                        mean_val = depth_info.get("values", {}).get("mean")
                        all_records.append({
                            "property": prop,
                            "depth": depth_info["label"],
                            "value": mean_val,
                            "unit": unit,
                        })
                break
            except Exception as e:
                if attempt < 2:
                    print(f"    Retry {attempt + 1}...")
                    time.sleep(2)
                else:
                    print(f"    Failed: {e}")

    if not all_records:
        print("  WARNING: No soil data retrieved")
        return pd.DataFrame()

    data = None  # clear for reuse below
    df = pd.DataFrame(all_records)

    # Convert SoilGrids integer-scaled values to real units
    # pH is stored as pH * 10
    df.loc[df["property"] == "phh2o", "value"] = (
        df.loc[df["property"] == "phh2o", "value"] / 10.0
    )

    # Add human-readable names
    name_map = {
        "phh2o": "pH (H₂O)",
        "ocd": "Organic Carbon Density (hg/m³)",
        "clay": "Clay Content (g/kg)",
        "sand": "Sand Content (g/kg)",
        "silt": "Silt Content (g/kg)",
        "nitrogen": "Total Nitrogen (cg/kg)",
        "cec": "Cation Exchange Capacity (mmol(c)/kg)",
        "soc": "Soil Organic Carbon (dg/kg)",
    }
    df["property_name"] = df["property"].map(name_map)

    print(f"  → {len(df)} soil records")
    return df


# ── NASA POWER ──────────────────────────────────────────────────────────────
POWER_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"

CLIMATE_PARAMS = [
    "T2M",              # Mean temperature (°C)
    "T2M_MAX",          # Max temperature (°C)
    "T2M_MIN",          # Min temperature (°C)
    "T2M_RANGE",        # Diurnal temperature range (°C)
    "RH2M",             # Relative humidity (%)
    "PRECTOTCORR",      # Precipitation (mm/day)
    "ALLSKY_SFC_SW_DWN",  # Solar radiation (MJ/m²/day)
]


def fetch_bruselas_climate() -> pd.DataFrame:
    """Fetch monthly climate data for Bruselas from NASA POWER."""
    query = {
        "parameters": ",".join(CLIMATE_PARAMS),
        "community": "AG",
        "longitude": LON,
        "latitude": LAT,
        "start": 2018,
        "end": 2025,
        "format": "JSON",
    }

    print(f"  Fetching NASA POWER for ({LAT}, {LON})...")
    resp = requests.get(POWER_URL, params=query, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    records = []
    param_data = data["properties"]["parameter"]
    for param_name, monthly_values in param_data.items():
        for month_key, value in monthly_values.items():
            if value == -999.0:  # NASA POWER missing data marker
                continue
            records.append({
                "year": int(month_key[:4]),
                "month": int(month_key[4:]),
                "parameter": param_name,
                "value": value,
            })

    df = pd.DataFrame(records)
    print(f"  → {len(df)} climate records ({df['year'].min()}–{df['year'].max()})")
    return df


# ── PubChem lipopeptides ────────────────────────────────────────────────────
PUG_REST = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

# Bacillus lipopeptide antibiotics + Beauveria metabolite
LIPOPEPTIDE_COMPOUNDS = {
    "surfactin": 443592,       # Surfactin — Bacillus subtilis
    "iturin_a": 6437066,       # Iturin A — Bacillus amyloliquefaciens
    "fengycin": 101099318,     # Fengycin — Bacillus subtilis
    "beauvericin": 105014,     # Beauvericin — Beauveria bassiana
}

PROPERTY_LIST = (
    "IUPACName,MolecularFormula,MolecularWeight,XLogP,TPSA,"
    "HBondDonorCount,HBondAcceptorCount,RotatableBondCount,"
    "ExactMass,MonoisotopicMass"
)


def fetch_lipopeptide_properties() -> pd.DataFrame:
    """Fetch molecular properties for lipopeptide compounds from PubChem."""
    all_props = []

    for name, cid in LIPOPEPTIDE_COMPOUNDS.items():
        url = f"{PUG_REST}/compound/cid/{cid}/property/{PROPERTY_LIST}/JSON"
        print(f"  {name} (CID {cid})...")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            props = resp.json()["PropertyTable"]["Properties"][0]
            props["compound_name"] = name
            all_props.append(props)
        except Exception as e:
            print(f"    Warning: {e}")
        time.sleep(0.3)

    df = pd.DataFrame(all_props)
    if not df.empty:
        cols = ["compound_name", "CID"] + [c for c in df.columns if c not in ("compound_name", "CID")]
        df = df[cols]

    print(f"  → {len(df)} compounds")
    return df


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Fetching Bruselas soil data (SoilGrids)...")
    try:
        soil_df = fetch_bruselas_soil()
        soil_df.to_csv(SOIL_PATH, index=False)
        print(f"Saved to {SOIL_PATH}\n")
    except Exception as e:
        print(f"Soil fetch failed: {e}\n")

    print("Fetching Bruselas climate data (NASA POWER)...")
    try:
        climate_df = fetch_bruselas_climate()
        climate_df.to_csv(CLIMATE_PATH, index=False)
        print(f"Saved to {CLIMATE_PATH}\n")
    except Exception as e:
        print(f"Climate fetch failed: {e}\n")

    print("Fetching lipopeptide properties (PubChem)...")
    try:
        lipo_df = fetch_lipopeptide_properties()
        lipo_df.to_csv(LIPOPEPTIDES_PATH, index=False)
        print(f"Saved to {LIPOPEPTIDES_PATH}\n")
    except Exception as e:
        print(f"Lipopeptide fetch failed: {e}\n")

    print("Done.")


if __name__ == "__main__":
    main()
