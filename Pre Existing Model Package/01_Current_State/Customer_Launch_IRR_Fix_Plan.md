# Customer Launch IRR Fix — Design Spec

**Status:** Draft design doc. Holds until Vlad slots into the reworked sprint roadmap.
**Affects:** Customer Launch tab (IRR engine), Assumptions block, possibly Launch Capacity at-cost composition.
**Goal:** Make F9 and Starship per-vehicle IRR apples-to-apples with the Starlink per-sat IRR engine.

---

## 1. Diagnosis (three compounding bugs)

The Customer Launch per-launch IRR engine (R117-R144) prints 287% F9 Blended IRR in 2025 vs 100% for Starlink V2 BB. The spread is mostly artifact, not signal.

**Bug 1 — Unit mismatch on N.** R119 / R121 compute `N = MIN(life clamp MAX years, lifetime reuses)`. `Lifetime reuses` is a launch count; the clamp is in years. The MIN compares two different units and outputs a value that is then consumed as an annual-IRR period count.

**Bug 2 — Per-launch margin masquerading as annual.** R131 label reads `$mm/yr — cadence × per-launch margin` but the formula `=D17-D34-D37` returns per-LAUNCH margin with no cadence multiplier. The IRR cashflow stream `(-D130, D131, D131, ...)` is therefore one launch's margin treated as one year of margin. Same defect on R141 (Starship).

**Bug 3 — Cost slug not fully-allocated.** F9 t=0 capex (R130) is just the booster manufacturing cost ($30M). Starlink's per-sat cost (R211) is sat unit cost + facility allocation per sat ($0.46M for V2 BB). Per-launch margin is also short: R131 subtracts variable cost (R34) only, not the full at-cost rate (R36 = variable + D&A share + fairing net of recovery).

Starship (R140-R144) has the identical architecture. It currently reads IRR=0 because per-launch margin is negative in 2025-26 (price=$0 until customer ramp). Once margin turns positive in 2027-28, the same blowup pattern activates.

---

## 2. Target framing — mirror Starlink

Switch Customer Launch from a per-launch IRR with N-launches to a **per-booster annual IRR with N-years**, matching Starlink's per-sat per-year structure.

| Component | Starlink (canonical) | Customer Launch (target) |
|---|---|---|
| t=0 capex slug | Per-sat cost = sat unit cost + facility per sat | Per-booster cost = booster mfg cost + Launch facility allocation per booster |
| Annual margin | Per-sat net marginal revenue per year | Per-booster annual margin = per-launch fully-allocated margin × cadence per booster per year |
| N | Economic life N (years), from Assumptions | Booster economic life in years, derived from lifetime reuses ÷ cadence |
| IRR engine | `IRR(IF(SEQUENCE(N+1)=1, -cost, annual_margin))` | Same, with per-booster inputs |
| Forward IRR | Y+2 offset via INDEX over the IRR row | Unchanged — pattern carries over |
| Blended IRR | (1-w)·Spot + w·Forward | Unchanged |

Per-booster framing is the right marginal-capital unit (matches Architecture §6.5 per-sat marginal IRR logic). The capital decision being signaled is "build one more booster" — not "fly one more launch."

---

## 3. Inputs required (Assumptions block additions)

Three labeled inputs to add. All `$B` column, by-label resolution. MC-eligible (Rule 22 — anything arbitrary is MC).

| Label (canonical) | F9 default | Starship default | Source / notes |
|---|---|---|---|
| `F9 booster economic life (years)` | derived: 50/12 ≈ 4.2; recommend lock at 8 to reflect realized cadence-utilization (Launch Capacity R65 = 6.1) | n/a | Year flat for F9 |
| `Starship booster economic life (years)` | n/a | year-row, derived from Launch Capacity R21 / R23 | Year-row — both reuses and cadence ramp |
| `Launch facility allocation per booster ($mm/booster)` | open — see §6 | open — see §6 | Starbase / pad / tower CapEx amortized over expected fleet |

Existing inputs reused: F9 cadence per booster (Launch Capacity R51 = 12 flat; R65 utilization = 6.1), Starship cadence (Launch Capacity R23), lifetime reuses (Launch Capacity R50 / R21).

---

## 4. Customer Launch tab rewrites

### F9 block (R117-R134, R207-R209 unchanged downstream)

- **R118** — keep (lifetime reuses memo, reference only).
- **R119 (rebuild)** — `F9 booster economic life N (years)`. Formula: `=INDEX(Assumptions!$B:$B, MATCH("F9 booster economic life (years)", Assumptions!$A:$A, 0))`. Year-flat.
- **R130 (rebuild)** — `F9 per-booster cost slug ($mm — t=0 capex)`. Formula: `= booster mfg cost + Launch facility allocation per booster`, both by-label from Assumptions.
- **R131 (rebuild)** — `F9 per-booster annual margin ($mm/yr)`. Formula: `=(D17 - D36 - D37) * D_cadence` where D36 is the full at-cost rate (Launch Capacity R71 by label, not R69 variable cost — captures D&A and fairing), and D_cadence is realized cadence per booster per year by-label from Launch Capacity (R65 utilization, not R51 ceiling).
- **R132 / R133 / R134** — IRR formulas keep their shape. Spot IRR runs `IRR(IF(SEQUENCE(D$119+1)=1, -$D$130, D131))`. Forward IRR offsets to year+2. Blended IRR unchanged.

### Starship block (R117-R121, R140-R144)

- **R121** — `Starship booster economic life N (years)`, year-row. Formula: `=Launch Capacity R21 / Launch Capacity R23` (by label), clamped at MAX life clamp.
- **R140** — `Starship per-booster cost slug ($mm)`. Formula: `= Starship mfg cost per stack + Launch facility allocation per booster` (year-row). Starship mfg already loaded in Launch Capacity R37 — keep that read, add facility allocation.
- **R141** — `Starship per-booster annual margin ($mm/yr)`. Formula: `=(D18 - Launch Capacity at-cost rate R40 by label - per-launch insurance/other) * Launch Capacity R23 cadence`. Anchor-and-offset on the year-row.
- **R142 / R143 / R144** — unchanged shape, consume corrected inputs.

### Combined Customer Launch IRR (R207-R209)

No structural change. R207 (Spot), R208 (Forward), R209 (Blended) already blend F9 and Starship by weighted-launch-share. Confirm weighting still resolves cleanly when both vehicles report on the same units (annual, per-booster) — which they now do.

---

## 5. Allocator queue + downstream

No allocator-side changes required for this fix. R42 (Allocator §4 Customer Launch Blended IRR) and R99 (§6 Customer Launch Blended IRR) keep their by-label INDEX/MATCH reads.

Note for the vehicle-level Allocator sprint (Sprint 10.7 per memory): if Customer Launch splits into separate F9 and Starship queue entries with their own per-vehicle IRR sigmoid rows, this fix is a prerequisite — without it the F9 row dominates the queue on artifact, not signal.

---

## 6. Open decisions — need Vlad to lock

These are the parameters with real epistemic weight; the rest is mechanical.

1. **`F9 booster economic life (years)` — value lock.** Three candidates:
   (a) 50 / 12 ceiling = 4.2 years (uses cadence ceiling — too optimistic)
   (b) 50 / 6.1 utilization = 8.2 years (uses realized cadence — matches Launch Capacity R65)
   (c) Lock at 8 years and treat as MC range [6, 10]
   **Recommend (c).**

2. **`Launch facility allocation per booster ($mm/booster)` — does this exist, and if not, how do we anchor it?**
   The Starlink per-sat IRR engine loads a facility share (V2 BB facility per sat ≈ $0.09M). Customer Launch has no analogous loading today. Pad/tower/Starbase CapEx is real but currently flows through Launch Capacity at-cost rate via the D&A share. **Question for Vlad:** is the D&A share in R36/R40 already capturing it, or should the IRR engine additionally load a per-booster facility share? Two views:
   (a) If at-cost rate is fully-loaded (D&A share covers pad capex amortized over launches), then per-launch margin already subtracts it — no separate per-booster facility line needed. Set facility allocation = 0.
   (b) If pad capex is amortized over LAUNCHES (not boosters), the per-launch margin captures it correctly via the at-cost rate. Then the per-booster IRR engine doesn't need a separate facility slug. **This is most likely correct under fully-allocated at-cost methodology (2026-05-20 amendments).**
   **Recommend (b).** Facility allocation per booster = 0 — pad capex is fully captured in the per-launch at-cost rate.

3. **Switching R131's price/cost basis from `R17 - R34 - R37` to `R17 - R36 - R37`** (variable → fully-allocated at-cost). This is the IRR-engine-side analog of the calibration shift. Confirm: do we want the IRR to reflect contribution margin (current, after variable cost only) or fully-allocated margin (proposed, net of D&A share)? Starlink R212 is fully-allocated. **Recommend matching Starlink — switch to R36 / R40 fully-allocated at-cost rate.**

---

## 7. Validation targets (sanity checks)

Pencil math under the proposed fix (using F9 defaults: booster $30M, economic life 8 years, cadence 6.1 flights/booster/yr, per-launch margin $111 - $19 fully-allocated - $7.77 insurance ≈ $84M, annual margin = $84 × 6.1 ≈ $512M):

- F9 Spot IRR ≈ `IRR(-30, [512]*8)` ≈ 1700%. **Still implausibly high** — flags a deeper issue: the booster cost slug is too thin relative to the cashflow stream it underwrites, even fully-allocated. Reuse value is real but undermeasured here.

Vlad: this suggests the fix is *necessary but not sufficient*. A second pass may be needed where we load the EXPECTED fleet build cost over the booster's economic life (not just one booster), or where we treat the IRR engine as ratio-of-lifetime-cashflow rather than year-by-year. Worth a phone-call-style decision before locking the spec.

Target sanity outcomes after fix:
- F9 Blended IRR: 100-300% range (high but bounded, similar to V3 BB)
- Starship Blended IRR: -50% to 50% (negative in early years, climbing as price ramps)
- F9 < V3 BB once V3 ramps (correct: mature platform vs new high-margin growth vehicle)
- Starship < F9 in 2025-27 (correct: early-life, underutilized cadence)

---

## 8. Out of scope for this fix

- Allocator queue restructuring (vehicle-level allocator is Sprint 10.7 per existing memory).
- Demand Curves rebuild (Sprint 10.5 per existing memory).
- Customer Launch margin CAGR amendment (already absorbed in Sprint 8.5).
- Launch Capacity at-cost rate composition audit — flagged as a sibling investigation if §6 Q2 surfaces a gap.
