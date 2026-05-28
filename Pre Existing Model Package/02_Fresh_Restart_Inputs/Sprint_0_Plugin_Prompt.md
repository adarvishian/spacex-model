# Sprint 0 — Excel Plugin Prompt (paste into a fresh blank Excel workbook with the plugin invoked)

---

You are the Excel Claude plugin executing **Sprint 0 of the SpaceX Model Rebuild v2**. The workbook open in front of you is a **fresh blank Excel workbook** (one default sheet, no data). You are about to populate it from scratch per the spec below.

## Before any cell writes

Read these constitutional docs in this order, from the workspace folder `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/`:

1. `00_README_Sprint_Kickoff.md` — kickoff protocol.
2. `01_Lessons_Learned.md` — 23 principles from V30.5 failure modes.
3. `02_Architecture_and_Methodology.md` — structural + math conventions (the source of truth on every cross-tab connection, IRR formula, conservation identity).
4. `03_Sprint_Roadmap_and_Verification.md` — 12-sprint roadmap + universal verification protocol.
5. `04_Assumptions_Tab_Spec.md` — column convention, MC distribution types, section structure.
6. `Model Execution Rules.md` — the 23 execution rules + Rule Compliance Preamble.
7. `2025 Anchors from Q4_25.md` — locked 2025 historical anchors.

Also confirm read access to:
- `04_Assumptions_Tab_Build_Plan.xlsx` — the row-by-row driver for Assumptions tab content.

Acknowledge each doc read in your first response. If you cannot read any of them from disk, say so — the spec is sufficient to execute against, but constitutional context is preferred.

## After constitutional reads, confirm

- The Rule Compliance Preamble in §1 of the spec below — read it box by box. All 12 boxes are ticked or marked N/A with justification by the spec author. If you find any box unjustified, halt and report.
- The §3.0 pre-flight checks pass (blank workbook, Build Plan readable, target path writable, docs read).

## Then execute

Follow §8 (execution sequence) exactly. Pace section by section; do not batch the full Assumptions tab in one write. After each of the 11 Assumptions sections, read back the last input row to confirm landing. Halt on any §4.3 condition.

When done, produce the §4.4 verification log block, write the Claude Log entry, save the workbook, and report completion.

---

# Sprint 0 Spec (below this line — execute against this)

# Sprint 0 — Assumptions Tab + Workbook Standards

**Sprint type**: Foundational. First cell-write of the rebuild v2.
**Execution context**: Excel Claude plugin chat, operating on a **fresh blank Excel workbook** opened by Vlad. The workbook has one default sheet (typically `Sheet1`) and no other content. The plugin's first action is to save the workbook to the target filename; all subsequent writes happen in that file.
**Target workbook**: `SpaceX_Model_v2_S0.xlsx`, saved to `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/`.
**Day budget**: 1 day.

---

## §0 — Constitutional references

- `00_README_Sprint_Kickoff.md` — kickoff protocol.
- `01_Lessons_Learned.md` — **Sprint 0 load-bearing principles**: 1 (architectural lockings day one), 6 (no tab without locked function), 7 (lock names day one), 11 (zero OFFSET), 12 (anchor-and-offset), 13 (year-offset helper row), 14 (cross-tab refs by label), 18 (MC ranges at creation), 19 (sanity halt), 20 (edge-year reads), 23 (calibration targets locked).
- `02_Architecture_and_Methodology.md` — §1 (15-tab inventory, sheet order locked), §2 (year horizon D:AC = 2025–2050, row 4 header, row 5 offsets), §17 (2025 calibration targets).
- `03_Sprint_Roadmap_and_Verification.md` — §3 Sprint 0 scope, §5 universal verification, §8 sprint-spec template.
- `04_Assumptions_Tab_Spec.md` — column convention, MC distribution types, section structure (11 logical sections, ~290 rows).
- `04_Assumptions_Tab_Build_Plan.xlsx` — row-by-row driver. Plugin walks this top-to-bottom and writes to the target workbook's Assumptions tab.
- `2025 Anchors from Q4_25.md` — locked 2025 historicals; calibration anchors.
- `Model Execution Rules.md` — 23 rules; Preamble below.

---

## §1 — Rule Compliance Preamble (mandatory)

- [x] **Rule 1** (one concept per write) — Section structure separates: tab creation, year header writes (row 4), year-offset writes (row 5), Assumptions column-A labels, column-B Base Case values, column-C notes, column D–AC year-row values, columns AG–AJ MC fields, formatting. Each is a discrete write block.
- [x] **Rule 3 / 23** (formula pattern) — Sprint 0 writes no formulas. Year header row 4 and year-offset row 5 are **literal integers**, never `=D5+1` chains. No `OFFSET()` anywhere.
- [x] **Rule 4** (verification gate) — §4 specifies read-back cells + expected values for ≥36 anchors covering starting cash, F9 fleet, F9 price, Mars/Moon R&D, Starshield decay, Starshield rev/Gbps, ARPUs, IPO, sigmoid k, Forward weight, year-row trajectory samples, and the row-4/row-5 standards on every active tab.
- [x] **Rule 6** (inline formulas) — N/A this sprint (no formulas written). All values are hardcoded constants per the Build Plan XLSX.
- [x] **Rule 10** (no row insertions) — N/A (fresh workbook, nothing to insert above). All writes append top-down per the Build Plan.
- [x] **Rule 11** (touch points) — Assumptions is a leaf source this sprint; nothing reads from it yet. Sprint 1+ wires reads against canonical labels.
- [x] **Rule 12** (label-based cross-tab refs) — N/A this sprint. No cross-tab references written.
- [x] **Rule 13** (vending-machine test) — N/A (no module body content this sprint).
- [x] **Rule 14** (no hardcoded constants in formulas) — N/A (no formulas). Assumptions is *where* the constants live, satisfying the rule's spirit.
- [x] **Rule 15** (sanity check halt thresholds) — §4.3 halt conditions explicit and quantitative.
- [x] **Rule 19** (save-as) — Target workbook `SpaceX_Model_v2_S0.xlsx` named in header. Save-as is **execution step 1** (§8.1) — before any cell writes.
- [x] **Rule 22** (stale-ref scan) — Trivially satisfied (no cross-tab refs to scan). Re-engages Sprint 1+.

Architecture & Methodology compliance:
- [x] Module P&L vending-machine framing — N/A this sprint.
- [x] Per-sat / per-launch marginal IRR engine — N/A directly, but the Assumptions inputs that drive it (Forward_weight = 0.7, Sigmoid_k = 2, ODC_design_life = 5, Mars_pct, Mars_floor, Starting_cash, IPO_year, IPO_amount, Vehicle_build_lead_time) are populated here per §4.2.
- [x] Allocator OUT contract — N/A this sprint; 11 canonical labels referenced Sprint 1+.
- [x] Year-offset helper row + year header — **CORE OUTPUT.** Pre-staged on every year-column tab per §3.3.
- [x] ZERO `OFFSET()` formulas — N/A (no formulas this sprint). Standing principle re-asserted.

All boxes ticked or marked N/A with justification. **If any box is unchecked, plugin halts and pushes back.** Otherwise proceed.

---

## §2 — Framing

**Why this sprint.** The rebuild needs a single source of truth for every input before any downstream calculation lands. V30.5's 35-spec accretion produced 200–400 cells of stale residue because inputs were added scattered across module tabs, then partially retracted, then re-added with different conventions. Sprint 0 sets the discipline: every behavioural assumption lives on Assumptions with a Base Case, an MC range, and a distribution type, populated at creation per Principle 18.

**Why now.** The four constitutional docs are locked. The Q4'25 anchors are locked. The Build Plan XLSX is row-by-row ready. There is no remaining open architectural question that blocks Sprint 0 — AI Stack is resolved standalone, Lunar Mars is resolved as strategic carve-out, ODC is resolved cash-driven, vehicle build is resolved as non-module claim.

**What this sprint produces.** A fresh workbook with:
1. 14 tabs in locked sheet order (Architecture §1 minus Demand Curves, which Sprint 4 imports if still load-bearing).
2. Year header (row 4, hardcoded integers D=2025…AC=2050) and year-offset helper (row 5, hardcoded integers D=0…AC=25) on every tab with year columns.
3. Assumptions tab fully populated per the Build Plan XLSX — ~290 rows across 11 sections, every input with Base Case + MC range + distribution + notes.
4. Claude Log tab seeded with header row + Sprint 0 entry.

**What this sprint does NOT produce.** Any formula. Any cross-tab reference. Any module body content. The other 12 tabs are skeletons — sheet exists, year header + offset row written, otherwise blank. Sprint 1 lays the Allocator IN/OUT contract; Sprints 2+ fill in module bodies.

---

## §3 — Scope

### §3.0 — Pre-flight checks (plugin runs BEFORE any cell writes)

1. **Confirm starting state**: open workbook has exactly one sheet, no named ranges, no data on any cell. If the workbook is not blank (e.g. has multiple sheets, or `Sheet1` has content) → **halt**, report what's there, push back to spec author. The plugin doesn't proceed against a non-blank workbook because residue from a prior open can corrupt the Sprint 0 baseline.
2. **Confirm Build Plan XLSX is readable**: open `04_Assumptions_Tab_Build_Plan.xlsx` from the workspace folder. Verify it has the expected section structure (11 sections per Assumptions Tab Spec §2). If unreadable or structurally unexpected → halt, report, push back.
3. **Confirm target path is writable**: verify `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/` is writable. If a file named `SpaceX_Model_v2_S0.xlsx` already exists at the target path → halt, ask Vlad whether to overwrite or pick a different suffix (e.g. `_S0a.xlsx`).
4. **Confirm constitutional docs read**: plugin acknowledges having read the seven docs in §0. (Plugin's own internal check; mention in the verification log.)

### §3.1 — Workbook creation + sheet order

**Step 1 (save-as)**: Before any other write, save the blank workbook as `SpaceX_Model_v2_S0.xlsx` at the target path. From this point on, the open workbook is `SpaceX_Model_v2_S0.xlsx`.

**Step 2 (sheet creation)**: The blank workbook has one default sheet. Rename it to `Assumptions` (this becomes the first tab in the locked order). Then create the remaining 13 tabs after `Assumptions`, in exactly this order, with these exact names (case, spacing, punctuation matter — Principle 7 locks them):

1. `Assumptions` *(renamed from default `Sheet1`)*
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

**Demand Curves**: NOT created this sprint. Deferred to Sprint 4. Open thread §7.1.

### §3.2 — Year header + year-offset helper row (every year-column tab)

On tabs 1–13 (every tab except `Claude Log`), write:

- **Row 4 — year header**: D4=2025, E4=2026, F4=2027, …, AC4=2050. **Literal integers**, not formulas. 26 cells per tab × 13 tabs = 338 cells.
- **Row 5 — year-offset helper**: D5=0, E5=1, F5=2, …, AC5=25. **Literal integers**, not formulas. 26 × 13 = 338 cells.

Per Principle 13 + Architecture §2. Per Stale Row Map §1.3, V30.5's recursive `D11=2025, E11=D11+1, …` chain broke a downstream cascade in Spec 04 when row 11 got wiped. Hardcoded integers eliminate the failure mode.

**Write structure (Rule 1):** for each tab, write row 4 in one operation, then row 5 in a second separate operation. Do not combine. Apply bold + bottom-border formatting to row 4 (year header) and a subtle grey fill to row 5 (year-offset helper) so the structural rows are visually distinct from data rows below.

### §3.3 — Assumptions tab build (Build Plan XLSX-driven)

Open `04_Assumptions_Tab_Build_Plan.xlsx` and walk rows top-to-bottom. For each row, write to the corresponding row on the target workbook's `Assumptions` tab per the column convention from Assumptions Tab Spec §1:

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
- **Section headers** (11 sections per Assumptions Tab Spec §2: Global, Allocator, Capacity, Customer Launch, Starlink, ODC, AI Stack, Lunar Mars, OpEx, CapEx, Valuation) — white-on-charcoal fill, bold, label at column A only.
- **Subsection headers** — italic, light grey fill, label at column A only.
- **Input rows** — column A label + B (or D–AC) value + C note + AG–AJ MC fields.

**For each input row from the Build Plan:**
1. Write column-A label.
2. If Base Case is single-value → write to column B; leave D–AC blank.
3. If year-row → write each year's value to D through AC as **static numbers** (plugin pre-computes from the Build Plan's start/end/CAGR parameters; per Assumptions Tab Spec §4, values not formulas live on Assumptions so Excel can't accidentally chain). Leave column B blank.
4. Write notes to column C.
5. Write MC Min to AG, MC Max to AH, MC Distribution to AI, MC notes to AJ.
6. Apply light yellow fill to AG:AJ when distribution ≠ `fixed` (MC-variable inputs visually flagged).

**Per Principle 18 (LOAD-BEARING):** every input has its MC range populated at creation. If the Build Plan XLSX lists an input without an MC range and distribution ≠ `fixed`, plugin **halts** and reports the offending row. No retroactive MC fill-ins; this is the discipline V30.5 lost.

**Pacing**: Don't attempt all ~290 rows in one massive operation. Walk section by section (11 sections); after each section, run a quick read-back of that section's last row to confirm the column-A label and column-B / D–AC values landed as expected. Catch issues early.

### §3.4 — Claude Log tab seeding

`Claude Log` tab — no year columns. Header row at row 1, in this exact column layout:

| Col | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| Row 1 | Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |

Apply bold to row 1, bottom border. The Sprint 0 entry at row 2 is written **after** §4 verification passes — see §5.

### §3.5 — Workbook save

Save the workbook after all writes complete and before the verification gate. The plugin runs verification against the saved file.

---

## §4 — Verification gate

Per Sprint Roadmap §5 + Principle 19/20/23. Any failure → halt, report, push back to spec author. No "proceed and document."

### §4.1 — Universal checks (§5.1–§5.5 of Sprint Roadmap)

- **§5.1 No formula errors workbook-wide.** Read every cell on every tab; count `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`. **Expected: zero.** Sprint 0 writes no formulas, so any error indicates a data-type miswrite or corrupt tab.
- **§5.2 Conservation block.** N/A this sprint — Group P&L conservation block is built Sprint 9. Trivially passes.
- **§5.3 Edge-year reads.** On the Assumptions tab, for selected year-row inputs (BB ARPU, DTC ARPU, EchoStar spectrum CapEx, Starship customer launch price, Mars/Moon R&D), read columns D (2025), I (2030), S (2040), AC (2050) and confirm trajectory shape matches the Build Plan.
- **§5.4 Round-trip stability.** Recalc the workbook 5 times. Since Sprint 0 writes no formulas, every cell should be invariant across recalcs. **Expected: bit-for-bit identical.** Drift indicates a corrupted cell or hidden formula.
- **§5.5 Stale-reference scan.** N/A this sprint (no cross-tab refs).

### §4.2 — Sprint 0 specific: 2025 anchor read-back (HALT GATE)

Per Principle 23 + §17 calibration targets. Plugin reads each anchor cell from the **Assumptions tab** (cell address determined by the Build Plan XLSX's row layout — plugin resolves the cell at execution time by finding the labeled row) and compares to the locked value. Any deviation outside tolerance → **halt**.

| Input (label on Assumptions col A) | Expected value | Tolerance | Source |
|---|---|---|---|
| `Starting cash EoY 2024 ($mm)` | **5,000** | exact | Q4'25 Earth R225 (rounded up from $4,700mm per Vlad lock) |
| `IPO injection amount ($mm)` | **30,000** | exact | Locked |
| `IPO year` | **2027** | exact | Locked |
| `Mars carve-out floor ($mm/yr)` | **1,000** | exact (Base Case) | Architecture §11.1; MC [500, 2500] |
| `Mars carve-out % of prior-year FCF` | **0.15** | exact (Base Case) | Architecture §11.1; MC [0.03, 0.35] |
| `IRR sigmoid k` | **2** | exact | Architecture §6.3 |
| `Forward IRR weight` | **0.7** | exact | Architecture §5.1 |
| `Vehicle build lead time (yrs)` | **2** | exact | Architecture §6.6 |
| `F9 fleet end-2024 (SoY 2025)` | **28** | exact | Q4'25 Earth R29 (V30.5 had 24 — corrected) |
| `F9 customer launch price 2025 ($mm)` (col D) | **111** | exact | Q4'25 Earth R132 (V30.5 had 67 — corrected) |
| `Starship customer launch price 2025 ($mm)` (col D) | **0** | exact | Pre-commercial; first revenue 2027 |
| `Starship customer launch price 2027 ($mm)` (col F) | **100** | exact | V30.5 trajectory |
| `Starlink BB ARPU 2025 ($/mo)` (col D) | **100** | exact | Q4'25 R454 |
| `Starlink BB ARPU 2030 ($/mo)` (col I) | **75** | exact | Architecture §8.4 trajectory |
| `Starlink DTC ARPU 2025 ($/mo)` (col D) | **16** | exact | Q4'25 R455 |
| `Starlink DTC ARPU 2030 ($/mo)` (col I) | **10** | exact | Architecture §8.4 trajectory |
| `Starshield Reserved % decay rate` | **0.25** | exact | Q4'25 Valuation Inputs R30 (V30.5 had 1.0 — corrected) |
| `Starshield Rev per Gbps ($)` | **164,699** | exact | Q4'25 Earth R120 (V30.5 had 167,421 — corrected) |
| `V2 BB active end-2025 (historical baseline)` | **5,246** | exact | Mach33 hard anchor |
| `V2 DTC active end-2025 (historical baseline)` | **650** | exact | Mach33 hard anchor |
| `Cumulative sats launched end-2024 (base year)` | **7,486** | exact | Q4'25 Earth R41 |
| `Satellite cost per kg (base) ($/kg)` | **650** | exact | Q4'25 + V30.5 match |
| `V2 Mini mass (kg)` | **575** | exact | Q4'25 + V30.5 match |
| `V2 Mini BB Gbps per sat` | **96** | exact | Disclosed |
| `ODC compute power per sat (kW)` | **140** | exact | V30.5 V2 Compute config; Vlad-confirmed |
| `Pr(A) credence on Model A` | **0.6** | exact | Sprint 3.5 default |
| `ODC design life (yrs)` | **5** | exact | Architecture §5.1 |
| `Mars/Moon R&D 2025 ($mm)` (col D) | **700** | ±$5 | Q4'25 Earth R174 (V30.5 had 500 — corrected) |
| `Starlink R&D start %` | **0.08** | exact | Architecture §12.1 |
| `Customer Launch R&D start %` | **0.25** | exact | Architecture §12.1 |
| `ODC R&D start %` | **0.30** | exact | Architecture §12.1 |
| `AI Stack R&D start %` | **0.15** | exact | Architecture §12.1 |
| `EchoStar spectrum CapEx 2025 ($mm)` (col D) | **5,000** | exact | Refine Spec 03 §5 |
| `EchoStar spectrum CapEx 2026 ($mm)` (col E) | **8,000** | exact | Refine Spec 03 §5 |
| `EchoStar spectrum useful life (yrs)` | **15** | exact | Refine Spec 03 §5 |
| `Tax rate` | **0.21** | exact | Standard |
| `Group WACC` | **0.10** | exact | Architecture §14.1 |
| `Terminal growth g` | **0.025** | exact | Architecture §14.1 |
| **Standards (every active tab):** | | | |
| Row 4 D column on each tab 1–13 | **2025** | exact | Architecture §2 |
| Row 4 AC column on each tab 1–13 | **2050** | exact | Architecture §2 |
| Row 5 D column on each tab 1–13 | **0** | exact | Architecture §2 |
| Row 5 AC column on each tab 1–13 | **25** | exact | Architecture §2 |

### §4.3 — Halt conditions (quantitative)

Per Rule 15. Plugin halts and reports if:

- **Any anchor in §4.2 deviates from expected value beyond tolerance.**
- **Any cell in row 4 on tabs 1–13 ≠ literal integer in {2025…2050}.**
- **Any cell in row 5 on tabs 1–13 ≠ literal integer in {0…25}.**
- **Any formula present on the Assumptions tab** (if Excel auto-converted a typed-in `=` somewhere, halt and rewrite as static value).
- **Any input from the Build Plan missing an MC range** when its distribution ≠ `fixed`.
- **Any sheet name deviates** from §3.1 exact list.
- **Any error value** (`#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`) anywhere in the workbook.

No "proceed and document." Halt is mandatory.

### §4.4 — Verification log (plugin produces)

After §4.1–§4.3 pass, plugin produces a log block in the chat:

```
Sprint 0 verification log
=========================

Workbook: /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/SpaceX_Model_v2_S0.xlsx

Tabs created (14):
  [list with cell counts per tab]

Year header + offset (rows 4 & 5):
  Tab 1 Assumptions:        OK (D4=2025, AC4=2050, D5=0, AC5=25)
  Tab 2 Allocator:           OK
  [... through Tab 13 Valuation ...]

Assumptions tab content:
  Rows written: ~290
  Sections: Global, Allocator, Capacity, Customer Launch, Starlink, ODC,
            AI Stack, Lunar Mars, OpEx, CapEx, Valuation
  Inputs with MC range: [count]
  Inputs with fixed distribution: [count]

§4.2 anchor read-back:
  [each row of the table with expected vs actual]

§4.1 universal checks:
  - Error scan: 0 / 0 / 0 / 0 / 0 / 0 / 0 (REF/VALUE/DIV0/NAME/NUM/NULL/NA)
  - Round-trip stability: 5 recalcs, bit-for-bit identical: PASS
  - Stale-ref scan: N/A this sprint
  - Conservation block: N/A this sprint

Flags / open questions: [any items needing Vlad attention]

Status: PASS → write Claude Log entry → save.
```

If any check fails, plugin reports the failure mode + the offending cell(s) and halts.

---

## §5 — Claude Log entry

Plugin appends to `Claude Log` row 2 (after §4 passes):

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| 2026-MM-DD *(today)* | 0 | Assumptions (built), Allocator + Launch Capacity + Customer Launch + Starlink + Starlink Capacity + ODC + AI Stack + Lunar Mars + Group P&L + OpEx + CapEx + Valuation (year header + offset row staged), Claude Log (created) | Built v2 baseline workbook from scratch. Created 14 tabs in locked sheet order per Architecture §1. Year header (D=2025…AC=2050) and year-offset row (D=0…AC=25) staged as literal integers on every year-column tab. Assumptions tab populated from Build Plan XLSX — ~290 rows across 11 sections (Global / Allocator / Capacity / Customer Launch / Starlink / ODC / AI Stack / Lunar Mars / OpEx / CapEx / Valuation). Every input has Base Case + MC range + distribution + notes per Principle 18. All §4.2 anchors verified at locked values (starting cash $5B, F9 fleet 28, F9 price $111M, Mars/Moon R&D $700M, Starshield decay 0.25, Starshield rev/Gbps $164,699). Six Q4'25 corrections vs V30.5 applied. | Demand Curves tab not yet imported — Sprint 4 (Starlink) decides whether to carry V9 content. | Sprint 1: Allocator skeleton + module shells (IN/OUT contract by label, module bodies empty). |

---

## §6 — Don't touch (out of scope)

- No formulas anywhere except literal integers on rows 4 and 5.
- No cross-tab references.
- No module body content. Tabs 2–13 are skeletons only — sheet exists, year header + year-offset row written, otherwise blank.
- No Allocator IN/OUT contract row labels (Sprint 1).
- No conservation block (Sprint 9).
- No Demand Curves tab (Sprint 4 decision).
- No styling beyond: Build Plan-specified section/subsection fills on Assumptions, MC yellow highlight on AG–AJ, italic memos, bold + bottom border on row 4, light grey fill on row 5. No charts, no conditional formatting, no data validation, no comments/notes objects, no freeze panes (Sprint 0.5 patch if Vlad wants them).

---

## §7 — Open thread (post-sprint considerations)

### §7.1 — Demand Curves tab

Per Architecture §1 row 14 and §18.5: V9 carries the Demand Curves tab as source for Starlink bandwidth demand. Sprint 4 (Starlink) decides:
(a) Import V9's Demand Curves tab as-is into the rebuild workbook.
(b) Replace with sub-derivation inside the Starlink tab.
(c) Drop entirely (if Starlink revenue is fully refactored to consume Capacity-tab Gbps).

Sprint 0 leaves the tab out. If (a) wins, Sprint 4 imports + adds year header + offset row then.

### §7.2 — Build Plan XLSX completeness audit

Plugin may discover during execution that the Build Plan XLSX is missing an input the constitutional docs imply (e.g. ODC internal vs external compute split year-row called for in Architecture §7.3 — Assumptions Tab Spec §6.2 flags this as new). If so:
- Plugin halts.
- Reports the missing input.
- Spec author either adds the input to the Build Plan and re-runs Sprint 0, or marks it deferred.

No silent input invention by the plugin. Per Rule 9 (when in doubt, ask).

### §7.3 — Inputs flagged for Vlad-level confirmation pre-execution

Per Assumptions Tab Spec §6:
- Mars carve-out % Base Case 15% (MC 3–35%) — confirm or push.
- ODC internal vs external compute split trajectory — confirm or push.
- AI Stack product ramps (Cursor / Grok consumer / Grok enterprise API) — confirm or push.
- Starship customer launch price $100M from 2027, −8%/yr decline — confirm or push.

If Vlad wants any of these reframed, edit the Build Plan XLSX before Sprint 0 fires. Otherwise plugin executes as-is.

### §7.4 — Visual styling

Build Plan-specified section/subsection fills, MC yellow highlight, italic memos, bold row 4, grey row 5. Anything more elaborate (column-width tuning, freeze panes at row 5, conditional formatting on out-of-range MC bounds, custom number formats) is out of scope for Sprint 0 but available as a Sprint 0.5 patch.

---

## §8 — Execution sequence (plugin runs in this order)

Per Rule 7 (deterministic order):

1. **Save-as** the blank workbook to `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/SpaceX_Model_v2_S0.xlsx`.
2. **Pre-flight checks** (§3.0): confirm blank workbook, Build Plan XLSX readable, target path writable, constitutional docs read.
3. **Rename default sheet** to `Assumptions`. Create the remaining 13 tabs in §3.1 order. Verify all 14 tab names are exact.
4. **Write row 4 year header** (literal integers 2025–2050) on tabs 1–13. One write per tab. Apply bold + bottom border.
5. **Write row 5 year-offset helper** (literal integers 0–25) on tabs 1–13. One write per tab. Apply light grey fill.
6. **Open `04_Assumptions_Tab_Build_Plan.xlsx`** and walk row-by-row, writing to `Assumptions` tab per §3.3. Pace section by section; after each of the 11 sections, do a quick read-back of the last input row.
7. **Halt during §3.3 if** any input missing MC range, any unrecognised distribution type, or any column-A label collision.
8. **Write Claude Log header row** (§3.4).
9. **Save the workbook.**
10. **Run §4 verification gate** against the saved file. Halt on any failure.
11. **Write Claude Log Sprint 0 entry** (§5).
12. **Save the workbook again** (final state).
13. **Produce verification log** in chat (§4.4 format).

---

# Begin execution

Acknowledge the constitutional doc reads, walk through the §1 Rule Compliance Preamble box by box, run §3.0 pre-flight, then execute §8 step by step. Do not write a single cell until the preamble is confirmed and pre-flight passes. Halt and ask if anything is unclear or any §4.3 condition fires.
