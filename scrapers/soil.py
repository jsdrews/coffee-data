"""
Pull ISRIC SoilGrids data for geocoded coffee farm locations and merge with CQI data.

Fetches soil properties (pH, organic carbon, clay, sand, silt) concurrently
for each unique coordinate.

Uses two approaches in order of preference:
  1. SoilGrids REST API v2.0 (https://rest.isric.org/soilgrids/v2.0/docs)
  2. ISRIC WCS (Web Coverage Service) at maps.isric.org — more reliable fallback

The WCS approach requests a 1x1 pixel GeoTIFF for each property/depth at
the target coordinate and reads the pixel value.
"""

import asyncio
import io
import struct
import sys
from pathlib import Path

import aiohttp
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

SOIL_CACHE = PROJECT_ROOT / "data" / "processed" / "soil_raw.csv"
INPUT_CQI = PROJECT_ROOT / "data" / "processed" / "cqi_with_climate.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "cqi_with_climate_soil.csv"
GEOCODED_PATH = PROJECT_ROOT / "data" / "processed" / "geocoded_regions.csv"

# ── REST API config ──────────────────────────────────────────────────────────
REST_API_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"

# ── WCS config ───────────────────────────────────────────────────────────────
# Each soil property has its own WCS map endpoint
WCS_BASE = "https://maps.isric.org/mapserv"

# Soil properties relevant to coffee quality
SOIL_PROPERTIES = {
    "phh2o": "phh2o",      # pH in H2O
    "ocd":   "ocd",        # Organic carbon density
    "clay":  "clay",       # Clay content (g/kg)
    "sand":  "sand",       # Sand content (g/kg)
    "silt":  "silt",       # Silt content (g/kg)
}

# WCS coverage IDs use this naming: {property}_{depth}_{stat}
# Depths relevant for coffee root zone (top 30cm covers feeder roots)
DEPTHS = ["0-5cm", "5-15cm", "15-30cm"]

MAX_CONCURRENT = 5  # Be polite to ISRIC servers


# ── REST API approach ────────────────────────────────────────────────────────

async def fetch_one_rest(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    lat: float,
    lon: float,
) -> list[dict]:
    """Fetch soil properties for a single coordinate from SoilGrids REST API."""
    params = [
        ("lon", lon),
        ("lat", lat),
        ("value", "mean"),
    ]
    for prop in SOIL_PROPERTIES:
        params.append(("property", prop))
    for depth in DEPTHS:
        params.append(("depth", depth))

    async with semaphore:
        try:
            async with session.get(
                REST_API_URL,
                params=params,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
        except Exception:
            return []

    records = []
    try:
        layers = data["properties"]["layers"]
        for layer in layers:
            prop_name = layer["name"]
            unit = layer.get("unit_measure", {}).get("mapped_units", "")
            for depth_info in layer["depths"]:
                depth_label = depth_info["label"]
                values = depth_info.get("values", {})
                mean_val = values.get("mean")
                records.append({
                    "lat": lat,
                    "lon": lon,
                    "property": prop_name,
                    "depth": depth_label,
                    "value": mean_val,
                    "unit": unit,
                })
    except (KeyError, TypeError):
        pass

    return records


# ── WCS approach ─────────────────────────────────────────────────────────────

def _parse_tiff_value(data: bytes) -> float | None:
    """Extract the first pixel value from a minimal GeoTIFF.

    SoilGrids WCS returns single-pixel GeoTIFFs. We parse just enough
    of the TIFF structure to find the strip data, avoiding a heavy
    dependency on rasterio/GDAL.
    """
    if len(data) < 8:
        return None

    # Check byte order
    bo = data[:2]
    if bo == b"II":
        endian = "<"
    elif bo == b"MM":
        endian = ">"
    else:
        return None

    # Verify TIFF magic number
    magic = struct.unpack(f"{endian}H", data[2:4])[0]
    if magic != 42:
        return None

    # Read IFD offset
    ifd_offset = struct.unpack(f"{endian}I", data[4:8])[0]
    if ifd_offset + 2 > len(data):
        return None

    num_entries = struct.unpack(f"{endian}H", data[ifd_offset:ifd_offset + 2])[0]

    strip_offset = None
    bits_per_sample = 16
    sample_format = 1  # 1=uint, 2=int, 3=float

    pos = ifd_offset + 2
    for _ in range(num_entries):
        if pos + 12 > len(data):
            break
        tag, type_id, count, value_offset = struct.unpack(
            f"{endian}HHI4s", data[pos:pos + 12]
        )
        # For values that fit in 4 bytes, value_offset IS the value
        if type_id == 3:  # SHORT
            val = struct.unpack(f"{endian}HH", value_offset)[0]
        elif type_id == 4:  # LONG
            val = struct.unpack(f"{endian}I", value_offset)[0]
        else:
            val = struct.unpack(f"{endian}I", value_offset)[0]

        if tag == 273:    # StripOffsets
            strip_offset = val
        elif tag == 258:  # BitsPerSample
            bits_per_sample = val
        elif tag == 339:  # SampleFormat
            sample_format = val

        pos += 12

    if strip_offset is None:
        return None

    # Read the pixel value
    if sample_format == 3:  # float
        if bits_per_sample == 32:
            if strip_offset + 4 > len(data):
                return None
            val = struct.unpack(f"{endian}f", data[strip_offset:strip_offset + 4])[0]
        elif bits_per_sample == 64:
            if strip_offset + 8 > len(data):
                return None
            val = struct.unpack(f"{endian}d", data[strip_offset:strip_offset + 8])[0]
        else:
            return None
    elif sample_format == 2:  # signed int
        if bits_per_sample == 16:
            if strip_offset + 2 > len(data):
                return None
            val = struct.unpack(f"{endian}h", data[strip_offset:strip_offset + 2])[0]
        elif bits_per_sample == 32:
            if strip_offset + 4 > len(data):
                return None
            val = struct.unpack(f"{endian}i", data[strip_offset:strip_offset + 4])[0]
        else:
            return None
    else:  # unsigned int
        if bits_per_sample == 8:
            if strip_offset + 1 > len(data):
                return None
            val = struct.unpack(f"{endian}B", data[strip_offset:strip_offset + 1])[0]
        elif bits_per_sample == 16:
            if strip_offset + 2 > len(data):
                return None
            val = struct.unpack(f"{endian}H", data[strip_offset:strip_offset + 2])[0]
        elif bits_per_sample == 32:
            if strip_offset + 4 > len(data):
                return None
            val = struct.unpack(f"{endian}I", data[strip_offset:strip_offset + 4])[0]
        else:
            return None

    # SoilGrids nodata is typically a very large negative or 0 for unsigned
    # -32768 is common nodata for int16
    if val == -32768 or val == 65535 or val == -2147483648:
        return None

    return float(val)


async def fetch_one_wcs_property(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    lat: float,
    lon: float,
    prop: str,
    depth: str,
) -> dict | None:
    """Fetch a single soil property at one depth via WCS GetCoverage."""
    # Coverage ID format: e.g. phh2o_0-5cm_mean
    coverage_id = f"{prop}_{depth}_mean"
    # Small bounding box around the point (approx 250m, matching SoilGrids resolution)
    delta = 0.0025  # ~250m at equator
    bbox = f"{lon - delta},{lat - delta},{lon + delta},{lat + delta}"

    params = {
        "map": f"/map/{prop}.map",
        "SERVICE": "WCS",
        "VERSION": "2.0.1",
        "REQUEST": "GetCoverage",
        "COVERAGEID": coverage_id,
        "FORMAT": "image/tiff",
        "SUBSET": f"long({lon - delta},{lon + delta})",
        "SUBSETTINGCRS": "http://www.opengis.net/def/crs/EPSG/0/4326",
    }
    # Add lat subset separately
    params["SUBSET"] = [
        f"long({lon - delta},{lon + delta})",
        f"lat({lat - delta},{lat + delta})",
    ]

    # aiohttp handles list params by repeating the key
    # We need to build the URL manually for repeated SUBSET params
    url = (
        f"{WCS_BASE}?map=/map/{prop}.map"
        f"&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage"
        f"&COVERAGEID={coverage_id}"
        f"&FORMAT=image/tiff"
        f"&SUBSET=long({lon - delta},{lon + delta})"
        f"&SUBSET=lat({lat - delta},{lat + delta})"
        f"&SUBSETTINGCRS=http://www.opengis.net/def/crs/EPSG/0/4326"
    )

    async with semaphore:
        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if resp.status != 200:
                    return None
                content_type = resp.headers.get("content-type", "")
                raw = await resp.read()
                if b"<ServiceException" in raw or b"<ows:Exception" in raw:
                    return None
        except Exception:
            return None

    value = _parse_tiff_value(raw)
    if value is None:
        return None

    return {
        "lat": lat,
        "lon": lon,
        "property": prop,
        "depth": depth,
        "value": value,
        "unit": "",
    }


async def fetch_one_wcs(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    lat: float,
    lon: float,
) -> list[dict]:
    """Fetch all soil properties for one coordinate via WCS."""
    tasks = []
    for prop in SOIL_PROPERTIES:
        for depth in DEPTHS:
            tasks.append(
                fetch_one_wcs_property(session, semaphore, lat, lon, prop, depth)
            )

    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]


# ── Main fetching logic ─────────────────────────────────────────────────────

async def _check_rest_api(session: aiohttp.ClientSession) -> bool:
    """Quick health check — is the REST API responding?"""
    params = [
        ("lon", 0),
        ("lat", 0),
        ("property", "phh2o"),
        ("depth", "0-5cm"),
        ("value", "mean"),
    ]
    try:
        async with session.get(
            REST_API_URL,
            params=params,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as resp:
            return resp.status == 200
    except Exception:
        return False


async def fetch_all_soil(coords: pd.DataFrame) -> pd.DataFrame:
    """Fetch SoilGrids data for all coordinates.

    Tries the REST API first; if it's down, falls back to WCS.
    """
    if SOIL_CACHE.exists():
        print(f"Loading cached soil data from {SOIL_CACHE}")
        return pd.read_csv(SOIL_CACHE)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    all_records: list[dict] = []
    total = len(coords)

    async with aiohttp.ClientSession() as session:
        # Decide which backend to use
        rest_ok = await _check_rest_api(session)
        if rest_ok:
            print("Using SoilGrids REST API")
            fetch_fn = fetch_one_rest
        else:
            print("REST API unavailable — falling back to WCS")
            fetch_fn = fetch_one_wcs

        tasks = []
        for _, row in coords.iterrows():
            lat = round(row["latitude"], 4)
            lon = round(row["longitude"], 4)
            tasks.append(fetch_fn(session, semaphore, lat, lon))

        done = 0
        for coro in asyncio.as_completed(tasks):
            records = await coro
            all_records.extend(records)
            done += 1
            if done % 10 == 0 or done == total:
                print(f"  [{done}/{total}] coordinates fetched...")

    result = pd.DataFrame(all_records) if all_records else pd.DataFrame()
    SOIL_CACHE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(SOIL_CACHE, index=False)
    print(f"Cached {len(result)} soil records to {SOIL_CACHE}")
    return result


def aggregate_soil(soil_raw: pd.DataFrame) -> pd.DataFrame:
    """Aggregate soil data: average across depths for each coordinate+property.

    SoilGrids returns integer-scaled values. Convert to standard units:
      - phh2o: stored as pH * 10  -> divide by 10
      - ocd:   hg/m³ (already in useful units)
      - clay/sand/silt: g/kg

    Returns a DataFrame with one row per coordinate and columns for each
    soil property (averaged across the top 30cm depth layers).
    """
    if soil_raw.empty:
        return pd.DataFrame()

    # Average across depth layers per coordinate + property
    avg = (
        soil_raw.groupby(["lat", "lon", "property"])["value"]
        .mean()
        .reset_index()
    )

    # Pivot so each property becomes a column
    pivoted = avg.pivot_table(
        index=["lat", "lon"],
        columns="property",
        values="value",
    ).reset_index()

    # Flatten column names
    pivoted.columns = [
        f"soil_{c}" if c not in ("lat", "lon") else c
        for c in pivoted.columns
    ]

    # Convert pH from 10x to actual pH
    if "soil_phh2o" in pivoted.columns:
        pivoted["soil_phh2o"] = pivoted["soil_phh2o"] / 10.0

    # Rename for clarity
    rename_map = {
        "soil_phh2o": "soil_ph",
        "soil_ocd": "soil_organic_carbon",
        "soil_clay": "soil_clay_content",
        "soil_sand": "soil_sand_content",
        "soil_silt": "soil_silt_content",
    }
    pivoted = pivoted.rename(columns=rename_map)

    return pivoted


def main():
    # Load geocoded coordinates
    geocoded = pd.read_csv(GEOCODED_PATH)
    coords = (
        geocoded[["latitude", "longitude"]]
        .dropna()
        .drop_duplicates()
        .reset_index(drop=True)
    )
    print(f"{len(coords)} unique coordinates to fetch soil data for")

    # Fetch soil data
    soil_raw = asyncio.run(fetch_all_soil(coords))

    if soil_raw.empty:
        print("No soil data retrieved. Exiting.")
        return

    # Aggregate across depths
    soil_agg = aggregate_soil(soil_raw)
    print(f"Soil data aggregated for {len(soil_agg)} locations")

    # Load existing CQI+climate dataset
    cqi = pd.read_csv(INPUT_CQI)
    print(f"Loaded {len(cqi)} rows from {INPUT_CQI}")

    # Round coordinates for matching (geocoded_regions uses full precision)
    cqi["lat_match"] = cqi["latitude"].round(4)
    cqi["lon_match"] = cqi["longitude"].round(4)
    soil_agg = soil_agg.rename(columns={"lat": "lat_match", "lon": "lon_match"})
    soil_agg["lat_match"] = soil_agg["lat_match"].round(4)
    soil_agg["lon_match"] = soil_agg["lon_match"].round(4)

    # Merge
    merged = cqi.merge(soil_agg, on=["lat_match", "lon_match"], how="left")
    merged = merged.drop(columns=["lat_match", "lon_match"])

    soil_cols = [c for c in merged.columns if c.startswith("soil_")]
    if soil_cols:
        has_soil = merged[soil_cols[0]].notna().sum()
        print(f"{has_soil}/{len(merged)} coffees have soil data")
    else:
        print("Warning: no soil columns in merged dataset")

    # Save
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
