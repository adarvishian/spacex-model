# Architecture & Methodology — Constitutional Document for SpaceX Model Rebuild v2

**Status**: Constitutional. Locked 2026-05-19.
**Authority**: Source of truth for the rebuild. Every sprint spec references this doc; every plugin write checks against it.
**Companion docs**: `01_Lessons_Learned.md` (the why), `Model Execution Rules.md` (the operational rules), `2025 Anchors from Q4_25.md` (the calibration targets), memories `project-rebuild-v2-status`, `project-anchored-assumptions-2025`, `project-rebuild-architecture`.

This doc combines structural design (what tabs exist, how they connect) and mathematical conventions (the formulas for IRR, sigmoid, conservation, terminal value). They are inseparable — every architectural choice implies a math convention.

---

## §0 — Preamble

**Reading order:** §1 (tab inventory) → §2 (year horizon) → §3 (module P&L convention) → §4 (Allocator contract) → §5 (IRR engine) → §6 (Allocator architecture) → §7 (internal transfers) → §8-11 (module-specific architecture) → §12-14 (Group / OpEx / CapEx / Valuation) → §15 (conservation) → §16 (cross-tab discipline) → §17 (calibration targets).

**Authority hierarchy:**
1. This doc (Architecture & Methodology) — locks structural and methodological decisions
2. `01_Lessons_Learned.md` — locks behavioral principles
3. `Model Execution Rules.md` — locks plugin-side operational discipline
4. Sprint specs — apply 1+2+3 to specific changes

A sprint spec cannot deviate from §§1-17 without first updating this doc.

**AI Stack resolution (key open question now closed):** AI Stack is a **standalone module** with its own tab and IRR engine. It receives compute from ODC via internal at-cost transfer (the Customer Launch ↔ consumer modules pattern) and sells AI products externally (Cursor seats, Grok subscriptions, Grok enterprise API). ODC has two output streams — external compute customers (real revenue) + internal compute to AI Stack (at-cost transfer, eliminated at Group). Justification in §10.

---

## §1 — Tab inventory (15 tabs, sheet order locked)

| # | Tab | Function | Owned by |
|---|---|---|---|
| 1 | Assumptions | Single source of truth for all inputs. 11 sections (Global, Allocator, Capacity, Customer Launch, Starlink, ODC, AI Stack, Moon/Mars, OpEx, CapEx, Valuation). Every input has cell ref, label, Base Case value, MC Min, MC Max, MC Distribution, Notes (per Principle 18). | Sprint 0 |
| 2 | Allocator | Cash pool tracker, queue gate, Mars carve-out, IRR-priority sigmoid blend (cash + kg queues), vehicle build claim, central IRR display. | Sprint 1 + Sprint 8 (skeleton vs brain) |
| 3 | Launch Capacity | Supply-side: Starship + F9 fleet, cadence (Wright's Law on cum upmass), payload, $/kg cost stack, total annual capacity in kg-to-LEO. **Not a P&L module.** | Customer Launch sprint |
| 4 | Customer Launch | Module: F9 + Starship external customer launches + at-cost internal launch transfer to consuming modules. Per-launch marginal IRR. | Customer Launch sprint |
| 5 | Starlink | Module: BB + DTC + Starshield revenue, constellation D&A, terminal COGS, spectrum amort, V2/V3 vehicle queue + ratchet. Per-vehicle marginal IRR. | Starlink sprint |
| 6 | Starlink Capacity | Aggregates Starlink constellation BB + DTC pools, allocates internal bandwidth claim to ODC, computes available bandwidth for external Starlink revenue. At-cost transfer pricing per pool. | Starlink sprint |
| 7 | ODC | Module: orbital compute satellites, dual revenue (Model A energy + Model B η with Pr(A) credence), per-sat marginal IRR, cash-driven deployment, internal compute to AI Stack + external to customers. | ODC sprint |
| 8 | AI Stack | Module: Cursor seats + Grok consumer + Grok enterprise API + (optionally Dojo terrestrial / Terrafab fab). Buys compute from ODC at-cost. Per-product marginal IRR or module-level IRR (TBD in AI Stack sprint based on product diversity). | AI Stack sprint |
| 9 | Lunar Mars | Module-but-not-in-IRR-queue: pre-revenue capital sink. BV engine (labour units + hardware) drives book value accumulation. Deployment driven by Mars/Moon strategic carve-out cash. | Lunar Mars sprint |
| 10 | Group P&L | Consolidated Revenue / EBITDA / D&A / EBIT / Taxes / NOPAT / CapEx / FCF. Inter-module elimination block. Corporate cost roll-up from OpEx + CapEx tabs. Conservation block (R99-R110 area). | Group P&L sprint |
| 11 | OpEx | Corporate operating costs only (vending-machine framing). R&D by module (start% / end% / CAGR per line), SG&A by function (S&M, G&A, CS), other corporate. | Group P&L sprint |
| 12 | CapEx | Module CapEx aggregation (read from modules) + Corporate CapEx (computed here: HQ, IT, engineering facilities) + Spectrum CapEx (EchoStar intangible). Corporate D&A computed here. | Group P&L sprint |
| 13 | Valuation | DCF off Group FCF (Gordon Growth terminal + smoothed 5-yr FCF), Sum-of-parts per module (per-module WACC + risk premium), Multiples cross-check, Comparables anchors, Sensitivity table. | Valuation sprint |
| 14 | Demand Curves | Bandwidth-driven Starlink revenue curve data (carried from V9). Read-only for Starlink revenue build. | Carried, no sprint changes |
| 15 | Claude Log | Running change log. One row per sprint. | Every sprint appends |

**Not in the workbook (deliberately):**
- Dashboard — deleted from V30.5; charts/scenarios consumed in Valuation tab or external doc
- ISM — cut 2026-05-12, never re-introduced
- Sub-tabs for individual AI Stack products (Cursor / Grok / etc.) — managed as sections within AI Stack tab

---

## §2 — Year horizon (locked D:AC = 2025-2050)

- **Year columns**: D through AC = 26 years × 2025 through 2050.
- **Year header row**: row 4 on every tab (D4 = 2025, E4 = 2026, ..., AC4 = 2050). Hardcoded integers.
- **Year-offset helper row** (Principle 13): row 5 on every tab with year columns. D5 = 0, E5 = 1, ..., AC5 = 25. Hardcoded integers, never recursive.
- Allocator tab and Starlink tab may use different year-header positions due to V9 inheritance — explicitly verified by Allocator + Starlink sprints; year-offset row aligns.

Every year-row formula uses anchor-and-offset (Principle 12): `$D$anchor × (1+rate)^E$5`. No prior-column recursion (Rule 23 exceptions for genuinely year-chained logic — cumulative sums, ratchet latches, EoY = BoY + adds — must be flagged inline in their sprint specs with one-line justification).

---

## §3 — Module P&L convention (vending machine)

Every module tab has structurally identical P&L:

```
ALLOCATOR IN BLOCK (top of tab)
    Capital Allocation ($mm)              ← from Allocator
    Starship Capacity Allocation (kg)     ← from Allocator
    Total Capital Available ($mm)         ← = sum

MODULE BODY (middle)
    Module-specific physical + economic build
    
P&L SECTION
    Revenue ($mm)                         ← summed from module-specific revenue lines
    
    COST OF GOODS SOLD ($mm)
        Constellation / fleet D&A          (direct production cost)
        Launch services cost              (internal at-cost transfer; eliminated at Group)
        Bandwidth services cost            (ODC-only; pays Starlink at-cost)
        Compute internal cost              (AI Stack-only; pays ODC at-cost)
        Ground ops % × revenue             (% rate from Assumptions)
        Spectrum amortization              (Starlink BB only; pulls from CapEx tab)
        Terminal COGS                     (Starlink only; net subscriber adds × $/terminal)
        Insurance % × revenue              (% rate)
        Other COGS % × revenue             (catch-all)
    Total COGS ($mm)                      ← SUM above
    
    Gross Profit ($mm)                    ← Revenue − Total COGS
    Module EBITDA ($mm)                   ← = Gross Profit (single canonical EBITDA — Principle 7)
    Module EBITDA Margin %                ← = Module EBITDA / Revenue
    
    CapEx ($mm)                            (cash outlay this year; physical assets only)
    Module FCF ($mm)                       ← = Module EBITDA + module D&A add-back − Module CapEx (pre-tax, pre-corp; tax applies only at Group)

ALLOCATOR OUT BLOCK (bottom of tab) — see §4
```

**Forbidden on any module tab (Principle 8):**
- R&D (any flavour) — lives on OpEx tab
- SG&A (S&M, G&A, customer service) — lives on OpEx tab
- Corporate overhead — doesn't exist anywhere (retired by Refine Spec 01)
- Taxes — Group P&L only
- Facilities D&A (HQ, IT, non-production) — CapEx tab
- Multiple flavors of EBITDA (True / after-overhead / etc.) — one canonical Module EBITDA = Gross Profit

**Mandatory:** Module EBITDA = Gross Profit. Module FCF is pre-tax, pre-corp-overhead. Per-sat / per-launch marginal IRR (§5) is computed on Module-level inputs (per-unit cost, per-unit net marginal revenue), not on fleet-level cash flows.

**Labeling note (added 2026-05-20):** The row labeled `Module EBITDA ($mm)` is mathematically Gross Profit (Revenue − COGS, where COGS includes fleet D&A and spectrum amort). It is not "EBITDA" in the traditional `Operating Income + D&A` sense — it's a contribution-margin variant where corporate OpEx (R&D, SG&A) is excluded entirely and module-level D&A is inside the COGS bucket. The Module FCF row then adds module D&A back to recover cash. The label `Module EBITDA` is kept (Principle 7 — no renames mid-build) but readers should understand the math. Conservation row R100 ("EBITDA check") and R103 ("D&A check") together ensure the framework stays consistent: Group EBITDA + Group D&A = Group Gross Profit + Σ module D&A, and Module FCF = Module EBITDA + Module D&A − Module CapEx with the D&A piece exactly equal to what was subtracted upstream.

---

## §4 — Allocator IN/OUT contract (canonical labels, by-label refs)

Every module's Allocator IN and Allocator OUT blocks use these canonical labels. Cross-tab pulls resolve by `INDEX(Module!D:D, MATCH("Label", Module!$A:$A, 0))` per Principle 14.

### §4.1 Allocator IN block (top of every module tab)

| Order | Canonical Label | Source |
|---|---|---|
| 1 | `INPUTS FROM CENTRAL ALLOCATOR` | section header |
| 2 | `Capital Allocation ($mm)` | `=INDEX(Allocator!D:D, MATCH("[module] cash allocation", Allocator!$A:$A, 0))` |
| 3 | `Starship Capacity Allocation (kg-to-LEO)` | `=INDEX(Allocator!D:D, MATCH("[module] kg allocation", Allocator!$A:$A, 0))` |
| 4 | `Total Capital Available ($mm)` | `= Capital Allocation` (no separate Cash Sweep row — Layer 3 sweep is killed; cash sweep functionality is subsumed by the cash pool tracker per §6) |

Lunar Mars's Allocator IN block has hardcoded zeros — Lunar Mars is outside the IRR queue. Its actual cash + kg arrive via the Mars carve-out off the top (§6.3).

### §4.2 Allocator OUT block (bottom of every module tab) — 11 canonical rows

| Order | Canonical Label | Computed from |
|---|---|---|
| 1 | `CENTRAL ALLOCATOR OUTPUTS` | section header |
| 2 | `Total Revenue ($mm)` | module Revenue total |
| 3 | `Module EBITDA ($mm)` | module Gross Profit |
| 4 | `Module EBITDA Margin %` | = Module EBITDA / Total Revenue (IFERROR for zero-revenue years) |
| 5 | `Module FCF ($mm)` | = Module EBITDA + module D&A add-back − Module CapEx (pre-tax, pre-corp) |
| 6 | `Module CapEx ($mm)` | module's annual physical CapEx — the **cash outlay** for new fleet/units this year. Feeds Group CapEx aggregation (CapEx tab §13.1) and Module FCF. |
| 7 | `Capital deployed ($mm)` | = actual deployment × unit cost — the **allocator-side accounting** of cash actually consumed by this module's deployment. In equilibrium equals Module CapEx (row 205). Divergence = allocation friction (allocator gave more than module could deploy, or less than module wanted). Diagnostic only — does NOT feed Group CapEx (Module CapEx does). |
| 8 | `Spot IRR` | per-sat / per-launch marginal IRR, current year — §5 |
| 9 | `Forward IRR (Y+2)` | per-sat / per-launch marginal IRR, year-D+2 cash flow stream |
| 10 | `Blended IRR` | = `(1 − w) × Spot + w × Forward`, w = 0.7 (Assumptions input) |
| 11 | `Capacity Demand (kg-to-LEO)` | module's uncapped kg demand (used for kg queue) |

**No Strategic Priority Weight row** (Principle 5). No Cash Sweep Contribution row (Layer 3 retired).

**Memo rows** below the canonical 11 may include fleet-level Spot/Forward/Blended IRR (per Spec 08 §4.2 pattern), other diagnostics. Memo rows are prefixed `Memo:` per Rule 17.

For Lunar Mars: canonical OUT is the same 11 rows but `Total Revenue = 0` (pre-revenue) and IRR rows = 0 (no IRR engine — strategic carve-out). Plus two extra rows below the contract: `Lunar Accumulated Book Value ($mm)` and `Mars Accumulated Book Value ($mm)` per Sprint 4 design.

For AI Stack: same 11 rows. Compute internal cost from ODC feeds into AI Stack COGS line; AI Stack revenue is external (Cursor + Grok + API). Capacity Demand = 0 (AI Stack doesn't consume Starship kg — see §10).

---

## §5 — Per-module IRR engine (per-sat / per-launch marginal IRR)

Per Principle 2. **Every module with deployable units uses this pattern. Day one. No fleet-level seeding, no NIC bases, no chicken-and-egg traps.**

### §5.1 The formula

For module M, year T:

```
CF stream (length N+1):
    t=0:  −cost_per_unit(T)                  (capex slug for one marginal unit)
    t=1:  net_marginal_revenue_per_unit(T+1)
    t=2:  net_marginal_revenue_per_unit(T+2)
    …
    t=N:  net_marginal_revenue_per_unit(T+N)

Spot IRR(T)       = IRR(CF stream evaluated at year T)
Forward IRR (Y+2) = IRR(CF stream evaluated at year T+2)
Blended IRR       = (1 − w) × Spot + w × Forward, w = 0.7 (Assumptions!Forward_weight)
```

In Excel:
```
Spot IRR cell:     =IFERROR(IRR(IF(_xlfn.SEQUENCE(1, N+1)=1, -cost_per_unit_D, net_rev_per_unit_D)), -1)
Forward IRR cell:  =IFERROR(IRR(IF(_xlfn.SEQUENCE(1, N+1)=1, -cost_per_unit_F, net_rev_per_unit_F)), -1)
Blended IRR cell:  =(1-Assumptions!Forward_weight)*Spot_IRR + Assumptions!Forward_weight*Forward_IRR
```

- `cost_per_unit` = sat unit cost + launch cost per sat (for sat modules); ship build cost (for Customer Launch); compute infrastructure per product unit (for AI Stack)
- `net_marginal_revenue_per_unit` = (per-unit revenue) − (per-unit marginal opex) − (per-unit internal transfer costs, e.g., bandwidth for ODC, compute for AI Stack)
- `N` = economic life. Default 5 years for sat modules. Customer Launch endogenous from cadence × lifetime reuses.

### §5.2 What goes in net_marginal_revenue_per_unit

Per Principle 8 (module COGS = direct production only):

| Module | net_marginal_revenue_per_sat/launch per year |
|---|---|
| Starlink (per vehicle: V2 BB, V2 DTC, V3 BB, V3 DTC) | = (per-sat revenue from bandwidth × $/Gbps × util) − (per-sat ground ops % × per-sat revenue) − (per-sat spectrum amort, BB only) − (per-sat insurance + other COGS %) |
| ODC (per sat) | = (Pr(A) × per-sat Model A revenue + Pr(B) × per-sat Model B revenue) − (per-sat SG&A% — wait, no, this is in OpEx tab not module — fix: per-sat ground ops % × per-sat revenue) − (per-sat bandwidth cost paid to Starlink) − (per-sat insurance + other COGS) |
| Customer Launch (per launch — external customer launches only) | = (Customer Launch external price per launch) − (variable cost per launch) − (D&A share per launch) − (insurance + other COGS per launch) |
| AI Stack (per product unit or per seat — TBD per AI Stack sprint) | = (per-unit revenue) − (per-unit compute cost paid to ODC at-cost) − (per-unit insurance + other COGS) |
| Lunar Mars | NO IRR engine (strategic carve-out) |

**Crucial:** corporate R&D, SG&A, taxes do NOT enter the per-unit IRR. They live at Group level. The per-unit IRR is the marginal-unit-economic return, not the fully-loaded after-corporate return.

### §5.3 Fleet-level IRR as memo only

A module-level (fleet-level) MFW-IRR may be retained as a Memo row beneath the canonical Allocator OUT for diagnostic purposes (per Sprint 8 §4.2 pattern). It does not feed the allocator. Label prefixed `Memo: Spot IRR (fleet-level, historical)` per Rule 17.

### §5.4 Cutoff: negative IRR → zero allocation

Modules / vehicles with `Blended IRR ≤ 0` receive zero cash and zero kg allocation. This is the strict IRR > 0 cutoff (Spec 09 §2.1). No floor-overrides, no strategic-weight back-doors.

---

## §6 — Allocator architecture

### §6.1 Cash pool tracker

Per Spec 06+07 architecture. Cash advances year-over-year via Group FCF (which already nets OpEx + Corp CapEx + Module CapEx + Taxes — no double-counting).

```
Allocator new section "CASH POOL TRACKER":

  Starting cash position EoY 2024 ($mm)     = Assumptions!Starting_cash      [$5,000mm anchored per Q4'25]
  IPO injection this year ($mm)              = IF(year = Assumptions!IPO_year, Assumptions!IPO_amount, 0)
                                                                            [$30,000mm in 2027]
  Prior-year Group FCF ($mm)                 = INDEX('Group P&L'!D:D, MATCH("GROUP FCF", 'Group P&L'!$A:$A, 0)) shifted prior year
  
  Cash BoY ($mm)                             = (prior year's Cash BoY) + (prior year's FCF) + (this year's IPO)
                                              (year-chained — Rule 23 exception, intentional)
```

Cash BoY year 2025 = Starting cash + IPO (if 2025) = $5,000mm + $0 = $5,000mm.
Cash BoY year 2027 = Cash BoY 2026 + Group FCF 2026 + $30,000mm IPO.

### §6.2 Queue gate (non-module claims)

Per Principle 4 (LOAD-BEARING). Reserve year-N's non-module cash needs before the IRR queue allocates.

```
Mars/Moon strategic carve-out ($mm)        = MAX(Assumptions!Mars_floor, prior-year Group FCF × Assumptions!Mars_pct)
                                              [floor $1,000mm; pct 15%]
                                              Uses prior-year FCF to break circularity (Principle 22).

Year-N non-module claims ($mm) =
    Total OpEx this year (from OpEx tab)
    + Corporate CapEx this year (from CapEx tab)
    + Spectrum CapEx this year (from CapEx tab)
    + Taxes this year (from Group P&L)
    + Mars/Moon strategic carve-out
                                              All non-module claims reserved BEFORE IRR queue.

Available cash for IRR queue ($mm)         = MAX(0, Cash BoY − Year-N non-module claims)
```

**Circularity note:** Year-N OpEx depends on year-N revenue, which depends on year-N CapEx, which depends on the IRR queue's allocation against `Available cash for IRR queue`. Iterative calc resolves; convergence target <10 iterations. The Mars carve-out uses prior-year FCF (not current-year) to weaken this loop.

### §6.3 IRR-priority sigmoid blend — cash queue

Per Spec 09 §2.4. Four (or five, if AI Stack standalone) modules compete: Customer Launch, Starlink, ODC, AI Stack. Lunar Mars is outside the queue.

```
For each module M:
    masked_demand_M  = IF(Blended_IRR_M > 0, cash_demand_M, 0)
    weight_M         = MAX(Blended_IRR_M, 0)^k                    (k = Assumptions!Sigmoid_k = 2)
    share_M          = weight_M / SUM_over_modules(weight_J)
    allocation_M     = MIN(masked_demand_M, Available_cash × share_M)
```

By construction `Σ shares ≤ 1` and `Σ allocations ≤ Available_cash`. No overflow. Negative-IRR modules: `weight = 0` → `share = 0` → `allocation = 0` (strict cutoff).

`cash_demand_M` is the module's uncapped cash ask (Starlink: large default per Spec 09 R494; ODC: per-sat CapEx × wanted deployment; AI Stack: per-product investment; Customer Launch: module CapEx for ground equipment + customer integration, NOT vehicle build which is at §6.5).

### §6.4 IRR-priority sigmoid blend — kg queue

Same architecture, same modules, same `k`, on Starship kg-to-LEO.

```
Total Starship capacity (kg)   = INDEX(Launch Capacity!D:D, MATCH("Total Annual Capacity (kg-to-LEO)", Launch Capacity!$A:$A, 0))
Lunar Mars reserved (kg)        = (Lunar slots + Mars slots derived from carve-out) × payload per ship × (1 + depot multiplier)
                                  This is reserved off the top before queue (per Sprint 4 / Principle architecture).
Capacity available for IRR queue = Total Starship capacity − Lunar Mars reserved

For each module M (same as cash queue):
    kg_masked_demand_M  = IF(Blended_IRR_M > 0, kg_demand_M, 0)
    kg_weight_M         = MAX(Blended_IRR_M, 0)^k
    kg_share_M          = kg_weight_M / Σ
    kg_allocation_M     = MIN(kg_masked_demand_M, Capacity_available × kg_share_M)
```

Same k for cash and kg queues. AI Stack's kg demand = 0 (terrestrial, doesn't consume Starship kg). Customer Launch's kg demand = external customer Starship kg only (NOT internal Starship launches consumed by Starlink/ODC — those are accounted for in the consuming modules' kg demand).

### §6.5 Module actual deployment

```
Actual deployment (units)   = MIN(
    cash_allocation_M / cost_per_unit_M,
    kg_allocation_M / mass_per_unit_M,
    internal_uncapped_demand_M
)
```

Downstream CapEx, Revenue, IRR all consume Actual deployment, not Demand. The MIN handles the case where any single resource binds.

### §6.6 Vehicle build cost claim — forward-aggregate-kg-demand-sized non-module claim

Per Spec 09 §2.7. Vehicle (Starship) build is **NOT** in Customer Launch CapEx. It is a non-module cash claim at the queue gate, sized by forward-aggregate kg demand across all consumers.

```
Forward aggregate kg demand (year T)  =
    INDEX(Starlink!D:D, MATCH("Capacity Demand (kg-to-LEO)", Starlink!$A:$A, 0)) at year (T + lead)
  + INDEX(ODC!D:D, MATCH("Capacity Demand (kg-to-LEO)", ODC!$A:$A, 0)) at year (T + lead)
  + INDEX(Customer Launch!D:D, MATCH("Capacity Demand (kg-to-LEO)", Customer Launch!$A:$A, 0)) at year (T + lead)
  + Lunar Mars kg reserved at year (T + lead)
                                       lead = Assumptions!Vehicle_build_lead_time = 2 yrs

Projected capacity (T + lead)         = Launch Capacity!D23 at year (T + lead)

Capacity gap (T)                      = MAX(0, forward_demand − projected_capacity)

Required vehicles (T)                  = capacity_gap / payload_per_launch / launches_per_vehicle_per_year
                                                                            (Assumptions: B500 = 24 launches/yr/vehicle)

Vehicle build claim (T) ($mm)          = required_vehicles × blended_build_cost_per_vehicle
                                                                            (= SH share × SH cost + ship share × ship cost; Assumptions!B501)
```

This claim feeds into Year-N non-module claims (§6.2). Customer Launch's allocator-OUT IRR isn't distorted by absorbing vehicle build cost it doesn't fully consume.

Vehicle D&A flows back to consumer modules via the at-cost internal launch transfer (§7.1) — so Starlink, ODC, Customer Launch (external share), AI Stack all absorb proportional vehicle D&A in their COGS. This preserves vending-machine framing.

**Vehicle D&A computation location (locked 2026-05-20):** Annual vehicle D&A is computed on the **Launch Capacity tab** (preferred owner — it already holds vehicle fleet CapEx, build rate, lifetime reuses, and per-vehicle cost stack). The Launch Capacity tab exposes two canonical year-row labels for consumers to read by INDEX/MATCH:

- `Annual vehicle D&A ($mm)` — total fleet D&A this year (= cumulative vehicle CapEx through year T / weighted-average useful life).
- `At-cost launch services rate ($mm/launch)` — = variable cost per launch + vehicle D&A allocated per launch (= annual vehicle D&A / total launches this year). This is the single per-launch at-cost rate charged to every consumer (Starlink, ODC, AI Stack, Customer Launch external).

If the Sprint 2 spec lands without these canonical rows, **Sprint 2.5 or Sprint 3 (Customer Launch)** takes the fallback: Customer Launch builds the vehicle D&A computation locally on its own tab and exposes the same two canonical labels there. Either home is acceptable; the labels stay the same so cross-tab references resolve via INDEX/MATCH regardless. Sprint 3's spec confirms the home before wiring Customer Launch's internal transfer revenue and COGS lines.

Vehicle CapEx is **NOT** in Customer Launch's Module CapEx (row 205) — it's the non-module cash claim sized at the queue gate. The Launch Capacity / Customer Launch at-cost rate then flows vehicle D&A back into consuming modules' COGS via Launch services cost. Vehicle D&A appears exactly once in Group D&A (via the consuming modules' COGS lines). Conservation row R103 (D&A check) catches double-counting; R105 (launch services elimination) catches mismatched rate × volume.

---

## §7 — Internal transfer mechanics (4-step pattern)

Per Principle 9 (gross at module IRR, eliminated at Group). Every internal flow follows:

1. **Source module** books internal transfer revenue (real cash inflow to source's P&L)
2. **Consuming module** books matching cost in COGS (real cash outflow from consumer's P&L)
3. **Group P&L elimination row** subtracts the flow once
4. **Conservation check row** verifies `Source internal rev = Σ Consuming module COGS for the flow`

### §7.1 Customer Launch ↔ consuming modules (launch services)

- **Internal transfer pricing (locked 2026-05-20 — fully-allocated)**: rate per launch = `variable cost per launch + vehicle D&A allocated per launch`. This is the same single blended rate charged to every consumer (Starlink, ODC, AI Stack, Customer Launch external). Computed on Launch Capacity (canonical label `At-cost launch services rate ($mm/launch)`); see §6.6. The "fully-allocated" choice means consumers absorb both the cash cost of operating a launch and the depreciation of the vehicle fleet — preserves vending-machine framing because vehicle D&A flows through to consuming modules' COGS, not Customer Launch's COGS.
- **Customer Launch P&L**: External revenue (commercial + government Starship customer launches) at market price + Internal transfer revenue (sum of internal launches consumed × at-cost rate).
- **Customer Launch IRR**: per-launch marginal IRR on external customer launches only. External economics; internal at-cost transfers don't contribute IRR signal.
- **Consuming modules' COGS line**: `Launch services cost ($mm) = (launches consumed by module) × (at-cost rate per launch)`.
- **Group P&L elimination**: `Internal launch services eliminated = − SUM of Launch services cost across consuming modules`. Equals Customer Launch internal transfer revenue (conservation).

### §7.2 ODC ↔ Starlink (bandwidth)

Per Refine Spec 04 architecture. ODC compute satellites have no ground downlink — all inference traffic routes via Starlink BB + DTC pools.

- **Bandwidth claim derivation**: ODC compute energy delivered (GWh/yr) × Gbps/(GWh/yr) conversion factor (Assumptions!B458, placeholder pending research). Split between BB (Assumptions!B459 = 50% PLACEHOLDER) and DTC pools.
- **At-cost transfer pricing per pool (locked 2026-05-20 — fully-allocated)**: `$/Gbps/yr = (pool cost basis) / (total active pool Gbps)`. BB cost basis = Gbps-share-weighted Constellation D&A + Ground ops + Spectrum amort (BB-only). DTC cost basis = same minus Spectrum (DTC uses MSS bands, no analogous intangible). "Fully-allocated" lock means the at-cost rate covers both cash COGS (ground ops, insurance share, other COGS) and non-cash D&A + spectrum amort — symmetric with launch services pricing (§7.1) and compute pricing (§7.3). The pool cost basis SUMS all Starlink BB COGS on its tab, divides by total active BB Gbps, then ODC pays its Gbps-share × that rate. Conservation row R106 catches any pricing mismatch.
- **Starlink internal bandwidth revenue**: `(ODC BB claim × BB rate) + (ODC DTC claim × DTC rate)`. Booked as new revenue line on Starlink.
- **ODC COGS line**: `Bandwidth services cost ($mm) = same total`. Booked as COGS.
- **Group P&L elimination**: `Internal bandwidth eliminated = − ODC bandwidth services cost`.
- **Capacity allocation**: Starlink's remaining available bandwidth (post-internal-claim) drives external Starlink BB/DTC revenue. Starlink Capacity tab handles the aggregation and split.

### §7.3 ODC ↔ AI Stack (internal compute)

New mechanism. ODC produces compute output (PFLOPS, tokens). Some sold externally to compute customers; some transferred internally to AI Stack at-cost.

- **At-cost transfer pricing (locked 2026-05-20 — fully-allocated)**: per-PFLOP-hr rate = (ODC fully-allocated annual cost) / (ODC total annual PFLOP-hrs produced). Fully-allocated cost = annual sat D&A + annual launch services cost paid to Launch Capacity + annual bandwidth services cost paid to Starlink + insurance + other COGS. Charged to AI Stack at this fully-allocated rate (not pure marginal cash cost — keeps vending-machine framing intact because ODC's D&A flows out via internal transfer revenue and into AI Stack's COGS, where it's eliminated at Group). The "per-sat marginal cost" language in earlier drafts is superseded: the at-cost rate is fully-allocated cost per PFLOP-hr, symmetric with §7.1 (launch services) and §7.2 (bandwidth).
- **Internal split (Assumptions input)**: `% of ODC compute output transferred to AI Stack internally` vs `% sold to external customers`. Year-row. Starts at high internal share (AI Stack is the anchor consumer); external share grows as external compute market matures.
- **ODC's two revenue streams**:
  - External revenue = `external compute share × Fleet PFLOPS × external $/PFLOP-hr`
  - Internal transfer revenue = `internal share × Fleet PFLOPS × marginal cost per PFLOP-hr`
- **AI Stack COGS line**: `Internal compute cost from ODC ($mm)` = same as ODC's internal transfer revenue.
- **Group P&L elimination**: `Internal compute eliminated = − AI Stack internal compute cost`. Equals ODC internal transfer revenue.

ODC's per-sat IRR reads off **external revenue only** (parallel to Customer Launch reading IRR off external launches only). Internal transfers don't contribute to ODC IRR signal. This keeps ODC's IRR a clean "should we build one more sat for external revenue" signal.

---

## §8 — Starlink architecture

### §8.1 V2 / V3 vehicle pools

Per Spec 09 §2.6. Two pools at the within-Starlink level (different markets, not interchangeable):

- **BB pool**: V2 Mini BB + V3 BB compete. Pool cash = Starlink cash × BB market share (Assumptions!R39 = 0.85). Pool kg = Starlink kg × R39.
- **DTC pool**: V2 Mini DTC + V3 DTC compete. Pool cash = Starlink cash × DTC market share (R40 = 0.15). Pool kg = Starlink kg × R40.

Within each pool, IRR-priority sigmoid blend (same k=2):
```
For each vehicle V in pool:
    V_share = (eligibility × MAX(IRR_V, 0)^k) / Σ
    V_cash  = pool_cash × V_share
    V_kg    = pool_kg × V_share
Actual sats deployed for vehicle V = MIN(V_cash / cost_per_sat, V_kg / mass_per_sat)
```

### §8.2 V2 → V3 ratchet (single flag, irreversible)

Per Spec 09 §2.8. Once any V3 sat (BB or DTC) deploys in any year, BOTH V2 lines (BB and DTC) shut down permanently.

```
R238 (ratchet flag, year-row):
    D238: =IF(OR(V3 BB launched > 0, V3 DTC launched > 0), 1, 0)
    E238: =IF(OR(D238 = 1, E V3 BB > 0, E V3 DTC > 0), 1, 0)
    F238:AC238: copy E238 across (year-chained latch — Rule 23 exception)

V2 BB eligibility = IF(AND(V2 BB IRR > 0, R238 = 0), 1, 0)
V2 DTC eligibility = IF(AND(V2 DTC IRR > 0, R238 = 0), 1, 0)
V3 BB / V3 DTC eligibility = IF(V3 IRR > 0, 1, 0)
```

### §8.3 V2 historical fleet retirement

Per Spec 09 §2.9. Historical 2024-end fleet (V2 BB 5,246 + V2 DTC 650) retires linearly over useful life N = 5 years.

```
R54 (V2 BB opening-balance deorbit):
    D54: =IF(year - 2025 < useful_life, Assumptions!V2_BB_historical / useful_life, 0)
    Year-row pattern same.
R61 (V2 DTC same).

Active V2 BB fleet = Historical baseline + cumulative V2 BB launched − cumulative V2 BB deorbit (in-horizon) − cumulative V2 BB opening-balance deorbit
```

By 2030 (5 years out from 2025), V2 historical fleet fully retired.

### §8.4 Starlink revenue (bandwidth-driven, derived subs)

Per Refine Spec 03 §4. Starlink revenue is bandwidth-driven (Gbps × $/Gbps from Demand Curves), not sub-driven. Subscribers are **derived** from revenue ÷ ARPU:

```
Broadband subscribers EoY (millions) = BB Revenue / BB ARPU
DTC subscribers EoY (millions) = DTC Revenue / DTC ARPU
Total Starlink subs EoY = sum
Net subscriber adds = year-over-year delta

Hardware Revenue (Terminals) = Net adds × blended retail price per terminal
Terminal COGS = Net adds × terminal COGS per unit
```

ARPU year-rows from Assumptions: BB $100/mo 2025 → $75/mo 2030, flat; DTC $16/mo 2025 → $10/mo 2030, flat.

### §8.5 Starlink Capacity tab (bandwidth aggregation)

Per Refine Spec 04. Separate tab handles the aggregation of constellation capacity, internal bandwidth claim to ODC, and at-cost transfer pricing. Starlink revenue rows repoint to read "Available BB Gbps" and "Available DTC Gbps" from this tab.

---

## §9 — ODC architecture

### §9.1 Cash-driven deployment (NOT stub year-row)

Per Q4'25 architecture + Vlad lock 2026-05-19. ODC has NO fixed deployment year-row. ODC reads `Cash Demand ($mm) = wanted_deployment × cost_per_sat` and competes in the outer IRR queue. Actual deployment = MIN(cash allocated / cost-per-sat, kg allocated / mass-per-sat).

Wanted deployment in early years (pre-IRR-positive) = 0. As Pr(A) × Model A + Pr(B) × Model B yields positive net marginal revenue per sat, IRR rises, queue allocates cash, deployment ramps.

### §9.2 Dual revenue model (Sprint 3.5)

Per Sprint 3.5 architecture. Two parallel revenue models, credence-weighted:

- **Model A (energy-anchored)**: `Revenue = Fleet_GW × Adjusted_CoreWeave_baseline × PUE_uplift × Util_factor`. CoreWeave 2026 anchor $12B/GW_IT/yr; orbital PUE 1.12 vs terrestrial 1.4.
- **Model B (η-anchored)**: `Revenue = Billable H100-equiv GPU-hrs × $/GPU-hr`, where billable hrs = `(η / F_ref) × util × ECR × 8760 × Fleet_GW`.

**Expected Revenue** = `Pr(A) × Model A + (1−Pr(A)) × Model B`. Pr(A) credence default 0.6 (Assumptions!Pr_A = 0.6).

### §9.3 External + internal compute split

Per §7.3. ODC produces total compute output; splits between external customers (real revenue) and AI Stack (at-cost internal transfer). Year-row split input on Assumptions.

ODC per-sat IRR reads off external revenue only (Principle 9 + §7.3 design).

### §9.4 Per-sat marginal IRR engine

Per Spec 08 Patch P. Engine structurally identical to Starlink V3 BB pattern (Spec 09 Patch M):

```
Per-sat Model A revenue / year = (compute_power / chip_TDP) × chip_FP8 / 1e6 × 8760 × util × ECR × price_per_GPU_hr / 1e6
Per-sat Model B revenue / year = (compute_power / 1e6) × CoreWeave_baseline_year × PUE_uplift × util_factor × 1000
Per-sat combined revenue / year = Pr(A) × A + (1−Pr(A)) × B
Per-sat marginal opex / year = combined revenue × (ground_ops% + insurance% + other%)
Per-sat bandwidth cost / year = (per-sat BB Gbps + DTC Gbps) × respective $/Gbps from Starlink Capacity
Per-sat net marginal revenue / year = combined revenue − opex − bandwidth

Cost per sat ($mm) = sat unit cost (subsystems + chips with WL) + launch cost per sat / 1e6

Spot IRR = IFERROR(IRR(IF(SEQUENCE(1, N+1)=1, −cost_per_sat, net_marginal_revenue)), −1)
N = 5 (Assumptions!ODC_design_life)
```

---

## §10 — AI Stack architecture (STANDALONE module)

**Resolution of the standalone-vs-rolled question:** AI Stack is **standalone**. Own tab, own IRR engine, own Allocator OUT contract. Receives compute from ODC via at-cost internal transfer (§7.3). Sells AI products externally.

**Justification:** AI Stack's product economics (Cursor seats × subscription ARPU; Grok consumer subs × ARPU; Grok enterprise API tokens × $/Mtoken) are structurally different from ODC's compute economics ($/GPU-hr × util × Fleet_GW). Putting them on the same module tab loses signal — a single IRR engine can't cleanly represent both a compute-supply business and a product-packaging business. Customer Launch's pattern (internal vs external launches on one module) works because both are launches at different prices. ODC + AI Stack are different products entirely. Keep separated.

### §10.1 AI Stack revenue structure

Three product lines (initial; expandable per AI Stack sprint):
- **Cursor (orchestration)**: subscription seats × $/seat/month. Year-row seat growth, monthly ARPU stub.
- **Grok consumer (Premium subscriptions)**: subs × $/sub/year. Rides X platform monetization.
- **Grok enterprise (API tokens)**: token volume × $/Mtoken. Year-row volume growth + token price deflation.

Additional product lines (Dojo terrestrial / Terrafab fab) may be added in AI Stack sprint if they're load-bearing for thesis. Each follows same pattern: volume × price.

### §10.2 AI Stack COGS

- Internal compute cost from ODC (§7.3) — biggest line, at-cost transfer
- Any direct product COGS (e.g., Cursor inference cost — though most inference cost is in the ODC compute charge already)
- Insurance + other COGS catch-all

NO R&D / SG&A / Tax on AI Stack tab. R&D for AI Stack lives on OpEx tab (own section: R&D — AI Stack). SG&A is corporate-allocated (S&M, G&A, CS) on OpEx tab.

### §10.3 AI Stack IRR engine

**Per-product marginal IRR** (TBD in AI Stack sprint — could be one composite engine or three product-specific engines).

Initial approach: one composite per-Cursor-seat-equivalent IRR if products have comparable unit economics. If not, three separate per-product IRRs feeding a blended module IRR. Resolve in AI Stack sprint.

### §10.4 AI Stack outside Layer 2 (kg queue)

AI Stack consumes ODC compute, not Starship kg. Its Capacity Demand row = 0. Per `project-ai-stack-no-launch-demand` memory.

In the outer cash queue, AI Stack competes for cash with Customer Launch, Starlink, ODC. Its IRR signal is the per-product marginal IRR.

---

## §11 — Lunar Mars architecture (strategic carve-out, NOT in IRR queue)

**Framing note (added 2026-05-20):** Lunar Mars intentionally diverges from vending-machine framing. Three structural differences:

1. **Pre-revenue throughout horizon** (Revenue = 0 every year 2025–2050). Module EBITDA = negative operating costs. Per-mission IRR engine deferred (Vlad lock 2026-05-19).
2. **BV is the load-bearing measure**, not cash flow. The accumulated book value engine (§11.4) builds up an off-balance-sheet asset from labour productivity + hardware mass landed. BV grows independently of cash CapEx — labour productivity learning compounds BV while cash CapEx tracks carve-out spend. The Valuation tab terminal anchor (§14.2) is `1.5 × Lunar+Mars BV at 2050`, so BV is what drives valuation.
3. **Cash CapEx ≠ BV depreciation in COGS**. Lunar Mars Module CapEx (row 205) = annual carve-out cash deployed. Module COGS includes mission ops (% of CapEx) + BV depreciation (= BV / capital_lifetime). In years where BV grows faster than CapEx (labour productivity learning compounding), BV depreciation in COGS exceeds cash CapEx for the year. That's the intended accounting — defensible, just unusual. Conservation row R102 (FCF check) and R103 (D&A check) treat Lunar Mars symmetrically with other modules; the BV-vs-cash divergence shows up as a wider Module FCF deficit, not a conservation failure.

The two BV memo rows on the Allocator OUT block (rows 211–212) are diagnostic outputs the Valuation tab reads by label. Lunar Mars receives kg via off-the-top reservation (§6.4 + §11.3); does not compete in the IRR queue.


### §11.1 Strategic carve-out — cash before IRR queue

Per Spec 06+07 architecture + Vlad lock 2026-05-19.

```
Mars/Moon strategic carve-out ($mm, year-row)  = MAX(Assumptions!Mars_floor, prior-year Group FCF × Assumptions!Mars_pct)
                                                  Uses prior-year FCF (breaks circularity).
                                                  **Mars_pct is MC-variable (Base Case 15%, wide range — central uncertainty on how much
                                                  Musk allocates to Mars vs terrestrial IRR-positive lines).** Floor also MC-variable.
```

This cash deducted from Cash BoY before the IRR queue runs (§6.2). Funds Lunar Mars module physical CapEx for the year.

### §11.2 Deployment driven by carve-out cash

```
Per-ship cost (Lunar) = Starship vehicle cost amortized × (1 + Lunar depot multiplier)
                       + payload value (labour units + hardware) per Lunar ship

Lunar ships deployed (year) = (Lunar share of carve-out cash) / per-ship cost
Mars ships deployed (year)   = (Mars share of carve-out cash) / per-ship cost (with Mars 5x depot)
```

Lunar/Mars share of carve-out: continuous Lunar (year-round) + window-bound Mars (every 26 months). Configurable Assumptions input — `Lunar share of carve-out cash`, `Mars share of carve-out cash`, year-row (sums to 100% per year).

**No exogenous slot year-rows.** R287/R288 in V30.5 (Lunar slots / Mars slots dedicated per year) get DROPPED as inputs. Derived from carve-out cash + per-ship cost.

### §11.3 Kg reservation off-the-top

Lunar/Mars kg reserved off-top from Starship total before kg queue runs. Per Sprint 4.

```
Lunar Mars kg reserved (year)  = (Lunar ships + Mars ships) × Starship LEO payload × (1 + depot multiplier average)
                                  (Sprint 4 design: full LEO payload × all flights including depot/refueling)

Capacity available for kg queue = Total Starship capacity − Lunar Mars kg reserved
```

### §11.4 BV engine (labour units + hardware) — kept from Sprint 4 / Q4'25

Per Vlad lock 2026-05-19. Methodology unchanged from Q4'25 Mars & Moon engine, Sprint 4 port.

```
Surface-landed Starships (year) = ships deployed / (1 + depot multiplier)
Surface payload (kg)             = surface_starships × payload_per_surface_ship
Labour units landed              = surface_payload × labour_share / labour_unit_mass
Hardware mass landed (kg)         = surface_payload × (1 − labour_share)

Active labour fleet (running sum, net of retirements at lifespan)
Annual production output ($mm)    = active_labour_fleet × labour_annual_output × productivity_learning
Annual hardware value add ($mm)   = hardware_mass_landed × hardware_$/kg

Annual book value contribution    = production_output + hardware_value_add
Accumulated book value (year)     = contribution(year) + prior_year_BV × (1 − 1/capital_lifetime)
                                    capital_lifetime = 10 yrs (Assumptions!R263)
```

Labour unit parameters (Assumptions §R268-R274): mass 60 kg, base hourly output $22/0.7 burdened, daily working hours 22, productivity factor 1.0, productivity learning 5%/yr, useful life 5 yrs.

### §11.5 Lunar Mars P&L

- Revenue = 0
- COGS = mission ops (% of CapEx) + BV depreciation per year
- Gross Profit = Module EBITDA = negative (operating costs only)
- CapEx = total mission spend per year (= carve-out cash deployed)
- FCF = heavily negative (CapEx dominates, no offsetting revenue)

### §11.6 Allocator OUT for Lunar Mars

Standard 11-row contract with IRR rows = 0 (no IRR engine). Plus 2 extra memo rows for diagnostic BV: `Lunar Accumulated Book Value ($mm)`, `Mars Accumulated Book Value ($mm)`.

**Per-mission marginal IRR deferred** — Vlad: "we can change this later." Not in rebuild scope.

---

## §12 — OpEx tab (corporate operating costs)

Per Refine Spec 03 architecture. Tab between Group P&L and CapEx.

### §12.1 R&D by module (start-bound CAGR per line)

Each module has 3 inputs (start %, end-state %, CAGR taper) feeding a year-row formula using anchor-and-offset:

```
For module M:
    D14_M (anchor)  = Assumptions!start%_M
    E14_M           = IF(CAGR >= 0,
                          MIN(end_%, $D$14_M × (1+CAGR)^E$5),
                          MAX(end_%, $D$14_M × (1+CAGR)^E$5))
    F14:AC14_M      = copy E14_M across
    $ value         = % × module revenue
```

| Module | Start % | End % | CAGR | Base |
|---|---|---|---|---|
| Starlink | 8% | 3% | −10%/yr | Starlink + Starshield rev |
| Launch (Customer Launch) | 25% | 4% | −20%/yr | Customer Launch external rev |
| ODC | 30% | 8% | −15%/yr | ODC rev (post-revenue years; see note below) |
| AI Stack | 15% | 5% | −10%/yr | AI Stack rev (post-revenue years; see note below) |
| Moon/Mars | year-row $-profile (D=$700M anchored, ramping per spec) | n/a | n/a | $-profile (pre-revenue) |

R&D — Moon/Mars uses a year-row $-profile (pre-revenue; not % of rev). 2025 anchor $700M from Q4'25.

**Pre-revenue R&D fix (locked 2026-05-20, Sprint 8 implements):** ODC R&D = 30% × ODC revenue gives $0 in 2025–2027 because ODC is pre-revenue by design. AI Stack has the same problem in its early-ramp years. But both physically have heavy R&D spend pre-revenue (ODC: sat dev, chip roadmap, ground network; AI Stack: Cursor + Grok product engineering). Convention: each module's R&D row uses a **switching formula** — `R&D_t = MAX($-profile_t, % × revenue_t)` per year, where the $-profile year-row covers pre-revenue years and the % × revenue formula takes over once revenue × % exceeds the $-profile floor. Assumptions tab gets two new $-profile year-rows: `ODC R&D $-profile ($mm/yr)` and `AI Stack R&D $-profile ($mm/yr)`. Initial Base Case stub trajectories to be Vlad-locked in Sprint 8 prep (suggested anchors: ODC $200M 2025 → $500M 2027 declining as % × rev takes over; AI Stack $50M 2025 → $300M 2028 declining similarly). Sprint 8 spec lands the formula + the two new Assumptions rows as a Sprint 0.5-style append (no row insertions, append below existing Assumptions rows; INDEX/MATCH by label keeps downstream references stable).

### §12.2 SG&A by function

| Function | Start % | End % | CAGR | Base |
|---|---|---|---|---|
| Sales & Marketing | 4% | 2% | −8%/yr | Starlink + Starshield + Customer Launch ext rev + **AI Stack rev** (added 2026-05-20 — AI Stack is a consumer product line with real marketing spend) |
| General & Admin | 5% | 6% | +1%/yr | Group rev net of elim |
| Customer Service | 2% flat | — | — | Starlink subscription rev (BB + DTC) |
| Other corporate operating | 1% flat | — | — | Group rev |

Total OpEx = sum of R&D lines + SG&A lines + other.

**AI Stack S&M (added 2026-05-20):** AI Stack revenue (Cursor seats + Grok consumer + Grok enterprise API) added to the S&M base. Cursor + Grok consumer have real go-to-market spend; Grok enterprise API has sales-team spend. Sprint 8 implements via the same `4% start → 2% end, −8%/yr` glide path applied to the expanded base. ODC revenue intentionally excluded from S&M base (B2B compute customers, low marketing intensity); Lunar Mars excluded (pre-revenue, R&D-only).

---

## §13 — CapEx tab (corporate + module aggregation)

Per Refine Spec 02 + Spec 03 §5.

### §13.1 Module CapEx aggregation (read from modules)

```
Customer Launch CapEx     = INDEX(Customer Launch!D:D, MATCH("Module CapEx", ...))   (excludes vehicle build per §6.6)
Starlink CapEx            = INDEX(Starlink!D:D, MATCH("Module CapEx", ...))
ODC CapEx                 = INDEX(ODC!D:D, MATCH("Module CapEx", ...))
AI Stack CapEx            = INDEX(AI Stack!D:D, MATCH("Module CapEx", ...))
Lunar Mars CapEx          = INDEX(Lunar Mars!D:D, MATCH("Module CapEx", ...))
Total Module CapEx        = SUM
```

### §13.2 Corporate CapEx (computed here)

Inputs from Assumptions (R393-R401): HQ buildings $50M/yr, Corporate IT $30M/yr, General engineering facilities $20M/yr, Other $10M/yr. Useful lives: HQ 30y, IT 7y, Gen eng 20y, Other 20y.

```
Total Corporate CapEx = SUM of inputs
Corporate D&A         = cumulative_CapEx_to_date / useful_life (straight-line per line)
```

### §13.3 Spectrum CapEx (EchoStar)

Per Refine Spec 03 §5. EchoStar mid-band intangible.

```
Year-row EchoStar CapEx (Assumptions!R452): 2025 $5B, 2026 $8B, 2027 $5B, 2028 $2B, 2029+ $0 (total $20B)
Useful life (R453) = 15 yrs

Cumulative spectrum intangible = running sum
Annual spectrum amortization   = cumulative_intangible / 15
                               → flows to Starlink COGS as Spectrum amortization line (BB only)
                               → contributes to Group D&A add-back in FCF calc
```

### §13.4 Total Group CapEx + Group D&A

```
Total Group CapEx = Total Module CapEx + Total Corporate CapEx + Annual Spectrum CapEx + Vehicle build claim
Total Group D&A   = Module D&A (in module COGS already) + Corporate D&A + (Spectrum amort is in Starlink COGS already)

The D&A add-back at FCF: add back module D&A + corporate D&A + spectrum amort (all non-cash; CapEx is the cash outflow)
```

---

## §14 — Valuation tab

Per Refine Spec 09 architecture.

### §14.1 Group DCF

```
WACC_group = Assumptions!Group_WACC = 0.10
g = Assumptions!Terminal_growth = 0.025

Live Group FCF (year) = INDEX('Group P&L'!D:D, MATCH("GROUP FCF", 'Group P&L'!$A:$A, 0)) per year
                       [bypass stale-cache via direct module FCF aggregation if Group P&L caching is bistable]

Discount factor (year) = 1 / (1 + WACC_group)^(year − 2025)
PV of FCF (year)        = FCF × Discount factor

Smoothed terminal FCF   = AVERAGE(FCF, last 5 yrs pre-2050)
Terminal value @ 2050    = smoothed × (1+g) / (WACC − g)
PV of Terminal           = Terminal / (1+WACC)^25

EV (raw)                 = SUM PV of FCF + PV of Terminal
EV (clamped)             = SUM MAX(0, PV of FCF) + PV of Terminal  [memo for cliff value-at-risk]
```

### §14.2 Sum-of-parts DCF (per module)

Each module gets standalone DCF:
- Risk-adjusted WACC: `Group_WACC + module_risk_premium` (premia per Spec 09: Starlink 0bps, Launch 100bps, ODC 200bps, AI Stack 300bps, Lunar Mars 500bps)
- Terminal: Gordon Growth for Starlink/Launch/ODC/AI Stack; BV-anchored (1.5× book value) for Lunar Mars

### §14.3 SoTP Multiples cross-check

Per-module revenue × multiple (Assumptions): Starlink 10×, ODC 6×, Launch 5×, AI Stack 5×, Lunar Mars $50B anchor.

### §14.4 Comparables anchors

Group EV (Morgan Stanley) $350B, Brant internal $2.5T (memo only — do not quote), Starlink standalone (Bernstein/JPM) $150B, ODC (CoreWeave-anchored) $50B, Launch (Rocket Lab) $40B, Lunar Mars (NASA HLS) $50B.

### §14.5 Sensitivity table

5×5 primary grid: Starship $/kg learning rate × Starlink TAM inflation rate. Plus 1D auxiliary sweeps on WACC, terminal g, capital pool growth. Static values, regenerated post-Spec.

---

## §15 — Group P&L walk + conservation block

### §15.1 The walk

```
Group Revenue (net of eliminations) = SUM(module revenues) − inter-module eliminations
−    Group COGS (sum of module COGS, net of elim)
=    Group Gross Profit

−    Total OpEx (from OpEx tab)
=    Group EBITDA (pre-D&A, pre-tax)
−    Corporate D&A (CapEx tab; spectrum amort is inside Starlink COGS so don't double-count)
=    Group EBIT
−    Taxes (= max(0, Group EBIT) × tax_rate)
=    NOPAT

+    Total D&A add-back (module D&A in COGS + corporate D&A; spectrum already in Starlink COGS = part of module D&A bucket)
−    Total Group CapEx (Module CapEx + Corporate CapEx + Spectrum CapEx + Vehicle build claim)
=    GROUP FCF
```

### §15.2 Conservation block (Group P&L R99-R110 area)

Every check reads 0 within ±$1M tolerance:

| Row | Check | Formula |
|---|---|---|
| R99 | Revenue check | = Total Revenue − Σ module revenues + Σ eliminations |
| R100 | EBITDA check | = Total EBITDA − Σ module EBITDAs |
| R101 | CapEx check | = Total Module CapEx − Σ module CapEx rows |
| R102 | FCF check | = Total Module FCF − Σ module FCF rows |
| R103 | D&A check | = Group D&A − (Σ module D&A in COGS + Corporate D&A) |
| R104 | EBIT consistency | = Group EBIT − (Group EBITDA − Group D&A) |
| R105 | Launch services elimination conservation | = Customer Launch internal transfer rev − Σ consuming modules' Launch services cost |
| R106 | Bandwidth elimination conservation | = Starlink internal bandwidth rev − ODC bandwidth services cost |
| R107 | Compute elimination conservation | = ODC internal transfer rev − AI Stack internal compute cost |
| R108 | ALL OK boolean | = AND(ABS(R99:R107) < 1) → "OK" / "CHECK" |
| R109 | Cash flow identity | = Starting cash + Σ IPO + Σ Group FCF − Σ deployed CapEx − Σ strategic carve-out − Cash EoY (final year) |

R108 = "OK" required for any sprint to declare complete (per Principle 19 + Rule 5).

---

## §16 — Cross-tab discipline + formula patterns

Per Principles 11-14. Summarized for reference:

- **All cross-tab references**: `INDEX(Tab!D:D, MATCH("Canonical Label", Tab!$A:$A, 0))`. Zero hardcoded `=Tab!Dxx` row references.
- **Year-row formulas**: anchor-and-offset. `$D$anchor × (1+rate)^E$5`. No prior-column recursion (Rule 23 exceptions for genuinely year-chained logic only).
- **Year-offset helper row**: D5 = 0, E5 = 1, ..., AC5 = 25 on every tab with year columns.
- **Dynamic ranges**: `INDEX(range, 1) : INDEX(range, N+1)`. Zero OFFSET formulas.
- **No row insertions in cross-referenced tabs** (Rule 10). Append below existing data instead.

---

## §17 — 2025 calibration targets (locked from Q4'25)

Per `project-anchored-assumptions-2025` memory + `2025 Anchors from Q4_25.md`. Every module sprint's verification reads its module's 2025 contribution and compares to target. Group P&L sprint verification reads consolidated 2025 outputs and compares to the full target set.

| Output | 2025 target | Tolerance |
|---|---|---|
| Group Revenue | $14,650mm | ±5% |
| Starlink + DTC revenue | $7,852mm | ±5% |
| of which DTC | $156.91mm (= 2% of total) | ±10% |
| Starshield revenue | $2,520mm | ±5% |
| Customer Launch revenue | $4,290mm (F9 customer) | ±5% |
| ODC revenue | $0 | exact |
| AI Stack revenue | $0 | exact |
| Lunar Mars revenue | $0 | exact |
| Group EBITDA | $8,690mm (59.3% margin) | ±5% |
| Group D&A | $1,060mm | ±10% |
| Group EBIT | (= EBITDA − D&A) | (calculated) |
| Taxes | (= max(0, EBIT) × 21%) | (calculated) |
| Group FCF | $3,670mm | ±5% |
| Total OpEx | $3,820mm | ±5% |
| Total CapEx | ~$2,030mm | ±10% |
| F9 launches (total) | 171 | ±5 |
| of which F9 customer | 38.58 | ±2 |
| Starship launches | 0 | exact |
| Active sats end-2025 | ~9,800 | ±5% |
| Implied EV (10× rev) | $111B | ±5% |
| Starting cash | $5,000mm | exact (locked input) |

Failure to hit any of these in 2025 triggers retune. The model must reproduce 2025 history before extrapolating to 2050.

---

## §18 — Open items to resolve during build

These are architectural questions that don't block Sprint 0 but need resolution before the relevant module sprint:

1. **AI Stack per-product IRR vs blended module IRR** — resolve in AI Stack sprint based on product diversity. Default: blended module IRR.
2. **Bandwidth Gbps/GWh conversion + BB/DTC split** — V30.5 R458 = 0.05, R459 = 0.50 are placeholders. Calibrate when ODC sprint runs or accept as MC-wide.
3. **ODC internal vs external compute share trajectory** — year-row split input. Anchor: high internal share early (AI Stack is anchor consumer), external share grows as compute-as-a-service market matures. Stub TBD in ODC sprint.
4. **Lunar/Mars Lunar-vs-Mars share of carve-out** — year-row split. Lunar continuous, Mars window-bound (every 26 months). Stub TBD in Lunar Mars sprint.
5. **Demand Curves tab — load-bearing?** Carries Starlink bandwidth demand from V9. If still load-bearing, retain. If superseded by sub-derivation in Starlink sprint, drop.

**Resolved 2026-05-20 (5 items previously open):**

6. ~~Vehicle D&A computation location~~ — **LOCKED** §6.6: Launch Capacity owns by preference; Sprint 3 (Customer Launch) is the fallback owner. Canonical labels `Annual vehicle D&A ($mm)` + `At-cost launch services rate ($mm/launch)`.
7. ~~Capital deployed vs Module CapEx semantics~~ — **LOCKED** §4.2: Module CapEx (row 205) = cash outlay feeding Group CapEx; Capital deployed (row 206) = allocator-side diagnostic, equilibrium-equal to row 205.
8. ~~At-cost transfer pricing methodology (launch services, bandwidth, compute)~~ — **LOCKED** §7.1, §7.2, §7.3: fully-allocated cost across all three flows.
9. ~~Pre-revenue R&D for ODC + AI Stack~~ — **LOCKED** §12.1: switching formula `MAX($-profile_t, % × revenue_t)`; two new Assumptions $-profile year-rows added in Sprint 8.
10. ~~AI Stack S&M base~~ — **LOCKED** §12.2: AI Stack rev added to S&M base.

---

## §19 — Amendment log

- **2026-05-19 (initial draft)** — Constitutional doc locked. 19 sections, ~1,200 lines. Combines structural design + math conventions. AI Stack resolved as standalone module. Lunar Mars deferred to strategic carve-out (no IRR engine). 2025 calibration targets locked from Q4'25. To be amended only when an architectural decision changes; amendments require updating the related memory entry.
- **2026-05-20 (accounting methodology locks — Sprint 2 in flight)** — Surfaced five load-bearing gaps during Sprint 1 post-mortem accounting review. Resolved without touching Sprint 2 scope: (1) Vehicle D&A computation location — Launch Capacity owns by preference; Sprint 3 (Customer Launch) is fallback owner via canonical labels `Annual vehicle D&A ($mm)` + `At-cost launch services rate ($mm/launch)` (§6.6). (2) Module CapEx vs Capital deployed — Module CapEx (row 205) = cash outlay feeding Group CapEx; Capital deployed (row 206) = allocator-side diagnostic (§4.2). (3) At-cost transfer pricing — fully-allocated across all three internal flows: launch services (§7.1), bandwidth (§7.2), compute (§7.3). (4) Pre-revenue R&D for ODC + AI Stack — switching formula `MAX($-profile_t, % × revenue_t)`; two new Assumptions $-profile year-rows added in Sprint 8 (§12.1). (5) AI Stack S&M — AI Stack revenue added to S&M base (§12.2). Plus documentation notes: §3 clarifies `Module EBITDA` labeling (math = Gross Profit, label retained per Principle 7); §11 documents Lunar Mars's intentional divergence from vending-machine framing (BV-driven, not cash-driven). §18 open-items list updated — five items moved from open to resolved.

---

## §20 — Sprint 11 amendments (2026-05-26 — combined sprint)

This section captures the load-bearing architectural amendments introduced by Sprint 11 (the "combined cleanup sprint" absorbing former Sprint 10.7 vehicle-level allocator + Sprint 10.7+ Launch Capacity endogenous fleet wiring + Sprint 10.8 D&A audit + Sprint 10.9 ODC audit). Each subsection explicitly supersedes the relevant earlier section's stated convention.

### §20.1 Allocator IN/OUT contract — vehicle-level for Starlink (supersedes §4.1 for Starlink module)

Starlink module has 4 vehicles (V2 BB, V2 DTC, V3 BB, V3 DTC) as top-level allocator queue entries. Per-vehicle Blended IRR (computed at Starlink R215/R220/R225/R230 memo rows post-Sprint-10.5 demand curves) feeds the cash + kg sigmoid queues directly. Other modules (Customer Launch, ODC, AI Stack, Lunar Mars) remain module-level.

**Starlink Allocator IN block (R7-R14):**

| Row | Canonical Label | Source |
|---|---|---|
| R7 | `INPUTS FROM CENTRAL ALLOCATOR` | section header |
| R8 | `Starlink V2 BB cash allocation ($mm)` | `=INDEX(Allocator!D:D, MATCH("Starlink V2 BB cash allocation", Allocator!$A:$A, 0))` |
| R9 | `Starlink V2 DTC cash allocation ($mm)` | same pattern |
| R10 | `Starlink V3 BB cash allocation ($mm)` | same pattern |
| R11 | `Starlink V3 DTC cash allocation ($mm)` | same pattern |
| R12 | `Starlink V3 BB kg allocation (kg-to-LEO)` | same pattern (Starship kg) |
| R13 | `Starlink V3 DTC kg allocation (kg-to-LEO)` | same pattern |
| R14 | `Total Capital Available ($mm)` | `=D8+D9+D10+D11` (sum of 4 vehicle cash allocations) |

V2 vehicles (V2 BB, V2 DTC) have **NO kg allocation row** — they fly on Falcon 9, not Starship. F9 supply is a separate constraint applied in deployment formulas (§20.3).

**Starlink Module-level Allocator OUT (R201-R210)** stays as rollup of per-vehicle outputs for Group P&L compatibility. Per-vehicle Allocator OUT rows (R215/R220/R225/R230 IRR memos + per-vehicle CapEx R88-R95) supply the granular data the allocator queues read.

**Six new canonical labels published on Allocator tab:**
1. `Starlink V2 BB cash allocation`
2. `Starlink V2 DTC cash allocation`
3. `Starlink V3 BB cash allocation`
4. `Starlink V3 DTC cash allocation`
5. `Starlink V3 BB kg allocation`
6. `Starlink V3 DTC kg allocation`

Existing canonical label `Starlink cash allocation` becomes the SUM rollup `=R88+R89+R90+R91` (preserves backward compat; Group P&L still reads module-level if needed).

### §20.2 Cash + kg sigmoid queues — per-vehicle for Starlink (supersedes §6.3, §6.4 for Starlink)

**Cash queue (Allocator §4)** expands from 4 sub-blocks (CL + SL + ODC + AIS) to **7 sub-blocks**: CL + Starlink V2 BB + Starlink V2 DTC + Starlink V3 BB + Starlink V3 DTC + ODC + AI Stack. Lunar Mars stays OUTSIDE the queue (strategic carve-out per §11).

For each Starlink vehicle sub-block:
```
Blended IRR_V       = INDEX(Starlink!D:D, MATCH("Memo: <V> Blended IRR", Starlink!$A:$A, 0))  (R215/R220/R225/R230)
cash_demand_V       = (gate_V) × (Starlink R88 + R89  for V2 BB; R90 + R91 for V2 DTC; R92 + R93 for V3 BB; R94 + R95 for V3 DTC)
weight_V            = MAX(IRR_V, 0)^k × IF(demand_V > 0, 1, 0)         (k = Assumptions!Sigmoid_k = 2)
share_V             = weight_V / Σ weights (across all 7 sub-blocks)
allocation_V        = MIN(IF(IRR_V > 0, demand_V, 0), Available cash × share_V)
```

**Three physical gates** (`gate_V`):
- **V3 startup gate** (V3 BB, V3 DTC): `IF(year >= Launch Capacity!R56 V3 Starlink launch trigger year, 1, 0)`. Pre-trigger (year < 2027): V3 demand = 0; sigmoid skips V3. Post-trigger: V3 demand resolves to real values.
- **V2 phase-out gate** (V2 BB, V2 DTC): `IF(year < Assumptions!V2 phase-out year, 1, 0)`. Pre-phase-out (year < 2028): V2 demand resolves normally. Post-phase-out (year >= 2028): V2 demand = 0; V2 line production assumed shut down.
- **F9 supply gate** (V2 BB, V2 DTC): applied at deployment formula (§20.3) — V2 deployment binds on F9 launches available, not in the sigmoid weight stage.

**Kg queue (Allocator §6)** has 5 sub-blocks: CL external Starship + Starlink V3 BB + Starlink V3 DTC + ODC + AI Stack (kg demand structural 0). V2 vehicles do NOT appear in the kg queue — they consume F9, not Starship.

For each V3 Starlink kg sub-block:
```
kg_demand_V         = gate_V (V3 startup) × INDEX(Starlink!D:D, MATCH("<V> Starship kg demand", Starlink!$A:$A, 0))  (R49 V3 BB or R50 V3 DTC)
kg_weight_V         = MAX(IRR_V, 0)^k × IF(kg_demand_V > 0, 1, 0)
kg_share_V          = kg_weight_V / Σ kg_weights
kg_allocation_V     = MIN(IF(IRR_V > 0, kg_demand_V, 0), Capacity_available × kg_share_V)
```

Lunar Mars kg reserved off-the-top before queue (per §11.3, unchanged).

### §20.3 Module deployment binding mandatory (supersedes §6.5 — strengthens "design intent" to "wiring requirement")

**Prior §6.5 said module deployment = MIN(cash/cost, kg/mass, internal_demand) but this was design intent, not wiring requirement. Sprint 10 + 10.5 module tabs did not implement; modules deployed via internal logic regardless of Allocator IN values, making the allocator advisory not binding. Sprint 11 makes this a mandatory wiring requirement for every IRR-positive module.**

**Starlink — per-vehicle deployment formulas (R33, R37, R39, R41):**

```
R33 V2 BB launches per year = IF(year >= V2 phase-out year, 0,
                                 IF(year = 2025,
                                    INDEX(Assumptions!B, MATCH("V2 Mini BB Sats Launched 2025", ..., 0)),  [first-year override]
                                    MIN(
                                      D8 V2 BB cash / R78 V2 BB sat unit cost,
                                      F9_launches_available × Assumptions!Sats per F9 launch — V2 BB,
                                      internal_uncapped_demand
                                    )
                                 )
                              )

R37 V2 DTC launches per year — same template, V2 DTC reads

R39 V3 BB launches per year = IF(year < V3 trigger year, 0,
                                 MIN(
                                   D10 V3 BB cash / R80 V3 BB sat unit cost,
                                   D12 V3 BB kg / Assumptions!V3 Mass (kg),
                                   internal_uncapped_demand
                                 )
                              )

R41 V3 DTC launches per year — same template, V3 DTC reads
```

`F9_launches_available` = Launch Capacity!R64 F9 launches per year − Customer Launch!R25 F9 customer launches per year (= F9 internal capacity available to Starlink V2 vehicles).

`internal_uncapped_demand` = Sprint 4's existing per-vehicle ramp formula if it exists (E33:AC33), else first-year anchor flat (D33 historical value).

**Non-Starlink modules — module CapEx formulas (R205) bind on Allocator IN R8:**

```
Customer Launch R205 Module CapEx = IF(year = 2025, historical anchor,
                                       MIN(R8 cash / per-unit cost, internal_demand) × per-unit cost)
ODC R205                          = same template
AI Stack R205                     = same template (Sprint 6 deferred — stays 0 until AI Stack module ships)
Lunar Mars R205                   = unchanged (binds on carve-out cash R35 directly)
```

**Conservation effect**: With deployment-binding live, Σ Module CapEx across modules should equal Σ Module cash allocations (within rounding for unit-cost arithmetic). The "$293B unallocated cash by 2050" pathology resolves once modules can deploy MORE when cash is available (V3 BB at high IRR absorbs cash as fast as its kg constraint allows).

### §20.4 Launch Capacity endogenous fleet wiring (NEW — supersedes §6.6 prior "claim only" framing)

**Prior §6.6 said Vehicle build claim is a non-module cash claim at queue gate. It sized the CASH claim correctly but did not wire the claim into endogenous Starship fleet build. The downstream consequence: Launch Capacity R34 Total Annual Capacity (kg-to-LEO) = 0 throughout horizon → V3 kg constraint binds at 0 → V3 deployment = 0 even post-trigger → Starlink 2028+ revenue collapses. Sprint 11 wires the cash claim into fleet build.**

**Starship fleet build (Launch Capacity tab):**

```
R8 Super Heavy manufacturing cost ($mm/unit)        — replicate D-col value across E:AC OR apply Wright's Law decay (Assumptions R14 currently 0)
R9 Starship 2nd-stage manufacturing cost ($mm/unit) — same
Blended cost per Starship vehicle                    = R8 + R9 (year-row)

R25 Boosters built per year (units, NEW endogenous formula) =
    IFERROR(
      INDEX(Allocator!$D:$AC, MATCH("Vehicle build claim ($mm)", Allocator!$A:$A, 0), D$5+1)
      / (R8 + R9),
      0
    )

R24/R27 fleet BoY/EoY chain unchanged (BoY = prior EoY; EoY = BoY + R25 built − R26 retired)
R33 Total Starship launches per year = R27 fleet × R23 launches per Starship vehicle per year
R34 Total Annual Capacity (kg-to-LEO) = R33 × R29 per-launch upmass
```

**F9 fleet build (Launch Capacity R55, R57, R61):**

```
R61 F9 manufactured per year (units, was hardcoded =17) becomes endogenous:
    R61 = IF(year < V3 trigger year, R55 F9 base build rate,
             R55 × MAX(0, 1 − (year − V3 trigger year) / R57 F9 build-rate decay window))
```

Pre-trigger: F9 build at base rate (8/yr per Assumptions R57). Post-trigger: linear decay over R57 = 8 years to zero (F9 production winds down as Starship takes over).

**Effect on Sprint 10 R150 vehicle build claim**: with R8/R9 replicated across years (or WL-decayed), R150 D-col $50M correctly sizes; E:AC also correctly sizes once forward demand exists. Sprint 10 carry-forward bug (R150 = $50M D-col only, $0 E:AC) resolves.

### §20.5 Lunar Mars BV engine — SoTP terminal value INPUT, NOT P&L D&A flow (CORRECTS §11.4 + §11.5)

**Prior §11.4 + §11.5 specified Lunar Mars BV depreciation in COGS, treating accumulated book value as capital subject to D&A depreciation. Sprint 7 implemented this; Sprint 9 routed `BV depreciation — Lunar` + `BV depreciation — Mars` into Group P&L R28 Group D&A formula. By 2050 this produced $478B/yr phantom D&A — accumulated BV ($5.6T Lunar+Mars total) depreciating at 10%/yr.**

**Correction**: BV is a **SoTP terminal value driver**, not a P&L D&A flow. The BV engine measures economic value of Lunar/Mars labour fleet + hardware accumulated on the surface — it is the basis for the Valuation tab's terminal anchor (§14.2 `1.5 × Lunar+Mars BV at 2050`). It is NOT a depreciation schedule that should flow through Group P&L.

**Concrete changes:**

1. **§11.4 retained** — BV accumulation formula unchanged. Lunar/Mars accumulated BV continues to be computed as labour productivity × hardware value × capital_lifetime decay. This output stays for Valuation tab consumption.

2. **§11.5 amended** — Lunar Mars Module COGS = mission ops only (% of CapEx). **BV depreciation REMOVED from COGS.** Lunar Mars P&L:
   - Revenue = 0
   - COGS = mission ops only (no BV depreciation)
   - Module D&A = proper depreciation of cumulative Lunar Mars Module CapEx (= cumulative carve-out cash deployed / Lunar Mars capital lifetime). This is the real cash-capital depreciation, not the BV-engine output.
   - Gross Profit = Module EBITDA = −(mission ops)
   - CapEx = annual carve-out cash deployed
   - FCF = Module EBITDA − Module CapEx (heavily negative, as before)

3. **§15 / §13.4 R28 Group D&A formula corrected**: REMOVE the two INDEX/MATCH reads for `BV depreciation — Lunar` and `BV depreciation — Mars`. Replace with a single read of `Lunar Mars Module D&A ($mm)` (the new proper cash-capital depreciation per §11.5 amendment above).

4. **`BV depreciation — Lunar` and `BV depreciation — Mars` rows** on Lunar Mars tab are RETAINED for Valuation tab terminal anchor calculation but FLAGGED in their column-A labels as `Memo: BV decay — Lunar (Valuation input only, NOT in Group D&A)`.

**Effect on Group P&L 2050:**
- Group D&A: $484B → ~$5.7B + proper LM Module D&A (likely ~$200-500M depending on cumulative LM CapEx) → total ~$6-6.5B
- Group EBITDA: unchanged at −$44.5B (LM BV wasn't in COGS; this is a separate AC_2050 EBITDA issue tied to OpEx-vs-revenue ratio in late years; surfaces post-correction)
- Group FCF 2050: was +$337B; recomputes as roughly EBITDA − Taxes (=0) + D&A − CapEx = −$44.5B + $6B − $52B = roughly −$90B. **MASSIVE swing** from +$337B to deeply negative. This is the correct answer; the +$337B was illusory FCF from D&A add-back of phantom BV depreciation.

This correction will cascade to Sprint 9 §6.8 calibration revision (Group FCF 2050 anchor changes dramatically).

### §20.6 V2 / V3 ratchet flag retired (supersedes §8.2)

**Prior §8.2 specified a single ratchet flag (R238 on Starlink tab, but in V2.13 it's R43) that once tripped permanently shuts down V2 BB and V2 DTC. This was a hardcoded latch; Sprint 10.7 analysis identified it as obsolete once vehicle-level allocator + 3 physical gates land.**

**Replacement**: The V2/V3 transition emerges from:
- V3 startup gate (§20.2) — V3 launches start at trigger year (Launch Capacity R56 = 2027)
- V2 phase-out gate (§20.2) — V2 production ends at V2 phase-out year (Assumptions, new MC input, Base Case 2028)
- Sigmoid IRR weighting — V3 BB IRR much higher than V2 BB (2.08 vs 0.53 in 2025; widens over time), so sigmoid concentrates cash on V3 even between trigger year and phase-out year

**Concrete changes:**
- Starlink R43 (V2/V3 ratchet flag) → cleared to 0; col A label appended with retirement note.
- Assumptions R320 (V2 DTC permanent cap flag) → cleared to 0; col A label retirement note.
- §8.2 superseded by §20.2 (sigmoid + gates).
- §8.1 vehicle pools framing simplified — V2 BB / V2 DTC / V3 BB / V3 DTC compete in unified cash sigmoid (no separate BB / DTC pool intra-Starlink); kg sigmoid for V3 only.

### §20.7 Customer Launch Capacity Demand — externalized for vehicle build claim (clarifies §6.6)

Per Sprint 10 spec, vehicle build claim sums forward kg demand across all consumers including Customer Launch. CL R210 Capacity Demand (kg-to-LEO) currently = 0 across all years because CL external Starship business isn't sized in the module. Sprint 11 amendment: Customer Launch R210 should reflect external customer Starship kg demand (= Customer Launch R24 Starship customer launches × per-launch upmass). If CL R24 is empty/zero, R210 stays 0 — but the canonical label resolves so vehicle build claim sums correctly.

### §20.8 ODC unit economics — model verdict accepted (clarifies §9)

**ODC per-sat IRR is negative throughout horizon (Spot IRR -0.39 in 2025, -0.07 in 2030, -0.15 in 2050).** Vlad lock 2026-05-26: this is **model verdict, not bug**. ODC's per-sat economics — per-sat revenue ~$0.5M/yr × 5-year life vs per-sat cost ~$3-5M (solar $1.25M + thermal $1.44M + chip cost) — produce negative IRR. The allocator correctly refuses to allocate cash to ODC. ODC stays at zero deployment unless either (a) ODC per-sat revenue assumption is revised upward (e.g., Mach33 ODC thesis — higher compute revenue per PFLOP); or (b) ODC strategic carve-out is added (Architecture §11 amendment to make ODC a strategic carve-out like Lunar Mars).

**Sprint 11 accepts (a) as deferred decision** — Vlad may revise Assumptions per-sat revenue inputs OR per-sat cost inputs in a Sprint 11.5 unit-economics pass. The architectural mechanism (allocator masks negative-IRR modules to zero allocation) is correct.

---

- **2026-05-26 (Sprint 11 combined cleanup — vehicle-level allocator + deployment binding + endogenous fleet wiring + LM BV correction)** — Eight load-bearing amendments combined into a single sprint. Captured as new §20 (Sprint 11 amendments block). Key changes: (1) §4.1 Allocator IN block — Starlink module has 4 vehicle-level cash + 2 vehicle-level kg reads, replacing single module-level entry. (2) §6.3 cash sigmoid expanded from 4 to 7 sub-blocks (CL + 4 SL vehicles + ODC + AIS). (3) §6.4 kg sigmoid restructured — V2 vehicles NOT in kg queue (fly on F9 not Starship); V3 vehicles in queue. (4) §6.5 deployment binding upgraded from design intent to mandatory wiring requirement — every IRR-positive module's R205 Module CapEx now binds on Allocator IN R8 via MIN(cash/cost, kg/mass, internal). (5) §6.6 Launch Capacity endogenous fleet wiring — Boosters built per year = Vehicle build claim cash / blended_cost_per_vehicle; F9 build rate decays via Assumptions schedule. Resolves Sprint 10 carry-forward R150 = $0 E:AC bug. (6) §8.2 V2/V3 ratchet retired — Starlink R43 + Assumptions R320 cleared with retirement-note labels. V2→V3 transition emerges from sigmoid weights + 3 physical gates (V3 trigger year, V2 phase-out year, F9 supply). New Assumptions input: V2 phase-out year (Base Case 2028, MC range). (7) §11.4 + §11.5 LM BV correction — BV engine is SoTP terminal value INPUT, NOT P&L D&A flow. Removed `BV depreciation — Lunar` + `BV depreciation — Mars` from Group P&L R28 Group D&A formula. Sprint 7 + Sprint 9 architectural error: BV depreciation routed into Group D&A inflated 2050 D&A from real ~$6B to phantom $484B. (8) §9 ODC unit economics clarification — per-sat IRR negative throughout horizon is model verdict; allocator correctly refuses cash to ODC. Deferred input revision to Sprint 11.5 audit pass. Cascading effect: Group P&L FCF 2050 recomputes from +$337B (illusory; included $478B phantom D&A add-back) to roughly -$90B (correct, post-correction). Sprint 9 §6.8 calibration target revision triggered post-Sprint-11.

### §20.9 Pre-IPO debt facility — cash inflow to break the deployment chicken-and-egg trap (AMENDED 2026-05-26 after Sprint 11 Block 2 collapse)

**Prior §6.1 Cash Pool Tracker** specified `Cash BoY(N) = Cash BoY(N-1) + Group FCF(N-1) + IPO injections(N)`. This worked structurally but assumed no external capital pre-IPO. Sprint 11 Block 2 attempted to wire Architecture §6.5 deployment binding (`MIN(cash/cost, kg/mass, internal_demand)`) and triggered the chicken-and-egg trap: pre-IPO Available cash = $0 (Cash BoY $5B − claims $11.6B) → modules can't deploy → no FCF → cash never recovers → Group Revenue 2050 collapsed $583B → $16B in V2.14.5.

**Correction**: SpaceX's historical funding pattern included pre-IPO debt + equity raises (~$5B/yr 2024-2025 from Series N + secondary rounds) that funded V2 fleet deployment. The Cash Pool Tracker needs to capture this external capital as a cash inflow.

**Amended §6.1 Cash Pool Tracker formula**:
```
Cash BoY(N) = Cash BoY(N-1) + Group FCF(N-1) + IPO injections(N) + Pre-IPO debt facility(N)
```

Where:
- Pre-IPO debt facility(N) reads a new Assumptions year-row input: `Pre-IPO bridge loan drawdown ($mm/yr)` — Base Case **$20,000M drawn in 2025 (per S-1 disclosure)**, $0 from 2026+ (single bridge to IPO 2027; IPO covers funding from then). MC range [$15,000M, $25,000M] triangle for draw amount; secondary MC input for draw-year (2025 vs 2026 vs split) if S-1 detail unclear. If S-1 specifies year-row split, refine: e.g., 2025 = $15B + 2026 = $5B.
- Allocator gains one new cash pool tracker row (between existing IPO and prior-FCF rows, or appended after R10) for the debt facility read.
- Cash BoY formula expanded to sum the new row.

**Effect on deployment binding**: With $20B bridge loan active, Available cash for IRR queue in 2025 = Cash BoY $5B + $20B bridge − $11.6B claims = **$13.4B available** (vs $0 pre-fix). This is sufficient to fund Starlink Module CapEx ($1.2B), Customer Launch CapEx ($33M), and substantial V3 BB ramp once trigger fires 2027 (V3 BB demand ~$4-5B in early years). In 2026: Cash BoY = $5B + $20B bridge + (-$2,569M 2025 FCF) − claims ~$15B (claims include $5B Spectrum 2nd-half) = roughly $4-5B available — modest but sufficient for V2 BB internal ramp. In 2027: $30B IPO arrives + bridge loan goes to $0 → Cash BoY jumps; Allocator queue has substantial capital for V3 ramp.

**Open architectural question (for Sprint 11.5 revision)**: should debt facility apply to BOTH allocator cash AND directly to module CapEx via a "non-allocator capital" line that bypasses the IRR queue entirely? This would let Starlink deploy in 2026 even if Allocator queue is gated — matching reality that debt-raised capital was deployed against pre-committed module CapEx plans, not allocated by IRR sigmoid. Defer to Vlad decision post-Sprint-11.

### §20.10 Amendment log entry — 2026-05-26 (Sprint 11 Block 2 collapse + debt facility fix)

Sprint 11 Block 2 (V2.14 → V2.14.5) wrote §3.5b + §3.6 + §3.7 + partial §3.9/§3.10/§3.11 but triggered chicken-and-egg trap via Architecture §6.5 deployment binding. Pre-IPO Available cash = $0 starves module deployment in 2026+ → Group Revenue 2050 collapsed from $583B (V2.14 Block 1 PASS state) to $16B. Recovery: revert to V2.14-a1636d7f (Block 1 PASS), apply §20.9 Pre-IPO bridge loan amendment (**$20B drawn 2025 per S-1 disclosure** — Vlad note 2026-05-26), then proceed with Block 2 writes (§3.5b/§3.6/§3.7/§3.9/§3.11) which now have a non-starved cash pipeline.

