# Sprint 0 — Assumptions Tab + Workbook Standards

**Sprint type**: Foundational. First cell-write of the rebuild v2.
**Execution context**: Excel Claude plugin chat, operating on an already-open Excel workbook that Vlad has pre-named via Save-As. The workbook has one empty sheet (any default name).
**Target workbook**: `SpaceX Model V2.1.xlsx` (Vlad pre-named; plugin operates on the open file).
**Day budget**: 1 day.

**This spec is fully self-contained.** It references no external XLSX, no constitutional MDs, no other files. Every input value the plugin needs to write is in §3.6 below. Every rule the plugin needs to follow is in §1 below. Every verification anchor is in §4 below.

**The plugin does NOT save the workbook.** Vlad handles all saving (initial Save-As pre-execution; intermediate + final saves during/after execution). The plugin executes cell writes against the live workbook session.

The plugin's first cell-write does NOT happen until: (a) the Rule Compliance Preamble in §1 is confirmed box-by-box, (b) Vlad-side pre-execution setup in §1.5 is complete, (c) the pre-flight checks in §3.0 pass.

---

## §1 — Rule Compliance Preamble (mandatory)

- [x] **Rule 1** (one concept per write) — Section structure separates: tab creation, year header writes (row 4), year-offset writes (row 5), Assumptions column-A labels, column-B Base Case values, column-C notes, column D–AC year-row values, columns AG–AJ MC fields, formatting. Each is a discrete write block.
- [x] **Rule 3 / 23** (formula pattern) — Sprint 0 writes no formulas. Year header row 4 and year-offset row 5 are **literal integers**, never `=D5+1` chains. No `OFFSET()` anywhere.
- [x] **Rule 4** (verification gate) — §4 specifies read-back cells + expected values for the locked anchors (starting cash, F9 fleet, F9 price, Mars/Moon R&D, Starshield decay, Starshield rev/Gbps, ARPUs, IPO, sigmoid k, Forward weight, year-row trajectory samples, and the row-4/row-5 standards on every active tab).
- [x] **Rule 6** (inline formulas) — N/A this sprint (no formulas written). All values are hardcoded constants from §3.6.
- [x] **Rule 10** (no row insertions) — N/A (fresh workbook, nothing to insert above). All writes append top-down per §3.6.
- [x] **Rule 11** (touch points) — Assumptions is a leaf source this sprint; nothing reads from it yet. Sprint 1+ wires reads against canonical labels.
- [x] **Rule 12** (label-based cross-tab refs) — N/A this sprint. No cross-tab references written.
- [x] **Rule 13** (vending-machine test) — N/A (no module body content this sprint).
- [x] **Rule 14** (no hardcoded constants in formulas) — N/A (no formulas). Assumptions is *where* the constants live, satisfying the rule's spirit.
- [x] **Rule 15** (sanity check halt thresholds) — §4.3 halt conditions explicit and quantitative.
- [x] **Rule 19** (save-as) — Target workbook `SpaceX Model V2.1.xlsx` named in header. **Vlad performs all saves** (capability constraint: Excel plugin operates on the currently-open workbook). Plugin verifies filename in §3.0 pre-flight check #1.
- [x] **Rule 22** (stale-ref scan) — Trivially satisfied (no cross-tab refs to scan). Re-engages Sprint 1+.

Architecture compliance (load-bearing items this sprint touches):
- [x] Module P&L vending-machine framing — N/A this sprint.
- [x] Per-sat / per-launch marginal IRR engine — N/A directly, but Sprint 0 populates the inputs that drive it (Forward weight = 0.7, Sigmoid k = 2, design lives = 5, Mars %, Mars floor, Starting cash, IPO, Vehicle build lead time = 2).
- [x] Allocator OUT contract — N/A this sprint; 11 canonical labels referenced Sprint 1+.
- [x] Year-offset helper row + year header — **CORE OUTPUT.** Pre-staged on every year-column tab per §3.2.
- [x] ZERO `OFFSET()` formulas — N/A (no formulas this sprint). Standing principle re-asserted.

All boxes ticked or marked N/A with justification. **If any box is unchecked, plugin halts and pushes back.** Otherwise proceed.

---

## §1.5 — Pre-execution setup (Vlad-side, before plugin chat starts)

Sprint 0 is the first cell-write of the rebuild. The Excel plugin has capability constraints that Vlad addresses outside the plugin chat:

### §1.5.1 — Save-as the target workbook (plugin cannot save-as)

1. Open a new blank Excel workbook (`File → New → Blank Workbook`).
2. `File → Save As` → name it `SpaceX Model V2.1.xlsx`.
3. The workbook now has exactly one sheet (whatever the default new sheet was named — `Sheet1`, `Sheet`, locale-dependent — that's fine), content-empty.
4. Leave the workbook open in Excel; the plugin will operate on it.

### §1.5.2 — Saving during + after execution

The plugin does not issue save commands. Vlad saves:
- After the plugin reports verification PASS (recommended: save to lock the Sprint 0 baseline).
- Whenever convenient mid-execution.

### §1.5.3 — Send the kickoff prompt with setup confirmation

Append this confirmation block to the kickoff prompt:

```
Pre-execution setup confirmed (per Sprint_0_Spec.md §1.5):
- Target workbook saved-as: `SpaceX Model V2.1.xlsx`, open in Excel plugin.
- I (Vlad) handle all saving; plugin must not issue save commands.
```

Plugin reads this confirmation as part of its §3.0 pre-flight.

---

## §2 — Framing

**Why this sprint.** The rebuild needs a single source of truth for every input before any downstream calculation lands. Sprint 0 sets the discipline: every behavioural assumption lives on the Assumptions tab with a Base Case, an MC range, and a distribution type, populated at creation. The locked input set is inlined in §3.6 — 300 rows across 11 sections.

**What this sprint produces.** A workbook with:
1. 14 tabs in locked sheet order (§3.1).
2. Year header (row 4, hardcoded integers D=2025…AC=2050) and year-offset helper (row 5, hardcoded integers D=0…AC=25) on every tab with year columns.
3. Assumptions tab fully populated per §3.6 — 300 rows across 11 sections, every input with Base Case + MC range + distribution + notes.
4. Claude Log tab seeded with header row + Sprint 0 entry.

**What this sprint does NOT produce.** Any formula. Any cross-tab reference. Any module body content. The other 12 tabs are skeletons — sheet exists, year header + offset row written, otherwise blank. No plugin-issued saves.

---

## §3 — Scope

### §3.0 — Pre-flight checks (plugin runs BEFORE any cell writes)

1. **Confirm target workbook is open and named correctly**: the open workbook's filename matches `SpaceX Model V2.1.xlsx`. If different → halt, push back to Vlad to complete §1.5.1.
2. **Confirm workbook starting state is content-empty**: workbook has exactly one sheet (any name), that sheet has zero used range (no cells with content, formulas, or named ranges), no charts, no embedded objects. If multiple sheets or any content → halt, report what's there, push back.
3. **Confirm kickoff prompt contained the §1.5.3 setup confirmation block** — Vlad has acknowledged "I handle all saving; plugin must not issue save commands." If missing → halt, ask Vlad to re-send kickoff with confirmation.

### §3.1 — Sheet renaming + tab creation

The open workbook has one sheet (locale-dependent default name). Rename it to `Assumptions`. Then create the remaining 13 tabs after `Assumptions`, in exactly this order, with these exact names (case, spacing, punctuation matter):

1. `Assumptions` *(renamed from default sheet)*
2. `Allocator`
3. `Launch Capacity`
4. `Customer Launch`
5. `Starlink`
6. `Starlink Capacity`
7. `ODC`
8. `AI Stack`
9. `Lunar Mars`
10. `Group P&L`
11. `OpEx`
12. `CapEx`
13. `Valuation`
14. `Claude Log`

Verify each tab name is exact before proceeding. Misnaming `Group P&L` as `Group P_L` or `Customer Launch` as `Customer_Launch` breaks every downstream cross-tab reference.

### §3.2 — Year header + year-offset helper row (every year-column tab)

On tabs 1–13 (every tab except `Claude Log`), write:

- **Row 4 — year header**: D4=2025, E4=2026, F4=2027, …, AC4=2050. **Literal integers**, not formulas. 26 cells per tab × 13 tabs = 338 cells.
- **Row 5 — year-offset helper**: D5=0, E5=1, F5=2, …, AC5=25. **Literal integers**, not formulas. 26 × 13 = 338 cells.

**Write structure (Rule 1):** for each tab, write row 4 in one operation, then row 5 in a second separate operation. Do not combine. Apply bold + bottom-border formatting to row 4 (year header) and a subtle grey fill to row 5 (year-offset helper) so structural rows are visually distinct from data rows.

### §3.3 — Assumptions tab build (driven by inline §3.6 below)

Walk the §3.6 row-by-row table top-to-bottom. For each row, write to the corresponding row on the Assumptions tab per this column convention:

**Column layout (cols A through AJ):**
- A — section header / input label
- B — Base Case (single-value inputs only)
- C — notes / source one-liner
- D–AC — year-row values (year-row inputs only; D=2025, E=2026, …, AC=2050)
- AG — MC Min
- AH — MC Max
- AI — MC Distribution (`triangle` / `lognormal` / `uniform` / `discrete` / `triangle-yearrow` / `fixed-yearrow` / `fixed`)
- AJ — MC notes / rationale

Columns AD, AE, AF are intentionally blank (visual gap between year-row and MC columns).

**Row roles:**
- **`SECT` rows** (11 — Global, Allocator, Capacity, Customer Launch, Starlink, ODC, AI Stack, Lunar Mars, OpEx, CapEx, Valuation) — white-on-charcoal fill, bold, label at column A only.
- **`SUB` rows** (47 subsection headers, label starts with `▸`) — italic, light grey fill, label at column A only.
- **`VAL` rows** (211 single-value inputs) — column A label + B value + C note + AG–AJ MC fields. D–AC blank.
- **`YR` rows** (31 year-row inputs) — column A label + C note + D–AC year values + AG–AJ MC fields. B blank.

**For each input row:**
1. Write column-A label.
2. If `VAL`: write Base Case to column B; leave D–AC blank.
3. If `YR`: write each year's value to D through AC as static numbers (no formulas).
4. Write notes to column C.
5. Write MC Min to AG, MC Max to AH, MC Distribution to AI, MC notes to AJ.
6. Apply light yellow fill to AG:AJ when distribution ≠ `fixed`.

**Per Principle 18 (LOAD-BEARING):** every input has its MC range populated at creation. If §3.6 lists a row without MC range and distribution ≠ `fixed`, plugin halts and reports the row.

**Pacing**: don't attempt all 300 rows in one massive operation. Walk section by section (11 sections); after each section, read back the last input row to confirm column-A label and column-B / D–AC values landed as expected. Catch issues early.

### §3.4 — Claude Log tab seeding

`Claude Log` tab — no year columns. Header row at row 1, in this exact column layout:

| Col | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| Row 1 | Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |

Apply bold to row 1, bottom border. The Sprint 0 entry at row 2 is written **after** §4 verification passes — see §5.

### §3.5 — Saving (Vlad's job, not the plugin's)

The plugin does not save. After all writes complete and verification reports PASS, Vlad saves the workbook in Excel (`Ctrl+S` / `Cmd+S`). Verification reads cells from the live workbook session, not from the saved file — no save required for verification to run.

### §3.6 — Inline Build Plan (300 rows — the row-by-row driver)

The plugin walks this table top-to-bottom and writes to the Assumptions tab per §3.3 conventions.

**Row format**: `R{row} | type | label | base | notes | mc_min | mc_max | mc_dist | mc_notes`. Year-row inputs (`YR`) have years appended below the main line in `YEAR=value` pairs.

```
R2 | SECT | §1 GLOBAL |  |  |  |  |  | 
R3 | VAL | Tax rate (corporate, US federal + state blended) | 0.21 | Standard US corporate rate; Q4'25 confirms. | 0.18 | 0.27 | triangle | MC range covers blue-state vs Trump-era tax reform variability
R4 | VAL | TAM inflation rate (annual) | 0.025 | TAM growth; industry standard. V30.5 R56 + Q4'25 confirms. | 0.01 | 0.05 | triangle | MC range per Q4'25 Valuation Inputs
R5 | VAL | GNI per capita growth rate (annual) | 0.03 | Used in Starlink demand-curve scaling. | 0.01 | 0.06 | triangle | 
R6 | SECT | §2 ALLOCATOR |  |  |  |  |  | 
R7 | SUB | ▸ Cash pool boundary inputs |  |  |  |  |  | 
R8 | VAL | Starting cash position EoY 2024 ($mm) | 5000 | Q4'25 anchored ($4.70B rounded). V30.5 had $20B — corrected. | 3000 | 7000 | triangle | Q4'25 Valuation Inputs central was within this range
R9 | VAL | IPO injection amount ($mm) | 30000 | Q4'25 Valuation Inputs R31 central $40B; using $30B as Vlad-locked Base Case. | 15000 | 60000 | lognormal | Q4'25 spread; tail upside is meaningful for terminal valuation
R10 | VAL | IPO injection year | 2027 | Vlad-locked. | 2026 | 2028 | discrete | Q4'25 had 2027/2028 split; discrete sample
R11 | SUB | ▸ Moon/Mars strategic carve-out (Vlad-confirmed MC-variable) |  |  |  |  |  | 
R12 | VAL | Mars carve-out % of prior-year Group FCF | 0.15 | Spec 06+07 stub. Vlad lock 2026-05-19: central uncertainty on how much SpaceX dedicates to Mars vs terrestrial IRR lines. MC-WIDE. | 0.03 | 0.35 | triangle | Wide range — Vlad: 'we don't know how much they'll dedicate'
R13 | VAL | Mars carve-out floor ($mm/yr) | 1000 | Floor below which carve-out doesn't drop even if prior FCF is small. | 500 | 2500 | triangle | MC-variable
R14 | VAL | Mars carve-out uses prior-year FCF (0/1) | 1 | 1 = prior year (breaks circularity per Principle 22). Structural input. |  |  | fixed | 
R15 | SUB | ▸ IRR engine + sigmoid blend parameters |  |  |  |  |  | 
R16 | VAL | Sigmoid IRR-blend exponent k | 2 | Spec 09 §2.1. Default k=2 across all sigmoid queues. | 1 | 3 | triangle | MC tunes allocator concentration vs diversification
R17 | VAL | Forward IRR weight w (Blended = (1-w)·Spot + w·Forward) | 0.7 | Spec 09 §2.10 unified. V30.5 B82 = 0.7. Same value used at module + vehicle level. | 0.5 | 0.85 | triangle | MC tunes forward-looking vs current-period weight
R18 | VAL | Forward IRR look-ahead horizon (years) | 2 | Y+2 throughout. Spec 09 kept; Y+5 not introduced. |  |  | fixed | Structural
R19 | VAL | MFW-IRR — Starlink economic life N (years) | 5 | Per-vehicle marginal IRR window. Sat useful life. | 4 | 7 | triangle | 
R20 | VAL | MFW-IRR — ODC economic life N (years) | 5 | Per-sat marginal IRR window. Compute hardware life. | 4 | 7 | triangle | 
R21 | VAL | MFW-IRR — AI Stack economic life N (years) | 5 | Per-product marginal IRR window. | 3 | 7 | triangle | 
R22 | VAL | MFW-IRR — Customer Launch economic life clamp MIN (years) | 1 | Lower bound on endogenous N (cadence × lifetime reuses). |  |  | fixed | 
R23 | VAL | MFW-IRR — Customer Launch economic life clamp MAX (years) | 10 | Upper bound on endogenous N. |  |  | fixed | 
R24 | SUB | ▸ Vehicle build claim (Spec 09 architecture) |  |  |  |  |  | 
R25 | VAL | Vehicle build claim toggle (0=legacy mode, 1=forward-demand-sized non-module claim) | 1 | Spec 09 architecture. Locked = 1. |  |  | fixed | Structural
R26 | VAL | Vehicle build lead time (years) | 2 | Matches Forward IRR Y+2 horizon. | 1 | 3 | discrete | 
R27 | VAL | Launches per Starship vehicle per year (cadence × variant blend, used for sizing) | 24 | Spec 09 stub. ~30 cadence × ~80% variant blend. | 18 | 36 | triangle | 
R28 | VAL | Vehicle masked-demand large default (sats; effectively uncapped) | 1000000 | Spec 09 mechanic. Vehicle eligibility binds at pool sizing, not internal ask. |  |  | fixed | Structural
R29 | VAL | Forward aggregate kg demand growth cap (× current capacity) | 2 | Cap on year-over-year demand growth used to size vehicle build claim. | 1.5 | 3 | triangle | 
R30 | SECT | §3 CAPACITY (Starship + F9) |  |  |  |  |  | 
R31 | SUB | ▸ Starship vehicle physical + cost parameters |  |  |  |  |  | 
R32 | VAL | Super Heavy manufacturing cost ($mm/unit, base year) | 35.1 | Reusability matrix anchor. Wright's Law base. | 25 | 45 | triangle | 
R33 | VAL | Starship 2nd-stage manufacturing cost ($mm/unit, base) | 23.4 | Reusability matrix anchor. | 18 | 30 | triangle | 
R34 | VAL | Ship refurb % of manufacturing | 0.02 | Per-reuse refurb cost. | 0.01 | 0.05 | triangle | 
R35 | VAL | Payload — booster-only mode (kg-to-LEO) | 150000 | Expendable ship config. Higher because no landing margin. | 130000 | 200000 | triangle | Q4'25 Valuation Inputs R19 central 187K — covers MC
R36 | VAL | Payload — fully reusable mode (kg-to-LEO) | 100000 | Reusable both stages. | 80000 | 150000 | triangle | 
R37 | VAL | Lifetime reuses per ship (cap) | 30 | Ship useful life cap. | 20 | 50 | triangle | 
R38 | VAL | Manufacturing learning rate (per doubling of cum units) | 0.1 | 10% per doubling. Q4'25 Valuation Inputs R18 central 0.145. | 0.05 | 0.2 | triangle | 
R39 | SUB | ▸ Starship cadence (Wright's Law on cum upmass) |  |  |  |  |  | 
R40 | VAL | Base turnaround time per booster (years/flight) | 1 | 2025 starting point. | 0.8 | 1.5 | triangle | 
R41 | VAL | WL learning rate — turnaround vs cum upmass doubling | 0.145 | Legacy model midpoint. Q4'25 confirms. | 0.05 | 0.25 | triangle | Q4'25 Valuation Inputs R18 range
R42 | VAL | Anchor year for cum-upmass Wright's Law | 2025 | Anchor year for the doublings count. |  |  | fixed | 
R43 | VAL | Cadence ceiling (flights/booster/year) | 60 | Physical refly ceiling at full maturity. | 40 | 100 | triangle | 
R44 | VAL | Max annual production growth rate (multiplier) | 2 | Mfg ceiling (×2/yr max). Q4'25 R27 central 2.5x. | 1.5 | 4 | triangle | 
R45 | SUB | ▸ Starship time-varying inputs (year-rows) |  |  |  |  |  | 
R46 | YR | Variant mix (% fully reusable) |  | Ramp to 95% by 2035. Tech readiness signal — stays exogenous (Sprint 7.5 confirmed). |  |  | fixed-yearrow | Tech-readiness curve
  YEARS: 2025=0, 2026=0.05, 2027=0.15, 2028=0.25, 2029=0.45, 2030=0.7, 2031=0.8, 2032=0.85, 2033=0.9, 2034=0.92, 2035=0.95, 2036=0.95, 2037=0.95, 2038=0.95, 2039=0.95, 2040=0.95, 2041=0.95, 2042=0.95, 2043=0.95, 2044=0.95, 2045=0.95, 2046=0.95, 2047=0.95, 2048=0.95, 2049=0.95, 2050=0.95
R47 | YR | Lifetime reuses per booster (year cap) |  | Ramps 5 → 100 as reliability matures. |  |  | fixed-yearrow | 
  YEARS: 2025=5, 2026=8, 2027=12, 2028=18, 2029=25, 2030=30, 2031=35, 2032=42, 2033=50, 2034=58, 2035=65, 2036=70, 2037=75, 2038=80, 2039=85, 2040=90, 2041=92, 2042=94, 2043=96, 2044=98, 2045=100, 2046=100, 2047=100, 2048=100, 2049=100, 2050=100
R48 | SUB | ▸ Falcon 9 physical + cost parameters |  |  |  |  |  | 
R49 | VAL | F9 booster (1st stage) mfg cost ($mm/unit) | 30 | 60% of total per reusability matrix source notes. | 25 | 35 | triangle | 
R50 | VAL | F9 2nd stage mfg cost ($mm/unit) | 10 | Expendable each flight. | 8 | 13 | triangle | 
R51 | VAL | F9 fairing cost net of 75% recovery ($mm/flight) | 1.25 | $5M × 25% non-recovered. | 1 | 2 | triangle | 
R52 | VAL | F9 per-launch ops cost ($mm) | 5 | Range, propellant, recovery. | 3 | 8 | triangle | 
R53 | VAL | F9 booster refurb % of mfg | 0.03 | Reusability matrix. | 0.02 | 0.05 | triangle | 
R54 | VAL | F9 payload to LEO (kg) | 22800 | Block 5 advertised. |  |  | fixed | Disclosed
R55 | VAL | F9 lifetime reuses per booster | 50 | Block 5 demonstrated ~30, theoretical 100+. | 30 | 100 | triangle | 
R56 | VAL | F9 Wright's Law mfg learning rate | 0.02 | Mature production line; minimal further learning. | 0 | 0.05 | triangle | 
R57 | VAL | F9 cadence per booster (flights/year, flat) | 12 | F9 past learning curve. | 10 | 15 | triangle | 
R58 | VAL | F9 base booster build rate (boosters/year, pre-V3-trigger) | 8 | Q4'25 had 17 manufactured in 2025 — but that's pre-decay; this is build floor. | 6 | 10 | triangle | 
R59 | VAL | V3 Starlink launch trigger year | 2027 | V3 heavy sats require Starship → F9 demand evaporates. | 2026 | 2028 | discrete | 
R60 | VAL | F9 build-rate decay window (years) | 8 | Linear decay over 8 yrs post-trigger. | 6 | 12 | triangle | 
R61 | VAL | F9 starting fleet at 2025 SoY (boosters) | 28 | Q4'25 Earth R29 anchored. V30.5 had 24 — corrected. |  |  | fixed | Historical anchor
R62 | SECT | §4 CUSTOMER LAUNCH |  |  |  |  |  | 
R63 | YR | F9 customer launch price ($mm/launch) — 2025 anchor |  | Q4'25 Earth R132 anchored at $111M. V30.5 had $67M — corrected. Year-row with -3%/yr decline. |  |  | fixed-yearrow | Anchored to Q4'25; declines at 3%/yr
  YEARS: 2025=111, 2026=107.67, 2027=104.44, 2028=101.3, 2029=98.26, 2030=95.31, 2031=92.45, 2032=89.68, 2033=87, 2034=84.39, 2035=81.86, 2036=79.4, 2037=77.02, 2038=74.71, 2039=72.47, 2040=70.29, 2041=68.18, 2042=66.13, 2043=64.15, 2044=62.22, 2045=60.36, 2046=58.55, 2047=56.79, 2048=55.09, 2049=53.43, 2050=51.83
R64 | YR | Starship customer launch price ($mm/launch) — year-row |  | Starts at $100M in 2027, declines 8%/yr (V30.5 R196 trajectory). |  |  | fixed-yearrow | Starts 2027, 8%/yr deflation
  YEARS: 2025=0, 2026=0, 2027=100, 2028=92, 2029=84.64, 2030=77.87, 2031=71.64, 2032=65.91, 2033=60.64, 2034=55.79, 2035=51.32, 2036=47.21, 2037=43.44, 2038=39.96, 2039=36.77, 2040=33.83, 2041=31.13, 2042=28.64, 2043=26.35, 2044=24.24, 2045=22.3, 2046=20.52, 2047=18.88, 2048=17.37, 2049=15.98, 2050=14.7
R65 | YR | Commercial launch market size ($mm/year) — year-row |  | $8B base 2025, 8% annual growth. |  |  | fixed-yearrow | $8B + 8%/yr growth
  YEARS: 2025=8000, 2026=8640, 2027=9331.2, 2028=10077.7, 2029=10883.9, 2030=11754.6, 2031=12695, 2032=13710.6, 2033=14807.4, 2034=15992, 2035=17271.4, 2036=18653.1, 2037=20145.4, 2038=21757, 2039=23497.5, 2040=25377.4, 2041=27407.5, 2042=29600.1, 2043=31968.2, 2044=34525.6, 2045=37287.7, 2046=40270.7, 2047=43492.3, 2048=46971.7, 2049=50729.4, 2050=54787.8
R66 | YR | Government launch market size ($mm/year) — year-row |  | $4B base 2025, 5% annual growth. |  |  | fixed-yearrow | $4B + 5%/yr growth
  YEARS: 2025=4000, 2026=4200, 2027=4410, 2028=4630.5, 2029=4862.02, 2030=5105.13, 2031=5360.38, 2032=5628.4, 2033=5909.82, 2034=6205.31, 2035=6515.58, 2036=6841.36, 2037=7183.43, 2038=7542.6, 2039=7919.73, 2040=8315.71, 2041=8731.5, 2042=9168.07, 2043=9626.48, 2044=10107.8, 2045=10613.2, 2046=11143.9, 2047=11701, 2048=12286.1, 2049=12900.4, 2050=13545.4
R67 | YR | SpaceX commercial market share % — year-row |  | 2025: 70% → 2040: 80% (linear glide). |  |  | fixed-yearrow | 
  YEARS: 2025=0.7, 2026=0.7067, 2027=0.7133, 2028=0.72, 2029=0.7267, 2030=0.7333, 2031=0.74, 2032=0.7467, 2033=0.7533, 2034=0.76, 2035=0.7667, 2036=0.7733, 2037=0.78, 2038=0.7867, 2039=0.7933, 2040=0.8, 2041=0.8, 2042=0.8, 2043=0.8, 2044=0.8, 2045=0.8, 2046=0.8, 2047=0.8, 2048=0.8, 2049=0.8, 2050=0.8
R68 | YR | SpaceX government market share % — year-row |  | 2025: 90% → 2040: 80% (linear decline). |  |  | fixed-yearrow | 
  YEARS: 2025=0.9, 2026=0.8933, 2027=0.8867, 2028=0.88, 2029=0.8733, 2030=0.8667, 2031=0.86, 2032=0.8533, 2033=0.8467, 2034=0.84, 2035=0.8333, 2036=0.8267, 2037=0.82, 2038=0.8133, 2039=0.8067, 2040=0.8, 2041=0.8, 2042=0.8, 2043=0.8, 2044=0.8, 2045=0.8, 2046=0.8, 2047=0.8, 2048=0.8, 2049=0.8, 2050=0.8
R69 | VAL | Launch insurance % of external revenue | 0.05 | 5% insurance on commercial launches. | 0.03 | 0.08 | triangle | 
R70 | VAL | Launch other COGS % of external revenue | 0.02 | Catch-all 2%. | 0.01 | 0.04 | triangle | 
R71 | VAL | Customer Launch depreciation useful life (years) | 5 | Spec 02 stub. | 4 | 7 | triangle | 
R72 | SECT | §5 STARLINK |  |  |  |  |  | 
R73 | SUB | ▸ Satellite physical |  |  |  |  |  | 
R74 | VAL | V2 Mini Mass (kg) | 575 | Disclosed. |  |  | fixed | Hard anchor
R75 | VAL | V3 Mass (kg) | 2000 | V3 estimated. | 1800 | 2200 | triangle | 
R76 | VAL | V2 Mini Bandwidth per Sat — BB (Gbps) | 96 | Disclosed. |  |  | fixed | Hard anchor
R77 | VAL | V2 Mini Bandwidth per Sat — DTC (Gbps) | 0.2 | Slim slice for direct-to-cell. Wide MC. | 0.1 | 5 | triangle | 
R78 | VAL | V3 BB Bandwidth per Sat — base year (Gbps) | 1000 | V3 design target. Speculative. | 500 | 2000 | triangle | 
R79 | VAL | V3 DTC Bandwidth per Sat (Gbps) | 2.75 | V3 DTC design. | 1 | 8 | triangle | 
R80 | VAL | Satellite useful life — V2 Mini (years) | 5 | Standard LEO sat life. | 4 | 6 | triangle | 
R81 | VAL | Satellite useful life — V3 (years) | 5 | Same useful life assumption. | 4 | 7 | triangle | 
R82 | VAL | CapEx Lag (years) | 1 | Year between mfg CapEx and on-orbit deploy. |  |  | fixed | 
R83 | SUB | ▸ Wright's Law parameters |  |  |  |  |  | 
R84 | VAL | Satellite cost per kg — base year ($/kg) | 650 | V2 unit cost / mass. Q4'25 confirms $643.50 in 2025. | 500 | 800 | triangle | 
R85 | VAL | Satellite cost per kg — learning rate | 0.05 | 5% per doubling. | 0.03 | 0.17 | triangle | Q4'25 wide range
R86 | VAL | V3 bandwidth per sat — learning rate | 0.05 | Bandwidth learning. | 0.03 | 0.17 | triangle | 
R87 | VAL | Cumulative sats at base year (end-2024) | 7486 | Mach33 tracking anchor. |  |  | fixed | Historical
R88 | VAL | Satellite cost floor ($/kg) | 400 | Irreducible mfg cost. | 300 | 500 | triangle | 
R89 | VAL | V3 bandwidth cap (Gbps) | 5000 | Physical bandwidth ceiling. | 3000 | 7000 | triangle | 
R90 | VAL | V2 Mini cost per kg — base year ($/kg) | 650 | Same as V3 base (shared production line). | 500 | 800 | triangle | 
R91 | VAL | V2 Mini cost per kg — learning rate | 0.05 | Wright's Law. | 0.03 | 0.1 | triangle | 
R92 | VAL | V2 Mini cost floor ($/kg) | 400 | Symmetric with V3. | 300 | 500 | triangle | 
R93 | SUB | ▸ Starshield (Vlad-corrected from Q4'25) |  |  |  |  |  | 
R94 | VAL | Starshield Reserved % — start | 0.0257 | 2.57% of bandwidth reserved 2025. | 0.015 | 0.04 | triangle | 
R95 | VAL | Starshield Reserved % — floor | 0.0001 | Decays toward 0.01%. | 5e-05 | 0.005 | triangle | 
R96 | VAL | Starshield Reserved % — decay rate | 0.25 | Q4'25 Valuation Inputs R30 = 0.25. V30.5 had 1.0 — CORRECTED. | 0.15 | 0.4 | triangle | Q4'25 anchored
R97 | VAL | Starshield Rev per Gbps — base year ($/Gbps) | 164699 | Q4'25 Earth R120 anchored. V30.5 had $167,421 — small correction. | 120000 | 220000 | triangle | 
R98 | VAL | Starshield Rev per Gbps — decay rate | 0.05 | Price compression. | 0.03 | 0.1 | triangle | 
R99 | SUB | ▸ Depreciation parameters |  |  |  |  |  | 
R100 | VAL | Satellite Dep per kg — base year ($/kg/yr) | 128.8 | Q4'25 R194 confirms. = $650/kg × annual depreciation rate. | 110 | 150 | triangle | 
R101 | VAL | Satellite Dep per kg — annual decay rate | 0.01 | Annual decline in dep rate. | 0.005 | 0.02 | triangle | 
R102 | VAL | Facility CapEx per satellite — base year ($) | 90650 | Per-sat ground-segment / facility allocation. Q4'25 R251 confirms. | 70000 | 120000 | triangle | 
R103 | VAL | Facility CapEx — learning rate | 0.1 | 10% per doubling. | 0.05 | 0.15 | triangle | 
R104 | SUB | ▸ Constellation opening balances (Mach33 historical anchors — hard) |  |  |  |  |  | 
R105 | VAL | V2 Mini BB Active Sats — end-2025 | 5246 | Mach33 Starlink tracking. Hard anchor. |  |  | fixed | Historical
R106 | VAL | V2 Mini DTC Active Sats — end-2025 | 650 | Mach33 Starlink tracking. Hard anchor. |  |  | fixed | Historical
R107 | VAL | V2 Mini BB Bandwidth — end-2025 (Gbps) | 503616 |  |  |  | fixed | Derived from hard anchors
R108 | VAL | V2 Mini DTC Bandwidth — end-2025 (Gbps) | 1936 | Derived. |  |  | fixed | Derived from hard anchors
R109 | VAL | Legacy V1/V1.5 Bandwidth — end-2025 (Gbps) | 71888 | Pre-V2 residual fleet. |  |  | fixed | Historical
R110 | VAL | V2 Mini BB Sats Launched 2025 | 2987 | Historical actual. |  |  | fixed | Historical
R111 | VAL | V2 Mini DTC Sats Launched 2025 | 182 | Historical actual. |  |  | fixed | Historical
R112 | VAL | V3 BB Sats Launched 2025 | 0 | Starship not yet operational. |  |  | fixed | Historical
R113 | VAL | V3 DTC Sats Launched 2025 | 0 | Starship not yet operational. |  |  | fixed | Historical
R114 | YR | Legacy V1/V1.5 Active Bandwidth (Gbps, year-row runoff) |  | Straight-line 4-year runoff. |  |  | fixed-yearrow | 
  YEARS: 2025=71888, 2026=53916, 2027=35944, 2028=17972, 2029=0, 2030=0, 2031=0, 2032=0, 2033=0, 2034=0, 2035=0, 2036=0, 2037=0, 2038=0, 2039=0, 2040=0, 2041=0, 2042=0, 2043=0, 2044=0, 2045=0, 2046=0, 2047=0, 2048=0, 2049=0, 2050=0
R115 | VAL | V2 Mini BB historical baseline (SoY 2025) | 5246 | Spec 09 input for V2 historical retirement. |  |  | fixed | Historical
R116 | VAL | V2 Mini DTC historical baseline (SoY 2025) | 650 | Spec 09 input for V2 historical retirement. |  |  | fixed | Historical
R117 | SUB | ▸ Deorbit parameters |  |  |  |  |  | 
R118 | VAL | V2 Mini BB Deorbit Lag (years) | 5 | Useful life. | 4 | 6 | triangle | 
R119 | VAL | V3 BB Deorbit Lag (years) | 5 | Same. | 4 | 7 | triangle | 
R120 | VAL | V2 Mini DTC Deorbit Lag (years) | 5 | Symmetric. | 4 | 6 | triangle | 
R121 | VAL | V3 DTC Deorbit Lag (years) | 5 | Symmetric. | 4 | 7 | triangle | 
R122 | VAL | Bandwidth Removed per Deorbited V2 Mini BB Sat (Gbps) | 96 | Matches V2 BB capacity. |  |  | fixed | Derived
R123 | VAL | Bandwidth Removed per Deorbited V2 Mini DTC Sat (Gbps) | 2.978 | Blended V2 DTC. |  |  | fixed | Derived
R124 | VAL | Bandwidth Removed per Deorbited V3 BB Sat (Gbps) | 1000 | Matches V3 BB design. |  |  | fixed | Derived
R125 | VAL | Bandwidth Removed per Deorbited V3 DTC Sat (Gbps) | 5 | Matches V3 DTC design. |  |  | fixed | Derived
R126 | SUB | ▸ Subscribers + ARPU + Terminals |  |  |  |  |  | 
R127 | VAL | Starting BoY 2025 subscribers (millions) | 5 | Mid-2024 disclosed. | 3 | 8 | triangle | 
R128 | YR | Broadband ARPU ($/sub/mo, year-row) |  | Glide path 2025: $100 → 2030: $75, flat after. |  |  | fixed-yearrow | 
  YEARS: 2025=100, 2026=95, 2027=90, 2028=85, 2029=80, 2030=75, 2031=75, 2032=75, 2033=75, 2034=75, 2035=75, 2036=75, 2037=75, 2038=75, 2039=75, 2040=75, 2041=75, 2042=75, 2043=75, 2044=75, 2045=75, 2046=75, 2047=75, 2048=75, 2049=75, 2050=75
R129 | YR | DTC ARPU ($/sub/mo, year-row) |  | $16/mo in 2025 → $10/mo by 2030, flat. |  |  | fixed-yearrow | 
  YEARS: 2025=16, 2026=14.8, 2027=13.6, 2028=12.4, 2029=11.2, 2030=10, 2031=10, 2032=10, 2033=10, 2034=10, 2035=10, 2036=10, 2037=10, 2038=10, 2039=10, 2040=10, 2041=10, 2042=10, 2043=10, 2044=10, 2045=10, 2046=10, 2047=10, 2048=10, 2049=10, 2050=10
R130 | VAL | Subsidy mix (% of net adds subsidized) | 0.5 | 50% subsidized stub. | 0.2 | 0.8 | triangle | 
R131 | VAL | Terminal retail price ($, non-subsidized) | 500 | Disclosed. | 400 | 600 | triangle | 
R132 | VAL | Terminal retail price ($, subsidized) | 300 | Disclosed subsidized price. | 200 | 400 | triangle | 
R133 | VAL | Terminal COGS per unit ($) | 500 | Unit cost; subsidy creates margin gap on subsidized half. | 400 | 700 | triangle | 
R134 | SUB | ▸ BB/DTC market mix (Spec 09) |  |  |  |  |  | 
R135 | VAL | BB market share % (Starlink revenue mix) | 0.85 | Fixed market mix input. Vlad-locked. | 0.8 | 0.95 | triangle | 
R136 | VAL | DTC market share % (Starlink revenue mix) | 0.15 |  |  |  | fixed | Derived = 1 - BB share
R137 | SUB | ▸ Bandwidth flow to ODC (Spec 04 PLACEHOLDERS) |  |  |  |  |  | 
R138 | VAL | Gbps per GWh/yr of ODC compute energy (PLACEHOLDER) | 0.05 | Pending research on token compression / multi-hop / duty cycle. WIDE MC. | 0.01 | 0.5 | lognormal | Placeholder — full range pending calibration
R139 | VAL | BB-share of ODC bandwidth claim (PLACEHOLDER) | 0.5 | 50% BB / 50% DTC stub. Pending consumer-phone vs fixed-broadband endpoint mix. | 0.2 | 0.8 | triangle | Placeholder
R140 | SUB | ▸ Starlink large-default cash + kg asks (Spec 09) |  |  |  |  |  | 
R141 | YR | Starlink kg ask year-row (large default, exceeds plausible capacity) |  | Spec 09 architecture. Outer queue caps via gate. |  |  | fixed-yearrow | Structural
  YEARS: 2025=10000000, 2026=10000000, 2027=10000000, 2028=10000000, 2029=10000000, 2030=10000000, 2031=10000000, 2032=10000000, 2033=10000000, 2034=10000000, 2035=10000000, 2036=10000000, 2037=10000000, 2038=10000000, 2039=10000000, 2040=10000000, 2041=10000000, 2042=10000000, 2043=10000000, 2044=10000000, 2045=10000000, 2046=10000000, 2047=10000000, 2048=10000000, 2049=10000000, 2050=10000000
R142 | YR | Starlink cash ask year-row ($mm, large default) |  | Spec 09 architecture. Outer queue caps via gate. |  |  | fixed-yearrow | Structural
  YEARS: 2025=100000, 2026=100000, 2027=100000, 2028=100000, 2029=100000, 2030=100000, 2031=100000, 2032=100000, 2033=100000, 2034=100000, 2035=100000, 2036=100000, 2037=100000, 2038=100000, 2039=100000, 2040=100000, 2041=100000, 2042=100000, 2043=100000, 2044=100000, 2045=100000, 2046=100000, 2047=100000, 2048=100000, 2049=100000, 2050=100000
R143 | SECT | §6 ODC |  |  |  |  |  | 
R144 | SUB | ▸ Satellite & subsystem anchors (V2 Compute config) |  |  |  |  |  | 
R145 | VAL | Compute power per sat (kW) | 140 | V30.5 V2 Compute config. Vlad lock: keep more aggressive than Q4'25 70 W/kg. | 80 | 200 | triangle | Vlad confirmed V30.5 more accurate than Q4'25
R146 | VAL | Solar generation per sat (kW, gen requirement) | 156 | Solar nameplate (~10% margin over compute). | 90 | 220 | triangle | 
R147 | VAL | Total sat dry mass (kg) | 1400 | V2 Compute mass. | 1000 | 1800 | triangle | 
R148 | VAL | F_ref — reference compute unit (TFLOPS, H100 FP8 dense) | 1979 | H100 industry anchor. |  |  | fixed | Industry spec
R149 | VAL | Effective Compute Ratio (ECR) | 0.6 | Workload fit factor. | 0.4 | 0.8 | triangle | 
R150 | VAL | Workload mix — % inference | 0.85 | Inference-dominant. | 0.6 | 0.95 | triangle | 
R151 | VAL | ODC fleet design life (years) | 5 | Compute hardware refresh cycle. | 4 | 7 | triangle | 
R152 | VAL | Sat solar generation (W, for $/W subsystem cost) | 156000 |  |  |  | fixed | Derived
R153 | VAL | Sat thermal mass (kg) | 480 | Thermal subsystem mass. | 350 | 600 | triangle | 
R154 | SUB | ▸ Subsystem unit costs (per-sat, flat unless noted) |  |  |  |  |  | 
R155 | VAL | Solar array unit cost ($/W) | 8 | SpaceX-internal Base. | 5 | 12 | triangle | 
R156 | VAL | Thermal system unit cost ($/kg) | 3000 | Orbital thermal premium. | 2000 | 5000 | triangle | 
R157 | VAL | Comms (ISL set) flat cost ($) | 75000 | Per-sat ISL hardware. | 50000 | 100000 | triangle | 
R158 | VAL | ADCS + avionics flat cost ($) | 150000 | Per-sat. | 100000 | 200000 | triangle | 
R159 | VAL | Structure flat cost ($) | 65000 | Per-sat. | 45000 | 90000 | triangle | 
R160 | VAL | Battery flat cost ($) | 40000 | Per-sat. | 25000 | 60000 | triangle | 
R161 | VAL | Shielding flat cost ($) | 25000 | Per-sat. | 15000 | 40000 | triangle | 
R162 | VAL | Integration & Test flat cost ($) | 150000 | Per-sat. | 100000 | 250000 | triangle | 
R163 | SUB | ▸ Wright's Law learning rates |  |  |  |  |  | 
R164 | VAL | LR — chips (per doubling) | 0 | Frontier chips reinvest capability, not price. |  |  | fixed | Structural assumption
R165 | VAL | LR — subsystems (per doubling) | 0.15 | 15% per doubling cum sats. | 0.05 | 0.25 | triangle | 
R166 | VAL | Anchor year for ODC Wright's Law | 2026 | First material deployment year. |  |  | fixed | 
R167 | SUB | ▸ Revenue parameters |  |  |  |  |  | 
R168 | VAL | Annual GPU-hr price deflation rate | 0.05 | 5%/yr price compression. | 0.02 | 0.1 | triangle | 
R169 | VAL | Ground station / network opex % of revenue | 0.02 | Ground ops cost. | 0.01 | 0.05 | triangle | 
R170 | VAL | ODC insurance % of revenue | 0.01 | 1% insurance. | 0.005 | 0.025 | triangle | 
R171 | VAL | ODC other COGS % of revenue | 0.03 | Catch-all. | 0.01 | 0.06 | triangle | 
R172 | SUB | ▸ Chip roadmap (year-rows, H100 → AI5 → Dojo-3) |  |  |  |  |  | 
R173 | YR | Chip TDP per chip (W) — year-row |  | H100=700 (2026), AI5=500 (2028), Dojo-3=600 (2031), interpolated. |  |  | fixed-yearrow | Speculative roadmap
  YEARS: 2025=700, 2026=700, 2027=600, 2028=500, 2029=533.333, 2030=566.667, 2031=600, 2032=600, 2033=600, 2034=600, 2035=600, 2036=600, 2037=600, 2038=600, 2039=600, 2040=600, 2041=600, 2042=600, 2043=600, 2044=600, 2045=600, 2046=600, 2047=600, 2048=600, 2049=600, 2050=600
R174 | YR | Chip FP8 performance per chip (TFLOPS) — year-row |  | H100=1979, AI5=1979, Dojo-3=4500. |  |  | fixed-yearrow | Speculative roadmap
  YEARS: 2025=1979, 2026=1979, 2027=1979, 2028=1979, 2029=2819.33, 2030=3659.67, 2031=4500, 2032=4500, 2033=4500, 2034=4500, 2035=4500, 2036=4500, 2037=4500, 2038=4500, 2039=4500, 2040=4500, 2041=4500, 2042=4500, 2043=4500, 2044=4500, 2045=4500, 2046=4500, 2047=4500, 2048=4500, 2049=4500, 2050=4500
R175 | YR | Chip mass per chip (kg) — year-row |  | 1.2 → 0.8 → 0.8. |  |  | fixed-yearrow | 
  YEARS: 2025=1.2, 2026=1.0667, 2027=0.9333, 2028=0.8, 2029=0.8, 2030=0.8, 2031=0.8, 2032=0.8, 2033=0.8, 2034=0.8, 2035=0.8, 2036=0.8, 2037=0.8, 2038=0.8, 2039=0.8, 2040=0.8, 2041=0.8, 2042=0.8, 2043=0.8, 2044=0.8, 2045=0.8, 2046=0.8, 2047=0.8, 2048=0.8, 2049=0.8, 2050=0.8
R176 | YR | Chip cost per chip ($) — year-row |  | $30K → $5K → $2.5K. |  |  | fixed-yearrow | Speculative roadmap
  YEARS: 2025=30000, 2026=21666.7, 2027=13333.3, 2028=5000, 2029=4166.67, 2030=3333.33, 2031=2500, 2032=2500, 2033=2500, 2034=2500, 2035=2500, 2036=2500, 2037=2500, 2038=2500, 2039=2500, 2040=2500, 2041=2500, 2042=2500, 2043=2500, 2044=2500, 2045=2500, 2046=2500, 2047=2500, 2048=2500, 2049=2500, 2050=2500
R177 | YR | Price per H100-equiv GPU-hr ($) — year-row |  | $2 in 2026, -5%/yr deflation. |  |  | fixed-yearrow | 
  YEARS: 2025=2, 2026=1.9, 2027=1.805, 2028=1.7147, 2029=1.629, 2030=1.5476, 2031=1.4702, 2032=1.3967, 2033=1.3268, 2034=1.2605, 2035=1.1975, 2036=1.1376, 2037=1.0807, 2038=1.0267, 2039=0.9753, 2040=0.9266, 2041=0.8803, 2042=0.8362, 2043=0.7944, 2044=0.7547, 2045=0.717, 2046=0.6811, 2047=0.6471, 2048=0.6147, 2049=0.584, 2050=0.5548
R178 | YR | Utilization % (fleet ramp) — year-row |  | 0.4 → 0.85 by 2029. |  |  | fixed-yearrow | 
  YEARS: 2025=0.4, 2026=0.5125, 2027=0.625, 2028=0.7375, 2029=0.85, 2030=0.85, 2031=0.85, 2032=0.85, 2033=0.85, 2034=0.85, 2035=0.85, 2036=0.85, 2037=0.85, 2038=0.85, 2039=0.85, 2040=0.85, 2041=0.85, 2042=0.85, 2043=0.85, 2044=0.85, 2045=0.85, 2046=0.85, 2047=0.85, 2048=0.85, 2049=0.85, 2050=0.85
R179 | SUB | ▸ Dual revenue model (Sprint 3.5) |  |  |  |  |  | 
R180 | VAL | Credence on Model A (Pr(A)) | 0.6 | Sprint 3.5 default. Pr(B) = 1 − Pr(A). | 0.2 | 0.8 | triangle | Epistemic weight, not scenario probability
R181 | VAL | CoreWeave baseline anchor ($B/GW_IT/yr, 2026) | 12 | Rittenhouse Research, $12B/GW_IT/yr. | 8 | 16 | triangle | 
R182 | VAL | PUE_base (terrestrial colo) | 1.4 | Industry standard terrestrial PUE. | 1.3 | 1.6 | triangle | 
R183 | VAL | Orbital PUE | 1.12 | First-principles: PDU 95% + pumps 3-5% + housekeeping 3% + eclipse 1%. | 1.05 | 1.3 | triangle | 
R184 | VAL | Terrestrial price deflation %/yr (Model A baseline year-row driver) | 0.05 | Matches GPU-hr deflation for model congruence. | 0.02 | 0.1 | triangle | 
R185 | VAL | Steady-state utilization (for Model A util-adjustment ratio) | 0.85 | Same as utilization steady-state. |  |  | fixed | Derived link
R186 | SUB | ▸ ODC internal vs external compute split (NEW per Vlad's framing) |  |  |  |  |  | 
R187 | YR | ODC internal compute share to AI Stack % — year-row |  | Most ODC compute feeds AI Stack internally early; external share grows as compute market matures. | 0.3 | 0.99 | triangle-yearrow | Vlad lock: most ODC feeds AI Stack internally. MC tunes external market growth.
  YEARS: 2025=0.95, 2026=0.9167, 2027=0.8833, 2028=0.85, 2029=0.8125, 2030=0.775, 2031=0.7375, 2032=0.7, 2033=0.675, 2034=0.65, 2035=0.625, 2036=0.6, 2037=0.575, 2038=0.55, 2039=0.525, 2040=0.5, 2041=0.49, 2042=0.48, 2043=0.47, 2044=0.46, 2045=0.45, 2046=0.44, 2047=0.43, 2048=0.42, 2049=0.41, 2050=0.4
R188 | YR | ODC external compute share to customers % — year-row |  | Derived = 1 − internal share. |  |  | fixed-yearrow | Derived
  YEARS: 2025=0.05, 2026=0.0833, 2027=0.1167, 2028=0.15, 2029=0.1875, 2030=0.225, 2031=0.2625, 2032=0.3, 2033=0.325, 2034=0.35, 2035=0.375, 2036=0.4, 2037=0.425, 2038=0.45, 2039=0.475, 2040=0.5, 2041=0.51, 2042=0.52, 2043=0.53, 2044=0.54, 2045=0.55, 2046=0.56, 2047=0.57, 2048=0.58, 2049=0.59, 2050=0.6
R189 | SECT | §7 AI STACK (standalone module) |  |  |  |  |  | 
R190 | SUB | ▸ Cursor (orchestration) |  |  |  |  |  | 
R191 | YR | Cursor paid seats (millions) — year-row |  | Vlad to tune. Stub: 2M in 2026 → 50M by 2035. |  |  | triangle-yearrow | Speculative product ramp
  YEARS: 2025=1, 2026=2, 2027=5.25, 2028=8.5, 2029=11.75, 2030=15, 2031=22, 2032=29, 2033=36, 2034=43, 2035=50, 2036=52, 2037=54, 2038=56, 2039=58, 2040=60, 2041=62, 2042=64, 2043=66, 2044=68, 2045=70, 2046=72, 2047=74, 2048=76, 2049=78, 2050=80
R192 | VAL | Cursor avg subscription price ($/seat/mo) | 20 | Disclosed Cursor pricing tier. | 15 | 30 | triangle | 
R193 | VAL | Cursor enterprise API rev per seat ($/year) | 60 | Adds ~25% to base subscription. | 30 | 100 | triangle | 
R194 | SUB | ▸ Grok consumer (X Premium / Grok Premium) |  |  |  |  |  | 
R195 | YR | Grok consumer paid subs (millions) — year-row |  | Vlad to tune. Stub: 5M in 2026 → 80M by 2035 (rides X platform growth + AI features). |  |  | triangle-yearrow | Speculative consumer ramp
  YEARS: 2025=2, 2026=5, 2027=11.25, 2028=17.5, 2029=23.75, 2030=30, 2031=40, 2032=50, 2033=60, 2034=70, 2035=80, 2036=82.6667, 2037=85.3333, 2038=88, 2039=90.6667, 2040=93.3333, 2041=96, 2042=98.6667, 2043=101.333, 2044=104, 2045=106.667, 2046=109.333, 2047=112, 2048=114.667, 2049=117.333, 2050=120
R196 | VAL | Grok consumer ARPU ($/user/year) | 96 | X Premium $84 + Grok Heavy upgrades = ~$96. | 60 | 150 | triangle | 
R197 | SUB | ▸ Grok enterprise (API) |  |  |  |  |  | 
R198 | YR | Grok enterprise API token volume (T tokens/year) — year-row |  | Vlad to tune. Stub: 5T in 2026 → 1000T by 2035. CAUTION: may need dampening — 2030 stub of 200T × $4/Mtoken = $800B, implausibly large share of inference market. |  |  | triangle-yearrow | Dampened from raw stub to keep 2030 revenue defensible
  YEARS: 2025=1, 2026=5, 2027=16.25, 2028=27.5, 2029=38.75, 2030=50, 2031=80, 2032=110, 2033=140, 2034=170, 2035=200, 2036=220, 2037=240, 2038=260, 2039=280, 2040=300, 2041=320, 2042=340, 2043=360, 2044=380, 2045=400, 2046=420, 2047=440, 2048=460, 2049=480, 2050=500
R199 | YR | Grok enterprise API price ($/Mtoken) — year-row |  | $5 in 2026, -5%/yr deflation (mirrors GPU-hr). |  |  | fixed-yearrow | 
  YEARS: 2025=5, 2026=4.75, 2027=4.5125, 2028=4.2869, 2029=4.0725, 2030=3.8689, 2031=3.6755, 2032=3.4917, 2033=3.3171, 2034=3.1512, 2035=2.9937, 2036=2.844, 2037=2.7018, 2038=2.5667, 2039=2.4384, 2040=2.3165, 2041=2.2006, 2042=2.0906, 2043=1.9861, 2044=1.8868, 2045=1.7924, 2046=1.7028, 2047=1.6177, 2048=1.5368, 2049=1.4599, 2050=1.3869
R200 | SUB | ▸ AI Stack operating parameters |  |  |  |  |  | 
R201 | VAL | AI Stack insurance % of revenue | 0.01 | 1% catch-all. | 0.005 | 0.025 | triangle | 
R202 | VAL | AI Stack other COGS % of revenue | 0.03 | 3% catch-all. | 0.01 | 0.06 | triangle | 
R203 | SECT | §8 LUNAR / MARS (strategic carve-out — NOT in IRR queue) |  |  |  |  |  | 
R204 | SUB | ▸ Module-wide parameters |  |  |  |  |  | 
R205 | VAL | Capital lifetime — book value straight-line depreciation (years) | 10 | Legacy BV methodology. | 7 | 15 | triangle | 
R206 | VAL | Module operating cost — Lunar (% of Lunar CapEx) | 0.05 | 5% mission ops. | 0.03 | 0.1 | triangle | 
R207 | VAL | Module operating cost — Mars (% of Mars CapEx) | 0.05 | Same. | 0.03 | 0.1 | triangle | 
R208 | SUB | ▸ Labour unit shared parameters (Optimus-class proxy) |  |  |  |  |  | 
R209 | VAL | Labour unit mass (kg) | 60 | Robotic class proxy. | 40 | 100 | triangle | 
R210 | VAL | Labour unit base hourly output ($/hr; burdened $22/0.7) | 31.43 |  |  |  | fixed | Derived
R211 | VAL | Labour unit daily working hours | 22 | Robots don't sleep. | 18 | 24 | triangle | 
R212 | VAL | Labour unit productivity factor vs human baseline | 1 | Parity stub. | 0.25 | 2 | triangle | Wide MC per Q4'25
R213 | VAL | Labour unit productivity learning rate (%/yr) | 0.05 | 5%/yr productivity gain. | 0.02 | 0.15 | triangle | 
R214 | VAL | Labour unit operational lifespan on surface (years) | 5 | Retirement vintage. | 3 | 8 | triangle | 
R215 | SUB | ▸ Lunar-specific |  |  |  |  |  | 
R216 | VAL | Lunar fuel depot multiplier per outbound Starship | 1 | 1 tanker per moon ship. | 0.5 | 2 | triangle | 
R217 | VAL | Lunar payload per surface-landed Starship (kg) | 50000 | Translunar with landing reserve. | 40000 | 60000 | triangle | 
R218 | VAL | Lunar % payload as labour units | 0.3 | 30% labour / 70% hardware. | 0.1 | 0.5 | triangle | 
R219 | SUB | ▸ Mars-specific |  |  |  |  |  | 
R220 | VAL | Mars fuel depot multiplier per outbound Starship | 5 | Rocket equation; 5 tankers per Mars ship. | 3 | 8 | triangle | 
R221 | VAL | Mars payload per surface-landed Starship (kg) | 100000 | Cargo Starship Mars landing. | 70000 | 130000 | triangle | 
R222 | VAL | Mars % payload as labour units | 0.3 | Same as Lunar. | 0.1 | 0.5 | triangle | 
R223 | SUB | ▸ Year-row cost curves |  |  |  |  |  | 
R224 | YR | Labour unit cost ($/unit) — declining curve |  | Tesla Optimus aspirational pricing trajectory. |  |  | triangle-yearrow | 
  YEARS: 2025=30000, 2026=30000, 2027=27500, 2028=25000, 2029=22500, 2030=20000, 2031=18400, 2032=16800, 2033=15200, 2034=13600, 2035=12000, 2036=11200, 2037=10400, 2038=9600, 2039=8800, 2040=8000, 2041=8000, 2042=8000, 2043=8000, 2044=8000, 2045=8000, 2046=8000, 2047=8000, 2048=8000, 2049=8000, 2050=8000
R225 | YR | Hardware replacement cost factor ($/kg landed) — declining |  | Supply chain maturation. |  |  | triangle-yearrow | 
  YEARS: 2025=1000, 2026=1000, 2027=950, 2028=900, 2029=850, 2030=800, 2031=740, 2032=680, 2033=620, 2034=560, 2035=500, 2036=486.667, 2037=473.333, 2038=460, 2039=446.667, 2040=433.333, 2041=420, 2042=406.667, 2043=393.333, 2044=380, 2045=366.667, 2046=353.333, 2047=340, 2048=326.667, 2049=313.333, 2050=300
R226 | SUB | ▸ Lunar / Mars share of carve-out cash (derived deployment) |  |  |  |  |  | 
R227 | YR | Lunar share of Mars/Moon carve-out cash — year-row |  | Lunar continuous (year-round); fills lower-cost end. Stub: high initially, drops as Mars windows arrive. |  |  | triangle-yearrow | Vlad to tune
  YEARS: 2025=1, 2026=0.85, 2027=0.7, 2028=0.6, 2029=0.5, 2030=0.4, 2031=0.36, 2032=0.32, 2033=0.28, 2034=0.24, 2035=0.2, 2036=0.1967, 2037=0.1933, 2038=0.19, 2039=0.1867, 2040=0.1833, 2041=0.18, 2042=0.1767, 2043=0.1733, 2044=0.17, 2045=0.1667, 2046=0.1633, 2047=0.16, 2048=0.1567, 2049=0.1533, 2050=0.15
R228 | YR | Mars share of carve-out cash — year-row |  | Window-bound (~every 26 months). Derived = 1 − Lunar share. |  |  | fixed-yearrow | Derived
  YEARS: 2025=0, 2026=0.15, 2027=0.3, 2028=0.4, 2029=0.5, 2030=0.6, 2031=0.64, 2032=0.68, 2033=0.72, 2034=0.76, 2035=0.8, 2036=0.8033, 2037=0.8067, 2038=0.81, 2039=0.8133, 2040=0.8167, 2041=0.82, 2042=0.8233, 2043=0.8267, 2044=0.83, 2045=0.8333, 2046=0.8367, 2047=0.84, 2048=0.8433, 2049=0.8467, 2050=0.85
R229 | SECT | §9 OPEX (Group-level) |  |  |  |  |  | 
R230 | SUB | ▸ R&D by module (start% / end% / CAGR taper per Spec 03 §2.2) |  |  |  |  |  | 
R231 | VAL | Starlink R&D — start % of (Starlink + Starshield) rev | 0.08 | Mature subscription business R&D high start (V3 + DTC ramp). | 0.03 | 0.12 | triangle | 
R232 | VAL | Starlink R&D — end-state % (floor) | 0.03 | Mature satcom peer floor. | 0.02 | 0.05 | triangle | 
R233 | VAL | Starlink R&D — CAGR (taper) | -0.1 | 10%/yr taper toward floor. | -0.2 | -0.05 | triangle | 
R234 | VAL | Customer Launch R&D — start % of external rev | 0.25 | Heavy 2025-2028 Starship dev. | 0.15 | 0.35 | triangle | 
R235 | VAL | Customer Launch R&D — end-state % (floor) | 0.04 | Mature post-Starship-commercial. | 0.02 | 0.08 | triangle | 
R236 | VAL | Customer Launch R&D — CAGR (taper) | -0.2 | Sharp taper. | -0.3 | -0.1 | triangle | 
R237 | VAL | ODC R&D — start % of ODC rev | 0.3 | Early-stage 30% R&D / rev. | 0.15 | 0.5 | triangle | 
R238 | VAL | ODC R&D — end-state % (floor) | 0.08 | 8% mature. | 0.05 | 0.15 | triangle | 
R239 | VAL | ODC R&D — CAGR (taper) | -0.15 | 15%/yr taper. | -0.25 | -0.1 | triangle | 
R240 | VAL | AI Stack R&D — start % of AI Stack rev | 0.15 | Software/R&D heavy. | 0.1 | 0.3 | triangle | 
R241 | VAL | AI Stack R&D — end-state % (floor) | 0.05 | Mature software. | 0.03 | 0.1 | triangle | 
R242 | VAL | AI Stack R&D — CAGR (taper) | -0.1 | Taper. | -0.2 | -0.05 | triangle | 
R243 | SUB | ▸ R&D — Moon/Mars ($-profile year-row, pre-revenue) |  |  |  |  |  | 
R244 | YR | R&D — Moon/Mars ($mm/yr) — year-row |  | Q4'25 anchored $700M in 2025 (V30.5 had $500M — bumped). Ramps then tapers per program lifecycle. |  |  | triangle-yearrow | Q4'25 anchored 2025; trajectory MC-variable
  YEARS: 2025=700, 2026=833.333, 2027=966.667, 2028=1100, 2029=1300, 2030=1500, 2031=1750, 2032=2000, 2033=2166.67, 2034=2333.33, 2035=2500, 2036=2300, 2037=2100, 2038=1900, 2039=1700, 2040=1500, 2041=1410, 2042=1320, 2043=1230, 2044=1140, 2045=1050, 2046=960, 2047=870, 2048=780, 2049=690, 2050=600
R245 | SUB | ▸ SG&A by function |  |  |  |  |  | 
R246 | VAL | Sales & Marketing — start % of (Starlink+Starshield+Customer Launch ext) rev | 0.04 | Includes terminal-acquisition marketing. | 0.02 | 0.06 | triangle | 
R247 | VAL | Sales & Marketing — end-state % (floor) | 0.02 | Mature. | 0.01 | 0.04 | triangle | 
R248 | VAL | Sales & Marketing — CAGR (taper) | -0.08 | Taper. | -0.15 | -0.04 | triangle | 
R249 | VAL | General & Administrative — start % of group rev | 0.05 | 5% G&A start. | 0.03 | 0.07 | triangle | 
R250 | VAL | General & Administrative — end-state % (ceiling) | 0.06 | Drifts up at scale (compliance / HQ). | 0.04 | 0.08 | triangle | 
R251 | VAL | General & Administrative — CAGR (drift) | 0.01 | 1%/yr drift up. | 0 | 0.03 | triangle | 
R252 | VAL | Customer Service — flat % of Starlink subscription rev | 0.02 | 2% CS on Starlink subs (BB + DTC). | 0.01 | 0.04 | triangle | 
R253 | VAL | Other corporate operating — flat % of group rev | 0.01 | 1% catch-all incl. regulatory fees. | 0.005 | 0.025 | triangle | 
R254 | SECT | §10 CAPEX (Corporate + Spectrum + Module Aggregation) |  |  |  |  |  | 
R255 | SUB | ▸ Corporate facilities CapEx ($mm/yr) |  |  |  |  |  | 
R256 | VAL | HQ buildings CapEx ($mm/yr, flat) | 50 | Stub. MC range wide given uncertainty on corporate expansion. | 20 | 150 | triangle | 
R257 | VAL | Corporate IT CapEx ($mm/yr, flat) | 30 | Stub. | 10 | 80 | triangle | 
R258 | VAL | General engineering facilities CapEx ($mm/yr, flat) | 20 | Stub. | 5 | 60 | triangle | 
R259 | VAL | Other corporate CapEx ($mm/yr, flat) | 10 | Stub. | 5 | 30 | triangle | 
R260 | SUB | ▸ Corporate useful lives |  |  |  |  |  | 
R261 | VAL | HQ buildings useful life (years) | 30 | Standard. | 25 | 40 | triangle | 
R262 | VAL | Corporate IT useful life (years) | 7 | IT refresh cycle. | 5 | 10 | triangle | 
R263 | VAL | General engineering facilities life (years) | 20 | Industrial facility life. | 15 | 30 | triangle | 
R264 | VAL | Other corporate useful life (years) | 20 | Generic. | 15 | 30 | triangle | 
R265 | SUB | ▸ Corporate historical capital base |  |  |  |  |  | 
R266 | VAL | Corporate historical capital base ($mm) | 2000 | Pre-2025 corporate CapEx accumulated. | 1000 | 3000 | triangle | 
R267 | SUB | ▸ EchoStar spectrum (Spec 03 §5) |  |  |  |  |  | 
R268 | YR | EchoStar mid-band CapEx ($mm) — year-row |  | $20B cumulative 2025-2028. Disclosed deal ~$17B; rebuild uses $20B Vlad-locked stub. |  |  | triangle-yearrow | Year-by-year cadence MC-variable; total $20B Vlad-locked
  YEARS: 2025=5000, 2026=8000, 2027=5000, 2028=2000, 2029=0, 2030=0, 2031=0, 2032=0, 2033=0, 2034=0, 2035=0, 2036=0, 2037=0, 2038=0, 2039=0, 2040=0, 2041=0, 2042=0, 2043=0, 2044=0, 2045=0, 2046=0, 2047=0, 2048=0, 2049=0, 2050=0
R269 | VAL | Spectrum useful life (years) | 15 | Spec 03 stub. | 10 | 25 | triangle | 
R270 | SECT | §11 VALUATION |  |  |  |  |  | 
R271 | SUB | ▸ WACC + risk premia |  |  |  |  |  | 
R272 | VAL | Group WACC | 0.1 | 10% stub for high-growth tech. | 0.08 | 0.14 | triangle | 
R273 | VAL | Risk premium — Starlink (over group WACC) | 0 | Mature; baseline = group. | 0 | 0.02 | triangle | 
R274 | VAL | Risk premium — Customer Launch | 0.01 | Cyclical demand + Starship dev risk. | 0 | 0.03 | triangle | 
R275 | VAL | Risk premium — ODC | 0.02 | Pre-revenue infra. | 0.01 | 0.04 | triangle | 
R276 | VAL | Risk premium — AI Stack | 0.03 | Speculative. | 0.02 | 0.05 | triangle | 
R277 | VAL | Risk premium — Lunar / Mars | 0.05 | Pre-revenue, narrative-heavy. | 0.02 | 0.08 | triangle | 
R278 | SUB | ▸ WACC component memos (not used in formulas) |  |  |  |  |  | 
R279 | VAL | Cost of equity (memo) | 0.115 | CAPM placeholder. |  |  | fixed | Memo only
R280 | VAL | Cost of debt (memo) | 0.09 | Apollo SpaceX private credit anchor ~9-11%. |  |  | fixed | Memo only
R281 | VAL | Leverage E/V (memo) | 0.7 | Informational. |  |  | fixed | Memo only
R282 | SUB | ▸ Terminal value parameters |  |  |  |  |  | 
R283 | VAL | Terminal growth rate g (group + most modules) | 0.025 | Gordon Growth perpetuity. | 0.015 | 0.035 | triangle | 
R284 | VAL | Starlink — exit revenue multiple | 8 | Mature satcom comp range. | 5 | 12 | triangle | 
R285 | VAL | Lunar / Mars — terminal BV multiplier | 1.5 | Wide range; deeply uncertain. | 0.5 | 3 | triangle | 
R286 | VAL | Starship D&A useful life — memo add-back for Launch standalone DCF | 8 | Vehicle lifetime_reuses anchor. | 5 | 12 | triangle | 
R287 | VAL | Terminal FCF averaging window (years pre-2050) | 5 | Smooths the FCF cliff. |  |  | fixed | Smoothing parameter
R288 | SUB | ▸ Comparables anchors ($B) |  |  |  |  |  | 
R289 | VAL | Comp anchor — Group EV (Morgan Stanley public) | 350 | Public sell-side note (2025). | 200 | 500 | triangle | 
R290 | VAL | Comp anchor — Group EV (Brant internal) | 2500 | ⚠ Memo only — DO NOT QUOTE EXTERNALLY. |  |  | fixed | Memo only — internal anchor
R291 | VAL | Comp anchor — Starlink standalone (Bernstein/JPM) | 150 | EV/Rev ~10× × $15B rev. | 100 | 250 | triangle | 
R292 | VAL | Comp anchor — ODC standalone (CoreWeave-anchored) | 50 | Pre-revenue placeholder. | 20 | 100 | triangle | 
R293 | VAL | Comp anchor — Customer Launch standalone (Rocket Lab) | 40 | EV/Rev ~5× × $8B 2025 launch rev. | 20 | 80 | triangle | 
R294 | VAL | Comp anchor — AI Stack standalone | 0 | Wakes when AI Stack revenue lights up. |  |  | fixed | Auto-wakes
R295 | VAL | Comp anchor — Lunar / Mars (NASA HLS lifetime) | 50 | Lifetime HLS contracts + Mars TAM. | 10 | 200 | triangle | Wide
R296 | SUB | ▸ SoTP multiples (EV/Revenue at 2050) |  |  |  |  |  | 
R297 | VAL | Multiple — Customer Launch (EV/Rev at 2050) | 5 | Rocket Lab proxy. | 3 | 8 | triangle | 
R298 | VAL | Multiple — Starlink (EV/Rev at 2050) | 10 | Mature satcom. | 6 | 14 | triangle | 
R299 | VAL | Multiple — ODC (EV/Rev at 2050) | 6 | CoreWeave proxy. | 3 | 10 | triangle | 
R300 | VAL | Multiple — AI Stack (EV/Rev at 2050) | 5 | Placeholder; AI Stack sprint may refine. | 3 | 10 | triangle | 
R301 | VAL | Multiple — Lunar / Mars (anchor stub, $B) | 50 | BV-based, not revenue-multiple. |  |  | fixed | BV-based
```

---

## §4 — Verification gate

Any failure → halt, report, push back. No "proceed and document."

### §4.1 — Universal checks

- **No formula errors workbook-wide.** Read every cell on every tab; count `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`. **Expected: zero.** Sprint 0 writes no formulas, so any error indicates a data-type miswrite.
- **Edge-year reads.** For year-row inputs (BB ARPU R128, DTC ARPU R129, EchoStar spectrum R268, Starship customer launch price R64, Mars/Moon R&D R244), read columns D (2025), I (2030), S (2040), AC (2050) and confirm trajectory shape matches §3.6.
- **Round-trip stability.** Recalc the workbook 5 times. Since Sprint 0 writes no formulas, every cell should be invariant. **Expected: bit-for-bit identical.**

### §4.2 — Sprint 0 anchor read-back (HALT GATE)

Plugin reads each anchor cell from the Assumptions tab (finds row by column-A label) and compares to expected value. Any deviation outside tolerance → halt.

| Assumptions col-A label | Expected | Tolerance |
|---|---|---|
| `Starting cash position EoY 2024 ($mm)` | 5000 | exact |
| `IPO injection amount ($mm)` | 30000 | exact |
| `IPO injection year` | 2027 | exact |
| `Mars carve-out floor ($mm/yr)` | 1000 | exact |
| `Mars carve-out % of prior-year Group FCF` | 0.15 | exact |
| `Sigmoid IRR-blend exponent k` | 2 | exact |
| `Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)` | 0.7 | exact |
| `Vehicle build lead time (years)` | 2 | exact |
| `F9 starting fleet at 2025 SoY (boosters)` | 28 | exact |
| `F9 customer launch price ($mm/launch) — 2025 anchor` col D (2025) | 111 | exact |
| `Starship customer launch price ($mm/launch) — year-row` col D (2025) | 0 | exact |
| `Starship customer launch price ($mm/launch) — year-row` col F (2027) | 100 | exact |
| `Broadband ARPU ($/sub/mo, year-row)` col D (2025) | 100 | exact |
| `Broadband ARPU ($/sub/mo, year-row)` col I (2030) | 75 | exact |
| `DTC ARPU ($/sub/mo, year-row)` col D (2025) | 16 | exact |
| `DTC ARPU ($/sub/mo, year-row)` col I (2030) | 10 | exact |
| `Starshield Reserved % — decay rate` | 0.25 | exact |
| `Starshield Rev per Gbps — base year ($/Gbps)` | 164699 | exact |
| `V2 Mini BB Active Sats — end-2025` | 5246 | exact |
| `V2 Mini DTC Active Sats — end-2025` | 650 | exact |
| `Cumulative sats at base year (end-2024)` | 7486 | exact |
| `Satellite cost per kg — base year ($/kg)` | 650 | exact |
| `V2 Mini Mass (kg)` | 575 | exact |
| `V2 Mini Bandwidth per Sat — BB (Gbps)` | 96 | exact |
| `Compute power per sat (kW)` | 140 | exact |
| `Credence on Model A (Pr(A))` | 0.6 | exact |
| `ODC fleet design life (years)` | 5 | exact |
| `R&D — Moon/Mars ($mm/yr) — year-row` col D (2025) | 700 | ±$5 |
| `Starlink R&D — start % of (Starlink + Starshield) rev` | 0.08 | exact |
| `Customer Launch R&D — start % of external rev` | 0.25 | exact |
| `ODC R&D — start % of ODC rev` | 0.3 | exact |
| `AI Stack R&D — start % of AI Stack rev` | 0.15 | exact |
| `EchoStar mid-band CapEx ($mm) — year-row` col D (2025) | 5000 | exact |
| `EchoStar mid-band CapEx ($mm) — year-row` col E (2026) | 8000 | exact |
| `Spectrum useful life (years)` | 15 | exact |
| `Tax rate (corporate, US federal + state blended)` | 0.21 | exact |
| `Group WACC` | 0.1 | exact |
| `Terminal growth rate g (group + most modules)` | 0.025 | exact |
| **Standards (every active tab):** | | |
| Row 4 D column on each tab 1–13 | 2025 | exact |
| Row 4 AC column on each tab 1–13 | 2050 | exact |
| Row 5 D column on each tab 1–13 | 0 | exact |
| Row 5 AC column on each tab 1–13 | 25 | exact |

### §4.3 — Halt conditions (quantitative)

Plugin halts and reports if:

- Any anchor in §4.2 deviates from expected beyond tolerance.
- Any cell in row 4 on tabs 1–13 ≠ literal integer in {2025…2050}.
- Any cell in row 5 on tabs 1–13 ≠ literal integer in {0…25}.
- Any formula present on the Assumptions tab.
- Any input from §3.6 missing an MC range when distribution ≠ `fixed`.
- Any sheet name deviates from §3.1 exact list.
- Any error value (`#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`) anywhere.

### §4.4 — Verification log (plugin produces in chat)

After §4.1–§4.3 pass, plugin produces:

```
Sprint 0 verification log
=========================

Workbook: SpaceX Model V2.1.xlsx (Vlad-saved)

Tabs created (14): [list with cell counts]

Year header + offset (rows 4 & 5):
  Tab 1 Assumptions:  OK (D4=2025, AC4=2050, D5=0, AC5=25)
  [... through Tab 13 Valuation ...]

Assumptions tab content:
  Rows written: 300 (11 SECT, 47 SUB, 211 VAL, 31 YR)
  Inputs with MC range: [count]
  Inputs with fixed distribution: [count]

§4.2 anchor read-back: [each row with expected vs actual]

§4.1 universal checks:
  - Error scan: 0/0/0/0/0/0/0
  - Round-trip stability: 5 recalcs, bit-for-bit identical: PASS

Flags / open questions: [any items needing Vlad attention]

Status: PASS → write Claude Log entry → leave workbook for Vlad to save.
```

---

## §5 — Claude Log entry

Plugin appends to `Claude Log` row 2 (after §4 passes):

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| 2026-05-20 | 0 | Assumptions (built), Allocator + Launch Capacity + Customer Launch + Starlink + Starlink Capacity + ODC + AI Stack + Lunar Mars + Group P&L + OpEx + CapEx + Valuation (year header + offset row staged), Claude Log (created) | Built v2 baseline workbook from scratch. Created 14 tabs in locked sheet order. Year header (D=2025…AC=2050) and year-offset row (D=0…AC=25) staged as literal integers on every year-column tab. Assumptions tab populated from §3.6 inline build plan — 300 rows across 11 sections. Every input has Base Case + MC range + distribution + notes. All §4.2 anchors verified (starting cash $5B, F9 fleet 28, F9 price $111M, Mars/Moon R&D $700M, Starshield decay 0.25, Starshield rev/Gbps $164,699). Six Q4'25 corrections vs V30.5 applied. | Demand Curves tab not yet imported — Sprint 4 decides. | Sprint 1: Allocator skeleton + module shells (IN/OUT contract by label, module bodies empty). |

---

## §6 — Don't touch (out of scope)

- No formulas anywhere except literal integers on rows 4 and 5.
- No cross-tab references.
- No module body content. Tabs 2–13 are skeletons only.
- No Allocator IN/OUT contract row labels (Sprint 1).
- No conservation block (Sprint 9).
- No Demand Curves tab (Sprint 4 decision).
- No plugin-issued save commands (Vlad saves).
- No styling beyond: section/subsection fills on Assumptions, MC yellow highlight on AG–AJ, italic memos, bold + bottom border on row 4, light grey fill on row 5.

---

## §7 — Open thread (post-sprint considerations)

### §7.1 — Demand Curves tab
V9 carries the Demand Curves tab as source for Starlink bandwidth demand. Sprint 4 decides import vs sub-derivation vs drop. Sprint 0 leaves it out.

### §7.2 — Inputs flagged for Vlad-level confirmation pre-execution
- Mars carve-out % Base Case 15% (MC 3–35%) — confirm or push.
- ODC internal vs external compute split trajectory (R187/R188) — confirm or push.
- AI Stack product ramps (Cursor R191 / Grok consumer R195 / Grok enterprise R198) — confirm or push.
- Starship customer launch price $100M from 2027, −8%/yr decline (R64) — confirm or push.

If Vlad wants any reframed, edit §3.6 in-spec before Sprint 0 fires.

### §7.3 — Workbook naming convention (decision needed before Sprint 1)
Sprint 0 output is `SpaceX Model V2.1.xlsx`. Default for downstream: continue `V2.N` (Sprint 1 → V2.2, etc.). Confirm before Sprint 1 spec fires.

### §7.4 — Visual styling
Section/subsection fills, MC yellow highlight, italic memos, bold row 4, grey row 5. Anything more elaborate (freeze panes, conditional formatting, custom number formats) is out of scope for Sprint 0; available as a Sprint 0.5 patch.

---

## §8 — Execution sequence (plugin runs in this order)

Save commands NOT in this sequence — Vlad handles all saving.

1. **Pre-flight checks** (§3.0): confirm target workbook open + correctly named, workbook content-empty, kickoff confirmation block received.
2. **Rename default sheet** (whatever its locale-dependent name) to `Assumptions`. Create the remaining 13 tabs in §3.1 order. Verify all 14 tab names are exact.
3. **Write row 4 year header** (literal integers 2025–2050) on tabs 1–13. One write per tab. Apply bold + bottom border.
4. **Write row 5 year-offset helper** (literal integers 0–25) on tabs 1–13. One write per tab. Apply light grey fill.
5. **Walk §3.6 row-by-row**, writing to `Assumptions` tab per §3.3. Pace section by section; after each of the 11 sections, read back the last input row.
6. **Halt during step 5 if** any input missing MC range, any unrecognised distribution type, or any column-A label collision.
7. **Write Claude Log header row** (§3.4).
8. **Run §4 verification gate** against the live workbook. Halt on any failure.
9. **Write Claude Log Sprint 0 entry** (§5).
10. **Produce verification log** in chat (§4.4 format). Done. Vlad saves the workbook.

---

## §9 — Amendment log

- **2026-05-19 (initial draft)** — First sprint spec of rebuild v2. Scope: Assumptions tab + workbook standards + year header/offset pre-stage on 13 active tabs.
- **2026-05-19 (revision 1)** — Redesigned for Excel plugin context: blank-workbook starting state, §3.0 pre-flight, save-as as step 1, §3.1 default sheet rename, §8 execution sequence.
- **2026-05-19 (revision 2)** — Removed §0 Constitutional References + "How this spec is executed" intro: plugin executes against the spec alone.
- **2026-05-20 (revision 3)** — Spec made fully self-contained per Vlad's "henceforth" rule (no external file references — Build Plan content inlined as §3.6, 300 rows). Plugin save commands removed per Vlad's "I do the saving" rule (§3.5, §8, Rule 19 bullet all updated). Pre-flight checks restated against capability surface: no filesystem reads, no save-as, kickoff confirmation block required. Target workbook locked to `SpaceX Model V2.1.xlsx` to match Vlad's pre-saved file. Process rule applies to Sprint 1+ specs going forward.
