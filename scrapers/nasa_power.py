"""
Client for the NASA POWER API — climate data for coffee farm locations.
https://power.larc.nasa.gov/

No API key required. Provides daily/monthly/annual weather data
(temperature, precipitation, humidity, solar radiation, etc.)
queryable by latitude/longitude.
"""

import pandas as pd
import requests

API_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"

# Parameters relevant to coffee growing and fermentation
CLIMATE_PARAMS = [
    "T2M",          # Temperature at 2m (°C)
    "T2M_MAX",      # Max temperature at 2m (°C)
    "T2M_MIN",      # Min temperature at 2m (°C)
    "T2M_RANGE",    # Temperature range at 2m (°C)
    "RH2M",         # Relative humidity at 2m (%)
    "PRECTOTCORR",  # Precipitation corrected (mm/day)
    "ALLSKY_SFC_SW_DWN",  # Solar radiation (MJ/m²/day)
]


def get_climate_data(
    lat: float,
    lon: float,
    start_year: int = 2010,
    end_year: int = 2024,
    params: list[str] | None = None,
) -> pd.DataFrame:
    """Fetch monthly climate data for a single coordinate.

    Args:
        lat: Latitude of the farm/region.
        lon: Longitude of the farm/region.
        start_year: Start year for data range.
        end_year: End year for data range.
        params: List of NASA POWER parameter codes. Defaults to CLIMATE_PARAMS.

    Returns:
        DataFrame with monthly climate values.
    """
    if params is None:
        params = CLIMATE_PARAMS

    query = {
        "parameters": ",".join(params),
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_year,
        "end": end_year,
        "format": "JSON",
    }

    resp = requests.get(API_URL, params=query, timeout=60)
    resp.raise_for_status()
    data = resp.json()

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

    return pd.DataFrame(records)


def get_climate_for_farms(
    farms: pd.DataFrame,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    **kwargs,
) -> pd.DataFrame:
    """Fetch climate data for a DataFrame of farm locations.

    Args:
        farms: DataFrame with latitude and longitude columns.
        lat_col: Name of the latitude column.
        lon_col: Name of the longitude column.
        **kwargs: Passed to get_climate_data.

    Returns:
        Combined DataFrame of climate data for all farms.
    """
    all_data = []
    coords = farms[[lat_col, lon_col]].drop_duplicates()

    for i, (_, row) in enumerate(coords.iterrows()):
        lat, lon = row[lat_col], row[lon_col]
        print(f"  [{i + 1}/{len(coords)}] Fetching climate for ({lat}, {lon})...")
        try:
            df = get_climate_data(lat, lon, **kwargs)
            all_data.append(df)
        except Exception as e:
            print(f"    Error: {e}")

    if not all_data:
        return pd.DataFrame()
    return pd.concat(all_data, ignore_index=True)


if __name__ == "__main__":
    # Example: fetch climate data for a Colombian coffee region (Huila)
    df = get_climate_data(lat=2.0, lon=-75.75, start_year=2018, end_year=2023)
    output_path = "data/raw/nasa_power_example.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")
