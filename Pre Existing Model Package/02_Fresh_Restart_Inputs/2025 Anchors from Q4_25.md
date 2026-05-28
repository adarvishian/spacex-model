# 2025 Anchors from Q4'25 CLEANUP — Replacements + Stub Kills

**Date**: 2026-05-19
**Source workbook**: `SpaceX Valuation Model Q4'25 CLEANUP.xlsx` (Vlad-confident 2025 figures)
**Target**: V30.5 Assumptions — replace arbitrary stubs with anchored Q4'25 values; drop inputs that have no historical anchor

Year column convention in Q4'25: column **J = 2025** on Earth tab, column **F = 2025** on Mars & Moon tab.

---

## 1. ⚠ HIGH-PRIORITY CORRECTIONS (V30.5 has wrong values)

These three are wrong and should be fixed before any rebuild.

| V30.5 cell | Current | Q4'25 anchor | Source | Notes |
|---|---|---|---|---|
| **R466 — Starting cash EoY 2024** | $20,000mm | **$4,700mm** | Earth R225 "Start Of Year Cash Reserve" J col | Q4'25 has $4.70B at start of 2025. Your $20B is way off. Either the $20B is a deliberate post-Apollo-raise position you have private info on, or a stale drift. |
| **R53 — Starshield Reserved % decay rate** | 1.0 | **0.25** | Valuation Inputs R30 median + Earth R102 trajectory (3% → 2.25% → 1.69%) | V30.5 = 1.0 reads as 100%/yr decay, zeros out Starshield instantly. Q4'25 uses 25%/yr. |
| **R54 — Starshield Rev per Gbps (base)** | $167,421 | **$164,699** | Earth R120 J col | Small correction, but anchored. |

---

## 2. 2025 ACTUAL HISTORICALS (lock as anchors; drop any V30.5 stub that diverges)

These are 2025 actuals from Q4'25 — Vlad-confident. Use as anchor; not subject to MC.

### Starlink fleet & launches

| 2025 metric | Q4'25 value | V30.5 location | Action |
|---|---|---|---|
| F9 launches 2025 (total) | 171 | (no direct cell — derived from F9 fleet × cadence) | Calibration check — V30.5 should produce ~171 |
| F9 customer launches 2025 | 38.58 | (derived in module) | Same — Starlink takes 132, customer takes 38.58 |
| Starship launches 2025 | 0 | R196 starts Starship customer rev at 2027 | OK — keep |
| F9 boosters manufactured 2025 | 17.01 | R179 = 8 (V30.5 base build rate) | V30.5 base rate is low — Q4'25 actual was 17. Update R179 to ~17 or set as actual override. |
| F9 fleet end-2024 (SoY 2025) | 28 boosters | R185 = 24 | **Update R185 from 24 → 28.** |
| Satellites launched 2025 (annual) | 3,840 | R96 V2 BB = 2,987 + R97 V2 DTC = 182 = 3,169 | Q4'25 includes ~670 V1/V1.5/Starshield replenishment + Starshield-tagged. V30.5 tracks V2 categories specifically — both are right at different granularity. Keep V30.5. |
| Cumulative sats launched end-2024 (= base year) | 7,486 | R41 = 7,486 | **Confirmed match.** |
| Cumulative sats launched end-2025 | 11,326 | derived | Should fall out of build. |
| Active sats end-2025 | 9,832 | R91 V2 BB 5,246 + R92 V2 DTC 650 = 5,896 active V2 | Q4'25 includes legacy V1/V1.5 (~750) + Starshield reservation pool. Different counting. Keep V30.5. |
| Active sat mass end-2025 | 5.49M kg | derived | Should fall out of build. |

### Starlink revenue

| 2025 metric | Q4'25 value | V30.5 location | Action |
|---|---|---|---|
| Starlink + DTC revenue 2025 | $7,852mm | (derived from R454 BB ARPU × subs + R455 DTC ARPU × subs) | Calibration target — V30.5 should produce ~$7.85B in 2025. |
| of which DTC | $156.91mm (2% of total) | R455 DTC ARPU $16/mo | V30.5 DTC component should be ~$157M in 2025. |
| Starshield revenue 2025 | $2,520mm | (derived from R51 × R54 × bandwidth) | Calibration target. |
| Consolidated revenue 2025 (Starlink + Starshield + Launch + Compute) | $14,650mm | Group P&L roll-up | Calibration anchor for whole model. |

### Customer Launch revenue

| 2025 metric | Q4'25 value | V30.5 location | Action |
|---|---|---|---|
| F9 customer revenue 2025 | $4,290mm | (derived from R191 × R193 × R195) | Calibration target. |
| F9 launch price 2025 | $111.11mm | R195 = $67/launch | **V30.5 R195 is wrong — Q4'25 actuals at $111M/launch. Update.** Public NSSL contracts run $80-150M; commercial cheaper. $67M is pre-2024 list pricing. |
| F9 Total Cost per launch | $50mm | R170 $30 + R171 $10 + R172 $1.25 + R173 $5 = $46.25mm | V30.5 within 8% of Q4'25 — close enough. Keep. |
| F9 Fixed Asset (CapEx) per launch | $37.5mm | (derived) | Per-launch booster capex amortization. |
| F9 Variable Cost (COGS) per launch | $12.5mm | (R171 + R172 + R173 = $16.25mm) | Q4'25 = $12.5M, V30.5 = $16.25M. Modest difference in cost allocation. |

### Cost & depreciation

| 2025 metric | Q4'25 value | V30.5 location | Action |
|---|---|---|---|
| Cost to Manufacture Satellite ($/kg) 2025 | $643.50 | R38 = $650 base year | **Confirmed match.** |
| Annual Constellation Depreciation 2025 | $706.93mm | (= R70 × active mass = $128.8 × 5.49M kg = $707M) | **Confirmed match.** |
| Total Depreciation 2025 | $1,060mm | (derived) | Calibration target. |
| Total OpEx 2025 | $3,820mm | (= R411-R438 sum) | Calibration target. |
| EBITDA 2025 | $8,690mm (margin 59.30%) | Group P&L | Calibration anchor. |
| FCF 2025 | $3,670mm | Group P&L FCF | Calibration anchor. |
| Operating Cash Flow 2025 | $6,820mm | (= EBITDA − cash taxes + change in NWC) | Calibration target. |

### Mars & Moon 2025

| 2025 metric | Q4'25 value | V30.5 location | Action |
|---|---|---|---|
| Mars & Moon R&D budget 2025 | $697.54mm | R425 D = $500mm | **Update R425 from $500M → $700M for 2025.** |
| Mars & Moon physical launches 2025 | 0 | R287 = 0 Lunar, R288 = 0 Mars | ✓ Already 0. |
| Mars & Moon mission cash spend 2025 | $0 | R287/R288 × R277/R282 logic | ✓ Zero. First physical launches Q4'25 has at 2028 transfer window. |

### Valuation 2025

| 2025 metric | Q4'25 value | V30.5 location | Action |
|---|---|---|---|
| Revenue multiple 2025 | 10x | R358 Starlink multiple = 10x | Match. |
| Implied EV 2025 (for cash-raise purposes) | $111.43B | Valuation tab | Anchor. |
| EBITDA multiple anchor | 18x | (not in V30.5 — V30.5 uses rev multiples) | Optional addition — could include both EBITDA × and Rev × in valuation. |

---

## 3. STRUCTURAL CORRECTION — ODC deployment is CASH-DRIVEN, not stub-driven

Per Q4'25 architecture: each year, compute sats launched = `cash_available_for_compute / sat_unit_cost`. **No fixed sat-count year-row.**

| V30.5 input | Value | Action |
|---|---|---|
| **R247 — ODC sats deployed per year (STUB year-row)** | D=0, I=3,800, AC=2,000 | **DROP ENTIRELY.** Replaced by allocator-driven deployment. ODC competes for cash + kg in outer queue. |
| ODC compute allocation share | — | **ADD NEW INPUT**: `ODC compute allocation share (% of investable cash post-Mars/Moon)` — Q4'25 anchor = 0.85. In your sigmoid-blend architecture this becomes a competing IRR signal, not a hardcoded share. |
| **R207 — ODC Compute power per sat (kW)** | 140 | **REVIEW.** Q4'25 W/kg = 70 in 2030 → 140 kW per 1,400 kg sat = 100 W/kg, 30% higher than Q4'25. Either V30.5 is V2-Compute-config-aggressive (defensible), or it's stale relative to Q4'25 calibration. |
| **R208 — Solar generation per sat (kW)** | 156 | Linked to R207 by design (~10% solar margin). Update with R207. |

The model behavior change: ODC growth becomes IRR-driven exactly like Starlink. Pre-revenue years (2025-2027) → ODC IRR negative → no ODC cash allocation → fleet stays at 0. Once Pr(A) × Model A + Pr(B) × Model B yields positive IRR → ODC competes for cash → fleet grows. Cap is allocator pool size + kg-to-LEO capacity, not a year-row stub.

---

## 4. ARBITRARY STUBS WITH NO HISTORICAL — drop unless you have a basis

These have no anchor in Q4'25 or any disclosed source. Recommend dropping or marking MC-wide. If you keep, lock the MC range.

| V30.5 cell | Label | Current value | Why arbitrary |
|---|---|---|---|
| R458 | Gbps per GWh/yr of ODC compute energy | 0.05 | Your own note: "PLACEHOLDER — pending research on token compression / multi-hop / duty cycle." No anchor exists. |
| R459 | BB-share of ODC bandwidth claim | 0.50 | Same — pending research. |
| R288 (S col) | Mars Starship slots reaching 2,000 in 2040 | 2,000 | Anchored to article reference. |
| R288 (AC col) | Mars Starship slots in 2050 | 20,000 | **10× growth from 2040 → 2050 has no anchor.** Q4'25 doesn't show 2050. If you have a Mach33 thesis driving 20K, lock it; otherwise scale down to ~5K or use 2030s growth rate trended forward (~3,000-5,000). |
| R289 (D col) | Labour unit cost 2026 | $30,000 | Anchored to Tesla Optimus aspirational pricing. Reasonable upper. |
| R29 | V2 Mini Bandwidth per Sat — DTC | 0.2 Gbps | Anchored — disclosed. Keep. |
| R31 | V3 Bandwidth per Sat — DTC | 2.75 Gbps | Anchored to V3 design — not disclosed publicly. Speculative but bounded. Keep with wide MC. |
| R241-R244 | Chip TDP / FP8 / mass / cost roadmap (H100 → AI5 → Dojo-3) | year-rows | Roadmap projection — H100 anchored; AI5 / Dojo-3 internal projections. Speculative. Keep but mark MC-wide. |
| R501 | Blended build cost per Starship vehicle | $32mm (40% × $35.1M SH + 60% × $23.4M ship) | Derived — anchored to R144 + R145 + R325. Keep. |
| R411 | Starlink R&D start % | 8% | Q4'25 has combined Starlink+Launch R&D at 15.87%. Decomposed by module, 8% on Starlink is high vs satcom peers (2-5%) — but defensible given V3 dev + DTC ramp. Mark MC [3%, 12%]. |
| R329 | Group WACC | 10% | Standard tech-growth WACC stub. Reasonable. Mark MC [8%, 14%]. |

---

## 5. WHAT TO KEEP AS-IS FROM V30.5 (Q4'25 confirms)

These V30.5 values match or align well with Q4'25 anchors. No change needed.

- **R38/R44** Satellite Cost per kg = $650 base (Q4'25: $643.50 in 2025)
- **R26** V2 Mini Mass = 575 kg (Q4'25: 575 kg in R458)
- **R28** V2 Mini BB Gbps = 96 (Q4'25: 96 in R449)
- **R30** V3 BB Gbps base = 1,000 (Q4'25: 246.57 in 2025 ramping to 330.05 in 2026 → trajectory toward V30.5's 1,000 by mid-2030s reasonable)
- **R41** Cumulative sats at base year = 7,486 (Q4'25: 7,486 at end-2024)
- **R56** TAM Inflation = 2.5% (industry standard, Q4'25 R20 implied)
- **R91/R92** V2 BB / DTC active end-2025 = 5,246 / 650 (Mach33 tracking; not in Q4'25 columns but consistent with V30.5 epistemic anchor)
- **R95** Legacy V1/V1.5 bandwidth = 71,888 Gbps (V30.5 own anchor)
- **R103** Legacy bandwidth runoff 4-yr straight-line
- **R195** F9 customer launch price — *update from $67M → $111M per Q4'25 R132*
- **R196** Starship customer launch price = $100M from 2027 (Q4'25 R133 had $240M in 2024 / $266.67M in 2025 — but pre-commercialization; V30.5's $100M from 2027 is forward-looking deflation, plausible)
- **R263** Lunar Mars capital lifetime = 10 years (Q4'25 R33 implied via book-value engine)
- **R269-R274** Labour unit shared parameters (Q4'25 has similar Optimus-class assumptions)
- **R277/R282** Lunar / Mars depot multipliers (Q4'25 has same rocket-equation-derived values)
- **R278/R283** Lunar / Mars payload per ship 50K / 100K kg (Q4'25 consistent)
- **R207-R215** ODC sat physical (V30.5 V2 Compute config; Q4'25 has W/kg = 70 in 2030 vs V30.5 implied 100 W/kg — mark for review)
- **R210/R211/R212** F_ref H100 = 1,979 / ECR = 0.6 / Workload mix 85% inference (Spec 3 anchors, Q4'25 consistent)
- **R250** Pr(A) on Model A = 0.6 (Spec 3.5 default; Q4'25 doesn't directly express but compatible)

---

## 6. RECOMMENDED ACTION LIST (before rebuild architecture spec)

In priority order:

1. **Fix R466 starting cash** $20B → $4.7B (or confirm $20B as deliberate Mach33 view with explicit rationale)
2. **Fix R53 Starshield decay rate** 1.0 → 0.25
3. **Fix R54 Starshield rev/Gbps** $167,421 → $164,699 (small)
4. **Fix R185 F9 starting fleet** 24 → 28
5. **Fix R195 F9 customer launch price** $67M → $111M (or update glide path)
6. **Bump R425 Mars/Moon R&D 2025** $500M → $700M
7. **Drop R247 ODC sats deployed STUB year-row entirely** — replace with cash-driven deployment (allocator pulls)
8. **Add ODC large-default cash + kg ask rows** (mirror Starlink R493/R494)
9. **Decide on R288 Mars slots 2050** 20,000 → ? (current is 10× growth 2040→2050 without anchor)
10. **Decide on R207 ODC compute power** 140 kW → keep aggressive or scale to Q4'25 W/kg = 70

Once you've nodded through these (or pushed back), the rebuild architecture spec locks the Assumptions tab values and the IRR engines can be designed against anchored historical 2025.

---

## 7. CALIBRATION TARGETS FOR THE REBUILD

The rebuild's 2025 outputs should match these Q4'25 anchors. If they don't, retune.

| Output | 2025 target | Source |
|---|---|---|
| Group Revenue | $14,650mm | Earth R145 |
| Starlink + DTC Revenue | $7,852mm | Earth R115 |
| Starshield Revenue | $2,520mm | Earth R121 |
| F9 Customer Launch Revenue | $4,290mm | Earth R136 |
| ODC Revenue | $0 | Earth R125 |
| Mars/Moon Revenue | $0 | (pre-revenue) |
| Group EBITDA | $8,690mm (59.3% margin) | Earth R179 |
| Group FCF | $3,670mm | Earth R223 |
| Group CapEx | ~$2,030mm | Earth R210 components |
| Constellation Depreciation | $707mm | Earth R195 |
| Total OpEx | $3,820mm | Earth R178 |
| F9 launches | 171 (132 Starlink + 39 customer) | Earth R68 |
| Starship launches | 0 | Earth R69 |
| Satellites launched (annual) | 3,840 | Earth R465 |
| Active satellites (end of year) | 9,832 | Earth R99 |
| Implied EV (10x Rev) | $111B | Earth R308 |

If the rebuild produces 2025 Group Revenue outside $14B-$15B band, halt and retune. Same for the other top-line anchors.
