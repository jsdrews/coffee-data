"""
Pull NASA POWER climate data for geocoded farm locations and merge with CQI data.

Fetches monthly temperature, humidity, and rainfall concurrently for each
unique coordinate, then filters to harvest-window months per country.
"""

import asyncio
import sys
from pathlib import Path

import aiohttp
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scrapers.nasa_power import CLIMATE_PARAMS
from scrapers.geocode import merge_coordinates
from utils.data import load_cqi
from utils.harvest import get_harvest_months

OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "cqi_with_climate.csv"
CLIMATE_CACHE = PROJECT_ROOT / "data" / "processed" / "climate_raw.csv"

API_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"
MAX_CONCURRENT = 10


async def fetch_one(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    lat: float,
    lon: float,
) -> list[dict]:
    """Fetch monthly climate data for a single coordinate."""
    params = {
        "parameters": ",".join(CLIMATE_PARAMS),
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": 2010,
        "end": 2023,
        "format": "JSON",
    }
    async with semaphore:
        try:
            async with session.get(
                API_URL, params=params, timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                if resp.status != 200:
                    print(f"  Error {resp.status} at ({lat}, {lon})")
                    return []
                data = await resp.json()
        except Exception as e:
            print(f"  Error at ({lat}, {lon}): {e}")
            return []

    records = []
    param_data = data["properties"]["parameter"]
    for param_name, monthly_values in param_data.items():
        for month_key, value in monthly_values.items():
            records.append({
                "year": int(month_key[:4]),
                "month": int(month_key[4:]),
                "parameter": param_name,
                "value": value,
                "lat": lat,
                "lon": lon,
            })
    return records


async def fetch_all_climate(coords: pd.DataFrame) -> pd.DataFrame:
    """Fetch NASA POWER data for all coordinates concurrently."""
    if CLIMATE_CACHE.exists():
        print(f"Loading cached climate data from {CLIMATE_CACHE}")
        return pd.read_csv(CLIMATE_CACHE)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    all_records = []
    total = len(coords)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _, row in coords.iterrows():
            lat = round(row["latitude"], 2)
            lon = round(row["longitude"], 2)
            tasks.append(fetch_one(session, semaphore, lat, lon))

        done = 0
        for coro in asyncio.as_completed(tasks):
            records = await coro
            all_records.extend(records)
            done += 1
            if done % 25 == 0:
                print(f"  [{done}/{total}] coordinates fetched...")

    result = pd.DataFrame(all_records) if all_records else pd.DataFrame()
    CLIMATE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(CLIMATE_CACHE, index=False)
    print(f"Cached {len(result)} climate records to {CLIMATE_CACHE}")
    return result


def aggregate_climate_by_location(
    climate: pd.DataFrame, df_with_coords: pd.DataFrame
) -> pd.DataFrame:
    """For each unique location, compute harvest-window climate averages."""
    locations = (
        df_with_coords[["country_of_origin", "latitude", "longitude"]]
        .dropna()
        .copy()
    )
    locations["lat_round"] = locations["latitude"].round(2)
    locations["lon_round"] = locations["longitude"].round(2)
    locations = locations.drop_duplicates(subset=["lat_round", "lon_round", "country_of_origin"])

    results = []
    for _, loc in locations.iterrows():
        country = loc["country_of_origin"]
        harvest = get_harvest_months(country)
        if harvest is None:
            continue

        lat, lon = loc["lat_round"], loc["lon_round"]
        coord_climate = climate[
            (climate["lat"] == lat)
            & (climate["lon"] == lon)
            & (climate["month"].isin(harvest))
        ]
        if coord_climate.empty:
            continue

        pivoted = coord_climate.pivot_table(
            index=["lat", "lon", "year"],
            columns="parameter",
            values="value",
        ).mean()

        record = pivoted.to_dict()
        record["lat_round"] = lat
        record["lon_round"] = lon
        results.append(record)

    return pd.DataFrame(results) if results else pd.DataFrame()


def main():
    df = load_cqi()

    geocoded = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "geocoded_regions.csv")
    df = merge_coordinates(df, geocoded)

    has_coords = df["latitude"].notna().sum()
    print(f"{has_coords}/{len(df)} coffees have coordinates")

    coords = (
        df[["latitude", "longitude"]]
        .dropna()
        .round(2)
        .drop_duplicates()
        .reset_index(drop=True)
    )
    print(f"{len(coords)} unique coordinates to fetch climate for")

    climate = asyncio.run(fetch_all_climate(coords))

    climate_by_loc = aggregate_climate_by_location(climate, df)
    print(f"Climate averages computed for {len(climate_by_loc)} locations")

    df["lat_round"] = df["latitude"].round(2)
    df["lon_round"] = df["longitude"].round(2)

    merged = df.merge(climate_by_loc, on=["lat_round", "lon_round"], how="left")
    merged = merged.drop(columns=["lat_round", "lon_round"])

    has_climate = merged["T2M"].notna().sum() if "T2M" in merged.columns else 0
    print(f"{has_climate}/{len(merged)} coffees have climate data")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
