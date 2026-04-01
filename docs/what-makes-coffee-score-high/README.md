# What Makes Coffee Score High?

An analysis of ~1,300 specialty coffees from 36 countries (CQI database) and 17,000+ Cup of Excellence competition entries, examining what drives cupping scores.

## Key findings

| # | Finding | Strength | Source |
|---|---------|----------|--------|
| 1 | **Flavor and aftertaste drive total score** (r=0.88, 0.87) | Strong | CQI |
| 2 | **More fermentation → slightly higher scores** (<1 pt gap, but consistent) | Moderate | CQI |
| 3 | **Naturals push outward on body** (7.60 vs 7.49 washed) | Observed | CQI |
| 4 | **Altitude is a weak predictor** (r=0.11, R²=0.02%) | Strong | CQI |
| 5 | **Country is the strongest single factor** (R²≈0.25) | Strong — but a black box | CQI |
| 6 | **Processing methods cluster climatically** — naturals in warmer/drier, washed in cooler/wetter | Observed | CQI + NASA POWER |
| 7 | **Climate-score correlations are partly artifacts** of country composition | Strong | CQI + NASA POWER |
| 8 | **Soil explains 70x more variance than altitude** (R²=4.2% vs 0.02%) | Moderate | CQI + SoilGrids |
| 9 | **Variety explains ~9% of variance** (vs 1.2% for processing); SL28/SL34 score highest | Moderate — confounded with country | CQI |
| 10 | **Experimental methods score 0.5–0.7 pts higher** in competitions; grew from 0% to ~20% of CoE entries (2015–2024) | Moderate — selection/novelty bias possible | CoE |

## What we haven't proven

- Causation in any direction — processing, variety, climate, and country are entangled
- Whether experimental methods score higher because of the technique or the farmer
- What "country" actually represents (terroir? selection bias? infrastructure?)

## Data sources

| Dataset | Records | Key fields |
|---------|---------|------------|
| [CQI Coffee Quality Database](https://www.kaggle.com/datasets/fatihb/coffee-quality-data-cqi) | 1,311 | Cupping attributes, processing, variety, altitude, country |
| [Cup of Excellence](https://cupofexcellence.org/competition-auction-results/) | 17,211 | Score, process, variety, farm, region, country, year |
| [NASA POWER](https://power.larc.nasa.gov/) | 337,610 | Monthly climate records for 265 locations |
| [ISRIC SoilGrids](https://soilgrids.org/) | 3,975 | Soil properties for 265 locations |

## Files

- `notebooks/what_makes_coffee_score_high.ipynb` — full analysis notebook (10 sections)
- `docs/what-makes-coffee-score-high/next-steps.md` — three proposed workstreams for further analysis

## Next steps

1. **Farm-level longitudinal analysis** — track same farms across CoE years to isolate processing effects
2. **Decompose the "country" effect** — replace country dummies with economic/agricultural indicators (World Bank API)
3. **Merge CQI + CoE datasets** — fuzzy-match farms to combine cupping detail with processing granularity

See [next-steps.md](next-steps.md) for full details.
