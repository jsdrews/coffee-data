# Data Sources for Coffee Pharmacognosy Research

What exists, what's downloadable, and what we can scrape or mine.

---

## 1. Fermentation Microbiology — Sequencing Data

### NCBI Sequence Read Archive (SRA)

Published 16S rRNA and ITS amplicon sequencing data from coffee fermentation studies. These are raw FASTQ files downloadable via `sratoolkit`.

| BioProject | Study | What's in it | Relevance |
|------------|-------|-------------|-----------|
| [PRJNA706460](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA706460/) | Altitude effects on microbial community in anaerobic coffee fermentation (Brazil) | 16S + ITS amplicon data, multiple altitudes | Directly relevant — microbial terroir (Q2) |
| [PRJNA1254155](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1254155/) | Fermentation strategies based on O₂ availability and processing time | Sequencing data across fermentation conditions | Relevant to Q1 — process-dependent microbiome |
| [PRJNA662831](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA662831/) | Food fermentation metagenome | Broader food fermentation — may include coffee | Check for coffee-specific samples |
| [PRJNA485506](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA485506/) | Fermentation metagenome | General fermentation | Check for coffee samples |

**How to access:** Install [SRA Toolkit](https://github.com/ncbi/sra-tools), then `fastq-dump --split-files SRR_ACCESSION`. Or use the SRA Run Selector to download accession lists in bulk. **Tip:** ENA (https://www.ebi.ac.uk/ena/browser/) mirrors SRA data and provides direct HTTP/FTP FASTQ download links — often easier than sra-toolkit.

**What to do with it:** Run QIIME2 or DADA2 pipeline on the FASTQ files to generate OTU/ASV tables, taxonomic assignments, and diversity metrics. Compare across varieties/altitudes/conditions.

### Pre-Analyzed Data (skip the bioinformatics)

- **MGnify** (https://www.ebi.ac.uk/metagenomics/) — EBI's analysis platform. Some SRA-deposited coffee data has been re-analyzed here. Provides pre-computed taxonomy profiles and functional annotations in TSV/BIOM format.
- **Qiita** (https://qiita.ucsd.edu/) — Microbiome study platform. Some coffee fermentation studies may have pre-processed OTU tables.
- **FoodMicrobionet** (http://www.foodmicrobionet.org/) — Database for food-associated microbiome studies with standardized OTU tables.

### Key Papers with Supplementary Data

These papers contain processed microbial abundance tables (often in supplementary materials as Excel/CSV) that can be extracted without re-running bioinformatics:

- [De Bruyn et al. (2017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5956267/) — "High-Throughput rRNA Gene Sequencing Reveals High and Complex Bacterial Diversity Associated with Brazilian Coffee Bean Fermentation" — 260±71 bacterial OTUs, 101±24 fungal OTUs
- [Díaz-López et al. (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10969282/) — "Metataxonomic Identification of Microorganisms during Coffee Fermentation in Colombian Farms (Cesar Department)" — **Colombian farms**, directly relevant
- [Velásquez et al. (2023)](https://bmcplantbiol.biomedcentral.com/articles/10.1186/s12870-023-04182-2) — "Characterization of Rhizosphere Bacterial Microbiome and Coffee Bean Fermentation in Castillo-Tambo and Bourbon Varieties in Popayán-Colombia" — **variety comparison (Castillo vs Bourbon)** in Colombia
- [Evangelista et al. (2021)](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2021.671395/full) — "Altitude of Coffee Cultivation Causes Shifts in Microbial Community Assembly" — altitude × microbiome × biochemical compounds
- [Hernández et al. (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10418422/) — Anaerobic-fermented coffee microbial diversity + ochratoxin inhibition — relevant to Q4 (bioactivity)

**Action:** Scrape supplementary tables from these papers. Many have OTU abundance matrices and metadata as .xlsx files.

---

## 2. Bioactive Compounds — Chemical Databases

### Phenol-Explorer
**URL:** http://phenol-explorer.eu

Coffee-specific data on polyphenols, especially chlorogenic acids:
- [Coffee beverage (filter) compounds](http://phenol-explorer.eu/contents/food/552) — full polyphenol composition
- [5-Caffeoylquinic acid (5-CQA)](http://phenol-explorer.eu/compounds/475) — the main CGA in coffee
- [Total chlorogenic acid](http://phenol-explorer.eu/compounds/948) — aggregate data
- [CGA metabolites](http://phenol-explorer.eu/metabolism/polyphenol-metabolites/948) — what happens after ingestion

**Format:** Web tables, scrapable. No API, but structured HTML.
**Action:** Scrape all coffee entries — compounds, concentrations, and metabolite pathways.

### FooDB
**URL:** https://foodb.ca | **API docs:** https://foodb.ca/api_doc

Comprehensive food compound database. Coffee entries include:
- Compound identities, concentrations, and food sources
- Links to external databases (PubChem, HMDB, KEGG)

**Format:** Full MySQL dump and CSV bulk export available at https://foodb.ca/downloads. Also JSON API (beta) and `massdatabase` R package.
**Action:** Download bulk CSV/SQL, filter for Coffea entries, extract compound-concentration pairs. Cross-reference with Phenol-Explorer.

### USDA FoodData Central
**URL:** https://fdc.nal.usda.gov | **API:** https://fdc.nal.usda.gov/api-guide.html

Nutrient composition data for coffee (brewed, espresso, green bean). Less granular than Phenol-Explorer for polyphenols, but covers macronutrients, minerals, and some bioactives.

**Format:** REST API, JSON. Free API key required.

### PubChem
**URL:** https://pubchem.ncbi.nlm.nih.gov

Individual compound pages with bioactivity assay data:
- [Chlorogenic acid (CID 1794427)](https://pubchem.ncbi.nlm.nih.gov/compound/1794427)
- [Cafestol (CID 108052)](https://pubchem.ncbi.nlm.nih.gov/compound/108052)
- [Kahweol (CID 114778)](https://pubchem.ncbi.nlm.nih.gov/compound/114778)
- [Trigonelline (CID 5570)](https://pubchem.ncbi.nlm.nih.gov/compound/5570)
- [Caffeine (CID 2519)](https://pubchem.ncbi.nlm.nih.gov/compound/2519)

**Format:** REST API ([PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)). Bioactivity assay data downloadable as CSV.
**Action:** Pull all bioassay results for the key coffee compounds.

### KNApSAcK
**URL:** http://www.knapsackfamily.com

Plant metabolite-species relationship database. Search for Coffea to get compound-species pairs with references.

**Format:** Web searchable, results can be exported. Limited programmatic access.

---

## 3. Pharmacological Activity — Drug/Target Databases

### ChEMBL
**URL:** https://www.ebi.ac.uk/chembl/

Open bioactivity database — binding affinity, IC50, EC50 data for compounds against protein targets. Contains entries for chlorogenic acid, cafestol, kahweol with documented bioactivities.

**Format:** REST API, bulk SQL download, or Python client (`chembl_webresource_client`).
**Action:** Query for all coffee bioactive compounds → get target profiles, potency data.

### DrugBank
**URL:** https://go.drugbank.com

Pharmacological data on caffeine (approved drug entry), plus experimental entries for other coffee compounds.

**Format:** XML bulk download (academic license, free). API for programmatic access.

### ClinicalTrials.gov
**URL:** https://clinicaltrials.gov

Search for trials involving coffee bioactives (chlorogenic acid, cafestol, etc.) to find human pharmacological data.

**Format:** REST API at `https://clinicaltrials.gov/api/v2/studies`. JSON/CSV export. Example: `?query.intr=chlorogenic%20acid`

### CTD (Comparative Toxicogenomics Database)
**URL:** http://ctdbase.org

Curates chemical-gene-disease interactions. Caffeine and chlorogenic acid have extensive entries linking them to gene targets and disease associations.

**Format:** Bulk TSV downloads.

### LOTUS (Natural Products)
**URL:** https://lotus.naturalproducts.net

Open database linking natural products to biological sources and activities. Coffee compounds present. SPARQL endpoint for programmatic access.

---

## 4. Metabolomics — LC-MS/GC-MS Profiling Data

### MetaboLights (EMBL-EBI)
**URL:** https://www.ebi.ac.uk/metabolights/

Open repository for metabolomics studies. Search for coffee-related studies — some include raw LC-MS data and processed metabolite matrices across varieties or processing methods.

**Format:** ISA-Tab metadata + raw instrument files. Processed data often as TSV.

### Metabolomics Workbench
**URL:** https://www.metabolomicsworkbench.org/

Similar to MetaboLights. Search for coffee studies. Key review paper: [Pua et al. (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8948666/) — "Metabolomics-Based Approach for Coffee Beverage Improvement" surveys what's been deposited.

**Action:** Search both repositories for coffee datasets. Download processed metabolite abundance tables.

### GNPS (Global Natural Products Social Molecular Networking)
**URL:** https://gnps.ucsd.edu

MS/MS spectral data for natural products. Coffee-derived compound spectra are in the library. Community-shared datasets downloadable. MGF/mzML format.

---

## 5. Terroir & Agronomic Data

### ISRIC SoilGrids
**URL:** https://soilgrids.org | **API:** REST/WCS

250m resolution soil data globally. We already use this in the `what-makes-coffee-score-high` track.
- pH, organic carbon, sand/silt/clay fractions, CEC, bulk density

**Status:** Already integrated — see `data/processed/soil_raw.csv`.

### NASA POWER
**URL:** https://power.larc.nasa.gov/ | **API:** REST

Monthly climate data: temperature, rainfall, humidity, solar radiation, wind speed.

**Status:** Already integrated — see `data/processed/climate_raw.csv`.

### CHIRPS (High-Resolution Rainfall)
**URL:** https://www.chc.ucsb.edu/data/chirps

0.05° (~5km) resolution rainfall estimates, daily and monthly, 1981–present. Particularly strong for tropical regions including Colombia.

**Format:** GeoTIFF, NetCDF, BIL. FTP or API access.

### WorldClim (Bioclimatic Variables)
**URL:** https://www.worldclim.org

19 bioclimatic variables at ~1km resolution: annual mean temperature, temperature seasonality, precipitation of driest quarter, etc. Historical (1970–2000) and CMIP6 future projections.

**Format:** GeoTIFF rasters. Free download.

### IGAC (Colombian Soil Surveys)
**URL:** https://geoportal.igac.gov.co

Colombian national soil surveys by department (Huila, Santander, Nariño, etc.). Soil classification maps and land use capability maps. Some WMS/WFS layers for GIS integration.

**Format:** Shapefiles, GeoTIFF. Some data requires purchase; geoportal has free viewable layers.

### IDEAM (Colombian Climate Stations)
**URL:** http://dhime.ideam.gov.co

Ground station weather data from across Colombia, including many coffee municipalities. More granular than satellite-derived data.

**Format:** CSV/Excel. Access can be bureaucratic.

### CIAT/CGIAR Dataverse
**URL:** https://dataverse.harvard.edu (search CIAT)

Coffee suitability models under climate change (Bunn et al. studies). Datasets in shapefiles, CSVs, R data files.

### Cenicafé Digital Repository
**URL:** https://biblioteca.cenicafe.org/

Colombia's national coffee research center. Resources include:
- 290+ climatological stations across Colombia's coffee regions
- 1,028 Coffea accessions in the Colombian Coffee Collection
- Variety trial data, soil studies, agro-ecological zoning
- Publications on Castillo, Cenicafé 1, Tabi, and other Colombian varieties

**Format:** Mostly PDFs and publications. Some data tables embedded in papers. No API.
**Action:** Mine the repository for variety trial data and soil characterization studies, especially for Huila and Santander regions.

### World Coffee Research — Variety Catalog
**URL:** https://varieties.worldcoffeeresearch.org/

55 arabica varieties, 47 robusta varieties. Includes:
- Agronomic data: yield, altitude range, disease resistance
- Sensory descriptors
- Genetic background and lineage

**Format:** Web + customizable PDF. Structured HTML, scrapable.
**Action:** Scrape variety catalog into structured data. Cross-reference with CQI/CoE variety data we already have.

### SCA Meta-Analysis on Coffee Acids
**URL:** https://sca.coffee/sca-news/2021/10/19/acids-in-coffee-a-review-of-sensory-measurements-and-meta-analysis-of-chemical-composition

Specialty Coffee Association review linking chemical composition (acids) to sensory measurements. Contains aggregated data from multiple studies.

---

## 6. Processing-Stage Compound Fate

### Key review: "From Plantation to Cup"
[Ferrão et al. (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8620865/) — "From Plantation to Cup: Changes in Bioactive Compounds during Coffee Processing"

Tracks CGA, trigonelline, caffeine, and other bioactives through each processing stage (fermentation → drying → roasting → brewing). Contains compiled data tables from multiple studies.

**Action:** Extract the compound-by-stage tables from supplementary materials. This is the backbone dataset for Q4.

### Cafestol & Kahweol Review
[Ren et al. (2019)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6747192/) — "Cafestol and Kahweol: A Review on Their Bioactivities and Pharmacological Properties"

Compiled pharmacological data on the two main coffee diterpenes: anti-inflammatory, hepatoprotective, anti-cancer, anti-diabetic mechanisms.

---

## Key gaps — what doesn't exist yet

1. **No systematic variety-specific microbiome comparison.** No study has done a controlled side-by-side of Geisha vs. Bourbon vs. Typica vs. Caturra fermentation microbiomes. Most studies compare processing methods, not cultivars. This would be a novel contribution.
2. **Anaerobic fermentation microbiome data is sparse.** Most published work covers traditional washed or natural; the newer anaerobic/carbonic maceration methods are underrepresented.
3. **No single database tracks compound fate through processing stages.** The green→fermented→dried→roasted pipeline data lives scattered across journal supplementary tables and needs to be curated manually from the literature.
4. **Terroir-microbiome studies are rare.** The closest is Verce et al. (KU Leuven) comparing Ethiopian regions. Colombian regional comparisons (e.g., Huila vs. Santander) are essentially absent.
5. **Metabolomics-microbiome integration** — linking specific fermentation microbes to specific flavor precursors and bioactive compounds — is the current research frontier with very little published data.

---

## Priority for scraping/mining

| Priority | Source | Effort | Value |
|----------|--------|--------|-------|
| **1** | Phenol-Explorer coffee entries | Low — structured HTML | Baseline compound inventory |
| **2** | PubChem bioassay data (5 key compounds) | Low — REST API | Pharmacological profiles |
| **3** | NCBI SRA BioProjects (PRJNA706460, PRJNA1254155) | Medium — bioinformatics pipeline needed | Raw microbial diversity data |
| **4** | Paper supplementary tables (6+ papers above) | Medium — manual + scraping | Processed OTU tables, compound measurements |
| **5** | World Coffee Research variety catalog | Low — web scrape | Variety agronomic/sensory data |
| **6** | FooDB coffee compounds | Low — API | Compound cross-reference |
| **7** | ChEMBL bioactivity queries | Low — API | Target/potency data |
| **8** | Cenicafé repository | High — PDF mining | Colombian-specific variety/soil data |
| **9** | MetaboLights/Metabolomics Workbench | Medium — search + download | Metabolite profiles across varieties |
| **10** | CTD (compound-gene-disease) | Low — bulk TSV | Disease association data for coffee compounds |
| **11** | ClinicalTrials.gov | Low — API | Human trial data on coffee bioactives |
| **12** | CHIRPS + WorldClim | Low — GeoTIFF download | High-res climate data for Colombian terroir |
