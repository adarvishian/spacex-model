# Sprint Roadmap + Verification Protocol — Constitutional Document for SpaceX Model Rebuild v2

**Status**: Constitutional. Locked 2026-05-19.
**Authority**: Source of truth for sprint sequencing and "is this sprint done?" criteria.
**Companion docs**: `01_Lessons_Learned.md`, `02_Architecture_and_Methodology.md`, `Model Execution Rules.md`, `2025 Anchors from Q4_25.md`.

This doc has two halves. Part A is the sprint roadmap (12 sprints, dependencies, day budget). Part B is the verification protocol (universal sprint completion criteria + sprint-specific calibration targets).

---

# PART A — Sprint Roadmap

## §0 — Build philosophy

**Architecture first, brain last.** Sprint 0 builds the Assumptions tab. Sprint 1 builds the Allocator skeleton + all module shells with the IN/OUT contract pre-wired but module bodies empty and allocator logic dormant. Sprints 2-7 fill module bodies one at a time, each with its per-sat / per-launch IRR engine and Allocator OUT contract live (against module-derived demand, not allocator-driven). Sprints 8-9 light up Group P&L + OpEx + CapEx aggregation. Sprint 10 finally lights up the allocator brain (IRR-priority sigmoid blend live; cash pool tracker reads Group FCF; queue gate reserves non-module claims). Sprint 11 builds Valuation. Sprint 12 layers MC ranges + outputs Pre-IPO deliverable.

**Why this order**: The original V30.5 build went module-by-module with allocator logic added incrementally across Sprints 5-7. Each layer (Layer 1, Layer 2, Layer 3) broke module IRRs that had been calibrated against the prior allocator state. Net result: 3+ retrofit passes per allocator change. The rebuild reverses this — modules calibrate against their own demand first (so 2025 outputs hit Q4'25 anchors), THEN the allocator overlay reshapes deployment in out-years. No retrofit cascade.

**Day budget**: 12 sprints, target 12-14 build days. Buffer 2-3 days for patches / sanity-check retunes. Total budget ~15-17 days. Tighter than the 2-week-ish IPO window; depends on no major sprint blow-ups.

## §1 — Sprint inventory (12 sprints)

| # | Sprint | Tabs touched | Day budget | Depends on |
|---|---|---|---|---|
| 0 | **Assumptions tab + workbook standards** | Assumptions (built), all tabs (year header + offset rows) | 1 day | Constitutional docs |
| 1 | **Allocator skeleton + module shells** | Allocator, all module tabs (IN/OUT contract rows, no bodies) | 1 day | Sprint 0 |
| 2 | **Launch Capacity tab** | Launch Capacity (full build), Assumptions (Starship/F9 inputs) | 1 day | Sprint 1 |
| 3 | **Customer Launch module** | Customer Launch (full body), Assumptions (Launch inputs) | 1 day | Sprint 2 |
| 4 | **Starlink module + Starlink Capacity tab** | Starlink (full body, V2/V3 pools, ratchet, historical fleet retirement), Starlink Capacity (full build) | 1.5 days | Sprint 1 (independent of 2-3) |
| 5 | **ODC module** | ODC (full body, per-sat IRR, dual revenue, bandwidth claim live) | 1.5 days | Sprint 4 (Starlink Capacity bandwidth rates) |
| 6 | **AI Stack module** | AI Stack (full body, product lines, internal compute cost from ODC) | 1 day | Sprint 5 (ODC for internal compute) |
| 7 | **Lunar Mars module** | Lunar Mars (BV engine, mission CapEx, NOT in IRR queue) | 1 day | Sprint 1 (independent of 2-6) |
| 8 | **OpEx tab + CapEx tab** | OpEx (R&D by module + SG&A by function), CapEx (corporate + spectrum + module aggregation) | 1 day | Sprints 3-7 (reads module CapEx + Group rev) |
| 9 | **Group P&L** | Group P&L (full walk, conservation block, eliminations) | 1 day | Sprint 8 |
| 10 | **Allocator brain light-up** | Allocator (cash pool live, queue gate live, IRR sigmoid blends live, vehicle build claim live, central IRR display) | 1 day | Sprint 9 |
| 11 | **Valuation** | Valuation (DCF + SoTP + Comparables + Sensitivity) | 1 day | Sprint 9 |
| 12 | **MC overlay + Pre-IPO outputs** | Assumptions (MC range columns), Valuation (MC engine), output extraction | 1 day | Sprint 11 |

**Total**: 13 days build budget. Add 2-3 buffer days for patch sprints (X.5 numbering pattern).

## §2 — Dependency graph

```
                            [Constitutional docs]
                                     │
                                     ▼
                             [Sprint 0: Assumptions]
                                     │
                                     ▼
                            [Sprint 1: Skeleton + shells]
                                     │
                  ┌──────────────────┼──────────────────┬──────────────────┐
                  ▼                  ▼                  ▼                  ▼
        [Sprint 2: Launch Cap]  [Sprint 4: Starlink + SC]  [Sprint 7: Lunar Mars]
                  │                  │
                  ▼                  ▼
        [Sprint 3: Cust Launch]  [Sprint 5: ODC]
                                     │
                                     ▼
                                [Sprint 6: AI Stack]
                                     │
                  ┌──────────────────┴──────────────────────────┐
                  ▼                                              ▼
            [Sprint 8: OpEx + CapEx]                       (Sprint 7 also feeds here)
                  │
                  ▼
            [Sprint 9: Group P&L]
                  │
                  ├──────────────────┬──────────────────┐
                  ▼                  ▼                  ▼
        [Sprint 10: Allocator]  [Sprint 11: Valuation]
                                     │
                                     ▼
                            [Sprint 12: MC + Pre-IPO]
```

**Parallelism possible**: Sprints 4 (Starlink) + Sprint 7 (Lunar Mars) can be drafted in parallel since they don't depend on each other. Realistically, separate plugin execution chats so I do the spec work sequentially in this chat, but plugin execution can run them concurrently if Vlad has bandwidth.

---

## §3 — Per-sprint scope (concise)

### Sprint 0 — Assumptions tab + workbook standards

**Scope**: Build the Assumptions tab from `04_Assumptions_Tab_Spec.md` (consolidated doc, task #17 — drafted before Sprint 0 fires). Establish workbook standards on every tab that will hold year columns: year header at row 4 (D=2025 ... AC=2050, hardcoded integers), year-offset helper at row 5 (D=0 ... AC=25, hardcoded integers).

**Inputs**: Constitutional docs (Architecture §1 tab inventory, §2 year horizon, §17 calibration targets).

**Outputs**: Populated Assumptions tab. Year header + offset row on every tab (even tabs that will be built later — pre-stage).

**Acceptance**: 2025 anchored values match `project-anchored-assumptions-2025` memory ($5B starting cash, 28 F9 fleet SoY, $111M F9 launch price, $700M Mars/Moon R&D, etc.). MC range columns populated for every input flagged MC-variable.

### Sprint 1 — Allocator skeleton + module shells

**Scope**: Build Allocator tab skeleton (section headers for Cash Pool Tracker, Queue Gate, Mars Carve-out, Cash Sigmoid Queue, Kg Sigmoid Queue, Vehicle Build Claim, Central IRR Display). Build module tab shells with: (a) Allocator IN block at top (Capital Allocation, Starship Capacity Allocation, Total Capital Available — INDEX/MATCH against Allocator) reading 0 placeholders for now, (b) Allocator OUT block at bottom (the 11 canonical rows from Architecture §4.2 — placeholders).

**Inputs**: Sprint 0 (Assumptions tab + year header/offset standards).

**Outputs**: Allocator tab structure (no live logic). Module shells (Customer Launch, Starlink, Starlink Capacity, ODC, AI Stack, Lunar Mars) — IN/OUT contract live by label, module bodies empty.

**Acceptance**: Every Allocator IN row on every module resolves to 0 (placeholder). Every Allocator OUT row on every module resolves to 0 (placeholder). Conservation block on Group P&L (built but not populated) reads OK at trivial 0 = 0 level. No #REF!/#NAME! errors.

### Sprint 2 — Launch Capacity tab

**Scope**: Full build of Launch Capacity tab. Starship section: vehicle costs, payload (booster-only mode 150K kg + fully reusable 100K kg), variant mix year-row, Wright's Law on cum upmass driving cadence (Sprint 1.5 mechanic), fleet build (boosters + ships built per year), cost stack ($/kg blended, total annual capacity kg-to-LEO). F9 section: vehicle costs, payload 22.8K kg, fleet decay logic (post-V3-trigger), per-launch ops cost. Output rows: Total Starship capacity (kg), F9 launches available, blended $/kg. NOT a P&L module — no Allocator IN/OUT contract.

**Inputs**: Sprint 1 (Allocator IN reads kg from here). Assumptions §3 (Starship + F9 inputs).

**Outputs**: Launch Capacity tab fully populated. Starship 2025 capacity ~450K kg (low — fleet not built yet). F9 launches 2025 = 171.

**Acceptance**: F9 launches 2025 = 171 ±5. F9 fleet end-2025 ≈ 39 ±5. Blended $/kg 2025 in $400-$800/kg range (early fleet, low N). Wright's Law cadence converges (cadence per booster 2025 ≈ 1, ramping to ~10-15 by 2030).

### Sprint 3 — Customer Launch module

**Scope**: Customer Launch module body. F9 external customer launches (commercial + government markets from Assumptions §4); Starship customer launches from 2027 with price decline. Per-launch marginal IRR engine (CF stream: −cost per launch, +(market price − COGS) for N years). Internal transfer revenue line (placeholder; lights up when consuming modules' launch services cost rows populate in Sprints 4-7). At-cost transfer pricing per Architecture §7.1 (locked 2026-05-20 — fully-allocated). Allocator OUT contract fully wired.

**Locked-this-sprint decisions (added 2026-05-20):**

1. **Vehicle D&A fallback ownership.** If Sprint 2 did not produce the canonical `Annual vehicle D&A ($mm)` and `At-cost launch services rate ($mm/launch)` rows on Launch Capacity, Sprint 3 takes them on the Customer Launch tab instead. Either home is acceptable per Architecture §6.6; canonical labels stay the same so all consuming-module INDEX/MATCH refs resolve regardless. Sprint 3 pre-flight reads Launch Capacity!$A:$A for the canonical labels — if present, Sprint 3 sources from there; if absent, Sprint 3 builds them locally. Document which home in the Sprint 3 Claude Log entry.
2. **Module CapEx vs Capital deployed convention** (Architecture §4.2, locked 2026-05-20). Customer Launch is the first module sprint to populate both rows. Row 205 (Module CapEx) = annual cash outlay for ground equipment + customer integration (NOT vehicle build — that's the non-module claim at the queue gate). Row 206 (Capital deployed) = equilibrium-equal to row 205 in Sprint 3 (no in-progress build lag for Customer Launch). Sprint 3 sets the convention that subsequent module sprints inherit: Capital deployed = Module CapEx unless the module has an explicit CapEx lag (Starlink R82 = 1 year is the only known case).
3. **Fully-allocated at-cost launch services rate.** Per Architecture §7.1, the at-cost rate published to consuming modules = variable cost per launch + vehicle D&A per launch. Sprint 3 writes the formula on whichever tab owns the canonical row (Launch Capacity or Customer Launch per point 1).

**Inputs**: Sprint 2 (Launch Capacity supply). Assumptions §4 (Customer Launch inputs).

**Outputs**: Customer Launch external revenue 2025 = $4.29B. Per-launch marginal IRR engine reports Spot/Forward/Blended IRR rows on Allocator OUT (live, but reads against placeholder allocations from Allocator).

**Acceptance**: F9 customer revenue 2025 = $4.29B ±5%. Starship customer revenue 2025 = $0 (pre-commercialization). Per-launch Blended IRR 2025 in 8-25% range (anchored to external customer economics, not fleet-level). Module FCF 2025 captured. Capital deployed (row 206) = Module CapEx (row 205) every year (no lag on Customer Launch).

### Sprint 4 — Starlink module + Starlink Capacity tab

**Scope**: Most complex module sprint. Two tabs:

**Starlink tab**: V2 BB / V2 DTC / V3 BB / V3 DTC vehicle build with BB/DTC pool sigmoid blend (Architecture §8.1). V2/V3 ratchet (Architecture §8.2 single flag latch). V2 historical fleet linear retirement over useful life (§8.3). Bandwidth-driven revenue (Architecture §8.4 — bandwidth Gbps × $/Gbps from Demand Curves; subscribers derived as Revenue / ARPU). Constellation D&A, terminal COGS, spectrum amortization (BB only), ground ops, insurance, other COGS. Per-vehicle marginal IRR engines. Allocator OUT contract wired.

**Starlink Capacity tab**: Aggregates Starlink constellation BB + DTC pools. Reads ODC bandwidth claim from ODC tab (will be 0 until Sprint 5 wires it; Spec 04 architecture). At-cost transfer pricing per pool **(fully-allocated per Architecture §7.2, locked 2026-05-20)**: BB pool cost basis = Gbps-share-weighted Constellation D&A + Ground ops + Spectrum amort (BB only); DTC pool cost basis = same minus Spectrum. Pool $/Gbps/yr = pool cost basis / total active pool Gbps. ODC pays its Gbps-share × the appropriate pool rate. Available bandwidth (post-internal-claim) for external Starlink revenue.

**Locked-this-sprint decision (added 2026-05-20):** Spectrum amort flows to Starlink BB COGS only (DTC uses MSS bands — no analogous intangible). The at-cost rate to ODC inherits the spectrum amort share via the BB pool cost basis. Capital deployed = Module CapEx for Starlink BB / DTC vehicle pools in equilibrium; differ in the CapEx Lag year (Assumptions R82 = 1 year) — that's the documented exception to the Sprint 3 convention.

**Inputs**: Sprint 1 (skeleton). Assumptions §5 (Starlink inputs).

**Outputs**: Starlink + DTC revenue 2025 = $7.85B. Starshield revenue 2025 = $2.52B. Active sats end-2025 ≈ 9,800 (V2 BB 5,246 + V2 DTC 650 + 2025 V2 launches 3,169 + legacy V1/V1.5 ≈ 750). Per-vehicle Blended IRR live on Allocator OUT.

**Acceptance**: Revenue targets hit ±5%. Net subscriber path derived from revenue (Refine Spec 03 architecture). BB ARPU implied = $100/mo, DTC ARPU = $16/mo in 2025. V2/V3 ratchet not yet fired (V3 launches = 0 in 2025). V2 historical retirement starts in 2025 (R54 = 5,246/5 = 1,049.2 V2 BB retired in 2025).

**Risk**: V9 logic inheritance — Demand Curves tab provides bandwidth demand year-row. Starlink revenue formula must consume Available BB Gbps from Starlink Capacity tab (post-internal-claim), not Total BB Gbps. Wiring order matters.

### Sprint 5 — ODC module

**Scope**: Most complex single module sprint. ODC body: sat physical specs (V2 Compute 140 kW per sat, 1400 kg dry mass), chip roadmap year-rows (H100 → AI5 → Dojo-3 linear interp), subsystem cost build (Wright's Law on subsystems, no learning on chips), per-sat Model A revenue (energy-anchored), per-sat Model B revenue (η-anchored), Pr(A)-weighted Expected Revenue. **Cash-driven deployment** (NO fixed stub year-row): ODC reads Cash Demand from its own per-sat economics and competes in outer queue. Per-sat marginal IRR engine. Bandwidth services cost (paid to Starlink, links Starlink Capacity tab's BB+DTC at-cost rates × ODC bandwidth claim). External vs internal compute split (% to AI Stack at-cost transfer, % to external customers at market). Allocator OUT contract wired.

**Locked-this-sprint decision (added 2026-05-20):** ODC → AI Stack internal compute pricing is **fully-allocated** per Architecture §7.3 (locked 2026-05-20). Rate per PFLOP-hr = (ODC fully-allocated annual cost) / (ODC total annual PFLOP-hrs). Fully-allocated cost = annual sat D&A + launch services cost paid to Launch Capacity + bandwidth services cost paid to Starlink + insurance + other COGS. ODC's per-sat marginal IRR engine reads off **external compute revenue only** (Principle 9 + §7.3) — internal at-cost transfers don't contribute IRR signal. The Sprint 5 spec writes the canonical row `ODC at-cost compute rate ($/PFLOP-hr)` on the ODC tab; AI Stack reads it by INDEX/MATCH in Sprint 6.

**Inputs**: Sprint 4 (Starlink Capacity bandwidth rates). Assumptions §6 (ODC inputs).

**Outputs**: ODC revenue 2025 = $0 (pre-deployment). ODC sats deployed 2025 = 0. Per-sat marginal IRR engine live — reads Pr(A) × A + (1−Pr(A)) × B; computes Spot/Forward/Blended IRR with N=5 years.

**Acceptance**: ODC revenue 2025 = $0 exact. ODC sats deployed 2025 = 0 exact. Per-sat marginal IRR converges (no #NUM! leaks to Allocator OUT). Starlink Capacity tab's BB and DTC at-cost rates feed ODC bandwidth cost line cleanly.

**Risk**: Bandwidth flow architectural complexity (Refine Spec 04). Per-sat marginal IRR mechanic identical to Starlink V3 BB pattern (Spec 09 Patch M / Spec 08 Patch P). Cash-driven deployment means ODC fleet stays at 0 until allocator-driven (Sprint 10) deals it cash. Pre-2027 ODC IRR likely zero or negative — module produces 0 deployment, which is correct.

### Sprint 6 — AI Stack module

**Scope**: AI Stack standalone module body. Three product lines: Cursor (subscription seats × $/seat/mo × 12), Grok consumer (subs × $/sub/yr), Grok enterprise API (tokens × $/Mtoken). Internal compute cost from ODC (at-cost transfer per Architecture §7.3 + §10). Per-product OR composite IRR engine (resolve in spec drafting — recommend composite for simplicity). Capacity Demand = 0 on Allocator OUT (terrestrial). Allocator OUT contract wired.

**Inputs**: Sprint 5 (ODC for internal compute cost). Assumptions §7 (AI Stack inputs).

**Outputs**: AI Stack revenue 2025 = ~0 (Cursor + Grok early ramp; may be small positive). Per-product IRR rows live.

**Acceptance**: AI Stack revenue 2025 close to 0 (pre-revenue or early-ramp). Internal compute cost from ODC reads at-cost transfer cleanly. No double-counting with ODC external revenue.

**Risk**: Per-product vs composite IRR — composite is simpler but loses product-level signal. Default to composite, revisit if Grok API economics dominate disproportionately.

### Sprint 7 — Lunar Mars module

**Scope**: Lunar Mars module body. Per Sprint 4 / Q4'25 architecture: BV engine (labour units + hardware). Labour units shared parameters (mass 60 kg, hourly output, productivity learning, useful life 5 yrs). Lunar / Mars depot multipliers (1× / 5×). Lunar / Mars payload per surface-landed Starship (50K / 100K kg). Strategic carve-out cash drives deployment (NOT exogenous slot year-rows — R287/R288 dropped). Mission ops % of CapEx. Standard 11-row Allocator OUT contract (IRR rows = 0; no IRR engine for Lunar Mars). Two extra rows for Lunar BV + Mars BV diagnostics.

**Inputs**: Sprint 1 (skeleton). Assumptions §8 (Lunar Mars inputs). Sprint 9 will eventually feed Group FCF for prior-year carve-out — Sprint 7 uses placeholder $0 prior FCF for 2025 (carve-out reads from R225 starting cash floor).

**Outputs**: Lunar Mars 2025: Revenue = 0, Mission CapEx = 0 (no physical launches; pre-2027 windows), Mars/Moon R&D $700M flows through OpEx (Sprint 8 will route it).

**Acceptance**: Module Revenue = 0 every year. Mars/Moon R&D 2025 = $700M (Q4'25 anchored). Strategic carve-out cash drives Lunar / Mars ships deployment in out-years (verify by 2030+ Mars fleet > 0). BV engine produces Lunar BV ramping per ship landed.

### Sprint 8 — OpEx tab + CapEx tab

**Scope**: Build OpEx tab (R&D by module per Architecture §12.1: Starlink 8% → 3% / Customer Launch 25% → 4% / ODC 30% → 8% / AI Stack 15% → 5% — anchor-and-offset bounded CAGR; Mars/Moon $-profile year-row). SG&A by function (§12.2). Build CapEx tab (module CapEx aggregation, corporate CapEx + useful lives, spectrum CapEx + 15-yr amortization). Corporate D&A schedule. Output: Total OpEx ($mm/yr) feeds Group P&L; Total Group CapEx feeds Group P&L; Spectrum amortization feeds Starlink COGS.

**Locked-this-sprint decisions (added 2026-05-20):**

1. **Pre-revenue R&D switch for ODC + AI Stack** (Architecture §12.1, locked 2026-05-20). ODC R&D = 30% × ODC revenue gives $0 in 2025–2027 by design — wrong because ODC physically has heavy R&D pre-revenue. Same problem on AI Stack early-ramp years. Sprint 8 implements a switching formula on both modules' R&D rows: `R&D_t = MAX($-profile_t, % × revenue_t)`. The $-profile dominates pre-revenue; the % × revenue formula takes over once it exceeds the floor. Sprint 8 spec adds two new Assumptions year-rows: `ODC R&D $-profile ($mm/yr)` and `AI Stack R&D $-profile ($mm/yr)`. Suggested Base Case trajectories — ODC: $200M 2025 → $500M 2027 (peak Starship + chip dev) → declining as % × rev takes over; AI Stack: $50M 2025 → $300M 2028 → declining similarly. Vlad to lock both trajectories before Sprint 8 fires. These are MC-variable (lognormal — skewed upside). Both new Assumptions rows append below existing inputs (no row insertions).
2. **AI Stack added to S&M base** (Architecture §12.2, locked 2026-05-20). S&M base now = Starlink + Starshield + Customer Launch external + AI Stack rev. Same `4% start → 2% end, −8%/yr` glide path applied to the expanded base. Sprint 8 spec writes the formula reading from each of the four module revenue rows by INDEX/MATCH.
3. **Capital deployed vs Module CapEx aggregation** (Architecture §4.2, Sprint 3 convention). CapEx tab module aggregation reads Module CapEx (row 205) from each module, NOT Capital deployed (row 206). Capital deployed is diagnostic-only and does not feed Group CapEx. Sprint 8 spec verifies the convention via a memo conservation check: Σ Module CapEx − Σ Capital deployed should be 0 in equilibrium (only Starlink CapEx Lag year deviates).

**Inputs**: Sprints 3-7 (module CapEx + revenue reads). Assumptions §9-10 (OpEx + CapEx inputs). Plus two new $-profile year-rows added pre-execution.

**Outputs**: Total OpEx 2025 = $3.82B. Corporate D&A ramp. Spectrum CapEx 2025 = $5B (EchoStar Year 1). ODC R&D 2025 ≈ $200M (from $-profile floor, since ODC rev = $0). AI Stack R&D 2025 ≈ $50M (from $-profile floor).

**Acceptance**: Total OpEx 2025 = $3.82B ±5%. Mars/Moon R&D 2025 = $700M ±5% (anchored). ODC R&D 2025 = $200M ±20% (new floor; loose tolerance pending Vlad anchor). AI Stack R&D 2025 = $50M ±20% (same). R&D by module sums to ~$2.5B 2025 (Starlink ~$830M + Customer Launch ~$1,073M + ODC ~$200M floor + AI Stack ~$50M floor + Mars/Moon $700M = ~$2,853M — slightly above the Q4'25 R175 ~$2.3B anchor; reflects the pre-revenue R&D fix). SG&A sums to ~$1.5B 2025 (AI Stack S&M addition is small in 2025 because AI Stack revenue is small).

### Sprint 9 — Group P&L

**Scope**: Build full Group P&L walk (§15.1). Inter-module eliminations block (R42-R45 for launch services / bandwidth / compute). Conservation block (§15.2 R99-R110 — Revenue / EBITDA / CapEx / FCF / D&A / EBIT consistency / launch elim / bandwidth elim / compute elim / ALL OK boolean / cash flow identity).

**Inputs**: Sprint 8 (OpEx + CapEx). Sprints 3-7 (module reads).

**Outputs**: Group Revenue 2025 = $14.65B, Group EBITDA = $8.69B (59.3% margin), Group D&A = $1.06B, Group EBIT = $7.63B, Taxes = $1.60B (21%), NOPAT = $6.03B, Total D&A add-back = $1.06B, Total Group CapEx = $2.03B, Group FCF = $5.06B (note: Q4'25 R223 = $3.67B — slight delta; will reconcile).

**Acceptance**: Conservation block R108 = "OK" in every year 2025-2050. Group Revenue 2025 = $14.65B ±5%. Group EBITDA 2025 = $8.69B ±5% (margin 59.3% ±2pp). Group FCF 2025 = $3.67B ±10% (some give for D&A treatment differences). All eliminations balance (launch services / bandwidth / compute internal transfer revenue = consuming modules' COGS).

**Risk**: This is the big calibration moment. If Group P&L outputs miss Q4'25 targets, halt and trace through module sprints. Likely culprits: wrong revenue formula in a module (Starlink bandwidth vs sub-driven), missing elimination row, double-counting D&A.

### Sprint 10 — Allocator brain light-up

**Scope**: Light up the Allocator logic that's been sitting dormant since Sprint 1. Cash pool tracker reads Group FCF (now live from Sprint 9) and computes Cash BoY for each year. Queue gate computes non-module claims (OpEx + Corp CapEx + Spectrum + Taxes + Mars carve-out) and subtracts from Cash BoY to produce Available Cash for IRR Queue. Cash IRR-priority sigmoid blend goes live: reads Blended IRR from each in-queue module (Customer Launch, Starlink — multiple vehicles, ODC, AI Stack) and allocates cash. Kg IRR-priority sigmoid blend same. Vehicle build claim sized by forward-aggregate-kg-demand (Architecture §6.6). Central IRR display panel populates.

**Inputs**: Sprint 9 (Group FCF). Sprint 7 (Lunar Mars BV). All module IRR engines (Sprints 3-6 + Starlink vehicle IRRs from Sprint 4).

**Outputs**: Allocator IN cells on every module switch from 0 placeholders to live IRR-driven allocations. Module deployment rebalances — Starlink fleet ramp shifts vs initial demand stubs; ODC fleet starts ramping in 2027+ as per-sat IRR turns positive; etc.

**Acceptance**: Conservation holds with allocator live. Year-N non-module claims subtracted before queue (verify Available Cash for Queue < Cash BoY by the claim amount). No module gets negative allocation. Negative-IRR modules get zero allocation. Sigmoid shares sum to 1 within rounding.

**Risk**: New within-year circular dependencies — module CapEx ← Allocator allocation ← module IRR ← module FCF ← module CapEx. Iterative calc must converge in <10 iterations. If bistability emerges (Principle 22), document and accept; may need to break circularity via prior-year reference somewhere.

**Likely outcome**: 2025 outputs SHIFT from their post-Sprint-9 baseline because allocator now drives module deployment. May need a Sprint 10.5 retune to keep 2025 outputs within ±5% of Q4'25 targets — the allocator's first-year allocation can over- or under-fund modules relative to their actual 2025 historical CapEx. **Recommended**: in Sprint 10, override 2025 module CapEx to historical actuals (R96 V2 BB launches 2,987, R97 V2 DTC 182, F9 manufactured 17.01) and let allocator drive 2026+ only. This preserves 2025 calibration while allowing allocator-driven dynamics in out-years.

### Sprint 11 — Valuation

**Scope**: Build Valuation tab per Architecture §14. Group DCF with 5-yr-smoothed terminal FCF + Gordon Growth. SoTP per-module DCF (per-module WACC = group + risk premium; per-module terminal). Multiples cross-check. Comparables anchors. Sensitivity table (5×5 grid: Starship $/kg learning rate × Starlink TAM inflation rate, plus auxiliary 1D sweeps on WACC / terminal g / capital pool growth). Static values via plugin recalc-and-paste.

**Inputs**: Sprint 9 (Group FCF). Sprint 10 (allocator-driven module FCFs).

**Outputs**: Group DCF EV. SoTP DCF total. Multiples-method total. Comparables vs anchor deltas. Sensitivity grid.

**Acceptance**: Group DCF EV in $500B - $1.5T range. SoTP DCF total within ±30% of Group DCF (per-module risk premia explain some divergence). Multiples-method total $5T-$9T (high — reflects 2050 saturated revenue × multiples). 2025 implied EV at 10× revenue multiple = $111B ±5%.

**Risk**: Iterative-calc bistability could make Group FCF read different values across recalcs (V28.1 had Valuation EV swing 4× across 6 recalcs). Live-aggregation helper rows on Valuation tab (read module FCFs directly via INDEX/MATCH bypass) per Spec 09 §4.1 architecture if needed.

### Sprint 12 — MC overlay + Pre-IPO outputs

**Scope**: MC ranges already populated on Assumptions tab from Sprint 0 (Principle 18). This sprint adds the MC ENGINE — sampling logic that draws from each input's distribution, recomputes, and outputs distribution of Group EV. Lightweight implementation (Excel-native triangle / lognormal / discrete sampling, or simple Python-based MC writing values back to Assumptions in a loop). Output: histogram + percentile table of Group EV. Pre-IPO deliverable: clean output extract (Group P&L summary table, Group EV with MC bands, sensitivity table, per-module breakdown).

**Inputs**: Sprint 11 (deterministic valuation engine live). Assumptions tab (MC range columns populated since Sprint 0).

**Outputs**: MC sampling produces ~5,000 trials. Group EV distribution: P10 / P50 / P90 / mean. Pre-IPO output package (CSV / chart-ready data / one-pager).

**Acceptance**: P50 Group EV within ±10% of deterministic baseline. P10 and P90 spans demonstrate model sensitivity to key inputs (Mars %, Starship learning rate, Starlink TAM inflation). No MC inputs missed (audit against Assumptions tab MC columns).

---

## §4 — Patch sprint pattern

Between numbered sprints, expect 1-3 patch sprints if calibration fails or sanity checks halt. Patch sprints use X.5 numbering (e.g., Sprint 4.5 if Starlink fails calibration). Patch sprints follow the same Rule Compliance Preamble + verification gate pattern as full sprints. Document the failure mode in the patch spec.

**Common patch scenarios**:
- Conservation break after a module sprint — trace through Group P&L conservation row that flags, repoint formula.
- Calibration miss — adjust a stub input or fix a unit conversion error.
- Iterative-calc non-convergence — break circularity with a prior-year reference somewhere.
- INDEX/MATCH not resolving — label mismatch between source and consumer; fix label.

---

# PART B — Verification Protocol

## §5 — Universal sprint completion criteria

Every sprint, regardless of which one, must pass this checklist before declaring complete. Plugin chats refuse to mark a sprint done if any item fails. Spec authors include this as the final §Verification section of every sprint spec.

### §5.1 No formula errors workbook-wide

```
Read every cell on every tab. Count occurrences of:
  #REF!  #VALUE!  #DIV/0!  #NAME?  #NUM!  #NULL!  #N/A

Expected: ZERO (except inside IFERROR-wrapped IRR helper cells, which are acceptable as long as they don't cascade to display rows).

Any error on a display row → halt, trace, fix before continuing.
```

### §5.2 Conservation block reads OK

```
Read Group P&L!D108:AC108 (the ALL OK boolean row) across all years.

Expected: every cell = "OK".

If any year reads "CHECK" → halt, trace, fix.

For the conservation block to populate (it only exists post-Sprint 9), this check kicks in from Sprint 9 onwards. Pre-Sprint-9 sprints verify trivially (e.g., "Allocator IN cells all read 0 → conservation trivially holds").
```

### §5.3 Edge-year reads (D / I / S / AC) at every verification gate

```
Per Principle 20 + Rule 16. Every read-back includes columns:
  D (2025)
  I (2030)
  S (2040)
  AC (2050)

Reading just one year hides edge-year bugs (pre-revenue divisions by zero, terminal-flow sign flips, horizon artifacts).
```

### §5.4 Round-trip stability

```
After all sprint writes complete:
  1. Recalc workbook 5 times (full rebuild).
  2. Capture values for key cells (Group EV, Group FCF 2030, Starlink revenue 2030, etc.).
  3. Compare across the 5 recalcs.

Expected: no key cell moves >$1M (or >0.1% for IRR/% cells) across recalcs.

If bistability detected (values cycle / drift), document the within-year circular dependency, accept if convergence target met, otherwise refactor to break circularity.
```

### §5.5 Stale-reference scan (Rule 22)

```
Per Principle 21. For every cross-tab reference on Valuation + Allocator + Group P&L:

  Identify the source cell (e.g., =Starlink!F210).
  Read the source cell's column-A label.
  Verify the consumer's labeled concept matches the source's label.

Expected: every cross-tab pull resolves to its source's labeled concept.

If any mismatch (e.g., "Blended IRR" pulling Forward IRR) → halt, trace, fix.
```

### §5.6 Sanity check halt thresholds

```
Per Principle 19 + Rule 15. Every sanity check in every spec has a quantitative halt threshold.

Common thresholds:
  - Starlink active sats < 50,000 throughout horizon (regulatory cap)
  - Starlink IRR not pinned at carry-forward 2040+ (terminal artifact)
  - Module FCF doesn't oscillate sign year-over-year > 3 times (bistability indicator)
  - Implied DTC subscribers < 15M in 2025 (anchored to Mach33 disclosed)
  - ODC fleet 2030 in 500-15,000 sat range (sanity)
  - Mars BV 2040 in $500B - $5T range (sanity)
  - Group FCF 2025 in $2B - $6B range (Q4'25 anchor ±tolerance)

Failure = halt and escalate to spec author + user. NEVER "proceed and document."
```

### §5.7 Claude Log entry

```
Single row appended to Claude Log tab. Columns: Date, Sprint number, Tabs touched, Summary (one paragraph), Outstanding (any deferred items), Next sprint.
```

---

## §6 — Sprint-specific calibration targets (2025 anchors from Q4'25)

Per Principle 23. Each sprint's verification reads its module's 2025 outputs and compares to these targets. Failure to hit = halt + retune.

### §6.1 Sprint 2 (Launch Capacity) calibration

| Output | 2025 target | Tolerance | Halt if |
|---|---|---|---|
| F9 total launches | 171 | ±5 | <160 or >185 |
| F9 fleet end-2025 | 39 | ±5 | <30 or >50 |
| F9 manufactured 2025 | 17 | ±2 | <13 or >22 |
| Starship launches | 0 | exact | any >0 |
| Total Starship capacity (kg) | ~450K | ±30% | <250K or >700K (depends on fleet build) |
| Blended $/kg | $400-$800 | range | outside |

### §6.2 Sprint 3 (Customer Launch) calibration

| Output | 2025 target | Tolerance | Halt if |
|---|---|---|---|
| F9 customer launches | 38.58 | ±2 | <30 or >50 |
| F9 customer revenue | $4,290mm | ±5% | <$3,800M or >$4,800M |
| F9 customer launch price | $111M | ±5% | <$95M or >$130M |
| Starship customer revenue | $0 | exact | any >0 |
| Per-launch Blended IRR | 8-25% | range | <0% or >50% |

### §6.3 Sprint 4 (Starlink + Starlink Capacity) calibration

| Output | 2025 target | Tolerance | Halt if |
|---|---|---|---|
| Starlink + DTC revenue | $7,852mm | ±5% | <$7,000M or >$8,700M |
| of which DTC | $157mm (≈2% of total) | ±15% | <$80M or >$250M |
| Starshield revenue | $2,520mm | ±5% | <$2,200M or >$2,900M |
| Active V2 BB sats end-2025 | 5,246 | exact | hardcoded baseline |
| Active V2 DTC sats end-2025 | 650 | exact | hardcoded baseline |
| V2 BB sats launched 2025 | 2,987 | exact | hardcoded baseline |
| V2 DTC sats launched 2025 | 182 | exact | hardcoded baseline |
| Total active sats end-2025 (incl. V1/V1.5 residual) | ~6,650-9,800 | wide | depends on V1/V1.5 inclusion convention |
| Implied BB ARPU | $100/mo | derived | check |
| Implied DTC ARPU | $16/mo | derived | check |
| Implied total Starlink subs end-2025 | 5.5-7.5M | range | <3M or >10M |
| V3 launches 2025 | 0 | exact | any >0 |
| Constellation D&A | $707mm | ±10% | <$600M or >$850M |
| Module EBITDA margin | 55-75% | range | <40% or >85% |

### §6.4 Sprint 5 (ODC) calibration

| Output | 2025 target | Tolerance | Halt if |
|---|---|---|---|
| ODC revenue | $0 | exact | any >$10M |
| ODC sats deployed 2025 | 0 | exact | any >5 |
| ODC fleet end-2025 | 0 | exact | any >5 |
| Per-sat marginal IRR 2025 | 0 or negative | n/a | reads positive (premature) |
| Bandwidth services cost paid to Starlink 2025 | $0 | exact | any >$10M |

ODC's 2025 target is essentially "no operations yet." Calibration kicks in for 2027+ output when ODC starts deploying.

### §6.5 Sprint 6 (AI Stack) calibration

| Output | 2025 target | Tolerance | Halt if |
|---|---|---|---|
| AI Stack revenue 2025 | 0 or small positive (Cursor early ramp) | <$500M | >$1B |
| Internal compute cost from ODC | $0 | exact | any >$10M (ODC pre-deployment) |

### §6.6 Sprint 7 (Lunar Mars) calibration

| Output | 2025 target | Tolerance | Halt if |
|---|---|---|---|
| Lunar Mars revenue | $0 | exact | any >0 |
| Mission CapEx 2025 | $0 | exact | any >$10M (pre-window) |
| Lunar BV accumulated 2025 | $0 | exact | any >$100M |
| Mars BV accumulated 2025 | $0 | exact | any >$100M |

Mars/Moon R&D ($700M 2025) flows through OpEx tab (Sprint 8), not Lunar Mars module.

### §6.7 Sprint 8 (OpEx + CapEx) calibration

| Output | 2025 target | Tolerance | Halt if |
|---|---|---|---|
| Starlink R&D | $830mm (8% × $10.37B Starlink+Starshield rev) | ±10% | <$650M or >$1.1B |
| Customer Launch R&D | $1,073mm (25% × $4.29B) | ±10% | <$800M or >$1.4B |
| ODC R&D | $200M (pre-revenue $-profile floor; locked 2026-05-20 — see Sprint 8 scope) | ±20% | <$120M or >$400M |
| AI Stack R&D | $50M (pre-revenue $-profile floor; locked 2026-05-20 — see Sprint 8 scope) | ±20% | <$30M or >$120M |
| Mars/Moon R&D 2025 | $700M | ±10% | <$500M or >$900M |
| Total R&D | ~$2,850M (Starlink $830M + Customer Launch $1,073M + ODC $200M floor + AI Stack $50M floor + Mars/Moon $700M; updated 2026-05-20 to reflect pre-revenue R&D fix) | ±10% | <$2,200M or >$3,400M |
| Total S&M | ~$586M (4% × $14.65B group) | ±15% | <$400M or >$800M |
| Total G&A | ~$733M (5% × group) | ±15% | <$500M or >$1B |
| Total CS | ~$157M (2% × $7.85B Starlink) | ±20% | <$100M or >$250M |
| Total OpEx | $3,820mm | ±5% | <$3,500M or >$4,200M |
| Total Group CapEx (incl. spectrum) | ~$7,030M (= $2,030M module + $5,000M spectrum) | ±10% | varies |
| Total Group D&A | ~$1,060M | ±10% | <$900M or >$1,300M |

### §6.8 Sprint 9 (Group P&L) calibration — THE BIG ONE (REVISED 2026-05-22)

**Sprint 9 amendment 2026-05-22**: targets REVISED per Vlad lock (AskUserQuestion 2026-05-22) + executed Sprint 9 PASS exact 2026-05-22 (V2.11). Q4'25 raw anchors retained as memo R122/R123 on Group P&L tab for archaeology only. Decomposition of rebuild-vs-Q4'25 gaps: (i) Module D&A inside COGS via vending-machine framing (Architecture §3 labeling note); (ii) fully-allocated launch transfer pricing flows vehicle D&A into consumers (~$1,200M COGS uplift); (iii) pre-revenue R&D floors ODC $200M + AI Stack $50M (Architecture §12.1 amendment 2026-05-20); (iv) EchoStar $5B treated as cash CapEx (Architecture §13.3); (v) Mars carve-out $1B treated as real cash drain (Vlad lock 2026-05-22 — `project-accounting-methodology-locks-2026-05-20` + `project-sprint-9-execution-status-2026-05-22`). Same architectural pattern as Sprint 8.5 OpEx target revision ($3,820M → $4,476M).

| Output | 2025 target (REVISED) | Tolerance | Halt if | Q4'25 original (archaeology) |
|---|---|---|---|---|
| Group Revenue | $14,650mm | ±5% | <$13,917M or >$15,382M | $14,650M (unchanged) |
| Group Gross Profit | $9,463M | ±10% | <$8,517M or >$10,409M | ~$10,830M |
| Group EBITDA | $4,904mm | ±5% | <$4,659M or >$5,149M | $8,690M |
| Group EBITDA Margin | 32.4% | ±3pp | <29.4% or >35.4% | 59.3% |
| Group D&A | $1,261M | ±10% | <$1,135M or >$1,387M | $1,060M |
| Group EBIT | ~$4,450M | derived ±$50M | check | ~$7,630M |
| Taxes (21%) | ~$934M | derived ±$50M | <$800M or >$1,050M | ~$1,600M |
| NOPAT | ~$3,516M | derived ±$50M | check | ~$6,030M |
| Total Group CapEx | $6,345M | ±5% (Sprint 8 anchor) | <$6,028M or >$6,663M | ~$7,030M (post-Sprint-10 with vehicle build) |
| Mars carve-out | $1,000M | exact (floor pre-Sprint-10) | non-$1,000M | n/a |
| **Group FCF** | **−$2,569M** | **±10%** | **<−$2,826M or >−$2,312M** | **$3,670M** |
| Conservation block ALL OK | "OK" every year | exact | any "CHECK" | unchanged (mandatory) |

If Sprint 9 misses any revised target → halt and trace through which input drifted. Most likely culprits: module R201/R202/R204/R205 drifted from Sprint 4/5/7 values; OpEx R53 changed post-Sprint-8.5; CapEx R45/R37/R41 changed; Customer Launch R70 internal transfer revenue drifted. Original Q4'25 anchors retained as memo rows R122/R123 on Group P&L tab for archaeology — NOT used as halt thresholds.

### §6.9 Sprint 10 (Allocator brain) calibration

| Output | Target | Notes |
|---|---|---|
| Cash BoY 2025 | $5,000mm | = starting cash, exact |
| Cash BoY 2027 | ~$15-25B | = $5B start + 2025 FCF + 2026 FCF + $30B IPO; depends on FCF chain |
| Year-N non-module claims 2025 | ~$5B (= OpEx $3.82B + Corp CapEx ~$0.1B + Spectrum $5B + Taxes $1.6B − some overlap) | sanity: not negative, not >Cash BoY |
| Available cash for IRR queue 2025 | likely 0 or small (claims > cash) | informational |
| Mars carve-out 2025 | $1B floor (no prior FCF) | exact at floor |
| Conservation post-allocator-light-up | "OK" | mandatory |

If 2025 Available Cash for Queue is 0 (claims exceed cash), modules get 0 allocation in 2025. **Override 2025 module CapEx to historical actuals** (V2 BB 2,987 launched, V2 DTC 182, F9 17 manufactured) so 2025 calibration holds; allocator drives 2026+ only. Document this override in the architecture spec as a "first-year override convention."

### §6.10 Sprint 11 (Valuation) calibration

| Output | 2025 target | Tolerance | Halt if |
|---|---|---|---|
| Implied EV 2025 (10× rev multiple) | $146.5B (= 10 × $14.65B) | ±5% | <$130B or >$170B |
| Group DCF EV | $500B - $1.5T | range | <$300B or >$3T |
| SoTP DCF total | within ±30% of Group DCF | range | beyond |
| Multiples-method total | $4T - $9T | range | <$2T or >$15T |
| Sensitivity grid center cell | matches baseline EV | within rounding | check |

### §6.11 Sprint 12 (MC + Pre-IPO outputs) calibration

| Output | Target | Notes |
|---|---|---|
| P50 Group EV from MC | within ±10% of Sprint 11 deterministic baseline | sanity |
| P10 / P90 spread | reflects key input variability | wide range expected |
| Output package | extracted, chart-ready | deliverable |

---

## §7 — Halt + escalation protocol

When any verification gate fails:

1. **Plugin chat halts.** No further writes in that sprint until resolved.
2. **Report the failure to the spec author (this chat)** with: which check failed, expected vs actual values, candidate causes.
3. **Spec author diagnoses.** Options: (a) trace through the failure, identify the bug, patch in-place; (b) revise the spec to address an architectural issue; (c) escalate to user if the failure reveals a deeper question.
4. **Resolved → resume sprint.** Or open a patch sprint (X.5 numbering) if the fix is structural.
5. **Document in Claude Log.** Both the failure and the resolution.

NEVER "proceed and document" without resolution. The 22M DTC subs failure in V26 (Principle 19 incident) is the cautionary tale.

---

## §8 — Sprint-spec template (for spec authors)

Every sprint spec opens with this skeleton:

```
# Sprint N — [Module name / scope]

**Source workbook**: V[N-1].xlsx
**Target workbook**: V[N].xlsx
**Day budget**: X days

## §0 — Constitutional references
- 01_Lessons_Learned.md (Principles X, Y, Z load-bearing for this sprint)
- 02_Architecture_and_Methodology.md §[applicable sections]
- Model Execution Rules.md (Rule Compliance Preamble below)

## §1 — Rule Compliance Preamble (mandatory)
[12-box checklist per Model Execution Rules]

## §2 — Framing
[Why this sprint, what it produces, dependencies]

## §3 — Patches (one section per discrete change)
[Per-patch: cells affected, current state, replacement, write pattern, verification gate]

## §4 — Verification (universal + sprint-specific)
[§5 universal checks + §6 sprint-specific calibration]

## §5 — Claude Log entry template

## §6 — Don't touch (out of scope)

## §7 — Open thread (post-sprint considerations)
```

---

## §9 — Amendment log

- **2026-05-19 (initial draft)** — Constitutional doc 3 of 4. 12 sprints, day budget 13-17 days including patches. Universal verification checklist + sprint-specific 2025 calibration targets from Q4'25. Sprint 10 first-year override convention noted for 2025 calibration preservation. To be amended as rebuild surfaces additional sprint dependencies.
- **2026-05-22 (Sprint 9 calibration target revision per Vlad lock)** — §6.8 Sprint 9 calibration table revised: Group Gross Profit $10,830M → $9,463M; Group EBITDA $8,690M → $4,904M (margin 59.3% → 32.4%); Group D&A $1,060M → $1,261M; Group EBIT ~$7,630M → ~$4,450M; Taxes ~$1,600M → ~$934M; NOPAT ~$6,030M → ~$3,516M; Total Group CapEx ~$7,030M → $6,345M (Sprint 8 anchor; $7,030M target holds post-Sprint-10 with vehicle build); **Group FCF $3,670M → −$2,569M ±10%**. Group Revenue $14,650M ±5% unchanged. Architectural decomposition documented in §6.8 amendment header: (i) Module D&A inside COGS via vending-machine framing; (ii) fully-allocated launch transfer pricing; (iii) pre-revenue R&D floors ODC $200M + AI Stack $50M; (iv) EchoStar $5B as cash CapEx; (v) Mars carve-out as real cash drain (Vlad lock 2026-05-22). Same architectural pattern as Sprint 8.5 OpEx target revision. Q4'25 raw anchors retained as memo rows R122/R123 on Group P&L tab for archaeology only — NOT used as halt thresholds. Sprint 9 executed PASS exact on all 5 revised targets 2026-05-22 (V2.11) — see `project-sprint-9-execution-status-2026-05-22`.
- **2026-05-20 (accounting methodology locks — Sprint 2 in flight)** — Amended Sprints 3, 4, 5, 8 with locked-this-sprint decisions surfaced during Sprint 1 post-mortem accounting review. Sprint 2 scope unchanged (already drafting in another chat). Sprint 3 inherits vehicle D&A fallback ownership (if Sprint 2 doesn't land canonical labels on Launch Capacity, Sprint 3 builds them on Customer Launch) + locks Module CapEx vs Capital deployed convention (equilibrium-equal except Starlink CapEx Lag). Sprint 4 + Sprint 5 lock fully-allocated at-cost pricing for bandwidth + compute respectively. Sprint 8 implements pre-revenue R&D switching formula `MAX($-profile, % × revenue)` for ODC + AI Stack, adds two new Assumptions $-profile year-rows, and adds AI Stack revenue to S&M base. §6.7 Sprint 8 calibration targets updated for new ODC R&D ($200M floor) + AI Stack R&D ($50M floor) + Total R&D (~$2,850M); §6.8 Group P&L EBITDA tolerance unchanged (the R&D bumps offset slightly against other lines).

---

## §10 — Sprint sizing convention (NEW 2026-05-26 after Sprint 11 execution lessons)

**Status**: Constitutional. Locked 2026-05-26 after Sprint 11 + Sprint 11b + Sprint 11c + Sprint 11d split chain demonstrated that combined-cleanup sprints exceeding ~5-7 §3 sections reliably hit Office.js context budget + calc engine session degradation.

### §10.1 Target sprint size

**Default target**: 3-5 §3 sections per sprint, single plugin chat from kickoff to PASS.

**Hard cap**: if a sprint specifies 7 or more §3 sections AND touches more than 4 tabs, MANDATORY split before execution:
- Split into N + N.5 (two sprints) or N.a + N.b (two blocks within N) — spec author's judgment
- Each block independently executable in a single plugin chat
- Vlad saves + reopens Excel between blocks (NOT just close window — fully quit Excel via Cmd+Q / File→Exit)
- Each block has its own kickoff prompt with: (a) prior block PASS state summary, (b) locked decisions from prior block, (c) explicit scope for this block

**Rationale**:
- Sprint 10 (10 §3 sections, mostly single-tab Allocator) — PASS in one chat
- Sprint 10.5 (5 §3 sections, ~3 tabs) — PASS clean
- Sprint 11 (13 §3 sections, 8 tabs) — required 4+ plugin chat attempts (11a, 11b/Block 2, 11c, 11d) due to context + calc engine issues
- The threshold is somewhere between 5-7 §3 sections AND 3-5 tabs

### §10.2 Assumptions write-then-reference protocol (LOAD-BEARING)

Per `feedback_assumptions_write_then_reference_footgun` memory: writing a new Assumptions tab row + immediately referencing it cross-tab in the same plugin chat reliably triggers calc engine session failure (Office.js corruption OR formulas-written-as-text). Sprint 11 Block 2 and Sprint 11c both fired this.

**Mandatory protocol** when a sprint adds new Assumptions row(s) AND cross-tab formulas reference them:

**Option A (RECOMMENDED for high-stakes writes)**:
1. Plugin Chat 1: write Assumptions row(s) ONLY. Pre-flight reads + verify B-col values after write.
2. Vlad saves + fully quits Excel + reopens.
3. Plugin Chat 2: write cross-tab formulas referencing the new Assumptions row(s). Pre-flight Probe 1 (formula text at first new row), Probe 2 (evaluated value), Probe 3 (sanity sweep).

**Option B (single chat, defensive)**:
1. Write Assumptions row(s) in one batch.
2. Force `worksheet.getItem("Assumptions").calculate()` followed by `context.sync()`.
3. **Mandatory probe**: write `=Assumptions!$B$[new_row]` to a scratch cell on another tab; sync; read value. If evaluates to the new value → calc engine is healthy. If returns 0 → HALT and switch to Option A.
4. Proceed with cross-tab formula writes.
5. Clean up scratch cell.

**Option C (Plugin-side fix if confirmed via Probe 1 in Option A continuation)**:
If post-reopen the Assumptions-referencing formula at the target cell shows TEXT not FORMULA, the prior plugin chat misused `set_cell_range` with `.values` API instead of `.formulas` API. Rewrite all affected cells using `.formulas` API explicitly.

### §10.3 Pre-flight calc engine sanity probe (mandatory for all sprints touching Assumptions)

Every plugin pre-flight from Sprint 12 onwards adds a calc-engine sanity probe BEFORE any writes:

```
Write `=Assumptions!$A$2` to a scratch cell on the Allocator tab (or any non-Assumptions tab).
Force calculate(full) + sync.
Read scratch cell value.
Expected: text matches Assumptions!A2 (a known cell with text content, e.g., "§1 GLOBAL").
If value is 0 OR empty string → calc engine corrupted from prior session. HALT and demand workbook reopen.
Clear scratch cell before proceeding.
```

This catches the calc engine session corruption before any writes can compound the issue.

### §10.4 Implications for Sprint 12 onwards

Per Sprint 11 lessons:

- **Sprint 12 (Valuation)** — large scope (per-vehicle DCF for Starlink × 4 + per-module DCF × 4 + SoTP + WACC + sensitivity + Football Field). Likely needs to split into Sprint 12a (DCF mechanics + WACC) + Sprint 12b (per-module DCF outputs + SoTP) + Sprint 12c (Football Field + sensitivity). Spec author scopes per §10.1.
- **Future combined-cleanup sprints** — if multiple §20-style amendments accumulate, lump them into one sprint NUMBER but split into blocks 11N.a / 11N.b / etc. as needed.
- **MC + Scenarios sprints** — large scope (every Assumptions input needs MC range; scenarios are thesis cuts). Likely Sprint 13a (MC input register) + Sprint 13b (MC engine) + Sprint 13c (Scenarios).

### §10.5 Process amendment summary (for future sprint chat kickoffs)

Every kickoff prompt from 2026-05-26 forward MUST include:
- Sprint sizing per §10.1 (target 3-5, max 7 §3 sections)
- Pre-flight calc engine sanity probe per §10.3
- If sprint touches Assumptions + cross-tab references, explicit Option A/B/C decision per §10.2
- Halt-at-section-boundary guidance for context budget management


- **2026-05-26 (Sprint 11 execution lessons — sprint sizing convention NEW §10)** — After Sprint 11 (13 §3 sections, 8 tabs) required four plugin chat attempts (11a, 11b/Block 2 partial, 11c §3.1.5 partial, 11d recovery) due to context budget exhaustion + Office.js calc engine session degradation (write-Assumptions-then-cross-tab-reference footgun fired twice), added §10 Sprint Sizing Convention. Target 3-5 §3 sections per sprint; hard cap 7 sections / 4 tabs above which split is mandatory. Mandatory pre-flight calc engine sanity probe (§10.3) catches session corruption before writes compound. Assumptions write-then-reference protocol (§10.2) provides three options for handling this pattern. Sprint 12 (Valuation) and Sprint 13 (MC + Scenarios) will be sized per these rules.
