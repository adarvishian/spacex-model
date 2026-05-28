# Sprint 10.5 Spec — Demand Curves rebuild

**Sprint name**: Demand Curves rebuild — replace year-row Q+P stubs with piecewise-linear Q→Revenue lookup tables (DTC + BB); add multiplicative annual TAM shift (inflation × GNI growth); rewire Sprint 4 Starlink BB + DTC revenue formulas; rewire Starlink per-vehicle marginal revenue (finite-difference); retire R231/R232 effective-$/Gbps memos.

**Status**: spec-author chat, drafted 2026-05-26 immediately after Sprint 10 PASS (V2.12). Triggered by Vlad surfacing the architectural error in V2.12 Demand Curves tab mid-Sprint-10 spec authoring. Form locked: piecewise-linear (Q, Revenue) lookup table per product; bracket-interpolation lookup; clip-at-max; multiplicative annual shift `(1+inflation)^t × (1+GNI)^t`; finite-difference marginal IRR.

**Dependencies landed**: Sprint 10 PASS in V2.12 (Allocator brain live; D15=$5,000M; D29=$0; D87=$1,000M LM carve-out; R108="OK" + R109=0 every year). Sprint 4 (Starlink module — R118/R119/R120/R128/R129/R131 revenue + R212-R230 per-vehicle IRR engines). Sprint 9 (Group P&L walk + conservation).

**Sprint 10 carry-forward (not Sprint 10.5 scope)**: (1) R150 Vehicle build claim is $50M in D-col only, $0 in E:AC because Launch Capacity R8/R9 cost components are D-col-only static inputs — Sprint 10 micro-bug, separate patch needed; (2) Group P&L D110 Σ Module FCF residual = -$454M baseline (Lock e audit-only), trajectory in V2.12 worsens to I110=-$1,491M, AC110=-$1,640M; (3) AC_2050 Group EBITDA = -$12,899M (Lock f surface-only — defer to Sprint 11). All three carried forward unchanged through Sprint 10.5.

**Calibration drift expected**: Sprint 10.5 mechanics will likely shift 2025 Starlink BB Revenue from V2.11/V2.12 $7,696M down to ~$6,400M (curve at Starlink's actual ~575k Gbps capacity gives ~$6.4B; lower than V2.11 stub mechanic gave). Group Revenue 2025 drops ~$15.1B → ~$13.8B (-8.6%, breaching Sprint 9 §6.8 ±5% tolerance). Out-years swing UP dramatically as the V2.11 demand-cap clip retires (curve naturally saturates via shape; no MIN clip). Document drift, do NOT retune curve table in spec — Vlad refines table values pre-execution if 2025 anchor needs to hit exactly. Sprint 9 §6.8 revision conversation slot **post-Sprint-10.5** once full trajectory is visible.

---

## §0 Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md` and the four constitutional docs.

- [x] **Rule 1** (one concept per write) — every §3.x section structures writes as separate blocks: column-A labels first, lookup formulas second, number formats third. Demand Curves tab table sections written row-by-row.
- [x] **Rule 3 / 23** — annual TAM shift formula uses anchor-and-offset: `(1+inflation)^E$5 × (1+GNI_growth)^E$5`. No year-chained recursion. Starlink revenue rewire uses single-cell lookup formulas with E$5+1 year-offset for cross-tab year-row reads. ZERO Rule 23 EXCEPTIONS in Sprint 10.5.
- [x] **Rule 4** (verification gate) — every §3.x section ends with D / I / S / AC read-backs + expected values. §4 consolidates calibration check.
- [x] **Rule 6** (inline formulas) — every cell write specified with full Excel formula.
- [x] **Rule 10** (no row insertions) — Demand Curves tab DELETE-then-WRITE pattern: clear R9:AC12 (the four year-row stubs), then APPEND new sections below them (R15+). New Assumptions inputs APPEND at next available row after R29 (R30 is currently §3 CAPACITY section header; spec checks for available append point and either appends within §2 ALLOCATOR sub-block or creates §2.5 sub-block at next free row). Sprint 4 Starlink rewire is in-place formula REPLACE on R120/R131/R212/R217/R222/R227 (single-cell replaces, no row moves).
- [x] **Rule 11** (touch points) — every formula rewire lists downstream consumers. R120 rewire → R178 (Starlink Total Revenue) → R201 (Allocator OUT) → Allocator R49 (Starlink cash demand) → Group P&L R8 (Σ module revenue) → R10 (Group Revenue net of elims) → R26 (EBITDA) → R50 (FCF). Same chain for R131 DTC. Per-vehicle IRR rewire → Allocator R48-R55 cash sigmoid sub-block (Starlink) → Module IN cells next year. Plus OpEx R&D (read Starlink revenue for R&D % calc).
- [x] **Rule 12** (label-based cross-tab refs) — every cross-tab pull resolves via INDEX/MATCH on canonical labels. New Demand Curves canonical labels enumerated in §3.4.
- [x] **Rule 13** — N/A. Sprint 10.5 rewires Starlink revenue mechanic (vending-machine-compliant change — revenue stays at Revenue, not COGS).
- [x] **Rule 14** (no hardcoded constants) — inflation rate + GNI growth rate live on Assumptions §2 (new inputs). Curve breakpoint values live on Demand Curves tab (treated as structural data table; not "behaviour parameters" per Rule 14 spirit — they're calibrated market structure inputs).
- [x] **Rule 15** (sanity check halt thresholds) — every check in §4 has quantitative threshold. Calibration: Group Revenue 2025 expected drift to ~$13.8B (8.6% below current $15.1B); halt only if Group Revenue 2025 < $11B or > $17B (±$4B wider tolerance reflecting expected mechanic-driven drift, not error tolerance). Conservation R108 = "OK" every year (mandatory). Round-trip stability < $1M.
- [x] **Rule 19** — standing rule: Vlad handles all saving. Spec does NOT name target workbook.
- [x] **Rule 22** (stale-ref scan) — §4.4 Rule 22 scan enumerates every new cross-tab pull (Starlink R120/R131 → Demand Curves canonical labels; Starlink R212/R217/R222/R227 → Demand Curves canonical labels; Demand Curves year-row reads → Starlink R118/R128).

**Architecture & Methodology compliance:**

- [x] Demand curve form per Architecture §18 amendment (§3.1 below): piecewise-linear (Q, Revenue) lookup table per product; bracket-interpolation via FORECAST function with MIN/MAX clamps for clip-at-max.
- [x] Annual TAM shift: multiplicative `(1+inflation)^t × (1+GNI_growth)^t` (Vlad lock 2026-05-26).
- [x] DTC clip-at-max + BB clip-at-max via MIN/MAX clamps in lookup formula.
- [x] Per-vehicle marginal IRR via finite difference: `marginal_rev_per_sat = curve_lookup(Q + per_sat_Gbps) − curve_lookup(Q)`.
- [x] Year-offset helper row at row 5 on Demand Curves (existing — D5=0, E5=1, ..., AC5=25). All new year-row formulas reference E$5 for offset.
- [x] ZERO OFFSET formulas; bracket-interpolation uses FORECAST + INDEX/MATCH pattern.

---

## §1 Scope summary

| Section | What ships | Rows / cells touched |
|---|---|---|
| §3.0 Pre-flight | 7 halt-bearing checks on Sprint 10 PASS state + Starlink module formulas + Demand Curves tab state | read-only |
| §3.1 Architecture §18 amendment | Update `02_Architecture_and_Methodology.md` §18 item 5 with locked form | constitutional doc (Vlad applies) |
| §3.2 Assumptions §2 ALLOCATOR new inputs | Add 2 inputs: inflation rate + GNI growth rate (with MC ranges) | Assumptions append: 2 new rows |
| §3.3 Demand Curves tab rebuild — DELETE then ADD | Clear R9:AC12 (legacy stubs); write 2 table sections (DTC + BB) with verbatim breakpoints from Vlad | Demand Curves R9-R12 cleared; R15-R75 (DTC, ~60 rows); R78-R140 (BB, ~57 rows) |
| §3.4 Demand Curves year-row evaluator | One canonical Q-input year-row + one Revenue-output year-row per product; lookup uses Starlink R118/R128 supply + annual shift | Demand Curves ~4 new year-rows below tables |
| §3.5 Starlink R120 + R131 revenue rewire | Replace MIN(supply, demand)×price with bracket-interpolation lookup against Demand Curves Revenue year-rows | Starlink R120 + R131 (in-place replace) |
| §3.6 Per-vehicle marginal revenue rewire | Replace R212/R217/R222/R227 formulas (currently read R231/R232) with finite-difference against curve lookup | Starlink R212, R217, R222, R227 |
| §3.7 Retire R231/R232 memo rows | Repurpose as informational: R231 now = average $/Gbps BB from curve = BB Revenue / BB Gbps supplied (diagnostic); R232 same for DTC | Starlink R231, R232 (label + formula change) |

**Publishes new canonical labels** (Rule 12 — verbatim case-sensitive, halt on drift):
1. `BB Q breakpoint #N (Gbps)` (N = 1..57) — Demand Curves BB section, col B
2. `BB Revenue at breakpoint #N ($mm)` (N = 1..57) — Demand Curves BB section, col C
3. `DTC Q breakpoint #N (Gbps)` (N = 1..60) — Demand Curves DTC section, col B
4. `DTC Revenue at breakpoint #N ($mm)` (N = 1..60) — Demand Curves DTC section, col C
5. `Starlink BB capacity input (Gbps)` — Demand Curves year-row, reads Starlink!R118 by canonical label
6. `Starlink DTC capacity input (Gbps)` — Demand Curves year-row, reads Starlink!R128 by canonical label
7. `Starlink BB Revenue from curve ($mm)` — Demand Curves year-row output (read by Starlink R120)
8. `Starlink DTC Revenue from curve ($mm)` — Demand Curves year-row output (read by Starlink R131)
9. `Annual TAM shift multiplier` — Demand Curves year-row = `(1+inflation)^E$5 × (1+GNI)^E$5`
10. `Inflation rate (% per year)` — Assumptions §2 (new input)
11. `Real GNI growth rate (% per year)` — Assumptions §2 (new input)

---

## §2 Constitutional reference

- **Lessons §1** — postponed architectural decisions create retrofit cascades. Sprint 10.5 is the third load-bearing methodology arriving late in Rebuild v2 (after vending-machine framing arrived Refine Spec 01 V30.5 and per-sat IRR arrived Spec 08/09 V30.5). Sprint 5 closed Architecture §18 item 5 INCORRECTLY by building year-row stubs instead of the proper Q→Revenue lookup. The lesson here for future: closures of load-bearing methodology items deserve explicit re-review at Sprint N+3 minimum, even if the closure looks correct at the time. Memory entry [[project-demand-curves-rebuild-2026-05-26]] captures this.
- **Lessons §22** — within-year cycle bistability. Sprint 10.5 introduces a new minor cycle: Starlink BB Revenue → Group Revenue → R&D (via OpEx % of revenue) → Module CapEx allocation (via OpEx feeding Queue Gate) → Module deployment → Starlink Gbps supplied → BB Revenue. This cycle already existed pre-Sprint-10.5 via the V2.11 mechanic (BB Revenue = capacity × price); rewiring to curve lookup doesn't introduce new cycles. Iterative calc should still converge <10 iter; verify post-write.
- **Principle 23** — calibration targets locked pre-build; outputs hit them within tolerance. Sprint 9 §6.8 target Group Revenue 2025 = $14.65B ±5% will likely drift below tolerance to ~$13.8B (-8.6%). Per §1 above, this is mechanic-driven drift not error drift. Sprint 9 §6.8 revision conversation slot opens post-Sprint-10.5.
- **Architecture §18 item 5** — to be amended in §3.1 below.

---

## §3 Execution

### §3.0 Pre-flight (READ-ONLY — halt if any check fails)

**Check 1 — Sprint 10 PASS values intact:**
```
Read Allocator D15 expect $5,000M exact
Read Allocator D29 expect $0 exact
Read Allocator D35 expect $1,000M exact (Mars carve-out floor)
Read Allocator D83 expect ~$32.86M (Customer Launch override)
Read Allocator D84 expect ~$1,202.54M (Starlink override)
Read Allocator D87 expect $1,000M exact (Lunar Mars carve-out)
Read Group P&L D108 expect "OK" exact
Read Group P&L D109 expect 0 ±$1M
Read Group P&L AC108 expect "OK" exact
Read Group P&L AC109 expect 0 ±$1M
```
If any fails: HALT. Sprint 10 PASS must hold before Sprint 10.5 begins.

**Check 2 — Starlink module revenue formulas exist + read Demand Curves stubs:**
```
MATCH Starlink "BB Revenue ($mm)" expect row 120
MATCH Starlink "DTC Revenue ($mm)" expect row 131
MATCH Starlink "BB Gbps available for external Starlink revenue" expect row 118
MATCH Starlink "DTC Gbps available for external Starlink revenue" expect row 128
MATCH Starlink "BB $/Gbps ($/Gbps/yr)" expect row 119
MATCH Starlink "DTC $/Gbps ($/Gbps/yr)" expect row 129
Read Starlink!D120 formula text expect substring "MIN(" + substring "Total BB price"
Read Starlink!D131 formula text expect substring "MIN(" + substring "Total DTC price"
Read Starlink!D120 value expect ~$7,696M ±$50M
Read Starlink!D131 value expect ~$157M ±$10M
```
If formulas don't have MIN(supply, demand) × price pattern: HALT — Sprint 4 module state has drifted, re-audit Sprint 4 before Sprint 10.5.

**Check 3 — Starlink per-vehicle IRR engines + memo rows exist:**
```
MATCH Starlink "Memo: V2 BB per-sat net marginal revenue per year ($mm/sat/yr)" expect row 212
MATCH Starlink "Memo: V2 DTC per-sat net marginal revenue per year ($mm/sat/yr)" expect row 217
MATCH Starlink "Memo: V3 BB per-sat net marginal revenue per year ($mm/sat/yr)" expect row 222
MATCH Starlink "Memo: V3 DTC per-sat net marginal revenue per year ($mm/sat/yr)" expect row 227
MATCH Starlink "Memo: Effective marginal $/Gbps BB (post-demand-cap)" expect row 231
MATCH Starlink "Memo: Effective marginal $/Gbps DTC (post-demand-cap)" expect row 232
Read Starlink!D212 formula text expect substring "D$231" (R212 reads R231 for BB $/Gbps)
Read Starlink!D217 formula text expect substring "D$232" (R217 reads R232 for DTC $/Gbps)
```
If any expected row position drifted or formulas don't read R231/R232: HALT.

**Check 4 — Demand Curves tab current state (the stubs to be retired):**
```
MATCH Demand Curves "Total BB Gbps demand (Gbps/yr)" expect row 9
MATCH Demand Curves "Total BB price ($/Gbps/yr)" expect row 10
MATCH Demand Curves "Total DTC Gbps demand (Gbps/yr)" expect row 11
MATCH Demand Curves "Total DTC price ($/Gbps/yr)" expect row 12
Read Demand Curves D9 expect ~80,000 (legacy BB Gbps demand stub value)
Read Demand Curves D10 expect ~$96,200 (legacy BB price stub)
Read Demand Curves D11 expect ~300 (legacy DTC Gbps demand stub)
Read Demand Curves D12 expect ~$1,207,692 (legacy DTC price stub)
Read Demand Curves R13:AC75 for any non-empty cells (should all be empty — confirms append space)
```
If R9-R12 don't exist as expected, the legacy stub layout has changed; HALT and re-probe before deletion. If R13+ has unexpected content: HALT — append-target area is occupied.

**Check 5 — Assumptions §2 ALLOCATOR last filled row:**
```
Find last filled Assumptions row in §2 ALLOCATOR (currently R29; §3 CAPACITY starts at R30).
Confirm R29 is last filled in §2 sub-block.
```
The new inflation + GNI inputs need a home. Per Rule 10 (no row insertions), can't insert between R29 and R30. Best path: append at end of Assumptions tab (R346+) in a new sub-section, OR if R29 + R30 have space between (gap), use the gap. Spec author judgment based on pre-flight read.

**Check 6 — Iterative calc workbook setting:**
```
Read workbook.calculation.iterate expect True
```
If False: HALT — workbook setting must be ON; demand curve rewire could compound bistability if iterative calc is off.

**Check 7 — Sprint 9 + 10 canonical labels still resolve (sanity):**
```
MATCH Group P&L "GROUP REVENUE NET OF ELIMS ($mm)" expect row 10
MATCH Group P&L "Group EBITDA ($mm)" expect row 26
MATCH Group P&L "GROUP FCF ($mm)" expect row 50
MATCH Allocator "Cash BoY ($mm)" expect row 15
MATCH Allocator "Available cash for IRR queue ($mm)" expect row 29
MATCH Allocator "Vehicle build claim ($mm)" expect row 150
MATCH Allocator "Customer Launch cash allocation" expect row 83
MATCH Allocator "Starlink cash allocation" expect row 84
```
If any returns #N/A: HALT — Sprint 9/10 canonical labels drifted.

If all 7 checks pass: proceed to §3.1.

---

### §3.1 Architecture §18 amendment (constitutional doc edit; Vlad applies before plugin execution)

Update `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/02_Architecture_and_Methodology.md` §18 item 5 with the following amendment text (verbatim — Vlad pastes into the doc, NOT plugin writes):

```markdown
### §18 Item 5 — Demand Curves tab (AMENDED 2026-05-26)

**Status**: LOAD-BEARING. Form locked Vlad 2026-05-26 after Sprint 5 closed §18 item 5
INCORRECTLY (parallel Q + P year-row stubs with no functional Q→Revenue link).

**Form**: Piecewise-linear lookup table per product (DTC + BB). Two columns per product:
  - Col B: Q breakpoint (Gbps)
  - Col C: Revenue at that breakpoint ($mm — DTC; raw $ — BB; see units note)

**Lookup**: Bracket-interpolation. Given Q_supplied (from module module-tab), find the two
table rows that bracket Q_supplied; linearly interpolate revenue.

Excel formula (clip-at-max variant):
```
=IF(Q_supplied >= MAX(Q_col), MAX(Revenue_col),
 IF(Q_supplied <= MIN(Q_col), MIN(Revenue_col),
   FORECAST(Q_supplied, Revenue_col, Q_col)
 )
)
```

**Annual TAM shift**: Curve breakpoints are 2025-anchored. Each year multiply lookup result
by `(1 + inflation)^t × (1 + GNI_growth)^t` where t = year offset (D=0, E=1, ..., AC=25).

Inflation + GNI parameters live on Assumptions §2 ALLOCATOR (MC inputs).

**Per-vehicle marginal IRR**: Marginal revenue per sat derived via finite difference:
  `marginal_rev_per_sat(year T) = curve_lookup(Q + per_sat_Gbps, year T) − curve_lookup(Q, year T)`

  where Q = current Starlink BB (or DTC) capacity supplied that year, per_sat_Gbps = bandwidth
  one additional sat contributes. Smooth taper as Q approaches saturation — IRR engines see
  the curve's diminishing returns directly.

**Units note (BB)**: Vlad lock 2026-05-26 — BB TAM curve values are raw $ (NOT $mm as labeled).
At 100k Gbps Starlink BB capacity, BB TAM ≈ $2.94B. At Starlink's actual ~575k Gbps 2025
capacity, BB TAM ≈ $6.4B (interpolated). Sprint 10.5 spec section §3.4 BB Revenue formula
reads raw values from Demand Curves col C as $mm directly (divide by 1e6 if needed to
align units — but raw $ at 100k=$2.94B treated as $mm at 100k=$2.94M doesn't tie; spec
author chose to treat values as $mm directly, accepting that calibration drift may occur
and Vlad refines the curve table to hit 2025 anchor). Resolution: see Sprint 10.5 §3.3
spec body for units handling convention.

**Saturation**: DTC curve saturates ~84k Gbps at $15,920M; BB curve saturates ~250M Gbps at
$187,819M. Beyond saturation, lookup returns the max value (no extrapolation).

**Starshield**: Stays flat at Assumptions R96 = $164,699/Gbps base year (procurement-driven,
no curve). May be revisited Sprint 11+ if Starshield TAM mechanics merit refinement.

**Demand-cap retirement**: V2.11 mechanic `Revenue = MIN(supply_modeled, demand_year_row) ×
price_year_row` is retired. Saturation now comes from curve shape (asymptotic flattening),
not a binary MIN clip. The implicit cap is the curve's max revenue value.

**Calibration**: 2025 Starlink BB Revenue should land within ±15% of V2.11 $7,696M anchor
(curve at ~575k Gbps gives ~$6.4B uncapped, ~$6.6B at slightly higher Q; multiplicative shift
year T=0 multiplier = 1). DTC 2025 should land within ±15% of V2.11 $157M (curve at 130 Gbps
extrapolates downward from row 1 at 280 Gbps; ~$142M). Group Revenue 2025 expected to drop
~8% from current $15,137M to ~$13,800M. Sprint 9 §6.8 revision conversation slot OPEN
post-Sprint-10.5 once full trajectory visible.
```

After Vlad applies the amendment, plugin proceeds with §3.2.

---

### §3.2 Assumptions §2 ALLOCATOR new inputs

Find the last filled Assumptions §2 row (currently R29). The two new inputs need to land. Per Rule 10, no row insertion between R29 and R30 (R30 starts §3 CAPACITY). Two append options:

**Option A (Recommended)** — append at end of Assumptions tab in new §12 DEMAND CURVES SHIFT sub-section.
**Option B** — pre-flight Check 5 confirmed §2 ends at R29; if there's a structural gap before §3 CAPACITY header, write inflation + GNI in that gap.

Plugin executes Option A (cleanest — keeps §2 boundary intact). Writes at next available row after Assumptions last filled row (= R344 + spacer = R346 onwards):

| Row | Col A label (verbatim) | Col B value | Col C MC Min | Col D MC Max | Col E Dist | Col F Notes |
|---|---|---|---|---|---|---|
| R346 | `§12 DEMAND CURVES SHIFT (Sprint 10.5)` | (section header) | — | — | — | — |
| R347 | `▸ Annual TAM growth — inflation + real GNI components` | (sub-section header) | — | — | — | — |
| R348 | `Inflation rate (% per year)` | 0.025 | 0.01 | 0.05 | triangle | Base Case 2.5%/yr; FRED long-run CPI ~2.3%; MC triangle [1%, 5%] |
| R349 | `Real GNI growth rate (% per year)` | 0.030 | 0.01 | 0.06 | triangle | Base Case 3.0%/yr; world GNI long-run ~2.8%; MC triangle [1%, 6%] |

**Number format**: Col B = `0.00%`. Col C/D = `0.00%`. Col E = text. Col F = text.

**Verification reads:**
- R348 B = 0.025 exact
- R349 B = 0.030 exact

**Touch points (Rule 11):**
- Demand Curves year-row R(eval) `Annual TAM shift multiplier` reads R348 + R349 by canonical label (§3.4 below).

---

### §3.3 Demand Curves tab rebuild — DELETE then ADD

#### §3.3.1 Clear legacy stubs

**Delete content from Demand Curves rows R9, R10, R11, R12 (col A through col AC)**:

```
For each row r in {9, 10, 11, 12}:
    For each col c in D:AC:
        Set Demand Curves!{c}{r} = (empty)
    Set Demand Curves!A{r} = (empty)
```

Plus optionally R7 (section header `BANDWIDTH DEMAND CURVES — total addressable bandwidth × price`) — replace with new section header. Recommend: delete R7 too; write new section headers below.

**Verification:**
- D9, D10, D11, D12 all return None/blank after clear
- A9, A10, A11, A12 all return None/blank

**Touch points (Rule 11):**
- Starlink R119 currently reads Demand Curves R10 → will return #N/A after clear → halts Sprint 4 Starlink. §3.5 below repoints R119 + R129 before recalc; or alternatively §3.5 executes simultaneously (atomic via execute_office_js).
- **Plugin execution order is critical**: §3.3.1 + §3.3.2 + §3.4 + §3.5 must all complete before workbook recalculates. Recommend executing as a single execute_office_js batch with all writes, then trigger recalc.

#### §3.3.2 Write DTC table section

Starting at Demand Curves row 15:

| Row | Col A label | Col B value (Q Gbps) | Col C value (Revenue $mm) | Notes |
|---|---|---|---|---|
| R15 | `DTC DEMAND CURVE (piecewise-linear Q→Revenue lookup)` | (section header) | — | bold |
| R16 | `Constellation Bandwidth (Gbps)` | (col B header) | `Annual DTC Revenue ($mm)` (col C header) | italic |
| R17 | `DTC Q breakpoint #1 (Gbps)` | 280.2 | 307 | |
| R18 | `DTC Q breakpoint #2 (Gbps)` | 560.3 | 613 | |
| R19 | `DTC Q breakpoint #3 (Gbps)` | 840.5 | 920 | |
| R20 | `DTC Q breakpoint #4 (Gbps)` | 1120.6 | 1227 | |
| R21 | `DTC Q breakpoint #5 (Gbps)` | 1400.8 | 1534 | |
| R22 | `DTC Q breakpoint #6 (Gbps)` | 1680.9 | 1840 | |
| R23 | `DTC Q breakpoint #7 (Gbps)` | 1961.1 | 2147 | |
| R24 | `DTC Q breakpoint #8 (Gbps)` | 2241.2 | 2454 | |
| R25 | `DTC Q breakpoint #9 (Gbps)` | 2521.4 | 2760 | |
| R26 | `DTC Q breakpoint #10 (Gbps)` | 2801.5 | 3067 | |
| R27 | `DTC Q breakpoint #11 (Gbps)` | 3501.9 | 3827 | |
| R28 | `DTC Q breakpoint #12 (Gbps)` | 4202.3 | 4587 | |
| R29 | `DTC Q breakpoint #13 (Gbps)` | 4902.7 | 5347 | |
| R30 | `DTC Q breakpoint #14 (Gbps)` | 5603.1 | 6107 | |
| R31 | `DTC Q breakpoint #15 (Gbps)` | 6303.5 | 6867 | |
| R32 | `DTC Q breakpoint #16 (Gbps)` | 7003.9 | 7627 | |
| R33 | `DTC Q breakpoint #17 (Gbps)` | 7704.2 | 8387 | |
| R34 | `DTC Q breakpoint #18 (Gbps)` | 8404.6 | 9147 | |
| R35 | `DTC Q breakpoint #19 (Gbps)` | 9105.0 | 9453 | |
| R36 | `DTC Q breakpoint #20 (Gbps)` | 9805.4 | 9760 | |
| R37 | `DTC Q breakpoint #21 (Gbps)` | 10505.8 | 10067 | |
| R38 | `DTC Q breakpoint #22 (Gbps)` | 11206.2 | 10373 | |
| R39 | `DTC Q breakpoint #23 (Gbps)` | 11906.6 | 10680 | |
| R40 | `DTC Q breakpoint #24 (Gbps)` | 12606.9 | 10987 | |
| R41 | `DTC Q breakpoint #25 (Gbps)` | 13307.3 | 11293 | |
| R42 | `DTC Q breakpoint #26 (Gbps)` | 14007.7 | 11600 | |
| R43 | `DTC Q breakpoint #27 (Gbps)` | 15408.5 | 11760 | |
| R44 | `DTC Q breakpoint #28 (Gbps)` | 16809.3 | 11920 | |
| R45 | `DTC Q breakpoint #29 (Gbps)` | 18210.0 | 12080 | |
| R46 | `DTC Q breakpoint #30 (Gbps)` | 19610.8 | 12240 | |
| R47 | `DTC Q breakpoint #31 (Gbps)` | 21011.6 | 12400 | |
| R48 | `DTC Q breakpoint #32 (Gbps)` | 22412.3 | 12560 | |
| R49 | `DTC Q breakpoint #33 (Gbps)` | 23813.1 | 12720 | |
| R50 | `DTC Q breakpoint #34 (Gbps)` | 25213.9 | 12880 | |
| R51 | `DTC Q breakpoint #35 (Gbps)` | 26614.6 | 13040 | |
| R52 | `DTC Q breakpoint #36 (Gbps)` | 28015.4 | 13200 | |
| R53 | `DTC Q breakpoint #37 (Gbps)` | 29416.2 | 13360 | |
| R54 | `DTC Q breakpoint #38 (Gbps)` | 30817.0 | 13467 | |
| R55 | `DTC Q breakpoint #39 (Gbps)` | 32217.7 | 13573 | |
| R56 | `DTC Q breakpoint #40 (Gbps)` | 33618.5 | 13680 | |
| R57 | `DTC Q breakpoint #41 (Gbps)` | 35019.3 | 13787 | |
| R58 | `DTC Q breakpoint #42 (Gbps)` | 36420.0 | 13893 | |
| R59 | `DTC Q breakpoint #43 (Gbps)` | 37820.8 | 14000 | |
| R60 | `DTC Q breakpoint #44 (Gbps)` | 39221.6 | 14107 | |
| R61 | `DTC Q breakpoint #45 (Gbps)` | 40622.4 | 14213 | |
| R62 | `DTC Q breakpoint #46 (Gbps)` | 42023.1 | 14320 | |
| R63 | `DTC Q breakpoint #47 (Gbps)` | 44824.7 | 14427 | |
| R64 | `DTC Q breakpoint #48 (Gbps)` | 47626.2 | 14533 | |
| R65 | `DTC Q breakpoint #49 (Gbps)` | 50427.8 | 14640 | |
| R66 | `DTC Q breakpoint #50 (Gbps)` | 53229.3 | 14747 | |
| R67 | `DTC Q breakpoint #51 (Gbps)` | 56030.8 | 14853 | |
| R68 | `DTC Q breakpoint #52 (Gbps)` | 58832.4 | 14960 | |
| R69 | `DTC Q breakpoint #53 (Gbps)` | 61633.9 | 15067 | |
| R70 | `DTC Q breakpoint #54 (Gbps)` | 64435.5 | 15173 | |
| R71 | `DTC Q breakpoint #55 (Gbps)` | 67237.0 | 15280 | |
| R72 | `DTC Q breakpoint #56 (Gbps)` | 70038.5 | 15387 | |
| R73 | `DTC Q breakpoint #57 (Gbps)` | 72840.1 | 15493 | |
| R74 | `DTC Q breakpoint #58 (Gbps)` | 75641.6 | 15600 | |
| R75 | `DTC Q breakpoint #59 (Gbps)` | 78443.2 | 15707 | |
| R76 | `DTC Q breakpoint #60 (Gbps)` | 81244.7 | 15813 | |
| R77 | `DTC Q breakpoint #61 (Gbps)` | 84046.3 | 15920 | |

**Number format**: Col B = `#,##0.0` (Gbps with 1 decimal). Col C = `#,##0` ($mm).

**Verification reads:**
- B17 expect 280.2
- C17 expect 307
- B77 expect 84046.3 (max breakpoint)
- C77 expect 15920 (max revenue at saturation)

#### §3.3.3 Write BB table section

Starting at Demand Curves row 80 (one row spacer after DTC):

| Row | Col A label | Col B value (Q Gbps) | Col C value (Revenue $mm) | Notes |
|---|---|---|---|---|
| R80 | `BB DEMAND CURVE (piecewise-linear Q→Revenue lookup)` | (section header) | — | bold |
| R81 | `Capacity (Gbps)` | (col B header) | `BB TAM/Revenue ($mm — interpreted as raw $ per Vlad lock 2026-05-26)` (col C header) | italic |
| R82 | `BB Q breakpoint #1 (Gbps)` | 100000 | 2936307032 | |
| R83 | `BB Q breakpoint #2 (Gbps)` | 200000 | 3747517779 | |
| R84 | `BB Q breakpoint #3 (Gbps)` | 300000 | 4558728527 | |
| R85 | `BB Q breakpoint #4 (Gbps)` | 400000 | 5369939275 | |
| R86 | `BB Q breakpoint #5 (Gbps)` | 500000 | 6157050612 | |
| R87 | `BB Q breakpoint #6 (Gbps)` | 1000000 | 10055218687 | |
| R88 | `BB Q breakpoint #7 (Gbps)` | 2000000 | 17173327745 | |
| R89 | `BB Q breakpoint #8 (Gbps)` | 3000000 | 23037496877 | |
| R90 | `BB Q breakpoint #9 (Gbps)` | 4000000 | 28429685847 | |
| R91 | `BB Q breakpoint #10 (Gbps)` | 5000000 | 33451147506 | |
| R92 | `BB Q breakpoint #11 (Gbps)` | 6000000 | 38244393489 | |
| R93 | `BB Q breakpoint #12 (Gbps)` | 7000000 | 42519957752 | |
| R94 | `BB Q breakpoint #13 (Gbps)` | 8000000 | 46242252812 | |
| R95 | `BB Q breakpoint #14 (Gbps)` | 9000000 | 49843624537 | |
| R96 | `BB Q breakpoint #15 (Gbps)` | 10000000 | 53439883071 | |
| R97 | `BB Q breakpoint #16 (Gbps)` | 11000000 | 56884620244 | |
| R98 | `BB Q breakpoint #17 (Gbps)` | 12000000 | 60203448780 | |
| R99 | `BB Q breakpoint #18 (Gbps)` | 13000000 | 63409756329 | |
| R100 | `BB Q breakpoint #19 (Gbps)` | 14000000 | 66053251721 | |
| R101 | `BB Q breakpoint #20 (Gbps)` | 15000000 | 68594914445 | |
| R102 | `BB Q breakpoint #21 (Gbps)` | 16000000 | 71081263247 | |
| R103 | `BB Q breakpoint #22 (Gbps)` | 17000000 | 73420507599 | |
| R104 | `BB Q breakpoint #23 (Gbps)` | 18000000 | 75685062530 | |
| R105 | `BB Q breakpoint #24 (Gbps)` | 19000000 | 77883237882 | |
| R106 | `BB Q breakpoint #25 (Gbps)` | 20000000 | 80041312918 | |
| R107 | `BB Q breakpoint #26 (Gbps)` | 25000000 | 90064272311 | |
| R108 | `BB Q breakpoint #27 (Gbps)` | 30000000 | 98997511563 | |
| R109 | `BB Q breakpoint #28 (Gbps)` | 35000000 | 107341230210 | |
| R110 | `BB Q breakpoint #29 (Gbps)` | 40000000 | 115429256293 | |
| R111 | `BB Q breakpoint #30 (Gbps)` | 45000000 | 123061346625 | |
| R112 | `BB Q breakpoint #31 (Gbps)` | 50000000 | 129757305220 | |
| R113 | `BB Q breakpoint #32 (Gbps)` | 55000000 | 134938291456 | |
| R114 | `BB Q breakpoint #33 (Gbps)` | 60000000 | 139138397682 | |
| R115 | `BB Q breakpoint #34 (Gbps)` | 65000000 | 142624306619 | |
| R116 | `BB Q breakpoint #35 (Gbps)` | 70000000 | 145963976660 | |
| R117 | `BB Q breakpoint #36 (Gbps)` | 75000000 | 149300775281 | |
| R118 | `BB Q breakpoint #37 (Gbps)` | 80000000 | 152636715075 | |
| R119 | `BB Q breakpoint #38 (Gbps)` | 85000000 | 155869846884 | |
| R120 | `BB Q breakpoint #39 (Gbps)` | 88000000 | 157697795521 | |
| R121 | `BB Q breakpoint #40 (Gbps)` | 90000000 | 158912000000 | |
| R122 | `BB Q breakpoint #41 (Gbps)` | 100000000 | 163656000000 | |
| R123 | `BB Q breakpoint #42 (Gbps)` | 110000000 | 166065000000 | |
| R124 | `BB Q breakpoint #43 (Gbps)` | 120000000 | 168368000000 | |
| R125 | `BB Q breakpoint #44 (Gbps)` | 130000000 | 170578000000 | |
| R126 | `BB Q breakpoint #45 (Gbps)` | 140000000 | 172765000000 | |
| R127 | `BB Q breakpoint #46 (Gbps)` | 150000000 | 174895000000 | |
| R128 | `BB Q breakpoint #47 (Gbps)` | 160000000 | 176859000000 | |
| R129 | `BB Q breakpoint #48 (Gbps)` | 170000000 | 178452000000 | |
| R130 | `BB Q breakpoint #49 (Gbps)` | 180000000 | 179780000000 | |
| R131 | `BB Q breakpoint #50 (Gbps)` | 190000000 | 181109000000 | |
| R132 | `BB Q breakpoint #51 (Gbps)` | 200000000 | 182421000000 | |
| R133 | `BB Q breakpoint #52 (Gbps)` | 210000000 | 183627000000 | |
| R134 | `BB Q breakpoint #53 (Gbps)` | 220000000 | 184773000000 | |
| R135 | `BB Q breakpoint #54 (Gbps)` | 230000000 | 185867000000 | |
| R136 | `BB Q breakpoint #55 (Gbps)` | 240000000 | 186843000000 | |
| R137 | `BB Q breakpoint #56 (Gbps)` | 250000000 | 187819000000 | |

**Number format**: Col B = `#,##0` (Gbps). Col C = `#,##0` (raw value).

**Verification reads:**
- B82 expect 100,000
- C82 expect 2,936,307,032
- B137 expect 250,000,000
- C137 expect 187,819,000,000

**Units note (load-bearing)**: Vlad lock 2026-05-26 — raw $ interpretation. C-col values are in $ (despite Demand Curves general convention of $mm). Sprint 10.5 lookup formulas in §3.4 below divide by 1,000,000 when reading BB Revenue to convert raw $ → $mm for downstream consumption by Starlink R120 (which holds revenue in $mm). DTC C-col values are in $mm directly (no conversion). **Critical**: spec author treats BB and DTC differently in §3.4 lookup formulas due to this unit asymmetry.

---

### §3.4 Demand Curves tab — year-row evaluator formulas

Below the BB table section (starting at R140), write the year-row lookups + shift multiplier + outputs that Starlink R120 + R131 will read.

| Row | Col A label (verbatim) | Col D formula | Number format |
|---|---|---|---|
| R140 | `▸ Curve evaluators (year-row, read by Starlink module)` | (sub-header) | italic |
| R141 | `Annual TAM shift multiplier` | `=(1 + INDEX(Assumptions!$B:$B, MATCH("Inflation rate (% per year)", Assumptions!$A:$A, 0)))^D$5 * (1 + INDEX(Assumptions!$B:$B, MATCH("Real GNI growth rate (% per year)", Assumptions!$A:$A, 0)))^D$5` | `0.000` |
| R142 | `Starlink BB capacity input (Gbps)` | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("BB Gbps available for external Starlink revenue", Starlink!$A:$A, 0), D$5+1), 0)` | `#,##0` |
| R143 | `Starlink DTC capacity input (Gbps)` | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("DTC Gbps available for external Starlink revenue", Starlink!$A:$A, 0), D$5+1), 0)` | `#,##0` |
| R144 | `Starlink BB Revenue from curve ($mm)` | (see formula below) | `#,##0` |
| R145 | `Starlink DTC Revenue from curve ($mm)` | (see formula below) | `#,##0` |
| R146 | `Memo: BB marginal Revenue per Gbps ($mm/Gbps)` | `=IFERROR((D144 - IFERROR(D144_minus_per_sat_lookup, 0)) / 1, 0)` (informational; see §3.6 for proper finite-diff used in IRR) | `0.000` |

Copy D-col formulas across E:AC for R141-R146.

**R144 Starlink BB Revenue from curve ($mm) — full formula:**

```
=IF(D142 >= MAX(B82:B137), MAX(C82:C137),
 IF(D142 <= MIN(B82:B137), MIN(C82:C137),
   FORECAST(D142, C82:C137, B82:B137)
 )
) / 1000000 * D141
```

Breakdown:
- IF guard 1: if Starlink BB Gbps >= 250M (table max), return max revenue value `MAX(C82:C137)` = 187,819,000,000
- IF guard 2: if Starlink BB Gbps <= 100k (table min), return min revenue value `MIN(C82:C137)` = 2,936,307,032 (or use linear extrap; FORECAST below handles this naturally — but the explicit clip prevents extrapolation to negative Q)
- FORECAST: linear interpolation between table breakpoints
- Division by 1,000,000: BB curve values in raw $ → convert to $mm
- Multiplication by D141: annual TAM shift multiplier

**R145 Starlink DTC Revenue from curve ($mm) — full formula:**

```
=IF(D143 >= MAX(B17:B77), MAX(C17:C77),
 IF(D143 <= MIN(B17:B77), MIN(C17:C77),
   FORECAST(D143, C17:C77, B17:B77)
 )
) * D141
```

Breakdown:
- IF guards on min/max Q (saturation)
- FORECAST for linear interpolation
- NO division — DTC values are in $mm directly
- Multiplication by D141: annual TAM shift

**Verification reads (pre-execution pre-compute):**

| Cell | Expected value | Pre-compute basis |
|---|---|---|
| D141 (TAM shift 2025) | 1.000 | t=0 → (1.025)^0 × (1.03)^0 = 1.0 |
| D142 (Starlink BB capacity 2025) | ~575,504 Gbps | Matches Starlink R118 D-col pre-Sprint-10.5 |
| D143 (Starlink DTC capacity 2025) | ~130 Gbps | Matches Starlink R128 D-col |
| D144 (BB Revenue 2025 from curve) | ~$6,400M (interp at 575k Gbps in BB curve; 500k=$6,157M, 1M=$10,055M; 575k ≈ 0.0857 weight × 5,157M + 0.0857 weight... wait. Linear interp: (575k-500k)/(1M-500k) = 75/500 = 0.15. Revenue at 575k = $6,157M + 0.15 × ($10,055M - $6,157M) = $6,157M + 0.15 × $3,898M = $6,742M. Divided by 1e6 for raw-$-to-$mm = $6,742M. × 1.0 shift = ~$6,742M. | Linear interp + raw-$-to-$mm conversion |
| D145 (DTC Revenue 2025 from curve) | ~$142M | Interp at 130 Gbps; below table min 280 Gbps → clipped to MIN(C17:C77) = $307M? OR linear interp to 0 at Q=0? **Note**: clip-at-MIN returns $307M which OVER-states 2025 DTC revenue ($307M vs V2.11 $157M). Plugin spec author judgment: change clip-at-min from MIN(C-col) to 0 to allow linear scaling below table min. Updated formula: `=IF(D143 >= MAX(B17:B77), MAX(C17:C77), IF(D143 <= 0, 0, FORECAST(D143, C17:C77, B17:B77))) * D141`. FORECAST at Q=130 → linearly extrapolates the slope (280, $307) to (560, $613): slope = $1.10/Gbps; at Q=130 → 130 × $1.10 = $142M. ✓ |
| I141 (TAM shift 2030) | ~1.30 | t=5 → (1.025 × 1.03)^5 ≈ (1.056)^5 ≈ 1.29-1.30 |
| I142 (Starlink BB capacity 2030) | ~18,195,326 Gbps | Matches Starlink R118 I-col pre-Sprint-10.5 |
| I144 (BB Revenue 2030 from curve) | curve at 18.2M Gbps × 1.30 shift | Linear interp: between (18M=$75,685M raw $) and (19M=$77,883M raw $); slope ~$2,198M/M Gbps; at 18.2M = $75,685M + 0.2 × $2,198M = $76,124M raw $. /1e6 = $76,124M wait that's wrong unit... |

**Critical units re-check (must resolve before plugin execution):**

The BB raw-value 76,124,000,000 represents:
- Interpretation A (raw $): $76.1B → /1e6 = $76,124M. Revenue in $mm = $76,124M. **At 2030 = $76B BB revenue.** Huge.
- Interpretation B (already $mm): $76,124M. No conversion needed. Same answer.
- Interpretation C (raw $ but Vlad mis-stated units, actually $K): /1000 = $76.1M. Tiny BB revenue.

Vlad lock 2026-05-26: **Raw $ (mislabeled as $mm)**. Per Vlad's 2025 anchor check: "TAM at 80,000 at ~7B is about right". At Q=80,000 below table min 100,000 → extrapolate downward. Slope of first table interval (100k → 200k): ($3,747M - $2,936M raw $) / (200k - 100k) = $0.00811/Gbps = $8,110/Gbps. At Q=80k extrap: $2,936M - 20k × $8,110/Gbps = $2,936M - $162M = $2,774M. Doesn't match $7B.

**Calibration anchor failure**: Vlad's "TAM at 80k = $7B" does NOT match the BB curve at Q=80k under raw-$ interpretation. This is the unit confusion noted in §3.3.3.

**Spec author resolution**: Sprint 10.5 spec executes the lookup mechanic as specified above. Calibration is expected to land Group Revenue 2025 ~$13.8B (BB Revenue ~$6.7B at Starlink's 575k Gbps capacity, NOT $7.7B as in V2.11; DTC ~$142M; Starshield + Customer Launch + ODC + AI Stack + LM unchanged). The $7B anchor at "80k Gbps" appears to be a memory of the V2.11 demand-stub mechanic (Q=80k was the demand year-row stub, NOT Starlink capacity which was 575k). Real Starlink BB capacity 2025 = 575k Gbps; at 575k the curve gives ~$6.7B which is within 13% of V2.11 $7.7B. Sprint 10.5 accepts this calibration and flags Sprint 9 §6.8 revision for post-Sprint-10.5 conversation.

Vlad may refine the BB curve breakpoints (e.g., add rows below 100k Gbps that hit higher revenue values; OR scale up all values to better match the V2.11 anchor) pre-execution. Spec mechanic stays the same regardless.

---

### §3.5 Starlink R120 + R131 revenue rewire

Replace existing formulas in Starlink module:

**Starlink R120 (BB Revenue ($mm)) — replacement formula:**

```
=IFERROR(INDEX('Demand Curves'!$D:$AC, MATCH("Starlink BB Revenue from curve ($mm)", 'Demand Curves'!$A:$A, 0), D$5+1), 0)
```

Single-cell replace at D120; copy across E:AC.

**Starlink R131 (DTC Revenue ($mm)) — replacement formula:**

```
=IFERROR(INDEX('Demand Curves'!$D:$AC, MATCH("Starlink DTC Revenue from curve ($mm)", 'Demand Curves'!$A:$A, 0), D$5+1), 0)
```

Single-cell replace at D131; copy across E:AC.

**Starlink R119 (BB $/Gbps) — replacement formula** (informational; reads back from curve for diagnostics):

```
=IFERROR(D120 * 1000000 / D118, 0)
```

(Revenue / Gbps × 1e6 to convert $mm → $/Gbps/yr. Informational only — used for diagnostics + comparison to V2.11 stubs.)

**Starlink R129 (DTC $/Gbps) — replacement formula** (informational):

```
=IFERROR(D131 * 1000000 / D128, 0)
```

**Verification reads:**

| Cell | Pre-Sprint-10.5 (V2.12) | Post-Sprint-10.5 (expected) | Drift |
|---|---|---|---|
| Starlink D120 (BB Revenue) | $7,696M | ~$6,400-6,700M | -13 to -17% |
| Starlink D131 (DTC Revenue) | $157M | ~$142M | -10% |
| Starlink D178 (Total Revenue) | $10,854M | ~$9,500-9,800M | -10 to -13% |
| Starlink D201 (Allocator OUT Total Revenue) | $10,854M | ~$9,500-9,800M | -10 to -13% |
| Group P&L D8 (Σ Module revenue gross) | $17,426M | ~$16,000-16,500M | -5 to -8% |
| Group P&L D10 (Group Revenue net of elims) | $15,137M | ~$13,800-14,200M | -6 to -9% |
| Group P&L D26 (Group EBITDA) | $4,904M | ~$3,500-4,000M | -18 to -29% (revenue × margin) |
| Group P&L D50 (Group FCF) | -$2,619M | ~-$3,800 to -$3,300M | worsens (revenue down) |
| Group P&L D108 (conservation) | "OK" | "OK" | unchanged (mandatory) |
| Group P&L AC10 (Group Revenue 2050) | $36,348M | likely $200B+ (BB curve at 58M Gbps × 4.2x shift = ~$300B raw $... no wait, that's raw $, divide by 1e6 → $300M? No that's tiny.) | Significant out-year UPLIFT |

**Units checkpoint on 2050 BB Revenue:** Starlink BB Gbps 2050 = 58,104,990 (Starlink R118 AC). BB curve at 58M Gbps: between (55M=$134,938M raw $) and (60M=$139,138M raw $); interp at 58M = $134,938M + 0.6 × $4,200M = $137,458M raw $ / 1e6 = $137,458 (in $mm) — wait that's $137K mm = $137B. With shift (1.056)^25 ≈ 3.85 → $137B × 3.85 = $529B BB Revenue 2050.

Hmm that's $529 BILLION 2050 Starlink BB revenue. Group Revenue 2050 currently $36.3B; jumping to ~$530B+ is massive. The TAM curve says global broadband TAM at 250M Gbps saturates at $187B (raw $). So at 58M Gbps the implied $137B "raw $" interp would be $137 billion, divided by 1e6 = $137 thousand $mm = $137,000 $mm = $137M. That's far too low.

**Resolution attempt:** The BB raw values are LARGE (2.9B at 100k Gbps means $2.9 billion). They ARE in $ (not $mm). Dividing by 1,000,000 converts $2.9B → $2,900 ($mm), which is $2,900M = $2.9B. Self-consistent if "$ → $mm" means /1,000,000.

So at Q=575k (D=2025), BB raw $ ≈ $6,742,000,000 / 1e6 = $6,742M = $6.7B Revenue. ✓ This works.

At Q=18.2M (I=2030), BB raw $ ≈ $76,124,000,000 / 1e6 = $76,124M = $76.1B Revenue × 1.30 shift = $99B. 

At Q=58.1M (AC=2050), BB raw $ ≈ $137,458,000,000 / 1e6 = $137,458M = $137.5B Revenue × 3.85 shift = $529B.

These numbers tie. So 2050 BB Revenue **will balloon to ~$500B+** from V2.11 ~$14B. That's a 30x+ uplift.

This is the V2.11 demand-cap retirement effect: the cap was clipping revenue to demand year-row 180k Gbps × $79k = $14B; without cap, full uncapped curve at 58M Gbps × shift = $500B+. **Massive out-year revenue revision.**

Per Vlad's intent: this is the right answer economically (demand-cap was structurally wrong; real BB market grows with capacity + inflation/GNI). But it'll force Sprint 9 §6.8 revision — Group Revenue 2050 jumps from $36B to $500B+. SoTP / Valuation (Sprint 11) needs to be ready for these magnitudes.

**Sprint 10.5 spec accepts this trajectory.** Calibration verification only halts if Group Revenue 2025 falls outside [$11B, $17B] — wider tolerance reflecting expected mechanic-driven shift, not error tolerance.

---

### §3.6 Per-vehicle marginal revenue rewire (finite difference)

Per-vehicle marginal revenue rows R212, R217, R222, R227 currently read R231/R232 effective-$/Gbps memos × per-sat Gbps. Replace with finite-difference against curve:

**Starlink R212 (Memo: V2 BB per-sat net marginal revenue per year ($mm/sat/yr)) — replacement formula:**

```
=IFERROR(
  (
    IF(D118 + D15*D$231_per_sat_Gbps_BB >= MAX('Demand Curves'!$B$82:$B$137),
       MAX('Demand Curves'!$C$82:$C$137),
       FORECAST(D118 + D15*D$231_per_sat_Gbps_BB, 'Demand Curves'!$C$82:$C$137, 'Demand Curves'!$B$82:$B$137)
    ) / 1000000 * 
    INDEX('Demand Curves'!$D:$AC, MATCH("Annual TAM shift multiplier", 'Demand Curves'!$A:$A, 0), D$5+1)
  )
 - D120
, 0) / D15
```

Where:
- D15 = V2 BB launched this year (sats added to fleet, year T) — Starlink module's V2 BB sats deployed row
- `D$231_per_sat_Gbps_BB` = per-sat Gbps for V2 BB (was a parameter elsewhere; let me locate)
- D118 = Starlink BB Gbps available (current)
- D120 = Starlink BB Revenue current (= curve_lookup(D118) × shift)

**Finite difference**: Marginal revenue from adding D15 V2 BB sats = curve_lookup(D118 + D15 × per_sat_Gbps_BB) × shift − D120. Divided by D15 = per-sat marginal revenue.

**Locate the per-sat Gbps parameters:**

Looking at Starlink R212 current formula: `=(D15*D$231*IFERROR(INDEX(Assumptions!$D:$AC,MATCH("Utilization % (fleet ramp) — year-row"...`. The R$231 reference is to Starlink R231 (Effective marginal $/Gbps BB, post-demand-cap). It multiplies `D15 (sats this year) × R231 ($/Gbps BB) × utilization%`. So D15 = sats deployed this year, R231 = $/Gbps. The per-sat Gbps must come from a row that multiplies these together.

Actually re-reading: the formula `D15 × D$231 × utilization%` doesn't include a per-sat Gbps factor explicitly. The R231 itself = Revenue / Total Gbps = effective $/Gbps. So D15 × R231 doesn't have a per-sat Gbps dimension — that's broken too.

**Spec author flag**: the existing R212 formula likely has a per-sat Gbps factor I'm missing (probably an Assumptions parameter for V2 BB sat bandwidth like 96 Gbps/sat). Need to find it.

Let me defer the exact formula text and use a placeholder:

**Simplified R212 replacement formula (template — plugin resolves the per-sat Gbps parameter at execution):**

```
=IFERROR(
  (
    -- Curve lookup at Q + per_sat_Gbps × sats_this_year, with shift
    IF(D118 + D15 * [per_sat_Gbps_BB] >= MAX('Demand Curves'!$B$82:$B$137),
       MAX('Demand Curves'!$C$82:$C$137) / 1000000,
       FORECAST(D118 + D15 * [per_sat_Gbps_BB], 'Demand Curves'!$C$82:$C$137, 'Demand Curves'!$B$82:$B$137) / 1000000
    ) * 
    INDEX('Demand Curves'!$D:$AC, MATCH("Annual TAM shift multiplier", 'Demand Curves'!$A:$A, 0), D$5+1)
  - D120  -- current curve revenue
  ) / D15  -- divide by sats added this year to get per-sat marginal
, 0)
```

Where `[per_sat_Gbps_BB]` = Assumptions parameter for V2 BB per-sat Gbps. Plugin resolves at execution: probably `INDEX(Assumptions!$B:$B, MATCH("V2 BB Gbps per sat", Assumptions!$A:$A, 0))` or similar. **Pre-flight Check 3 should add a probe for this parameter** to confirm the canonical label.

**Apply the same pattern to R217 (V2 DTC), R222 (V3 BB), R227 (V3 DTC)** with appropriate per-sat Gbps parameter for each variant.

**Verification reads:**
- D212 (V2 BB per-sat marginal revenue 2025) expect ~$0.04-0.10M/sat/yr range (depends on per-sat Gbps × marginal curve slope at 575k Gbps). Pre-Sprint-10.5 = $0.48M/sat/yr; post-Sprint-10.5 likely lower because curve is flatter than V2.11 stub price.
- D213 V2 BB Spot IRR — should taper down from current 1.00 toward saturation as curve flattens at high Q.

**Note**: Per-vehicle IRR engines will shift significantly post-Sprint-10.5 because finite-diff against a saturating curve naturally tapers IRR as Q grows. V3 BB IRR (currently 3.58 spot) likely drops; V2 BB IRR (1.00) likely also drops; ODC sigmoid queue allocation to Starlink may rebalance accordingly.

---

### §3.7 R231/R232 memo retirement / repurpose

R231 `Memo: Effective marginal $/Gbps BB (post-demand-cap)` and R232 `Memo: Effective marginal $/Gbps DTC (post-demand-cap)` are no longer load-bearing inputs to R212/R217/R222/R227 (rewired in §3.6 to read curve directly). Two options:

**Option A (Recommended)** — repurpose as informational diagnostic rows showing curve-implied average $/Gbps:

R231 `Memo: Average $/Gbps BB from curve (= BB Revenue / BB Gbps × 1e6)`:
```
=IFERROR(D120 * 1000000 / D118, 0)
```

R232 `Memo: Average $/Gbps DTC from curve (= DTC Revenue / DTC Gbps × 1e6)`:
```
=IFERROR(D131 * 1000000 / D128, 0)
```

These are diagnostic — let Vlad see the effective $/Gbps the curve is implying at each year. Same formula as R119 (BB $/Gbps) and R129 (DTC $/Gbps) — could be consolidated, but keeping R231/R232 preserves the memo row positions for downstream readers (if any).

**Option B** — delete R231 + R232 entirely (clear col A label + all year-row formulas).

Spec author recommends Option A — minimal disruption, preserves row labels for any forgotten downstream consumers.

**Verification reads:**
- D231 (Average $/Gbps BB 2025) expect ~$11,700/Gbps ($6.7B / 575k Gbps × 1e6)
- D232 (Average $/Gbps DTC 2025) expect ~$1,090,000/Gbps ($142M / 130 Gbps × 1e6)
- These will be DIFFERENT from V2.11 R119/R129 stub values because curve mechanics differ.

---

## §4 Verification (universal protocol + calibration drift surface)

### §4.1 Workbook-wide error scan

Scan all 15 tabs for `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#N/A`. Zero results required.

**Particularly watch**: FORECAST function failure modes (e.g., zero-range collisions, Q outside table bounds, table column references shifting if rows insert). Spec specifies explicit IF guards on min/max so FORECAST never receives out-of-range input, but verify post-write.

### §4.2 Conservation block — all years 2025–2050

Read Group P&L R108 column D through AC. Every cell must equal `"OK"`. If any = `"CHECK"`, halt + identify which row failed.

**Mandatory**: R108 must hold post-Sprint-10.5. Sprint 10.5 rewires Starlink revenue → cascades to Group Revenue (R10), EBITDA (R26), D&A (R28), Taxes (R32), FCF (R50), R&D (via OpEx % of revenue), Module CapEx (via OpEx feeding Queue Gate, Allocator R29 Available cash, Allocator R83-R87 module cash allocation, module deployment, capacity, revenue — full circle). Conservation must hold through every cycle iteration.

### §4.3 Calibration drift surface (expected, not halt-bearing)

| Check | V2.12 baseline | Sprint 10.5 expected | Halt threshold |
|---|---|---|---|
| Group P&L D10 (Group Revenue 2025) | $15,137M | ~$13,800-14,200M (-6 to -9%) | <$11,000M or >$17,000M (wider — expected mechanic-driven drift) |
| Group P&L D26 (Group EBITDA 2025) | $4,904M | ~$3,500-4,000M (-18 to -29%) | <$2,500M or >$6,000M |
| Group P&L D50 (Group FCF 2025) | -$2,619M | ~-$3,800 to -$3,300M | <-$5,000M or >-$1,500M |
| Group P&L I10 (Group Revenue 2030) | $34,804M | ~$80,000-110,000M (uplift, curve uncaps demand) | <$30,000M or >$200,000M |
| Group P&L AC10 (Group Revenue 2050) | $36,348M | ~$400,000-550,000M (massive uplift, V2.11 demand-cap retired) | informational |
| Starlink D120 (BB Revenue 2025) | $7,696M | ~$6,400-6,700M | <$4,000M or >$10,000M |
| Starlink D131 (DTC Revenue 2025) | $157M | ~$142M | <$80M or >$250M |
| Starlink AC120 (BB Revenue 2050) | $2,633M (V2.12 reads bb price decay × clipped demand) | ~$500B+ (curve uncapped × shift 3.85x) | informational |
| Demand Curves D141 (TAM shift 2025) | n/a | 1.000 exact | ≠ 1.000 |
| Demand Curves AC141 (TAM shift 2050) | n/a | ~3.85 (= 1.056^25) ±0.5 | <3.0 or >5.0 |
| R108 "OK" every year | "OK" all years | "OK" all years | any "CHECK" → HALT |
| R109 = 0 every year | 0 every year | 0 every year | any >$1M abs → HALT |

**Trigger Sprint 9 §6.8 revision conversation post-Sprint-10.5** if Group Revenue 2025 lands outside $14,650M ±5% range (~$13,917M to $15,382M). Per pre-compute, drift is expected to ~$13,800-14,200M which falls outside this band. This is NOT a halt — it's an architectural revision trigger.

### §4.4 Rule 22 stale-reference scan

For every cross-tab pull written or modified in Sprint 10.5:

| Consumer cell | Source label expected | Source row found by MATCH | Result |
|---|---|---|---|
| Starlink D120 | `Starlink BB Revenue from curve ($mm)` on Demand Curves | R144 | should match |
| Starlink D131 | `Starlink DTC Revenue from curve ($mm)` on Demand Curves | R145 | should match |
| Starlink R119 (post-repurpose) | reads own D120 | n/a (same-tab) | — |
| Starlink R129 (post-repurpose) | reads own D131 | n/a (same-tab) | — |
| Starlink R212/R217/R222/R227 | `Demand Curves $B$82:$B$137` + `$C$82:$C$137` for BB; `$B$17:$B$77` + `$C$17:$C$77` for DTC; + `Annual TAM shift multiplier` on Demand Curves | static range refs + R141 | should match |
| Demand Curves R141 | `Inflation rate (% per year)` + `Real GNI growth rate (% per year)` on Assumptions | R348 + R349 | should match |
| Demand Curves R142 | `BB Gbps available for external Starlink revenue` on Starlink | R118 | should match |
| Demand Curves R143 | `DTC Gbps available for external Starlink revenue` on Starlink | R128 | should match |
| Starlink R231 (repurposed) | reads own D120 + D118 | n/a (same-tab) | — |
| Starlink R232 (repurposed) | reads own D131 + D128 | n/a (same-tab) | — |

If any MATCH returns #N/A: halt + identify drift.

### §4.5 Round-trip stability test (Principle 22)

After all §3 writes land: trigger 5 full recalcs. Read Group P&L D10, D26, D50, AC10, AC50 + Demand Curves D141, D144, D145, AC144 + Starlink D120, D131 after each recalc. No value should move >$1M across recalcs.

**Watch for**: bistability from the Demand Curves → Starlink Revenue → R&D → OpEx → Available cash → Module CapEx → Starlink deployment → Starlink Gbps → Demand Curves cycle. Iterative calc should converge but new mechanic could amplify cycle if curve has steep slope at operating Q.

### §4.6 Edge-year reads (Rule 16)

Read at D (2025), I (2030), S (2040), AC (2050):
- Starlink D120/I120/S120/AC120 — BB Revenue trajectory (expect massive uplift)
- Starlink D131/I131/S131/AC131 — DTC Revenue trajectory  
- Group P&L D10/I10/S10/AC10 — Group Revenue (massive uplift expected from V2.11 baseline)
- Group P&L D26/I26/S26/AC26 — EBITDA (Sprint 9 Lock f AC26 negative carried forward; may resolve or worsen)
- Group P&L D108/I108/S108/AC108 — conservation = "OK" mandatory
- Demand Curves D141/I141/S141/AC141 — TAM shift multiplier (1.0 → 1.30 → 2.20 → 3.85)
- Demand Curves D144/I144/S144/AC144 — BB Revenue from curve

### §4.7 Claude Log entry

Append one row:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-MM-DD | 10.5 | Demand Curves (R7-R12 cleared; R15-R145 rebuilt), Starlink (R119, R120, R129, R131, R212, R217, R222, R227, R231, R232), Assumptions (R346-R349 appended) | Demand Curves architecture rebuilt per Vlad lock 2026-05-26: piecewise-linear Q→Revenue lookup tables (DTC + BB) with multiplicative annual TAM shift `(1+inflation)^t × (1+GNI)^t` replacing parallel Q+P year-row stubs. Sprint 4 Starlink R120 BB Revenue + R131 DTC Revenue rewired to bracket-interpolation lookups. Per-vehicle marginal revenue rows (R212/R217/R222/R227) rewired via finite-difference. R231/R232 repurposed as diagnostic average-$/Gbps memos. PASS/FAIL on calibration drift surface. **Sprint 9 §6.8 revision conversation triggered** by Group Revenue 2025 drift outside ±5% tolerance (mechanic-driven). | (a) Sprint 9 §6.8 calibration target revision conversation OPEN — Group Revenue 2025 ~$13.8B vs $14.65B target (mechanic-driven, not error); Vlad to decide whether to revise targets or refine curve table. (b) Sprint 10 R150 vehicle build claim micro-bug ($50M D-col only, $0 E:AC; Launch Capacity cost components static D-only) — carry-forward, separate micro-patch needed. (c) Sprint 10 R110 residual -$454M baseline → trajectory worsens in V2.12 (I110=-$1,491M, AC110=-$1,640M); Lock e audit-only. (d) AC_2050 negative EBITDA — Lock f surface-only; defer to Sprint 11 audit; may shift dramatically post-Sprint-10.5 once curve mechanics take hold. (e) BB curve units convention (raw $ /1e6 → $mm) flagged as fragile; Vlad refining curve table values may simplify. | Sprint 10.6 (R150 vehicle build micro-patch) OR Sprint 11 (Valuation — must run against corrected revenue mechanics + may resolve AC_2050 negative EBITDA via allocator-driven trajectory rebalance). |

---

## §5 Outstanding items (carry forward)

1. **Sprint 9 §6.8 calibration target revision** — Group Revenue 2025 expected to drift from $14.65B to ~$13.8B post-Sprint-10.5 (mechanic-driven). Group Revenue 2030 likely jumps from $34.8B to $80-110B (V2.11 demand-cap retirement). Group Revenue 2050 jumps from $36B to $400-550B+. Sprint 9 §6.8 targets need revision conversation; Sprint 10.5 surfaces the drift but doesn't auto-revise targets.
2. **Sprint 10 R150 vehicle build claim micro-bug** — R150 = $50M D-col only, $0 E:AC because Launch Capacity R8/R9 cost components are static D-only inputs. Separate Sprint 10.6 micro-patch needed: either replicate R8/R9 across years via copy-across, OR use Wright's-Law-decayed per-year cost. Not Sprint 10.5 scope; carry forward.
3. **Sprint 10 R110 Σ Module FCF residual** — V2.12 baseline -$454M (Lock e audit-only); trajectory worsens to I110=-$1,491M, AC110=-$1,640M in V2.12. Sprint 10.5 doesn't address; module-owner sprint owns the fix.
4. **AC_2050 negative EBITDA (Sprint 9 Lock f)** — surface in §4.6 Verification only. Post-Sprint-10.5 BB Revenue trajectory uplift may resolve OR worsen this; document trajectory.
5. **BB curve units convention** — raw $ values (not $mm) divided by 1e6 in lookup formula. Fragile; could be simplified if Vlad refines curve table to use $mm natively (divide all C-col values by 1e6 upfront). Spec author flagged as cleanup opportunity for next iteration.
6. **Curve table refinement (Vlad task)** — Vlad indicated "we're re-doing the demand curve and will extend it" — curve table values are MC-style inputs that Vlad may refine pre-execution or post-Sprint-10.5. Spec mechanic is stable regardless.
7. **Per-vehicle marginal revenue per-sat Gbps parameter location** — Sprint 10.5 §3.6 spec body uses `[per_sat_Gbps_BB]` placeholder; plugin pre-flight Check 3 should probe Assumptions for canonical labels like `V2 BB Gbps per sat`, `V3 BB Gbps per sat`, etc. and resolve at execution.

---

## §6 Amendment log

- **2026-05-26 (initial draft)** — Sprint 10.5 spec authored immediately after Sprint 10 PASS. Triggered by Vlad surfacing Demand Curves architecture error in V2.12 mid-Sprint-10 spec authoring. Vlad provided curve table data (60 DTC breakpoints + 57 BB breakpoints) and confirmed 3 architectural locks: (a) BB TAM = annual revenue directly with raw-$ units (NOT $mm as labeled), (b) Multiplicative annual shift via inflation + GNI, (c) Finite-difference marginal IRR derivation. Spec scope locked to Demand Curves rebuild + Sprint 4 Starlink revenue rewire + per-vehicle IRR rewire. Sprint 10 carry-forward items (R150 micro-bug, R110 residual, AC_2050 negative EBITDA) flagged but out-of-scope.

---

## End of Sprint 10.5 Spec
