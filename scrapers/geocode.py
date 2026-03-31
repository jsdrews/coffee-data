"""
Geocode coffee farm locations using OpenStreetMap's Nominatim.

Takes the CQI dataset's country + region fields and resolves them to
latitude/longitude coordinates for use with NASA POWER climate data.
"""

import time
from pathlib import Path

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "geocoded_regions.csv"


def build_query(row: pd.Series) -> str:
    """Build a geocoding query from country + region."""
    country = row["country_of_origin"]
    region = row.get("region", "")

    # Clean up country names for better geocoding
    country_fixes = {
        "United States (Hawaii)": "Hawaii, United States",
        "United States (Puerto Rico)": "Puerto Rico",
        "Tanzania, United Republic Of": "Tanzania",
        "Cote d?Ivoire": "Ivory Coast",
    }
    country = country_fixes.get(country, country)

    if pd.notna(region) and region.strip():
        return f"{region}, {country}"
    return country


def geocode_regions(df: pd.DataFrame) -> pd.DataFrame:
    """Geocode unique country+region combinations.

    Returns a DataFrame with columns:
        country_of_origin, region, latitude, longitude, geocode_query
    """
    geolocator = Nominatim(
        user_agent="CoffeeDataResearch/0.1 (academic research project)",
        timeout=10,
    )
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.1)

    # Get unique location combinations
    locations = (
        df[["country_of_origin", "region"]]
        .drop_duplicates()
        .dropna(subset=["country_of_origin"])
        .copy()
    )
    locations["geocode_query"] = locations.apply(build_query, axis=1)

    # Deduplicate queries (different rows may produce the same query)
    unique_queries = locations["geocode_query"].unique()
    print(f"Geocoding {len(unique_queries)} unique locations...")

    query_results = {}
    for i, query in enumerate(unique_queries):
        if (i + 1) % 25 == 0:
            print(f"  [{i + 1}/{len(unique_queries)}] {query}")
        try:
            result = geocode(query)
            if result:
                query_results[query] = (result.latitude, result.longitude)
            else:
                # Fall back to country-only query
                country_part = query.split(",")[-1].strip()
                result = geocode(country_part)
                if result:
                    query_results[query] = (result.latitude, result.longitude)
                else:
                    query_results[query] = (None, None)
        except Exception as e:
            print(f"  Error geocoding '{query}': {e}")
            query_results[query] = (None, None)

    locations["latitude"] = locations["geocode_query"].map(lambda q: query_results.get(q, (None, None))[0])
    locations["longitude"] = locations["geocode_query"].map(lambda q: query_results.get(q, (None, None))[1])

    success = locations["latitude"].notna().sum()
    print(f"Geocoded {success}/{len(locations)} locations ({success/len(locations)*100:.0f}%)")

    return locations


def geocode_and_save(df: pd.DataFrame) -> pd.DataFrame:
    """Geocode regions and save results to CSV for reuse."""
    # Check for cached results
    if OUTPUT_PATH.exists():
        print(f"Loading cached geocoding results from {OUTPUT_PATH}")
        return pd.read_csv(OUTPUT_PATH)

    results = geocode_regions(df)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")
    return results


def merge_coordinates(df: pd.DataFrame, geocoded: pd.DataFrame) -> pd.DataFrame:
    """Merge geocoded coordinates back into the main dataset."""
    return df.merge(
        geocoded[["country_of_origin", "region", "latitude", "longitude"]],
        on=["country_of_origin", "region"],
        how="left",
    )


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))
    from utils.data import load_cqi

    df = load_cqi()
    geocoded = geocode_and_save(df)

    merged = merge_coordinates(df, geocoded)
    has_coords = merged["latitude"].notna().sum()
    print(f"\n{has_coords}/{len(merged)} coffees now have coordinates ({has_coords/len(merged)*100:.0f}%)")
