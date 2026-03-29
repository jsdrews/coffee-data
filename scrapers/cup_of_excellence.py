"""
Scraper for Cup of Excellence competition and auction results.
https://cupofexcellence.org/competition-auction-results/

Collects cupping scores, auction prices, farm names, and regions
for coffees across 11+ producing countries (1999–present).
"""

import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://cupofexcellence.org/competition-auction-results"

COUNTRIES = [
    "brazil",
    "burundi",
    "colombia",
    "costa-rica",
    "ecuador",
    "el-salvador",
    "ethiopia",
    "guatemala",
    "honduras",
    "indonesia",
    "mexico",
    "nicaragua",
    "peru",
    "rwanda",
]

HEADERS = {
    "User-Agent": "CoffeeDataResearch/0.1 (academic research project)"
}


def get_country_page(country: str) -> BeautifulSoup | None:
    """Fetch the results page for a given country."""
    url = f"{BASE_URL}/{country}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        print(f"Failed to fetch {country}: {resp.status_code}")
        return None
    return BeautifulSoup(resp.text, "lxml")


def parse_results_table(soup: BeautifulSoup) -> list[dict]:
    """Extract competition results from a parsed page.

    NOTE: The actual HTML structure may differ from what's assumed here.
    Run this once, inspect the output, and adjust selectors as needed.
    """
    rows = []
    tables = soup.find_all("table")
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        for tr in table.find_all("tr")[1:]:
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            if cells and len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))
    return rows


def scrape_all_countries(delay: float = 2.0) -> pd.DataFrame:
    """Scrape results for all countries with a polite delay between requests."""
    all_results = []
    for country in COUNTRIES:
        print(f"Scraping {country}...")
        soup = get_country_page(country)
        if soup:
            results = parse_results_table(soup)
            for row in results:
                row["country"] = country
            all_results.extend(results)
        time.sleep(delay)

    df = pd.DataFrame(all_results)
    return df


if __name__ == "__main__":
    df = scrape_all_countries()
    output_path = "data/raw/cup_of_excellence.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")
