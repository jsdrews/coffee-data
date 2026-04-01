# Coffee Pharmacognosy

Fermentation-to-function coffee science: how variety, terroir, and processing shape microbial communities and bioactive compounds with therapeutic potential.

## Research questions

### 1. Variety-dependent microbial profiles in washed fermentation

How does the microbial profile (bacteria + yeast diversity and relative abundance) during standard anaerobic washed fermentation differ across varieties — Geisha, Orange/Pink Bourbon, Typica, Caturra, etc.?

**Key considerations:**
- Mucilage composition (sugar concentration, pH, organic acid ratios, pectin structure) varies by variety and creates selective pressure on microbial communities
- Dominant genera include Leuconostoc, Lactobacillus, Weissella (LAB) and Pichia, Saccharomyces, Hanseniaspora (yeasts)
- Microbial succession follows a general arc (aerotolerant → strict anaerobes as O₂ depletes and pH drops), but timing and dominant species shift by variety
- Metagenomic sequencing (16S rRNA for bacteria, ITS for fungi) is the gold standard methodology

### 2. Microbial terroir — same variety, different regions

A Geisha at 1800m in Bruselas, Huila won't express the same microbial profile or sensory outcome as a Geisha at 1800m in Santander. Factors beyond altitude:

- **Soil microbiome** — indigenous microbial community on cherry surfaces at harvest is seeded from soil; Huila (volcanic) vs Santander (sedimentary) differ dramatically
- **Soil chemistry** — pH, mineral content (Ca, Mg, K, P), organic matter
- **Microclimate** — humidity, diurnal temperature range, rainfall, UV exposure
- **Implication:** altitude alone is insufficient; "microbial terroir" is the relevant concept

### 3. Harvest-to-cup data pipeline (Nogales application)

Map a single lot (e.g., Geisha) from harvest through roasting, tracking data at every step:

| Stage | Data points |
|-------|-------------|
| Pre-harvest | Soil pH, rainfall, microclimate |
| Harvest | Cherry weight (kg), Brix |
| Sorting | Float test discard weight, density sorting |
| Processing (per method) | Fermentation temp, pH, duration; drying temps, moisture (daily); weight at each stage; defect discard weights |
| Post-processing | Green bean weight, moisture content, water activity |
| Roasting | Roest machine profiles (RoR, development time, first crack, end temp) |
| Cupping | SCA score breakdown |

This pipeline is a DAG — each processing method (natural/honey/washed) branches from the same harvest input. Applicable as a reusable template across varieties x processes per season.

**Goal:** Identify which upstream variables most strongly predict cupping outcomes (regression from soil-to-cup).

### 4. Bioactive compounds and therapeutic potential

Compounds of interest at the intersection of fermentation microbiology and pharmacology:

| Compound class | Examples | Bioactivity | Processing fate |
|---------------|----------|-------------|-----------------|
| Chlorogenic acids (CGAs) | 5-CQA, 3-CQA | Antioxidant, anti-inflammatory, neuroprotective | Degraded significantly during roasting |
| Trigonelline | — | Neuroprotective | Partially converts to niacin (B3) during roasting |
| Melanoidins | — | Prebiotic, antioxidant, metal-chelating | Formed during Maillard reaction in roasting |
| Microbial metabolites | Bioactive peptides, exopolysaccharides, SCFAs | Various | Produced during fermentation |
| Diterpenes | Cafestol, kahweol | Anti-inflammatory, potentially anti-carcinogenic | Largely retained through roasting |
| Caffeine | — | Stimulant, synergistic effects with other coffee compounds | Relatively stable through processing |

**Core question:** Can fermentation conditions be tuned to enhance or preserve specific bioactive compounds? This connects questions 1-3 (microbiology + processing pipeline) to pharmacological endpoints.

**Career paths:** Natural products chemistry / pharmacognosy, food bioactives research, microbial biotechnology. Relevant institutions: CIRAD, Cenicafé, university food science programs.

## Data landscape summary

**What exists and is accessible:**
- Fermentation microbiome sequencing data on NCBI SRA (multiple BioProjects, including Colombian farms and altitude comparisons)
- Chemical compound databases with API/bulk access: Phenol-Explorer (polyphenols), FooDB (bulk CSV/SQL), PubChem (bioassays), ChEMBL (target/potency)
- Pharmacological and clinical data: ChEMBL, DrugBank, CTD (compound-gene-disease), ClinicalTrials.gov
- Climate and soil data already integrated in this project (NASA POWER, SoilGrids), plus CHIRPS, WorldClim, IGAC (Colombian soil surveys)
- World Coffee Research variety catalog (55 arabica varieties, scrapable)
- Cenicafé digital repository (Colombian variety trials, 290 climate stations — mostly PDFs)

**Key gaps — where the research opportunities are:**
1. **No controlled variety-specific microbiome comparison exists.** Nobody has done Geisha vs. Bourbon vs. Typica vs. Caturra under the same fermentation conditions. This is publishable and doable with access to Nogales lots.
2. **Anaerobic fermentation is underrepresented** in published sequencing data — most studies cover traditional washed or natural.
3. **No database tracks compound fate through the full processing pipeline.** Green→fermented→dried→roasted data is scattered across journal supplementary tables.
4. **Colombian regional microbial terroir comparisons don't exist.** Huila vs. Santander (or any two Colombian departments) has not been studied microbiologically.
5. **Metabolomics-microbiome integration** — linking specific fermentation microbes to specific bioactive compounds — is the current research frontier with very little data.

Gaps 1 and 4 are directly answerable with fermentation samples from Nogales. Gaps 3 and 5 are where the harvest-to-cup data pipeline (Q3) becomes a research instrument, not just a farm management tool.

See [data-sources.md](data-sources.md) for the full inventory with URLs, formats, and API details.

## Relationship to `what-makes-coffee-score-high`

That research track asks: *what predicts cupping score?*
This one asks: *what do the microbes do, and what bioactive compounds result?*

They converge at the processing pipeline — the same data (variety, terroir, fermentation parameters, cupping outcomes) feeds both questions. Soil and fermentation data from question 3 could directly enrich the existing CQI/CoE analysis.
