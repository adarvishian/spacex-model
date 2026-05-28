# Sprint 1 — Allocator Skeleton + Module Shells

**Sprint type**: Structural. Lays the cross-tab wiring contract before any module body fills.
**Execution context**: Excel Claude plugin chat, operating on an already-open Excel workbook that Vlad has pre-named via Save-As from the Sprint 0 output. Source is V2.1.xlsx (Sprint 0 baseline). Target is V2.2.xlsx.
**Target workbook**: `SpaceX Model V2.2.xlsx` (Vlad pre-named via Save-As from V2.1).
**Day budget**: 1 day.

**This spec is fully self-contained.** It references no external XLSX, no constitutional MDs, no other files. Every label, every formula, every cell write, every verification anchor lives in this document. The plugin executes against the spec alone.

**The plugin does NOT save the workbook.** Vlad handles all saving (initial Save-As of V2.1 → V2.2 pre-execution; intermediate + final saves during/after execution). The plugin executes cell writes against the live workbook session.

The plugin's first cell-write does NOT happen until (a) the Rule Compliance Preamble in §1 is confirmed box-by-box, (b) the Vlad-side pre-execution setup in §1.5 is complete, (c) the pre-flight checks in §3.0 pass.

---

## §1 — Rule Compliance Preamble (mandatory)

- [x] **Rule 1** (one concept per write) — Section structure separates: Allocator section headers, Allocator canonical allocation labels, module IN-block labels, module IN-block formulas (one row at a time per module), module OUT-block labels, module OUT-block 0 placeholders, Group P&L conservation labels, Group P&L conservation formulas, non-module tab title rows, and formatting. Each is a discrete write block per §3 and §8.
- [x] **Rule 3 / 23** (formula pattern) — Sprint 1 writes only one class of formula: `=INDEX(Allocator!D:D, MATCH("<canonical label>", Allocator!$A:$A, 0))` in module IN blocks (D column anchor, copy across E:AC — Excel shifts `D:D` → `E:E` → ... correctly because the column reference is relative). And `=IF(AND(ABS(D99)<1,...,ABS(D107)<1),"OK","CHECK")` on Group P&L R108 (per-column, copy across). No anchor-and-offset CAGR ramps in this sprint. No `OFFSET()` anywhere.
- [x] **Rule 4** (verification gate) — §4 specifies read-back cells + expected values for every section. Edge years D (2025), I (2030), S (2040), AC (2050) covered on every IN-block, OUT-block, and conservation read.
- [x] **Rule 6** (inline formulas) — Every cell write specified with full Excel formula or literal value in §3.2–§3.6 below.
- [x] **Rule 10** (no row insertions) — All Sprint 1 writes append into pre-staged blank rows on tabs that already exist (created Sprint 0). No `insert_row` operations anywhere.
- [x] **Rule 11** (touch points) — Sprint 1 introduces the Allocator IN/OUT contract. Touch points: (a) each module IN block reads from Allocator's canonical allocation rows via label; (b) Allocator's canonical allocation rows are placeholders that Sprint 10 populates; (c) module OUT blocks are placeholders that module-body sprints (Sprint 3–7) populate; (d) Group P&L R108 reads R99–R107. No SUM ranges to expand this sprint.
- [x] **Rule 12** (label-based cross-tab refs) — Every IN-block formula uses `INDEX(Allocator!D:D, MATCH("<label>", Allocator!$A:$A, 0))` per Architecture §4.1. Zero hardcoded `=Allocator!Dxx` row references.
- [x] **Rule 13** (vending-machine test) — N/A this sprint (no module body content). The OUT-block contract enforces vending-machine framing structurally: one canonical `Module EBITDA ($mm)` row (not "True EBITDA" / "after-overhead" variants).
- [x] **Rule 14** (no hardcoded constants in formulas) — Sprint 1 has no behavioural constants in formulas. The Blended IRR weight `Assumptions!Forward_weight` (B17 = 0.7) is not used this sprint (OUT-block IRR rows are 0 placeholders, not the Blended formula — that lands Sprint 3–7 per module).
- [x] **Rule 15** (sanity check halt thresholds) — §4.3 halt conditions explicit and quantitative (every IN-block cell = 0; every OUT-block cell = 0; R108 = "OK" every year; zero error values).
- [x] **Rule 19** (save-as) — Source `SpaceX Model V2.1.xlsx`, target `SpaceX Model V2.2.xlsx`. **Vlad performs all saves**: Vlad opens V2.1, Save-As → V2.2, then sends the kickoff prompt. Plugin verifies target filename in §3.0 pre-flight check #1.
- [x] **Rule 22** (stale-ref scan) — Sprint 1's only cross-tab refs are the module IN-block INDEX/MATCH formulas. §4.2 anchor read-back verifies each resolves to 0 (the placeholder value Sprint 1 writes into the matching Allocator canonical allocation rows). If any IN-block returns `#N/A`, the label-vs-source contract is broken → halt.

Architecture compliance (load-bearing items this sprint touches):
- [x] Module P&L vending-machine framing — enforced structurally via OUT-block contract (single `Module EBITDA ($mm)` row; no R&D/SG&A/overhead/tax rows).
- [x] Per-sat / per-launch marginal IRR engine — N/A directly; OUT-block reserves rows 207 (Spot IRR), 208 (Forward IRR Y+2), 209 (Blended IRR) for module-body sprints to fill.
- [x] Allocator OUT contract — canonical 11 rows written this sprint per Architecture §4.2 (header + 10 data rows). Lunar Mars gets the 11 + 2 extra BV memo rows.
- [x] Year-offset helper row + year header — Sprint 0 placed these on every active tab (D=2025, AC=2050 at row 4; D=0, AC=25 at row 5). Sprint 1 inherits.
- [x] ZERO `OFFSET()` formulas — Standing principle re-asserted; none introduced this sprint.

All boxes ticked or marked N/A with justification. **If any box is unchecked, plugin halts and pushes back.** Otherwise proceed.

---

## §1.5 — Pre-execution setup (Vlad-side, before plugin chat starts)

Sprint 1 continues from the Sprint 0 baseline. Vlad addresses capability constraints outside the plugin chat:

### §1.5.1 — Save-as from V2.1 → V2.2 (plugin cannot save-as)

1. Open `SpaceX Model V2.1.xlsx` (Sprint 0 output, saved by Vlad after Sprint 0 verification PASS).
2. `File → Save As` → name it `SpaceX Model V2.2.xlsx`.
3. The workbook now has all 14 tabs from Sprint 0 with their content intact (Assumptions populated, row 4 + row 5 standards on every year-column tab, Claude Log header + Sprint 0 entry).
4. Leave the workbook open in Excel; the plugin operates on it.

### §1.5.2 — Saving during + after execution

The plugin does not issue save commands. Vlad saves:
- After the plugin reports verification PASS (recommended: save to lock the Sprint 1 baseline).
- Whenever convenient mid-execution.

### §1.5.3 — Send the kickoff prompt with setup confirmation

Append this confirmation block to the kickoff prompt:

```
Pre-execution setup confirmed (per Sprint_1_Spec.md §1.5):
- Source workbook: SpaceX Model V2.1.xlsx (Sprint 0 output, verified PASS).
- Target workbook saved-as: `SpaceX Model V2.2.xlsx`, open in Excel plugin.
- I (Vlad) handle all saving; plugin must not issue save commands.
```

Plugin reads this confirmation as part of its §3.0 pre-flight.

---

## §2 — Framing

**Why this sprint.** Build the cross-tab wiring contract before any module body fills. By the end of Sprint 1, every module tab knows where to look for its cash and kg allocations (Allocator canonical rows, resolved by label), every module exposes the 11 canonical OUT rows that downstream consumers will read by label, and Group P&L's conservation block is in place — all reading 0 trivially because every input is a 0 placeholder. Sprint 2 onwards fills the module bodies into the 190 rows between the IN block (rows 7–10) and the OUT block (row 200+); Sprint 10 fills the Allocator computation rows that drive the canonical allocation labels; Sprint 9 swaps the conservation block's 0 placeholders for live INDEX/MATCH formulas.

**What this sprint produces.**
1. Allocator tab populated with section headers + the 10 canonical allocation rows (5 cash, 5 kg) + reserved blank rows for Sprint 10's computation logic. All allocation row values D:AC = literal 0.
2. Five module tabs (Customer Launch, Starlink, ODC, AI Stack, Lunar Mars) with IN block at rows 7–10 (label + live `INDEX/MATCH` formula resolving against Allocator) and OUT block at rows 200–210 (11 canonical rows: 1 header + 10 data rows, all data row D:AC = literal 0). Lunar Mars extends to rows 211–212 with two BV memo rows.
3. Non-P&L tabs (Launch Capacity, Starlink Capacity, OpEx, CapEx, Valuation) — title row only at row 6 (single label, column A, bold, for visual orientation). No IN/OUT contract on these tabs (they are not P&L modules per Architecture §1 and §3).
4. Group P&L conservation block at rows 99–109 — labels in column A, D:AC = literal 0 on R99–R107 and R109, formula on R108 (`=IF(AND(ABS(D99)<1,...,ABS(D107)<1),"OK","CHECK")`). Trivially reads "OK" every year because all upstream cells = 0.
5. Claude Log row 3 appended with Sprint 1 entry.

**What this sprint does NOT produce.**
- Any module body content (revenue, COGS, CapEx, IRR engines, etc.) — that's Sprint 3–7.
- Any Allocator computation logic (Cash BoY, queue gate, sigmoid blends, vehicle build claim) — that's Sprint 10.
- Any Group P&L walk above row 99 (Revenue → EBITDA → D&A → EBIT → Taxes → NOPAT → FCF) — that's Sprint 9.
- Any OpEx / CapEx tab content — that's Sprint 8.
- Any Valuation tab content — that's Sprint 11.
- Any internal-transfer flows (launch services, bandwidth, internal compute) — those land in the module-body sprints + Sprint 9 elimination block.
- Plugin-issued saves.

---

## §3 — Scope

### §3.0 — Pre-flight checks (plugin runs BEFORE any cell writes)

1. **Confirm target workbook is open and named correctly**: the open workbook's filename matches `SpaceX Model V2.2.xlsx`. If different → halt, push back to Vlad to complete §1.5.1.
2. **Confirm Sprint 0 baseline is intact**:
   - Workbook has exactly 14 tabs in this order: `Assumptions`, `Allocator`, `Launch Capacity`, `Customer Launch`, `Starlink`, `Starlink Capacity`, `ODC`, `AI Stack`, `Lunar Mars`, `Group P&L`, `OpEx`, `CapEx`, `Valuation`, `Claude Log`. If any tab missing, misordered, or misnamed → halt, push back.
   - On each of tabs 1–13: row 4 has hardcoded integer year header (D4=2025, AC4=2050) and row 5 has hardcoded integer year-offset (D5=0, AC5=25). If any deviation → halt.
   - Assumptions tab has populated rows R2 through R301 with content per Sprint 0 §3.6. Spot-check anchor `Starting cash position EoY 2024 ($mm)` = 5000 (column B). If missing or wrong → halt, push back (Sprint 0 has not actually completed).
   - Claude Log row 2 has Sprint 0 entry (Date column A2 = `2026-05-20`, Sprint column B2 = `0`). If missing → halt.
3. **Confirm the Assumptions tab cells the Sprint 1 contract references later still hold their Sprint 0 values**:
   - `Forward IRR weight w` at B17 = 0.7 (used by future module-body sprints; Sprint 1 doesn't reference but verifies).
   - `Sigmoid IRR-blend exponent k` at B16 = 2 (same).
   If different → halt (suggests Sprint 0 didn't land cleanly).
4. **Confirm kickoff prompt contained the §1.5.3 setup confirmation block** — Vlad has acknowledged "I handle all saving; plugin must not issue save commands." If missing → halt, ask Vlad to re-send kickoff with confirmation.

### §3.1 — Workbook layout (no new tabs, no renames)

Sprint 1 introduces no new tabs and renames none. All work happens on tabs already created in Sprint 0:

- Allocator (skeleton built this sprint)
- Customer Launch, Starlink, ODC, AI Stack, Lunar Mars (module shells built this sprint)
- Launch Capacity, Starlink Capacity, OpEx, CapEx, Valuation (title row only this sprint)
- Group P&L (conservation block built this sprint; P&L walk above remains blank for Sprint 9)
- Assumptions, Claude Log — untouched except for Claude Log row 3 append per §5

### §3.2 — Allocator tab build

The Allocator tab is structurally divided into nine sections. Sprint 1 writes section headers + the 10 canonical module-allocation rows. Sprint 10 will populate the reserved blank rows between sections with the computation logic (Cash BoY tracker, queue gate, sigmoid blends, vehicle build claim, central IRR display).

**Row layout** (column A labels; values per §3.2.2):

| Row | Type | Column A label | Notes |
|---|---|---|---|
| 4 | (Sprint 0) | year header | D4=2025, AC4=2050 |
| 5 | (Sprint 0) | year-offset | D5=0, AC5=25 |
| 6 | (blank) | — | visual gap |
| 7 | SECT | `§1 CASH POOL TRACKER` | section header — Sprint 10 fills rows 8–15 |
| 8 | (reserved) | — | blank — Sprint 10 |
| 9 | (reserved) | — | blank — Sprint 10 |
| 10 | (reserved) | — | blank — Sprint 10 |
| 11 | (reserved) | — | blank — Sprint 10 |
| 12 | (reserved) | — | blank — Sprint 10 |
| 13 | (reserved) | — | blank — Sprint 10 |
| 14 | (reserved) | — | blank — Sprint 10 |
| 15 | (reserved) | — | blank — Sprint 10 |
| 16 | (blank) | — | visual gap |
| 17 | SECT | `§2 QUEUE GATE` | section header — Sprint 10 fills rows 18–29 |
| 18–29 | (reserved) | — | blank — Sprint 10 (OpEx claim, Corp CapEx claim, Spectrum claim, Taxes claim, Mars carve-out claim, Vehicle build claim, Total non-module claims, Available cash for IRR queue) |
| 30 | (blank) | — | visual gap |
| 31 | SECT | `§3 MARS/MOON STRATEGIC CARVE-OUT` | section header — Sprint 7/10 fills rows 32–37 |
| 32–37 | (reserved) | — | blank — Sprint 7/10 (Mars %, floor, Lunar share, Mars share, total carve-out) |
| 38 | (blank) | — | visual gap |
| 39 | SECT | `§4 CASH IRR-PRIORITY SIGMOID QUEUE` | section header — Sprint 10 fills rows 40–80 |
| 40–80 | (reserved) | — | blank — Sprint 10 (per-module sub-blocks: Blended IRR, cash demand, masked demand, weight, share) |
| 81 | (blank) | — | visual gap |
| 82 | SECT | `§5 MODULE CASH ALLOCATIONS (canonical labels — read by module IN blocks)` | section header |
| 83 | VAL | `Customer Launch cash allocation` | D:AC = literal 0 |
| 84 | VAL | `Starlink cash allocation` | D:AC = literal 0 |
| 85 | VAL | `ODC cash allocation` | D:AC = literal 0 |
| 86 | VAL | `AI Stack cash allocation` | D:AC = literal 0 |
| 87 | VAL | `Lunar Mars cash allocation` | D:AC = literal 0 |
| 88 | (blank) | — | visual gap |
| 89 | SECT | `§6 KG IRR-PRIORITY SIGMOID QUEUE` | section header — Sprint 10 fills rows 90–130 |
| 90–130 | (reserved) | — | blank — Sprint 10 (Total Starship capacity, Lunar Mars reserved, Capacity available, per-module sub-blocks) |
| 131 | (blank) | — | visual gap |
| 132 | SECT | `§7 MODULE KG ALLOCATIONS (canonical labels — read by module IN blocks)` | section header |
| 133 | VAL | `Customer Launch kg allocation` | D:AC = literal 0 |
| 134 | VAL | `Starlink kg allocation` | D:AC = literal 0 |
| 135 | VAL | `ODC kg allocation` | D:AC = literal 0 |
| 136 | VAL | `AI Stack kg allocation` | D:AC = literal 0 (always 0 — terrestrial per Architecture §10.4) |
| 137 | VAL | `Lunar Mars kg allocation` | D:AC = literal 0 |
| 138 | (blank) | — | visual gap |
| 139 | SECT | `§8 VEHICLE BUILD CLAIM` | section header — Sprint 10 fills rows 140–150 |
| 140–150 | (reserved) | — | blank — Sprint 10 (Forward aggregate kg demand, Projected capacity T+2, Capacity gap, Required vehicles, Vehicle build claim $mm) |
| 151 | (blank) | — | visual gap |
| 152 | SECT | `§9 CENTRAL IRR DISPLAY` | section header — Sprint 10 fills rows 153–165 |
| 153–165 | (reserved) | — | blank — Sprint 10 (per-module Blended IRR memo + group allocation totals sanity rows) |

#### §3.2.1 — Allocator section headers (10 SECT rows)

Plugin writes column A only for rows 7, 17, 31, 39, 82, 89, 132, 139, 152 (the nine section headers above). Format: white-on-charcoal fill (RGB 51,51,51 / white text), bold, font-size 11. Apply to A:AC of the header row (single-row fill across the year columns for visual continuity). Cells B:AC of the header rows hold no values.

**Write structure (Rule 1)**: one tool call per section header. Do NOT write all 9 headers in one bulk operation — the formatting + label combination must land cleanly per row.

#### §3.2.2 — Allocator canonical allocation rows (10 VAL rows)

Plugin writes the 10 canonical allocation rows: 5 cash (rows 83–87) + 5 kg (rows 133–137). Each row gets:

- **Column A label** (exact, case-sensitive — these are the contract):
  - Row 83: `Customer Launch cash allocation`
  - Row 84: `Starlink cash allocation`
  - Row 85: `ODC cash allocation`
  - Row 86: `AI Stack cash allocation`
  - Row 87: `Lunar Mars cash allocation`
  - Row 133: `Customer Launch kg allocation`
  - Row 134: `Starlink kg allocation`
  - Row 135: `ODC kg allocation`
  - Row 136: `AI Stack kg allocation`
  - Row 137: `Lunar Mars kg allocation`
- **Columns D through AC**: literal integer 0 (not a formula; not text "0"; a numeric zero). 26 cells per row × 10 rows = 260 cells.
- **Column C note** (one-liner for human reader):
  - Cash rows (83–87): `Sprint 10 populates from sigmoid blend (§4). Sprint 1 = 0 placeholder.`
  - Kg rows (133–137): `Sprint 10 populates from kg sigmoid blend (§6). Sprint 1 = 0 placeholder.`
  - Row 136 specifically: `AI Stack consumes no Starship kg (terrestrial per Architecture §10.4). Locked at 0 across the horizon.`

**Write structure (Rule 1)**: write column A labels for all 10 rows in one block (single column, single concept). Then write D:AC literal 0s for all 10 rows in a second block. Then write column C notes in a third block. Three discrete writes total for the 10 rows. Number format on D:AC: `#,##0` (no decimals — these are $mm and kg, both integer-ish at the contract level).

### §3.3 — Module shells (5 modules with IN/OUT contract)

The five P&L modules — **Customer Launch, Starlink, ODC, AI Stack, Lunar Mars** — share an identical structural shell this sprint:

- **Rows 4–5** (Sprint 0): year header + year-offset.
- **Row 6**: blank.
- **Rows 7–10**: Allocator IN block (4 rows: section header + 3 data rows). Live formulas.
- **Rows 11–199**: blank (reserved for module body — Sprint 3, 4, 5, 6, 7 fill these).
- **Rows 200–210**: Allocator OUT block (11 rows: section header + 10 data rows). Literal 0 placeholders on data rows.
- **Rows 211–212**: BV memo rows. **Lunar Mars only.** Other four modules leave these blank.

Sprint 1 writes rows 7–10 and rows 200–212 on each of the five module tabs.

#### §3.3.1 — Allocator IN block (rows 7–10 on every P&L module)

For each module M in {Customer Launch, Starlink, ODC, AI Stack, Lunar Mars}, write the following four rows on M's tab:

| Row | Col A label | Col D formula (copy to E:AC) | Col C note |
|---|---|---|---|
| 7 | `INPUTS FROM CENTRAL ALLOCATOR` | (no formula — section header) | (blank) |
| 8 | `Capital Allocation ($mm)` | `=INDEX(Allocator!D:D, MATCH("<M> cash allocation", Allocator!$A:$A, 0))` | `Reads Allocator §5 by label. Sprint 1 returns 0 (placeholder upstream).` |
| 9 | `Starship Capacity Allocation (kg-to-LEO)` | `=INDEX(Allocator!D:D, MATCH("<M> kg allocation", Allocator!$A:$A, 0))` | `Reads Allocator §7 by label. Sprint 1 returns 0 (placeholder upstream).` |
| 10 | `Total Capital Available ($mm)` | `=D8` | `= Capital Allocation (no separate Cash Sweep row — Layer 3 retired).` |

The `<M>` placeholder resolves to the exact module name (case-sensitive, matching the canonical labels written in §3.2.2). So on the Customer Launch tab, row 8 D becomes:

```
=INDEX(Allocator!D:D, MATCH("Customer Launch cash allocation", Allocator!$A:$A, 0))
```

And on the Starlink tab, row 8 D becomes:

```
=INDEX(Allocator!D:D, MATCH("Starlink cash allocation", Allocator!$A:$A, 0))
```

**Excel copy-across behavior:** `Allocator!D:D` uses a relative column reference. When the formula is copied from D8 → E8 → F8 → ... → AC8, Excel shifts to `Allocator!E:E`, `Allocator!F:F`, ..., `Allocator!AC:AC` respectively. `Allocator!$A:$A` uses an absolute column reference (locked by `$`), so MATCH always searches column A. This is the correct anchor pattern for year-row INDEX/MATCH reads per Architecture §16.

**Write structure (Rule 1)** — for each module, do this in five discrete write blocks:

1. Row 7 column A: section header label only. Apply white-on-charcoal fill across A7:AC7 (matching Allocator section-header formatting).
2. Row 8 column A: `Capital Allocation ($mm)` label. Plus row 8 column C: note.
3. Row 8 column D: write the INDEX/MATCH formula above. Then `copyToRange` source D8, destination E8:AC8. (Rule 2: single-cell source.) Apply number format `#,##0`.
4. Row 9 column A: `Starship Capacity Allocation (kg-to-LEO)` label. Plus row 9 column C: note. Row 9 column D: INDEX/MATCH formula for `<M> kg allocation`. `copyToRange` source D9, destination E9:AC9. Number format `#,##0`.
5. Row 10 column A: `Total Capital Available ($mm)` label. Plus row 10 column C: note. Row 10 column D: `=D8`. `copyToRange` source D10, destination E10:AC10. (Excel shifts `=D8` → `=E8` → ... → `=AC8` correctly because D8 is a relative reference.) Number format `#,##0`.

After each module's IN block lands, read D8, I8, S8, AC8 (Capital Allocation 2025, 2030, 2040, 2050). All four must read 0 (because Allocator's canonical allocation row at the matching label is 0 per §3.2.2). Same read on row 9 (kg allocation, all 0) and row 10 (Total Capital Available, all 0 because = D8). Any cell returning `#N/A`, `#NAME?`, `#REF!`, or any non-zero value → halt and report (the label-vs-source contract is broken).

#### §3.3.2 — Allocator OUT block (rows 200–210 on every P&L module; 211–212 on Lunar Mars)

For each module M, write the 11 canonical OUT rows at rows 200–210:

| Row | Col A label | Col D:AC value | Col C note |
|---|---|---|---|
| 200 | `CENTRAL ALLOCATOR OUTPUTS` | (no value — section header) | (blank) |
| 201 | `Total Revenue ($mm)` | literal 0 | `Module-body sprint fills.` |
| 202 | `Module EBITDA ($mm)` | literal 0 | `Gross Profit per vending-machine framing. Module-body sprint fills.` |
| 203 | `Module EBITDA Margin %` | literal 0 | `= EBITDA / Revenue with IFERROR guard. Module-body sprint fills.` |
| 204 | `Module FCF ($mm)` | literal 0 | `= EBITDA + module D&A add-back − Module CapEx, pre-tax pre-corp. Module-body sprint fills.` |
| 205 | `Module CapEx ($mm)` | literal 0 | `Module-body sprint fills.` |
| 206 | `Capital deployed ($mm)` | literal 0 | `= actual deployment × unit cost. Module-body sprint fills.` |
| 207 | `Spot IRR` | literal 0 | `Per-sat / per-launch marginal IRR. Module-body sprint fills using IFERROR(IRR(...),-1).` |
| 208 | `Forward IRR (Y+2)` | literal 0 | `Per-sat / per-launch marginal IRR evaluated at T+2. Module-body sprint fills.` |
| 209 | `Blended IRR` | literal 0 | `= (1−Forward_weight)·Spot + Forward_weight·Forward; Forward_weight = Assumptions!B17 = 0.7. Module-body sprint fills.` |
| 210 | `Capacity Demand (kg-to-LEO)` | literal 0 | `Module's uncapped kg demand fed to Allocator §6. Module-body sprint fills.` |

**Lunar Mars only** — append two BV memo rows below the canonical OUT block (per Architecture §4.2 + §11.6):

| Row | Col A label | Col D:AC value | Col C note |
|---|---|---|---|
| 211 | `Lunar Accumulated Book Value ($mm)` | literal 0 | `Memo: BV engine output. Lunar Mars module sprint fills.` |
| 212 | `Mars Accumulated Book Value ($mm)` | literal 0 | `Memo: BV engine output. Lunar Mars module sprint fills.` |

Apply italic font to rows 211 and 212 column A label (per Rule 17 — memo rows clearly flagged).

**Write structure (Rule 1)** — for each module, do this in three discrete write blocks:

1. Row 200 column A: section header label. Apply white-on-charcoal fill across A200:AC200.
2. Rows 201–210 column A: 10 canonical OUT labels in a single column-A block. Plus column C notes in a second column-C block.
3. Rows 201–210 columns D:AC: literal 0 across all 10 rows × 26 columns = 260 cells. Number format `#,##0` for rows 201, 202, 204, 205, 206 (currency). Number format `0.0%` for row 203 (margin). Number format `0.0%` for rows 207, 208, 209 (IRR). Number format `#,##0` for row 210 (kg).

For Lunar Mars only, after the above three blocks, do two additional writes:
4. Rows 211–212 column A: BV memo labels (italic). Plus column C notes.
5. Rows 211–212 columns D:AC: literal 0. Number format `#,##0`.

After each module's OUT block lands, read D201, I201, S201, AC201 (Total Revenue at 2025, 2030, 2040, 2050) → all must read 0. Same spot-check on row 209 (Blended IRR) and row 210 (Capacity Demand). Any non-zero or error value → halt.

#### §3.3.3 — Module write order (Rule 1 pacing)

Plugin writes the five module shells one at a time, in this order:

1. **Customer Launch** (simplest — no derived rows, no BV memos).
2. **Starlink** (same as Customer Launch — standard 11-row OUT block).
3. **ODC** (same).
4. **AI Stack** (same).
5. **Lunar Mars** (last — adds the 2 BV memo rows).

After each module, read back the four anchor cells (D8, D9, D10 — IN block; D201, D209, D210 — OUT block) and confirm = 0 across the board. Catch issues early per the standard Sprint 0 pacing pattern. Do NOT batch all five modules into one write sequence.

### §3.4 — Non-P&L tab title rows

The five non-P&L tabs (`Launch Capacity`, `Starlink Capacity`, `OpEx`, `CapEx`, `Valuation`) get a single title row at row 6 — column A only — for visual orientation. These tabs are NOT P&L modules per Architecture §1 and §3; they do not get the Allocator IN/OUT contract.

Sprint 8 (OpEx + CapEx), Sprint 9 (Group P&L — separately handled in §3.5), Sprint 2 (Launch Capacity), and the Starlink sprint (Starlink Capacity), Sprint 11 (Valuation) fill the rest.

| Tab | Row | Col A label | Format |
|---|---|---|---|
| Launch Capacity | 6 | `LAUNCH CAPACITY — supply-side: Starship + F9 fleet, cadence, payload, $/kg cost stack, total annual kg-to-LEO. Sprint 2 fills.` | bold, font-size 11, no fill |
| Starlink Capacity | 6 | `STARLINK CAPACITY — aggregates constellation BB + DTC pools, allocates internal bandwidth claim to ODC, computes available bandwidth for external Starlink revenue. Sprint 4 fills.` | bold, font-size 11, no fill |
| OpEx | 6 | `OPEX — corporate operating costs (R&D by module + SG&A by function). Sprint 8 fills.` | bold, font-size 11, no fill |
| CapEx | 6 | `CAPEX — module CapEx aggregation + corporate CapEx + spectrum CapEx + corporate D&A. Sprint 8 fills.` | bold, font-size 11, no fill |
| Valuation | 6 | `VALUATION — DCF off Group FCF + Sum-of-parts per module + Multiples cross-check + Comparables + Sensitivity. Sprint 11 fills.` | bold, font-size 11, no fill |

**Write structure (Rule 1)**: five discrete writes (one per tab), each writing the column-A title cell plus the format. Do not batch.

### §3.5 — Group P&L conservation block (trivial 0 = 0 form)

Group P&L tab gets the conservation block at rows 99–109 per Architecture §15.2. Sprint 1 writes labels + literal 0 placeholders + the R108 boolean formula. Sprint 9 will replace R99–R107 and R109 placeholders with live conservation formulas (INDEX/MATCH against module OUT rows + Group P&L's Revenue/EBITDA/CapEx/FCF/D&A walk above row 99). R108's formula structure stays.

Group P&L tab layout this sprint:

- **Rows 4–5** (Sprint 0): year header + year-offset.
- **Row 6**: title row — column A: `GROUP P&L — consolidated Revenue / EBITDA / D&A / EBIT / Taxes / NOPAT / CapEx / FCF + inter-module eliminations + conservation block. Sprint 9 fills the P&L walk above row 99.` Bold, font-size 11.
- **Rows 7–98**: blank (reserved for Sprint 9 P&L walk + elimination block).
- **Row 99**: conservation row — Revenue check.
- **Row 100**: conservation row — EBITDA check.
- **Row 101**: conservation row — CapEx check.
- **Row 102**: conservation row — FCF check.
- **Row 103**: conservation row — D&A check.
- **Row 104**: conservation row — EBIT consistency.
- **Row 105**: conservation row — Launch services elimination conservation.
- **Row 106**: conservation row — Bandwidth elimination conservation.
- **Row 107**: conservation row — Compute elimination conservation.
- **Row 108**: ALL OK boolean — formula.
- **Row 109**: Cash flow identity check — placeholder.

Detailed row-by-row:

| Row | Col A label | Col D:AC value | Col C note | Format |
|---|---|---|---|---|
| 99 | `Revenue check` | literal 0 | `Sprint 9: = Total Revenue − Σ module revenues + Σ eliminations. Sprint 1 = 0 placeholder.` | `#,##0` |
| 100 | `EBITDA check` | literal 0 | `Sprint 9: = Total EBITDA − Σ module EBITDAs.` | `#,##0` |
| 101 | `CapEx check` | literal 0 | `Sprint 9: = Total Module CapEx − Σ module CapEx.` | `#,##0` |
| 102 | `FCF check` | literal 0 | `Sprint 9: = Total Module FCF − Σ module FCF.` | `#,##0` |
| 103 | `D&A check` | literal 0 | `Sprint 9: = Group D&A − (Σ module D&A in COGS + Corporate D&A).` | `#,##0` |
| 104 | `EBIT consistency` | literal 0 | `Sprint 9: = Group EBIT − (Group EBITDA − Group D&A).` | `#,##0` |
| 105 | `Launch services elimination conservation` | literal 0 | `Sprint 9: = Customer Launch internal transfer rev − Σ consuming modules' Launch services cost.` | `#,##0` |
| 106 | `Bandwidth elimination conservation` | literal 0 | `Sprint 9: = Starlink internal bandwidth rev − ODC bandwidth services cost.` | `#,##0` |
| 107 | `Compute elimination conservation` | literal 0 | `Sprint 9: = ODC internal transfer rev − AI Stack internal compute cost.` | `#,##0` |
| 108 | `ALL OK boolean` | `=IF(AND(ABS(D99)<1,ABS(D100)<1,ABS(D101)<1,ABS(D102)<1,ABS(D103)<1,ABS(D104)<1,ABS(D105)<1,ABS(D106)<1,ABS(D107)<1),"OK","CHECK")` (D-column form; copy across E:AC — relative refs shift correctly) | `R108 = "OK" required for any sprint to declare complete (Rule 5).` | text (no number format) |
| 109 | `Cash flow identity` | literal 0 | `Sprint 9: = Starting cash + Σ IPO + Σ Group FCF − Σ deployed CapEx − Σ strategic carve-out − Cash EoY (final year).` | `#,##0` |

**Write structure (Rule 1)** — five discrete writes:

1. Row 6 column A title row + format.
2. Rows 99–109 column A labels (single column block).
3. Rows 99–107 + 109 columns D:AC literal 0 (single block of 10 rows × 26 cols = 260 cells; skip R108 — formula goes in next step).
4. Row 108 column D: write the AND formula above. Then `copyToRange` source D108, destination E108:AC108. Excel shifts `D99:D107` → `E99:E107` → ... → `AC99:AC107` correctly because all refs are relative.
5. Column C notes for rows 99–109 (single column block). Apply italic to rows 99–109 column A labels (these are diagnostic checks, not operative P&L lines — per Rule 17 memo convention adapted for the conservation block).

After all writes land, read D108, I108, S108, AC108. **Every cell must read the text string "OK".** If any year reads `"CHECK"`, `#REF!`, `#NAME?`, or any other value → halt and report. The trivial 0 = 0 conservation contract is the gate for Sprint 1 to declare complete.

### §3.6 — Saving (Vlad's job, not the plugin's)

The plugin does not save. After all writes complete and verification reports PASS, Vlad saves the workbook in Excel (`Ctrl+S` / `Cmd+S`). Verification reads cells from the live workbook session, not from the saved file — no save required for verification to run.

---

## §4 — Verification gate

Any failure → halt, report, push back. No "proceed and document."

### §4.1 — Universal checks

- **No formula errors workbook-wide.** Read every cell on every tab; count `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`. **Expected: zero.** The only formulas Sprint 1 writes are (a) module IN-block INDEX/MATCH refs on rows 8–9 of each of 5 modules (10 row-formulas × 26 columns = 260 cells), (b) module IN-block `=D8` refs on row 10 of each of 5 modules (5 row-formulas × 26 columns = 130 cells), (c) Group P&L R108 boolean (26 cells). Total formula cells: 416. Every one must resolve to a valid value (the IN/MATCH formulas to 0; R108 to "OK"). Any error indicates a label mismatch (Rule 12 violation) or a write-time corruption.
- **Edge-year reads.** For every formula cell, read columns D (2025), I (2030), S (2040), AC (2050) and confirm value matches expectation. Listed in §4.2.
- **Round-trip stability.** Recalc the workbook 5 times. Sprint 1's formulas are all single-pass (no iterative dependencies); every cell must be invariant across recalcs. **Expected: bit-for-bit identical.** Any drift → halt (suggests workbook iterative-calc settings are conflicting with Sprint 1's pure-feedforward formulas).

### §4.2 — Sprint 1 anchor read-back (HALT GATE)

Plugin reads each anchor cell and compares to expected value. Any deviation → halt.

**Allocator canonical allocation rows (10 labels × 4 edge years = 40 reads):**

| Cell | Tab | Expected | Tolerance |
|---|---|---|---|
| A83 | Allocator | text `Customer Launch cash allocation` | exact |
| A84 | Allocator | text `Starlink cash allocation` | exact |
| A85 | Allocator | text `ODC cash allocation` | exact |
| A86 | Allocator | text `AI Stack cash allocation` | exact |
| A87 | Allocator | text `Lunar Mars cash allocation` | exact |
| A133 | Allocator | text `Customer Launch kg allocation` | exact |
| A134 | Allocator | text `Starlink kg allocation` | exact |
| A135 | Allocator | text `ODC kg allocation` | exact |
| A136 | Allocator | text `AI Stack kg allocation` | exact |
| A137 | Allocator | text `Lunar Mars kg allocation` | exact |
| D83, I83, S83, AC83 | Allocator | 0 | exact |
| D84, I84, S84, AC84 | Allocator | 0 | exact |
| D85, I85, S85, AC85 | Allocator | 0 | exact |
| D86, I86, S86, AC86 | Allocator | 0 | exact |
| D87, I87, S87, AC87 | Allocator | 0 | exact |
| D133, I133, S133, AC133 | Allocator | 0 | exact |
| D134, I134, S134, AC134 | Allocator | 0 | exact |
| D135, I135, S135, AC135 | Allocator | 0 | exact |
| D136, I136, S136, AC136 | Allocator | 0 | exact |
| D137, I137, S137, AC137 | Allocator | 0 | exact |

**Module IN blocks (5 modules × 4 edge years × 3 rows = 60 reads):**

For each module M in {Customer Launch, Starlink, ODC, AI Stack, Lunar Mars}:

| Cell on M's tab | Expected | Tolerance |
|---|---|---|
| A7 | text `INPUTS FROM CENTRAL ALLOCATOR` | exact |
| A8 | text `Capital Allocation ($mm)` | exact |
| A9 | text `Starship Capacity Allocation (kg-to-LEO)` | exact |
| A10 | text `Total Capital Available ($mm)` | exact |
| D8, I8, S8, AC8 | 0 (resolved via INDEX/MATCH against Allocator) | exact |
| D9, I9, S9, AC9 | 0 (resolved via INDEX/MATCH against Allocator) | exact |
| D10, I10, S10, AC10 | 0 (= D8 / E8 / ... / AC8) | exact |

**Module OUT blocks (5 modules × 4 edge years × 10 data rows = 200 reads):**

For each module M:

| Cell on M's tab | Expected | Tolerance |
|---|---|---|
| A200 | text `CENTRAL ALLOCATOR OUTPUTS` | exact |
| A201 | text `Total Revenue ($mm)` | exact |
| A202 | text `Module EBITDA ($mm)` | exact |
| A203 | text `Module EBITDA Margin %` | exact |
| A204 | text `Module FCF ($mm)` | exact |
| A205 | text `Module CapEx ($mm)` | exact |
| A206 | text `Capital deployed ($mm)` | exact |
| A207 | text `Spot IRR` | exact |
| A208 | text `Forward IRR (Y+2)` | exact |
| A209 | text `Blended IRR` | exact |
| A210 | text `Capacity Demand (kg-to-LEO)` | exact |
| D201, I201, S201, AC201 | 0 | exact |
| D202, I202, S202, AC202 | 0 | exact |
| D203, I203, S203, AC203 | 0 | exact |
| D204, I204, S204, AC204 | 0 | exact |
| D205, I205, S205, AC205 | 0 | exact |
| D206, I206, S206, AC206 | 0 | exact |
| D207, I207, S207, AC207 | 0 | exact |
| D208, I208, S208, AC208 | 0 | exact |
| D209, I209, S209, AC209 | 0 | exact |
| D210, I210, S210, AC210 | 0 | exact |

**Lunar Mars BV memo rows (4 edge years × 2 rows = 8 additional reads):**

| Cell on Lunar Mars tab | Expected | Tolerance |
|---|---|---|
| A211 | text `Lunar Accumulated Book Value ($mm)` | exact |
| A212 | text `Mars Accumulated Book Value ($mm)` | exact |
| D211, I211, S211, AC211 | 0 | exact |
| D212, I212, S212, AC212 | 0 | exact |

**Group P&L conservation block (1 boolean row × 4 edge years + 10 placeholder rows × 4 edge years = 44 reads):**

| Cell on Group P&L tab | Expected | Tolerance |
|---|---|---|
| A99 | text `Revenue check` | exact |
| A100 | text `EBITDA check` | exact |
| A101 | text `CapEx check` | exact |
| A102 | text `FCF check` | exact |
| A103 | text `D&A check` | exact |
| A104 | text `EBIT consistency` | exact |
| A105 | text `Launch services elimination conservation` | exact |
| A106 | text `Bandwidth elimination conservation` | exact |
| A107 | text `Compute elimination conservation` | exact |
| A108 | text `ALL OK boolean` | exact |
| A109 | text `Cash flow identity` | exact |
| D99, I99, S99, AC99 | 0 | exact |
| D100, I100, S100, AC100 | 0 | exact |
| D101, I101, S101, AC101 | 0 | exact |
| D102, I102, S102, AC102 | 0 | exact |
| D103, I103, S103, AC103 | 0 | exact |
| D104, I104, S104, AC104 | 0 | exact |
| D105, I105, S105, AC105 | 0 | exact |
| D106, I106, S106, AC106 | 0 | exact |
| D107, I107, S107, AC107 | 0 | exact |
| **D108, I108, S108, AC108** | **text `"OK"`** | **exact** |
| D109, I109, S109, AC109 | 0 | exact |

**Non-P&L tab title rows (5 reads):**

| Cell | Expected |
|---|---|
| Launch Capacity!A6 | text starts with `LAUNCH CAPACITY` |
| Starlink Capacity!A6 | text starts with `STARLINK CAPACITY` |
| OpEx!A6 | text starts with `OPEX` |
| CapEx!A6 | text starts with `CAPEX` |
| Valuation!A6 | text starts with `VALUATION` |

**Sprint 0 inheritance spot-check (4 reads — protects against accidental damage):**

| Cell | Tab | Expected | Tolerance |
|---|---|---|---|
| D4 | Allocator | 2025 | exact |
| AC4 | Allocator | 2050 | exact |
| D5 | Allocator | 0 | exact |
| AC5 | Allocator | 25 | exact |
| Assumptions!B8 | Assumptions | 5000 (Starting cash position EoY 2024) | exact |
| Assumptions!B17 | Assumptions | 0.7 (Forward IRR weight w) | exact |

### §4.3 — Halt conditions (quantitative)

Plugin halts and reports if:

- Any anchor in §4.2 deviates from expected.
- Any cell in row 4 on tabs 1–13 ≠ literal integer in {2025…2050} (Sprint 0 inheritance check).
- Any cell in row 5 on tabs 1–13 ≠ literal integer in {0…25} (Sprint 0 inheritance check).
- Any error value (`#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`) anywhere in the workbook.
- Any IN-block INDEX/MATCH formula returns anything other than 0 (means either the Allocator canonical allocation row label is misspelled, the value is non-zero, or the MATCH is hitting the wrong row).
- Any OUT-block data cell (D:AC on rows 201–210, or 211–212 for Lunar Mars) ≠ literal 0.
- Any Group P&L R108 cell (D108:AC108) ≠ text `"OK"`.
- Any sheet name has changed from the Sprint 0 list (§3.1).
- Round-trip stability fails (cell value drifts across 5 recalcs).

### §4.4 — Verification log (plugin produces in chat)

After §4.1–§4.3 pass, plugin produces:

```
Sprint 1 verification log
=========================

Workbook: SpaceX Model V2.2.xlsx (Vlad-saved as from V2.1)

Sprint 0 inheritance: PASS
  - 14 tabs present in locked order
  - Row 4 + Row 5 standards intact on tabs 1-13
  - Assumptions!B8 (Starting cash) = 5000
  - Assumptions!B17 (Forward IRR weight) = 0.7
  - Claude Log row 2 (Sprint 0 entry) intact

Allocator skeleton: PASS
  - 9 section headers at rows 7, 17, 31, 39, 82, 89, 132, 139, 152
  - 10 canonical allocation rows (cash 83-87, kg 133-137)
  - All 10 × 26 = 260 allocation cells = 0
  - Reserved blank rows preserved for Sprint 10

Module shells (5 of 5): PASS
  - Customer Launch: IN block rows 7-10 (D8 = 0, D9 = 0, D10 = 0 via INDEX/MATCH); OUT block rows 200-210 (all data cells = 0)
  - Starlink: IN block rows 7-10 (resolves to 0); OUT block rows 200-210 (= 0)
  - ODC: IN block rows 7-10 (resolves to 0); OUT block rows 200-210 (= 0)
  - AI Stack: IN block rows 7-10 (resolves to 0); OUT block rows 200-210 (= 0)
  - Lunar Mars: IN block rows 7-10 (resolves to 0); OUT block rows 200-210 + BV memos 211-212 (= 0)

Group P&L conservation block: PASS
  - Rows 99-109 labels written
  - R99-R107 + R109 D:AC = 0 placeholders
  - R108 D:AC = "OK" (trivial 0 = 0 conservation passes)

Non-P&L title rows (5 of 5): PASS
  - Launch Capacity!A6, Starlink Capacity!A6, OpEx!A6, CapEx!A6, Valuation!A6

§4.1 universal checks:
  - Error scan (#REF!/#VALUE!/#DIV/0!/#NAME?/#NUM!/#NULL!/#N/A): 0/0/0/0/0/0/0
  - Round-trip stability: 5 recalcs, bit-for-bit identical: PASS

Flags / open questions: [any items needing Vlad attention]

Status: PASS → write Claude Log entry → leave workbook for Vlad to save.
```

---

## §5 — Claude Log entry

Plugin appends to `Claude Log` row 3 (after §4 passes):

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| 2026-MM-DD | 1 | Allocator (skeleton: 9 section headers + 10 canonical allocation rows at canonical labels); Customer Launch + Starlink + ODC + AI Stack + Lunar Mars (IN block rows 7-10 with live INDEX/MATCH against Allocator + OUT block rows 200-210 with literal 0 placeholders; Lunar Mars also rows 211-212 BV memos); Launch Capacity + Starlink Capacity + OpEx + CapEx + Valuation (title row 6 only); Group P&L (conservation block rows 99-109 with R108 boolean formula); Claude Log (this row). | Wired the cross-tab contract. Every module's IN block resolves to 0 via INDEX/MATCH against Allocator's canonical allocation labels (5 cash, 5 kg). Every module's OUT block has the 11 canonical rows (Lunar Mars adds 2 BV memos). Group P&L conservation block reads OK at trivial 0=0 across all years. No formula errors, round-trip stable. | Reserved blank rows on Allocator (rows 8-15, 18-29, 32-37, 40-80, 90-130, 140-150, 153-165) await Sprint 10 computation logic. Reserved blank rows 11-199 on each module tab await module-body sprints (Customer Launch = Sprint 3, Starlink = Sprint 4, ODC = Sprint 5, AI Stack = Sprint 6, Lunar Mars = Sprint 7). Group P&L rows 7-98 await Sprint 9 P&L walk. | Sprint 2: Launch Capacity tab full build (Starship + F9 fleet, cadence, payload, $/kg cost stack, total annual kg-to-LEO capacity). |

Date column populated by plugin with actual execution date.

---

## §6 — Don't touch (out of scope)

- No module body content on any of the 5 module tabs (revenue, COGS, CapEx, IRR engines, deployment logic, ratchets, retirement schedules). Sprint 2–7.
- No Allocator computation logic (Cash BoY tracker, queue gate computations, Mars carve-out formula, sigmoid blend, vehicle build claim sizing, central IRR display). Sprint 10.
- No Group P&L walk above row 99 (Revenue → COGS → EBITDA → D&A → EBIT → Taxes → NOPAT → CapEx → FCF). Sprint 9.
- No replacement of conservation block R99–R107 + R109 placeholder 0s with live INDEX/MATCH formulas. Sprint 9 (R108 formula stays as written this sprint).
- No OpEx tab content (R&D by module, SG&A by function, Mars/Moon R&D year-row). Sprint 8.
- No CapEx tab content (module CapEx aggregation, Corporate CapEx, Spectrum CapEx, Corporate D&A). Sprint 8.
- No Launch Capacity / Starlink Capacity tab content. Sprint 2 + Sprint 4 respectively.
- No Valuation tab content. Sprint 11.
- No internal-transfer flow rows (launch services, bandwidth, internal compute) on module tabs or eliminations on Group P&L. Module-body sprints + Sprint 9.
- No MC engine (sampling logic, distribution outputs). Sprint 12.
- No edits to Assumptions tab (every input is locked from Sprint 0; if any value is wrong, file a Sprint 0.5 patch — do not edit in this sprint).
- No edits to Claude Log row 2 (Sprint 0 entry is locked).
- No row insertions anywhere (Rule 10).
- No plugin-issued save commands.
- No styling beyond: white-on-charcoal section-header fills on Allocator + module OUT-block headers (rows 7 / 17 / 31 / 39 / 82 / 89 / 132 / 139 / 152 on Allocator; row 7 + row 200 on each module); italic on Lunar Mars BV memo rows + Group P&L conservation row labels; bold on non-P&L tab title rows + module IN-block section header.

---

## §7 — Open thread (post-sprint considerations)

### §7.1 — Workbook naming convention continues

Sprint 1 output is `SpaceX Model V2.2.xlsx`. Default for downstream: continue `V2.N` (Sprint 2 → V2.3, etc.). Sprint 0 §7.3 confirmed this convention; Sprint 1 inherits.

### §7.2 — Allocator row positions are now locked

The 10 canonical allocation labels at rows 83–87 (cash) and 133–137 (kg) are LOAD-BEARING. Every future cross-tab reference uses INDEX/MATCH on the column-A label, so row positions can technically shift — but per Rule 10, no row insertions on cross-referenced tabs. Sprint 10 fills reserved rows (8–15, 18–29, 32–37, 40–80, 90–130, 140–150, 153–165) without disturbing the canonical rows. If Sprint 10 needs more rows for any subsection than reserved, file a Sprint 10.5 patch — do not insert rows.

### §7.3 — Module body row budget

Module bodies (Sprint 3–7) get rows 11–199 = 189 usable rows per module. V30.5's largest module tab (Starlink) used ~190 rows; this should be sufficient. If a module-body sprint needs more, append BELOW row 212 (after the OUT block) — but that breaks the convention that OUT block is the last block on the tab and risks confusion. Strong preference: stay within rows 11–199. File a Sprint X.5 patch if a module body genuinely needs >189 rows.

### §7.4 — IN-block formula reliability

The INDEX/MATCH formulas on rows 8–9 of each module tab reference the Allocator's canonical allocation rows by label. If a future sprint accidentally renames or deletes one of those labels, every module IN block returns `#N/A` and every downstream computation breaks. Rule 22 stale-ref scan picks this up. Sprint 1's verification §4.2 has the labels enumerated; future sprints' verifications should re-verify against the same list whenever they touch Allocator.

### §7.5 — Module OUT-block formula upgrade in module-body sprints

When module-body sprints (3–7) fill the OUT block, they replace the literal 0 on each data row with the appropriate formula:
- Row 201 (Total Revenue): SUM or = label-resolved reference to the module's revenue total row in the body.
- Row 202 (Module EBITDA): = Gross Profit row in body.
- Row 203 (Module EBITDA Margin %): `=IFERROR(D202/D201, 0)` per Rule 20.
- Row 204 (Module FCF): = D202 + D&A add-back − D205.
- Row 205 (Module CapEx): = label-resolved reference to body.
- Row 206 (Capital deployed): = actual deployment × unit cost.
- Rows 207–208 (Spot/Forward IRR): `=IFERROR(IRR(IF(SEQUENCE(1,N+1)=1, -cost_per_unit, net_marginal_revenue)), -1)` per Architecture §5.1.
- Row 209 (Blended IRR): `=(1-Assumptions!$B$17)*D207 + Assumptions!$B$17*D208`.
- Row 210 (Capacity Demand): = label-resolved reference to body's kg demand row.

Module-body sprints write their own §3 patches against this contract.

---

## §8 — Execution sequence (plugin runs in this order)

Save commands NOT in this sequence — Vlad handles all saving.

1. **Pre-flight checks** (§3.0): confirm target workbook open + correctly named, Sprint 0 baseline intact, Assumptions anchors hold, kickoff confirmation block received.
2. **Allocator skeleton** (§3.2):
   1. Write 9 section headers (rows 7, 17, 31, 39, 82, 89, 132, 139, 152) — one per write, with white-on-charcoal formatting.
   2. Write 10 canonical allocation row column-A labels (rows 83–87 + 133–137) — single column-A block.
   3. Write 10 × 26 = 260 cells of literal 0 on rows 83–87 D:AC + 133–137 D:AC — single block. Number format `#,##0`.
   4. Write 10 column-C notes — single column-C block.
   5. Read-back: A83, A84, A85, A86, A87, A133, A134, A135, A136, A137 labels + D83, D87, AC87, D133, D137, AC137 cells (=0).
3. **Module shells** (§3.3) — one module at a time, in order Customer Launch → Starlink → ODC → AI Stack → Lunar Mars. For each:
   1. **IN block (rows 7–10)**:
      - Row 7 column A section header label + white-on-charcoal fill A7:AC7.
      - Row 8 column A label + column C note.
      - Row 8 column D: INDEX/MATCH formula. `copyToRange` source D8, destination E8:AC8. Number format `#,##0` on D8:AC8.
      - Row 9 column A label + column C note.
      - Row 9 column D: INDEX/MATCH formula. `copyToRange` source D9, destination E9:AC9. Number format `#,##0`.
      - Row 10 column A label + column C note.
      - Row 10 column D: `=D8`. `copyToRange` source D10, destination E10:AC10. Number format `#,##0`.
   2. **OUT block (rows 200–210)**:
      - Row 200 column A section header label + white-on-charcoal fill A200:AC200.
      - Rows 201–210 column A labels — single column-A block.
      - Rows 201–210 column C notes — single column-C block.
      - Rows 201–210 columns D:AC literal 0 — single block. Apply number formats per row (§3.3.2).
   3. **For Lunar Mars only — BV memo rows (rows 211–212)**:
      - Row 211 column A label (italic) + column C note.
      - Row 212 column A label (italic) + column C note.
      - Rows 211–212 columns D:AC literal 0. Number format `#,##0`.
   4. **Read-back for module**: A7, A8, A9, A10, A200, A201, A209, A210 labels + D8, D9, D10, D201, D209, D210, AC10, AC210 cells (all = 0; A cells = expected text). For Lunar Mars also A211, A212 + D211, D212 (= 0).
4. **Halt during step 3 if** any IN-block cell returns non-zero (label mismatch on Allocator), any error value, or any label-vs-source mismatch.
5. **Non-P&L tab title rows** (§3.4) — five discrete writes, one per tab.
6. **Group P&L conservation block** (§3.5):
   1. Row 6 column A title row + format.
   2. Rows 99–109 column A labels.
   3. Rows 99–107 + 109 columns D:AC literal 0 (skip R108).
   4. Row 108 column D: AND formula. `copyToRange` source D108, destination E108:AC108. Verify D108 returns text `"OK"`.
   5. Column C notes for rows 99–109.
   6. Read-back: D108, I108, S108, AC108 — all must read `"OK"`. If any reads `"CHECK"` → halt.
7. **Run §4 verification gate** against the live workbook. Halt on any failure.
8. **Write Claude Log Sprint 1 entry** (§5) — row 3 of Claude Log tab, six columns.
9. **Produce verification log** in chat (§4.4 format). Done. Vlad saves the workbook.

---

## §9 — Amendment log

- **2026-05-20 (initial draft)** — Second sprint spec of rebuild v2. Scope: Allocator section-header skeleton + 10 canonical allocation rows (cash + kg, by-label contract); module shells for 5 P&L modules (Customer Launch, Starlink, ODC, AI Stack, Lunar Mars) with IN block (rows 7–10, live INDEX/MATCH) and OUT block (rows 200–210, literal 0 placeholders); Lunar Mars BV memo rows 211–212; non-P&L tab title rows; Group P&L conservation block rows 99–109 with R108 boolean formula (trivial OK at 0=0). Self-contained per the kickoff README standing process rules: no external file references; plugin save commands removed.
