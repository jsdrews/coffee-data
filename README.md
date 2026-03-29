# coffee-data

Collecting and analyzing data from the coffee industry — focusing on how climate influences fermentation and cup quality across farms worldwide.

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
