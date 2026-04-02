"""
Scraper for World Coffee Research Arabica Variety Catalog.
https://varieties.worldcoffeeresearch.org

Extracts variety names, agronomic characteristics, and text descriptions
from the listing page and individual variety pages.

The listing page at /arabica/varieties contains all varieties as divs with
data-searchable-* attributes (text fields like lineage, breeder, history)
and data-* attributes (ID-coded categorical fields like stature, yield).

Individual variety pages render the categorical values as labels, so we
scrape those to get the human-readable characteristics.
"""

import re
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "wcr_varieties.csv"

BASE_URL = "https://varieties.worldcoffeeresearch.org"

HEADERS = {
    "User-Agent": "CoffeeDataResearch/0.1 (academic research project)"
}

# Characteristics to extract from individual variety pages
CHARACTERISTICS = [
    "Stature",
    "Bean Size",
    "Optimal Altitude",
    "Yield Potential",
    "Quality potential at high altitude",
    "Coffee Leaf Rust",
    "Coffee Berry Disease",
    "Nematodes",
    "Leaf Tip Color",
    "Nutrition Requirement",
    "Ripening of Fruit",
    "Year of First Production",
    "Cherry to Green Bean Outturn",
    "Planting Density",
]


def _get_listing_page() -> list[dict]:
    """Extract variety names, URLs, and text attributes from the listing page."""
    url = f"{BASE_URL}/arabica/varieties"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    elements = soup.find_all(attrs={"data-searchable-lineage": True})

    varieties = []
    for el in elements:
        h3 = el.find("h3")
        name = h3.get_text(strip=True) if h3 else ""
        if not name:
            continue

        span = el.find("span", class_=re.compile(r"italic"))
        alt_name = span.get_text(strip=True) if span else ""

        link = el.find("a", href=re.compile(r"/varieties/"))
        page_url = link["href"] if link else ""

        p = el.find("p")
        description = p.get_text(strip=True) if p else ""

        varieties.append({
            "name": name,
            "alt_name": alt_name,
            "page_url": page_url,
            "description": description,
            "lineage": el.get("data-searchable-lineage", ""),
            "breeder": el.get("data-searchable-breeder", ""),
            "history": el.get("data-searchable-history", ""),
            "additional_info": el.get("data-searchable-additional-agromomic-information", ""),
            "genetic_group": el.get("data-genetic-description-arabica", ""),
        })

    return varieties


def _scrape_variety_page(url: str) -> dict[str, str]:
    """Scrape characteristics from an individual variety page."""
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code != 200:
        return {}

    soup = BeautifulSoup(r.text, "lxml")
    chars = {}

    for span in soup.find_all("span"):
        text = span.get_text(strip=True)
        if text in CHARACTERISTICS:
            parent = span.parent
            value_div = parent.find_next("div", class_=re.compile(r"text-txt-black"))
            if value_div:
                chars[text] = value_div.get_text(strip=True)

    return chars


def scrape_all() -> pd.DataFrame:
    """Scrape the full WCR variety catalog."""
    print("Fetching variety listing...")
    varieties = _get_listing_page()
    print(f"  → {len(varieties)} varieties found")

    print("\nScraping individual variety pages...")
    for i, var in enumerate(varieties):
        url = var["page_url"]
        if not url:
            continue
        if not url.startswith("http"):
            url = BASE_URL + url

        print(f"  [{i+1}/{len(varieties)}] {var['name']}...")
        chars = _scrape_variety_page(url)
        var.update(chars)
        time.sleep(0.3)  # be polite

    df = pd.DataFrame(varieties)

    # Clean up column names
    col_map = {c: c.lower().replace(" ", "_") for c in df.columns}
    df = df.rename(columns=col_map)

    return df


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = scrape_all()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved {len(df)} varieties to {OUTPUT_PATH}")
    print(f"\nColumns: {list(df.columns)}")
    if "quality_potential_at_high_altitude" in df.columns:
        print(f"\nQuality potential distribution:")
        print(df["quality_potential_at_high_altitude"].value_counts().to_string())
