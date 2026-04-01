# Next Steps

What we've established so far and where the analysis can go next.

## What we've shown

| Finding | Strength | Source |
|---------|----------|--------|
| Flavor and aftertaste drive total score (r=0.88, 0.87) | Strong — directly observed | CQI (1,311 samples) |
| Processing method shifts flavor profile (naturals have more body) | Moderate — observed but not causally isolated | CQI |
| More fermentation correlates with slightly higher scores | Moderate — consistent but <1 point gap | CQI |
| Altitude is a weak predictor (r=0.11, R²=0.02%) | Strong — directly observed | CQI |
| Soil explains 70x more variance than altitude (R²=4.2%) | Moderate — observed, pH and sand significant | CQI + SoilGrids |
| Variety explains ~9% of variance (vs 1.2% for processing) | Moderate — confounded with country | CQI |
| Country is the strongest single factor (R²≈0.25) | Strong — but "country" is a black box | CQI |
| Aggregate climate-processing correlations are partly artifacts | Strong — within-country analysis shows inconsistency | CQI + NASA POWER |
| Experimental methods score 0.5–0.7 pts higher in competitions | Moderate — observed but selection/novelty bias possible | CoE (17,211 entries) |
| Experimental methods grew from 0% to ~20% of CoE entries (2015–2024) | Strong — directly observed | CoE |

## What we haven't proven

- **Causation** in any direction. Processing, variety, climate, and country are all entangled.
- That climate **determines** which processing methods succeed (within-country analysis was mixed).
- Whether experimental methods score higher because of the **technique** or the **farmer**.
- What "country" actually represents — terroir? selection bias? farming tradition? infrastructure?

---

## Three workstreams

### 1. Farm-level longitudinal analysis (CoE data)

**Question:** When the same farm changes processing methods across years, does their score change?

**Why it matters:** This is the closest thing to a controlled experiment in our data. Within-farm comparisons hold soil, altitude, climate, and farmer skill roughly constant — isolating the effect of processing.

**Approach:**
- Deduplicate/fuzzy-match farm names across years in `data/raw/cup_of_excellence.csv` (17,211 entries, 25 years)
- Identify farms appearing 3+ times
- Track score trajectories, flagging years where processing method changed
- Test: do farms that switch to experimental methods see score increases?
- Secondary: look for score inflation over time (are competition scores rising independent of method?)

**Challenges:**
- Farm name spelling varies across years (e.g., "El Injerto" vs "Finca El Injerto")
- Need fuzzy matching (fuzzywuzzy or rapidfuzz) plus manual verification for top candidates
- Sample size for farms that actually switch methods may be small

**Output:** New notebook section — "What happens when farms change methods?"

### 2. Decompose the "country" effect

**Question:** What does "country" actually capture? Can we replace it with measurable variables?

**Why it matters:** Country is our strongest predictor (R²≈0.25) but it's unexplainable. If we can decompose it into economic, agricultural, or institutional factors, we learn something actionable.

**Approach:**
- Pull country-level indicators from the World Bank API (no auth needed):
  - GDP per capita
  - Agriculture value added (% of GDP)
  - Coffee export volume/value (UN Comtrade or ICO data)
- Add coffee-specific indicators if available:
  - Average farm size
  - % specialty vs commodity production
  - Presence of quality-focused institutions (CoE participation, SCA chapters)
- Run regression: replace country dummies with these continuous variables and see how much R² they absorb
- If economic indicators absorb most of the country effect, the story shifts from "terroir" to "investment"

**Challenges:**
- Some indicators may not be available for all 36 countries
- Country-level averages may be too coarse — within-country variation matters
- Risk of ecological fallacy (country-level GDP doesn't mean individual farms are wealthy)

**Output:** New notebook section — "What makes a coffee country?"

### 3. Merge CQI and CoE datasets

**Question:** Can we combine CQI's cupping detail with CoE's processing granularity?

**Why it matters:** CQI has attribute-level scores (aroma, body, acidity, etc.) but crude processing categories. CoE has detailed processing (anaerobic, carbonic maceration, etc.) but only total scores. Merging gives us: *do anaerobic coffees score high because of body? acidity? something else?*

**Approach:**
- Match on country + region + farm name (fuzzy)
- Even partial matches are valuable — we don't need 1:1 mapping, just enough overlap to characterize processing-attribute relationships
- Alternative: use CoE's variety+process+country combinations to impute likely cupping profiles from CQI data

**Challenges:**
- CQI and CoE use different scoring scales (CQI: 0-100 summed attributes, CoE: panel consensus)
- Time periods may not overlap perfectly
- Farm names in CQI may be less detailed than CoE

**Output:** New notebook section or enriched existing sections

---

## Suggested order

1. **Farm longitudinal analysis first** — highest impact, self-contained within CoE data, no new data fetching needed
2. **Country decomposition second** — requires World Bank API calls but the scraper pattern already exists
3. **Dataset merge third** — most complex, benefits from learnings in steps 1–2

## Data we already have

| File | Records | Key fields |
|------|---------|------------|
| `data/processed/cqi_with_climate_soil.csv` | 1,311 | cupping attributes, processing, variety, altitude, country, lat/lon, climate (7 params), soil (5 props) |
| `data/raw/cup_of_excellence.csv` | 17,211 | score, process, variety, farm, farmer, region, country, year, result_tier |
| `data/processed/climate_raw.csv` | 337,610 | monthly climate records for 265 locations |
| `data/processed/soil_raw.csv` | 3,975 | soil properties for 265 locations |
| `data/processed/geocoded_regions.csv` | 362 | region → lat/lon mappings |

## Dependencies to add

- `rapidfuzz` or `thefuzz` — for fuzzy farm name matching (workstreams 1 and 3)
- `wbgapi` or direct World Bank API calls — for country indicators (workstream 2)
