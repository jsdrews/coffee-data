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

**What are bioactive compounds?** Chemical compounds in coffee that have a measurable effect on human biology beyond basic nutrition. Caffeine is the obvious one (blocks adenosine receptors → alertness), but coffee has hundreds of others. "Bioactive" simply means "biologically active" — it does something to your cells or systems.

**Why care about preserving or enhancing them?** Because processing destroys some and creates others. Roasting degrades 50–80% of chlorogenic acids but creates melanoidins (which are prebiotic). Fermentation produces microbial metabolites that don't exist in the raw cherry. The choices a farm makes — how long to ferment, how hot to roast — literally change the health profile of the final cup. If you can show "our process retains 2x the chlorogenic acid content," that's a sellable claim to health-conscious buyers and potentially to nutraceutical companies.

**Core question:** Can fermentation conditions be tuned to enhance or preserve specific bioactive compounds? This connects questions 1-3 (microbiology + processing pipeline) to pharmacological endpoints.

**Career paths:** Natural products chemistry / pharmacognosy, food bioactives research, microbial biotechnology. Relevant institutions: CIRAD, Cenicafé, university food science programs.

## What the pipeline stages measure and why they matter

Each stage of the harvest-to-cup pipeline is a transformation that changes the bean physically and chemically. The measurements at each stage are the independent variables; cupping score is the dependent variable.

| Stage | What's actually happening | What the measurements tell you |
|-------|--------------------------|-------------------------------|
| Harvest (Brix, weight) | Sugar content of the cherry at picking | Higher Brix = riper cherry = more fermentable sugars = more flavor precursors |
| Float sorting (discard weight) | Underdeveloped/defective cherries float | What % of harvest is unusable — a quality and yield metric |
| Fermentation (temp, pH, duration) | Microbes eat sugars, produce acids, alcohols, esters | These metabolites become flavor precursors. pH drop = acid production. Temp affects which microbes dominate |
| Drying (temp, moisture, days) | Water removal, continued slow chemical reactions | Too fast = uneven drying = defects. Too slow = mold risk. Target moisture ~10–12% |
| Defect sorting (discard weight) | Remove beans with physical defects (insect damage, mold, broken) | More defects removed = cleaner cup, but also = lower yield |
| Roasting (RoR, development time, first crack) | Maillard reaction, caramelization, CGA degradation | Controls acidity, body, sweetness, bitterness in the final cup |
| Cupping (SCA score) | Standardized tasting: aroma, flavor, aftertaste, acidity, body, balance | The output variable — what everything upstream is trying to optimize |

With enough lots tracked through this pipeline, you can run regressions to find which upstream variables actually predict cupping score — and which don't matter as much as people assume.

## Data sources

### Collected (scraped/downloaded)

| Source | Records | What it provides | Scraper |
|--------|---------|-----------------|---------|
| [Phenol-Explorer](http://phenol-explorer.eu) | 69 | Polyphenol concentrations for 4 coffee beverage types (filter, espresso, Arabica filter, Robusta filter) | `scrapers/phenol_explorer.py` |
| [FooDB](https://foodb.ca) | 16,340 | Full chemical inventory — all known compounds with concentrations for Arabica, Robusta, general coffee, coffee mocha | `scrapers/foodb.py` |
| [PubChem](https://pubchem.ncbi.nlm.nih.gov) | 5,510 | Bioassay results for 5 key compounds: caffeine, chlorogenic acid, cafestol, kahweol, trigonelline (156 active) | `scrapers/pubchem.py` |
| [ChEMBL](https://www.ebi.ac.uk/chembl/) | 3,333 | Bioactivity measurements (IC50, EC50, Ki, pChEMBL) against specific protein targets | `scrapers/chembl.py` |
| [World Coffee Research](https://varieties.worldcoffeeresearch.org) | 70 | Arabica variety catalog — quality potential, yield, disease resistance, stature, lineage | `scrapers/wcr_varieties.py` |

Also cross-referenced with existing project datasets:
- **CQI** (1,311 coffees) — cupping scores, variety, processing, country
- **Cup of Excellence** (17,211 lots) — competition scores, variety, farm, region
- **NASA POWER** — climate data for farm locations
- **ISRIC SoilGrids** — soil properties for farm locations

### Not yet collected (future opportunities)

| Source | Type | Relevance |
|--------|------|-----------|
| [NCBI SRA](https://www.ncbi.nlm.nih.gov/sra) | Fermentation microbiome sequencing (16S/ITS) | Q1, Q2 — multiple BioProjects including Colombian farms |
| [DrugBank](https://go.drugbank.com/) | Approved drug interactions with coffee compounds | Q4 — clinical relevance |
| [CTD](http://ctdbase.org/) | Compound-gene-disease associations | Q4 — connects compounds to disease pathways |
| [Cenicafé](https://www.cenicafe.org/) | Colombian variety trials, 290 climate stations | Q2, Q3 — mostly PDFs, limited API |
| [MetaboLights](https://www.ebi.ac.uk/metabolights/) | Coffee metabolomics studies | Q1, Q4 — fermentation metabolite profiles |
| [IGAC](https://www.igac.gov.co/) | Colombian soil surveys | Q2 — detailed regional soil data |

See [data-sources.md](data-sources.md) for the full inventory with URLs, formats, and API details.

See [pipeline.md](pipeline.md) for the full pipeline outline: what to measure, what to prove, and how it helps Nogales.

## Data landscape

**Key gaps — where the research opportunities are:**
1. **No controlled variety-specific microbiome comparison exists.** Nobody has done Geisha vs. Bourbon vs. Typica vs. Caturra under the same fermentation conditions. This is publishable and doable with access to Nogales lots.
2. **Anaerobic fermentation is underrepresented** in published sequencing data — most studies cover traditional washed or natural.
3. **No database tracks compound fate through the full processing pipeline.** Green→fermented→dried→roasted data is scattered across journal supplementary tables.
4. **Colombian regional microbial terroir comparisons don't exist.** Huila vs. Santander (or any two Colombian departments) has not been studied microbiologically.
5. **Metabolomics-microbiome integration** — linking specific fermentation microbes to specific bioactive compounds — is the current research frontier with very little data.

Gaps 1 and 4 are directly answerable with fermentation samples from Nogales. Gaps 3 and 5 are where the harvest-to-cup data pipeline (Q3) becomes a research instrument, not just a farm management tool.

See [data-sources.md](data-sources.md) for the full inventory with URLs, formats, and API details.

## Next steps: what we can build now

The research has two layers: a **reference library** (what's already known about coffee compounds and varieties) and **experiments** (new data from Nogales fermentations and sequencing). The scrapes below build the reference library — they're prerequisite context that makes the lab work interpretable.

| Scrape | What it gives us | Which question it serves | Why it's needed |
|--------|-----------------|------------------------|-----------------|
| **Phenol-Explorer** | Baseline polyphenol inventory — what's in coffee, at what concentrations | Q4 (bioactives) | You need to know what's there before you can ask what processing does to it |
| **PubChem bioassays** | What these compounds *do* pharmacologically — target proteins, potency, mechanisms | Q4 (therapeutic potential) | Answers "why should anyone care about chlorogenic acid?" with data, not claims |
| **World Coffee Research catalog** | Agronomic and sensory profiles for 70 varieties — genetic lineage, altitude ranges, disease resistance | Q1 (variety differences) | Baseline for understanding *why* varieties might host different microbes (different mucilage, different chemistry) |
| **ChEMBL bioactivity** | Detailed potency data (IC50, EC50) for coffee compounds against specific drug targets | Q4 | The bridge between "coffee contains X" and "X could treat Y" |
| **FooDB** | Broader chemical inventory — all known coffee compounds with concentrations, not just polyphenols | Q3 + Q4 | Reference dataset for what compounds to look for at each pipeline stage |

None of these directly answer Q1 (variety microbiome) or Q2 (terroir microbiome) — those require fermentation samples and 16S/ITS sequencing, which is lab work at Nogales. But without the reference library, you wouldn't know what compounds matter, why they matter, or what to measure in those samples.

**Think of it as: scrapes = reference library, Nogales data = the experiment, pipeline = the instrument connecting them.**

## How this research helps Nogales

### Immediate (this harvest season)

- **The data pipeline (Q3) reveals where value is lost.** Structured lot tracking would surface patterns like "lots that dried at X moisture rate scored 2 points higher" or "block A discards 15% at float sorting vs 5% from block B — why?" That's margin sitting in the data.
- **Lot-specific roast optimization.** Connecting Roest profiles back to processing parameters means optimizing roast curves per lot instead of using a generic profile. A natural Geisha and a washed Caturra from the same farm want different roasts — the pipeline makes that obvious from data instead of trial and error.

### Medium-term (1–2 seasons)

- **Process control, not just recipes.** Microbial profiling (Q1) moves fermentation from "72 hours because that's what works" to "ferment until the LAB-to-yeast ratio hits this target." That's how you get consistency across lots and seasons — the difference between a recipe and a controlled process.
- **Parcel-level variety placement.** If Nogales has parcels at different elevations or soil types, understanding the microbial and chemical differences between them (Q2) means assigning varieties and processing methods to the plots where they'll perform best. Plant Geisha where the soil and microbes favor its expression, not just where there's space.

### Longer-term (competitive positioning)

- **Data-backed traceability narratives.** Specialty buyers increasingly want traceability backed by science. A farm that can say "this lot's chlorogenic acid profile was shaped by our specific fermentation protocol, verified by metabolomic analysis" is selling a fundamentally different product than "washed Geisha, 1800m." That commands premium pricing.
- **Functional coffee / bioactives market.** The pharmacognosy angle (Q4) opens markets beyond cup score — functional coffee, health-positioned products, nutraceutical partnerships. If Nogales can show their fermentation approach preserves or enhances specific bioactive compounds (e.g., higher CGA retention, specific microbial metabolites), that's a value proposition beyond flavor.
- **Research site brand equity.** Published results on variety-specific microbiome profiles or Colombian microbial terroir would make Nogales a named research site. Farms like Finca El Injerto and Hacienda La Esmeralda benefit enormously from this association with innovation — it's brand equity in the specialty market.

**The core insight:** Most specialty farms optimize for one variable — cupping score. This research gives Nogales multiple optimization axes (microbial health, bioactive content, processing efficiency, lot consistency) that all feed back into both quality and margin. The data pipeline is the foundation; everything else builds on it.

---

## Analysis findings

Analysis notebook: [`notebooks/coffee_pharmacognosy.ipynb`](../../notebooks/coffee_pharmacognosy.ipynb)

### Key findings

| Finding | Source | Strength |
|---------|--------|----------|
| Coffee polyphenols are dominated by 3 caffeoylquinic acids (~180 mg/cup combined) | Phenol-Explorer | Strong — direct measurement |
| Robusta has 1.5–2x higher CGA concentrations than Arabica | Phenol-Explorer, FooDB | Strong — consistent across databases |
| Arabica has dramatically higher lipid content (oleic acid ~54x, linolenic acid ~400x) | FooDB | Observed — may reflect preparation method differences |
| Chlorogenic acid reaches drug-like potency (pChEMBL 7.0 = 100 nM) against multiple targets | ChEMBL | Observed — in vitro, not clinical |
| Trigonelline has the highest max potency of any coffee compound (pChEMBL 7.89) but sparse data | ChEMBL | Weak — only 4 measurements with potency data |
| Caffeine's primary targets are adenosine receptors A1/A2a/A2b/A3 (3,024 records) | ChEMBL | Strong — well-characterized |
| Quality-yield tradeoff is real: Exceptional varieties are mostly Low–Medium yield | WCR (70 varieties) | Strong |
| Geisha scores 1+ point above all other varieties in Cup of Excellence (89.23 mean, n=544) | WCR + CoE | Strong — large sample |
| WCR quality ratings broadly predict CoE scores, but separation narrows at top tiers | WCR + CoE | Moderate — CoE pre-filters to top lots |

### What to measure at Nogales

Based on the reference data, the compounds most worth tracking through the harvest-to-cup pipeline:

1. **Chlorogenic acids (especially 5-CQA)** — highest concentration (~70 mg/100 ml in filter coffee), most processing-sensitive (40–80% loss during roasting), pharmacologically active against inflammation and oxidative stress targets
2. **Trigonelline** — neuroprotective, partially converts to niacin (vitamin B3) during roasting; sparse pharmacological data means new measurements are publishable
3. **Caffeine** — stable through processing but varies by variety; most-studied coffee compound with clear mechanism (adenosine receptor antagonism)
4. **Lipid profile (oleic/linolenic acids)** — affects mouthfeel and body, varies dramatically between species and likely between varieties
5. **Microbial metabolites** — fermentation-specific compounds not present in the cherry (organic acids, esters, alcohols) — this is the data that doesn't exist yet and represents the biggest research opportunity

---

## Relationship to `what-makes-coffee-score-high`

That research track asks: *what predicts cupping score?*
This one asks: *what do the microbes do, and what bioactive compounds result?*

They converge at the processing pipeline — the same data (variety, terroir, fermentation parameters, cupping outcomes) feeds both questions. Soil and fermentation data from question 3 could directly enrich the existing CQI/CoE analysis.
