# Field Observations

Observations and updates from Nogales farm, Bruselas, Huila.

---

## April 6: Project update — three active workstreams

She has three components running in parallel, all connected through the soil → plant → cherry → cup pipeline.

### Component 1: Lab microcosm study (pH stabilization) — wrapping up

Studying the effects of fresh coffee byproducts on soil pH vs. mature compost.

**What Nogales does:** Coffee waste (fermentation mosto, pulp, husks, parchment, grounds) + food scraps → turned and dried for ~1 month → stabilized mature compost with safe pH. This is applied to coffee plants (Geisha gets the premium treatment).

**What she's testing:** Fresh mosto or fresh pulp added directly to soil vs. mature compost — tracking visual changes and pH over time. First round ran too long with concentrations too high. Now repeating:
- 100g soil, lower concentrations of mosto/pulp
- pH readings at day 1, 3, 5, 7
- Goal: verify literature that pH stabilizes after ~1 week
- Jars prepared April 6, waiting on fresh mosto/pulp (arriving ~April 7)

**Why it matters:** Many farms around Bruselas dump fresh pulp directly onto coffee plants without composting. Fresh byproducts are acidic and potentially phytotoxic. Showing that pH takes ~1 week to stabilize — and that Nogales' month-long composting process is scientifically sound — is a teachable finding for the local coffee community.

**Time required:** Minimal. 4 pH readings over one week, ~15 min per reading. Done by ~April 14.

### Component 2: Microbial inoculation tanks (second farm) — new

Nogales has a **second property** that's just now becoming harvestable (plants have been growing for years). This farm uses a more advanced soil treatment: **microbial inoculation**.

**Setup:** They buy ~1 kg at a time of commercially available beneficial soil microbes and multiply them in 1,000-liter tanks before application.

**Organisms identified:**
- **Bacillus** spp. — soil probiotic bacteria. Nitrogen fixation, phosphorus solubilization, disease suppression. Widely used in agriculture as biofertilizer.
- **Beauveria** (likely *B. bassiana*) — entomopathogenic fungus. Infects and kills coffee berry borer (*Hypothenemus hampei* / broca) and other insect pests. Biological pest control alternative to chemical pesticides.
- **Metarhizium** (likely *M. anisopliae*) — another entomopathogenic fungus. Complementary to Beauveria, different host range. Also used for broca control.

**What the farm wants:**
1. Model growth curves of these organisms in the tanks
2. Identify/flag potential contamination

**Challenges:**
- Mixed-culture growth modeling is non-trivial without proper microbiology lab equipment
- Contamination detection ideally requires plating, microscopy, or sequencing
- Tank conditions (temperature, aeration, nutrient medium, pH) all affect growth dynamics
- She may need to scope this to what's achievable with available equipment

**Why it matters:** This is biological crop management — replacing chemical pesticides and synthetic fertilizers with targeted beneficial microbes. If she can characterize the tank dynamics and help the farm quality-control their inoculant production, that's both practically useful and scientifically interesting. The broca (coffee berry borer) is the #1 pest threat to specialty coffee worldwide.

### Component 3: Harvest-to-cup data pipeline — ready, waiting for cherry

The lot tracking framework we built. Harvest is imminent ("very, very soon"). See [pipeline.md](pipeline.md) and [six-week-plan.md](six-week-plan.md) for the full design.

### How the three components connect

These are one story at three scales:

```
SOIL TREATMENT → PLANT HEALTH → CHERRY QUALITY → FERMENTATION → CUP
      ↑                                                   ↑
  Component 1 & 2                                   Component 3
  (what goes into the soil)                   (what comes out of the cherry)
```

- Component 1 proves Nogales' composting practice is scientifically sound
- Component 2 characterizes their advanced biological inputs (beneficial microbes)
- Component 3 captures what those inputs ultimately produce (cherry quality, cupping score)

The unifying narrative: **soil health is upstream of everything in specialty coffee.** Most farms optimize at the processing stage (fermentation, drying, roasting). Nogales is also optimizing at the soil stage — and they're doing it with both traditional methods (mature compost) and advanced methods (microbial inoculation). The data pipeline connects soil inputs to cup outputs.

### Timeline

| Week | Comp 1 (pH study) | Comp 2 (inoculation tanks) | Comp 3 (harvest pipeline) |
|------|-------------------|---------------------------|--------------------------|
| Apr 6–12 | Add mosto/pulp, pH at day 1, 3, 5, 7 | Visit second farm, document tank setup, sample if possible | Finalize lot tracking, confirm equipment |
| Apr 13–19 | **Done.** Write up | Research growth models, plan sampling | Watch for first ripe cherry |
| Apr 20+ | — | Tank sampling if access available | **Harvest starts.** Full pipeline active |

Component 1 is trivial work — 4 readings in a week. It doesn't compete with anything else. Component 2 needs scoping (what's achievable without a full lab?). Component 3 is the main event once cherry arrives.

### Soil care at Nogales — variety-specific treatment

From the April 3 walk and WCR data:
- **Geisha receives the mature compost** (premium treatment). Geisha is WCR-classified as Low yield, Exceptional quality, Susceptible to disease — a demanding variety that responds strongly to nutrition.
- **Tipica babies** are also compost-treated (visible in photos — dark compost mounds around seedlings).
- **Java** has "low fertilizer requirement" per WCR — hardier, less demanding.
- **The second farm** goes further with microbial inoculation (Bacillus + Beauveria + Metarhizium) — targeted biological inputs beyond just compost.

This suggests Nogales is already making variety-specific soil decisions, even if not explicitly framed that way. The Geisha gets the best compost because it needs it most and returns the most value.

---

## April 3: Farm walk observations

## Varieties observed

Nogales has at least 5 varieties planted in separate lots:

| Variety | Lot name | Cherry status (Apr 3) | Plant maturity | Planting density | Notes |
|---------|----------|----------------------|----------------|-----------------|-------|
| Yellow Bourbon | Lote Aguacate | Sparse, green, unripe | Short mature trees | Well-spaced, dispersed | Treated with mature compost |
| Orange Bourbon | — | Green, denser at bottom branches, sparse at tops | Mix of tall mature + babies | Moderate spacing | Tallest trees on the farm, some very tall |
| Bourbon Rojo ("Brojo") | — | Densest cherry of any lot, some nearly full trees | Mature | Densely planted, rows visible | Cherry concentrated toward tops — may indicate recent stumping |
| Java | — | Pretty bare overall | Grows tall, mature | Densely planted, distinct rows | Similar planting pattern to Brojo |
| Tipica | — | No cherries at all, only buds | Almost all babies (~1 year) | ~4 feet apart, spread out | Recently planted, compost-treated, branches at hip height |

## Harvest timing assessment

**Harvest has not started as of April 3.** Evidence:
- Cherries overwhelmingly green/unripe across all lots
- Only a few scattered red cherries visible (on Brojo trees)
- Tipica has only buds — no flowers, no fruit
- Densest cherry loads (Brojo) are still weeks from ripe

**Estimated first pick:** Late April to mid-May for earliest lots (Brojo appears furthest along). Some lots may not be pickable until May–June.

**Tipica will not produce this season.** The lot is almost entirely baby plants (~1 year old) — first meaningful harvest likely 2028–2029.

This confirms the NASA POWER climate model (primary harvest April–June) but places the start later than the earliest estimate.

## Implications for the research plan

### Option A (leave mid-May) is significantly constrained
- She may catch the very first pick of the earliest lots (Brojo, possibly Orange Bourbon)
- Unlikely to have enough cherry for multiple variety comparisons
- No time for drying + roasting + cupping cycle
- Still valuable: fermentation experiments on whatever cherry is available, plus all the setup work

### Option B (stay through harvest) becomes much more important
- Full harvest window (May–June) gives access to multiple varieties as they ripen sequentially
- Enough time for complete pipeline cycles (cherry → cup)
- Bourbon Rojo ripening first, then Orange Bourbon, then Yellow Bourbon, then Java — natural sequencing for variety comparison

### Available variety comparisons
- **Three Bourbon color variants** (Yellow, Orange, Rojo) on one farm is excellent — similar genetics, different phenotypes. Direct comparison under identical fermentation reveals whether color variant affects microbial community or cup profile.
- **Bourbon vs. Java** — different genetic backgrounds (Bourbon-type vs. Ethiopian landrace), both classified "Very Good" quality in WCR, both grown at the same farm
- **Tipica is out for this season** — too young to produce harvestable cherry

### Questions to ask the farm
1. When was each lot planted? (Establishes plant age and expected productivity)
2. Have any lots been stumped recently? (Would explain Brojo's top-heavy cherry pattern)
3. What was last season's harvest timing? (Best predictor of this season)
4. When do they expect first pick this season?
5. What processing methods have they used for each variety?

## Her questions — answers from the data

### How long before a baby coffee plant produces harvestable cherry?

Arabica at ~1800m in Colombia:
- **Year 1:** Vegetative growth only (what the Tipica babies are now)
- **Year 2:** May flower, but yields negligible. Some farmers strip early fruit to redirect energy to roots/branches
- **Year 3:** First small harvest (~1–2 lbs cherry per tree)
- **Year 4+:** Full production (~5–10 lbs cherry per tree per year)
- **Productive lifespan:** 20–30+ years with proper management (pruning, stumping, nutrition)

WCR catalog lists "Year of First Production" for some varieties but this field is not consistently populated.

### Can you pick from baby plants?

Yes, but yields are tiny. The 1–2 year old plants with a few cherries are technically harvestable but barely worth picking individually. Deliberate stripping of early fruit is a common practice — it sacrifices a small first harvest for stronger long-term plant development.

### Why are some mature plants bare at the start of harvest?

Multiple possible causes:
- **Biennial bearing:** Coffee alternates between heavy and light years. Last season's heavy producer may be resting.
- **Nutrient depletion:** Heavy production exhausts K, N, P. Without replenishment, next cycle is sparse.
- **Uneven flowering:** Irregular rain timing → poor flower set.
- **Plant age:** Very old plants (15+ years) decline without stumping.
- **Microsite variation:** Shade, drainage, and soil depth vary tree-to-tree.

### Is sparse-tops / dense-bottoms specific to Orange Bourbon?

No — it's a **tall variety characteristic**:
- Coffee fruits on lateral branches. Lower branches are older = more fruiting nodes.
- Tall varieties (Bourbon, Typica, Java — all classified "Tall" by WCR) invest in vertical growth. Upper branches are newer, fewer fruiting nodes.
- This is one reason farms periodically **stump** plants (cut trunk to ~30cm to force lateral regrowth).

The Brojo trees showing the opposite pattern (cherries concentrated at tops) may indicate:
- Recent stumping → newer regrowth at top is the current fruiting wood
- Or different lot age / management history

### What is "Brojo"?

Almost certainly **Bourbon Rojo** (Red Bourbon). She alternates between "Brojo" and "Roho" (= Rojo, Spanish for "red") in her notes. This is the classic red-fruited Bourbon, as distinct from the Yellow Bourbon and Orange Bourbon lots on the farm.

Having three Bourbon color variants (Yellow, Orange, Rojo) on one farm is valuable for research — similar genetic background, different phenotypes. A controlled fermentation comparison across all three would reveal whether color variant affects microbial community composition or cup profile.
