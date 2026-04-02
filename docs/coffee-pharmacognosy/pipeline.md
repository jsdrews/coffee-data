# The Nogales Pipeline: From Cherry to Proof

A concrete outline of what needs to happen at Nogales, what it proves, and why it matters.

## The pipeline

The pipeline tracks a coffee lot from the soil it grows in to the cup it's scored in, recording data at every stage. Each stage is a transformation — chemical, physical, or biological — and the measurements capture what changed.

```
SOIL → CHERRY → FERMENTATION → DRYING → GREEN BEAN → ROASTING → CUP
  │       │          │             │          │            │         │
  │       │          │             │          │            │         └─ SCA cupping score
  │       │          │             │          │            └─ Roest profiles (RoR, dev time, end temp)
  │       │          │             │          └─ Moisture, water activity, weight, defect count
  │       │          │             └─ Daily: temp, humidity, moisture, weight
  │       │          └─ Hourly: temp, pH, Brix; samples for sequencing + chemistry
  │       └─ Cherry weight, Brix, float-test discard weight
  └─ Soil pH, mineral content; microclimate (temp, humidity, rainfall)
```

The pipeline is a **DAG** (directed acyclic graph): from a single harvest, processing branches into washed/honey/natural, each producing a separate lot with its own data trail. Running multiple processing methods on the same cherry harvest is the experimental design — it holds variety and terroir constant while varying process.

### What's measured at each stage

| Stage | Measurements | Equipment needed | Frequency |
|-------|-------------|-----------------|-----------|
| **Pre-harvest** | Soil pH, Ca/Mg/K/P, organic matter; ambient temp, humidity, rainfall | Soil test kit or lab; weather station | Once per parcel per season |
| **Harvest** | Cherry weight (kg), Brix (refractometer), float-test discard % | Scale, refractometer, water tank | Per lot |
| **Fermentation** | Temperature, pH, Brix (hourly or 2x/day); fermentation duration; fermentation method (aerobic/anaerobic, with/without mucilage) | pH meter, thermometer, refractometer | Per lot, hourly–daily |
| **Fermentation samples** | Swabs or liquid samples for 16S rRNA (bacteria) and ITS (fungi) sequencing; optional HPLC samples for compound measurement | Sterile swabs, collection tubes, cold chain to lab | 3–4 timepoints per fermentation (0h, 24h, 48h, end) |
| **Drying** | Bean temperature, ambient humidity, moisture content, weight | Moisture meter, hygrometer, scale | Daily per lot |
| **Green bean** | Final moisture content, water activity, weight, screen size, defect count/weight | Moisture meter, aw meter, screens | Per lot |
| **Roasting** | Full Roest profile: rate of rise (RoR), development time ratio, first crack time/temp, end temperature, total time | Roest roaster (already at Nogales) | Per roast |
| **Cupping** | Full SCA protocol: fragrance/aroma, flavor, aftertaste, acidity, body, balance, uniformity, clean cup, sweetness, overall | Cupping setup, trained cuppers | Per lot |

### What's new vs. what Nogales probably already does

Most farms already record harvest weight, moisture, and cupping scores. The **new** work is:

1. **Structured fermentation monitoring** — hourly pH and temperature logs, not just "fermented for 72 hours"
2. **Microbial sampling** — collecting swabs/liquid at multiple timepoints during fermentation for sequencing
3. **Chemical sampling** — optional HPLC samples at cherry, post-fermentation, green, and roasted stages to track compound fate
4. **Consistent lot tracking** — same lot ID from cherry through cup, with all measurements linked

Items 2 and 3 require a lab partner (university or Cenicafé). Items 1 and 4 are just discipline and a spreadsheet (or app).

## What we prove

### Hypothesis 1: Different varieties host different microbes under the same fermentation conditions

**Design:** Take 3+ varieties grown at Nogales (e.g., Geisha, Bourbon, Caturra) from the same harvest window. Process all three with identical washed anaerobic fermentation. Collect microbial samples at 0h, 24h, 48h, and end of fermentation.

**What the data shows:** 16S/ITS sequencing reveals whether the microbial community composition (which species, at what abundance) differs by variety. Our reference data shows varieties differ in mucilage sugar content and pH, which creates selective pressure — but nobody has measured whether this actually produces different microbial communities under controlled conditions.

**What it proves:** That variety selection is a fermentation variable, not just an agronomic one. The cherry isn't a passive substrate — it shapes which microbes thrive.

**Why it's publishable:** No controlled variety-comparison microbiome study exists in the literature. This would be a first.

### Hypothesis 2: The same variety produces different microbial profiles at different sites

**Design:** If Nogales has parcels at different elevations or soil types, ferment the same variety (e.g., Bourbon) from two parcels using identical processing. Compare microbial profiles.

**What the data shows:** Whether "microbial terroir" is real — do indigenous soil microbes on the cherry surface seed the fermentation differently based on where the tree grows?

**What it proves:** That terroir isn't just about altitude and rainfall — it includes the invisible microbial community. Two farms at the same altitude in different regions could produce fundamentally different fermentations from the same variety.

### Hypothesis 3: Fermentation conditions affect bioactive compound retention

**Design:** Track chlorogenic acid (5-CQA), trigonelline, and caffeine concentrations at 4 stages: fresh cherry → post-fermentation → green bean → roasted bean. Compare across processing methods (washed vs. natural vs. honey) from the same harvest.

**What the data shows:** How much of each compound survives each transformation. Our reference data tells us filter coffee contains ~70 mg/100ml of 5-CQA and that roasting degrades 40–80% — but nobody has measured where in the pipeline the loss happens, or whether fermentation method affects the starting point for roasting.

**What it proves:** That processing decisions have measurable chemical consequences beyond flavor. A specific fermentation protocol might retain 2x the chlorogenic acid of another — that's a quantifiable health claim.

**Requires:** HPLC analysis at a university lab (Cenicafé, Universidad Nacional, or similar). ~$50–150 per sample depending on the panel.

### Hypothesis 4: Upstream variables predict cupping score

**Design:** After 2+ seasons of structured lot tracking (hypothesis-agnostic — just record everything), run regressions: which upstream measurements (Brix at harvest, fermentation pH curve, drying rate, soil pH, etc.) actually predict cupping score?

**What the data shows:** Which variables matter and which don't. Maybe Brix at harvest predicts 30% of score variance and fermentation duration predicts 5%. Maybe soil pH matters more than altitude. We don't know yet — and neither does anyone else with this level of granularity from a single farm.

**What it proves:** Which levers Nogales can actually pull to improve quality, and which are noise. Replaces intuition with evidence.

## How this helps Nogales

### Immediate value (this season, no lab required)

| Action | What it costs | What it gives |
|--------|--------------|---------------|
| Structured lot tracking (harvest → cup) | Time: ~15 min per lot per day | Identifies where value is lost. "Block A discards 15% at sorting vs 5% from block B — why?" |
| Fermentation pH/temp logging | pH meter (~$50), thermometer, discipline | Moves from "72 hours" to "ferment until pH hits 4.2." Consistency across lots and seasons |
| Split-processing experiments | Same harvest, different methods | Direct comparison: does this Geisha score higher washed or natural? Data instead of guessing |
| Lot-specific roast curves | Roest profiles linked to processing data | Optimize roast per lot instead of one-size-fits-all. A natural Geisha wants a different roast than a washed Caturra |

### Medium-term value (1–2 seasons, needs lab partner)

| Action | What it costs | What it gives |
|--------|--------------|---------------|
| Microbial profiling (16S/ITS) | ~$100–200 per sample, 12–20 samples per experiment | Scientific proof that Nogales' fermentation is unique. Publishable data. Process control based on microbial targets, not time |
| Compound tracking (HPLC) | ~$50–150 per sample, 16–24 samples per experiment | Quantified bioactive content at each stage. "Our washed process retains 60% of chlorogenic acids vs 40% for the industry average" |
| Cross-parcel terroir comparison | Same as above, applied to 2+ parcels | Parcel-level variety placement: plant Geisha where soil microbes favor its expression |

### Longer-term value (competitive positioning)

- **Functional coffee claims.** If compound tracking shows Nogales' process retains unusually high levels of chlorogenic acid or produces specific microbial metabolites, that's a marketable health story — not vague "antioxidants" but specific compounds with documented pharmacological activity (our ChEMBL data shows chlorogenic acid at drug-like potency against inflammation targets)
- **Research site brand equity.** Published papers naming Nogales as the study site = permanent marketing. La Esmeralda and El Injerto built their brands partly through research association
- **Premium pricing justification.** "This lot scored 88" justifies a price. "This lot scored 88, retains 2x the normal chlorogenic acid content, and was fermented under a microbial profile optimized for flavor precursor production" justifies a higher one
- **Data moat.** After 3+ seasons of structured data, Nogales would have the most granular single-farm dataset in specialty coffee. That's a competitive advantage that compounds over time — every season's data makes the models better

## What we've already built (the reference library)

The 5 datasets we scraped provide the context that makes all of the above interpretable:

| Dataset | Role in the pipeline |
|---------|---------------------|
| **Phenol-Explorer** (69 records) | Baseline: what polyphenols are in coffee and at what concentrations. Without this, compound tracking has no reference point |
| **FooDB** (16,340 records) | Full chemical inventory: what compounds to look for at each pipeline stage. The checklist for HPLC panels |
| **PubChem** (5,510 bioassays) | Why specific compounds matter: which are pharmacologically active and against what targets. The "so what?" for compound retention data |
| **ChEMBL** (3,333 records) | How potent these compounds are: pChEMBL values quantify therapeutic potential. The bridge from "coffee contains X" to "X could treat Y" |
| **WCR Varieties** (70 profiles) | Why varieties differ: genetic lineage, quality-yield tradeoffs, agronomic characteristics. Context for why Geisha and Bourbon might host different microbes |

These datasets are the reference library. Nogales provides the experiment. The pipeline connects them.

## Minimum viable experiment

If Nogales wants to start with the smallest useful experiment:

1. **Pick 2 varieties** from the same harvest window (e.g., Geisha + Bourbon)
2. **Process both washed anaerobic**, identical conditions
3. **Log pH and temperature** every 4–6 hours during fermentation
4. **Collect 4 swab samples** per fermentation (0h, 24h, 48h, end) → send to a university lab for 16S/ITS sequencing
5. **Cup both lots** using full SCA protocol
6. **Record everything** in a structured format (we can build the data entry template)

That's ~8 microbial samples (~$800–1600 for sequencing), plus time and discipline. It answers Hypothesis 1 and produces publishable data. Everything else scales from there.
