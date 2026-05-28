# Sprint 3 — Customer Launch Module Body + Patches D/A/B/E §6.13

**Source workbook**: `SpaceX Model V2.4.xlsx` (Sprint 2 output, verified PASS — Launch Capacity tab end-to-end, F9 + Starship sections, canonical labels locked, 2025 calibration: F9 launches 171 ✓ F9 fleet EoY 39 ✓ F9 manufactured 17 ✓ Starship launches 0 ✓ Blended $/kg $778 ✓).
**Target workbook**: `SpaceX Model V2.5.xlsx` (Vlad has Save-As'd from V2.4 → V2.5 before this kickoff per standing process rule 2).
**Day budget**: 1 day
**Date drafted**: 2026-05-20

---

## §0 — Constitutional references

- **`01_Lessons_Learned.md`**: Principles 1 (no postponed architectural decisions — F9-vs-Starship customer split IRR-driven, locked this sprint), 2 (per-launch marginal IRR — Sprint 3 builds the engine for both F9 + Starship customer launches), 6 (no tab without a locked function — Customer Launch is a P&L module per Architecture §1), 7 (canonical labels day one — `F9 customer launches per year` + `Starship customer launches per year` + `Customer Launch internal transfer revenue` published this sprint), 8 (module COGS = direct production only — no R&D/SG&A/overhead/taxes on Customer Launch tab), 9 (internal transfers gross at module IRR, eliminated at Group), 11 (no OFFSET; INDEX-only), 12 (anchor-and-offset for ramps), 13 (year-offset row 5 standard already in place from Sprint 0/1), 14 (INDEX/MATCH on labels), 17 (delete superseded rows in same spec — R34 ship refurb % deleted per Patch E §6.13), 18 (MC ranges at input creation — every new Assumptions row this sprint has MC range populated), 22 (within-year cycles — Customer Launch deliberately avoids cycles by reading Launch Capacity outputs which are supply-side static).
- **`02_Architecture_and_Methodology.md`**: §1 (tab #4 = Customer Launch — second module tab in sheet order), §3 (vending-machine framing — Revenue → COGS → Gross Profit = Module EBITDA → CapEx → Module FCF; no R&D/SG&A/overhead/taxes), §4.1 (Allocator IN block already in place from Sprint 1 at rows 7-10), §4.2 (Allocator OUT contract — 11 canonical rows at 200-210 — Sprint 3 overwrites Sprint 1 literal-0 placeholders with live formulas), §5.1 (per-launch IRR formula: CF stream length N+1, t=0 cost slug, t=1..N net marginal revenue), §5.2 (Customer Launch net marginal revenue per launch = price − variable cost − D&A share − insurance − other COGS — external launches only per §5.2 + §7.1), §5.4 (strict IRR > 0 cutoff — Architecture rule, not enforced at Customer Launch level since Customer Launch reads outer allocator IRR cutoff via Allocator OUT consumption), §6.6 (vehicle D&A on Launch Capacity — confirmed by Sprint 2 PASS; Customer Launch reads R40 LEO at-cost + R71 F9 at-cost by INDEX/MATCH; fallback to Customer Launch ownership NOT triggered), §7.1 (Customer Launch ↔ consuming modules launch services — 4-step Rule 21 pattern: Customer Launch books internal transfer revenue, Sprint 4/5/6 will book Launch services cost in COGS, Sprint 9 Group P&L eliminates, conservation row R105 verifies), §17 (2025 calibration targets — F9 customer revenue $4,290M).
- **`03_Sprint_Roadmap_and_Verification.md`**: §3 Sprint 3 scope + locked-this-sprint decisions (vehicle D&A fallback ownership = NOT triggered since Sprint 2 published R40 + R71; Module CapEx vs Capital deployed convention — Sprint 3 sets the equilibrium-equal convention; fully-allocated at-cost rate per Architecture §7.1), §5 universal verification (no errors, conservation OK, edge-year reads, round-trip stability, stale-ref scan, sanity halts, Claude Log), §6.2 Sprint 3 calibration targets (F9 customer launches 38.58 ±2, F9 customer revenue $4,290M ±5%, F9 customer launch price $111M ±5%, Starship customer revenue $0 exact, per-launch Blended IRR 8-25% range — see §7 Open Thread for calibration target reconciliation), §8 sprint-spec template (followed below).
- **`04_Assumptions_Tab_Spec.md`**: §1 (column convention — row 1 year header + row 2 year-offset deviation, locked), §2 §4 Customer Launch existing inputs (R22-R23 MFW-IRR economic life clamps MIN=1 MAX=10, R62 §4 section header, R63 F9 customer launch price year-row anchored $111M -3%/yr, R64 Starship customer launch price year-row $100M from 2027 -8%/yr — DEPRECATED by Sprint 3 §3.3.7 lock #2; new price = at-cost × margin, R71 Customer Launch depreciation useful life 5y, R234-R236 Customer Launch R&D in OpEx scope NOT this sprint, R274 Customer Launch risk premium 0.01, R293 Comp anchor Rocket Lab $40B, R297 Multiple 5x).
- **`Model Execution Rules.md`**: Mandatory Rule Compliance Preamble at §1; Rules 1 / 3 / 4 / 5 / 10 / 11 / 12 / 13 / 14 / 16 / 17 / 19 / 21 / 22 / 23 load-bearing.
- **`2025 Anchors from Q4_25.md`**: F9 customer launches 2025 = 38.58 (Earth R51), F9 customer revenue 2025 = $4,290M (Earth R136), F9 customer launch price 2025 = $111M (Earth R132), Starship customer revenue 2025 = $0 (pre-commercial).
- **`Sprint_0_Spec.md`** §3.6 (Customer Launch inputs R22-R23, R62-R71, R234-R236, R274, R293, R297 — every label and Base Case value inlined in §3.3 below).
- **`Sprint_1_Spec.md`** §3.3 (Customer Launch shell — Allocator IN at rows 7-10, Allocator OUT at rows 200-210 with literal 0 placeholders; Sprint 3 fills rows 11-199 in between, overwrites OUT block placeholders with live formulas).
- **`Sprint_2_Spec.md`** §3.1 (Launch Capacity row map — R40 `Starship at-cost rate ($mm/launch)`, R71 `F9 at-cost rate ($mm/launch)`, R34 `Total Annual Capacity (kg-to-LEO)`, R68 `F9 Annual Capacity (kg-to-LEO)`, R64 `F9 launches per year` — canonical labels Sprint 3 reads by INDEX/MATCH).
- **`Sprint_2_to_3_Patch_F9_Retirement_and_Starship_Ops.md`**: MANDATORY ABSORPTION — Patches D (Sprint 2 execution fixes), A (F9 retirement engine), B (F9 demand-driven wiring), C (SUPERSEDED — do not implement), E §6.13 (Starship cost mechanic split-cost-curve canonical formulation). Patch C explicitly NOT implemented. Five patches fold into Sprint 3 per §5.1–§5.5 of patch doc; execution sequence D → A → B → E §6.13 → Customer Launch body per §8.

---

## §1 — Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md` and the four constitutional docs. Each box ticked or justified N/A:

- [x] **Rule 1** (one concept per write) — §3 structured as discrete blocks. Every row's column-A label is written in a separate `set_cell` call from its D-column anchor formula, and the D-anchor formula is a separate call from the E:AC copyToRange. Assumptions amendments execute as: (i) label write, (ii) Base Case value write, (iii) MC Min/Max/Distribution writes, (iv) Notes write — four discrete writes per new Assumptions row.
- [x] **Rule 3 / 23** (formula pattern) — every deterministic ramp on Customer Launch tab (Starship customer margin year-row, total customer market year-row) uses anchor-and-offset on `E$5` and a locked anchor cell. Year-chained exceptions explicitly flagged inline: (a) Per-launch IRR engine uses N-length cashflow array constructed via SEQUENCE — not year-chained, but uses dynamic-array slicing per Architecture §5.1 IRR formula pattern. No other year-chained logic on Customer Launch tab.
- [x] **Rule 4** (verification gate) — §4.3 enumerates explicit read-back cells at D (2025), I (2030), S (2040), AC (2050) with expected values for: F9 customer launches per year, F9 customer revenue, Starship customer launches per year, Starship customer revenue, Customer Launch total revenue, Customer Launch internal transfer revenue, Module EBITDA, Module CapEx, Module FCF, per-launch Spot/Forward/Blended IRR (F9 + Starship).
- [x] **Rule 6** (inline formulas) — every cell write in §3 specified with the full Excel formula. No "see Architecture §5" hand-waves — IRR formula pattern inlined verbatim. INDEX/MATCH calls on Assumptions / Launch Capacity / Customer Launch (intra-tab) written out with exact canonical labels.
- [x] **Rule 10** (no row insertions) — Customer Launch tab Sprint 3 writes appended to rows 11–199 (between Sprint 1's IN block at 7-10 and OUT block at 200-210). Sprint 1 OUT block placeholders OVERWRITTEN in place (same row numbers) per Architecture §4.2 — no row insertions on Customer Launch tab. Launch Capacity tab amendments under Patches D/A/B/E §6.13 are formula REPLACEMENTS at existing row numbers (preserving Sprint 2's row map). Assumptions tab amendments — Patch E §6.13 appends 10 new rows below Sprint 0's last-used Assumptions §3 row + 2 new rows in §4 (Total customer market + Starship customer margin); R34 ship refurb % DELETED per Patch E §6.13 + Vlad lock 2026-05-20. The R34 deletion is the only DELETE operation; it executes as a single discrete write before the appends per Rule 1. R10 unchanged from §3.3.0 below: NO `insert_row` operations; only appends + the single R34 delete + in-place formula replacements.
- [x] **Rule 11** (touch points) — every new Customer Launch line item enumerates its (i) intra-tab SUM range (Revenue total, COGS total), (ii) Allocator OUT pull (`Total Revenue`, `Module EBITDA`, `Module FCF`, `Module CapEx`, `Capital deployed`, `Spot IRR`, `Forward IRR (Y+2)`, `Blended IRR`, `Capacity Demand (kg-to-LEO)` — 9 of the 11 canonical OUT rows actively populated, plus `Module EBITDA Margin %` derived), (iii) Sprint 9 Group P&L pull location (will pull `Total Revenue`, `Module EBITDA`, `Module CapEx`, `Module FCF` via INDEX/MATCH), (iv) Sprint 9 conservation row R105 (Launch services elimination) — reads `Customer Launch internal transfer revenue` and Σ consuming modules' Launch services cost. Touch points enumerated per row in §3.6.
- [x] **Rule 12** (label-based cross-tab refs) — every cross-tab pull on Customer Launch tab uses `INDEX(Tab!D:D, MATCH("<exact canonical label>", Tab!$A:$A, 0))` or year-row equivalent `INDEX(Tab!$D:$AC, MATCH("<label>", Tab!$A:$A, 0), E$5+offset)`. Zero hardcoded row-number references. Specifically: Customer Launch reads Launch Capacity R40 by label `Starship at-cost rate ($mm/launch)`, R71 by label `F9 at-cost rate ($mm/launch)`, R34 by label `Total Annual Capacity (kg-to-LEO)`, R68 by label `F9 Annual Capacity (kg-to-LEO)`.
- [x] **Rule 13** (vending-machine test) — Customer Launch P&L stops at Module EBITDA = Gross Profit. No R&D / SG&A / customer service / corporate overhead / taxes anywhere on Customer Launch tab. R&D lives on OpEx tab (R234-R236 inputs, Sprint 8 owns the formula). The exception is Internal Transfer Revenue (intercompany flow, NOT OpEx) — Architecture §7.1 4-step pattern.
- [x] **Rule 14** (no hardcoded constants) — every behavior input resolves to an Assumptions row by label. Specific declared exceptions: (a) Mathematical constants (1, 0 in IFERROR fallbacks); (b) IRR engine SEQUENCE() arguments are dynamic-array constructs, not hardcoded values; (c) 2025 + 2026 F9 customer launch overrides (D = 38.58, E ≈ 38.58 × growth) are anchored to the new Assumptions year-row `Total customer launch market (launches/yr)`, not hardcoded — overrides resolve via INDEX/MATCH.
- [x] **Rule 15** (sanity check halt thresholds) — §4.2 / §4.4 every check has quantitative halt threshold. F9 customer launches 2025 outside [36.5, 40.5] halt. F9 customer revenue 2025 outside [$3,800M, $4,800M] halt. Starship customer revenue 2025 ≠ $0 halt. F9 per-launch Blended IRR 2025 outside [0%, 50%] halt (note: §6.2 target 8-25% range — see §7 Open Thread for calibration target reconciliation since per-launch margin economics are very high; spec-side halt threshold relaxed to <0% or >50% per §6.2 literal halt language; if IRR comes in >50% Vlad reviews calibration assumptions). Per-launch IRR `#NUM!` or negative INFINITY = halt + push back.
- [x] **Rule 17** (delete superseded rows) — Sprint 0 R64 `Starship customer launch price ($mm/launch) — year-row` is DEPRECATED (label retained for back-compat per Principle 7 — no renames; cell formulas left as Sprint 0 values for memo purposes). Customer Launch tab does NOT read R64 — instead computes Starship customer price = at_cost × (1 + margin) per Vlad lock #2 2026-05-20. R64 deprecation noted in §6 Don't Touch + §7 Open Thread (clean cell-clear can happen in Sprint 9 audit if desired). Patch E §6.13 R34 ship refurb % DELETED from Assumptions in §3.3.5.
- [x] **Rule 19** (save-as) — target workbook named explicitly: `SpaceX Model V2.5.xlsx`. Per standing process rule 2 (locked 2026-05-20), Vlad has already Save-As'd V2.4 → V2.5 before this kickoff; plugin operates on the live open session and does NOT issue any save commands. §3.0 pre-flight verifies V2.5 is the active workbook name.
- [x] **Rule 21** (internal flows need elimination + conservation) — Customer Launch introduces the FIRST live internal transfer flow in the rebuild: Launch services from Customer Launch (source) to Sprint 4 Starlink, Sprint 5 ODC, Sprint 6 AI Stack (consumers — not yet populated this sprint). 4-step pattern: (1) Customer Launch books `Customer Launch internal transfer revenue ($mm)` row reading Σ consuming modules' launch demands × at-cost rate, (2) Sprint 4/5/6 will book Launch services cost in COGS in future sprints, (3) Sprint 9 Group P&L R105 eliminates the flow, (4) Sprint 9 conservation row R105 verifies match. For Sprint 3 verification, consuming modules read 0 via IFERROR-0 wrappers — internal transfer revenue resolves to 0 at Sprint 3 exit. Lights up endogenously in Sprint 4/5/6.
- [x] **Rule 22** (stale-ref scan) — §4.5 enumerates by-label scan: (i) Customer Launch's Launch Capacity reads (R40 / R71 / R34 / R68) confirmed against Launch Capacity row labels; (ii) Customer Launch's intra-tab references all by-label; (iii) Sprint 1 OUT block placeholders OVERWRITTEN with live formulas — Sprint 3 verifies the 11 canonical OUT labels match Architecture §4.2 verbatim; (iv) future Sprint 4/5/6 will reference Customer Launch by canonical labels listed in §3.6.X row map — Sprint 3 publishes those labels exactly.

**Architecture & Methodology compliance:**

- [x] Module P&L follows vending-machine framing (Architecture §3) — Customer Launch builds Revenue → COGS → Gross Profit = Module EBITDA → Module CapEx → Module FCF per §3.6. No R&D / SG&A / overhead / taxes.
- [x] Per-launch marginal IRR engine (Architecture §5) — §3.7 builds F9 + Starship per-launch IRR engines. N = lifetime reuses clamped at R23 = 10 yr ceiling per Vlad lock #4 2026-05-20. Per-launch IRR reads external customer economics only (Principle 9 + §7.1) — internal at-cost transfers don't contribute to IRR signal.
- [x] Allocator OUT contract uses canonical 11 labels (Architecture §4.2) — §3.8 overwrites Sprint 1 placeholders. 9 rows populate with live formulas (Total Revenue, Module EBITDA, Module EBITDA Margin %, Module FCF, Module CapEx, Capital deployed, Spot IRR, Forward IRR Y+2, Blended IRR); Capacity Demand (kg-to-LEO) = external customer Starship kg per Architecture §6.4 ("Customer Launch's kg demand = external customer Starship kg only"). 11 of 11 OUT rows populated.
- [x] Year-offset helper row at row 5 + year header at row 4 on Customer Launch tab — already in place from Sprint 0 / 1. §3.0 pre-flight confirms D4 = 2025, D5 = 0, AC4 = 2050, AC5 = 25.
- [x] ZERO `OFFSET()` formulas; INDEX:INDEX patterns used (Principle 11) — confirmed.

**Patch absorbed from Sprint 2 → 3:**

- [x] **Patches D / A / B / E §6.13 absorbed from `Sprint_2_to_3_Patch_F9_Retirement_and_Starship_Ops.md`** — Patch D (R71 + R24/R27/R28 E:AC extension) executes FIRST per §8 execution sequence. Patches A (F9 retirement engine launch-driven) + B (F9 demand-driven wiring) execute on Launch Capacity rows R62, R64 with one new Assumptions row appended (F9 retirement rate). Patch C SUPERSEDED — no standalone Starship per-launch ops cost row added. Patch E §6.13 executes LAST per execution sequence with R32/R33 value updates, R34 DELETED from Assumptions, R46 step function at 2027, R30 cum stacks live, R37-R41 formulas replaced, 6 new mfg/ops/booster-share Assumptions rows + 4 payload year-row inputs. All five patches' Assumptions amendments inlined verbatim in §3.3 below.

If any box is unchecked, the spec author justifies or amends before execution starts. Plugin refuses to write a single cell against an unticked-or-unjustified preamble.

---

## §1.5 — Pre-execution setup (Vlad confirms before plugin starts writing)

Per standing process rule 3 (locked 2026-05-20), the kickoff prompt includes this confirmation block. The plugin's §3.0 pre-flight verifies it before any cell write.

**Vlad attests:**

1. **Target workbook is open** with name `SpaceX Model V2.5.xlsx` (Save-As completed from V2.4 → V2.5 before this kickoff).
2. **Vlad will handle all saves** — the plugin operates on the live open workbook session and will NOT issue any save / save-as / write-file commands. Verification reads cells from the session directly.
3. **No other tabs are open in this workbook** that could conflict with Customer Launch + Launch Capacity + Assumptions writes (Assumptions tab needs WRITE access this sprint for Patch A + Patch E §6.13 + Sprint 3 new inputs).

If any of the above is not true, plugin halts at pre-flight per Rule 9 and pushes back to Vlad.

---

## §2 — Framing

**Why this sprint:** Sprint 3 builds the Customer Launch module body end-to-end. This is the SECOND module tab (after Launch Capacity, which is supply-only). Customer Launch consumes Launch Capacity's at-cost rates (R40 LEO Starship + R71 F9) and computes external customer launch economics, internal transfer pricing to future-sprint consumers (Sprint 4 Starlink, Sprint 5 ODC, Sprint 6 AI Stack), per-launch marginal IRR (F9 + Starship), and the full Allocator OUT contract.

This sprint also absorbs five patches from `Sprint_2_to_3_Patch_F9_Retirement_and_Starship_Ops.md` per Vlad lock 2026-05-20:

- **Patch D** (execution sequence FIRST): Extends Launch Capacity R71 + R24/R27/R28 to E:AC. Fixes two real execution gaps from Sprint 2 V2.4.
- **Patch A**: Replaces flat F9 retirement (6/yr stub) with launch-driven retirement mirroring Q4'25 Earth!$B$30 = 0.01 retirement rate per launch. One new Assumptions row.
- **Patch B**: Replaces F9 launches 2027+ linear decay stub with demand-driven wiring `MIN(fleet × cadence, F9 customer demand + Starlink V2 internal demand)`. Customer Launch publishes `F9 customer launches per year` as canonical output. Starlink (Sprint 4) will publish V2 internal demand; IFERROR-0 wrapper for the Sprint 3-only state.
- **Patch C** SUPERSEDED by Patch E §6.13 — do NOT implement.
- **Patch E §6.13** (execution sequence LAST): Starship cost mechanic split-cost-curve canonical formulation. Two separate Wright's Law curves (manufacturing $90M anchor 15% learning + ops+fuel+refurb $12M anchor 10% learning). Both decline with scale. Booster/ship split 60/40. R40 LEO at-cost (canonical for Sprint 3/4/5/10) + R41 ship-expended Moon/Mars (Sprint 7 reads this). R32 → $54M, R33 → $36M (Mach33 split), R34 ship refurb % DELETED, R46 step function at 2027, 10 new Assumptions rows.

**Locks for this sprint (Vlad 2026-05-20):**

1. **F9 vs Starship customer launch split is IRR-driven, not exogenous share** (Vlad lock #1). Total customer launch market is a year-row input (Assumptions §4); F9 vs Starship split determined by per-vehicle IRR + capacity. Implementation: Starship customer launches = MIN(market demand, Starship unused capacity post-Starlink+ODC, IRR-positive gate); F9 customer = MAX(0, market demand − Starship customer launches, F9 capacity, IRR-positive gate). Mirrors Q4'25 R56 but cleaner. Sprint 4/5 internal demand reads with IFERROR-0 wrappers (resolve to 0 until those sprints fire).
2. **Starship customer launch price = at-cost × profit margin** (Vlad lock #2). Sprint 0 R64 (fixed $100M starting 2027 -8%/yr) DEPRECATED to memo. New Assumptions §4 inputs: margin multiplier (year-row, 2027 anchor 4.0x → 2050 terminal 1.5x via bounded-CAGR). Customer Launch tab computes Starship customer price = INDEX(Launch Capacity!D:D, MATCH("Starship at-cost rate ($mm/launch)", ...)) × (1 + margin year-row). F9 customer price keeps Sprint 0 R63 anchor $111M -3%/yr (historical observed market pricing — no margin override needed).
3. **Starship customer launches mechanic** (Vlad lock #3 = Rec): MIN(market demand, Starship unused capacity post-Starlink+ODC), IFERROR-0 wrappers. Per Vlad lock #1 above + Architecture §7.1.
4. **Per-launch IRR cashflow stream lifetime N = lifetime reuses (improves over time), clamped at R23** (Vlad lock #4). F9 N = MIN(R23 = 10, R50 = 50) = 10 (constant). Starship N = MIN(R23 = 10, R21 year-row 5 → 100) — varies from 5 in 2025 to 10 from ~2027 onwards. Each period in CF stream = one year (annual cashflow at cadence × per-launch margin). Reads R23 + R50 + R21 by INDEX/MATCH (no hardcoded constants per Rule 14).

**What it produces (canonical output rows — single source of truth; labels exact, no renames):**

| Row (Customer Launch tab) | Canonical label | Consumed by |
|---|---|---|
| (TBD by plugin in 11-199 range) | `Total customer launch market (launches/yr)` | Sprint 3 internal split |
| ↑ | `F9 customer launches per year` | **Patch B Launch Capacity R64** + Sprint 4 internal share computation + Sprint 11 Valuation |
| ↑ | `Starship customer launches per year` | Sprint 5 ODC kg conservation memo + Sprint 11 Valuation |
| ↑ | `F9 customer launch price ($mm/launch)` | Memo for diagnostics; Customer Launch revenue line reads it |
| ↑ | `Starship customer launch price ($mm/launch)` | Memo for diagnostics; Customer Launch revenue line reads it |
| ↑ | `Customer Launch internal transfer revenue ($mm)` | **Sprint 9 Group P&L R105 elimination** (Σ consuming modules' Launch services cost) |
| ↑ | `Total Revenue ($mm)` (Allocator OUT R201/202) | Sprint 9 Group P&L module revenue aggregator |
| ↑ | `Module EBITDA ($mm)` (Allocator OUT R203) | Sprint 9 + Sprint 11 |
| ↑ | `Module FCF ($mm)` (Allocator OUT R205) | Sprint 9 + Sprint 11 |
| ↑ | `Module CapEx ($mm)` (Allocator OUT R206) | Sprint 8 CapEx tab aggregation + Sprint 9 |
| ↑ | `Capital deployed ($mm)` (Allocator OUT R207) | Diagnostic only — does NOT feed Group CapEx per Architecture §4.2 |
| ↑ | `Spot IRR` (Allocator OUT R208) | Sprint 10 Allocator brain |
| ↑ | `Forward IRR (Y+2)` (Allocator OUT R209) | Sprint 10 |
| ↑ | `Blended IRR` (Allocator OUT R210) | Sprint 10 |
| ↑ | `Capacity Demand (kg-to-LEO)` (Allocator OUT R211 — note: Architecture §4.2 says R211 but Sprint 1 placed it as the 11th OUT row at R210 immediately above; Sprint 3 confirms exact row from Sprint 1 row-map and writes there) | Sprint 10 Allocator kg queue |

**What it deliberately does NOT do:**

- Does NOT add R&D / SG&A / corporate overhead / taxes to Customer Launch (vending-machine framing — Principle 8 + Rule 13).
- Does NOT compute vehicle build cost claim — that's Sprint 10 Allocator (Architecture §6.6).
- Does NOT write to Sprint 4 Starlink / Sprint 5 ODC / Sprint 6 AI Stack — internal transfer revenue resolves to 0 via IFERROR-0 wrappers at Sprint 3 exit; lights up endogenously in those sprints.
- Does NOT write to Group P&L / OpEx / CapEx / Valuation tabs — those sprints read Customer Launch by canonical labels.
- Does NOT touch Sprint 0 R64 cell formulas — DEPRECATED to memo (label retained per Principle 7); Customer Launch ignores R64 and computes Starship price endogenously.

**Dependencies:**

- Sprint 0 (Assumptions §4 R22-R23 + R62-R71 + R234-R236 + R274 + R293 + R297; new Sprint 3 amendments per §3.3).
- Sprint 1 (Customer Launch shell at IN rows 7-10 + OUT rows 200-210).
- Sprint 2 (Launch Capacity tab end-to-end, V2.4 PASS).
- Patches D/A/B/E §6.13 (per execution sequence §8).

---

## §3 — Scope

### §3.0 Pre-flight (plugin verifies BEFORE any cell write)

Plugin halts on any failure and pushes back to Vlad.

1. **Workbook name** = `SpaceX Model V2.5.xlsx` (active workbook in session). Halt if name is `V2.4`, `V2.4.xlsx`, or anything else — Vlad missed the Save-As.
2. **Customer Launch tab exists** with sheet position #4 (per Architecture §1: Assumptions #1, Allocator #2, Launch Capacity #3, Customer Launch #4). Halt if tab missing or wrong position.
3. **Customer Launch row 4** reads year header: D4 = 2025, I4 = 2030, S4 = 2040, AC4 = 2050. Halt if any mismatch.
4. **Customer Launch row 5** reads year offset: D5 = 0, I5 = 5, S5 = 15, AC5 = 25. Halt if any mismatch.
5. **Customer Launch Allocator IN block** at rows 7-10 confirmed via label match: A7 = "INPUTS FROM CENTRAL ALLOCATOR" (or Sprint 1 equivalent), A8 contains "Capital Allocation" substring, A9 contains "Starship Capacity Allocation" substring, A10 contains "Total Capital Available" substring. Halt if any label mismatch.
6. **Customer Launch Allocator OUT block** at rows 200-210 confirmed via label match: A200 = "CENTRAL ALLOCATOR OUTPUTS" (or Sprint 1 equivalent), A201..A210 contain the 11 canonical OUT labels per Architecture §4.2. Halt if any label mismatch.
7. **Customer Launch rows 11–199** are empty in V2.4. Plugin reads A11:A199 and confirms all blank (Sprint 1 left module body empty). Halt if anything non-blank exists in this range — Sprint 1 deviation needing investigation.
8. **Launch Capacity tab V2.4 state**: D71 = $17.75M (single-value F9 at-cost). Plugin reads E71 to confirm Patch D needed (E71 should be empty/None pre-Patch-D; Patch D writes E71:AC71). Plugin reads D24, D27, D28 (Starship year-chains) and E24, E27, E28 to confirm E:AC extension needed.
9. **Assumptions §4 Customer Launch section** confirmed via `MATCH("§4 CUSTOMER LAUNCH", Assumptions!$A:$A, 0)` — hit at any row number is fine. Halt if section header missing.
10. **Assumptions R34 row** (`Ship refurb % of manufacturing`) confirmed present (will be DELETED in Patch E §6.13 — §3.3.5). Plugin reads `MATCH("Ship refurb % of manufacturing", Assumptions!$A:$A, 0)` — halt if no match (means R34 doesn't exist or Sprint 0 used different label).
11. **Assumptions R63 + R64** confirmed present (R63 `F9 customer launch price ($mm/launch) — 2025 anchor` year-row; R64 `Starship customer launch price ($mm/launch) — year-row` year-row). R64 is DEPRECATED but stays in workbook for memo purposes.

All 11 pre-flight checks must pass. If any fail, halt and push back.

### §3.1 Patch absorption summary

Sprint 3 absorbs four patches (Patch C SUPERSEDED, not executed). Execution sequence per §8:

1. **Patch D** (§3.2 below) — Sprint 2 execution fixes on Launch Capacity (R71 + R24/R27/R28 E:AC extension). 6 plugin operations. <5 min.
2. **Patches A + B Assumptions amendments** (§3.3.1) — new Assumptions §3 row: `F9 retirement rate (% of launches/year)`. 4 discrete writes (label, Base Case, MC range, Notes).
3. **Patch E §6.13 Assumptions amendments** (§3.3.2–§3.3.5) — R32/R33 updates, R34 DELETE, R46 step function, 6 new cost rows + 4 new payload rows = 10 new appends. ~50 discrete writes.
4. **Sprint 3 new Assumptions §4 amendments** (§3.3.6–§3.3.7) — Total customer launch market year-row (1 new row), Starship customer margin year-row (3 new bounded-CAGR inputs: start anchor, end floor, CAGR). 4 new rows. ~20 discrete writes.
5. **Patch A Launch Capacity formula** (§3.4.1) — R62 replacement (launch-driven retirement). 2 writes (D62 unchanged as anchor + E62 formula + copyToRange).
6. **Patch B Launch Capacity formula** (§3.4.2) — R64 replacement (demand-driven 2027+). 2 writes (D64 + E64 unchanged anchors + F64 demand formula + copyToRange).
7. **Patch E §6.13 Launch Capacity formulas** (§3.5) — R30 (cum stacks NEW), R37 (mfg formula NEW), R38 (ops formula NEW), R39 (D&A LEO formula NEW), R40 (LEO at-cost = D38+D39, replaces Sprint 2 D37+D38+D39), R41 (Moon/Mars at-cost memo NEW). 6 formula sections × 3 writes each = ~18 writes.
8. **Customer Launch module body** (§3.6) — rows 11-199 (TBD exact row map by plugin; spec provides logical structure + canonical labels + formulas; plugin maps to specific row numbers).
9. **Per-launch IRR engine** (§3.7) — F9 + Starship Spot/Forward/Blended IRR with N-period CF streams.
10. **Allocator OUT contract wiring** (§3.8) — overwrites Sprint 1's 11 literal-0 rows at 200-210 with live formulas.

Total estimated discrete writes: ~150-200. Day budget: 1 day.

### §3.2 Patch D execution — Launch Capacity E:AC extensions (FIRST in execution sequence)

Reference: `Sprint_2_to_3_Patch_F9_Retirement_and_Starship_Ops.md` §5.2 (Fix A — extend R71 flat) + §5.3 (Fix B — extend R24/R27/R28 year-chains).

#### §3.2.1 Fix A — Launch Capacity R71 E:AC extension

```
Plugin operation: copyToRange source D71, destination E71:AC71
```

D71 formula in V2.4 is `=D69+D70` (single-cell formula referencing absolute D-column inputs). The copy produces identical $17.75M in every year — flat by design.

**Verification:** Read E71, I71, S71, AC71 — all should equal $17.75M. Then read R77 in same columns — all should equal ~$778 per kg.

#### §3.2.2 Fix B — Launch Capacity R24/R27/R28 E:AC extensions

```
Plugin operation 1 (R24 — Booster fleet BoY):
  Write E24 = =D27   (year-chained: BoY = prior year EoY — Rule 23 exception, intentional)
  copyToRange source E24, destination F24:AC24

Plugin operation 2 (R27 — Booster fleet EoY):
  copyToRange source D27, destination E27:AC27
  (D27 formula =D24+D25-D26 propagates correctly as relative-reference pattern:
   E27 becomes =E24+E25-E26, F27 becomes =F24+F25-F26, etc.)

Plugin operation 3 (R28 — Cum upmass):
  Write E28 = =D28+D33*D29   (year-chained running sum — Rule 23 exception)
  copyToRange source E28, destination F28:AC28
```

R29 (per-launch upmass year-row) check: V2.4 shows R29 IS populated across years (D=150000, I=115000, AC=102500), so R29 propagated correctly in Sprint 2. If pre-flight check reveals R29 D-only, copyToRange D29 → E29:AC29 as plugin operation 4.

**Verification:** Read E24, I24, S24, AC24 — all 0 (boosters built R25 = 0 placeholder, so fleet stays 0). Same pattern for R27, R28. These cells now hold LIVE FORMULAS, not None values.

### §3.3 Assumptions tab amendments

Plugin appends new rows below existing Assumptions §3 + §4 last-used rows per Rule 10. Each amendment is a discrete row addition: (i) label write to column A, (ii) Base Case write to column B, (iii) MC Min to column AG, (iv) MC Max to column AH, (v) MC Distribution to column AI, (vi) Notes to column AJ. Six discrete writes per new row.

For year-row inputs, the year columns D:AC get populated per the year-row pattern. For VAL inputs, only B-column populated.

#### §3.3.1 New Assumptions §3 row — Patch A (F9 retirement rate)

| Field | Value |
|---|---|
| Column A label | `F9 retirement rate (% of launches/year)` |
| Type | VAL (single value) |
| Base Case (B) | `0.01` |
| Notes (C) | `Q4'25 Earth!$B$30. = "Percentage of launches in the current year that result in retirement." Implies ~100-launch fleet-average lifetime under steady-state. Sprint 0 R55 had lifetime reuses per booster = 50 — those two inputs are reconcilable: R55 = 50 caps any individual booster's flights (technical limit), 0.01 = 1% retires on average per launch (probabilistic, captures attrition + mid-life retirement decisions). Patch A amends Launch Capacity R62 to use this rate.` |
| MC Min (AG) | `0.005` |
| MC Max (AH) | `0.02` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `Bookends: 0.5%/launch (= 200-launch lifetime, ultra-conservative) → 2%/launch (= 50-launch lifetime, matches R55). Q4'25 Base Case 1% sits at central tendency.` |

#### §3.3.2 Existing Assumptions row updates — Patch E §6.13

| Row | Label | Old value | New value | MC Min | MC Max | MC Dist | Notes |
|---|---|---|---|---|---|---|---|
| R32 | `Super Heavy manufacturing cost ($mm/unit, base year)` | 35.1 | **54** | 42 | 70 | triangle | Mach33: booster 60% × $90M total mfg = $54M today. ±25% MC range. |
| R33 | `Starship 2nd-stage manufacturing cost ($mm/unit, base)` | 23.4 | **36** | 27 | 50 | triangle | Mach33: ship 40% × $90M total mfg = $36M today. ±25% MC range. |

Plugin operations per row: (i) overwrite B-col Base Case, (ii) write MC Min AG-col, (iii) write MC Max AH-col, (iv) write MC Distribution AI-col, (v) overwrite Notes AJ-col. Label column A unchanged.

#### §3.3.3 R46 step function — Patch E §6.13

R46 `Variant mix (% fully reusable)` year-row in V2.4 is Sprint 0 ramp (D=0, E=0.05, F=0.15, G=0.25, H=0.45, I=0.7, M=0.92, N=0.95, S=0.95, AC=0.95).

Replace with step function per Vlad lock 2026-05-20:

```
Plugin writes year by year (10 discrete writes — each year is a hardcoded value, not a formula):
  D46 = 0   (2025: pre-commercial)
  E46 = 0   (2026: first commercial flight late-year, treat as pre-commercial for full-year accounting)
  F46 = 1.0  (2027: 100% fully reusable)
  G46 through AC46: write 1.0 in each year via copyToRange F46 → G46:AC46
```

After: variant mix is step function. 2025-2026 = 0% reusable (no Starship commercial); 2027-2050 = 100% reusable.

Notes update: `Step function 0 → 1.0 at 2027 per Q4'25 Valuation Inputs!R17 + R23 + Vlad lock 2026-05-20. 2025-2026 are pre-commercial test era (no reusable launches modeled). Sprint 7 Lunar Mars reads booster-only memo R41 for ship-expended Moon/Mars missions; LEO consumers (Sprint 3/4/5/10) read fully-reusable R40.`

#### §3.3.4 R34 DELETE — Patch E §6.13

R34 `Ship refurb % of manufacturing` (Sprint 0 value = 0.02) DELETED per Patch E §6.13 + Vlad lock 2026-05-20 (folded into ops+fuel+refurb cost curve).

```
Plugin operation: delete the entire R34 row from Assumptions tab.
  - Find R34 by MATCH("Ship refurb % of manufacturing", Assumptions!$A:$A, 0)
  - Delete that row (single delete operation)
  - Confirm post-delete that MATCH("Ship refurb % of manufacturing", ...) returns #N/A
```

**Critical:** This is the ONLY DELETE operation in Sprint 3 (Rule 10 exception explicitly Vlad-approved). Plugin executes before any new row appends so the row map below references post-delete state.

**Touch-points check:** After delete, search workbook for any references to "Ship refurb % of manufacturing" label — should be zero (Sprint 2 V2.4 R10 read this row on Launch Capacity, but Patch E §6.13 replaces R37-R40 formulas which removes the R10 / R34 dependency). Sprint 0 spec referenced R34 only in Assumptions §3 input list. No downstream reads.

If plugin finds any non-Assumptions reference to R34's label, halt + push back per Rule 9.

#### §3.3.5 New Assumptions §3 rows — Patch E §6.13 cost stack inputs

Append below Sprint 0's last-used Assumptions §3 row + the §3.3.1 F9 retirement rate row (per Rule 10).

6 new rows for split-cost-curve canonical formulation:

| Label | Base Case | MC Min | MC Max | MC Dist | Notes |
|---|---|---|---|---|---|
| `Starship manufacturing cost anchor ($mm/stack, 2024 baseline)` | **90** | 70 | 130 | triangle | Mach33 today anchor (booster $54M + ship $36M). ±25% MC range captures SpaceX disclosed vs internal estimates. |
| `Starship manufacturing WL learning rate (% reduction per doubling cum stacks)` | **0.15** | 0.10 | 0.25 | triangle | Mach33 stated + Q4'25 R159 + NASA aerospace standard. Q4'25 Valuation Inputs!R21 has same. MC bracket: 10% (conservative aerospace) → 25% (aggressive industrial scale). |
| `Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)` | **4** | 2 | 10 | triangle | Q4'25 R160 default. Represents ~4 successful Starship integrated flight tests through end-2024. MC range covers 2-10 (varying definitions of "successful test"). |
| `Starship ops + fuel + refurb cost anchor ($mm/launch, 2024 baseline)` | **12** | 8 | 20 | triangle | Mach33 today: $10M ops+fuel + $2M refurb. MC range ±50% reflects high uncertainty on Starship ground-handling cost vs Falcon 9 maturity. |
| `Starship ops + fuel + refurb WL learning rate (% reduction per doubling cum stacks)` | **0.10** | 0.05 | 0.15 | triangle | Back-derived from Mach33's three regime anchors ($12M → $5.5M → $3.25M). MC range wider than mfg's because ops+fuel+refurb learning is less-studied. |
| `Starship booster share of manufacturing cost (% of stack mfg)` | **0.60** | 0.50 | 0.70 | triangle | Mach33 booster 60% / ship 40% split. Booster is heavier + 33 Raptors vs ship's 6. MC range captures variant build complexity. |

#### §3.3.6 New Assumptions §3 payload rows — Patch E §6.13 + §6.12

Append below §3.3.5 rows:

| Label | Base Case | MC Min | MC Max | MC Dist | Notes |
|---|---|---|---|---|---|
| `Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)` | **100000** | 75000 | 130000 | triangle | Sprint 0 R12 value retained as 2025 baseline anchor. Q4'25 Earth!I76 has 2024 baseline = 75K kg; Sprint 0 anchored at 100K (slightly more optimistic but defensible for 2025 V3 era). |
| `Starship payload — 2030 anchor (kg-to-LEO, fully reusable mode)` | **200000** | 150000 | 250000 | triangle | Q4'25 Valuation Inputs!R19 median = 200K. Drives the bounded-CAGR year-row. Mach33 1k/yr regime anchor. |
| `Starship payload — max cap (kg-to-LEO)` | **250000** | 200000 | 300000 | triangle | Q4'25 Earth!R74 = 250K (matches Mach33's 10k/yr regime payload anchor). Hard ceiling on R29 per-launch upmass. |
| `Starship payload — booster-only mode delta (kg, additive to fully-reusable payload)` | **50000** | 30000 | 80000 | triangle | The ~50K kg payload bonus from not landing the ship (Sprint 0 R11 − R12 = 150K − 100K = 50K). Applied to booster-only mode (Moon/Mars per Patch E §6.11). |

#### §3.3.7 New Assumptions §4 Customer Launch rows — Sprint 3 inputs (Vlad locks #1 + #2)

Append below Sprint 0's existing §4 row R71 (`Customer Launch depreciation useful life`).

**Vlad lock #1 — Total customer launch market year-row + growth:**

| Label | Type | Base Case | MC Min | MC Max | MC Dist | Notes |
|---|---|---|---|---|---|---|
| `Total customer launch market (launches/yr) — 2025 anchor` | VAL | **38.58** | 30 | 50 | triangle | Q4'25 Earth!R51 anchored value (commercial + government F9 customer launches). 2025-2026 served 100% by F9 (Starship pre-commercial). 2027+ split F9 vs Starship per IRR + capacity gates on Customer Launch tab. |
| `Total customer launch market CAGR (% growth/yr)` | VAL | **0.05** | -0.02 | 0.12 | triangle | Customer launch market grows ~5%/yr as global space economy expands (satellite ops, ISAM, gov contracts). Wide MC range reflects market sizing uncertainty. |

Customer Launch tab uses these to compute total demand year-row via anchor-and-offset: total_demand(year T) = `anchor × (1 + CAGR)^year_offset`.

**Vlad lock #2 — Starship customer launch profit margin (year-row bounded-CAGR):**

| Label | Type | Base Case | MC Min | MC Max | MC Dist | Notes |
|---|---|---|---|---|---|---|
| `Starship customer launch margin — 2027 anchor (multiplier on at-cost rate)` | VAL | **4.0** | 2.0 | 6.0 | triangle | Customer pays 4× SpaceX's at-cost rate during 2027 capacity-constrained early-Starship era. At 2027 Starship at-cost ≈ $19.5M, customer price = $19.5M × 4.0 = $78M. Aligned with Mach33 view that SpaceX captures large margin while Starship capacity scarce. MC range wide because no historical anchor. |
| `Starship customer launch margin — 2050 terminal (multiplier on at-cost rate, floor)` | VAL | **1.5** | 1.2 | 2.5 | triangle | At full industrial scale, margin compresses to 50% (1.5× at-cost) as launch market matures + competition emerges. Still above F9's terminal margin because Starship maintains payload + cadence moat. |
| `Starship customer launch margin — CAGR (% change/yr from 2027 anchor)` | VAL | **-0.045** | -0.08 | -0.02 | triangle | -4.5%/yr brings margin from 4.0 (2027) to 1.5 (2050) over 23 years. Sharper compression in MC Min (-8%/yr); slower in MC Max (-2%/yr). |

Customer Launch tab uses these to compute Starship margin year-row via anchor-and-offset bounded-CAGR pattern (Rule 3 + Rule 23):
- 2025-2026: 0 (no commercial Starship)
- 2027 (F-col): anchor = 4.0
- 2028-2050: bounded-CAGR `MAX(end_floor, anchor × (1 + CAGR)^(year_offset − 2))` where year_offset = E$5 and 2 = year offset of 2027 anchor (F$5 = 2 since D5=0, E5=1, F5=2).

### §3.4 Patch A + B execution on Launch Capacity (formula replacements)

#### §3.4.1 Patch A — Launch Capacity R62 (F9 retirement engine)

Reference: Patch doc §2.3.

```
A62 unchanged: "F9 retired per year (boosters)"

D62 unchanged: =6   (2025 historical anchor: 28 SoY + 17 manufactured − 39 EoY = 6 retired; locks §6.1 calibration)

E62 = =MIN(E60 + E61, E64 * INDEX(Assumptions!$B:$B, MATCH("F9 retirement rate (% of launches/year)", Assumptions!$A:$A, 0)))

copyToRange source E62, destination F62:AC62
```

D62 stays hardcoded at 6 per Sprint 2 calibration anchor. E62 onwards uses Q4'25 mechanic.

#### §3.4.2 Patch B — Launch Capacity R64 (F9 demand-driven wiring)

Reference: Patch doc §3.2.

```
A64 unchanged: "F9 launches per year"

D64 unchanged: =171   (2025 Q4'25 historical anchor)
E64 unchanged: =171   (2026 carryover anchor; pre-V3-ramp)

F64 = =MIN(
         F60 * $D$51,
         IFERROR(INDEX('Customer Launch'!D:D, MATCH("F9 customer launches per year", 'Customer Launch'!$A:$A, 0)), 0)
       + IFERROR(INDEX(Starlink!D:D, MATCH("F9 V2 BB launches (internal)", Starlink!$A:$A, 0)), 0)
       + IFERROR(INDEX(Starlink!D:D, MATCH("F9 V2 DTC launches (internal)", Starlink!$A:$A, 0)), 0)
       )

copyToRange source F64, destination G64:AC64
```

2027 onward: F9 launches = MIN(fleet × cadence, customer demand from Customer Launch + Starlink V2 internal demand). IFERROR wraps because Sprint 3 builds Customer Launch first; Starlink (Sprint 4) hasn't written its rows yet. By Sprint 4 exit those resolve.

### §3.5 Patch E §6.13 execution on Launch Capacity (Starship cost mechanic)

Reference: Patch doc §6.13.4.

#### §3.5.1 NEW row R30 — Cum stacks running sum

```
A30 = "Cum Starship stacks manufactured (end-of-year, units)"

D30 = =INDEX(Assumptions!$B:$B, MATCH("Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)", Assumptions!$A:$A, 0))
   (Anchor: end-2024 cum stacks = 4)

E30 = =D30 + D25   (Rule 23 year-chained running sum; D25 = boosters built = stacks built per year)

copyToRange source E30, destination F30:AC30
```

Format: D30:AC30 integer `#,##0`.

#### §3.5.2 REPURPOSED R37 — Starship manufacturing cost ($mm/stack)

```
A37 = "Starship manufacturing cost ($mm/stack, this year)"   (NEW label — was "Starship variable cost per launch")

D37 = =INDEX(Assumptions!$B:$B, MATCH("Starship manufacturing cost anchor ($mm/stack, 2024 baseline)", Assumptions!$A:$A, 0))
      * (
          D30 / INDEX(Assumptions!$B:$B, MATCH("Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)", Assumptions!$A:$A, 0))
        )^(LOG(1 - INDEX(Assumptions!$B:$B, MATCH("Starship manufacturing WL learning rate (% reduction per doubling cum stacks)", Assumptions!$A:$A, 0)), 2))

copyToRange source D37, destination E37:AC37
```

At cum=4 anchor: $90M × 1 = $90M (constant until Sprint 10 lights up R25 cum-stacks growth).

#### §3.5.3 REPURPOSED R38 — Starship ops+fuel+refurb ($mm/launch)

```
A38 = "Starship ops + fuel + refurb cost per launch ($mm, this year)"   (NEW label)

D38 = =INDEX(Assumptions!$B:$B, MATCH("Starship ops + fuel + refurb cost anchor ($mm/launch, 2024 baseline)", Assumptions!$A:$A, 0))
      * (
          D30 / INDEX(Assumptions!$B:$B, MATCH("Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)", Assumptions!$A:$A, 0))
        )^(LOG(1 - INDEX(Assumptions!$B:$B, MATCH("Starship ops + fuel + refurb WL learning rate (% reduction per doubling cum stacks)", Assumptions!$A:$A, 0)), 2))

copyToRange source D38, destination E38:AC38
```

At cum=4 anchor: $12M (constant until Sprint 10).

#### §3.5.4 REPURPOSED R39 — Starship D&A share LEO mode ($mm/launch)

```
A39 = "Starship D&A share per launch, fully reusable mode ($mm)"   (NEW label)

D39 = =IFERROR(
        D37 * (
          INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0)) / D21
        + (1 - INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0))) / $D$13
        )
        , 0)

copyToRange source D39, destination E39:AC39
```

At cum=4 2025 with R21=5, $D$13=30: D39 = $90M × (0.60/5 + 0.40/30) = $90M × 0.1333 = $12M.
At 2030 R21=30: $90M × (0.60/30 + 0.40/30) = $3M.
At 2050 R21=100: $90M × (0.60/100 + 0.40/30) = $1.74M.

#### §3.5.5 R40 — Starship LEO at-cost rate (REPLACES Sprint 2 formula)

```
A40 = "Starship at-cost rate ($mm/launch)"   (UNCHANGED label — canonical Sprint 3/4/5/10 read)

D40 = =D38 + D39   (NEW formula: ops+fuel+refurb per launch + D&A share)

copyToRange source D40, destination E40:AC40
```

At cum=4 2025: D40 = $12M + $12M = **$24.0M** (down from Sprint 2 pre-patch $30.42M).
At 2030 (Sprint 2 R25=0 placeholder, cum still 4): D40 = $12M + $3M = **$15M**.

#### §3.5.6 NEW R41 — Starship Moon/Mars at-cost memo

```
A41 = "Memo: Starship at-cost rate, ship-expended mode (Moon/Mars, $mm/launch)"

D41 = =D38
      + IFERROR(D37 * INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0)) / D21, 0)
      + D37 * (1 - INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0)))

copyToRange source D41, destination E41:AC41
```

At cum=4 2025: D41 = $12M + $10.8M + $36M = **$58.8M**.
Sprint 7 Lunar Mars reads R41 by label.

### §3.6 Customer Launch module body — cell-by-cell build (rows 11–199)

Plugin maps logical rows below to specific Customer Launch tab row numbers. Row numbers in §3.6.X are spec-suggested; plugin may adjust as long as canonical labels match and writes stay in 11–199 range.

#### §3.6.0 Section headers + subsections

Sprint 3 builds the module body in 6 logical sections. Suggested row map (plugin confirms exact rows post-Sprint-1):

```
R12 (SECT): "CUSTOMER LAUNCH — MODULE BODY"
R13: blank spacer
R14 (SUB): "▸ Demand mechanic (total market + F9 vs Starship split via IRR + capacity)"
R15-R30: Demand mechanic rows
R31: blank spacer
R32 (SUB): "▸ F9 customer launches — economics"
R33-R45: F9 customer revenue, price, cost
R46: blank spacer
R47 (SUB): "▸ Starship customer launches — economics"
R48-R65: Starship customer revenue, price (= at-cost × margin), cost
R66: blank spacer
R67 (SUB): "▸ Internal transfer revenue (launch services to Sprint 4/5/6 consumers)"
R68-R80: Internal transfer mechanism rows
R81: blank spacer
R82 (SUB): "▸ Module P&L (vending-machine: Revenue → COGS → Module EBITDA → CapEx → FCF)"
R83-R115: P&L rows
R116: blank spacer
R117 (SUB): "▸ Per-launch marginal IRR engines (F9 + Starship, external customer only)"
R118-R175: IRR engine helper rows + final Spot/Forward/Blended IRR per vehicle
R176: blank spacer
R177 (SUB): "▸ Memo: Allocator OUT diagnostic checks"
R178-R199: memo / diagnostic rows
```

Plugin writes section + subsection headers as discrete label-only writes (Rule 1). Format: SECT = white-on-charcoal fill bold; SUB = italic light grey fill.

#### §3.6.1 Demand mechanic (rows 15–30)

**Row 15: Total customer launch market year-row.**

```
A15 = "Total customer launch market (launches/yr)"

D15 = =INDEX(Assumptions!$B:$B, MATCH("Total customer launch market (launches/yr) — 2025 anchor", Assumptions!$A:$A, 0))
   (Anchor at 2025 = 38.58)

E15 = =$D$15 * (1 + INDEX(Assumptions!$B:$B, MATCH("Total customer launch market CAGR (% growth/yr)", Assumptions!$A:$A, 0)))^E$5
   (Anchor-and-offset bounded-CAGR per Rule 3 + Rule 23)

copyToRange source E15, destination F15:AC15
```

Expected: D15 = 38.58, I15 = 38.58 × 1.05^5 = 49.24, S15 = 38.58 × 1.05^15 = 80.21, AC15 = 38.58 × 1.05^25 = 130.7.

**Row 16: Starship customer launch margin multiplier year-row.**

```
A16 = "Starship customer launch margin multiplier (year-row)"

D16 = 0   (no Starship commercial in 2025)
E16 = 0   (no Starship commercial in 2026; first commercial flight late H2 2026 — full-year accounting at 0)
F16 = =INDEX(Assumptions!$B:$B, MATCH("Starship customer launch margin — 2027 anchor (multiplier on at-cost rate)", Assumptions!$A:$A, 0))
   (2027 anchor = 4.0)

G16 = =MAX(
        INDEX(Assumptions!$B:$B, MATCH("Starship customer launch margin — 2050 terminal (multiplier on at-cost rate, floor)", Assumptions!$A:$A, 0)),
        $F$16 * (1 + INDEX(Assumptions!$B:$B, MATCH("Starship customer launch margin — CAGR (% change/yr from 2027 anchor)", Assumptions!$A:$A, 0)))^(G$5 - 2)
      )
   (Bounded-CAGR floored at terminal; G$5 - 2 = year offset from 2027 anchor at F$5 = 2)

copyToRange source G16, destination H16:AC16
```

Expected: D16 = 0, E16 = 0, F16 = 4.0, I16 = MAX(1.5, 4.0 × 0.955^3) = MAX(1.5, 3.484) = 3.484, S16 = MAX(1.5, 4.0 × 0.955^13) = MAX(1.5, 2.193) = 2.193, AC16 = MAX(1.5, 4.0 × 0.955^23) = MAX(1.5, 1.385) = 1.5 (clamped at floor).

**Row 17: F9 customer launch price year-row (read from Sprint 0 R63).**

```
A17 = "F9 customer launch price ($mm/launch)"

D17 = =INDEX(Assumptions!$D:$AC, MATCH("F9 customer launch price ($mm/launch) — 2025 anchor", Assumptions!$A:$A, 0), D$5+1)
   (Sprint 0 R63 year-row; D5=0 → col 1 = year 2025 = $111M)

copyToRange source D17, destination E17:AC17
```

Expected: D17 = $111M, I17 = $111M × 0.97^5 = $95.4M, S17 = $111M × 0.97^15 = $70.7M, AC17 = $111M × 0.97^25 = $52.4M.

**Row 18: Starship customer launch price ($mm/launch) — derived from at-cost × margin.**

```
A18 = "Starship customer launch price ($mm/launch)"

D18 = =IFERROR(D16 * INDEX('Launch Capacity'!$D:$AC, MATCH("Starship at-cost rate ($mm/launch)", 'Launch Capacity'!$A:$A, 0), D$5+1), 0)
   (= margin year-row × Starship LEO at-cost rate from Launch Capacity R40)
   (At D16=0: D18=0. At F16=4.0 and Launch Capacity F40 ≈ $19.5M: F18 = $78M.)

copyToRange source D18, destination E18:AC18
```

Expected: D18 = 0 × $24M = $0, E18 = 0 × $24M = $0, F18 = 4.0 × $19.5M = $78M, I18 = 3.484 × $15.0M = $52.3M (assuming Sprint 2 R25=0 placeholder; R40 stays flat at low cum-stacks), S18 = 2.193 × $13.74M = $30.1M, AC18 = 1.5 × $13.74M = $20.6M.

**Row 19: blank spacer.**

**Row 20: Starship Total Annual Capacity (kg-to-LEO) — read from Launch Capacity R34.**

```
A20 = "Starship Total Annual Capacity (kg-to-LEO) — from Launch Capacity"

D20 = =INDEX('Launch Capacity'!$D:$AC, MATCH("Total Annual Capacity (kg-to-LEO)", 'Launch Capacity'!$A:$A, 0), D$5+1)

copyToRange source D20, destination E20:AC20
```

Expected: 0 throughout Sprint 3 (Sprint 10 Allocator brain writes R25 cum stacks → fleet → launches → capacity).

**Row 21: Per-launch upmass — read from Launch Capacity R29.**

```
A21 = "Per-launch upmass (kg) — from Launch Capacity"

D21 = =INDEX('Launch Capacity'!$D:$AC, MATCH("Per-launch upmass (kg)", 'Launch Capacity'!$A:$A, 0), D$5+1)

copyToRange source D21, destination E21:AC21
```

**Row 22: Internal Starship demand from Sprint 4 + 5 + 6 (IFERROR-0 wrappers).**

```
A22 = "Starship internal kg demand (post-Starlink + ODC + AI Stack)"

D22 = =IFERROR(INDEX(Starlink!$D:$AC, MATCH("V3 BB Starship kg demand", Starlink!$A:$A, 0), D$5+1), 0)
      + IFERROR(INDEX(Starlink!$D:$AC, MATCH("V3 DTC Starship kg demand", Starlink!$A:$A, 0), D$5+1), 0)
      + IFERROR(INDEX(ODC!$D:$AC, MATCH("ODC Starship kg demand", ODC!$A:$A, 0), D$5+1), 0)
      + IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("AI Stack Starship kg demand", 'AI Stack'!$A:$A, 0), D$5+1), 0)

copyToRange source D22, destination E22:AC22
```

Expected: 0 throughout Sprint 3 (Sprint 4/5/6 haven't fired). Lights up in those sprints.

**Row 23: Starship customer capacity available (kg).**

```
A23 = "Starship capacity available for customer launches (kg)"

D23 = =MAX(0, D20 - D22)

copyToRange source D23, destination E23:AC23
```

Expected: 0 throughout Sprint 3 (D20 = 0).

**Row 24: Starship customer launches per year — IRR + capacity gated.**

```
A24 = "Starship customer launches per year"

D24 = 0   (2025 hardcoded: no Starship commercial)
E24 = 0   (2026 hardcoded: no Starship commercial — pre-2027 lock)
F24 = =IF(
        AND(
          INDEX($A:$AC, MATCH("Starship per-launch Blended IRR (external customer economics)", $A:$A, 0), F$5+4) > 0,
          D16 > 0
        ),
        MIN(
          $D$15 * (1 + INDEX(Assumptions!$B:$B, MATCH("Total customer launch market CAGR (% growth/yr)", Assumptions!$A:$A, 0)))^F$5,
          IFERROR(F23 / F21, 0)
        ),
        0
      )
   (2027+ gating: if Starship IRR > 0 AND margin > 0 (= Starship commercial), Starship takes the min of total demand and unused capacity in launches.
    Total demand reads forward from $D$15 anchor.
    Unused capacity in launches = capacity_kg / per-launch upmass.)

copyToRange source F24, destination G24:AC24
```

Note: This formula references its own per-launch IRR row by label (forward dependency — Starship IRR row lives in §3.7 below). The plugin writes IRR rows first (§3.7), THEN populates row 24's F-column formula. Execution sequence per §8.

Expected at Sprint 3 exit (with Sprint 4/5/6 demand = 0): D24/E24 = 0; F24 onward = MIN(market_demand × growth, capacity / upmass) — but capacity = 0 from Launch Capacity, so F24+ = 0.

**Row 25: F9 customer launches per year — residual after Starship + IRR gate.**

```
A25 = "F9 customer launches per year"

D25 = 38.58   (Q4'25 anchor: 2025 historical)
E25 = =$D$25 * (1 + INDEX(Assumptions!$B:$B, MATCH("Total customer launch market CAGR (% growth/yr)", Assumptions!$A:$A, 0)))   (2026 carryover: total market growth, Starship not commercial)
F25 = =IF(
        INDEX($A:$AC, MATCH("F9 per-launch Blended IRR (external customer economics)", $A:$A, 0), F$5+4) > 0,
        MAX(0, 
          $D$15 * (1 + INDEX(Assumptions!$B:$B, MATCH("Total customer launch market CAGR (% growth/yr)", Assumptions!$A:$A, 0)))^F$5
          - F24
        ),
        0
      )
   (2027+ gating: if F9 IRR > 0, F9 takes the residual after Starship absorbs its capped share.
    No F9 capacity check here — Sprint 2 Launch Capacity R68 F9 Annual Capacity (kg-to-LEO) is uncapped at 7.66M kg (39 fleet × 12 cadence × 22.8K kg), well above 50 customer launches × 22.8K kg = 1.14M kg.)

copyToRange source F25, destination G25:AC25
```

Expected: D25 = 38.58, E25 ≈ 38.58 × 1.05 = 40.51, F25 ≈ MAX(0, 38.58 × 1.05^2 − 0) = 42.54 (Sprint 3 Starship at 0 because capacity = 0; once Sprint 4/5 fire + Sprint 10 lights up vehicle build, this rebalances).

**Touch points for §3.6.1:**
- Row 25 (`F9 customer launches per year`) is read by Patch B Launch Capacity R64 (§3.4.2 above) — canonical label MUST match exactly.
- Row 24 (`Starship customer launches per year`) is read by Sprint 5 ODC kg conservation memo (future) and Sprint 11 Valuation.

#### §3.6.2 F9 customer revenue + cost (rows 33–45)

**Row 33: F9 customer revenue ($mm).**

```
A33 = "F9 customer revenue ($mm)"

D33 = =D25 * D17   (= F9 customer launches × F9 customer launch price)
copyToRange source D33, destination E33:AC33
```

Expected: D33 = 38.58 × $111M = $4,282M (matches Q4'25 anchor $4,290M within rounding).

**Row 34: F9 variable cost per launch ($mm).**

```
A34 = "F9 variable cost per launch ($mm) — read from Launch Capacity"

D34 = =INDEX('Launch Capacity'!$D:$AC, MATCH("F9 variable cost per launch ($mm)", 'Launch Capacity'!$A:$A, 0), D$5+1)
   (Reads Launch Capacity R69 = single-value $13.75M — Sprint 2 V2.4 confirmed)

copyToRange source D34, destination E34:AC34
```

Expected: D34 = $13.75M flat across years (F9 cost stack is flat).

**Row 35: F9 D&A share per launch ($mm).**

```
A35 = "F9 D&A share per launch ($mm) — read from Launch Capacity"

D35 = =INDEX('Launch Capacity'!$D:$AC, MATCH("F9 booster D&A share per launch ($mm)", 'Launch Capacity'!$A:$A, 0), D$5+1)
   (Reads Launch Capacity R70 = single-value $4M = R44 / R50 = $30M / 50 lifetime reuses — Sprint 2 V2.4 confirmed)

copyToRange source D35, destination E35:AC35
```

Expected: D35 = $4M flat.

**Row 36: F9 at-cost rate per launch ($mm) — read from Launch Capacity R71.**

```
A36 = "F9 at-cost rate ($mm/launch) — read from Launch Capacity"

D36 = =INDEX('Launch Capacity'!$D:$AC, MATCH("F9 at-cost rate ($mm/launch)", 'Launch Capacity'!$A:$A, 0), D$5+1)

copyToRange source D36, destination E36:AC36
```

Expected: D36 = $17.75M flat.

**Row 37: F9 customer launch insurance + other COGS ($mm/launch).**

```
A37 = "F9 customer launch insurance + other COGS ($mm/launch)"

D37 = =D33 * (INDEX(Assumptions!$B:$B, MATCH("Insurance % of revenue", Assumptions!$A:$A, 0)) + INDEX(Assumptions!$B:$B, MATCH("Other COGS % of revenue", Assumptions!$A:$A, 0)))
   (Per-launch insurance + other COGS = (insurance% + other%) × per-launch revenue)
   Wait — this should be per-launch, so divide by launches:

D37 = =IFERROR(D33 / D25, 0) * (INDEX(Assumptions!$B:$B, MATCH("Insurance % of revenue", Assumptions!$A:$A, 0)) + INDEX(Assumptions!$B:$B, MATCH("Other COGS % of revenue", Assumptions!$A:$A, 0)))
   (= per-launch revenue × (insurance% + other%); reduces to F9 customer launch price × (i% + o%))

copyToRange source D37, destination E37:AC37
```

Note: Architecture §5.2 says module COGS includes "insurance + other COGS %" as a % of revenue. Sprint 0 should have inputs `Insurance % of revenue` and `Other COGS % of revenue` — plugin verifies via MATCH lookup. If labels differ slightly (e.g. `Insurance % rev`), plugin halts per Rule 9 and pushes back.

If Sprint 0 doesn't have these rows, mark as Open Thread (§7) and use 0.01 + 0.01 = 0.02 placeholder (2% combined) with explicit memo: insurance ≈ 1% of revenue, other COGS ≈ 1% of revenue.

#### §3.6.3 Starship customer revenue + cost (rows 48–65)

Same pattern as §3.6.2 for Starship.

**Row 48: Starship customer revenue ($mm).**

```
A48 = "Starship customer revenue ($mm)"

D48 = =D24 * D18   (= Starship customer launches × Starship customer launch price)
copyToRange source D48, destination E48:AC48
```

Expected: D48 = 0 × $0 = $0 (2025 Starship pre-commercial); E48 = 0 × $0 = $0; F48 ≈ Starship customer launches × $78M (varies with Sprint 4/5/10 wiring).

**Rows 49–52: Starship variable, D&A share, at-cost rate, insurance+other.** (Same structure as F9; reads Launch Capacity R38, R39, R40 by label.)

#### §3.6.4 Internal transfer revenue (rows 68–80)

Per Architecture §7.1 4-step pattern + Rule 21.

**Row 68: F9 internal launches (consumed by Starlink V2 BB + DTC — Sprint 4 will publish).**

```
A68 = "F9 internal launches (BB + DTC)"

D68 = =IFERROR(INDEX(Starlink!$D:$AC, MATCH("F9 V2 BB launches (internal)", Starlink!$A:$A, 0), D$5+1), 0)
      + IFERROR(INDEX(Starlink!$D:$AC, MATCH("F9 V2 DTC launches (internal)", Starlink!$A:$A, 0), D$5+1), 0)

copyToRange source D68, destination E68:AC68
```

Expected: 0 throughout Sprint 3 (Sprint 4 hasn't fired). Lights up in Sprint 4.

**Row 69: Starship internal launches (consumed by Starlink V3 + ODC + AI Stack — Sprints 4/5/6 will publish).**

```
A69 = "Starship internal launches (V3 BB + V3 DTC + ODC + AI Stack)"

D69 = =IFERROR(F22 / D21, 0)   (= internal kg demand / per-launch upmass; reads row 22 above)

Actually wait — row 22 reads kg demand. We need launches not kg. The reconciliation:
Starlink V3 BB internal launches = V3 BB sats deployed × mass per V3 BB sat / per-launch upmass.
Sprint 4 will publish "Starship V3 BB launches (internal)", "Starship V3 DTC launches (internal)" directly. Sprint 5 ODC publishes "ODC Starship launches (internal)". Sprint 6 AI Stack: AI Stack has 0 kg demand per Architecture §10.4.

So row 69:

D69 = =IFERROR(INDEX(Starlink!$D:$AC, MATCH("Starship V3 BB launches (internal)", Starlink!$A:$A, 0), D$5+1), 0)
      + IFERROR(INDEX(Starlink!$D:$AC, MATCH("Starship V3 DTC launches (internal)", Starlink!$A:$A, 0), D$5+1), 0)
      + IFERROR(INDEX(ODC!$D:$AC, MATCH("ODC Starship launches (internal)", ODC!$A:$A, 0), D$5+1), 0)

copyToRange source D69, destination E69:AC69
```

Expected: 0 throughout Sprint 3.

**Row 70: Customer Launch internal transfer revenue ($mm) — the CANONICAL row Sprint 9 R105 reads for elimination.**

```
A70 = "Customer Launch internal transfer revenue ($mm)"

D70 = =D68 * D36 + D69 * INDEX('Launch Capacity'!$D:$AC, MATCH("Starship at-cost rate ($mm/launch)", 'Launch Capacity'!$A:$A, 0), D$5+1)
   (= F9 internal launches × F9 at-cost + Starship internal launches × Starship at-cost LEO mode)

copyToRange source D70, destination E70:AC70
```

Expected: 0 throughout Sprint 3 (D68 = 0, D69 = 0). Lights up in Sprint 4/5 endogenously.

**Touch points for §3.6.4:**
- Row 70 (`Customer Launch internal transfer revenue ($mm)`) is read by Sprint 9 Group P&L R105 elimination conservation. Canonical label.
- Per Rule 21 4-step: source = row 70 here, consumers = Sprint 4/5/6 future Launch services cost rows in their COGS, elimination = Sprint 9 R105, conservation = R105 verifies match.

#### §3.6.5 P&L (rows 83–115)

Vending-machine framing (Architecture §3 + Rule 13). No R&D / SG&A / overhead / taxes.

**Row 83: Total Revenue ($mm).**

```
A83 = "Total Revenue ($mm)"

D83 = =D33 + D48 + D70   (= F9 customer revenue + Starship customer revenue + Internal transfer revenue)

copyToRange source D83, destination E83:AC83
```

Expected: D83 = $4,282M + $0 + $0 = $4,282M (matches Q4'25 anchor within tolerance).

**Row 84: COGS section header.**

```
A84 (SUB) = "▸ COST OF GOODS SOLD ($mm)"
```

**Rows 85–93: COGS components.**

```
A85 = "F9 variable cost ($mm)"
D85 = =D25 * D34 + D68 * D34   (= (customer F9 launches + internal F9 launches) × F9 variable cost per launch)

A86 = "F9 D&A share ($mm)"
D86 = =D25 * D35 + D68 * D35   (= total F9 launches × F9 D&A share per launch)

A87 = "Starship variable cost ($mm)"
D87 = =D24 * INDEX('Launch Capacity'!$D:$AC, MATCH("Starship ops + fuel + refurb cost per launch ($mm, this year)", 'Launch Capacity'!$A:$A, 0), D$5+1)
      + D69 * INDEX('Launch Capacity'!$D:$AC, MATCH("Starship ops + fuel + refurb cost per launch ($mm, this year)", 'Launch Capacity'!$A:$A, 0), D$5+1)

A88 = "Starship D&A share ($mm)"
D88 = =D24 * INDEX('Launch Capacity'!$D:$AC, MATCH("Starship D&A share per launch, fully reusable mode ($mm)", 'Launch Capacity'!$A:$A, 0), D$5+1)
      + D69 * INDEX('Launch Capacity'!$D:$AC, MATCH("Starship D&A share per launch, fully reusable mode ($mm)", 'Launch Capacity'!$A:$A, 0), D$5+1)

A89 = "Customer Launch ground ops % of revenue ($mm)"
D89 = =D83 * IFERROR(INDEX(Assumptions!$B:$B, MATCH("Customer Launch ground ops % of revenue", Assumptions!$A:$A, 0)), 0.01)

A90 = "Customer Launch insurance ($mm)"
D90 = =D83 * IFERROR(INDEX(Assumptions!$B:$B, MATCH("Customer Launch insurance % of revenue", Assumptions!$A:$A, 0)), 0.01)

A91 = "Customer Launch other COGS ($mm)"
D91 = =D83 * IFERROR(INDEX(Assumptions!$B:$B, MATCH("Customer Launch other COGS % of revenue", Assumptions!$A:$A, 0)), 0.01)

A92 = (blank — reserved for future bandwidth/compute internal cost lines — Customer Launch doesn't consume from other modules per Architecture §3 footprint)

A93 = "Total COGS ($mm)"
D93 = =SUM(D85:D92)

copyToRange source D{row}, destination E{row}:AC{row} for each of D85, D86, D87, D88, D89, D90, D91, D93
```

If Sprint 0 doesn't have rows `Customer Launch ground ops % of revenue` / `Customer Launch insurance % of revenue` / `Customer Launch other COGS % of revenue` (which is likely — Sprint 0 only had Module-specific cost rows for Starlink), plugin uses IFERROR fallback to 0.01 (1%) per Sprint 0 Spec §3.6 typical placeholder. Mark as Open Thread (§7) for Sprint 8 to add these to Assumptions properly with MC ranges.

**Row 94: Gross Profit ($mm).**

```
A94 = "Gross Profit ($mm)"
D94 = =D83 - D93
copyToRange source D94, destination E94:AC94
```

**Row 95: Module EBITDA ($mm) = Gross Profit (single canonical EBITDA per Principle 7).**

```
A95 = "Module EBITDA ($mm)"
D95 = =D94
copyToRange source D95, destination E95:AC95
```

**Row 96: Module EBITDA Margin %.**

```
A96 = "Module EBITDA Margin %"
D96 = =IFERROR(D95 / D83, 0)
copyToRange source D96, destination E96:AC96
```

**Rows 97–98: blank + section header.**

```
A97: blank
A98 (SUB) = "▸ CAPEX + FCF"
```

**Row 99: Module CapEx ($mm).** Per Architecture §4.2 (Sprint 3 sets the convention):

```
A99 = "Module CapEx ($mm)"
D99 = =D83 * IFERROR(INDEX(Assumptions!$B:$B, MATCH("Customer Launch ground equipment CapEx % of revenue", Assumptions!$A:$A, 0)), 0.005)
   (= ground equipment + customer integration; NOT vehicle build per Architecture §6.6)

copyToRange source D99, destination E99:AC99
```

Expected: D99 ≈ $4,282M × 0.5% = $21M (rough). If Sprint 0 doesn't have the row, fallback 0.5% via IFERROR. Open Thread for Sprint 8.

**Row 100: Module D&A ($mm).** For Customer Launch the D&A flows through from Launch Capacity R39 (Starship LEO D&A share) and R70 (F9 D&A share) into COGS rows 86 + 88. Module D&A line on Allocator OUT is informational:

```
A100 = "Module D&A ($mm) — informational (also in COGS rows 86 + 88)"
D100 = =D86 + D88   (= F9 D&A + Starship D&A captured in COGS)
copyToRange source D100, destination E100:AC100
```

**Row 101: Module FCF ($mm).** Per Architecture §4.2:

```
A101 = "Module FCF ($mm)"
D101 = =D95 + D100 - D99   (= EBITDA + D&A add-back − CapEx; pre-tax pre-corp per vending-machine)
copyToRange source D101, destination E101:AC101
```

**Row 102: Capital deployed ($mm).** Per Architecture §4.2 + Sprint 3 lock #2 (locked-this-sprint decision per Sprint Roadmap §3 Sprint 3):

```
A102 = "Capital deployed ($mm)"
D102 = =D99   (= Module CapEx; Customer Launch has no CapEx lag, equilibrium-equal convention sets default for subsequent modules)
copyToRange source D102, destination E102:AC102
```

#### §3.6.6 Per-launch IRR engine — F9 + Starship (rows 118–175)

Per Architecture §5.1 IRR formula pattern + Vlad lock #4 2026-05-20 (N = lifetime reuses clamped at R23 = 10).

**N derivation rows.**

```
A118 = "F9 lifetime reuses per booster — read from Assumptions"
D118 = =INDEX(Assumptions!$B:$B, MATCH("F9 lifetime reuses per booster", Assumptions!$A:$A, 0))
   (Sprint 0 R50 = 50 single-value)

A119 = "F9 IRR cashflow stream period count N (clamped at R23 MAX)"
D119 = =MIN(INDEX(Assumptions!$B:$B, MATCH("MFW-IRR — Customer Launch economic life clamp MAX (years)", Assumptions!$A:$A, 0)), D118)
   (= MIN(10, 50) = 10 for F9)

A120 = "Starship lifetime reuses per booster — year-row from Launch Capacity R21"
D120 = =INDEX('Launch Capacity'!$D:$AC, MATCH("Lifetime reuses per booster (year cap)", 'Launch Capacity'!$A:$A, 0), D$5+1)
copyToRange source D120, destination E120:AC120
   (Year-row: D120=5, I120=15, S120=60, AC120=100)

A121 = "Starship IRR cashflow stream period count N (clamped at R23 MAX, year-row)"
D121 = =MIN(INDEX(Assumptions!$B:$B, MATCH("MFW-IRR — Customer Launch economic life clamp MAX (years)", Assumptions!$A:$A, 0)), D120)
copyToRange source D121, destination E121:AC121
   (= MIN(10, 5..100) = varies: D121=5, I121=10, S121=10, AC121=10)
```

**F9 per-launch IRR.**

Cashflow stream construction per Architecture §5.1:
- t=0: cost slug = F9 booster cost (Sprint 0 R44 = $30M) — anchored, single value
- t=1..N: cadence × per-launch margin (= cadence × (price − variable_cost − D&A share − insurance/other))
- N = D119 = 10 years

Wait — Architecture §5.2 says net_marginal_revenue_per_launch = (price − variable − D&A_share − insurance − other). And t=0 cost = cost_per_unit. The question is: what's cost_per_unit?

Reading Architecture §5.1 closer: `cost_per_unit = sat unit cost + launch cost per sat (for sat modules); ship build cost (for Customer Launch); ...`

For Customer Launch, cost_per_unit = ship build cost = vehicle full cost.
- For F9: full booster cost = Sprint 0 R44 = $30M.
- For Starship: full stack cost = Patch E §6.13 R37 manufacturing cost ($mm/stack) at current year — varies via Wright's Law.

Net marginal revenue per period (year) = cadence × (per-launch margin where margin = price − variable cost only — NOT D&A_share which is in the t=0 capex slug).

```
A130 = "F9 per-launch cost slug ($mm — t=0 capex)"
D130 = =INDEX(Assumptions!$B:$B, MATCH("F9 booster (1st stage) mfg cost ($mm/unit, base year)", Assumptions!$A:$A, 0))
   (Sprint 0 R44 = $30M single value)

A131 = "F9 per-launch annual margin ($mm/yr — cadence × per-launch margin)"
D131 = =INDEX(Assumptions!$B:$B, MATCH("F9 cadence per booster (flights/year, flat)", Assumptions!$A:$A, 0))
      * (D17 - D34 - D37)
   (= cadence × (customer price − variable cost − insurance/other; D&A excluded because it's in t=0 cost slug))

copyToRange source D131, destination E131:AC131
```

Expected: D131 = 12 × ($111 − $13.75 − $4.28) = 12 × $92.97 = $1,116M (per year).

Hmm — this is enormous. IRR will be 1000%+ even at low N. Sprint Roadmap §6.2 calibration target 8-25% is likely a holdover from V30.5 fleet-level MFW-IRR — not achievable with marginal per-launch IRR. Flag in Open Thread (§7).

Spot IRR formula per Architecture §5.1:
```
A132 = "F9 Spot IRR (per-launch marginal IRR, current year — external customer economics)"
D132 = =IFERROR(IRR(IF(_xlfn.SEQUENCE(1, $D$119+1)=1, -$D$130, D131)), -1)
   (CF stream: [-D130, D131, D131, ..., D131] of length N+1 where N = D119 = 10)

copyToRange source D132, destination E132:AC132
   (E132 reads E131 etc — relative reference shifts; works for year-row IRR)
```

Forward IRR (Y+2) per Architecture §5.1 — uses year T+2 inputs:
```
A133 = "F9 Forward IRR (Y+2) — per-launch marginal IRR, year T+2 cashflow"
D133 = =IFERROR(IRR(IF(_xlfn.SEQUENCE(1, $D$119+1)=1, -$D$130, F131)), -1)
   (CF stream uses F131 = year 2027 cashflow; row 131 with column offset +2)

For E133:AC133, the relative ref pattern shifts as well. E133 reads G131 (= 2028 cashflow); F133 reads H131; etc. Implemented via copyToRange after E133 written manually.

copyToRange source E133, destination F133:AC133
```

Blended IRR:
```
A134 = "F9 per-launch Blended IRR (external customer economics)"
D134 = =(1 - INDEX(Assumptions!$B:$B, MATCH("Forward weight", Assumptions!$A:$A, 0))) * D132
      + INDEX(Assumptions!$B:$B, MATCH("Forward weight", Assumptions!$A:$A, 0)) * D133
   (= (1−w) × Spot + w × Forward where w = Sprint 0 Forward_weight = 0.7)

copyToRange source D134, destination E134:AC134
```

**Starship per-launch IRR.** Same pattern but with year-varying cost slug (R37 manufacturing cost from Launch Capacity, varies via Wright's Law) and year-varying N (D121).

```
A140 = "Starship per-launch cost slug ($mm — year-row of manufacturing cost from Launch Capacity R37)"
D140 = =INDEX('Launch Capacity'!$D:$AC, MATCH("Starship manufacturing cost ($mm/stack, this year)", 'Launch Capacity'!$A:$A, 0), D$5+1)

copyToRange source D140, destination E140:AC140
   (At cum=4 anchor: D140 = $90M; once Sprint 10 lights up, declines via WL)

A141 = "Starship per-launch annual margin ($mm/yr — cadence × per-launch margin)"
D141 = =INDEX('Launch Capacity'!$D:$AC, MATCH("Launches per Starship vehicle per year (cadence)", 'Launch Capacity'!$A:$A, 0), D$5+1)
      * (D18 - INDEX('Launch Capacity'!$D:$AC, MATCH("Starship ops + fuel + refurb cost per launch ($mm, this year)", 'Launch Capacity'!$A:$A, 0), D$5+1) - IFERROR(D48 / D24, 0) * (INDEX(Assumptions!$B:$B, MATCH("Customer Launch insurance % of revenue", Assumptions!$A:$A, 0)) + INDEX(Assumptions!$B:$B, MATCH("Customer Launch other COGS % of revenue", Assumptions!$A:$A, 0))))
   (= cadence × (Starship customer price − ops+fuel+refurb − insurance/other share); D&A excluded because it's in t=0 cost slug)

copyToRange source D141, destination E141:AC141
```

Expected: D141 = 0 (2025: customer launches = 0 → margin formulas divide-by-zero protected by IFERROR; per-launch margin = 0).

Spot / Forward / Blended Starship IRR same pattern as F9 with N year-row reference:
```
A142 = "Starship Spot IRR"
D142 = =IFERROR(IRR(IF(_xlfn.SEQUENCE(1, $D$121+1)=1, -$D$140, D141)), -1)
   (CF stream uses D121 = 5 in 2025, 10 from 2027+. Note: $D$121 absolute — actually should be relative since N varies per year.)

Better: D142 = =IFERROR(IRR(IF(_xlfn.SEQUENCE(1, D121+1)=1, -D140, D141)), -1)
   (D121 relative — each year reads its own N value.)

copyToRange source D142, destination E142:AC142
```

A143 = "Starship Forward IRR (Y+2)"
D143 = =IFERROR(IRR(IF(_xlfn.SEQUENCE(1, F121+1)=1, -F140, F141)), -1)

copyToRange source E143, destination F143:AC143

A144 = "Starship per-launch Blended IRR (external customer economics)"
D144 = =(1 - INDEX(Assumptions!$B:$B, MATCH("Forward weight", Assumptions!$A:$A, 0))) * D142
      + INDEX(Assumptions!$B:$B, MATCH("Forward weight", Assumptions!$A:$A, 0)) * D143

copyToRange source D144, destination E144:AC144

Expected: D144 = 0 (no Starship commercial 2025); D144 from 2027 onwards depends on margin year-row + Starship cost trajectory. Likely large positive (similar to F9).

**Row 24 + Row 25 reference back:** As noted in §3.6.1, rows 24 and 25 reference IRR rows 144 and 134 respectively. After writing IRR rows 130-144, plugin returns to rows 24-25 and re-confirms F-col references resolve.

#### §3.6.7 Memo + diagnostic rows (rows 178–199)

```
A178 (SUB) = "▸ Memo: 2025 calibration anchors"
A179 = "Memo: F9 customer launches 2025"
D179 = =D25
A180 = "Memo: F9 customer revenue 2025 (target $4,290M ±5%)"
D180 = =D33
A181 = "Memo: Starship customer revenue 2025 (target $0 exact)"
D181 = =D48
A182 = "Memo: 2025 calibration PASS/CHECK"
D182 = =IF(AND(ABS(D179-38.58)<2, ABS(D180-4290)/4290<0.05, ABS(D181)<1), "PASS", "CHECK")
```

Format: italic + light grey for memo rows; D182 conditional format green for PASS, red for CHECK.

### §3.7 Per-launch IRR engine — included in §3.6.6 above

Per-launch IRR engine inline in §3.6.6 to keep formula context locality. Rows 118-144 cover N derivation, cost slug, annual margin, Spot/Forward/Blended IRR per vehicle. F9 IRR rows 130-134; Starship IRR rows 140-144.

### §3.8 Allocator OUT contract — overwrite Sprint 1 placeholders (rows 200–210)

Sprint 1 deliverable was Allocator OUT block at rows 200-210 with 11 canonical labels + literal 0 placeholders on data rows. Sprint 3 overwrites the data rows (D:AC) with live formulas. Labels at column A unchanged (canonical per Architecture §4.2).

```
R200 (SECT header — unchanged): "CENTRAL ALLOCATOR OUTPUTS"
R201 (label unchanged: "Total Revenue ($mm)")
  D201 = =D83
  copyToRange source D201, destination E201:AC201

R202 (label unchanged: "Module EBITDA ($mm)")
  D202 = =D95
  copyToRange source D202, destination E202:AC202

R203 (label unchanged: "Module EBITDA Margin %")
  D203 = =D96   (IFERROR-wrapped in source)
  copyToRange source D203, destination E203:AC203

R204 (label unchanged: "Module FCF ($mm)")
  D204 = =D101
  copyToRange source D204, destination E204:AC204

R205 (label unchanged: "Module CapEx ($mm)")
  D205 = =D99
  copyToRange source D205, destination E205:AC205

R206 (label unchanged: "Capital deployed ($mm)")
  D206 = =D102
  copyToRange source D206, destination E206:AC206

R207 (label unchanged: "Spot IRR")
  D207 = =(D132 + D142) / 2
  Wait — Spot IRR on Allocator OUT should be a single module IRR. For Customer Launch with two vehicles (F9 + Starship), the "module Spot IRR" presented to Allocator should be the weighted blend.

Per Architecture §5.3: Customer Launch publishes one per-launch IRR at the module level. The two per-vehicle IRRs (F9 + Starship) are memo rows below the canonical 11. Customer Launch's canonical "Spot IRR" = weighted by external customer revenue share:

  D207 = =IFERROR((D132 * D33 + D142 * D48) / (D33 + D48), 0)
   (= revenue-weighted F9 Spot IRR + Starship Spot IRR; IFERROR for zero-revenue years)
  copyToRange source D207, destination E207:AC207

R208 (label unchanged: "Forward IRR (Y+2)")
  D208 = =IFERROR((D133 * F33 + D143 * F48) / (F33 + F48), 0)
   (= forward-revenue-weighted F9 + Starship Forward IRR)
  copyToRange source D208, destination E208:AC208

R209 (label unchanged: "Blended IRR")
  D209 = =(1 - INDEX(Assumptions!$B:$B, MATCH("Forward weight", Assumptions!$A:$A, 0))) * D207
        + INDEX(Assumptions!$B:$B, MATCH("Forward weight", Assumptions!$A:$A, 0)) * D208
  copyToRange source D209, destination E209:AC209

R210 (label unchanged: "Capacity Demand (kg-to-LEO)")
  D210 = =D24 * D21   (= Starship customer launches × per-launch upmass; F9 customer launches NOT in kg queue per Architecture §6.4)
  copyToRange source D210, destination E210:AC210
```

Sprint 1's exact row mapping is 200–210. Plugin confirms via label match (Rule 22) before overwrite.

Memo rows below R210 (Architecture §4.2 allows): F9 Spot/Forward/Blended IRR + Starship Spot/Forward/Blended IRR at memo rows R211–R216 (prefix `Memo:` per Rule 17, italic). These give Sprint 10 visibility into per-vehicle IRR signal if needed.

---

## §4 — Verification gate

### §4.1 Universal checks (per Sprint Roadmap §5)

1. **No formula errors workbook-wide.** Count `#REF!` / `#VALUE!` / `#DIV/0!` / `#NAME?` / `#NUM!` / `#NULL!` / `#N/A` across all tabs. Expected: ZERO (except inside IFERROR-wrapped IRR helper cells which are acceptable). Any error on a display row → halt.
2. **Conservation block ALL OK boolean.** Read Group P&L D108:AC108. Per Sprint 1 spec, the conservation block exists but evaluates to OK at trivial 0 = 0 level until Sprint 9 fires. Sprint 3 doesn't break the trivial-OK state.
3. **Edge-year reads.** §4.3 below lists D / I / S / AC reads.
4. **Round-trip stability.** Recalc workbook 5 times. No key cell moves >$1M (or >0.1% for IRR/% cells) across recalcs.
5. **Stale-ref scan.** §4.5 below.
6. **Sanity halt thresholds.** §4.4 below.
7. **Claude Log entry.** §5 template.

### §4.2 Sprint 3 calibration (Sprint Roadmap §6.2 — verbatim)

| Output | Read from | 2025 expected | Tolerance | Halt threshold |
|---|---|---|---|---|
| F9 customer launches | D25 (Customer Launch tab) | 38.58 | ±2 | <36.58 or >40.58 |
| F9 customer revenue | D33 (Customer Launch tab) | $4,290M | ±5% | <$3,800M or >$4,800M |
| F9 customer launch price | D17 (Customer Launch tab) | $111M | ±5% | <$95M or >$130M |
| Starship customer revenue | D48 (Customer Launch tab) | $0 | exact | any > $1M |
| Per-launch Blended IRR 2025 (F9 only, since Starship = 0) | D134 (Customer Launch tab) | range 8-25% per Sprint Roadmap §6.2 — but see §7 Open Thread for reconciliation; per-launch marginal IRR economics may produce >50% | per §6.2 lit-halt: <0% or >50% halt; if 8-25% literal target not hit Vlad reviews | <0% halt always; >50% reviewed |
| Customer Launch Module FCF 2025 | D101 (Customer Launch tab) | captured (no specific target — see §6.2; Module FCF = EBITDA + D&A − CapEx, pre-tax) | informational | n/a |

D182 calibration memo cell aggregates the above — read D182; if "PASS", §4.2 passes.

### §4.3 Edge-year read-back (D / I / S / AC)

Plugin reads these cells across columns D (2025), I (2030), S (2040), AC (2050) and reports actual vs expected. Tolerance ±5% on continuous values, exact on integer-count cells.

| Customer Launch row | Label | D (2025) | I (2030) | S (2040) | AC (2050) |
|---|---|---|---|---|---|
| 15 | Total customer launch market | 38.58 | 49.24 | 80.21 | 130.7 |
| 17 | F9 customer launch price | $111 | $95.4 | $70.7 | $52.4 |
| 18 | Starship customer launch price | $0 | $52.3 | $30.1 | $20.6 |
| 24 | Starship customer launches | 0 | varies (depends on Sprint 4/5 internal demand at 0 in Sprint 3) | varies | varies |
| 25 | F9 customer launches | 38.58 | residual ≈ 49.24 (Sprint 3 only; Sprint 4/5 will redistribute) | varies | varies |
| 33 | F9 customer revenue | $4,282M | varies | varies | varies |
| 48 | Starship customer revenue | $0 | depends | depends | depends |
| 70 | Customer Launch internal transfer revenue | $0 | $0 (Sprint 3 only) | $0 (Sprint 3 only) | $0 (Sprint 3 only) |
| 83 | Total Revenue | $4,282M | varies | varies | varies |
| 95 | Module EBITDA | varies | varies | varies | varies |
| 96 | Module EBITDA Margin % | varies (~95% — minimal COGS) | varies | varies | varies |
| 99 | Module CapEx | ~$21M (0.5% × $4,282M) | varies | varies | varies |
| 101 | Module FCF | EBITDA + D&A − CapEx | varies | varies | varies |
| 134 | F9 per-launch Blended IRR | very high (likely >100%; see §7 Open Thread) | similar | similar | similar |
| 144 | Starship per-launch Blended IRR | 0 (no commercial) | varies | varies | varies |
| 201 | Allocator OUT Total Revenue (= D83) | $4,282M | match | match | match |
| 209 | Allocator OUT Blended IRR | revenue-weighted IRR | varies | varies | varies |

Plugin reports actual vs expected for each cell. Variances >5% halt and push back.

Launch Capacity tab post-Patch-D + Patch-A/B + Patch-E §6.13 read-backs:

| Launch Capacity row | Label | D (2025) | I (2030) | S (2040) | AC (2050) |
|---|---|---|---|---|---|
| 24 | Booster fleet BoY | 0 | 0 | 0 | 0 |
| 27 | Booster fleet EoY | 0 | 0 | 0 | 0 |
| 28 | Cum upmass | 0 | 0 | 0 | 0 |
| 30 (NEW Patch E) | Cum stacks | 4 | 4 | 4 | 4 |
| 37 (Patch E) | Starship mfg cost | $90M | $90M | $90M | $90M |
| 38 (Patch E) | Starship ops+fuel+refurb | $12M | $12M | $12M | $12M |
| 39 (Patch E) | Starship D&A LEO | $12M | $3M | $1.92M | $1.74M |
| 40 (Patch E) | Starship at-cost LEO | $24M | $15M | $13.92M | $13.74M |
| 41 (NEW Patch E) | Starship at-cost Moon/Mars | $58.8M | $49.8M | $48.72M | $48.54M |
| 46 (Patch E step) | Variant mix % reusable | 0 | 1.0 | 1.0 | 1.0 |
| 62 (Patch A) | F9 retired | 6 (D unchanged) | drops as launches drop | drops | drops |
| 64 (Patch B) | F9 launches | 171 | demand-driven (depends on Sprint 4 V2 internal demand at 0 — F9 launches = F9 customer ≈ 49) | varies | varies |
| 71 (Patch D extended) | F9 at-cost | $17.75M | $17.75M | $17.75M | $17.75M |
| 77 | Blended $/kg | ~$778 | varies | varies | varies |

### §4.4 Sanity check halt thresholds (per Rule 15)

- F9 customer launches 2025 outside [36.58, 40.58] → halt.
- F9 customer revenue 2025 outside [$3,800M, $4,800M] → halt.
- F9 customer launch price 2025 outside [$95M, $130M] → halt.
- Starship customer revenue 2025 > $1M (should be exact $0) → halt.
- F9 per-launch Blended IRR 2025 < 0% → halt (negative IRR = no allocation per §5.4 → calibration failure).
- F9 per-launch Blended IRR 2025 > 50% → soft halt + Vlad review (target was 8-25% per §6.2; expected to fail with marginal per-launch economics — flag in Open Thread §7 for target reconciliation).
- Starship per-launch Blended IRR 2025 ≠ 0 → halt (Starship customer revenue = 0 in 2025 means IRR not defined; should evaluate to 0 via IFERROR).
- Any `#NUM!` / `#DIV/0!` / `#REF!` on Allocator OUT rows 201-210 → halt.
- Patch D verification: E71, I71, S71, AC71 ≠ $17.75M → halt (Fix A failed).
- Patch D verification: E24, I24, S24, AC24 ≠ 0 → halt (Fix B R24 propagation failed).
- Patch E §6.13 verification: D40 (Starship LEO at-cost 2025) outside [$22M, $26M] → halt.
- Patch E §6.13 verification: R34 still exists on Assumptions → halt (delete failed).

### §4.5 Stale-ref scan (per Rule 22)

After all writes, plugin verifies cross-tab references resolve correctly:

1. **Customer Launch reads from Launch Capacity (by label):**
   - D36 reads `F9 at-cost rate ($mm/launch)` — confirm Launch Capacity R71 column A = exact string.
   - D34 reads `F9 variable cost per launch ($mm)` — confirm Launch Capacity R69 column A.
   - D35 reads `F9 booster D&A share per launch ($mm)` — confirm Launch Capacity R70 column A.
   - D20 reads `Total Annual Capacity (kg-to-LEO)` — confirm Launch Capacity R34 column A.
   - D21 reads `Per-launch upmass (kg)` — confirm Launch Capacity R29 column A.
   - D140 reads `Starship manufacturing cost ($mm/stack, this year)` — confirm Launch Capacity R37 column A (Patch E §6.13 NEW label).
   - D87 + D141 read `Starship ops + fuel + refurb cost per launch ($mm, this year)` — confirm Launch Capacity R38 column A (Patch E §6.13 NEW label).
   - D88 reads `Starship D&A share per launch, fully reusable mode ($mm)` — confirm Launch Capacity R39 column A (Patch E §6.13 NEW label).
2. **Customer Launch reads from Assumptions (by label):** all 10+ INDEX/MATCH calls resolve. Specifically the new Sprint 3 amendments: `Total customer launch market (launches/yr) — 2025 anchor`, `Total customer launch market CAGR (% growth/yr)`, `Starship customer launch margin — 2027 anchor (multiplier on at-cost rate)`, `Starship customer launch margin — 2050 terminal (multiplier on at-cost rate, floor)`, `Starship customer launch margin — CAGR (% change/yr from 2027 anchor)`, `F9 retirement rate (% of launches/year)`, plus Patch E §6.13 inputs (mfg anchor, mfg WL rate, anchor cum units, ops anchor, ops WL rate, booster share, payload anchors).
3. **Launch Capacity reads from Customer Launch (Patch B):** R64 F-formula reads `F9 customer launches per year` from Customer Launch — confirm Customer Launch R25 column A label.
4. **Customer Launch Allocator OUT R201–R210 labels** match Architecture §4.2 verbatim (Sprint 1 wrote them; Sprint 3 doesn't modify).

Any label mismatch → halt + push back per Rule 22.

### §4.6 Don't-touch verification

Plugin confirms NO writes outside:
- Customer Launch tab rows 11-199 (module body) + 200-210 (OUT block data cells, labels unchanged)
- Launch Capacity tab rows 24, 27, 28, 30, 37-41, 62, 64, 71 (Patch D + A + B + E §6.13 formula amendments)
- Assumptions tab: row updates (R32, R33, R46) + row delete (R34) + row appends (10 new Patch E §6.13 + 5 new Sprint 3 + 1 new Patch A = 16 new rows)
- Claude Log tab: ONE new row appended

Plugin reads pre-flight cell counts of each tab, re-reads post-execution; any tab other than Customer Launch + Launch Capacity + Assumptions + Claude Log showing a delta = halt + push back.

---

## §5 — Claude Log entry template

Plugin appends one row to the Claude Log tab on the workbook:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-MM-DD | 3 | Customer Launch (full module body), Launch Capacity (Patches D + A + B + E §6.13 amendments), Assumptions (R32/R33 updates, R34 delete, R46 step function, 16 new rows total), Claude Log (append) | Built Customer Launch module body end-to-end: demand mechanic (total market year-row anchored 38.58 in 2025 + 5%/yr CAGR; F9 vs Starship split IRR + capacity gated per Vlad lock #1), F9 economics (price $111M, revenue $4,282M ✓ matches Q4'25 $4,290M anchor), Starship economics (price = at-cost × margin year-row 4.0x in 2027 → 1.5x terminal per Vlad lock #2; price $0 in 2025-2026, $78M in 2027), internal transfer revenue mechanism (resolves to 0 via IFERROR-0 wrappers until Sprint 4/5/6 fire), P&L vending-machine framing (Revenue → COGS → Gross Profit = Module EBITDA → CapEx → FCF — no R&D/SG&A/overhead/taxes), per-launch IRR engines (N = lifetime reuses clamped at R23 = 10 per Vlad lock #4; F9 N=10 constant, Starship N year-row 5→10), Allocator OUT contract live (revenue-weighted Spot/Forward/Blended IRR + Capacity Demand kg). Patch D extensions PASS (R71 + R24/R27/R28 to E:AC). Patch A F9 retirement engine PASS (launch-driven, Q4'25 mirror $B$30 = 0.01). Patch B F9 demand-driven wiring PASS (R64 reads Customer Launch + Starlink IFERROR-0). Patch E §6.13 Starship cost overhaul PASS (split-cost-curve canonical formulation: manufacturing + ops+fuel+refurb separate WL curves, R34 deleted from Assumptions, 10 new cost+payload rows + Mach33 $54M/$36M booster/ship update, R46 step function at 2027). 2025 calibration: F9 customer launches 38.58 ✓, F9 customer revenue $4,282M ✓, F9 price $111M ✓, Starship customer revenue $0 ✓. | (a) F9 per-launch Blended IRR likely >100% due to marginal per-launch economics ($111M revenue / $17.75M at-cost). Sprint Roadmap §6.2 target 8-25% likely V30.5 holdover from fleet-level MFW-IRR — needs reconciliation: either amend target to "marginal per-launch IRR magnitude expected high; halt only if <0% or unbounded" OR change IRR formula to deduct corporate overhead per launch (which violates vending-machine framing). Plugin flagged for spec author + Vlad review. (b) Sprint 0 R64 (`Starship customer launch price year-row`) DEPRECATED per Vlad lock #2 but cell formulas retained for memo (Principle 7 no renames). Clean cell-clear can happen in Sprint 9 audit if desired. (c) Customer Launch insurance % / other COGS % / ground equipment CapEx % / ground ops % rows not in Sprint 0 R234-R236 scope. Spec used IFERROR-0.01/0.005 fallbacks. Sprint 8 should add proper Assumptions rows with MC ranges. (d) Sprint Roadmap §6.1 Starship 2025 capacity target "~450K kg" mismatch with actual 0 (Sprint 10 vehicle build claim writes R25) — already documented in Sprint 2 §7 item 3; Sprint 10 owns reconciliation. (e) Sprint 4 V2 BB / V2 DTC internal launch labels and Sprint 5 ODC kg demand labels expected: `F9 V2 BB launches (internal)`, `F9 V2 DTC launches (internal)`, `Starship V3 BB launches (internal)`, `Starship V3 DTC launches (internal)`, `V3 BB Starship kg demand`, `V3 DTC Starship kg demand`, `ODC Starship kg demand`, `ODC Starship launches (internal)`. Sprint 4/5 spec authors confirm exact strings against Sprint 3 IFERROR wrappers. | Sprint 4 — Starlink module + Starlink Capacity tab |

---

## §6 — Don't touch (out of scope)

Sprint 3 writes ONLY to:
- Customer Launch tab rows 11-199 (module body) + 200-210 OUT block data cells (labels unchanged from Sprint 1)
- Launch Capacity tab Patch D + A + B + E §6.13 amendments (R24, R27, R28, R30, R37-R41, R62, R64, R71 — formula replacements at existing row positions OR new content at previously-blank rows)
- Assumptions tab: R32/R33 value updates, R34 single-row DELETE, R46 step function year values, 16 new rows appended below existing §3 + §4 last-used rows
- Claude Log tab (one new row appended)

Sprint 3 does NOT touch:
- Allocator tab (Sprint 10 owns the brain light-up)
- Starlink / Starlink Capacity / ODC / AI Stack / Lunar Mars / OpEx / CapEx / Valuation / Group P&L / Demand Curves tabs (those sprints fire separately)
- Sprint 0 R64 cell formulas (DEPRECATED but retained per Principle 7 — no renames; cell formulas left as Sprint 0 values for memo purposes; Customer Launch ignores R64 entirely)
- Any save / save-as / file-write operation (Vlad handles all saves per standing process rule 2)
- Any row insertion (Rule 10) — only appends, single R34 delete, in-place formula replacements

If the plugin discovers a need to write outside the above scope, HALT per Rule 9 and push back to spec author.

---

## §7 — Open thread (post-Sprint 3 considerations)

These are flagged for spec author attention but do not block Sprint 3 PASS:

1. **Per-launch IRR magnitude vs §6.2 target 8-25%.** F9 per-launch Blended IRR with marginal economics likely lands >100% (revenue $111M / at-cost $17.75M margin × 12 cadence × 10 yr N produces enormous IRR). Sprint Roadmap §6.2 target 8-25% is a holdover from V30.5 fleet-level MFW-IRR with corporate overhead deducted. Architecture §5 explicitly mandates per-launch marginal IRR with no corporate overhead. The two are incompatible. Recommend: amend Sprint Roadmap §6.2 Sprint 3 target to "Per-launch Blended IRR 2025: large positive (typically 50-300%); halt only if <0%". OR change Customer Launch IRR formula to subtract a corporate-overhead-per-launch placeholder, which would violate vending-machine framing. Vlad decides which after seeing actual numbers.

2. **Sprint 0 R64 deprecation cleanup.** R64 `Starship customer launch price ($mm/launch) — year-row` retained per Principle 7 (no renames mid-build) but Customer Launch ignores it entirely (price = at-cost × margin per Vlad lock #2). Future Sprint 9 audit can either: (a) clear R64 formulas leaving empty year-row with deprecation note, or (b) repoint R64 to read from Customer Launch's computed price row 18 (=Customer_Launch!D18 etc) for backward-compat with any external doc references. Defer to Sprint 9 audit.

3. **Customer Launch tab missing % rates on Assumptions.** Sprint 0 has Module-specific COGS % rates for Starlink (insurance %, other %) but not for Customer Launch. Sprint 3 used IFERROR fallbacks (0.01 insurance + 0.01 other + 0.005 ground equip CapEx + 0.01 ground ops). Sprint 8 OpEx + CapEx spec should add proper rows: `Customer Launch ground ops % of revenue`, `Customer Launch insurance % of revenue`, `Customer Launch other COGS % of revenue`, `Customer Launch ground equipment CapEx % of revenue`. Each MC-variable per Principle 18.

4. **Sprint Roadmap §6.1 Starship 2025 capacity ~450K target reconciliation.** Inherited from Sprint 2 §7 item 3. Starship boosters built = 0 in Sprint 3 (Sprint 10 vehicle build claim writes R25 endogenously). Sprint 10 owns the reconciliation. Sprint 3 doesn't surface new info.

5. **Sprint 4/5 internal-demand canonical labels.** Sprint 3 publishes Customer Launch labels: `F9 customer launches per year`, `Starship customer launches per year`, `Customer Launch internal transfer revenue ($mm)`. Sprint 4 expected to publish: `F9 V2 BB launches (internal)`, `F9 V2 DTC launches (internal)`, `Starship V3 BB launches (internal)`, `Starship V3 DTC launches (internal)`, `V3 BB Starship kg demand`, `V3 DTC Starship kg demand`. Sprint 5 expected to publish: `ODC Starship launches (internal)`, `ODC Starship kg demand`. Sprint 6 AI Stack: kg demand = 0 (terrestrial). Sprint 4/5 spec authors confirm exact strings against Sprint 3 IFERROR wrappers before plugin fires.

6. **Patch C SUPERSEDED but Sprint 2 §7 item 1 still references it.** Patch C added a standalone Starship per-launch ops cost row to Assumptions; Patch E §6.13 absorbed it into the ops+fuel+refurb anchor ($12M). Patch C explicitly NOT executed in Sprint 3. Sprint 4 + Sprint 5 + Sprint 10 spec authors aware: Starship per-launch ops cost is now Patch E §6.13's R38 ops+fuel+refurb cost per launch, read by INDEX/MATCH from Launch Capacity.

7. **F9 lifetime reuses inputs reconciliation.** Sprint 0 R50 = 50 (technical ceiling). Patch A introduces R64 retirement rate = 0.01/launch (= 100-launch fleet-average lifetime). Both inputs coexist — R50 for D&A amortization (cost-side), R64 retirement rate for fleet evolution (volume-side). Documented in Patch A §2.4 (kept for clarity).

8. **Customer Launch ground ops + insurance + other COGS rates.** Used 0.01/0.01/0.01 IFERROR fallbacks. Approximate Sprint 0 placeholders. Sprint 8 needs to lock these with MC ranges.

9. **Customer Launch ground equipment CapEx.** Used 0.005 (0.5%) IFERROR fallback. Sprint 8 / Sprint 11 may need to anchor this to a Mach33 estimate (e.g. Cape Canaveral + Boca Chica ground systems CapEx).

10. **Forward IRR cashflow stream shift implementation.** Architecture §5.1 says Forward IRR = IRR(CF stream evaluated at year T+2). Spec implemented as `=IFERROR(IRR(IF(_xlfn.SEQUENCE(1, $D$119+1)=1, -$D$130, F131)), -1)` for D-column Forward IRR — uses F131 (2027 cashflow) as the t=1 entry. For E-column Forward IRR (2026), uses G131 (2028). This is the relative-reference shift Architecture §5.1 implies. Plugin verifies the F131 vs G131 vs H131 shift works correctly under copyToRange.

---

## §8 — Execution sequence (plugin order of operations)

Plugin executes in this fixed order. Each block is one or more discrete tool calls per Rule 1.

1. **Pre-flight (§3.0)** — verify all 11 checks. Halt on any failure.
2. **Patch D Fix A (§3.2.1)** — copyToRange D71 → E71:AC71 on Launch Capacity. Verify E71, I71, S71, AC71 = $17.75M.
3. **Patch D Fix B (§3.2.2)** — 3 plugin operations for R24, R27, R28 E:AC extensions. Verify E24, I24, S24, AC24 = 0; same for R27, R28.
4. **Patch A + Sprint 3 Assumptions amendments (§3.3.1 + §3.3.7)** — append F9 retirement rate row + Customer Launch market year-row + margin year-row inputs to Assumptions. Each row: 6 discrete writes (label, value, MC Min, MC Max, MC Dist, Notes).
5. **Patch E §6.13 Assumptions amendments (§3.3.2–§3.3.6)** —
   - First: DELETE R34 (`Ship refurb % of manufacturing`) — single delete operation.
   - Then: update R32 ($54M) + R33 ($36M) + R46 step function — value writes.
   - Then: append 6 cost stack rows + 4 payload rows — 10 new rows × 6 writes each = 60 writes.
6. **Patch A Launch Capacity R62 formula (§3.4.1)** — write E62 + copyToRange F62:AC62.
7. **Patch B Launch Capacity R64 formula (§3.4.2)** — write F64 + copyToRange G64:AC64.
8. **Patch E §6.13 Launch Capacity formulas (§3.5)** —
   - R30 cum stacks: A30 label + D30 anchor + E30 year-chained + copyToRange F30:AC30.
   - R37 mfg cost: A37 label + D37 formula + copyToRange E37:AC37.
   - R38 ops+fuel+refurb: A38 label + D38 formula + copyToRange E38:AC38.
   - R39 D&A LEO: A39 label + D39 formula + copyToRange E39:AC39.
   - R40 at-cost LEO: D40 formula REPLACED (label unchanged) + copyToRange E40:AC40.
   - R41 at-cost Moon/Mars memo: A41 label + D41 formula + copyToRange E41:AC41.
9. **VERIFICATION GATE 1 — Launch Capacity post-patches** — read D40 (= $24.0M ±5%), D41 (= $58.8M ±5%), I40, S40, AC40, I41, S41, AC41, E71 (= $17.75M), I71, S71, AC71, D62 (= 6), E62 (launch-driven retirement), D64 (= 171), E64 (= 171), F64 (demand-driven; F64 = MIN(fleet × cadence, IFERROR_0 + Customer Launch F25 once §3.6.1 fires)). Halt on variance.
10. **Customer Launch tab section + subsection headers (§3.6.0)** — 7 SECT/SUB writes.
11. **Customer Launch demand mechanic (§3.6.1)** — rows 15-25. Write Total customer market (R15), Starship margin (R16), F9 price R17 (read from Sprint 0 R63), Starship price R18 (= at-cost × margin), Starship capacity R20-R23, then per-vehicle launch rows R24-R25 — but R24 and R25 reference IRR rows 134, 144 which are written in step 13. So:
    - First pass: write R15-R23 + R25 with `D25 = 38.58` hardcoded + `E25 = D25 × (1+CAGR)` + `F25:AC25` with placeholder formula that's a copy of E25 logic (i.e. residual market without IRR gate, since IRR rows not yet live).
    - Same for R24: write D24 = 0, E24 = 0, F24:AC24 with placeholder formula treating Starship IRR as positive (since IRR rows not yet live).
    - Then return after step 13 IRR engine fires to repoint F25 + F24 to the IRR-gated formulas.
12. **Customer Launch F9 + Starship cost/revenue rows (§3.6.2 + §3.6.3)** — rows 33-37 (F9) + rows 48-52 (Starship). All read Launch Capacity by label.
13. **Customer Launch internal transfer revenue (§3.6.4)** — rows 68-70. All resolve to 0 via IFERROR-0 wrappers in Sprint 3 (Sprint 4/5/6 not yet fired).
14. **Customer Launch P&L (§3.6.5)** — rows 83-102. Revenue → COGS → EBITDA → CapEx → FCF.
15. **Customer Launch per-launch IRR engine (§3.6.6 / §3.7)** — rows 118-144. N derivation (R118-R121), F9 cost slug + annual margin + Spot/Forward/Blended (R130-R134), Starship same (R140-R144).
16. **Return to §3.6.1 R24 + R25 IRR-gated formulas** — repoint F24 + F25 to reference IRR rows 134 + 144 + capacity row 23. After this, R24/R25 final.
17. **Customer Launch memo rows (§3.6.7)** — rows 178-182. Calibration PASS/CHECK indicator.
18. **VERIFICATION GATE 2 — Customer Launch module body** — read D25 (= 38.58), D33 (= $4,282M, ±5% of $4,290M target), D17 (= $111M), D48 (= $0), D95 (Module EBITDA), D101 (Module FCF), D99 (Module CapEx), D102 (Capital deployed = D99), D134 (F9 Blended IRR — flagged for §7 reconciliation), D144 (Starship Blended IRR = 0). Halt on variance.
19. **Allocator OUT contract overwrite (§3.8)** — rows 201-210 data cell formulas overwrite Sprint 1 literal 0s. Labels unchanged.
20. **VERIFICATION GATE 3 — Allocator OUT** — read R201 = D83, R202 = D95, R204 = D101, R205 = D99, R206 = D102, R207 = revenue-weighted Spot IRR, R208 = Forward IRR, R209 = Blended IRR, R210 = Capacity Demand (= D24 × D21 = 0 in 2025). Confirm against module body values.
21. **§4.1 universal checks** — workbook-wide error scan (zero `#REF!` etc), conservation block (still trivially OK at Sprint 3 stage; Sprint 9 owns full conservation), edge-year read-back per §4.3, stale-ref scan per §4.5, round-trip stability test (5x recalc, no value moves >$1M).
22. **§4.6 don't-touch verification** — confirm no writes outside Customer Launch + Launch Capacity + Assumptions + Claude Log.
23. **§5 Claude Log entry** — append one row.
24. **Sprint 3 complete declaration** — push back to spec author with all read-back values + PASS status.

---

## §9 — Amendment log

- **2026-05-20 (initial draft)** — Sprint 3 spec drafted as Vlad's kickoff prompt directed. Four load-bearing methodology choices locked via spec author chat with Vlad: (1) F9 vs Starship customer launch split = IRR + capacity gated (replaces my recommendation of hardcoded share %); (2) Starship customer launch price = at-cost × margin year-row (replaces Sprint 0 R64 fixed price; R64 deprecated to memo); (3) Starship customer launches mechanic = MIN(market demand, unused capacity post-Starlink+ODC), IFERROR-0 wrappers; (4) IRR cashflow stream lifetime N = lifetime reuses clamped at R23 = 10 (improves over time as R21 ramps for Starship). Spec mirrors Sprint 0 / 1 / 2 structure: §1 Rule Compliance Preamble + Architecture compliance + Patch absorption attestation fully ticked. §3 lays out cell-by-cell build with full Excel formulas inlined. §4 verification gate per Sprint Roadmap §5 + §6.2. §7 Open Thread surfaces 10 items including the IRR magnitude vs §6.2 target reconciliation. Patches D + A + B + E §6.13 fully absorbed per execution sequence §8 (D first, A + B Assumptions + LC, E §6.13 last). Patch C explicitly SUPERSEDED — not implemented. Plugin operates on V2.5 live session; Vlad handles all saves per standing process rule 2.
