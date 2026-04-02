"""
Scraper for Phenol-Explorer coffee polyphenol data.
http://phenol-explorer.eu

Fetches polyphenol compound concentrations for all coffee food entries:
  - Coffee beverage [Filter] (id=552)
  - Coffee beverage [Filter], decaffeinated (id=553)
  - Arabica coffee beverage [Filter] (id=662)
  - Robusta coffee beverage [Filter] (id=666)

Each page contains HTML tables with compound names, mean concentrations,
min, max, SD, and number of references. The tables use a consistent
structure with class="list composition".
"""

import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "phenol_explorer.csv"

BASE_URL = "http://phenol-explorer.eu"

COFFEE_FOODS = {
    552: "Coffee beverage [Filter]",
    553: "Coffee beverage [Filter], decaffeinated",
    662: "Arabica coffee beverage [Filter]",
    666: "Robusta coffee beverage [Filter]",
}

HEADERS = {
    "User-Agent": "CoffeeDataResearch/0.1 (academic research project)"
}


def _parse_food_page(food_id: int, food_name: str) -> list[dict]:
    """Parse a single food's composition page into rows."""
    url = f"{BASE_URL}/contents/food/{food_id}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    tables = soup.find_all("table", class_="composition")
    rows: list[dict] = []

    for table in tables:
        current_class = ""
        current_subclass = ""

        for tr in table.find_all("tr"):
            classes = " ".join(tr.get("class", []))

            # Section headers (e.g., "Phenolic acids", "Lignans")
            if "header" in classes:
                th = tr.find("th", class_="inner")
                if th:
                    current_class = th.get_text(strip=True)
                    current_subclass = ""
                continue

            tds = tr.find_all("td")
            if not tds:
                continue

            # Rows with rowspan have the subclass in the first <td>
            # (e.g., "Hydroxycinnamic acids"), compound in second <td>
            # Rows without rowspan continue the previous subclass
            first_td = tds[0]
            if first_td.get("rowspan"):
                current_subclass = first_td.get_text(strip=True)
                tds = tds[1:]  # shift — compound name is next
            elif len(tds) >= 8:
                # Full row without rowspan — subclass continues
                pass
            else:
                continue

            if len(tds) < 7:
                continue

            # Extract compound name and ID from the link
            compound_link = tds[0].find("a")
            if not compound_link:
                continue

            compound_name = compound_link.get_text(strip=True)
            compound_href = compound_link.get("href", "")
            compound_id_match = re.search(r"/compounds/(\d+)", compound_href)
            compound_id = compound_id_match.group(1) if compound_id_match else ""

            # Extract mean content value from the content_value cell
            content_cell = tds[1]
            content_link = content_cell.find("a", href=re.compile(r"/contents/show"))
            mean_value = content_link.get_text(strip=True) if content_link else ""

            # Extract units
            units_span = content_cell.find("span", class_="units")
            units = units_span.get_text(strip=True) if units_span else ""

            # min, max, SD, n, N, references
            min_val = tds[2].get_text(strip=True) if len(tds) > 2 else ""
            max_val = tds[3].get_text(strip=True) if len(tds) > 3 else ""
            sd_val = tds[4].get_text(strip=True) if len(tds) > 4 else ""
            n_val = tds[5].get_text(strip=True) if len(tds) > 5 else ""
            n_samples = tds[6].get_text(strip=True) if len(tds) > 6 else ""
            n_refs = tds[7].get_text(strip=True) if len(tds) > 7 else ""

            rows.append({
                "food_id": food_id,
                "food_name": food_name,
                "polyphenol_class": current_class,
                "polyphenol_subclass": current_subclass,
                "compound_id": compound_id,
                "compound_name": compound_name,
                "mean_content": mean_value,
                "units": units,
                "min": min_val,
                "max": max_val,
                "sd": sd_val,
                "n_values": n_val,
                "n_samples": n_samples,
                "n_references": n_refs,
            })

    return rows


def scrape_all() -> pd.DataFrame:
    """Scrape all coffee entries from Phenol-Explorer."""
    all_rows: list[dict] = []

    for food_id, food_name in COFFEE_FOODS.items():
        print(f"  Scraping {food_name} (id={food_id})...")
        rows = _parse_food_page(food_id, food_name)
        print(f"    → {len(rows)} compounds")
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)

    if not df.empty:
        # Convert numeric columns
        for col in ("mean_content", "min", "max", "sd"):
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = scrape_all()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved {len(df)} rows to {OUTPUT_PATH}")
    print(f"\nCompounds per coffee type:")
    print(df.groupby("food_name")["compound_name"].count().to_string())
    print(f"\nPolyphenol classes:")
    print(df.groupby("polyphenol_class")["compound_name"].count().to_string())
