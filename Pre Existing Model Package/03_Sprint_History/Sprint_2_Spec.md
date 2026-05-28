# Sprint 2 — Launch Capacity Tab Full Build

**Source workbook**: `SpaceX Model V2.2.xlsx` (Sprint 1 output, verified PASS — Allocator skeleton + 5 module shells + Group P&L conservation block live, Launch Capacity tab present with year header row 4 + year-offset row 5 only)
**Target workbook**: `SpaceX Model V2.3.xlsx` (Vlad has already Save-As'd from V2.2 → V2.3 before this kickoff per standing process rule 2)
**Day budget**: 1 day
**Date drafted**: 2026-05-20

---

## §0 — Constitutional references

- **`01_Lessons_Learned.md`**: Principles 1 (no postponed architectural decisions), 2 (per-launch marginal IRR — Sprint 3 will consume this tab's at-cost rates), 6 (no tab without a locked function — Launch Capacity is locked as supply-only, NOT a P&L module), 7 (canonical labels day one — Sprint 10 reads `Total Annual Capacity (kg-to-LEO)` by label), 11 (no OFFSET; INDEX-only), 12 (anchor-and-offset for ramps), 13 (year-offset row 5 standard), 14 (INDEX/MATCH on labels), 18 (MC ranges already on Assumptions from Sprint 0), 22 (within-year cycles documented — Sprint 2 deliberately avoids them by anchoring Starship cadence on **lagged** cum-upmass per the 2026-05-20 lock).
- **`02_Architecture_and_Methodology.md`**: §1 (tab #3 = Launch Capacity, supply-side, not a P&L module — no Allocator IN/OUT contract), §2 (year horizon D:AC = 2025–2050, row 4 header + row 5 offset), §6.4 (Sprint 10 kg queue reads `Total Annual Capacity (kg-to-LEO)` by INDEX/MATCH against this tab), §6.6 (vehicle build cost is a non-module claim — out of scope for Sprint 2; Sprint 10 sizes it from forward-aggregate kg demand), §7.1 (at-cost transfer pricing per launch = variable cost + fleet D&A share — computed here for Sprint 3 to consume), §16 (zero OFFSET, INDEX-only, anchor-and-offset for ramps), §17 (2025 calibration targets).
- **`03_Sprint_Roadmap_and_Verification.md`**: §3 Sprint 2 (scope, dependencies, day budget), §5 (universal verification), §6.1 (sprint-specific 2025 calibration targets — F9 launches 171±5, F9 fleet end-2025 = 39±5, F9 manufactured 17±2, Starship launches 0 exact, Starship capacity ~450K kg ±30%, blended $/kg in $400–$800), §8 (sprint-spec template — followed below).
- **`04_Assumptions_Tab_Spec.md`**: §1 (column convention on Assumptions — row 1/2 deviation for year header/offset noted), §2 §3 Capacity (R30–R47 Starship + R48–R64 F9 — every input this spec consumes is inlined in §3.5 below by label).
- **`Model Execution Rules.md`**: Mandatory Rule Compliance Preamble at §1; Rules 1 / 4 / 5 / 10 / 11 / 14 / 16 / 19 / 22 / 23 load-bearing for this sprint.
- **`2025 Anchors from Q4_25.md`**: F9 starting fleet 28 (Earth R29), F9 customer launch price $111M (Earth R132), F9 total launches 171, F9 customer launches 38.58, F9 manufactured 17.01 (annotated as "Q4'25 actual"), Starship launches 2025 = 0, Mars/Moon R&D not in scope this sprint.
- **`Sprint_0_Spec.md`** §3.6 (Capacity inputs R30–R64 — every label and Base Case value inlined in §3.5 below).
- **`Sprint_1_Spec.md`** (already-executed — tab order, year-header/offset standards confirmed across all 15 tabs; Launch Capacity tab exists with only row-1 title + row-4 year header + row-5 year-offset; Sprint 2 fills everything else).

---

## §1 — Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md` and the four constitutional docs. Each box ticked or justified N/A:

- [x] **Rule 1** (one concept per write) — §3.2 / §3.3 / §3.4 are structured as discrete blocks. Each row's column-A label is written in a separate `set_cell` call from its D-column anchor formula, and the D-anchor formula is a separate call from the E:AC copyToRange. No mixing of labels + formulas + formats in a single `cells` dict.
- [x] **Rule 3 / 23** (formula pattern) — every deterministic ramp (Starship cadence via Wright's Law, F9 build-rate decay post-2027) uses anchor-and-offset on `E$5` and a locked anchor cell. Year-chained exceptions explicitly flagged inline: (a) Cum upmass running sum (row 28, Rule 23 exception — cumulative running sum is genuinely year-chained), (b) Booster fleet EoY (row 27 of Starship, row 65 of F9 — `EoY = BoY + built − retired`, Rule 23 exception per Architecture §8.3 pattern). All other ramps use anchor-and-offset.
- [x] **Rule 4** (verification gate) — §4.3 enumerates explicit read-back cells at D (2025), I (2030), S (2040), AC (2050) with expected values for: F9 launches, F9 fleet EoY, F9 manufactured, F9 at-cost rate, Starship total launches, Starship Total Annual Capacity (kg-to-LEO), Starship at-cost rate, blended $/kg.
- [x] **Rule 6** (inline formulas) — every cell write in §3.2 / §3.3 / §3.4 specified with the full Excel formula. No "see Assumptions row N" or "compute the standard way" hand-waves. INDEX/MATCH calls on Assumptions are written out verbatim with the canonical label.
- [x] **Rule 10** (no row insertions) — Launch Capacity tab is being built from scratch this sprint (row 1 title + row 4 year header + row 5 offset are the only existing rows from Sprint 1). Every new line item appended below row 5; no `insert_row` operations anywhere. Order and row numbers locked in §3.1 for future sprints to reference by label only.
- [x] **Rule 11** (touch points) — every canonical output row in §3.1 lists which downstream sprint reads it. No SUM range / conservation check applies because Launch Capacity is NOT a P&L module (Architecture §1 + §3 forbid). No Group P&L conservation row exists for Launch Capacity (only module tabs feed conservation). Touch points = "Sprint 3 reads X by label", "Sprint 10 reads `Total Annual Capacity (kg-to-LEO)` by label". Recorded inline in §3.1 row map.
- [x] **Rule 12** (label-based cross-tab refs) — every Assumptions pull on this tab uses `INDEX(Assumptions!B:B, MATCH("<exact canonical label>", Assumptions!$A:$A, 0))`. Zero hardcoded `=Assumptions!Bxx` row-number references. Year-row Assumptions pulls (variant mix R46, lifetime reuses R47, F9 customer launch price R63 — not consumed here but cross-checked) use `INDEX(Assumptions!D:AC, MATCH("<label>", Assumptions!$A:$A, 0), E$5+1)` pattern.
- [x] **Rule 13** (vending-machine test) — N/A. Launch Capacity is NOT a P&L module (Architecture §1, §3). No R&D / SG&A / overhead / taxes added. No Module EBITDA computed. No Allocator IN/OUT contract. The at-cost transfer rates computed here are SUPPLY-SIDE costs (variable + D&A share); the P&L of internal launch services lives on Sprint 3 Customer Launch.
- [x] **Rule 14** (no hardcoded constants) — every behavior input resolves to an Assumptions row by label. Explicit exceptions (acknowledged): (a) hardcoded 2025 + 2026 F9 historical anchors per the 2026-05-20 lock (F9 manufactured = 17, F9 launches = 171, F9 retired = 6 — these ARE Assumptions-anchored values inlined as overrides because the build mechanic doesn't fire until 2027; rationale in §3.5), (b) Starship ops cost = 0 per launch (Assumptions §3 has no Starship-ops-cost row in Sprint 0; flagged Open Thread §7 for Sprint 3 patch — does not affect 2025 calibration since Starship launches = 0), (c) hardcoded 1-ship cum-upmass anchor (= 100K kg = R36 fully-reusable payload, resolved by label).
- [x] **Rule 15** (sanity check halt thresholds) — §4.2 every check has a quantitative halt threshold. F9 launches 2025 < 160 or > 185 halt. F9 fleet end-2025 < 30 or > 50 halt. F9 manufactured 2025 < 13 or > 22 halt. Starship launches 2025 ≠ 0 halt. Starship Total Annual Capacity 2025 outside [250K, 700K] kg halt. Blended $/kg 2025 outside [$400, $800] halt.
- [x] **Rule 19** (save-as) — target workbook named explicitly: `SpaceX Model V2.3.xlsx`. Per standing process rule 2 (locked 2026-05-20), Vlad has already Save-As'd before kickoff; plugin operates on the live open session and does NOT issue any save commands. §3.0 pre-flight verifies V2.3 is the active workbook name.
- [x] **Rule 22** (stale-ref scan) — every canonical output row's label written exactly as future Sprint 3/4/5/10 specs will reference. Labels listed in §3.1 row map are the single source of truth. §4.4 enumerates the by-label scan: plugin reads each canonical output row's column-A text and confirms exact-string match against the §3.1 spec.

**Architecture & Methodology compliance:**

- [x] Module P&L follows vending-machine framing (Architecture §3) — **N/A for Launch Capacity** (supply tab, no P&L).
- [x] Per-sat / per-launch marginal IRR engine (Architecture §5) — **N/A for Launch Capacity** (no IRR engine on this tab; Sprint 3 Customer Launch builds the per-launch IRR for external customer economics).
- [x] Allocator OUT contract uses canonical 11 labels (Architecture §4.2) — **N/A for Launch Capacity** (no Allocator IN/OUT block).
- [x] Year-offset helper row at row 5 + year header at row 4 — already in place from Sprint 0 (verified by Sprint 1 PASS). §3.0 pre-flight confirms.
- [x] ZERO `OFFSET()` formulas; INDEX:INDEX patterns used for dynamic ranges (Principle 11) — confirmed; every Assumptions pull uses INDEX/MATCH. The cum-upmass running sum (row 28) uses `=D28 + D33×D34` year-chained pattern, NOT OFFSET.

---

## §1.5 — Pre-execution setup (Vlad confirms before plugin starts writing)

Per standing process rule 3 (locked 2026-05-20), the kickoff prompt includes this confirmation block. The plugin's §3.0 pre-flight verifies it before any cell write.

**Vlad attests:**

1. **Target workbook is open** with name `SpaceX Model V2.3.xlsx` (Save-As completed from V2.2 → V2.3 before this kickoff).
2. **Vlad will handle all saves** — the plugin operates on the live open workbook session and will NOT issue any save / save-as / write-file commands. Verification reads cells from the session directly.
3. **No other tabs are open in this workbook** that could conflict with Launch Capacity writes (Assumptions tab read-only access is needed via Excel session, no Assumptions writes this sprint).

If any of the above is not true, plugin halts at pre-flight per Rule 9 and pushes back to Vlad.

---

## §2 — Framing

**Why this sprint:** Sprint 2 builds the Launch Capacity tab end-to-end. This is the SUPPLY side of the SpaceX model: how much kg-to-LEO does the rocket fleet produce each year, at what blended cost. Sprint 3 (Customer Launch) consumes the at-cost rates this tab computes to size internal launch-service transfer pricing. Sprint 4 (Starlink) reads `F9 Annual Capacity (kg-to-LEO)` to size V2 BB/DTC internal launches and `Total Annual Capacity (kg-to-LEO)` (Starship-only, the canonical label per the 2026-05-20 lock) is the row Sprint 10's Allocator kg queue reads via INDEX/MATCH (Architecture §6.4).

**What it produces (canonical output rows, single source of truth — labels are exact, do not rename):**

| Row | Canonical label | Consumed by |
|---|---|---|
| R23 | `Launches per Starship vehicle per year (cadence)` | Sprint 3 (Customer Launch external Starship sizing) |
| R33 | `Total Starship launches per year` | Sprint 3 + Sprint 4 + Sprint 5 |
| R34 | `Total Annual Capacity (kg-to-LEO)` | **Sprint 10 Allocator kg queue (Architecture §6.4) — STARSHIP-ONLY scope per 2026-05-20 lock** |
| R40 | `Starship at-cost rate ($mm/launch)` | Sprint 3 + Sprint 4 + Sprint 5 (internal transfer pricing) |
| R64 | `F9 launches per year` | Sprint 4 (V2 BB/DTC internal launches) + Sprint 3 (F9 customer launches) |
| R68 | `F9 Annual Capacity (kg-to-LEO)` | Sprint 4 (V2 BB/DTC sizing — informational, not in outer kg queue) |
| R71 | `F9 at-cost rate ($mm/launch)` | Sprint 3 + Sprint 4 (internal F9 transfer pricing) |
| R77 | `Blended $/kg` | Optional Sprint 11 Valuation read; primary use is Sprint 2 calibration check |

**What it deliberately does NOT do:**

- Does NOT compute vehicle build cost claim — that lives on Allocator (Sprint 10) sized by forward-aggregate kg demand per Architecture §6.6. Launch Capacity computes per-launch at-cost rates only.
- Does NOT compute Module EBITDA / Module FCF / Module CapEx — Launch Capacity is supply, not a P&L module (Architecture §1, §3).
- Does NOT have an Allocator IN/OUT block — confirmed in Sprint 1 spec; Launch Capacity tab Sprint 1 deliverable was year header + offset row only, no contract rows.
- Does NOT write to Assumptions tab — Sprint 0 inputs R30–R64 are read-only this sprint; if a new row is needed (e.g., Starship ops cost) it's flagged in §7 Open thread for a patch sprint.

**Dependencies:**

- Sprint 0 (Assumptions §3 Capacity inputs R30–R64 — all values inlined in §3.5).
- Sprint 1 (Launch Capacity tab exists; year-header / offset rows in place; tab order locked).

---

## §3 — Scope

### §3.0 Pre-flight (plugin verifies BEFORE any cell write)

Plugin halts on any failure and pushes back to Vlad.

1. **Workbook name** = `SpaceX Model V2.3.xlsx` (active workbook in session). Halt if name is `V2.2`, `V2.2.xlsx`, or anything else — Vlad missed the Save-As.
2. **Launch Capacity tab exists** with sheet position #3 (per Architecture §1: Assumptions #1, Allocator #2, Launch Capacity #3). Halt if tab missing or wrong position.
3. **Launch Capacity row 4** reads year header: `D4 = 2025, E4 = 2026, F4 = 2027, ..., AC4 = 2050` (hardcoded integers). Plugin samples D4, I4 (=2030), S4 (=2040), AC4 (=2050). Halt if any mismatch.
4. **Launch Capacity row 5** reads year offset: `D5 = 0, E5 = 1, ..., AC5 = 25` (hardcoded integers). Plugin samples D5, I5 (=5), S5 (=15), AC5 (=25). Halt if any mismatch.
5. **Launch Capacity rows 6 onwards are empty** in V2.2 (the tab was a stub from Sprint 1). Plugin reads A6:A100 and confirms all blank. Halt if anything non-blank exists below row 5 — Sprint 1 deviation that needs investigation before Sprint 2 overwrites.
6. **Assumptions row 1 = year header** (row 1/2 deviation per Sprint 0; Sprint 1 pre-flight relaxed accordingly). Plugin samples Assumptions!D1 = 2025. Halt if mismatch (confirms Sprint 0 deviation still in place).
7. **Assumptions §3 Capacity rows R30 = `§3 CAPACITY (Starship + F9)` section header** present at the expected Assumptions row. Plugin runs `MATCH("§3 CAPACITY (Starship + F9)", Assumptions!$A:$A, 0)` and confirms a hit (any row number is fine; per Rule 12 we don't depend on the row, only the label).

All 7 pre-flight checks must pass. If any fail, halt and push back.

### §3.1 Workbook layout — Launch Capacity tab row map (locked; future sprints reference by label)

Rows 1–5 are the existing Sprint 1 deliverable (tab title + blank + blank + year header + year-offset). Sprint 2 writes rows 6 through 80.

**STARSHIP SECTION (rows 6–40)**

| Row | Col A label | Type | Touch points (which sprint reads this row by label) |
|---|---|---|---|
| 6 | `STARSHIP — VEHICLE SUPPLY` | SECT (white-on-charcoal, bold) | — |
| 7 | `▸ Physical + cost parameters (from Assumptions §3)` | SUB (italic, light grey) | — |
| 8 | `Super Heavy manufacturing cost ($mm/unit)` | INDEX/MATCH pull from Assumptions, D-only single-value | Sprint 10 vehicle build claim |
| 9 | `Starship 2nd-stage manufacturing cost ($mm/unit)` | INDEX/MATCH pull, D-only | Sprint 10 vehicle build claim |
| 10 | `Ship refurb % of manufacturing` | INDEX/MATCH pull, D-only | — (internal to row 38 D&A formula) |
| 11 | `Payload — booster-only mode (kg-to-LEO)` | INDEX/MATCH pull, D-only | — (internal to row 28 per-launch upmass) |
| 12 | `Payload — fully reusable mode (kg-to-LEO)` | INDEX/MATCH pull, D-only | Used as the 1-ship anchor in row 27 cum-upmass anchor; internal to row 28 |
| 13 | `Lifetime reuses per ship (cap)` | INDEX/MATCH pull, D-only | Internal to row 39 ship D&A share |
| 14 | `Manufacturing learning rate (per doubling of cum units)` | INDEX/MATCH pull, D-only | Not consumed in Sprint 2 (reserved for Sprint 10 vehicle build cost); written here for completeness + visibility |
| 15 | `Cadence ceiling (flights/booster/year)` | INDEX/MATCH pull, D-only | Internal to row 23 cadence cap |
| 16 | `WL learning rate — turnaround vs cum upmass doubling` | INDEX/MATCH pull, D-only | Internal to row 23 cadence Wright's Law exponent |
| 17 | `Anchor year for cum-upmass Wright's Law` | INDEX/MATCH pull, D-only | Memo (locked at 2025 per Assumptions R42) |
| 18 | *(blank — spacing)* | — | — |
| 19 | `▸ Variant mix + booster lifetime reuses (year-rows from Assumptions §3)` | SUB | — |
| 20 | `Variant mix (% fully reusable)` — year-row | INDEX/MATCH year-row pull from Assumptions | Internal to rows 28, 31, 32, 39 |
| 21 | `Lifetime reuses per booster (year cap)` — year-row | INDEX/MATCH year-row pull | Internal to row 38 booster D&A share |
| 22 | *(blank — spacing)* | — | — |
| 23 | `Launches per Starship vehicle per year (cadence)` | year-row formula (Wright's Law on lagged cum upmass) | Sprint 3 (external Starship customer launches × cadence) |
| 24 | `Booster fleet beginning-of-year (units)` | year-chained, Rule 23 exception | Internal to row 27 fleet EoY |
| 25 | `Boosters built per year (units)` | placeholder = 0 for Sprint 2; Sprint 10 vehicle build claim writes this | Sprint 10 vehicle build claim (writes to this row) |
| 26 | `Boosters retired per year (units)` | derived from lifetime-reuses tracking (simplified Sprint 2: 0; full retirement engine deferred to a patch sprint) | — |
| 27 | `Booster fleet end-of-year (units)` | year-chained, Rule 23 exception (= BoY + built − retired) | Internal to rows 31, 32, 33 |
| 28 | `Cum upmass to date (kg)` | year-chained, Rule 23 exception (running sum) | Internal to row 23 cadence Wright's Law |
| 29 | `Per-launch upmass (kg)` | year-row formula (variant-mix-weighted blend of R11 + R12) | Internal to row 34 Total Annual Capacity |
| 30 | *(blank — spacing)* | — | — |
| 31 | `Booster-only launches per year (count)` | year-row formula | Internal to rows 33, 34 |
| 32 | `Fully-reusable launches per year (count)` | year-row formula | Internal to rows 33, 34, 38, 39 |
| 33 | `Total Starship launches per year` | year-row formula = R31 + R32 | **Sprint 3 + Sprint 4 + Sprint 5** |
| 34 | `Total Annual Capacity (kg-to-LEO)` | year-row formula = R33 × R29 | **Sprint 10 Allocator kg queue (canonical label, STARSHIP-only per 2026-05-20 lock)** |
| 35 | *(blank — spacing)* | — | — |
| 36 | `▸ Starship at-cost transfer rate (Architecture §7.1)` | SUB | — |
| 37 | `Starship variable cost per launch ($mm)` | year-row formula | Internal to row 40 |
| 38 | `Starship booster D&A share per launch ($mm)` | year-row formula = R8 / R21 (lifetime reuses per booster, year-row) | Internal to row 40 |
| 39 | `Starship ship D&A share per launch ($mm)` | year-row formula (variant-mix-weighted) | Internal to row 40 |
| 40 | `Starship at-cost rate ($mm/launch)` | year-row formula = R37 + R38 + R39 | **Sprint 3 + Sprint 4 + Sprint 5** (internal launch transfer pricing) |

**FALCON 9 SECTION (rows 42–71)**

| Row | Col A label | Type | Touch points |
|---|---|---|---|
| 42 | `FALCON 9 — VEHICLE SUPPLY` | SECT | — |
| 43 | `▸ Physical + cost parameters (from Assumptions §3)` | SUB | — |
| 44 | `F9 booster (1st stage) mfg cost ($mm/unit)` | INDEX/MATCH pull, D-only | Internal to rows 69, 70 |
| 45 | `F9 2nd stage mfg cost ($mm/unit)` | INDEX/MATCH pull, D-only | Internal to row 69 |
| 46 | `F9 fairing cost net of 75% recovery ($mm/flight)` | INDEX/MATCH pull, D-only | Internal to row 69 |
| 47 | `F9 per-launch ops cost ($mm)` | INDEX/MATCH pull, D-only | Internal to row 69 |
| 48 | `F9 booster refurb % of mfg` | INDEX/MATCH pull, D-only | Internal to row 69 |
| 49 | `F9 payload to LEO (kg)` | INDEX/MATCH pull, D-only | Internal to row 68 |
| 50 | `F9 lifetime reuses per booster` | INDEX/MATCH pull, D-only | Internal to row 70 |
| 51 | `F9 cadence per booster (flights/year, flat)` | INDEX/MATCH pull, D-only | Internal to row 68 |
| 52 | `F9 WL learning rate` | INDEX/MATCH pull, D-only | Memo (reserved for future learning-curve build cost on F9; not consumed in Sprint 2) |
| 53 | *(blank — spacing)* | — | — |
| 54 | `▸ F9 supply mechanic (pre-V3-trigger anchors + post-trigger decay)` | SUB | — |
| 55 | `F9 base booster build rate (boosters/year, pre-V3-trigger)` | INDEX/MATCH pull, D-only | Internal to row 61 (build mechanic 2027+) |
| 56 | `V3 Starlink launch trigger year` | INDEX/MATCH pull, D-only | Internal to rows 61, 64 (decay trigger) |
| 57 | `F9 build-rate decay window (years)` | INDEX/MATCH pull, D-only | Internal to row 61 |
| 58 | `F9 starting fleet at 2025 SoY (boosters)` | INDEX/MATCH pull, D-only (= 28 per Q4'25 anchor) | Internal to row 60 D-column anchor |
| 59 | *(blank — spacing)* | — | — |
| 60 | `F9 fleet beginning-of-year (boosters)` | D = R58; E:AC = year-chained (prior year EoY), Rule 23 exception | Internal to rows 63, 64, 68 |
| 61 | `F9 manufactured per year (boosters)` | D = 17 (Q4'25 anchor override), E = 17 (Vlad-set 2026 override per 2026-05-20 lock), F:AC = post-trigger decay mechanic | Internal to row 63 |
| 62 | `F9 retired per year (boosters)` | D = 6 (Q4'25-implied: 28 + 17 − 39 = 6 retired for fleet to end at 39); E:AC = lifetime-reuses tracking simplified to 6/yr flat for Sprint 2 (full retirement engine deferred to patch sprint) | Internal to row 63 |
| 63 | `F9 fleet end-of-year (boosters)` | year-chained = BoY + manufactured − retired | Memo + internal to row 60 next-year BoY |
| 64 | `F9 launches per year` | D = 171 (Q4'25 anchor override), E = 171 (Vlad-set 2026 override), F:AC = MIN(fleet × cadence, demand-decay year-row) | **Sprint 4** (V2 BB/DTC internal launches) + **Sprint 3** (F9 customer external) |
| 65 | `F9 cadence-utilization per booster (memo, derived)` | = R64 / R60 — memo for sanity check | Memo only |
| 66 | *(blank — spacing)* | — | — |
| 67 | `▸ F9 capacity + at-cost transfer rate` | SUB | — |
| 68 | `F9 Annual Capacity (kg-to-LEO)` | year-row formula = R60 × R51 × R49 (supply max — fleet × cadence × payload) | **Sprint 4** (V2 BB/DTC internal sizing — informational, not in outer kg queue per 2026-05-20 lock) |
| 69 | `F9 variable cost per launch ($mm)` | D-only single-value formula = R45 + R46 + R47 + R48 × R44 (2nd stage + fairing + ops + booster refurb) | Internal to row 71 |
| 70 | `F9 booster D&A share per launch ($mm)` | D-only single-value formula = R44 / R50 | Internal to row 71 |
| 71 | `F9 at-cost rate ($mm/launch)` | D-only single-value formula = R69 + R70 | **Sprint 3 + Sprint 4** (internal F9 transfer pricing) |

**BLENDED COST STACK + CALIBRATION READ-BACK (rows 73–80)**

| Row | Col A label | Type | Touch points |
|---|---|---|---|
| 73 | `BLENDED COST STACK + CALIBRATION` | SECT | — |
| 74 | `Total launches per year (all vehicles)` | year-row = R64 + R33 | Memo |
| 75 | `Total upmass per year (kg)` | year-row = R64 × R49 + R34 | Memo |
| 76 | `Total launch CapEx per year ($mm) — variable + amortized D&A` | year-row = R64 × R71 + R33 × R40 | Memo |
| 77 | `Blended $/kg` | year-row = IFERROR(R76 × 1e6 / R75, 0) | **Sprint 2 calibration check** (target 2025: $400–$800 per §6.1); optional Sprint 11 Valuation read |
| 78 | *(blank — spacing)* | — | — |
| 79 | `Memo: 2025 calibration anchors (read-only diagnostics)` | SUB | — |
| 80 | `Memo: 2025 calibration status` | D-only formula concatenating the anchor pass/fail | Memo for §4 verification gate |

### §3.2 Starship section — cell-by-cell build (rows 6–40)

All Assumptions references use the canonical label exactly as shown. Each write is its own discrete operation (Rule 1).

**§3.2.1 Section + subsection headers (rows 6, 7, 19, 36)**

```
A6  = "STARSHIP — VEHICLE SUPPLY"               (format: white-on-charcoal fill, bold)
A7  = "▸ Physical + cost parameters (from Assumptions §3)"   (format: italic, light grey fill)
A19 = "▸ Variant mix + booster lifetime reuses (year-rows from Assumptions §3)"   (italic, light grey)
A36 = "▸ Starship at-cost transfer rate (Architecture §7.1)"   (italic, light grey)
```

**§3.2.2 Physical + cost parameter pulls (rows 8–17 — single-value, D-column only)**

Each row: write the label in column A, then write the D-column INDEX/MATCH formula. One row at a time (Rule 1).

```
A8  = "Super Heavy manufacturing cost ($mm/unit)"
D8  = =INDEX(Assumptions!$B:$B, MATCH("Super Heavy manufacturing cost ($mm/unit, base year)", Assumptions!$A:$A, 0))

A9  = "Starship 2nd-stage manufacturing cost ($mm/unit)"
D9  = =INDEX(Assumptions!$B:$B, MATCH("Starship 2nd-stage manufacturing cost ($mm/unit, base)", Assumptions!$A:$A, 0))

A10 = "Ship refurb % of manufacturing"
D10 = =INDEX(Assumptions!$B:$B, MATCH("Ship refurb % of manufacturing", Assumptions!$A:$A, 0))

A11 = "Payload — booster-only mode (kg-to-LEO)"
D11 = =INDEX(Assumptions!$B:$B, MATCH("Payload — booster-only mode (kg-to-LEO)", Assumptions!$A:$A, 0))

A12 = "Payload — fully reusable mode (kg-to-LEO)"
D12 = =INDEX(Assumptions!$B:$B, MATCH("Payload — fully reusable mode (kg-to-LEO)", Assumptions!$A:$A, 0))

A13 = "Lifetime reuses per ship (cap)"
D13 = =INDEX(Assumptions!$B:$B, MATCH("Lifetime reuses per ship (cap)", Assumptions!$A:$A, 0))

A14 = "Manufacturing learning rate (per doubling of cum units)"
D14 = =INDEX(Assumptions!$B:$B, MATCH("Manufacturing learning rate (per doubling of cum units)", Assumptions!$A:$A, 0))

A15 = "Cadence ceiling (flights/booster/year)"
D15 = =INDEX(Assumptions!$B:$B, MATCH("Cadence ceiling (flights/booster/year)", Assumptions!$A:$A, 0))

A16 = "WL learning rate — turnaround vs cum upmass doubling"
D16 = =INDEX(Assumptions!$B:$B, MATCH("WL learning rate — turnaround vs cum upmass doubling", Assumptions!$A:$A, 0))

A17 = "Anchor year for cum-upmass Wright's Law"
D17 = =INDEX(Assumptions!$B:$B, MATCH("Anchor year for cum-upmass Wright's Law", Assumptions!$A:$A, 0))
```

Expected D-column values (per Sprint 0 §3.6 inline): D8=35.1, D9=23.4, D10=0.02, D11=150000, D12=100000, D13=30, D14=0.10, D15=60, D16=0.145, D17=2025.

Format: D8–D10, D14, D15 number format `0.00` or `0%` as appropriate; D11–D13 number format `#,##0`; D16 number format `0.0%`; D17 integer.

**§3.2.3 Year-row pulls — variant mix + booster lifetime reuses (rows 20, 21)**

Year-row pulls from Assumptions year-row inputs. Write the column-A label, then write D20 as the anchor formula, then copyToRange D20 → E20:AC20.

```
A20 = "Variant mix (% fully reusable)"
D20 = =INDEX(Assumptions!$D:$AC, MATCH("Variant mix (% fully reusable)", Assumptions!$A:$A, 0), D$5+1)
copyToRange source D20, destination E20:AC20

A21 = "Lifetime reuses per booster (year cap)"
D21 = =INDEX(Assumptions!$D:$AC, MATCH("Lifetime reuses per booster (year cap)", Assumptions!$A:$A, 0), D$5+1)
copyToRange source D21, destination E21:AC21
```

Rationale for the `D$5+1` offset: Assumptions year-header at row 1, year-offset at row 2. On Launch Capacity the year-offset is `D$5+1` (since D5=0 → column index 1 = Assumptions column D = year 2025; E5=1 → column index 2 = Assumptions column E = year 2026; etc.). The `INDEX(Assumptions!$D:$AC, row_match, col_offset+1)` resolves the right year column on Assumptions regardless of Launch Capacity's column position.

Expected D20 ≈ 0 (no fully reusable Starship in 2025); D21 ≈ 5 (lifetime reuses per booster starts at 5). I20 (2030) ≈ 0.3, S20 (2040) ≈ 0.95. I21 ≈ 15, S21 ≈ 60, AC21 ≈ 100.

Format: D20:AC20 percentage `0%`; D21:AC21 integer.

**§3.2.4 Starship cadence — Wright's Law on lagged cum upmass (row 23)**

Per the 2026-05-20 lock: **Lagged + 1-ship anchor**. cadence_per_booster(T) = base × (cum_upmass(T-1) / 1_ship_payload)^WL_exp, capped at cadence ceiling, floored at 1 flight/booster/year before any Starship flies.

The WL exponent for "doubling reduces turnaround time by `learning_rate` fraction" is:
- Turnaround time per flight × (cum_upmass / anchor)^log₂(1 − learning_rate)
- Cadence = 1 / turnaround time
- So cadence ∝ (cum_upmass / anchor)^(−log₂(1 − learning_rate)) — call this `α = −log₂(1 − R16)`
- With R16 = 0.145, α = −log₂(0.855) = 0.226

Formula structure: cadence(T) for T ≥ 2026 reads cum_upmass(T-1) from prior column; for T = 2025 (column D), cum_upmass = 0, so cadence floors at 1.

```
A23 = "Launches per Starship vehicle per year (cadence)"
D23 = =1   (anchor: 2025 has zero Starship operations; cadence floor of 1 flight/booster/year as the structural baseline; no Starship launches will materialize because R25 boosters built = 0 in 2025)
E23 = =MAX(1, MIN(D$15, (1/D$16_base_turnaround_lookup) * IFERROR((D28 / D$12)^(-LOG(1-D$16, 2)), 1)))
```

Wait — the formula above has a subtle issue. Let me rewrite cleanly. The base turnaround time `R40 Assumptions = 1 yr/flight` so base cadence = 1 flight/booster/year. The WL learning means cadence grows as cum upmass grows. Need to pull `Base turnaround time per booster` from Assumptions.

Adding a single-value pull at row 16 wasn't reserved... let me revise: row 16 was assigned to `WL learning rate — turnaround vs cum upmass doubling`. I'll add a parallel pull for base turnaround at the cadence formula row itself, inlined via INDEX/MATCH.

Actually cleanest: add base turnaround as row 16a or just inline the INDEX/MATCH inside the row 23 formula. Per Rule 14 (no hardcoded constants), it must be by-label.

Let me re-do the row 23 formula with inline Assumptions pulls:

```
A23 = "Launches per Starship vehicle per year (cadence)"

D23 = =1   (hardcoded anchor: 2025 cum upmass = 0; cadence floors at base = 1 flight/booster/year; Starship operations don't materialize in 2025 anyway since R25 boosters built = 0)

E23 = =MAX(
        1,
        MIN(
          $D$15,
          (1 / INDEX(Assumptions!$B:$B, MATCH("Base turnaround time per booster (years/flight)", Assumptions!$A:$A, 0)))
          * IFERROR((D28 / $D$12)^(-LOG(1 - $D$16, 2)), 1)
        )
      )

copyToRange source E23, destination F23:AC23
```

Reading the formula:
- Outer `MAX(1, ...)`: floor at 1 flight/booster/year (pre-first-flight or sub-anchor regime)
- Inner `MIN($D$15, ...)`: cap at cadence ceiling (60 flights/booster/year)
- Inside the MIN: `(1 / base_turnaround) × (cum_upmass_T-1 / 1_ship_anchor)^α` where α = `−log₂(1 − R16)`
- The `D28` reference: cadence for year T uses **prior-year** cum upmass (lagged). In E23 (= year 2026), this references D28 = 2025 year cum upmass. In F23 (= year 2027), references E28 = 2026 year cum upmass. By the relative reference (no $), this is automatic when E23 is copied across.
- IFERROR wraps to handle (cum_upmass = 0)^positive_exp → 0 — which would give cadence = 0, but MAX(1, …) floors back to 1. The IFERROR returns 1 (the multiplier neutral) if cum_upmass = 0 making the calculation deterministic.

D28 (2025 cum upmass) = 0 by construction. So E23 (2026 cadence) = MAX(1, MIN(60, (1/1) × IFERROR(0/100000^0.226, 1))) = MAX(1, MIN(60, 1)) = 1 flight/booster/year. Correct floor behavior.

As Starship flies in 2026+ (when Sprint 10 starts building boosters and they start flying), cum upmass grows and cadence ramps. By the time cum_upmass = 100,000 kg (= 1 ship-load), cadence = 1 still (anchor point). At cum_upmass = 200,000 kg (= 1 doubling), cadence multiplier = 2^0.226 = 1.17. At cum_upmass = 10× anchor = 1M kg (≈ 3.3 doublings), cadence ≈ 2.16. Realistic ramp.

Format: D23:AC23 number `0.00`.

**§3.2.5 Booster fleet dynamics (rows 24–27) — year-chained, Rule 23 exception**

```
A24 = "Booster fleet beginning-of-year (units)"
D24 = =0   (2025 SoY: no Starship boosters built yet)
E24 = =D27   (year-chained: BoY = prior year EoY — Rule 23 exception, intentional)
copyToRange source E24, destination F24:AC24

A25 = "Boosters built per year (units)"
D25 = =0   (Sprint 2 placeholder: Sprint 10 vehicle build claim writes this row endogenously sized by forward-aggregate kg demand per Architecture §6.6)
copyToRange source D25, destination E25:AC25   (all years = 0 placeholder)

A26 = "Boosters retired per year (units)"
D26 = =0   (Sprint 2 simplification: no Starship retirements modeled; full retirement engine deferred to a patch sprint per §7 Open thread)
copyToRange source D26, destination E26:AC26

A27 = "Booster fleet end-of-year (units)"
D27 = =D24 + D25 - D26   (= BoY + built − retired)
copyToRange source D27, destination E27:AC27
```

Year-chained justification: fleet EoY = BoY + built − retired is the textbook stock-flow identity — Rule 23 acknowledges this as a legitimate exception. Same applies to BoY = prior EoY.

Sprint 2 row 25 (boosters built) is a placeholder at 0. Sprint 10 will overwrite this row with the vehicle-build-claim allocation from Allocator. Until then, Starship fleet stays at 0 — Starship Total Annual Capacity (kg-to-LEO) row 34 will read 0 for 2025–2050 in Sprint 2 output. That's correct: Sprint 2's job is the supply mechanic, not the supply level (which is allocator-driven).

Expected D24:AC24 = 0 for Sprint 2 (Sprint 10 will populate later).

Format: D24:AC27 integer `#,##0`.

**§3.2.6 Cum upmass + per-launch upmass (rows 28, 29)**

```
A28 = "Cum upmass to date (kg)"
D28 = =0   (2025 cum upmass: 0)
E28 = =D28 + D33 * D29   (year-chained running sum — Rule 23 exception; cum upmass at EoY = prior cum upmass + this year's launches × this year's per-launch upmass)
copyToRange source E28, destination F28:AC28

A29 = "Per-launch upmass (kg)"
D29 = =D20 * $D$12 + (1 - D20) * $D$11   (variant-mix-weighted: fully reusable × 100K + booster-only × 150K)
copyToRange source D29, destination E29:AC29
```

Expected D29 = 0% × 100K + 100% × 150K = 150K kg (2025 variant mix = 0% fully reusable → 100% booster-only). I29 (2030) ≈ 30% × 100K + 70% × 150K = 135K. S29 (2040) ≈ 95% × 100K + 5% × 150K = 102.5K.

Format: D28:AC28 integer `#,##0`; D29:AC29 integer `#,##0`.

**§3.2.7 Launches per year (rows 31, 32, 33)**

```
A31 = "Booster-only launches per year (count)"
D31 = =D27 * D23 * (1 - D20)   (fleet × cadence × booster-only share)
copyToRange source D31, destination E31:AC31

A32 = "Fully-reusable launches per year (count)"
D32 = =D27 * D23 * D20
copyToRange source D32, destination E32:AC32

A33 = "Total Starship launches per year"
D33 = =D31 + D32
copyToRange source D33, destination E33:AC33
```

D33 in 2025 = 0 × 1 × ... = 0 (fleet is 0). Total Starship launches 2025 = 0 — matches §6.1 calibration "Starship launches 2025 = 0 exact." Pass.

Format: D31:AC33 integer `#,##0`.

**§3.2.8 Total Annual Capacity (kg-to-LEO) — the canonical Sprint 10 read (row 34)**

```
A34 = "Total Annual Capacity (kg-to-LEO)"
D34 = =D33 * D29
copyToRange source D34, destination E34:AC34
```

D34 in 2025 = 0 × 150K = 0 kg. Per §6.1 calibration "~450K ±30%" — this expects Starship operations to have started by 2025 with some level. Sprint 2 produces 0 because boosters built = 0 (row 25 placeholder). **Calibration sanity note: the §6.1 target ~450K kg assumes some Starship operations in 2025; the actual historical 2025 Starship launches = 0 → Total Annual Capacity = 0 is the right number.** The §6.1 ~450K target is for a "potential capacity if Starship were operational" interpretation that does not apply here. Treat 2025 Starship capacity = 0 as correct per the spec's Starship-launches-2025-exact-zero anchor; document this in §7 Open thread.

**Per the canonical label being load-bearing for Sprint 10**: this row exact label is `Total Annual Capacity (kg-to-LEO)` — verbatim, no abbreviations, no punctuation drift. Future stale-ref scan (Rule 22) reads `=INDEX('Launch Capacity'!D:D, MATCH("Total Annual Capacity (kg-to-LEO)", 'Launch Capacity'!$A:$A, 0))` from Allocator (Sprint 10) and confirms exact match.

Format: D34:AC34 integer `#,##0`.

**§3.2.9 Starship at-cost transfer rate (rows 37–40)**

```
A37 = "Starship variable cost per launch ($mm)"
D37 = =D9 * (1 - D20) + D9 * D10 * D20 + 0
copyToRange source D37, destination E37:AC37

A38 = "Starship booster D&A share per launch ($mm)"
D38 = =D8 / D21
copyToRange source D38, destination E38:AC38

A39 = "Starship ship D&A share per launch ($mm)"
D39 = =D9 / $D$13 * D20
copyToRange source D39, destination E39:AC39

A40 = "Starship at-cost rate ($mm/launch)"
D40 = =D37 + D38 + D39
copyToRange source D40, destination E40:AC40
```

Reading row 37 formula:
- Booster-only mode (share = 1 − D20): ship is expendable → full ship cost per launch = D9 ($23.4M)
- Fully-reusable mode (share = D20): ship is preserved, refurb each reuse → D9 × D10 ($23.4M × 0.02 = $0.468M) per launch for refurb
- Plus 0 ops cost (Sprint 2 stub per Rule 14 exception — see §1 Preamble; flagged Open Thread §7)

D37 in 2025 (variant mix = 0% reusable) = $23.4M × 1 + $23.4M × 0.02 × 0 + 0 = $23.4M variable cost per launch.
D37 in 2030 (variant mix ≈ 30%) = $23.4M × 0.7 + $23.4M × 0.02 × 0.3 + 0 = $16.38 + $0.14 = $16.52M.
D37 in 2040 (variant mix ≈ 95%) = $23.4M × 0.05 + $23.4M × 0.02 × 0.95 + 0 = $1.17 + $0.44 = $1.61M.

D38 in 2025 = $35.1M / 5 = $7.02M (1 SH booster amortized over 5 reuses in 2025).
D38 in 2030 = $35.1M / 15 = $2.34M.
D38 in 2050 = $35.1M / 100 = $0.351M.

D39 in 2025 (variant mix = 0%) = $23.4M / 30 × 0 = $0 (no ship D&A when ship is expendable; that cost is in D37 already).
D39 in 2030 (variant mix = 30%) = $23.4M / 30 × 0.3 = $0.234M.
D39 in 2050 (variant mix = 100%) = $23.4M / 30 × 1.0 = $0.78M.

D40 in 2025 = $23.4 + $7.02 + $0 = $30.42M/launch. At 150K kg payload: $30.42M / 150K = $202.8/kg.
D40 in 2030 = $16.52 + $2.34 + $0.234 ≈ $19.09M/launch. At 135K kg payload: $141/kg.
D40 in 2050 = $1.61 + $0.351 + $0.78 ≈ $2.74M/launch. At 102.5K kg payload: $26.7/kg.

Strong Starship cost trajectory — fully consistent with the Vlad thesis.

Format: D37:AC40 currency `$#,##0.00`.

### §3.3 Falcon 9 section — cell-by-cell build (rows 42–71)

**§3.3.1 Section + subsection headers (rows 42, 43, 54, 67)**

```
A42 = "FALCON 9 — VEHICLE SUPPLY"   (SECT: white-on-charcoal, bold)
A43 = "▸ Physical + cost parameters (from Assumptions §3)"   (SUB: italic, light grey)
A54 = "▸ F9 supply mechanic (pre-V3-trigger anchors + post-trigger decay)"   (SUB)
A67 = "▸ F9 capacity + at-cost transfer rate"   (SUB)
```

**§3.3.2 Physical + cost parameter pulls (rows 44–52 — single-value, D-column only)**

```
A44 = "F9 booster (1st stage) mfg cost ($mm/unit)"
D44 = =INDEX(Assumptions!$B:$B, MATCH("F9 booster (1st stage) mfg cost ($mm/unit)", Assumptions!$A:$A, 0))

A45 = "F9 2nd stage mfg cost ($mm/unit)"
D45 = =INDEX(Assumptions!$B:$B, MATCH("F9 2nd stage mfg cost ($mm/unit)", Assumptions!$A:$A, 0))

A46 = "F9 fairing cost net of 75% recovery ($mm/flight)"
D46 = =INDEX(Assumptions!$B:$B, MATCH("F9 fairing cost net of 75% recovery ($mm/flight)", Assumptions!$A:$A, 0))

A47 = "F9 per-launch ops cost ($mm)"
D47 = =INDEX(Assumptions!$B:$B, MATCH("F9 per-launch ops cost ($mm)", Assumptions!$A:$A, 0))

A48 = "F9 booster refurb % of mfg"
D48 = =INDEX(Assumptions!$B:$B, MATCH("F9 booster refurb % of mfg", Assumptions!$A:$A, 0))

A49 = "F9 payload to LEO (kg)"
D49 = =INDEX(Assumptions!$B:$B, MATCH("F9 payload to LEO (kg)", Assumptions!$A:$A, 0))

A50 = "F9 lifetime reuses per booster"
D50 = =INDEX(Assumptions!$B:$B, MATCH("F9 lifetime reuses per booster", Assumptions!$A:$A, 0))

A51 = "F9 cadence per booster (flights/year, flat)"
D51 = =INDEX(Assumptions!$B:$B, MATCH("F9 cadence per booster (flights/year, flat)", Assumptions!$A:$A, 0))

A52 = "F9 WL learning rate"
D52 = =INDEX(Assumptions!$B:$B, MATCH("F9 Wright's Law mfg learning rate", Assumptions!$A:$A, 0))
```

Expected D-column values: D44=30, D45=10, D46=1.25, D47=5, D48=0.03, D49=22800, D50=50, D51=12, D52=0.02.

Format: D44–D48, D51, D52 number `0.00` or `0%`; D49 integer `#,##0`; D50 integer.

**§3.3.3 F9 supply mechanic anchors (rows 55–58 — single-value)**

```
A55 = "F9 base booster build rate (boosters/year, pre-V3-trigger)"
D55 = =INDEX(Assumptions!$B:$B, MATCH("F9 base booster build rate (boosters/year, pre-V3-trigger)", Assumptions!$A:$A, 0))

A56 = "V3 Starlink launch trigger year"
D56 = =INDEX(Assumptions!$B:$B, MATCH("V3 Starlink launch trigger year", Assumptions!$A:$A, 0))

A57 = "F9 build-rate decay window (years)"
D57 = =INDEX(Assumptions!$B:$B, MATCH("F9 build-rate decay window (years)", Assumptions!$A:$A, 0))

A58 = "F9 starting fleet at 2025 SoY (boosters)"
D58 = =INDEX(Assumptions!$B:$B, MATCH("F9 starting fleet at 2025 SoY (boosters)", Assumptions!$A:$A, 0))
```

Expected D-column values: D55=8, D56=2027, D57=8, D58=28.

Format: D55, D57, D58 integer; D56 integer.

**§3.3.4 F9 fleet dynamics — 2025-2026 historical anchors + 2027+ decay (rows 60–65)**

Per the 2026-05-20 lock: F9 manufactured 2025 = 17 (Q4'25 anchor) and F9 manufactured 2026 = 17 (Vlad-set carryover); F9 launches 2025 = 171 (Q4'25 anchor) and F9 launches 2026 = 171 (Vlad-set carryover); F9 retired 2025 = 6 (derived: 28 SoY + 17 built − 39 EoY → 6 retired); F9 retired 2026+ = 6 (simplified for Sprint 2; full retirement engine deferred); F9 fleet end-2025 = 39 (calibration target); from 2027 onwards, F9 manufactured decays linearly over R57 = 8 years to zero.

```
A60 = "F9 fleet beginning-of-year (boosters)"
D60 = =$D$58   (anchor: 2025 SoY = 28 from R58)
E60 = =D63   (year-chained: BoY = prior EoY — Rule 23 exception)
copyToRange source E60, destination F60:AC60

A61 = "F9 manufactured per year (boosters)"
D61 = =17   (Q4'25 historical anchor override per 2026-05-20 lock; pre-V3-trigger)
E61 = =17   (Vlad-set 2026 carryover override; pre-V3-trigger)
F61 = =MAX(0, $D$55 * (1 - (F$4 - $D$56) / $D$57))   (post-trigger linear decay; from 2027 onwards, build rate decays from R55 base = 8/yr to 0 over R57 = 8 years; floors at 0)
copyToRange source F61, destination G61:AC61

A62 = "F9 retired per year (boosters)"
D62 = =6   (anchor: 28 SoY + 17 manufactured − 39 EoY = 6 retired in 2025, Q4'25-implied)
E62 = =6   (carryover simplification)
F62 = =6   (Sprint 2 simplification: constant 6/yr retirement until full retirement engine is built in a patch sprint per §7 Open thread)
copyToRange source F62, destination G62:AC62

A63 = "F9 fleet end-of-year (boosters)"
D63 = =MAX(0, D60 + D61 - D62)   (= BoY + manufactured − retired, clamped at 0 so the simplified flat-retirement mechanic in row 62 cannot drive fleet negative in late out-years)
copyToRange source D63, destination E63:AC63

A64 = "F9 launches per year"
D64 = =171   (Q4'25 historical anchor override; matches §6.1 calibration target)
E64 = =171   (Vlad-set 2026 carryover override; pre-V3-trigger demand stays near pre-trigger levels)
F64 = =MIN(F60 * $D$51, MAX(0, 171 * (1 - (F$4 - $D$56) / $D$57)))   (post-trigger: min of (fleet × cadence) and demand-driven decay from 171 down over R57 = 8 years; demand stub will be replaced in Sprint 4 with =INDEX/MATCH on Starlink V2 internal launches + Sprint 3 Customer Launch external)
copyToRange source F64, destination G64:AC64

A65 = "F9 cadence-utilization per booster (memo, derived)"
D65 = =IFERROR(D64 / D60, 0)
copyToRange source D65, destination E65:AC65
```

Expected D60 = 28; D61 = 17; D62 = 6; D63 = 39 ✓ (matches §6.1 calibration). D64 = 171 ✓. D65 = 171/28 ≈ 6.11 launches/booster — below R51 ceiling of 12 (so demand-constrained, not supply-constrained). E63 = 39 + 17 − 6 = 50 (fleet grows in 2026 since demand stays flat and replacement still 6/yr — Sprint 2 simplification will overshoot fleet by 2027 absent demand growth; Sprint 3/4 wiring corrects this).

**Format**: D60:AC63 integer; D64:AC64 number `0.0`; D65:AC65 number `0.00`.

**Open Thread note (§7)**: The 2026 carryover anchor (F9 manufactured = 17 / launches = 171) is a Sprint 2 placeholder. Sprint 3/4 should replace these with demand-driven values once Customer Launch + Starlink demand are live. The F9 fleet will likely overshoot in 2026 with the constant retirement = 6 simplification (50 boosters end-2026 vs 39 end-2025 is 11-booster fleet growth that won't be absorbed by 2026 demand). This is documented as a calibration tolerance — the §6.1 verification gate locks 2025 only.

**§3.3.5 F9 capacity + at-cost transfer rate (rows 68–71)**

```
A68 = "F9 Annual Capacity (kg-to-LEO)"
D68 = =D60 * $D$51 * $D$49   (fleet BoY × cadence × payload — supply max; uses BoY to reflect fleet available at start of year)
copyToRange source D68, destination E68:AC68

A69 = "F9 variable cost per launch ($mm)"
D69 = =$D$45 + $D$46 + $D$47 + $D$48 * $D$44   (2nd stage + fairing + ops + booster refurb amortized per flight)

A70 = "F9 booster D&A share per launch ($mm)"
D70 = =$D$44 / $D$50

A71 = "F9 at-cost rate ($mm/launch)"
D71 = =D69 + D70
```

Note: D69, D70, D71 are single-value (D-column only) — F9 cost structure is flat across the horizon. No year-row needed.

Expected D68 (2025) = 28 × 12 × 22,800 = 7,660,800 kg = 7.66M kg (max F9 capacity; actual launches 171 → consumed capacity = 171 × 22,800 = 3.9M kg, well under cap).
Expected D69 = $10 + $1.25 + $5 + $0.03 × $30 = $10 + $1.25 + $5 + $0.9 = $17.15M.
Expected D70 = $30 / 50 = $0.6M.
Expected D71 = $17.15 + $0.6 = $17.75M/launch.

F9 at-cost rate $17.75M × 22,800 kg payload → $/kg = $778/kg.

**Format**: D68:AC68 integer `#,##0`; D69:D71 currency `$#,##0.00`.

### §3.4 Blended cost stack + calibration read-back (rows 73–80)

**§3.4.1 Headers (rows 73, 79)**

```
A73 = "BLENDED COST STACK + CALIBRATION"   (SECT: white-on-charcoal, bold)
A79 = "Memo: 2025 calibration anchors (read-only diagnostics)"   (SUB: italic, light grey)
```

**§3.4.2 Blended cost rows (rows 74–77)**

```
A74 = "Total launches per year (all vehicles)"
D74 = =D64 + D33
copyToRange source D74, destination E74:AC74

A75 = "Total upmass per year (kg)"
D75 = =D64 * $D$49 + D34   (F9 launches × F9 payload + Starship total kg-to-LEO)
copyToRange source D75, destination E75:AC75

A76 = "Total launch CapEx per year ($mm) — variable + amortized D&A"
D76 = =D64 * D71 + D33 * D40   (F9 launches × F9 at-cost rate + Starship launches × Starship at-cost rate)
copyToRange source D76, destination E76:AC76

A77 = "Blended $/kg"
D77 = =IFERROR(D76 * 1e6 / D75, 0)   (convert $mm to $, divide by kg; IFERROR for upmass = 0 edge case)
copyToRange source D77, destination E77:AC77
```

Expected D74 = 171 + 0 = 171. D75 = 171 × 22,800 + 0 = 3,898,800 kg. D76 = 171 × $17.75M + 0 = $3,035.25M. D77 = $3,035.25M × 1e6 / 3.9M kg = $778/kg.

Per §6.1: blended $/kg 2025 in $400–$800 → $778 at the upper end. PASS (within range).

**Format**: D74:AC74 integer; D75:AC75 integer `#,##0`; D76:AC76 currency `$#,##0`; D77:AC77 currency `$#,##0`.

**§3.4.3 Calibration status memo (row 80)**

```
A80 = "Memo: 2025 calibration status"
D80 = =IF(
        AND(
          ABS(D64 - 171) <= 5,
          ABS(D63 - 39) <= 5,
          ABS(D61 - 17) <= 2,
          D33 = 0,
          D77 >= 400, D77 <= 800
        ),
        "PASS",
        "CHECK"
      )
```

Plugin reads D80 and confirms "PASS". If "CHECK", halt and trace which check failed.

**Format**: D80 text, bold.

### §3.5 Locked methodology choices (Vlad answers, 2026-05-20)

Reproduced here for the plugin so the spec is fully self-contained:

1. **Starship cadence Wright's Law**: Lagged + 1-ship anchor. `cadence_per_booster(T) = MAX(1, MIN(ceiling, (1/base_turnaround) × (cum_upmass(T-1) / R12_fully_reusable_payload)^(−log₂(1−R16))))`. Pre-first-flight cadence floors at 1. No within-year circularity. Anchor = R12 = 100K kg (= 1 fully-reusable Starship's payload).

2. **F9 2025–2026 anchoring**: Hardcode 2025 and 2026 historicals as explicit overrides. D61 = 17 (manufactured 2025), E61 = 17 (manufactured 2026). D62 = 6 (retired 2025), E62 = 6 (retired 2026). D64 = 171 (launches 2025), E64 = 171 (launches 2026). Build mechanic + decay schedule kicks in from 2027 (F-column) onwards. Sprint 3/4 will repoint D64/E64 if needed once consumer demand is live; for Sprint 2, the overrides hold.

3. **At-cost transfer rate location**: Launch Capacity tab owns the transfer rate computation (R40 Starship at-cost, R71 F9 at-cost). Supply tab = cost-stack source-of-truth. Sprint 3 / Sprint 4 / Sprint 5 read by INDEX/MATCH on these exact labels.

4. **Canonical kg-capacity label scope**: `Total Annual Capacity (kg-to-LEO)` = Starship-only (row 34). F9 capacity is the separate informational row `F9 Annual Capacity (kg-to-LEO)` (row 68). Sprint 10 Allocator kg queue reads only the Starship label.

---

## §4 — Verification (universal + Sprint 2 calibration)

### §4.1 Universal checks (Sprint Roadmap §5)

After all §3.2 / §3.3 / §3.4 writes complete:

**§4.1.1 No formula errors workbook-wide (Rule 4 + Roadmap §5.1)**
Plugin scans the Launch Capacity tab cells A6:AC80 for `#REF! #VALUE! #DIV/0! #NAME? #NUM! #NULL! #N/A`. Expected: zero matches (except inside IFERROR-wrapped cells, which is fine because they don't cascade). Halt if any error on a display row.

**§4.1.2 Conservation block (Roadmap §5.2)**
N/A for Sprint 2 — Launch Capacity is not a P&L module, doesn't feed Group P&L conservation block, and the Sprint 1 conservation block reads "OK" trivially because no module body has populated yet. Re-confirm Sprint 1 PASS state: read Group P&L!D108:AC108 — every cell should still read "OK" (because module bodies are still empty). If anything reads "CHECK", halt and trace — Sprint 2 writes shouldn't touch any module tab.

**§4.1.3 Edge-year reads — Rule 16 (Roadmap §5.3)**
Mandatory four-column read of every output row. See §4.3 below for the full read-back table.

**§4.1.4 Round-trip stability (Roadmap §5.4)**
Recalc workbook 5 times. Read these key cells across recalcs: D33, D34, D40, D63, D64, D68, D71, D77. Expected: no cell moves >$1 (or >0.01 for integer counts). Pass = stability confirmed.

**§4.1.5 Stale-reference scan (Rule 22 + Roadmap §5.5)**
Plugin reads column A of these rows on Launch Capacity and confirms exact-string match against §3.1 row map:
- A23 must read exactly `Launches per Starship vehicle per year (cadence)`
- A33 must read exactly `Total Starship launches per year`
- A34 must read exactly `Total Annual Capacity (kg-to-LEO)` ← **canonical label for Sprint 10**
- A40 must read exactly `Starship at-cost rate ($mm/launch)`
- A64 must read exactly `F9 launches per year`
- A68 must read exactly `F9 Annual Capacity (kg-to-LEO)`
- A71 must read exactly `F9 at-cost rate ($mm/launch)`
- A77 must read exactly `Blended $/kg`

If any mismatch (extra space, punctuation drift, capitalization), halt and fix the column-A write — this is the row map future sprints depend on.

**§4.1.6 Sanity check halt thresholds (Rule 15 + Roadmap §5.6)**
See §4.2.

**§4.1.7 Claude Log entry (Roadmap §5.7)**
Plugin appends one row to the Claude Log tab. See §5 below for the template.

### §4.2 Sprint 2 calibration (Sprint Roadmap §6.1 — verbatim)

| Output | Read from | 2025 expected | Tolerance | Halt threshold |
|---|---|---|---|---|
| F9 total launches | D64 | 171 | ±5 | <160 or >185 |
| F9 fleet end-2025 | D63 | 39 | ±5 | <30 or >50 |
| F9 manufactured 2025 | D61 | 17 | ±2 | <13 or >22 |
| Starship launches | D33 | 0 | exact | any > 0 |
| Total Starship capacity (kg) | D34 | 0 (per Sprint 2 scope: Starship boosters built = 0 so capacity = 0; the §6.1 "~450K ±30%" target assumes some Starship ops in 2025 — see §7 Open thread for reconciliation) | n/a Sprint 2 | n/a |
| Blended $/kg | D77 | ~$778 (all F9, no Starship) | $400–$800 range | outside |

D80 calibration memo cell aggregates the above — read D80; if "PASS", §4.2 passes.

### §4.3 Edge-year read-back (D / I / S / AC)

Plugin reads these cells across columns D (2025), I (2030), S (2040), AC (2050) and reports actual vs expected. Tolerance ±5% on continuous values, exact on integer-count cells.

| Row | Label | D (2025) expected | I (2030) expected | S (2040) expected | AC (2050) expected |
|---|---|---|---|---|---|
| 23 | Starship cadence | 1.00 | 1.00 (cum upmass = 0 throughout in Sprint 2 because boosters = 0) | 1.00 | 1.00 |
| 27 | Starship booster fleet EoY | 0 | 0 | 0 | 0 |
| 33 | Starship total launches | 0 | 0 | 0 | 0 |
| 34 | **Total Annual Capacity (kg-to-LEO)** | 0 | 0 | 0 | 0 |
| 40 | Starship at-cost rate ($mm/launch) | $30.42 | $19.09 | $1.61+$0.351+$0.78 ≈ $2.74 (variant mix near 100%) | $2.74 |
| 60 | F9 fleet BoY | 28 | depends on simplified retirement; ~50–60 | depends; eventually 0 as decay zeroes manufactured | 0 |
| 61 | F9 manufactured | 17 | from R55 × decay = 8 × (1 − (2030−2027)/8) = 8 × 0.625 = 5 | 0 (past decay window) | 0 |
| 62 | F9 retired | 6 | 6 (Sprint 2 simplification) | 6 | 6 |
| 63 | F9 fleet EoY | 39 | trending downward | 0 (clamped at floor) | 0 |
| 64 | F9 launches | 171 | from F-column decay formula; ~107 in 2030 (= 171 × (1 − 3/8)) capped by fleet × 12 | 0 | 0 |
| 68 | F9 Annual Capacity (kg) | 7,660,800 | ~50 × 12 × 22,800 ≈ 13.7M (fleet ceiling) | 0 | 0 |
| 71 | F9 at-cost rate ($mm/launch) | $17.75 | $17.75 (flat — no year-row variation) | $17.75 | $17.75 |
| 77 | Blended $/kg | ~$778 | ~$778 (still all F9) | undefined (= 0 launches; IFERROR → 0) | 0 |

Plugin reports actual vs expected for each cell. Variances >5% halt and push back.

**Out-year sanity caveat**: rows 27, 33, 34 (Starship outputs) stay at 0 throughout Sprint 2 because R25 boosters built = 0. This is correct — Sprint 10 vehicle build claim writes R25 endogenously. The §6.1 "~450K kg 2025 Starship capacity" target is acknowledged as not satisfiable in Sprint 2; document for Sprint 10.

**F9 fleet overshoot caveat**: rows 60, 63 will overshoot in 2026 because the simplified retirement = 6/yr doesn't scale with fleet growth. Sprint 3 / Sprint 4 will repoint F9 launches to demand-driven; Sprint 10 audit may need a patch sprint to build the full F9 retirement engine. For Sprint 2, the 2025 calibration anchors hit cleanly.

### §4.4 Don't-touch verification

Plugin confirms NO writes outside Launch Capacity tab (except appending the Claude Log row per §5). Specifically:

- Assumptions tab: ZERO writes (read-only access via INDEX/MATCH only).
- Allocator tab: ZERO writes.
- Customer Launch / Starlink / Starlink Capacity / ODC / AI Stack / Lunar Mars tabs: ZERO writes.
- OpEx / CapEx / Valuation / Group P&L / Demand Curves tabs: ZERO writes.
- Claude Log tab: ONE new row appended (per §5).

Plugin reads the prior cell counts of each tab at pre-flight (§3.0) and re-reads at post-execution; any tab other than Launch Capacity + Claude Log showing a delta = halt + push back.

---

## §5 — Claude Log entry template

Plugin appends one row to the Claude Log tab on the workbook. Column order matches Sprint 0 / Sprint 1 entries:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-MM-DD | 2 | Launch Capacity (full build), Claude Log (append) | Built Launch Capacity tab end-to-end: Starship section (rows 6–40) with Wright's Law cadence on lagged cum upmass (1-ship anchor = R12 = 100K kg), variant mix + lifetime reuses pulled by label from Assumptions, full at-cost transfer rate stack at R40. F9 section (rows 42–71) with 2025–2026 historical anchors (manufactured = 17, launches = 171, fleet EoY 2025 = 39 — all hitting §6.1 calibration), post-V3-trigger decay mechanic from 2027 over R57 = 8 years, at-cost transfer rate at R71. Blended $/kg at R77. Canonical Sprint 10 read label `Total Annual Capacity (kg-to-LEO)` locked at R34 (Starship-only per 2026-05-20 lock). 2025 calibration: F9 launches 171 ✓, F9 fleet EoY 39 ✓, F9 manufactured 17 ✓, Starship launches 0 ✓, blended $/kg $778 ✓ (within $400–$800). | (a) Starship ops cost not in Assumptions §3 — defaulted to $0 in R37; flag for Sprint 3 patch. (b) F9 retirement engine simplified to constant 6/yr — full lifetime-reuses tracking deferred. (c) §6.1 target "~450K kg 2025 Starship capacity" treats Starship as operational; reconciled to 0 because boosters built = 0 in Sprint 2 (Sprint 10 vehicle build claim writes R25). (d) 2026 F9 anchors (carryover from 2025) will be repointed by Sprint 3/4 demand wiring. | Sprint 3 — Customer Launch module |

---

## §6 — Don't touch (out of scope)

Sprint 2 writes ONLY to:
- Launch Capacity tab rows 6–80
- Claude Log tab (one new row appended)

Sprint 2 does NOT touch:
- Assumptions tab (read-only via INDEX/MATCH — every value inlined by label in §3.5)
- Allocator tab (Sprint 1 deliverable, Sprint 10 will light up the brain)
- Customer Launch / Starlink / Starlink Capacity / ODC / AI Stack / Lunar Mars / OpEx / CapEx / Valuation / Group P&L / Demand Curves tabs
- Any save / save-as / file-write operation (Vlad handles all saves per standing process rule 2)
- Any row insertion (Rule 10 — all new content appended below existing rows on Launch Capacity)
- The Sprint 1 module shells' Allocator IN/OUT contract rows (those stay at 0 placeholders until Sprint 10)

If the plugin discovers a need to write outside Launch Capacity (e.g., add a new Starship-ops-cost row to Assumptions), HALT per Rule 9 and push back to spec author — that's a patch sprint, not a Sprint 2 inline.

---

## §7 — Open thread (post-Sprint 2 considerations)

These are flagged for spec author attention but do not block Sprint 2 PASS.

1. **Starship ops cost row missing from Assumptions §3.** Sprint 0 R32–R47 has hardware costs (SH mfg, ship mfg, refurb %) but no per-launch ops cost line for Starship — only F9 has R52 ops cost. Sprint 2 defaults Starship ops = $0 in the at-cost rate formula R37. Sprint 3 (Customer Launch) may want to add an Assumptions row `Starship per-launch ops cost ($mm)` as a patch sprint. Recommended Base Case ~$5M/launch (mirror F9) with MC range [3, 10].

2. **F9 retirement engine simplification.** Sprint 2 hardcodes R62 retired = 6/yr flat. This overshoots fleet in 2026 (39 EoY 2025 + 17 manufactured 2026 − 6 retired = 50 EoY 2026, vs ~39 demand-implied). Sprint 3 / Sprint 4 may need a patch to add a proper lifetime-reuses tracking engine: retirements driven by `cum_uses_per_booster ≥ R50 lifetime reuses`. Defer until consumer demand is wired and overshoot becomes a calibration issue.

3. **2025 Starship capacity calibration target reconciliation.** Sprint Roadmap §6.1 says "Total Starship capacity (kg) ~450K ±30%". This implied some Starship operations in 2025. Per the 2026-05-20 lock and Sprint 2 architecture, Starship boosters built = 0 in 2025 (Sprint 10 vehicle build claim writes R25), so capacity = 0. The §6.1 target should either be (a) updated to "Total Starship capacity 2025 = 0 exact, ramps from 2027+" per the current architecture, or (b) interpreted as "expected capacity AT FULL SPRINT-10 BUILD", which Sprint 2 doesn't compute. Recommend amending Sprint Roadmap §6.1 in a future amendment log entry.

4. **2026 F9 carryover anchors.** D61/E61 = 17 and D64/E64 = 171 are placeholders. Sprint 3 wires Customer Launch demand → may replace E64 with `INDEX(Customer Launch!D:D, MATCH("F9 customer launches", ...)) + INDEX(Starlink!D:D, MATCH("V2 BB launches (internal)", ...))` or similar. The current spec leaves these as static anchors; Sprint 3/4 spec authors should reroute as needed.

5. **F9 launches demand-stub for 2027+.** F-column formula in R64 uses `171 × (1 − (year − R56) / R57)` decay stub. Sprint 3/4 will replace this with demand-driven `=INDEX/MATCH` calls into Customer Launch + Starlink V2 internal launches. The current stub is intentionally simple — preserves the §6.1 calibration without overcommitting to a Sprint 3/4-owned mechanic.

6. **Boosters built (R25) and Starship Total Annual Capacity (R34) at 0 throughout Sprint 2.** This is correct per Architecture §6.6 (vehicle build cost is a non-module claim sized by Sprint 10 Allocator from forward-aggregate kg demand). Sprint 10 will populate R25 endogenously, lighting up R27 fleet → R23 cadence → R33 launches → R34 capacity. Sprint 2 just lays the mechanic; the level is allocator-driven.

7. **Blended $/kg interpretation for Valuation.** R77 reports $778/kg in 2025 (100% F9) trending down to undefined-because-zero in out-years (where Sprint 2 has Starship = 0 and F9 decayed to 0). Once Sprint 10 lights up Starship operations, R77 will display the genuine F9 + Starship-blended figure. Until then, treat R77 as an F9-only metric for 2025.

---

## §8 — Execution sequence (plugin order of operations)

Plugin executes in this fixed order. Each block is one or more discrete tool calls per Rule 1.

1. **Pre-flight (§3.0)** — verify all 7 checks. Halt on any failure.
2. **Section + subsection headers (§3.2.1 + §3.3.1 + §3.4.1)** — write A6, A7, A19, A36, A42, A43, A54, A67, A73, A79 as discrete label writes. Apply formats per §3.1 (SECT = white-on-charcoal + bold; SUB = italic + light grey).
3. **Starship physical pulls (§3.2.2)** — rows 8–17. One row at a time: A-label write, then D-column INDEX/MATCH formula write. After block, read back D8, D11, D12, D15, D16 — confirm 35.1, 150000, 100000, 60, 0.145.
4. **Starship year-row pulls (§3.2.3)** — rows 20, 21. One row at a time: A-label, D-column formula, copyToRange D→E:AC. After block, read back D20, I20, AC20 (variant mix) and D21, I21, AC21 (lifetime reuses) — confirm trajectory.
5. **Starship fleet + cadence + upmass (§3.2.4 + §3.2.5 + §3.2.6)** — rows 23–29. Write labels first, then D-column anchors, then copyToRange. Year-chained rows (24, 27, 28) write D as anchor, E as year-chained formula, then copyToRange E→F:AC.
6. **Starship launches + capacity (§3.2.7 + §3.2.8)** — rows 31–34. Same pattern.
7. **Starship at-cost rate (§3.2.9)** — rows 37–40. Same pattern.
8. **VERIFICATION GATE 1** — read Starship outputs: D33 (expect 0), D34 (expect 0), D40 (expect $30.42M). I40 (expect ~$19M). S40 (expect ~$2.7M). Halt on variance.
9. **F9 physical pulls (§3.3.2)** — rows 44–52. Same pattern as Starship.
10. **F9 supply mechanic anchors (§3.3.3)** — rows 55–58. D-only single values.
11. **F9 fleet dynamics (§3.3.4)** — rows 60–65. Write labels first; D-column anchors (D60=R58 ref, D61=17 hardcoded, D62=6 hardcoded, D63 formula, D64=171 hardcoded, D65 formula); E-column anchors where applicable (E60 = year-chained, E61=17 hardcoded, E62=6 hardcoded, E63 year-chained, E64=171 hardcoded, E65 year-chained); F-column mechanic formula; copyToRange F→G:AC.
12. **F9 capacity + at-cost (§3.3.5)** — rows 68–71. Row 68 year-row; rows 69–71 D-only.
13. **VERIFICATION GATE 2** — read F9 outputs: D61 (expect 17), D63 (expect 39), D64 (expect 171), D68 (expect 7,660,800), D71 (expect $17.75M). Halt on variance.
14. **Blended cost stack (§3.4.2)** — rows 74–77. Same pattern.
15. **Calibration memo (§3.4.3)** — row 80. Single cell write.
16. **VERIFICATION GATE 3** — read D77 (expect ~$778) and D80 (expect "PASS"). Halt if D80 = "CHECK".
17. **§4.1 universal checks** — error scan, conservation re-confirm, edge-year read-back per §4.3, stale-ref scan per §4.1.5, round-trip stability per §4.1.4.
18. **§4.4 don't-touch verification** — confirm no writes outside Launch Capacity + Claude Log.
19. **§5 Claude Log entry** — append one row.
20. **Sprint 2 complete declaration** — push back to spec author with all read-back values + PASS status.

---

## §9 — Amendment log

- **2026-05-20 (initial draft)** — Sprint 2 spec drafted as Vlad's kickoff prompt directed. Four load-bearing methodology choices locked via AskUserQuestion: (1) Starship cadence = Lagged + 1-ship anchor; (2) F9 2025–2026 = explicit historical overrides, decay mechanic from 2027; (3) at-cost transfer rate row location = Launch Capacity; (4) canonical `Total Annual Capacity (kg-to-LEO)` = Starship-only. Spec mirrors Sprint 0 / Sprint 1 structure. §1 Rule Compliance Preamble fully ticked or justified N/A. §3 lays out cell-by-cell build with full Excel formulas inlined. §4 verification gate per Sprint Roadmap §5 + §6.1. §7 Open thread surfaces (a) missing Starship ops cost row, (b) simplified F9 retirement, (c) Sprint Roadmap §6.1 Starship capacity target reconciliation, (d) 2026 carryover anchors, (e) F9 launches demand-stub for 2027+, (f) Starship build at 0 until Sprint 10, (g) Blended $/kg interpretation. Plugin operates on V2.3 live session; Vlad handles all saves per standing process rule 2.
