# coffee-data

Collecting and analyzing data from the coffee industry — focusing on how climate influences fermentation and cup quality across farms worldwide.

## Research Tracks

- **[What Makes Coffee Score High?](docs/what-makes-coffee-score-high/)** — Analysis of ~1,300 CQI coffees and 17,000+ Cup of Excellence entries. Key findings: flavor/aftertaste drive score, soil explains 70x more variance than altitude, country is the strongest predictor.
- **[Coffee Pharmacognosy](docs/coffee-pharmacognosy/)** — Fermentation-to-function science: how variety, terroir, and processing shape microbial communities and bioactive compounds with therapeutic potential. Includes a data sources inventory and research gap analysis.

## Data Sources

### Cupping & quality

| Source | Records | Description |
|--------|---------|-------------|
| [CQI Coffee Quality Database](https://www.kaggle.com/datasets/fatihb/coffee-quality-data-cqi) | 1,311 | Cupping attributes, processing, variety, altitude, country |
| [Cup of Excellence](https://cupofexcellence.org/competition-auction-results/) | 17,211 | Competition scores, variety, farm, region, country (1999–present) |

### Climate & soil

| Source | Records | Description |
|--------|---------|-------------|
| [NASA POWER](https://power.larc.nasa.gov/) | 337,610 | Monthly climate data (temperature, rainfall, humidity, solar radiation) |
| [ISRIC SoilGrids](https://soilgrids.org/) | 3,975 | Soil properties (pH, organic carbon, clay/sand/silt, CEC) for 265 locations |

### Chemistry & pharmacology

| Source | Records | Description |
|--------|---------|-------------|
| [Phenol-Explorer](http://phenol-explorer.eu) | 69 | Polyphenol concentrations for 4 coffee beverage types |
| [FooDB](https://foodb.ca) | 16,340 | Full chemical inventory — compounds and concentrations for Arabica, Robusta, general coffee |
| [PubChem](https://pubchem.ncbi.nlm.nih.gov) | 5,510 | Bioassay results for caffeine, chlorogenic acid, cafestol, kahweol, trigonelline |
| [ChEMBL](https://www.ebi.ac.uk/chembl/) | 3,333 | Bioactivity measurements (IC50, EC50, Ki) against protein targets |

### Varieties

| Source | Records | Description |
|--------|---------|-------------|
| [World Coffee Research](https://varieties.worldcoffeeresearch.org) | 70 | Arabica variety catalog — quality, yield, disease resistance, lineage |

## Setup

Requires Python 3.11+ and [Task](https://taskfile.dev/).

```sh
task setup
```

## Usage

```sh
task scrape            # Run all scrapers
task scrape:cqi        # Download CQI dataset from Kaggle
task scrape:coe        # Scrape Cup of Excellence results
task scrape:climate    # Fetch NASA POWER climate data
task scrape:phenol-explorer  # Scrape polyphenol data
task scrape:foodb      # Extract FooDB coffee compounds
task scrape:pubchem    # Pull PubChem bioassay data
task scrape:chembl     # Pull ChEMBL bioactivity data
task scrape:wcr        # Scrape WCR variety catalog
task notebook          # Launch Jupyter
task export            # Convert all notebooks to HTML
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
