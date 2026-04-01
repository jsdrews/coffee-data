"""
Scraper for Cup of Excellence competition and auction results.
https://cupofexcellence.org/competition-auction-results/

Collects cupping scores, auction prices, farm names, regions, varieties,
and processing methods for coffees across 11+ producing countries (1999–present).

The site uses two domains:
  - cupofexcellence.org       (results through ~2021)
  - allianceforcoffeeexcellence.org  (results from ~2022 onward)

Each competition page lives at /{country}-{year}/ and contains one or two
static HTML tables (COE Winners and National Winners) styled with the
"mtr-table" responsive-table plugin.

Column headers vary by country/year but commonly include:
  RANK, SCORE, FARM, FARMER, REGION, VARIETY, PROCESS, WEIGHT (kg)
  (Ethiopia uses ZONE + WOREDA instead of REGION)
"""

import asyncio
import re
from urllib.parse import urljoin

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

# Both domains host results; the old site links to the newer one
DOMAINS = [
    "https://cupofexcellence.org",
    "https://allianceforcoffeeexcellence.org",
]

INDEX_PATHS = [
    "/competition-auction-results/",
]

HEADERS = {
    "User-Agent": "CoffeeDataResearch/0.1 (academic research project)"
}

MAX_CONCURRENT = 4

# Regex to extract country and year from a results-page URL slug
_SLUG_RE = re.compile(
    r"/([a-z][a-z\-]+?)-(\d{4})(?:-[a-z]+)?/?$", re.IGNORECASE
)

# Canonical column names we map to (lowercase keys)
_COLUMN_MAP = {
    "rank": "rank",
    "#": "rank",
    "score": "score",
    "farm": "farm",
    "farmer": "farmer",
    "farmer / organization": "farmer",
    "farmer/organization": "farmer",
    "producer": "farmer",
    "region": "region",
    "zone": "zone",
    "woreda": "woreda",
    "department": "region",
    "state": "region",
    "variety": "variety",
    "varieties": "variety",
    "process": "process",
    "processing": "process",
    "weight": "weight_kg",
    "weight (kg)": "weight_kg",
    "lbs": "weight_lbs",
    "price/lb": "price_per_lb",
    "price": "price_per_lb",
    "total value": "total_value",
    "# of bids": "num_bids",
    "altitude": "altitude",
    "elevation": "altitude",
}


async def _fetch(
    session: aiohttp.ClientSession,
    url: str,
    timeout_s: int = 30,
) -> str | None:
    """Fetch a URL; return HTML text or None on failure."""
    try:
        async with session.get(
            url, timeout=aiohttp.ClientTimeout(total=timeout_s)
        ) as resp:
            if resp.status != 200:
                print(f"  [{resp.status}] {url}")
                return None
            return await resp.text()
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


# --------------------------------------------------------------------------- #
#  Step 1: Discover all competition-result page URLs from the index pages
# --------------------------------------------------------------------------- #

async def discover_result_urls(session: aiohttp.ClientSession) -> list[str]:
    """Scrape the index/nav pages on both domains to find all result-page URLs.

    Result URLs look like  /{country}-{year}/  (e.g. /brazil-2021/).
    We collect them from <a> tags in the navigation menu and page body.
    """
    seen: set[str] = set()
    urls: list[str] = []

    for domain in DOMAINS:
        for path in INDEX_PATHS:
            index_url = domain + path
            html = await _fetch(session, index_url)
            if not html:
                continue

            soup = BeautifulSoup(html, "lxml")
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                # Normalise relative URLs
                if href.startswith("/"):
                    href = urljoin(domain, href)

                # Only keep links that look like competition result pages
                if _SLUG_RE.search(href) and href not in seen:
                    seen.add(href)
                    urls.append(href)

    print(f"Discovered {len(urls)} result-page URLs")
    return sorted(urls)


def _parse_slug(url: str) -> tuple[str, str]:
    """Extract (country, year) from a result-page URL."""
    m = _SLUG_RE.search(url)
    if m:
        return m.group(1), m.group(2)
    return "unknown", "unknown"


# --------------------------------------------------------------------------- #
#  Step 2: Parse the results tables on each competition page
# --------------------------------------------------------------------------- #

def _normalise_header(raw: str) -> str:
    """Map a raw column header to a canonical name."""
    key = raw.strip().lower()
    return _COLUMN_MAP.get(key, key)


def parse_results_table(soup: BeautifulSoup) -> list[dict]:
    """Extract competition results from a parsed results page.

    Pages typically have one or two HTML tables:
      1. COE Winning Farms (scores >= ~87)
      2. National Winners   (scores ~85-87)

    The tables use a WordPress responsive-table plugin whose cells have
    classes like ``mtr-th-tag`` and ``mtr-td-tag`` and a wrapper class
    ``mtr-table``.  However the underlying markup is still plain
    ``<table>/<tr>/<th>/<td>`` so standard BeautifulSoup selectors work.

    We label each row with a ``result_tier`` field ("coe_winner" or
    "national_winner") based on the heading that precedes the table.
    """
    all_rows: list[dict] = []

    # Determine section labels: walk through headings that precede each table
    tables = soup.find_all("table")
    for table in tables:
        # Figure out what tier this table represents by looking at preceding
        # heading text (h1-h4 or strong tags).
        tier = _infer_tier(table)

        # --- Extract headers ------------------------------------------------
        header_cells = table.find_all("th")
        if not header_cells:
            # Some older pages put headers in the first <tr> as <td>
            first_row = table.find("tr")
            if first_row:
                header_cells = first_row.find_all("td")
            if not header_cells:
                continue

        headers = [_normalise_header(th.get_text(strip=True)) for th in header_cells]

        # Skip tables that don't look like results (e.g. layout tables)
        if not any(h in ("rank", "score", "farm", "farmer") for h in headers):
            continue

        # --- Extract data rows ---------------------------------------------
        data_rows = table.find_all("tr")
        # Skip the header row (first <tr> that contained <th> or header <td>)
        start = 1 if header_cells else 0

        for tr in data_rows[start:]:
            cells = tr.find_all("td")
            if not cells:
                continue

            values = [td.get_text(strip=True) for td in cells]

            # Handle rows where column count doesn't match headers.
            # Pad or truncate to avoid crashes; misaligned rows will still
            # be captured for manual review.
            if len(values) < len(headers):
                values.extend([""] * (len(headers) - len(values)))
            elif len(values) > len(headers):
                values = values[: len(headers)]

            row = dict(zip(headers, values))
            row["result_tier"] = tier
            all_rows.append(row)

    return all_rows


def _infer_tier(table_tag) -> str:
    """Look at text before a <table> to decide if it's COE or National."""
    # Walk backwards through previous siblings and parent to find a heading
    for sib in _previous_text_elements(table_tag):
        text = sib.lower()
        if "national" in text:
            return "national_winner"
        if "winning" in text or "coe" in text or "cup of excellence" in text:
            return "coe_winner"
    return "coe_winner"  # default


def _previous_text_elements(tag, limit: int = 10):
    """Yield stripped text from elements preceding *tag* (siblings + parent)."""
    count = 0
    for sib in tag.previous_siblings:
        if count >= limit:
            break
        text = getattr(sib, "get_text", lambda **_: "")
        t = text(strip=True) if callable(text) else ""
        if t:
            yield t
            count += 1


# --------------------------------------------------------------------------- #
#  Step 3: Scrape all pages and assemble a DataFrame
# --------------------------------------------------------------------------- #

async def scrape_all() -> pd.DataFrame:
    """Discover and scrape all Cup of Excellence result pages."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    all_results: list[dict] = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        result_urls = await discover_result_urls(session)

        async def fetch_and_parse(url: str):
            async with semaphore:
                slug_country, slug_year = _parse_slug(url)
                print(f"  Scraping {slug_country} {slug_year} ...")
                html = await _fetch(session, url)
                if not html:
                    return []
                soup = BeautifulSoup(html, "lxml")
                rows = parse_results_table(soup)
                for row in rows:
                    row["country"] = slug_country
                    row["year"] = slug_year
                    row["source_url"] = url
                return rows

        tasks = [fetch_and_parse(url) for url in result_urls]
        results = await asyncio.gather(*tasks)

    for rows in results:
        all_results.extend(rows)

    df = pd.DataFrame(all_results)
    if not df.empty:
        _post_process(df)
    return df


def _post_process(df: pd.DataFrame) -> None:
    """Clean up the DataFrame in-place."""
    # Normalise the process column for easier analysis
    if "process" in df.columns:
        df["process"] = df["process"].str.strip().str.title()

    # Convert score to numeric
    if "score" in df.columns:
        df["score"] = pd.to_numeric(df["score"], errors="coerce")

    # Merge zone/woreda into region when region is absent (Ethiopia pages)
    if "zone" in df.columns:
        if "region" not in df.columns:
            df["region"] = ""
        mask = df["region"].eq("") | df["region"].isna()
        if "woreda" in df.columns:
            df.loc[mask, "region"] = (
                df.loc[mask, "zone"].fillna("")
                + " / "
                + df.loc[mask, "woreda"].fillna("")
            )
        else:
            df.loc[mask, "region"] = df.loc[mask, "zone"].fillna("")

    # Ensure country names are clean
    if "country" in df.columns:
        df["country"] = (
            df["country"]
            .str.replace("-", " ", regex=False)
            .str.title()
        )


# --------------------------------------------------------------------------- #
#  CLI entry point
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    df = asyncio.run(scrape_all())
    output_path = "data/raw/cup_of_excellence.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved {len(df)} rows to {output_path}")

    # Quick summary of processing methods
    if "process" in df.columns:
        print("\nProcessing methods found:")
        print(df["process"].value_counts().to_string())
