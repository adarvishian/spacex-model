# AI Stack Module — Architecture Scoping Document

**Status**: Architecture-only scoping, parallel build. Not yet a sprint spec. Drops into Sprint 6 (deferred) of the SpaceX Rebuild v2 once locked.
**Author**: Mach33 (Vlad + Claude)
**Date**: 2026-05-22
**Builds on**: 1 GW AI Value Chain Model (revenue side, May 2026), AI Stack Cost Margins Model (margins side, May 2026)
**Constitutional reference**: `01_Lessons_Learned.md`, `02_Architecture_and_Methodology.md`, `Model Execution Rules.md` (SpaceX Rebuild v2)
**Thesis reference**: T-001 (ODC growth-multiple), T-002 (Starship priority queue), T-006 (multi-planetary AI-stack platform)
**Spelling note**: this document uses **"Terafab"** to match the source Excel models (`Mach33_1GW_AI_Value_Chain_Model.xlsx`, `Model_ AI Stack Cost Margins.xlsx`). The Mach33 memory file and T-006 thesis spell it **"Terrafab"** (double-r). Going forward, workbook + analysis outputs standardize on "Terafab" (single-r) per the May 2026 published analyses.

---

## 0. Context and scope of this document

This document locks the **architectural decisions** for the AI Stack module before any workbook cell is written. It does not specify formulas, cell addresses, or row layouts — those belong to the Sprint 6 spec that follows once Vlad signs off on the architecture.

The build runs in parallel to the rebuild-v2 trunk (Sprint 7 just landed; Sprint 6 is deferred pending exactly the epistemic locks this document is meant to close). The deliverable from this work stream is a **standalone AI Stack workbook** that proves out the structure end-to-end; once stable, the structure ports into the SpaceX model as Sprint 6's module.

Mirroring the S-1 historicals parallel build pattern: separate workbook, separate chat lineage, ports into the trunk after the architecture is battle-tested.

**Two source models feed this scoping**:

1. **1 GW AI Value Chain Model** — single-GW reference unit, single-year, steady-state. Establishes revenue per layer ($41.6B/GW gross stack, $25.1B/GW end-user TAM) and the three SpaceX business-model configurations (A Full-stack, B Wholesale, C Hybrid).
2. **AI Stack Cost Margins Model** — same single-GW reference, layers margin profiles on top (L1 40% / L2 67% / L3 50% / L4 15% / L5 5% EBITDA, base). Stage 2 walks the cost cascade through the three configurations.

Both are **per-GW, steady-state** models. The architecture's main job is to convert them into a **2025–2050 yearly module** that respects the rebuild-v2 conventions (vending-machine, anchor-and-offset, allocator OUT contract, queue gate, MC discipline).

**What this document does**:

- Maps the NVIDIA five-layer framework onto three sub-modules as requested (Compute / Application / Orchestration), with Energy and Chips handled as upstream COGS.
- Answers the four open epistemic questions that deferred Sprint 6: product ramp method, PFLOP-hr derivation, IRR engine choice, CapEx vs R&D treatment.
- Specifies terrestrial vs ODC split.
- Names the calibration anchors and the MC register.
- Lists open decisions for Vlad before workbook construction begins.

**What this document does NOT do**:

- Specify formulas, cell addresses, or row layouts (Sprint 6 spec job).
- Lock the workbook file naming or versioning (Vlad's call).
- Resolve the Application IRR engine architecture (flagged as open question §11).
- Pre-commit the Pr(A) / Pr(B) / Pr(C) credence weights (treated as MC inputs).

---

## 1. The five-layer framework, mapped to three sub-modules

The two analyses use NVIDIA's five-layer decomposition (per Huang GTC 2026 keynote, Mach33-revised). The user has requested three sub-modules. The mapping is:

| NVIDIA layer | Sub-module placement | Role |
|---|---|---|
| **L1 Energy** ($0.7B/GW, 40% EBITDA) | Upstream COGS into Compute | Internal cost line on Compute; terrestrial vs ODC switches the source |
| **L2 Chips** ($6.6B/GW, 67% EBITDA) | Upstream COGS into Compute, with Terafab toggle | Internal cost line on Compute; toggle decides if Terafab captures the margin or NVIDIA does |
| **L3 Infrastructure** ($9.2B/GW, 50% EBITDA) | **Sub-module 1: Compute** | Sells $/PFLOP-hr to internal Application + external tenants |
| **L4 Model + Application** ($20.1B/GW, 15% EBITDA) | **Sub-module 2: Application** | Sells inference + first-party applications (Grok + xAI consumer/enterprise) |
| **L5 Orchestration** ($5.0B/GW, 5% EBITDA) | **Sub-module 3: Orchestration** | Sells agentic-workflow / domain-specific products (Cursor, etc.) |

**Why this mapping** (and not 5 sub-modules to mirror the NVIDIA layers):

- **L1 and L2 are not standalone businesses inside SpaceX** in the modelled horizon. They are inputs to Compute. Energy is purchased (or generated BTM); chips are purchased (or built via Terafab).
- **Terafab is the highest-EBITDA-dollar internalization lever in the cascade** ($4.4B/GW at NVIDIA-parity, layer-additive, business-model-independent per the margins analysis). But it sits structurally as a chip-supplier business, not a stack-revenue business. **Terafab gets handled as a toggle in L2 COGS, not as a separate sub-module.** If Terafab toggle = ON, the L2 margin accrues to SpaceX as internal transfer revenue (eliminated at Group P&L); if OFF, NVIDIA captures it and SpaceX pays gross.
- **The three sub-modules above match the T-006 thesis layering** (Cursor → LLMs → Hosting). The framing is consistent across deliverables.
- **It keeps the IRR allocator coherent.** Only Compute participates in the cash queue (the others are R&D-driven, not CapEx-driven — see §11).

### 1.1 What about Terafab as its own module?

Open question deferred to Vlad. Two viable structures:

- **Option A (default in this scoping)**: Terafab is a toggle inside L2 COGS on Compute. Internal transfer mechanics handle the captured margin. No standalone Terafab tab.
- **Option B**: Terafab gets its own sub-module (4th tab) — Chips revenue is $/GPU × GPU build, COGS is fab operations, and SpaceX-Compute is the only consumer (internal transfer at NVIDIA-parity price).

**Argument for Option A**: keeps the AI Stack module at three sub-modules per user instruction; Terafab CapEx is addressed in a separate Mach33 piece (per the margins analysis disclaimer); a toggle preserves model-A/B/C parity (the L2 capture is identical in all three configurations).

**Argument for Option B**: Terafab has its own CapEx schedule, ramp curve, and per-product IRR. It IS a business inside the platform per T-006 thesis. Carving it out preserves the orthogonality the margins analysis emphasised.

**Recommendation**: Option A for the parallel build (architecture stays at three sub-modules per request); revisit when the standalone workbook proves out the L2 capture mechanics. If the toggle gets ugly to model, escalate to Option B.

---

## 2. Workbook architecture

### 2.1 Tab list

Standalone parallel-build workbook. Tab order:

1. **README** — versioning, sources, methodology locks (mirrors `02_Architecture_and_Methodology` excerpts for the AI Stack module).
2. **Assumptions** — full MC register (7-column layout per Rebuild v2: cell ref, label, base, MC min, MC max, MC distribution, notes).
3. **Compute Supply** — physical-input tab: kW deployed → PFLOP-hr/yr supply (terrestrial + orbital split). This is the upstream supply tab; Compute reads from it.
4. **Compute** — Sub-module 1. Vending-machine P&L. Reads PFLOP-hr from Compute Supply; sells to internal Application + external tenants.
5. **Application** — Sub-module 2. Vending-machine P&L. Consumes PFLOP-hr from Compute (internal transfer at $/PFLOP-hr internal price); sells inference and first-party applications.
6. **Orchestration** — Sub-module 3. Vending-machine P&L. Consumes Application API output (internal transfer at L4 internal price); sells agentic-workflow products.
7. **Business Model Switch** — credence-weighted blend of Models A / B / C. Drives which layers SpaceX retains revenue from.
8. **Group AI Stack P&L** — module roll-up. Inter-module eliminations + conservation checks.
9. **Calibration** — back-tests vs the per-GW reference numbers from both source models. ±5% tolerance per Rule 23.
10. **Claude Log** — sprint-by-sprint history.

**Note** on tab count: 7 working tabs (excluding README, Calibration, Claude Log) is more than a typical single-module sprint. The AI Stack module is unusually rich because it spans three commercial layers; the additional tabs are the load-bearing scaffolding that makes the layer separation tractable.

### 2.2 Year horizon

Standard Rebuild v2 horizon: **2025 → 2050, columns D:AC.** Year header at row 4 (D4=2025, ..., AC4=2050). Year offset at row 5 (D5=0, E5=1, ..., AC5=25).

Anchor-and-offset (Rule 23) applies throughout. No prior-column chasing on deterministic ramps.

### 2.3 Allocator OUT contract

Every sub-module exposes the canonical 11 labels (`02_Architecture §4.2`):

1. Total Revenue
2. COGS Total
3. Gross Profit / Module EBITDA
4. EBIT
5. CapEx
6. Module FCF
7. Spot IRR
8. Forward IRR Y+2
9. Blended IRR
10. Capacity Demand (PFLOP-hr or kW)
11. Capital Deployed (cumulative)

Application + Orchestration have IRR rows that may evaluate to N/A or `IFERROR(..., 0)` depending on the IRR engine choice resolved in §11. Capacity Demand on Application/Orchestration is denominated in PFLOP-hr (their consumption from Compute).

### 2.4 Inter-module flows + eliminations

Three internal flows. Each flow follows the four-step pattern (Rule 21):

| Flow | Source | Consumer | Internal price | Eliminated at |
|---|---|---|---|---|
| **F1** Chips → Compute | Terafab toggle ON: internal transfer at NVIDIA-parity ASP × GPU count. Toggle OFF: external NVIDIA market price (no internal flow). | Compute COGS | NVIDIA-parity ASP (Assumptions input) | Group AI Stack P&L when toggle ON |
| **F2** Compute → Application | Compute sells PFLOP-hr to Application | Application COGS | $/PFLOP-hr internal (Compute's L3 unit price) | Group AI Stack P&L |
| **F3** Application → Orchestration | Application sells inference API to Orchestration (Cursor consumes Grok or external) | Orchestration COGS | $/PFLOP-hr × Orchestration's inference share of revenue (Application's L4 unit price) | Group AI Stack P&L |

Conservation row on Group AI Stack P&L verifies, for each year and each flow, that source-side internal transfer revenue equals sum of consumer-side internal COGS. Target = exact zero, ±$1mm tolerance.

**Per Architecture §4.4**: module IRR engines see gross flows (Compute's IRR includes its internal sales to Application); consolidation sees netted flows. Both views are correct.

---

## 3. Compute Supply tab — the PFLOP-hr derivation (open question #2 closed)

This is the load-bearing physical-input tab. It converts deployed power (kW) into sellable inference capacity (PFLOP-hr/yr).

### 3.1 Derivation chain (single year, single environment)

Step-wise build, anchor-and-offset across years:

```
Deployed capacity (MW)                        ← Allocator output (terrestrial) OR ODC module (orbital)
× (1 / PUE)                                   ← PUE = 1.3 base (Uptime Institute), per-environment input
= IT power (MW)
÷ Per-GPU TDP (W) × 1e6                       ← 700 W base (H100-equiv), with Wright's Law improvement curve
= GPU count
× Per-GPU PFLOP rating                        ← H100-equiv = 1 PFLOP (FP8 sparse), with generation-uplift curve
= Installed PFLOP capacity
× Hours/year (8760) × Utilization rate        ← 80% base (CoreWeave contracted-backlog level)
= Annual PFLOP-hr supply
```

**Two environment-specific inputs** (terrestrial vs ODC):

| Input | Terrestrial | ODC |
|---|---|---|
| **PUE** | 1.3 (Uptime hyperscaler avg) | Different — orbital thermal regime; user-input from ODC module if integrated; standalone default 1.1 |
| **Per-GPU TDP** | 700 W (H100-equiv) | Same chip, same TDP — but cooling environment is different (thermal subsystem absorbs in the ODC module, not here) |

### 3.2 Wright's Law on tokens-per-watt

The revenue analysis explicitly flags forward economics: "tokens per watt has improved meaningfully across the H100, H200, and B200 transitions disclosed by NVIDIA, and inference-stack improvements compound that effect. The $41.6B/GW figure plausibly represents a floor for the 2026–2028 buildout window, not a ceiling: even if pricing per token continues to fall, the same gigawatt processes far more tokens."

The model encodes this as **a per-PFLOP-hr efficiency curve**, separate from the $/PFLOP-hr pricing curve:

- `Effective_PFLOP-hr_per_kW(year) = Effective_PFLOP-hr_per_kW(2025) × (1 + tokens_per_watt_CAGR)^year_offset`
- Tokens-per-watt CAGR is an MC input (base 25%/yr per Wright's-Law-fit to H100→H200→B200; range 15%–40%)

This decouples physical-capacity growth from revenue-rate evolution. Pricing per PFLOP-hr can fall, capacity per kW can rise, and the two together resolve into revenue per kW.

### 3.3 PFLOP-hr → revenue conversion (per layer)

Each downstream sub-module reads PFLOP-hr from this tab and applies a layer-specific $/PFLOP-hr rate:

| Layer | $/PFLOP-hr base anchor | Source |
|---|---|---|
| **L3 Compute** | $/PFLOP-hr = $9.2B / (PFLOP-hr per GW per year, base case) | CoreWeave FY25 10-K Q4 run-rate $10,480/GPU/yr, divided through PFLOP/GPU |
| **L4 Application** | $/PFLOP-hr = $20.1B / (PFLOP-hr per GW per year, base case) | Friar anchor × 2.4× calibration, allocated 80/20 with L5 |
| **L5 Orchestration** | $/PFLOP-hr = $5.0B / (PFLOP-hr per GW per year, base case) | Friar anchor × 2.4× calibration, 20% of L4+L5 |

These rates are not constants — they evolve. Architecture §4 covers the demand-side ramps.

### 3.4 Cross-tab handoff

`Compute Supply` exposes (Allocator OUT-style labels):

- Deployed capacity (MW, by terrestrial / ODC split)
- IT power (MW)
- GPU count (H100-equivalents)
- Annual PFLOP-hr supply (by terrestrial / ODC split)
- Effective $/PFLOP-hr at L3 (with Wright's Law evolution)
- Effective $/PFLOP-hr at L4 (with Friar→Anthropic band evolution)
- Effective $/PFLOP-hr at L5 (with orchestration ramp)

Compute, Application, Orchestration tabs all pull from these labels via INDEX/MATCH (Rule 12).

---

## 4. Product ramps (open question #1 closed)

Three independent ramp curves, each on its own row of the Compute Supply tab, each anchor-and-offset (Rule 23):

### 4.1 Deployment ramp — kW per year (supply-side)

- **Source**: Allocator output. For the standalone parallel build, hardcoded by year from Vlad's published SpaceX capacity trajectory (Colossus 1 at 300 MW today, Colossus 2 ramp, ODC if applicable).
- **Inside the SpaceX trunk**: Module CapEx allocator decision (cash queue), translated into deployed kW via Compute Supply tab.
- **Anchor-and-offset**: D-column = 2025 deployed MW; E:AC built off an S-curve OR a hardcoded year-by-year override sourced from Mach33 capacity projections.

### 4.2 Utilization ramp — % of installed capacity actually billable

- **Source**: per-facility utilization curve. New facilities take 6–18 months to ramp through tenant onboarding, GPU installation, and full utilization (per revenue analysis).
- **Method**: weighted blend of installed-this-year MW (low utilization) and prior-vintage MW (high utilization). Vintage-aware utilization curve.
- **Anchor-and-offset**: each vintage has a utilization-by-age table; current-year utilization is `Σ vintage_MW × utilization(age) / total_MW`.

### 4.3 Demand-rate ramp — $/PFLOP-hr evolution by layer

This is the most epistemically loaded ramp. Three sub-curves, all anchor-and-offset:

- **L3 (Compute)**: CoreWeave Q4'25 run-rate $10,480/GPU/yr is the 2025 anchor. Forward evolution governed by (a) Wright's Law deflation on $/PFLOP-hr (negative) and (b) demand growth on PFLOP-hr consumption (positive). Net direction: pricing falls, volume rises, revenue/GW rises slowly.
- **L4 (Application)**: Friar anchor $10.5B/GW (2023–25 OpenAI blended) → $25.1B/GW (Mach33 calibrated 2026) → Anthropic ceiling $20–30B/GW. The 2026–2030 trajectory ramps from Friar to Anthropic-class; post-2030 the rate stabilizes at the Anthropic-class anchor with continued Wright's Law deflation in pricing offset by volume.
- **L5 (Orchestration)**: 20% of L4+L5 (Mach33 assumption, MC range 10–35% to capture the Cursor-class economics range).

**Methodological lock**: this is the where the Mach33 analyses are most opinionated. The 2.4× calibration (Mach33 heuristic) is reproduced in the workbook as a documented multiplier with its own MC range — bear 1.0× (no calibration; Friar floor only), base 2.4× (Mach33 published), bull 2.85× (Anthropic ceiling).

### 4.4 Total revenue per layer per year

Per layer: `Revenue(layer, year) = PFLOP-hr_supply(year) × utilization(year) × $/PFLOP-hr(layer, year) × business_model_capture(layer)`

Where `business_model_capture` is the credence-weighted blend from §7.

---

## 5. Compute sub-module (Sub-module 1) — vending machine

### 5.1 Revenue stack

- **External (wholesale L3 to tenants)**: PFLOP-hr × $/PFLOP-hr × external_share. External share is the % of Compute capacity NOT consumed internally by Application.
- **Internal (to Application)**: PFLOP-hr × $/PFLOP-hr × internal_share. At-cost (or at-NVIDIA-parity if Vlad chooses to model an internal markup — open question §11.4).

### 5.2 COGS

Per vending-machine framing (Lesson 8, Rule 13). Module COGS contains only direct production costs:

- **L1 Energy** internal cost line. Terrestrial: gas BTM weighted blend (60% gas / 25% renewable / 15% nuclear per margins analysis, MC ranges per Cost Assumptions Bear/Bull). ODC: amortised solar PV CapEx (handled via ODC module Allocator OUT, or solar-PV CapEx amortised inline if standalone).
- **L2 Chips** internal cost line. Terafab toggle ON: internal transfer from Terafab at NVIDIA-parity ASP × GPU count, eliminated at Group P&L. Toggle OFF: external NVIDIA at market ASP.
- **L3 operations** — data center variable cost (power, cooling delta, network bandwidth, on-site labour). Anchored on CoreWeave 10-K cost breakdown.

**⚠ GPU / fleet D&A — methodology delta (load-bearing)**: depreciation is excluded in the source margins analysis ("analysis stops at EBITDA"). The trunk methodology has fleet D&A in Module COGS per the 2026-05-20 accounting lock #1 (vehicle / fleet D&A ownership at module level). **Resolution**: AI Stack standalone workbook initially **excludes D&A** to preserve cross-validation with the published source numbers. On trunk port, GPU + data-center-shell D&A is added to Compute Module COGS to match the trunk convention. This delta means standalone-workbook EBITDA per GW ≠ trunk-port EBITDA per GW. The Methodology Delta document (§16 Stage 2) tracks the gap line by line, and the Calibration tab back-tests both views in parallel.

### 5.3 Gross Profit / Module EBITDA

Per layer, base anchor: 50% (CoreWeave Adj EBITDA $3.09B / $5.13B = 60% FY25, discounted toward AWS 35% / Nebius +12% → 50% base). Bear 30%, Bull 65% — MC range.

### 5.4 CapEx

Per-MW CapEx for data center build. Two flavors:

- **Compute_Terrestrial CapEx** ($/MW): real estate, power infra, cooling, networking, build labour. Anchored on hyperscaler reported $/MW. Does NOT include GPUs (those flow through Chips internal transfer or external NVIDIA purchase, recorded separately).
- **Compute_ODC CapEx**: comes from ODC module (per existing rebuild v2 ODC architecture). AI Stack module reads ODC's PFLOP-hr supply as an Allocator IN; ODC's CapEx is NOT duplicated here.

### 5.5 Allocator OUT (Compute)

11 canonical labels. IRR engine: per-MW marginal IRR — `[−CapEx_per_MW, +FCF_per_MW_yr1, ..., +FCF_per_MW_yr5]`. CoreWeave's 10-year IT-equipment useful-life convention bounds the period; 5-year IRR window is conservative for L3 economics.

---

## 6. Application sub-module (Sub-module 2) — vending machine

### 6.1 Revenue stack

- **First-party applications (Grok consumer + xAI enterprise)**: L4 revenue per PFLOP-hr × consumed_PFLOP-hr × business_model_capture.
- **External API access (Grok API to third parties)**: L4 revenue per PFLOP-hr × external_share.

### 6.2 COGS

- **Internal transfer from Compute**: PFLOP-hr × $/PFLOP-hr internal price. Eliminated at Group AI Stack P&L.
- **Training compute** (separate from inference): bear in mind ~35% of compute is training in 2026 (1 − 0.65 inference share from the revenue analysis). Training compute is COGS, not R&D, when accounting is GAAP (per the AI Stack margins analysis L4 cost basis note: "L4 cost = inference + training blended, Anthropic GAAP convention"). Inference-share split is an Assumptions input.
- **Customer-service / billing**: NOT in COGS per vending machine. Sits in Group AI Stack OpEx (or Group SpaceX OpEx when ported to trunk).

### 6.3 R&D — pre-revenue capitalization lock

This is where the **2026-05-20 accounting methodology lock** bites: pre-revenue R&D is capitalized; post-revenue R&D is expensed. For Application:

- Grok / xAI R&D **pre-2025** (model development sunk cost): capitalized as opening intangible, amortized over the modelled horizon. Anchored on disclosed Musk-era xAI R&D spend.
- Grok / xAI R&D **2025 onwards** (model maintenance + frontier upgrades): expensed. Sits in OpEx, not COGS.

Per the AI Stack margins analysis Stage 2 cost cascade: "L4 training, research, and SG&A is $17.1 billion [per GW base case]." That $17.1B is the full L4 cost line (=85% × $20.1B at 15% EBITDA). In the trunk vending-machine convention, that splits roughly as:

| L4 cost component (margins analysis $17.1B/GW) | AI Stack module placement |
|---|---|
| Training compute (inference + training blend cost) | Compute internal transfer COGS |
| Model R&D maintenance | OpEx (not COGS) |
| Customer service / billing | OpEx (not COGS) |
| Sales & marketing | OpEx (not COGS) |

A reconciliation row on the Calibration tab back-tests this split against the analysis's published $17.1B figure. Per-line allocation is an MC input.

### 6.4 CapEx

Application CapEx is small in absolute dollars (it's a software business). Two line items:

- **Capitalized R&D (pre-2025 only)** as an opening intangible balance — see §6.3.
- **Application-layer hardware / infrastructure beyond what Compute provides** — likely zero in the modelled horizon; placeholder row for completeness.

### 6.5 Allocator OUT (Application)

11 canonical labels. **IRR engine: open question §11**. Most likely treatment: Application sits OUTSIDE the cash queue IRR allocator (it has minimal CapEx); economics roll up to Module FCF directly. Application IRR row is computed as a per-PFLOP-hr return ratio for diagnostic visibility but does not drive cash allocation.

---

## 7. Orchestration sub-module (Sub-module 3) — vending machine

### 7.1 Revenue stack

L5 revenue — Cursor-class orchestration revenue per PFLOP-hr (the demand-side denominator is upstream Compute supply, even though Orchestration adds value above the model layer). Pricing anchored on Cursor 2025–26 reported revenue scaled to inference consumption.

### 7.2 COGS

- **API spend** to Application (or external model providers in Model B configurations): inference token cost × tokens consumed. Internal transfer at L4 internal price, eliminated at Group AI Stack P&L.
- **Direct delivery cost**: engineering / customer-facing infra. Sits in Module COGS.

ICONIQ 2026P aggregate GM for AI-native operators is 52%; Bessemer Supernova reports 25% GM (Cursor named explicitly). Mach33 base GM: 52% (MC range 25%–60%).

### 7.3 Gross Profit / Module EBITDA

Base anchor: 5% EBITDA (ICONIQ scaling-stage cost stack sums to ~99% of revenue per the analysis). Bear: −30% (Cursor pre-Composer reality through 2027). Bull: 30% (mature SaaS orchestration economics).

### 7.4 R&D

Same pre-revenue / post-revenue methodology lock as Application (§6.3). Cursor pre-acquisition R&D = opening intangible if acquired; ongoing R&D = OpEx.

### 7.5 CapEx

Essentially zero. Software business. Placeholder row.

### 7.6 Allocator OUT (Orchestration)

11 canonical labels. **IRR engine: same architecture as Application** — outside cash queue, IRR row diagnostic only.

---

## 8. Energy and Chips — upstream COGS handling

### 8.1 Energy (L1) — terrestrial vs ODC switch

| Environment | Method | Margin captured |
|---|---|---|
| **Terrestrial BTM** (Model A + Model C) | Gas-weighted blend (60% gas / 25% renewable / 15% nuclear per margins analysis). Energy IPP-margin captured by SpaceX. | 40% EBITDA on $0.7B/GW (= $279M/GW Energy capture per the margins cascade) |
| **Terrestrial delivered PPA** (Model B) | SpaceX buys delivered power at PPA price. No L1 margin capture. | 0 |
| **ODC orbital** | Solar PV amortised CapEx. Energy is "free" (solar) but CapEx is heavy. Sits in ODC module, not AI Stack. | N/A — handled by ODC module |

The Energy row on Compute COGS is an **environment switch** driven by:

- For terrestrial: a per-MW BTM-vs-PPA mix (Assumptions input, MC range 0–100%).
- For ODC: $0 in Compute COGS (energy is captured upstream in ODC module CapEx).

### 8.2 Chips (L2) — Terafab toggle

Single workbook-level toggle (Assumptions input). Three states for MC purposes:

- **Toggle = 1 (Terafab ON, NVIDIA-parity)**: SpaceX captures L2 EBITDA margin of 67% × $6.6B/GW = $4.4B/GW. Internal transfer from notional Terafab to Compute at NVIDIA-parity ASP. Eliminated at Group AI Stack P&L.
- **Toggle = 0 (Terafab OFF, buy from NVIDIA)**: SpaceX pays NVIDIA gross. Zero L2 capture.
- **Toggle = 0.5 (Terafab sub-parity, MC range)**: blended capture at sub-parity margin (e.g. 50% L2 EBITDA per the margins analysis bear case sensitivity). Used in Monte Carlo to capture the execution-quality range.

**Per the margins analysis disclaimer**: "Assuming Terafab achieves NVIDIA's 67% EBITDA margin ignores three decades of incumbent supply-chain and software moats. This is a theoretical upper bound, not a baseline forecast." The MC range on the toggle reflects this disclaimer.

**Terafab CapEx**: explicitly out of scope for this module per the margins analysis ("addressed in a separate Mach33 piece on AI infrastructure capex"). When ported to the SpaceX trunk, Terafab CapEx is a separate corporate-CapEx line claimed at the allocator queue gate. AI Stack module sees only Terafab's run-rate economics, not its build cost.

---

## 9. Business Model Switch tab — credence-weighted blend

Three SpaceX business-model configurations are run in parallel in the real world (per the revenue analysis Investor Takeaways). The workbook handles this with **per-layer capture rates** driven by a credence weight on each model.

### 9.1 Capture matrix (per the source models)

| Layer | Model A (Full-stack) | Model B (Wholesale) | Model C (Hybrid) |
|---|---|---|---|
| L1 Energy | 1.0 (BTM) | **0.0** (PPA delivered — tenant pays external generator; no L1 margin to SpaceX) | 1.0 (BTM) |
| L2 Chips | 1.0 (Terafab if ON) | 1.0 (Terafab if ON) | 1.0 (Terafab if ON) |
| L3 Infrastructure | 1.0 (internal) | 1.0 (wholesale to tenant) | 1.0 (internal) |
| L4 Model+App | 1.0 (Grok+xAI internal) | 0.0 (tenant owns) | 1.0 (Grok+xAI internal) |
| L5 Orchestration | 1.0 (own e.g. Cursor) | 0.0 (tenant owns) | 0.0 (partner owns) |

**Source-model inconsistency resolved**: the revenue-side 1 GW model has Model B with L1 capture = 1.0 (Mach33 published convention error — Anthropic at Colossus 1 pays PPA externally, so SpaceX should not book L1 margin). The margins-side model has Model B with L1 = 0.0 ("Pays PPA externally"). **The matrix above adopts the margins-model convention** (L1 = 0.0 for Model B). When the workbook ports, the Calibration tab must use the corrected matrix and explicitly flag the delta from the revenue analysis's published number.

### 9.2 Blended capture

```
Capture(layer, year) = Pr(A) × matrix[A, layer] + Pr(B) × matrix[B, layer] + Pr(C) × matrix[C, layer]
```

Where `Pr(A) + Pr(B) + Pr(C) = 1`. The credences are **MC inputs** with year-varying base anchors that reflect Mach33's "progressive internalization" thesis from the revenue analysis:

| Year | Pr(A) Full-stack | Pr(B) Wholesale | Pr(C) Hybrid |
|---|---|---|---|
| 2026 (today) | 0.05 | 0.50 | 0.45 |
| 2030 | 0.35 | 0.30 | 0.35 |
| 2035 | 0.55 | 0.20 | 0.25 |
| 2050 | 0.70 | 0.10 | 0.20 |

These anchor weights are MC inputs (triangle distributions, ranges per Vlad's calibration). The progression reflects the revenue analysis's central thesis: SpaceX runs all three in parallel during the 2026–2030 buildout window, then progressively internalises through the 2030s as Grok matures and Terafab comes online. Cursor acquisition would accelerate Pr(A); Cursor partnership-only keeps weight on Pr(C).

### 9.3 Mapping the matrix to the three sub-modules

Critically, Pr(B) does NOT zero out Application + Orchestration revenue. Pr(B) means **SpaceX as wholesale operator captures only L2 + L3**; the L4 + L5 revenue still EXISTS in the value chain, it just accrues to the tenant. The blended workbook revenue for Application and Orchestration is therefore weighted by (Pr(A) + Pr(C)) for L4 and Pr(A) only for L5.

The Business Model Switch tab is the mechanism that gates which sub-module revenue lines fire in each year, based on the credence weights.

---

## 10. Calibration anchors (Rule 23, ±5% tolerance)

The Calibration tab back-tests the workbook against the two source models' published per-GW figures. Lock pre-build:

| Anchor | Source | Target value (per GW, 2025/26 base case) | Tolerance |
|---|---|---|---|
| Total stack revenue | 1 GW Revenue Stack | $41.6 B | ±5% |
| End-user TAM (L4+L5) | Both models | $25.1 B | ±5% |
| L1 Energy revenue | 1 GW Revenue Stack | $0.7 B | ±5% |
| L2 Chips revenue | 1 GW Revenue Stack | $6.6 B | ±5% |
| L3 Infrastructure revenue | 1 GW Revenue Stack | $9.2 B | ±5% |
| L4 Model+App revenue | 1 GW Revenue Stack | $20.1 B | ±5% |
| L5 Orchestration revenue | 1 GW Revenue Stack | $5.0 B | ±5% |
| Model A EBITDA (base) | AI Stack Cost Margins Stage 2 | $12.6 B / GW | ±5% |
| Model B EBITDA (base) | AI Stack Cost Margins Stage 2 | $9.0 B / GW | ±5% |
| Model C EBITDA (base) | AI Stack Cost Margins Stage 2 | $12.3 B / GW | ±5% |
| Colossus 1 cross-check (300 MW Anthropic deal) | 1 GW model + xAI press release | $5 B / yr model-implied (analyst band $3.5–5.5B) | Within band |
| Anthropic ARR back-test | Anthropic Apr 2026 disclosure | $30 B ARR on 1.0–1.5 GW deployed | Within band |

These anchors lock at 2025/26 base case at 1 GW reference. The yearly module's 2025 column at 1 GW deployed must reproduce these within tolerance. If it doesn't, the methodology breaks and Sprint 6 halts (Rule 15).

---

## 11. IRR engine choice (open question #3 — partially resolved)

This is the deepest architectural question. The four open questions deferred Sprint 6; this one is the hardest.

### 11.1 The problem

The Compute sub-module is CapEx-heavy and IRR-natural. Per-MW marginal IRR drops in cleanly:
`IRR_per_MW = IRR([−CapEx_per_MW, +FCF_per_MW_yr1, ..., +FCF_per_MW_yr5])`.

But Application + Orchestration are R&D-heavy and CapEx-light. The IRR engine that works for satellites does not work for software businesses. Three candidate architectures:

### 11.2 Candidate architectures

**Candidate 1: Application + Orchestration OUTSIDE the cash queue IRR allocator.** Their economics roll up to Module FCF directly; their cash claims (R&D OpEx, customer-acquisition spend) are non-module-claim line items handled at the queue gate (per Lesson 4 / Architecture §4.4). IRR rows on Allocator OUT are diagnostic only — computed as a per-PFLOP-hr capture ratio for visibility, but they don't drive allocation. **Recommendation**: this is the default for the parallel build.

**Candidate 2: Per-product marginal IRR on R&D investment.** Treat each Grok model generation as a "product" with R&D investment and a forward FCF stream. IRR is computed on the R&D investment, not on physical CapEx. This is intellectually appealing but methodologically thorny — model generations are not discrete enough to be cleanly per-product, and the FCF attribution to a generation is fuzzy.

**Candidate 3: Strategic carve-out (Moon/Mars analogue).** Application + Orchestration as strategic R&D investments that consume non-module-claim cash, sized as `MAX(floor, prior_FCF × pct)`, with the per-year capture flowing through to Group AI Stack EBITDA via the credence-weighted revenue blend. **No IRR engine.** This mirrors how Moon/Mars is handled in Sprint 7.

### 11.3 Recommendation

**Compute** uses Candidate 1 (full per-MW marginal IRR, participates in cash queue).
**Application + Orchestration** use Candidate 1 (outside cash queue; diagnostic IRR only; R&D claims at queue gate as non-module claim).
**Terafab** (when modelled standalone in Option B): per-GPU marginal IRR on Terafab CapEx, participates in cash queue alongside Compute.

This keeps the IRR allocator coherent: only CapEx-intensive modules participate in IRR-priority allocation; R&D-intensive modules are non-module claims competing with corporate OpEx, taxes, and Spectrum CapEx at the queue gate.

### 11.4 Open sub-question: internal-transfer markup on Compute → Application

When Compute sells PFLOP-hr internally to Application, should it sell at-cost or at-market? **This is a substantive conflict between the source-model methodology and the trunk's 2026-05-20 accounting-lock #3 — flagged as the highest-priority Vlad sign-off in §15.**

- **At-cost (trunk lock default)**: Compute's internal margin = 0%; Application captures the full L4 economics. Total stack revenue counts once at end-user, internal flow eliminated cleanly. **Matches accounting-lock #3** which requires fully-allocated at-cost transfer pricing symmetrically across launch / bandwidth / compute flows. Extending the same convention to Compute→Application makes it a fourth symmetric at-cost flow.
- **At-market / Stage 2 Option C (source-model convention)**: Compute captures its L3 margin internally, and Application's L4 margin is computed on top of the cost basis (L1 + L2 + L3 internal price). Used in the AI Stack Cost Margins model ("each owned layer pays its internal cost basis for inputs from below"). Produces "gross flows" with $41.6B/GW of internal economic activity, matching the published source-analysis numbers.

**The conflict**: the source-model convention is at-market; the trunk lock is at-cost. They produce different per-module IRRs. The right answer depends on whether IRR is computed on stand-alone economics (at-market) or post-elimination economics (at-cost).

**Provisional recommendation for the standalone parallel build**: build with the at-market Stage 2 Option C convention so the workbook cross-validates against published source-analysis figures. When porting to the trunk, convert to at-cost per accounting-lock #3. The Methodology Delta document (§16 Stage 2) captures this delta explicitly.

Internal transfers eliminate cleanly at Group AI Stack P&L in both conventions. Group AI Stack revenue counts each $ once (at end-user); module-level revenue includes internal flows for IRR computation.

---

## 12. CapEx vs R&D treatment (open question #4 closed)

Tied to §6.3 and §7.4 and the 2026-05-20 accounting methodology lock:

| Sub-module | CapEx (in module) | R&D pre-revenue (capitalized) | R&D post-revenue (OpEx) | Customer service / S&M |
|---|---|---|---|---|
| Compute | Data center build $/MW + GPUs (Module CapEx) | N/A (already a revenue business) | N/A | Tenant relationships → Group SG&A |
| Application | Capitalized R&D pre-2025 (opening intangible) | Grok / xAI R&D pre-2025 sunk → opening intangible balance, amortized | Grok / xAI R&D 2025+ → Group OpEx | Group OpEx |
| Orchestration | Capitalized R&D pre-acquisition (if Cursor acquired) | Cursor R&D pre-acquisition (if acquired) → opening intangible | Ongoing engineering → Group OpEx | Group OpEx |
| Terafab (if Option B) | Fab CapEx (out of scope per source analysis disclaimer) | N/A | Process R&D → Group OpEx | Tenant → Compute, no S&M |

This matches the AI Stack Cost Margins analysis's GAAP convention (Anthropic-style: training compute in COGS, not in capitalized R&D) AND the trunk's 2026-05-20 lock (pre-revenue R&D capitalized, post-revenue R&D expensed).

---

## 13. Terrestrial vs ODC split (user requirement closed)

### 13.1 Where the split lives

The terrestrial-vs-ODC distinction only matters at **Compute Supply** and **Compute COGS**. Application and Orchestration are location-agnostic — they consume PFLOP-hr regardless of where the PFLOP-hr originated.

### 13.2 Compute Supply split

Compute Supply tab has parallel rows for terrestrial and ODC kW deployed. PFLOP-hr supply rolls up to a Total PFLOP-hr row that downstream tabs reference. Two switches:

- **Terrestrial PUE = 1.3** vs **ODC PUE = different (orbital thermal regime)**. Both are Assumptions inputs.
- **Per-GPU effective output (PFLOP)** is identical in both environments (same chip).

### 13.3 Compute COGS split

- **L1 Energy COGS**: terrestrial = gas-weighted BTM cost; ODC = $0 here (energy cost absorbed in ODC module CapEx amortisation, which appears in the trunk via ODC module's at-cost transfer to AI Stack).
- **L2 Chips COGS**: identical in both environments (Terafab serves both, same toggle).
- **L3 Infrastructure CapEx**: terrestrial = data center build $/MW; ODC = $0 here (handled by ODC module).

### 13.4 Critical integration point with ODC module

When ported to the SpaceX trunk, the AI Stack module **must not double-count ODC CapEx**. The ODC module owns the orbital data center build (per Sprint 5 architecture); the AI Stack module CONSUMES ODC's PFLOP-hr supply via internal transfer at-cost (or at-market, per §11.4).

The parallel-build standalone workbook should include placeholder rows for ODC PFLOP-hr supply (with toggleable ODC fraction of total PFLOP-hr) so the integration is clean when ported.

### 13.5 Cross-reference to T-001 thesis

This separation directly supports the T-001 ODC growth-multiple thesis: ODC PFLOP-hr supply feeds AI Stack revenue, but ODC capacity in the 2026–2030 window is small (terrestrial Colossus dominates). ODCs preserve the growth multiple post-2030 by providing the next chunk of supply growth when terrestrial buildout maxes out — they're not a 2030 revenue line, they're the option value that justifies the multiple.

### 13.6 LOCKED: AI Stack consumes ZERO kg-to-LEO Starship capacity

Per memory `project_ai_stack_no_launch_demand`: **AI Stack is terrestrial-only at the kg-to-LEO claim layer. Capacity Demand (kg-to-LEO) = 0 permanently across all years** in the Allocator OUT contract — not just dormant, structurally zero.

ODC's compute supply flows to AI Stack via internal transfer of PFLOP-hr, not via Starship launch demand. ODC consumes Starship capacity to deploy its own constellation; AI Stack consumes ODC's PFLOP-hr output. The kg-to-LEO chain stops at ODC.

This lock means AI Stack does **not** compete in the Starship priority queue (T-002) for launch slots. T-002's "Compute" position in the priority queue refers to ODC's launch demand, not AI Stack's. Sprint 6 spec must enforce this with a permanent `=0` on the AI Stack Capacity Demand row.

---

## 14. MC discipline — the input register

Per Rule 18 (MC ranges captured at input creation), every Assumptions input has its MC range populated when the row is created. Categorized inputs:

### 14.1 Physical / structural inputs

| Input | Base | MC range | Distribution | Notes |
|---|---|---|---|---|
| PUE (terrestrial) | 1.3 | 1.25–1.45 | Triangle | Uptime hyperscaler avg + worse new-build |
| PUE (ODC) | 1.1 | 1.05–1.3 | Triangle | Orbital thermal regime estimate |
| Per-GPU TDP (W) | 700 | 600–800 | Triangle | H100-equiv normalization |
| Per-GPU PFLOP rating | 1.0 | 0.8–1.5 | Triangle | H100-equiv = 1; generation uplift compound |
| Hours/yr | 8760 | Structural | None | Structural — no MC |
| GPU utilization rate | 80% | 65%–90% | Triangle | CoreWeave contracted-backlog level |
| GPU depreciation period (years) | 5 | 3–6 | Triangle | Amazon FY24 10-K basis |

### 14.2 Demand-side inputs

| Input | Base | MC range | Distribution | Notes |
|---|---|---|---|---|
| Electricity $/kWh (terrestrial blend) | $0.08 | $0.05–$0.12 | Triangle | EIA national industrial avg ±range |
| L3 $/GPU/yr (Compute revenue rate, 2025) | $10,480 | $8,552–$17,000 | Triangle | CoreWeave 10-K FY25 to high-end steady-state |
| Friar anchor (OpenAI $B/GW) | $10.5B | Structural | None | Locked at disclosed value |
| Anthropic ceiling ($B/GW) | $25B | $20B–$30B | Uniform | Implied range from disclosed ARR / est. GW |
| Inference share (Q1'26) | 65% | 56%–75% | Triangle | Mach33 estimate, with Epoch/Sacra anchors |
| Revenue intensity multiplier | 1.45× | 1.0×–1.65× | Triangle | Mach33 calibration |
| L4/L5 split (L5 share) | 20% | 10%–35% | Triangle | Mach33 assumption |
| Tokens-per-watt CAGR | 25%/yr | 15%–40% | Triangle | Wright's Law fit |

### 14.3 Margin inputs (per layer, per scenario from the margins analysis)

| Input | Base | MC range | Distribution | Notes |
|---|---|---|---|---|
| L1 EBITDA margin (gas-weighted) | 40% | 30%–55% | Triangle | Talen + Clearway + Constellation blend |
| L2 EBITDA margin (Terafab parity) | 67% | 50%–75% | Triangle | NVIDIA C&N segment OP margin |
| L3 EBITDA margin | 50% | 30%–65% | Triangle | CoreWeave 60% discounted to AWS 35% range |
| L4 EBITDA margin | 15% | −30% to 40% | Triangle | OpenAI burn to Anthropic 2028 guide |
| L5 EBITDA margin | 5% | −30% to 30% | Triangle | ICONIQ / Cursor pre-Composer |
| Energy mix: gas BTM weight | 60% | 40%–80% | Triangle | Per margins analysis |
| Energy mix: renewable PPA weight | 25% | 15%–30% | Triangle | Per margins analysis |
| Energy mix: nuclear PPA weight | 15% | 5%–30% | Triangle | Per margins analysis |

### 14.4 Business-model credence inputs (year-varying)

Pr(A), Pr(B), Pr(C) for 2026 / 2030 / 2035 / 2050 — anchor points with MC triangle distributions per year. Inter-year values interpolated linearly.

### 14.5 Toggles

| Toggle | States | Default | MC treatment |
|---|---|---|---|
| Terafab | 0 / 0.5 / 1 | 1 (ON, NVIDIA-parity) | Discrete distribution (0=0.2, 0.5=0.3, 1=0.5) reflecting uncertainty on Terafab execution |
| Compute Internal Transfer Pricing | at-cost / at-market | at-market (Stage 2 Option C) | Discrete (at-market 0.7, at-cost 0.3) |
| Terrestrial vs ODC kW split | % ODC of total | Year-varying ramp | Per-year triangle |

---

## 15. Open questions for Vlad before workbook construction

These are the architectural decisions Vlad needs to sign off on before the standalone parallel-build workbook is constructed. Some have a recommended default in this scoping; some are genuinely open:

| # | Question | Recommended default | Status |
|---|---|---|---|
| Q1 | Terafab as toggle inside L2 COGS (Option A) or 4th sub-module (Option B)? | **A** for parallel build; revisit when L2 mechanics validated | Vlad sign-off needed |
| Q2 | Application + Orchestration outside cash queue IRR allocator (Candidate 1)? | **Yes** | Vlad sign-off needed |
| **Q3** | **Internal transfer pricing: at-cost (trunk lock #3) or at-market (source-model Stage 2 Option C)?** | **HIGHEST-PRIORITY ESCALATION** — see §11.4. Substantive conflict between source-model convention and 2026-05-20 accounting-lock #3. Provisional: at-market for parallel build, convert to at-cost on trunk port. | Vlad sign-off needed |
| Q4 | Capitalize pre-2025 Grok/xAI R&D as opening intangible? Anchor on what disclosed figure? | Yes, anchor on best-available xAI R&D disclosure | Vlad to source anchor figure |
| Q5 | Pr(A)/Pr(B)/Pr(C) credence anchors — accept the §9.2 schedule or revise? | §9.2 schedule as starting anchors | Vlad calibration call |
| Q6 | Should the standalone workbook integrate with the ODC PFLOP-hr supply right away, or use a stub ODC input until trunk port? | Stub ODC input until trunk port (clean separation) | Vlad sign-off needed |
| Q7 | Tokens-per-watt CAGR base anchor — 25%/yr feels aggressive; should we anchor lower? | 25%/yr base, MC range 15–40% | Vlad / Aaron call |
| Q8 | Should the source-model "Stage 2 Option C cost cascade" exactly reproduce in the workbook (i.e. per-layer Owned/External flags), or is a credence-weighted blend sufficient? | Credence-weighted blend (§9) is cleaner; cross-validation via Calibration tab back-tests against source-model published outputs | Vlad sign-off needed |

**Resolved by memory / constitutional framework — NOT open**:

- ~~AI Stack rolls into ODC vs standalone module~~ → resolved 2026-05-19 per locked rebuild architecture: AI Stack is a standalone module. T-006 framing is narrative-only at Group P&L layering.
- ~~Standalone workbook Monte Carlo sprint vs inherit trunk MC sprint~~ → resolved per rebuild-v2 architecture: build with point-estimate fixed assumptions; MC ranges populated at input creation but MC sampling layered at the end via dedicated MC sprint. Parallel build follows the same convention.

---

## 16. Path from this scoping to Sprint 6 trunk integration

Three-stage path:

### Stage 1 — Standalone parallel-build workbook (next deliverable)

Once Vlad signs off on §15 open questions, this scoping converts into a **Sprint Spec for the standalone AI Stack workbook** following the Rebuild v2 spec template:

- Rule Compliance Preamble at the top
- Sections: Assumptions tab population, Compute Supply, Compute, Application, Orchestration, Business Model Switch, Group AI Stack P&L, Calibration
- Verification: ±5% calibration against the §10 anchors at 1 GW reference (2025); MC ranges populated at input creation; conservation rows on internal flows.

This produces a working AI Stack workbook independent of the trunk. Vlad can validate the structure, pressure-test the unit economics, and use it for client / X-post / weekly-analysis deliverables in parallel to the trunk sprints.

### Stage 2 — Methodology delta documentation

A short delta doc captures every methodological difference between the standalone workbook and the trunk convention. Known deltas as of this scoping:

1. **GPU depreciation**: standalone excludes (per source-model methodology); trunk includes in Module COGS per 2026-05-20 accounting lock. Trunk port adds D&A row.
2. **Customer service / S&M**: standalone has it as Group AI Stack OpEx; trunk has it as Group SpaceX OpEx (rolls up to one level higher).
3. **Energy COGS for ODC**: standalone uses stub ODC supply with hardcoded energy cost share; trunk reads from ODC module Allocator OUT at-cost transfer.
4. **R&D capitalization**: standalone uses simple opening intangible; trunk may have a more sophisticated R&D schedule per Sprint 4.5 D&A target work.
5. **Pre-revenue R&D treatment**: standalone follows the 2026-05-20 lock by design; trunk lock confirmed before port.

### Stage 3 — Sprint 6 port

When trunk is ready (i.e. when Sprint 6 fires), the standalone workbook's module tabs are imported into the trunk workbook with the methodology deltas applied. The trunk Allocator picks up Compute as a participant in the cash queue; Application + Orchestration register their non-module-claim cash needs at the queue gate.

Sprint 6 spec at that point is mostly mechanical: port the validated structure, apply the deltas, run the universal verification protocol, hit calibration.

---

## 17. What this scoping closes

For the record — Sprint 6 was deferred per memory note `project_sprint_6_deferred` on 2026-05-20 pending:

- Product ramp curves — **closed §4**
- PFLOP-hr derivation — **closed §3**
- IRR engine choice — **closed §11 (with Vlad sign-off on Candidate 1 default)**
- (User added) Capital intensity / CapEx vs R&D model — **closed §12**
- (User added) Terrestrial vs ODC split — **closed §13**

The remaining blockers are the 10 open questions in §15 (mostly sign-off / anchor-sourcing items, not structural unknowns).

Once §15 is resolved, the standalone parallel-build workbook can begin. Sprint 6 in the trunk waits for the standalone build to validate the structure.

---

## 18. Sources

- **1 GW AI Value Chain Model** (Mach33, May 2026). 5 tabs: Assumptions, 1 GW Revenue Stack, Business Models, Sensitivity, Source Index.
- **AI Stack Cost Margins Model** (Mach33, May 2026). 10 tabs: Assumptions, Cost Assumptions, 1 GW Revenue Stack, Stage 1 - Layer Margins, Stage 2 - SpaceX Capture, Business Models, Sensitivity, Sensitivity - Margin, Source Index, Source Index - Cost.
- **Breaking Down the AI Revenue Stack** (Mach33 analysis, May 13, 2026). NVIDIA five-layer framework, three SpaceX business models, $41.6B/GW stack.
- **Breaking Down AI EBITDA Margins** (Mach33 analysis, May 20, 2026). Stage 1 + Stage 2 cost cascade, $12.6B/$9.0B/$12.3B per-GW EBITDA for Models A/B/C, bear-case inversion.
- **Mach33 Thesis Library** T-001, T-002, T-006.
- **Rebuild v2 constitutional docs**: `01_Lessons_Learned`, `02_Architecture_and_Methodology`, `03_Sprint_Roadmap_and_Verification`, `Model Execution Rules`.
- **Memory notes**: `project_sprint_6_deferred`, `project_accounting_methodology_locks_2026_05_20`, `feedback_anchor_and_offset`, `feedback_allocator_contract_by_label`, `feedback_queue_gate_for_non_module_claims`, `project_ai_stack_no_launch_demand`.

---

## 19. Document control

- **Version**: 0.1 (architecture-only, pre-workbook scoping)
- **Date**: 2026-05-22
- **Next milestone**: §15 sign-off → standalone parallel-build Sprint Spec
- **Trunk impact**: Sprint 6 spec downstream; no trunk workbook changes from this document alone
