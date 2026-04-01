# coffee-data

Collecting and analyzing data from the coffee industry — focusing on how climate influences fermentation and cup quality across farms worldwide.

## Research Tracks

- **[What Makes Coffee Score High?](docs/what-makes-coffee-score-high/)** — Analysis of ~1,300 CQI coffees and 17,000+ Cup of Excellence entries. Key findings: flavor/aftertaste drive score, soil explains 70x more variance than altitude, country is the strongest predictor.
- **[Coffee Pharmacognosy](docs/coffee-pharmacognosy/)** — Fermentation-to-function science: how variety, terroir, and processing shape microbial communities and bioactive compounds with therapeutic potential. Includes a data sources inventory and research gap analysis.

## Data Sources

- **[CQI Coffee Quality Database](https://www.kaggle.com/datasets/fatihb/coffee-quality-data-cqi)** — ~1,300 coffees with farm info, processing methods, and cupping scores
- **[Cup of Excellence](https://cupofexcellence.org/competition-auction-results/)** — Auction results and cupping scores for top-rated coffees across 14 countries (1999–present)
- **[NASA POWER](https://power.larc.nasa.gov/)** — Monthly climate data (temperature, rainfall, humidity, solar radiation) for any coordinate

## Setup

Requires Python 3.11+ and [Task](https://taskfile.dev/).

```sh
task setup
```

## Usage

```sh
task scrape:cqi       # Download CQI dataset from Kaggle
task scrape:coe       # Scrape Cup of Excellence results
task scrape:climate   # Fetch NASA POWER climate data
task notebook         # Launch Jupyter
```

Run `task --list` for all available commands.

## Project Structure

```
scrapers/           # Data collection scripts
data/raw/           # Downloaded/scraped data (gitignored)
data/processed/     # Cleaned/merged datasets (gitignored)
notebooks/          # Jupyter notebooks for analysis
utils/              # Shared helpers
```
