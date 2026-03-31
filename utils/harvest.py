"""
Harvest timing by country.

Maps coffee-producing countries to their primary harvest months.
Used to window NASA POWER climate queries to the actual processing period.

Sources:
- Mercanta Coffee Seasonality (coffeehunter.com/coffee-seasonality/)
- Royal Coffee Harvest Guide
"""

# Months as integers (1=Jan, 12=Dec)
HARVEST_MONTHS: dict[str, list[int]] = {
    "Brazil":           [5, 6, 7, 8, 9],
    "Burundi":          [3, 4, 5, 6, 7],
    "China":            [10, 11, 12, 1, 2],
    "Colombia":         [10, 11, 12, 1, 2],     # main crop; mitaca Apr-Jun
    "Costa Rica":       [11, 12, 1, 2, 3],
    "Ecuador":          [5, 6, 7, 8],
    "El Salvador":      [11, 12, 1, 2, 3],
    "Ethiopia":         [10, 11, 12, 1],
    "Guatemala":        [12, 1, 2, 3],
    "Haiti":            [7, 8, 9, 10],
    "Honduras":         [11, 12, 1, 2, 3],
    "India":            [11, 12, 1, 2, 3],
    "Indonesia":        [5, 6, 7, 8, 9],
    "Ivory Coast":      [11, 12, 1, 2],
    "Japan":            [10, 11, 12],
    "Kenya":            [10, 11, 12],            # main crop; fly crop Jun-Aug
    "Laos":             [11, 12, 1, 2],
    "Malawi":           [5, 6, 7, 8, 9],
    "Mexico":           [11, 12, 1, 2, 3],
    "Myanmar":          [11, 12, 1, 2],
    "Nicaragua":        [11, 12, 1, 2, 3],
    "Panama":           [12, 1, 2, 3],
    "Papua New Guinea": [4, 5, 6, 7, 8],
    "Peru":             [5, 6, 7, 8, 9],
    "Philippines":      [10, 11, 12, 1, 2],
    "Rwanda":           [3, 4, 5, 6, 7],
    "Taiwan":           [10, 11, 12],
    "Tanzania":         [7, 8, 9, 10, 11, 12],
    "Thailand":         [11, 12, 1, 2],
    "Uganda":           [10, 11, 12, 1, 2],
    "United States":    [8, 9, 10, 11, 12],      # Hawaii
    "Vietnam":          [10, 11, 12, 1, 2, 3],
    "Zambia":           [5, 6, 7, 8, 9],
}

# Aliases for country name variants in the CQI data
COUNTRY_ALIASES = {
    "United States (Hawaii)": "United States",
    "United States (Puerto Rico)": "United States",
    "Tanzania, United Republic Of": "Tanzania",
    "Cote d?Ivoire": "Ivory Coast",
    "Mauritius": None,  # not a major producer, no data
}


def get_harvest_months(country: str) -> list[int] | None:
    """Return harvest months for a country, handling aliases."""
    resolved = COUNTRY_ALIASES.get(country, country)
    if resolved is None:
        return None
    return HARVEST_MONTHS.get(resolved)
