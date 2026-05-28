# Sprint 7 — Lunar Mars module (strategic carve-out, NOT in IRR queue) + BV engine + kg reservation off-the-top + Allocator §3 carve-out section + 2 BV memo rows

**Day budget**: 1 day (per Sprint Roadmap §1)
**Owner**: Lunar Mars sprint (this chat = spec author; separate fresh chat will execute as plugin)
**Status**: Spec authoring; constitutional docs + Sprint 0/1/5 read; seven architectural locks captured via AskUserQuestion 2026-05-20.

---

## §0 — Constitutional references

- `01_Lessons_Learned.md` — load-bearing principles for Sprint 7:
  - **Principle 1** (postponed architectural decisions create retrofit cascades) — Sprint 7 locks Mars carve-out architecture day-one; no later sprint retrofits the queue gate or BV engine.
  - **Principle 2** (per-sat marginal IRR) — Lunar Mars EXEMPT. No IRR engine; R207/R208/R209 = hardcoded 0. Architecture §11.6 defers per-mission IRR explicitly.
  - **Principle 3** (Allocator IN/OUT by label, not row) — Sprint 7 reads Allocator §3 carve-out + Assumptions §8 by INDEX/MATCH on canonical labels.
  - **Principle 4** (queue gate reserves non-module claims before module CapEx) — Mars carve-out is the LOAD-BEARING non-module claim Sprint 7 publishes for Sprint 10's queue gate.
  - **Principle 8** (vending-machine framing — module COGS direct production only) — NO R&D / SG&A / overhead / taxes on Lunar Mars tab. Mars/Moon R&D flows through OpEx tab (Sprint 8 owns).
  - **Principle 11** (zero OFFSET formulas) — all year-row lookbacks use `INDEX(range, 1, col_num)` patterns.
  - **Principle 12 + Rule 23** (anchor-and-offset for ramps) — every ramp references `$D$anchor + E$5 offset`. Year-chained logic (BV running sum, active labour fleet retirement cohort) flagged inline as Rule 23 exceptions.
  - **Principle 18** (MC ranges at input creation) — two new year-row Assumptions amendments include MC ranges in column AG:AJ.
  - **Principle 21 / Rule 22** (stale-ref scan) — Sprint 7 §4.5 scans Allocator §3 + Lunar Mars OUT block + BV memo labels.
  - **Principle 22** (within-year cycle deliberate) — Sprint 7 introduces ONE cross-year dependency: Mars carve-out reads prior-year Group FCF via Allocator (Sprint 1 placeholder = 0 until Sprint 10 lights up Cash Pool Tracker). Within-year cycle dormant in Sprint 7. Iterative calc remains ON workbook-wide (100 iter / 0.001 tol).
  - **Principle 23** (calibration targets) — Sprint 7 calibration is trivial: Lunar Mars revenue 2025 = $0 exact; Mission CapEx 2025 = $0 exact; Lunar BV 2025 = $0 exact; Mars BV 2025 = $0 exact.

- `02_Architecture_and_Methodology.md`:
  - **§1** (tab inventory) — Lunar Mars = tab #9.
  - **§3** (module P&L vending-machine framing) — Lunar Mars's pre-revenue divergence documented in Architecture §11 framing note.
  - **§4.1** (Allocator IN block) — Lunar Mars's IN block hardcoded zeros (Sprint 1 implementation reads via INDEX/MATCH against Allocator R87/R137 = 0 placeholders).
  - **§4.2** (Allocator OUT — standard 11-row + 2 BV memo rows) — Sprint 7 overwrites Sprint 1 literal-0 placeholders.
  - **§5** (per-module IRR) — N/A for Lunar Mars (R207/R208/R209 hardcoded `=0`).
  - **§6.2** (queue gate — Mars carve-out reserved BEFORE IRR queue) — Sprint 7 publishes the canonical carve-out year-row on Allocator §3 for Sprint 10 to consume.
  - **§6.4** (kg queue — Lunar Mars kg reserved off-the-top) — Sprint 7 publishes Lunar Mars kg reservation on Lunar Mars tab for Sprint 10 to consume.
  - **§11** (full Lunar Mars architecture) — §11.1 strategic carve-out, §11.2 deployment, §11.3 kg reservation, §11.4 BV engine, §11.5 P&L, §11.6 Allocator OUT.
  - **§14.2** (Valuation SoTP terminal) — Sprint 11 reads R211/R212 BV memo rows for `1.5 × Lunar+Mars BV at 2050` anchor.
  - **§17** (calibration) — Lunar Mars revenue 2025 = $0 exact.

- `03_Sprint_Roadmap_and_Verification.md`:
  - **§3 Sprint 7** scope + acceptance criteria.
  - **§6.6 Sprint 7 calibration** — Lunar Mars revenue $0, Mission CapEx 2025 $0, Lunar BV 2025 $0, Mars BV 2025 $0 (all exact). Mars/Moon R&D $700M 2025 NOT on Lunar Mars tab — flows OpEx (Sprint 8).
  - **§5 universal verification protocol** — #REF/#NUM scan, conservation block (trivial in Sprint 7 — pre-Sprint-9), edge-year reads (D/I/S/AC), round-trip stability, stale-ref scan, Claude Log entry.

- `Model Execution Rules.md` — Rule Compliance Preamble below (§1).

- `2025 Anchors from Q4_25.md` — §5 Mars & Moon 2025 anchors: physical launches 2025 = 0, Mars & Moon mission cash spend 2025 = $0, Mars & Moon R&D 2025 = $697.54M ≈ $700M anchor (lives on OpEx tab Sprint 8, NOT Lunar Mars).

---

## §1 — Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md` and the four constitutional docs. Confirmed before execution:

- [x] **Rule 1** (one concept per write) — §3 structure separates Assumptions amendments (§3.1), Allocator §3 carve-out section (§3.2), Lunar Mars tab body cell-by-cell (§3.3), Allocator OUT contract overwrite (§3.4). Each cell-block is a discrete write per Rule 1; labels, formulas, formats split.
- [x] **Rule 3 / 23** (formula pattern) — every deterministic ramp uses anchor-and-offset (`$D$anchor + E$5`). Year-chained Rule 23 exceptions flagged inline with one-line justification: (a) Active labour fleet running sum (§3.3.6); (b) Accumulated book value running sum (§3.3.7); (c) Labour cohort retirement lookback (§3.3.6 — uses `IF(E$5 - useful_life < 0, 0, INDEX(...))` guard for INDEX col_num<1 spill per memory `feedback-index-col-zero-spills`).
- [x] **Rule 4** (verification gate) — every section in §3 has explicit read-back cells (D / I / S / AC) + expected values. §4.1 universal #REF scan, §4.2 edge-year reads on Lunar Mars tab body, §4.3 conservation trivial check, §4.4 round-trip stability, §4.5 stale-ref scan, §4.6 Sprint 7 calibration table.
- [x] **Rule 6** (inline formulas) — every cell write in §3 specified with the full Excel formula. No "see Architecture §11.4" hand-waves. INDEX/MATCH calls written with exact canonical labels (case-sensitive verbatim).
- [x] **Rule 10** (no row insertions) — confirmed: §3.1 Assumptions amendments APPEND below Sprint 0's last-used row (R230 per Sprint 5 §3.2 amendment register; pre-flight MATCH-probes last-used row before drafting cell refs). §3.2 Allocator §3 fills the RESERVED rows 32-37 left blank by Sprint 1. §3.3 Lunar Mars body fills the BLANK rows 11-199 left empty by Sprint 1. §3.4 OVERWRITES Sprint 1's literal-0 placeholders on Lunar Mars rows 200-212 (no insertion).
- [x] **Rule 11** (touch points) — every new line item on Lunar Mars tab + Allocator §3 lists its SUM range / aggregator / conservation check / downstream consumer in §3 inline. The 7 canonical Sprint 7 publishes (Total Revenue R201, Module EBITDA R202, Module FCF R204, Module CapEx R205, Capacity Demand R210, Lunar BV R211, Mars BV R212) enumerate their downstream readers in §3.4.
- [x] **Rule 12** (label-based cross-tab refs) — every cross-tab read uses `INDEX(Tab!D:D, MATCH("Canonical Label", Tab!$A:$A, 0))`. Zero hardcoded `=Tab!Dxxx` refs anywhere. Allocator §3 carve-out cash → Lunar Mars module via label. Lunar Mars OUT → Sprint 8 / Sprint 11 via label.
- [x] **Rule 13** (vending-machine test) — Lunar Mars tab gets NO R&D / SG&A / overhead / taxes added. Lunar Mars is structurally pre-revenue (Revenue = 0 every year), so the vending-machine test reduces to: Module COGS = mission ops (% of CapEx) + BV depreciation; Module EBITDA = Gross Profit = negative (operating costs only); Module CapEx = carve-out cash deployed. Sprint 7 §4 verification confirms NO R&D row on Lunar Mars tab.
- [x] **Rule 14** (no hardcoded constants) — every behaviour input read from Assumptions tab by canonical label. The hardcoded `=0` on IRR rows R207/R208/R209 is a literal-zero placeholder per Architecture §11.6 (per-mission IRR deferred — Vlad lock 2026-05-20), NOT a behaviour constant; the alternative (`=IFERROR(IRR(...), -1)`) is explicitly out of scope. Flagged inline at §3.4 with one-line justification.
- [x] **Rule 15** (sanity check halt thresholds) — §4.6 calibration table specifies quantitative halt thresholds: Lunar Mars revenue 2025 = $0 (any >$0 → halt); Mission CapEx 2025 = $0 (any >$10M → halt); Lunar BV 2025 = $0 (any >$100M → halt); Mars BV 2025 = $0 (any >$100M → halt); 2030+ Mars fleet > 0 sanity (if 2030 Mars surface missions = 0 with non-zero Mars share of carve-out, formula bug → halt).
- [x] **Rule 19** (save-as) — N/A per standing rules locked 2026-05-20: spec does NOT name workbook files; Vlad handles versioning entirely outside the spec. Confirmed in `feedback-no-workbook-names-in-specs` memory.
- [x] **Rule 22** (stale-ref scan) — §4.5 lists three scan checkpoints: (1) Allocator §3 carve-out outputs read by Lunar Mars module via INDEX/MATCH on label; (2) Lunar Mars OUT block (R201-R210 + R211/R212) labels MATCH against Sprint 1's published strings before overwriting; (3) Assumptions §8 amendment dedupe — MATCH probes on each candidate amendment label confirm no existing dupe.

Architecture & Methodology compliance:
- [x] Module P&L follows vending-machine framing (Architecture §3) — Lunar Mars's intentional divergence (pre-revenue throughout; BV-driven valuation; cash CapEx ≠ BV depreciation in COGS) documented in Architecture §11 framing note. Spec §3.3 §3.3.8 Lunar Mars P&L matches: Revenue=0, COGS=ops%+BV depreciation, Module EBITDA = Gross Profit = negative, Module CapEx = carve-out cash deployed, Module FCF = heavily negative.
- [x] Per-sat / per-launch marginal IRR (Architecture §5) — N/A for Lunar Mars (Architecture §11.6 lock). R207/R208/R209 hardcoded `=0`.
- [x] Allocator OUT contract uses canonical 11 labels (Architecture §4.2) — Sprint 7 §3.4 overwrites Sprint 1 placeholders with module-derived values; IRR rows R207/R208/R209 written as literal `=0`; two BV memo rows R211/R212 italic per Rule 17 retain Sprint 1's canonical labels verbatim.
- [x] Year-offset helper row at row 5 + year header at row 4 — Sprint 0 wrote both on Lunar Mars tab; Sprint 7 §3.0 pre-flight confirms.
- [x] ZERO `OFFSET()` formulas — all dynamic ranges use INDEX-based patterns. BV cohort retirement lookback uses `IF(E$5 - useful_life < 1, 0, INDEX($D14:$AC14, 1, E$5 - useful_life + 1))` with explicit INDEX col_num guard per memory `feedback-index-col-zero-spills`.

---

## §1.5 — Pre-execution setup (NO workbook-name confirmation needed)

Per standing rules locked 2026-05-20 (`feedback-no-workbook-names-in-specs`): plugin operates on whatever workbook is open in Vlad's Excel session. Vlad handles versioning. Spec omits all workbook filename references.

Plugin §3.0 pre-flight (described in §3.0 below) confirms:

1. **Tab positions and existence** — exactly 14 tabs in order: `Assumptions`, `Allocator`, `Launch Capacity`, `Customer Launch`, `Starlink`, `Starlink Capacity`, `ODC`, `AI Stack`, `Lunar Mars`, `Group P&L`, `OpEx`, `CapEx`, `Valuation`, `Claude Log`. Plus `Demand Curves` may exist as tab 14 per Sprint 4.5 Patch absorbed into Sprint 5 §3.1 (Demand Curves tab built; Claude Log moves to tab 15 in that case). Per Sprint 5 amendment 1: total tab count = 14 or 15. Sprint 7 doesn't care about Demand Curves position — only confirms `Lunar Mars` is tab named exactly that.

2. **Iterative calc still enabled workbook-wide** — 100 iterations, 0.001 tolerance. Per memory `project-iterative-calc-enabled-2026-05-20`. Sprint 7 introduces ONE cross-year dependency (Mars carve-out reads prior-year Group FCF via Allocator R32-R37 → Sprint 1 placeholder = 0 in 2025 because Group P&L doesn't exist with content until Sprint 9). Within-year cycle dormant. If iterative calc OFF, halt and push back to Vlad.

3. **Sprint 3.6 micro-patch state** — confirm whether Sprint_3.6_Patch_*.md exists in the workspace folder. As of Sprint 7 spec authoring 2026-05-20, NO Sprint 3.6 patch file present. Per memory `project-sprint-3-6-micro-patch-needed`: Customer Launch G16:AC16 returns #N/A from missing Assumptions row `Starship customer launch margin — CAGR (% change/yr from 2027 anchor)`. Sprint 7 doesn't block on Sprint 3.6 (Sprint 7 only writes to Lunar Mars + Allocator §3 + Assumptions amendments). The orphan #N/A error on Customer Launch G16:AC16 remains surfaced through Sprint 7 §4.1 workbook-wide #N/A scan as a PRE-EXISTING inherited error. Plugin documents in Claude Log as inherited from Sprint 5; does not halt Sprint 7 execution.

4. **Sprint 5 canonical labels still resolve (sanity)** — pre-flight runs MATCH probes against:
   - `ODC` tab column A for: `Total Revenue ($mm)` (R201), `Module EBITDA ($mm)` (R202), `Module FCF ($mm)` (R204), `Module CapEx ($mm)` (R205), `Capacity Demand (kg-to-LEO)` (R210). All five must resolve to ODC's published label strings. Mismatch = halt (Sprint 5 may have drifted; Sprint 7 doesn't proceed until restored).
   - `Allocator` tab column A for: `Lunar Mars cash allocation` (R87 per Sprint 1 §3.2.2), `Lunar Mars kg allocation` (R137 per Sprint 1 §3.2.2). Both must resolve to literal-0 placeholders. Mismatch = halt.
   - `Lunar Mars` tab column A for: `INPUTS FROM CENTRAL ALLOCATOR` (R7), `Capital Allocation ($mm)` (R8), `Starship Capacity Allocation (kg-to-LEO)` (R9), `Total Capital Available ($mm)` (R10), `CENTRAL ALLOCATOR OUTPUTS` (R200), and all 10 OUT rows R201-R210 + R211 / R212 BV memo labels. Match verbatim (case-sensitive) against Sprint 1 §3.3.2 published strings. Mismatch = halt.

5. **Vlad locked seven architectural decisions 2026-05-20** (recorded in §9 amendment log):
   - Mars carve-out Base Case: 15% / $1,000M floor (Sprint 0 R12/R13 unchanged); Lunar/Moon emphasis reflected via Lunar/Mars share trajectory below.
   - Lunar/Mars share trajectory: 100% Lunar pre-2028, **70% Lunar / 30% Mars from 2028 onwards** (Vlad: shifting focus to Moon over Mars vs first iteration). Sprint 7 writes Sprint 0 R227 (Lunar share) + R228 (Mars share = 1 − R227) year-row values accordingly.
   - Labour share trajectory: year-row ramp D=2025 0.3 → AC=2050 0.7 (MC triangle-yearrow). Sprint 7 appends TWO new Assumptions year-rows (`Lunar labour share of surface payload — year-row` + `Mars labour share of surface payload — year-row`); R218/R222 single-value 0.3 stays as orphan diagnostic.
   - Per-mission IRR engine: deferred. R207/R208/R209 hardcoded literal `=0`.
   - BV memo labels: Sprint 1 verbatim — `Lunar Accumulated Book Value ($mm)` (R211) + `Mars Accumulated Book Value ($mm)` (R212), italic per Rule 17.
   - OpEx Mars/Moon R&D ownership: Sprint 8 owns. Sprint 7 writes NO R&D row on Lunar Mars tab.
   - Hardware $/kg: Sprint 0 R225 year-row `Hardware replacement cost factor ($/kg landed) — declining` reads by canonical label. NO Assumptions amendment.

---

## §2 — Framing

### §2.1 What this sprint does

Sprint 7 builds the **Lunar Mars module tab body** (rows 11-199 on Lunar Mars tab) + the **Allocator §3 Mars/Moon strategic carve-out section** (Allocator rows 32-37 reserved by Sprint 1 §3.2 layout) + **two new Assumptions year-row amendments** (Lunar / Mars labour share trajectories) + **Sprint 7 fills in Sprint 0 stub year-rows** (R227 Lunar share, R228 Mars share = 1−R227). Sprint 7 publishes 7 canonical labels for downstream consumers (5 standard Allocator OUT + 2 BV memos).

### §2.2 What this sprint does NOT do

- **No IRR engine on Lunar Mars** (Architecture §11.6 lock — per-mission marginal IRR deferred; Vlad: "we can change this later"). R207/R208/R209 hardcoded `=0`.
- **No R&D / SG&A / overhead / taxes** on Lunar Mars tab (Rule 13 — vending-machine test). Mars/Moon R&D $700M 2025 flows through OpEx tab (Sprint 8 owns).
- **No Allocator brain light-up** — Sprint 10 lights up Cash Pool Tracker, Queue Gate, sigmoid blends, vehicle build claim. Sprint 7 only writes the carve-out section that Sprint 10 reads.
- **No Lunar Mars allocator IN row activation** — Sprint 1 placed `=INDEX(Allocator!D:D, MATCH("Lunar Mars cash allocation", Allocator!$A:$A, 0))` on Lunar Mars R8 reading Allocator R87 = literal 0. Per Architecture §4.1: "Lunar Mars's Allocator IN block has hardcoded zeros — Lunar Mars is outside the IRR queue. Its actual cash + kg arrive via the Mars carve-out off the top." Sprint 7 reads carve-out cash from Allocator §3 directly (NOT from the IN block); confirms IN block resolves to 0 in §3.0 pre-flight.
- **No Group P&L / Group FCF prior-year wiring** — Sprint 9 builds Group P&L. Sprint 7's Allocator §3 carve-out formula reads `INDEX('Group P&L'!D:D, MATCH("GROUP FCF", 'Group P&L'!$A:$A, 0))` lookback by one year, which returns 0 / #N/A until Sprint 9 lights up. Sprint 7 wraps with `IFERROR(..., 0)` so the lookback fails gracefully and the carve-out hits its floor ($1,000M from 2025 onwards). When Sprint 9 lands, the formula activates without needing rewire.

### §2.3 Why this matters

Lunar Mars is **architecturally distinct from the four IRR-queue modules** (Customer Launch, Starlink, ODC, AI Stack):
- Pre-revenue throughout 2025-2050 (Revenue = $0 every year exact)
- NOT in IRR queue (no IRR engine; strategic carve-out off-the-top per Architecture §6.2 + §11.1)
- Cash drives deployment (NOT IRR-driven); ships deployed = carve-out share / per-ship cost
- BV is the load-bearing valuation measure (Sprint 11 Valuation reads R211/R212 × 1.5 multiplier for SoTP terminal anchor per Architecture §14.2)
- Kg reserved off-the-top before Sprint 10 kg queue runs (per Architecture §6.4)

Per Principle 4 (cash queue reserves non-module claims before module CapEx): Mars carve-out is a LOAD-BEARING non-module cash claim that MUST be reserved before Sprint 10's IRR sigmoid blend allocates the remaining cash pool. Sprint 7 publishes the canonical carve-out year-row on Allocator §3 that Sprint 10's Queue Gate (Allocator §2 rows 18-29) will subtract.

### §2.4 Cross-year dependency introduced

Sprint 7 introduces ONE new cross-year dependency:
- `Mars/Moon strategic carve-out ($mm/yr)` reads prior-year Group FCF (via Allocator §3 formula)
- Sprint 1 placeholder: Group P&L doesn't exist with FCF yet → IFERROR returns 0 → carve-out hits floor $1,000M from 2025 onwards
- Sprint 9 lights up: Group FCF starts producing real numbers → carve-out becomes `MAX($1,000M, prior-year FCF × 15%)`

Per Principle 22 (within-year cycle deliberate + iterative calc bistability): Mars carve-out using PRIOR-year FCF (not current-year) breaks circularity. The cross-year reference is safe under iterative calc; convergence trivially holds (no within-year feedback loop).

Within-year cycle DORMANT in Sprint 7 — no feedback into the same year's computation. Iterative calc remains ON workbook-wide (100 iter / 0.001 tol per memory `project-iterative-calc-enabled-2026-05-20`) because prior sprints' cycles are still live (e.g., Sprint 4's Starlink ↔ Starlink Capacity %).

---

## §3 — Scope

### §3.0 — Pre-flight checks (run BEFORE any §3.x writes)

Plugin executes these checks in order. Halt on any miss. No writes proceed until all pass.

1. **Tab existence + position** — confirm `Lunar Mars` tab exists at position #9 (or #9 if Demand Curves at #14 with Claude Log at #15). Confirm `Allocator` tab at position #2, `Assumptions` at #1, `Launch Capacity` at #3.

2. **Year header + offset row on Lunar Mars tab** — confirm:
   - `Lunar Mars!D4 = 2025`, `Lunar Mars!E4 = 2026`, ..., `Lunar Mars!AC4 = 2050` (Sprint 0 §3.8 wrote integers; spot-check D4, I4=2030, S4=2040, AC4=2050).
   - `Lunar Mars!D5 = 0`, `Lunar Mars!E5 = 1`, ..., `Lunar Mars!AC5 = 25` (Sprint 0; spot-check D5, I5=5, S5=15, AC5=25).
   - Halt if any cell missing or non-integer.

3. **Lunar Mars IN block (Sprint 1) intact** — read:
   - `Lunar Mars!A7 = "INPUTS FROM CENTRAL ALLOCATOR"` (exact string)
   - `Lunar Mars!A8 = "Capital Allocation ($mm)"`
   - `Lunar Mars!A9 = "Starship Capacity Allocation (kg-to-LEO)"`
   - `Lunar Mars!A10 = "Total Capital Available ($mm)"`
   - `Lunar Mars!D8 = formula =INDEX(Allocator!D:D, MATCH("Lunar Mars cash allocation", Allocator!$A:$A, 0))`
   - `Lunar Mars!D8` evaluated value = 0 (Sprint 1 placeholder upstream)
   - Same for D9 (kg allocation = 0), D10 (Total Capital Available = D8 = 0).
   - Halt if any cell missing, label drifted, or formula broken.

4. **Lunar Mars OUT block (Sprint 1) intact** — read:
   - `Lunar Mars!A200 = "CENTRAL ALLOCATOR OUTPUTS"`
   - `Lunar Mars!A201 = "Total Revenue ($mm)"`
   - `Lunar Mars!A202 = "Module EBITDA ($mm)"`
   - `Lunar Mars!A203 = "Module EBITDA Margin %"`
   - `Lunar Mars!A204 = "Module FCF ($mm)"`
   - `Lunar Mars!A205 = "Module CapEx ($mm)"`
   - `Lunar Mars!A206 = "Capital deployed ($mm)"`
   - `Lunar Mars!A207 = "Spot IRR"`
   - `Lunar Mars!A208 = "Forward IRR (Y+2)"`
   - `Lunar Mars!A209 = "Blended IRR"`
   - `Lunar Mars!A210 = "Capacity Demand (kg-to-LEO)"`
   - `Lunar Mars!A211 = "Lunar Accumulated Book Value ($mm)"` (italic per Rule 17)
   - `Lunar Mars!A212 = "Mars Accumulated Book Value ($mm)"` (italic per Rule 17)
   - `Lunar Mars!D201:AC212` evaluated values all = 0 (Sprint 1 placeholders)
   - Halt if any label drifted or any value non-zero.

5. **Allocator §3 reserved rows blank** — confirm:
   - `Allocator!A31 = "§3 MARS/MOON STRATEGIC CARVE-OUT"` (Sprint 1 §3.2.1 wrote section header)
   - `Allocator!A32:A37` = all blank (Sprint 1 left reserved for Sprint 7)
   - `Allocator!D32:AC37` = all blank
   - Halt if any cell non-blank.

6. **Sprint 5 canonical labels resolve on ODC tab (sanity)** — MATCH probes:
   - `MATCH("Total Revenue ($mm)", ODC!$A:$A, 0)` resolves (returns row 201 expected)
   - `MATCH("Module EBITDA ($mm)", ODC!$A:$A, 0)` resolves (row 202)
   - `MATCH("Module FCF ($mm)", ODC!$A:$A, 0)` resolves (row 204)
   - `MATCH("Module CapEx ($mm)", ODC!$A:$A, 0)` resolves (row 205)
   - `MATCH("Capacity Demand (kg-to-LEO)", ODC!$A:$A, 0)` resolves (row 210)
   - Halt if any MATCH returns #N/A — Sprint 5 may have drifted; Sprint 7 doesn't restore.

7. **Assumptions §8 Lunar Mars inputs exist** — MATCH probes:
   - `MATCH("Capital lifetime — book value straight-line depreciation (years)", Assumptions!$A:$A, 0)` → expect Sprint 0 R205
   - `MATCH("Labour unit mass (kg)", Assumptions!$A:$A, 0)` → R209
   - `MATCH("Labour unit base hourly output ($/hr; burdened $22/0.7)", Assumptions!$A:$A, 0)` → R210
   - `MATCH("Labour unit daily working hours", Assumptions!$A:$A, 0)` → R211
   - `MATCH("Labour unit productivity factor vs human baseline", Assumptions!$A:$A, 0)` → R212
   - `MATCH("Labour unit productivity learning rate (%/yr)", Assumptions!$A:$A, 0)` → R213
   - `MATCH("Labour unit operational lifespan on surface (years)", Assumptions!$A:$A, 0)` → R214
   - `MATCH("Module operating cost — Lunar (% of Lunar CapEx)", Assumptions!$A:$A, 0)` → R206
   - `MATCH("Module operating cost — Mars (% of Mars CapEx)", Assumptions!$A:$A, 0)` → R207
   - `MATCH("Lunar fuel depot multiplier per outbound Starship", Assumptions!$A:$A, 0)` → R216
   - `MATCH("Lunar payload per surface-landed Starship (kg)", Assumptions!$A:$A, 0)` → R217
   - `MATCH("Mars fuel depot multiplier per outbound Starship", Assumptions!$A:$A, 0)` → R220
   - `MATCH("Mars payload per surface-landed Starship (kg)", Assumptions!$A:$A, 0)` → R221
   - `MATCH("Hardware replacement cost factor ($/kg landed) — declining", Assumptions!$A:$A, 0)` → R225
   - `MATCH("Lunar share of Mars/Moon carve-out cash — year-row", Assumptions!$A:$A, 0)` → R227
   - `MATCH("Mars share of carve-out cash — year-row", Assumptions!$A:$A, 0)` → R228
   - `MATCH("Mars carve-out % of prior-year Group FCF", Assumptions!$A:$A, 0)` → R12
   - `MATCH("Mars carve-out floor ($mm/yr)", Assumptions!$A:$A, 0)` → R13
   - `MATCH("Mars carve-out uses prior-year FCF (0/1)", Assumptions!$A:$A, 0)` → R14
   - Halt on any #N/A — Sprint 0 label drift; Sprint 7 doesn't proceed.

8. **Dedupe check on Sprint 7 candidate amendments** — MATCH probes to confirm new labels DO NOT exist yet:
   - `MATCH("Lunar labour share of surface payload — year-row", Assumptions!$A:$A, 0)` → MUST return #N/A (will be added in §3.1)
   - `MATCH("Mars labour share of surface payload — year-row", Assumptions!$A:$A, 0)` → MUST return #N/A
   - If either returns a row number (dupe), halt and report — investigate prior sprint added it.

9. **Iterative calc setting** — confirm 100 iterations / 0.001 max change. Halt if OFF or different values.

10. **Find Assumptions tab last-used row** — `=COUNTA(Assumptions!$A:$A)` or equivalent. Sprint 0 ended at R301; Sprint 5 §3.2 added 8 amendments (R302-R309); Sprint 5 §3.2.c/d may have added 3+3 more. Plugin records the actual last-used row N; Sprint 7 §3.1 appends two new rows at N+1, N+2.

After all 10 pre-flight checks pass, plugin proceeds to §3.1.

---

### §3.1 — Assumptions tab amendments (append TWO new year-row rows below last-used row)

Per Rule 10 (no row insertions). Plugin appends below Sprint 0's + Sprint 5's last-used row (call it row `N` from §3.0 step 10).

#### §3.1.a — `Lunar labour share of surface payload — year-row`

Append at row `N+1`. Columns:

- **A** (label): `Lunar labour share of surface payload — year-row`
- **B**: blank (year-row input; not single-value)
- **C** (notes): `Fraction of Lunar surface payload allocated to labour units vs hardware. Year-row ramp reflects tech-stack maturity. Sprint 7 amends Sprint 0 R218 single-value 0.3 into year-row 0.3 → 0.7 per Vlad lock 2026-05-20. R218 becomes orphan diagnostic; reads in §3.3 use this new year-row.`
- **D:AC** (year-row values): linear ramp from 0.3 (2025) to 0.7 (2050). 25-step linear interpolation:
  - D=2025: 0.3
  - E=2026: 0.3 + (0.7−0.3) × 1/25 = 0.316
  - F=2027: 0.3 + (0.4) × 2/25 = 0.332
  - G=2028: 0.348
  - H=2029: 0.364
  - I=2030: 0.380
  - J=2031: 0.396
  - K=2032: 0.412
  - L=2033: 0.428
  - M=2034: 0.444
  - N=2035: 0.460
  - O=2036: 0.476
  - P=2037: 0.492
  - Q=2038: 0.508
  - R=2039: 0.524
  - S=2040: 0.540
  - T=2041: 0.556
  - U=2042: 0.572
  - V=2043: 0.588
  - W=2044: 0.604
  - X=2045: 0.620
  - Y=2046: 0.636
  - Z=2047: 0.652
  - AA=2048: 0.668
  - AB=2049: 0.684
  - AC=2050: 0.700
- **AG** (MC Min): 0.1
- **AH** (MC Max): 0.7 (anchored at AC value as central tendency upper)
- **AI** (MC Distribution): `triangle-yearrow`
- **AJ** (MC notes): `Wide MC — labour-share trajectory deeply uncertain. Early years (2025-2030) labour-share could realistically range [0.1, 0.5]; late years (2045-2050) [0.4, 0.85]. Triangle-yearrow samples multiplier on entire row.`

**Plugin write structure (Rule 1)**:
1. Write column A label at row `N+1` (one tool call).
2. Write column C notes (one tool call).
3. Write D:AC year-row values (one tool call — single-row block of 26 cells, hardcoded numerics).
4. Write AG:AJ MC fields (one tool call — single-row block of 4 cells).
5. Apply number format `0.000` to D:AC (3-decimal precision for share values).

**Verification read-back**:
- A{N+1} = exact label string above.
- D{N+1} = 0.3, I{N+1} = 0.380, S{N+1} = 0.540, AC{N+1} = 0.700 (edge years per Rule 16).
- AG{N+1} = 0.1, AH{N+1} = 0.7, AI{N+1} = `triangle-yearrow`.
- Halt on any mismatch.

#### §3.1.b — `Mars labour share of surface payload — year-row`

Append at row `N+2`. Same structure as §3.1.a (year-row 0.3 → 0.7 linear, same MC). Note in C: `Same trajectory as Lunar share — Mars payload mix mirrors Lunar maturity ramp. Sprint 7 amends Sprint 0 R222 single-value 0.3 into year-row per Vlad lock 2026-05-20.`

Identical column-by-column values to §3.1.a.

**Verification read-back**: same pattern as §3.1.a, applied to row `N+2`.

#### §3.1.c — Fill in Sprint 0 stub year-rows R227 + R228

Sprint 0 §8 R227 + R228 were stubbed as year-rows with no D:AC values (Vlad to tune). Sprint 7 writes them now per Vlad lock 2026-05-20 (70/30 Lunar-heavy from 2028).

**R227 `Lunar share of Mars/Moon carve-out cash — year-row`**:
- D:G (2025-2028): write hardcoded `1.0`, `1.0`, `1.0`, `1.0` — 100% Lunar pre-Mars-window-open
  - Wait — Vlad locked: "100% Lunar pre-2028, 70/30 Lunar-heavy from 2028". So 2028 starts the 70/30 split.
- Corrected: D=2025: 1.0, E=2026: 1.0, F=2027: 1.0 (pre-2028 = 100% Lunar); G=2028 onwards: 0.7
- Full row:
  - D=2025: 1.0
  - E=2026: 1.0
  - F=2027: 1.0
  - G=2028: 0.7
  - H=2029: 0.7
  - I=2030: 0.7
  - J=2031: 0.7
  - K=2032: 0.7
  - L=2033: 0.7
  - M=2034: 0.7
  - N=2035: 0.7
  - O=2036: 0.7
  - P=2037: 0.7
  - Q=2038: 0.7
  - R=2039: 0.7
  - S=2040: 0.7
  - T=2041: 0.7
  - U=2042: 0.7
  - V=2043: 0.7
  - W=2044: 0.7
  - X=2045: 0.7
  - Y=2046: 0.7
  - Z=2047: 0.7
  - AA=2048: 0.7
  - AB=2049: 0.7
  - AC=2050: 0.7
- AG/AH/AI/AJ (Sprint 0 left blank since stub; Sprint 7 confirms `triangle-yearrow` from Sprint 0 spec; AG=0.4 / AH=1.0 / AI=`triangle-yearrow` / AJ=`Wide — Vlad: shifting focus to Moon over Mars vs first iteration. MC range reflects uncertainty on continuous Lunar emphasis.`)
- Number format `0.0%` on D:AC (percentage display since this is a share).

**R228 `Mars share of carve-out cash — year-row`**:
- Per Sprint 0 notes: `Derived = 1 − Lunar share. fixed-yearrow.`
- Sprint 7 writes formula `=1 - INDEX($D227:$AC227, 1, E$5+1)` ... wait — Sprint 0 R227 / R228 are at physical rows 227 / 228 on Assumptions. Direct cross-row references on the same tab are fine.
- Simpler: D228 = `=1-D227`, E228 = `=1-E227`, ... copyToRange source D228, destination E228:AC228.
- Plugin writes:
  - D228 formula: `=1-D227`
  - copyToRange source D228, destination E228:AC228
- Per Rule 23 — this is NOT a year-chained ramp (each cell only references its own column's R227 value, not prior column). Safe.
- Number format `0.0%` on D:AC.
- AG/AH/AI/AJ: AG=blank / AH=blank / AI=`fixed-yearrow` / AJ=`Derived = 1 − Lunar share. No independent MC sample.`

**Verification read-back**:
- R227: D=100%, F=100%, G=70%, I=70%, S=70%, AC=70%
- R228: D=0%, F=0%, G=30%, I=30%, S=30%, AC=30%
- R228 D evaluates as formula `=1-D227` returning 0.
- Halt on any mismatch.

#### §3.1.d — Mark Sprint 0 R218 + R222 as superseded (memo flag, do NOT delete)

Per Principle 17 (delete superseded rows in same spec) — but Rule 10 forbids row insertions; deletion would require row insertion downstream rewires. Cleanest path: **leave R218 + R222 in place but add a column C note flagging them as orphan**.

- **R218 `Lunar % payload as labour units`** — read existing column C; append to column C: ` [LEGACY — Sprint 7 superseded by year-row "Lunar labour share of surface payload — year-row" at row N+1. This single-value row is orphan / no longer read by BV engine.]`
- **R222 `Mars % payload as labour units`** — same pattern: ` [LEGACY — Sprint 7 superseded by year-row at row N+2.]`

Plugin reads existing C218 / C222 content, concatenates the legacy flag, writes back. Two discrete writes.

**Plugin alternative if append-to-existing-C is technically complex**: overwrite C218 / C222 entirely with: `[LEGACY — Sprint 7 superseded by "Lunar labour share of surface payload — year-row" at row N+1. Original note: 30% labour / 70% hardware. This single-value row is orphan / no longer read by BV engine.]` (Lunar) and equivalent for Mars at C222.

**Verification**: read C218 / C222 — confirms `[LEGACY — Sprint 7 superseded` substring present. The B218 / B222 single-values (0.3 each) remain in place; BV engine in §3.3 does NOT read them.

---

### §3.2 — Allocator §3 MARS/MOON STRATEGIC CARVE-OUT section (rows 32-37)

Per Sprint 1 §3.2.1: Allocator R31 = section header `§3 MARS/MOON STRATEGIC CARVE-OUT`. Rows 32-37 reserved blank for Sprint 7. Sprint 7 fills rows 32-37 now.

**Row layout** (Sprint 7 writes 6 data rows):

| Row | Col A label | Col D formula (copy to E:AC) | Col C note |
|---|---|---|---|
| 32 | `Mars carve-out % of prior-year Group FCF (input)` | `=INDEX(Assumptions!$B:$B, MATCH("Mars carve-out % of prior-year Group FCF", Assumptions!$A:$A, 0))` | `Reads Assumptions R12 by canonical label. Single value spread across year-row D:AC. Base Case 15%; MC [3%, 35%] triangle.` |
| 33 | `Mars carve-out floor ($mm/yr) (input)` | `=INDEX(Assumptions!$B:$B, MATCH("Mars carve-out floor ($mm/yr)", Assumptions!$A:$A, 0))` | `Reads Assumptions R13. Base Case $1,000M; MC [$500M, $2,500M] triangle.` |
| 34 | `Prior-year Group FCF read ($mm/yr)` | `=IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF", 'Group P&L'!$A:$A, 0), E$5), 0)` | `Year-lookback by 1: column D=2025 reads year-offset E$5+1−2 = (D$5=0)+1−2 = -1 → IFERROR returns 0. For E=2026 onwards, reads prior column's GROUP FCF (E$5−1+1 = E$5 = 1 for 2026 reads col D=2025 FCF). Sprint 1 placeholder: Group P&L doesn't exist yet → IFERROR=0. Sprint 9 lights up.` |
| 35 | `Mars/Moon strategic carve-out ($mm/yr)` | `=MAX(D33, D32*D34)` | `Architecture §11.1: MAX(floor, prior-year FCF × pct). Pre-Sprint-9: prior FCF=0 → carve-out hits floor. THIS IS THE CANONICAL ROW Sprint 10 Queue Gate (Allocator §2 R18-R29) subtracts as a non-module claim AND Lunar Mars module reads as its cash inflow.` |
| 36 | `Lunar share of carve-out (% — year-row)` | `=INDEX(Assumptions!$D:$AC, MATCH("Lunar share of Mars/Moon carve-out cash — year-row", Assumptions!$A:$A, 0), E$5+1)` | `Reads Assumptions R227 year-row by canonical label. INDEX col_num = E$5+1 maps D=2025 → col 1 → returns Assumptions!D227 (= 1.0).` |
| 37 | `Mars share of carve-out (% — year-row)` | `=INDEX(Assumptions!$D:$AC, MATCH("Mars share of carve-out cash — year-row", Assumptions!$A:$A, 0), E$5+1)` | `Reads Assumptions R228 year-row.` |

**Plugin write structure (Rule 1 — 6 rows, each as a discrete labelled block)**:

For each row 32, 33, 34, 35, 36, 37:
1. Write column A label (one tool call per row).
2. Write column C note (one tool call per row).
3. Write column D formula explicitly (one tool call per row).
4. copyToRange source D{row}, destination E{row}:AC{row} (one tool call per row, single-cell source per Rule 2).
5. Apply number format:
   - Row 32: `0.0%` (percentage — Mars carve-out %)
   - Row 33: `#,##0` (currency $mm)
   - Row 34: `#,##0` (currency $mm)
   - Row 35: `#,##0` (currency $mm)
   - Row 36: `0.0%` (percentage)
   - Row 37: `0.0%` (percentage)

**6 rows × 5 discrete write blocks = 30 tool calls.** Plugin paces one row at a time per Rule 3.

**Verification read-back per row** (Rule 4 + Rule 16):

Row 32 (Mars carve-out %):
- D32 = 0.15, I32 = 0.15, S32 = 0.15, AC32 = 0.15
- Each year reads same Assumptions B12 (single value spread).
- Halt if not 0.15.

Row 33 (Mars carve-out floor):
- D33 = 1000, I33 = 1000, S33 = 1000, AC33 = 1000 ($mm).

Row 34 (Prior-year Group FCF read):
- D34 = 0 (IFERROR catches because Group P&L doesn't exist yet)
- I34 = 0, S34 = 0, AC34 = 0 (same — Sprint 9 will light up).
- Halt if any non-zero (means Group P&L exists but Sprint 7 didn't expect this).

Row 35 (Mars/Moon strategic carve-out — CANONICAL):
- D35 = MAX(1000, 0.15 × 0) = 1000 (hits floor)
- I35 = 1000, S35 = 1000, AC35 = 1000 (all hit floor pre-Sprint-9).
- Halt if D35 ≠ 1000.

Row 36 (Lunar share):
- D36 = 1.0, F36 = 1.0, G36 = 0.7, I36 = 0.7, S36 = 0.7, AC36 = 0.7
- Halt if D36 ≠ 1.0 or G36 ≠ 0.7.

Row 37 (Mars share):
- D37 = 0.0, F37 = 0.0, G37 = 0.3, I37 = 0.3, S37 = 0.3, AC37 = 0.3
- Halt if D37 ≠ 0.0 or G37 ≠ 0.3.

---

### §3.3 — Lunar Mars tab module body (rows 11-199)

The module body has 9 sub-sections. Layout:

| Rows | Sub-section | Concept |
|---|---|---|
| 11-15 | §3.3.1 | Carve-out cash inflow (read from Allocator §3) |
| 17-25 | §3.3.2 | Per-ship cost build |
| 27-35 | §3.3.3 | Lunar mission deployment |
| 37-45 | §3.3.4 | Mars mission deployment |
| 47-55 | §3.3.5 | Kg reservation off-the-top (canonical row for Sprint 10 §6.4) |
| 57-80 | §3.3.6 | Surface payload + labour units + hardware mass landed (BV engine inputs) |
| 82-110 | §3.3.7 | BV engine: active labour fleet, production output, hardware value-add, accumulated book value (Lunar + Mars separately) |
| 112-130 | §3.3.8 | Lunar Mars P&L: Revenue (=0), COGS, EBITDA, CapEx, FCF |
| 132-145 | §3.3.9 | Memo rows + diagnostics |

Each sub-section follows the pattern: SECT header (charcoal/white) → SUB header (italic) → VAL rows (column A label + column C note + column D formula + copyToRange E:AC).

Plugin executes one sub-section at a time, with verification gate (read D / I / S / AC) after each per Rule 4 + Rule 16.

#### §3.3.1 — Carve-out cash inflow (rows 11-15)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 11 | `CARVE-OUT CASH INFLOW (Architecture §11.1 — read from Allocator §3)` | (section header, no value) | charcoal/white fill, bold | text |
| 12 | `Total Mars/Moon strategic carve-out ($mm/yr)` | `=INDEX(Allocator!$D:$AC, MATCH("Mars/Moon strategic carve-out ($mm/yr)", Allocator!$A:$A, 0), E$5+1)` | `Reads Allocator R35 canonical row by label. Sprint 10 will activate prior-year Group FCF lookup; Sprint 7 reads floor $1,000M.` | `#,##0` |
| 13 | `Lunar share of carve-out (% — year-row)` | `=INDEX(Allocator!$D:$AC, MATCH("Lunar share of carve-out (% — year-row)", Allocator!$A:$A, 0), E$5+1)` | `Reads Allocator R36. 100% pre-2028, 70% 2028+.` | `0.0%` |
| 14 | `Mars share of carve-out (% — year-row)` | `=INDEX(Allocator!$D:$AC, MATCH("Mars share of carve-out (% — year-row)", Allocator!$A:$A, 0), E$5+1)` | `Reads Allocator R37. 0% pre-2028, 30% 2028+.` | `0.0%` |
| 15 | `Lunar cash allocation ($mm)` | `=D12*D13` | `Total carve-out × Lunar share. Sprint 7 pre-Sprint-9: $1,000M × 100% = $1,000M 2025-2027; $1,000M × 70% = $700M 2028+.` | `#,##0` |

Add R16: `Mars cash allocation ($mm)` = `=D12*D14`. Note: `Total carve-out × Mars share. $1,000M × 0% = $0M 2025-2027; $1,000M × 30% = $300M 2028+.` Format `#,##0`.

**Plugin pacing**: 6 rows (11 header + 12-16 data). Five discrete data row writes. Header row write separate. 6 total row-blocks.

**Verification (Rule 4 + Rule 16)**:
- D11 = section header text. Charcoal fill applied to A11:AC11.
- D12 = 1000, I12 = 1000, S12 = 1000, AC12 = 1000.
- D13 = 1.0, F13 = 1.0, G13 = 0.7, AC13 = 0.7.
- D14 = 0.0, F14 = 0.0, G14 = 0.3, AC14 = 0.3.
- D15 = 1000, F15 = 1000, G15 = 700, AC15 = 700.
- D16 = 0, F16 = 0, G16 = 300, AC16 = 300.
- Halt on any mismatch.

#### §3.3.2 — Per-ship cost build (rows 17-25)

Per Architecture §11.2: `Per-ship cost = Starship vehicle cost amortized × (1 + depot multiplier) + payload value (labour units + hardware) per ship`. Interpretation locked in §9 amendment 1 below: "ships deployed" = surface missions; per-ship cost = total mission cost (surface + depot vehicle launches + payload).

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 17 | `PER-SHIP COST BUILD (Architecture §11.2)` | section header | charcoal/white | text |
| 18 | `Starship vehicle cost amortized ($mm/ship)` | `=IFERROR(INDEX('Launch Capacity'!$D:$AC, MATCH("Blended Starship build cost per vehicle ($mm)", 'Launch Capacity'!$A:$A, 0), E$5+1) / IFERROR(INDEX(Assumptions!$B:$B, MATCH("Lifetime reuses per ship (cap)", Assumptions!$A:$A, 0)), 30), 32)` | `Per-vehicle cost / lifetime reuses (30 ships per vehicle, Sprint 0 R37 = 30). Reads Launch Capacity by canonical label if available; falls back to $32M default (Sprint 0 R501 blended build cost). Per Rule 14 — no hardcoded constants; the 32 fallback covers the case where Launch Capacity hasn't published this row yet.` | `#,##0.0` |
| 19 | `Lunar depot multiplier (×)` | `=INDEX(Assumptions!$B:$B, MATCH("Lunar fuel depot multiplier per outbound Starship", Assumptions!$A:$A, 0))` | `Reads Assumptions R216 = 1.` | `0.0` |
| 20 | `Mars depot multiplier (×)` | `=INDEX(Assumptions!$B:$B, MATCH("Mars fuel depot multiplier per outbound Starship", Assumptions!$A:$A, 0))` | `Reads Assumptions R220 = 5.` | `0.0` |
| 21 | `Lunar payload per surface ship (kg)` | `=INDEX(Assumptions!$B:$B, MATCH("Lunar payload per surface-landed Starship (kg)", Assumptions!$A:$A, 0))` | `Reads Assumptions R217 = 50,000 kg.` | `#,##0` |
| 22 | `Mars payload per surface ship (kg)` | `=INDEX(Assumptions!$B:$B, MATCH("Mars payload per surface-landed Starship (kg)", Assumptions!$A:$A, 0))` | `Reads Assumptions R221 = 100,000 kg.` | `#,##0` |
| 23 | `Hardware $/kg landed (year-row)` | `=INDEX(Assumptions!$D:$AC, MATCH("Hardware replacement cost factor ($/kg landed) — declining", Assumptions!$A:$A, 0), E$5+1)` | `Reads Assumptions R225 year-row. Declining cost basis per Q4'25 methodology.` | `#,##0` |
| 24 | `Lunar payload value ($mm/ship)` | `=D21*(1-INDEX(Assumptions!$D:$AC, MATCH("Lunar labour share of surface payload — year-row", Assumptions!$A:$A, 0), E$5+1))*D23/1000000` | `Hardware-component value per Lunar ship = (Lunar payload kg) × (1 − Lunar labour share) × hardware $/kg / 1e6 → $mm. Labour units have separate value path (production output via BV engine). For per-ship-cost purposes, labour units are an input cost = labour_kg × hardware_$/kg (proxy since Optimus-class units have similar manufacturing cost basis to general hardware per kg). NOTE: This is the COST basis for per-ship cost build; the VALUE basis (production output) is computed in BV engine §3.3.7.` | `#,##0.0` |
| 25 | `Mars payload value ($mm/ship)` | `=D22*(1-INDEX(Assumptions!$D:$AC, MATCH("Mars labour share of surface payload — year-row", Assumptions!$A:$A, 0), E$5+1))*D23/1000000` | `Same as Lunar but Mars payload (100K kg) and Mars labour share.` | `#,##0.0` |

Plus:
| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 26 | `Per-ship cost — Lunar ($mm)` | `=D18*(1+D19)+D24` | `Architecture §11.2: vehicle cost × (1 + Lunar depot) + Lunar payload value. = $32M × 2 + payload ≈ $64M + payload.` | `#,##0.0` |
| (next) 27 | `Per-ship cost — Mars ($mm)` | `=D18*(1+D20)+D25` | `Architecture §11.2: vehicle cost × (1 + Mars depot) + Mars payload value. = $32M × 6 + payload ≈ $192M + payload.` | `#,##0.0` |

**Pacing**: 11 rows (17-27). Apply Rule 3 row-by-row pacing.

**Verification (Rule 4 + Rule 16)**:
- D18 = ~32 (whether read from Launch Capacity or fallback), I18 / S18 / AC18 same range.
- D19 = 1.0, D20 = 5.0 (constant single-value reads from Assumptions).
- D21 = 50000, D22 = 100000.
- D23 = read year-row from R225 (Sprint 0 declining profile — value depends on Vlad's anchor; range expected $5K-$30K/kg).
- D24 = 50000 × (1 − 0.3) × ~$15K / 1e6 ≈ $525/ship × ~ 1 = ~$0.525M ... wait that's tiny. Let me re-check.
  - 50000 kg × 0.7 (hardware share) × $15,000/kg = $525,000,000 / 1e6 = $525M. OK that's huge.
  - Actually re-do: 50000 × 0.7 × 15000 = 525,000,000 (raw dollars) → /1e6 = $525 $mm.
  - That's ~$525M payload value for a Lunar surface ship. Big number.
- D26 (Per-ship cost Lunar) = $32M × 2 + $525M = $589M per Lunar surface mission.
- D27 (Per-ship cost Mars) = $32M × 6 + $1,050M (Mars payload 100K × 0.7 × $15K / 1e6 = $1,050M) = $1,242M per Mars surface mission.
- These are sanity-only. Will halt if D26 < $50M (would mean payload value broken) or > $5,000M (would mean unit conversion wrong).
- Edge-year reads: I26 / S26 / AC26 trend depends on hardware $/kg declining + labour share rising; expect D26 ~$589M decaying to AC26 ~$200-300M (cheaper hardware + more labour value-add not in cost basis).

Caveat in C24/C25 + §9: The "payload value" used in per-ship cost is a proxy = hardware mass × hardware $/kg. Labour units are TREATED as having same per-kg cost basis as hardware for the per-ship-cost calculation (mfg cost basis of Optimus units ≈ general hardware $/kg). This is a Sprint 7 simplifying assumption that mirrors the kickoff framing. Flagged in §9 amendment 2.

#### §3.3.3 — Lunar mission deployment (rows 29-35)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 29 | `LUNAR MISSION DEPLOYMENT (Architecture §11.2)` | section header | charcoal/white | text |
| 30 | `Lunar surface missions deployed (count)` | `=IFERROR(D15/D26, 0)` | `Lunar cash allocation / per-ship cost Lunar. = $1,000M / $589M ≈ 1.7 missions in 2025-2027 (100% Lunar). 2028+ at 70% share: $700M / per-ship cost ≈ 1.2-2.5 missions/yr depending on cost trajectory. IFERROR guards pre-revenue years where per-ship cost could be 0 (defensive).` | `0.00` |
| 31 | `Lunar total vehicle launches (count)` | `=D30*(1+D19)` | `Each surface mission = 1 surface ship + Lunar depot multiplier depot tankers. Per Architecture §11.3.` | `0.00` |
| 32 | `Lunar surface payload mass (kg landed)` | `=D30*D21` | `Surface missions × payload per surface ship (50K kg).` | `#,##0` |
| 33 | `Lunar labour share this year (%)` | `=INDEX(Assumptions!$D:$AC, MATCH("Lunar labour share of surface payload — year-row", Assumptions!$A:$A, 0), E$5+1)` | `Reads year-row amendment §3.1.a. D=2025 0.3 → AC=2050 0.7.` | `0.0%` |
| 34 | `Lunar labour mass landed (kg)` | `=D32*D33` | `Surface payload × labour share.` | `#,##0` |
| 35 | `Lunar hardware mass landed (kg)` | `=D32*(1-D33)` | `Surface payload × (1 − labour share).` | `#,##0` |

**Pacing**: 7 rows. One row at a time per Rule 3.

**Verification**:
- D30 = ~1.7 (= 1000 / 589), I30 = ~1.7 (carve-out at 70%: 700 / 580ish ≈ 1.2), S30 / AC30 depend on cost trajectory.
- D31 = D30 × 2 ≈ 3.4 (Lunar depot 1, so 2× launches per mission).
- D32 = D30 × 50000 ≈ 85,000 kg.
- D33 = 0.3, I33 = 0.380, S33 = 0.540, AC33 = 0.700.
- D34 = D32 × 0.3 ≈ 25,500 kg labour landed in 2025.
- D35 = D32 × 0.7 ≈ 59,500 kg hardware landed in 2025.
- Sanity halt: D32 > 500,000 kg (would mean 10+ missions in 2025, defies pre-2028 window framing — but Lunar IS continuous, so 1-3 missions in 2025-2027 expected; >5 missions = halt).

#### §3.3.4 — Mars mission deployment (rows 37-45)

Symmetric to §3.3.3 but for Mars:

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 37 | `MARS MISSION DEPLOYMENT (Architecture §11.2)` | section header | charcoal/white | text |
| 38 | `Mars surface missions deployed (count)` | `=IFERROR(D16/D27, 0)` | `Mars cash allocation / per-ship cost Mars. = $0 / $1,242M = 0 in 2025-2027 (0% Mars share); $300M / per-ship cost Mars ≈ 0.2-0.5 missions/yr from 2028 onwards.` | `0.00` |
| 39 | `Mars total vehicle launches (count)` | `=D38*(1+D20)` | `Each surface mission = 1 surface + 5 depot tankers. = surface × 6.` | `0.00` |
| 40 | `Mars surface payload mass (kg landed)` | `=D38*D22` | `Surface missions × Mars payload (100K kg).` | `#,##0` |
| 41 | `Mars labour share this year (%)` | `=INDEX(Assumptions!$D:$AC, MATCH("Mars labour share of surface payload — year-row", Assumptions!$A:$A, 0), E$5+1)` | `Reads year-row amendment §3.1.b. Same trajectory as Lunar.` | `0.0%` |
| 42 | `Mars labour mass landed (kg)` | `=D40*D41` | `Surface × Mars labour share.` | `#,##0` |
| 43 | `Mars hardware mass landed (kg)` | `=D40*(1-D41)` | `Surface × (1 − Mars labour share).` | `#,##0` |

**Verification**:
- D38 = 0 / $1,242M = 0 (pre-2028 Mars share = 0%).
- G38 (2028) = $300M / $1,242M ≈ 0.24 missions.
- I38 (2030) ≈ 0.24-0.3 (depending on cost trajectory).
- D40 = 0, G40 ≈ 24,000 kg, I40 ≈ 24,000-30,000 kg.
- Sanity: D38 = 0 exact (Mars share = 0% pre-2028 + IFERROR).

#### §3.3.5 — Kg reservation off-the-top (rows 47-55) — CANONICAL ROW for Sprint 10 §6.4

Per Architecture §11.3 + §6.4. THIS IS the row Sprint 10 Kg Queue Gate reads to compute `Capacity available for IRR queue = Total Starship capacity − Lunar Mars kg reserved`.

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 47 | `KG RESERVATION OFF-THE-TOP (Architecture §11.3 + §6.4)` | section header | charcoal/white | text |
| 48 | `Starship LEO payload per launch (kg)` | `=IFERROR(INDEX('Launch Capacity'!$D:$AC, MATCH("Starship LEO payload per launch (kg, Compute config)", 'Launch Capacity'!$A:$A, 0), E$5+1), 150000)` | `Reads Launch Capacity by canonical label per Sprint 5 §3.6 amendment 5 (added by Sprint 5 as new Assumptions). Fallback 150K kg (booster-only mode). Used for kg reservation off-top: each vehicle launch consumes full LEO payload of fuel (depot) or kg (surface).` | `#,##0` |
| 49 | `Lunar total launches × LEO payload (kg)` | `=D31*D48` | `Lunar vehicle launches × LEO payload — kg consumed off-top by Lunar program.` | `#,##0` |
| 50 | `Mars total launches × LEO payload (kg)` | `=D39*D48` | `Mars vehicle launches × LEO payload — kg consumed off-top by Mars program.` | `#,##0` |
| 51 | `Lunar Mars total kg reserved off-top (kg-to-LEO)` | `=D49+D50` | `Architecture §11.3: (Lunar + Mars total launches) × LEO payload. Sprint 10 §6.4 subtracts this from Total Starship capacity BEFORE the IRR queue runs. THIS IS THE CANONICAL CONSUMED ROW.` | `#,##0` |

**Verification**:
- D48 = 150,000 (kg LEO payload per launch).
- D49 = D31 × 150,000 ≈ 3.4 × 150K = ~510,000 kg.
- D50 = D39 × 150,000 = 0 × 150K = 0 kg (Mars share=0 pre-2028).
- D51 = D49 + D50 ≈ 510,000 kg reserved in 2025.
- G51 (2028) ≈ (Lunar 70% missions × 2 + Mars 30% missions × 6) × 150K → varies; sanity range $300K-$1M kg in 2028.
- Sanity halt: D51 > 5,000,000 kg in 2025 (would consume >5M kg — implausible vs 2025 Starship capacity ~450K kg per Sprint 2 §3.3 calibration target).

**Cross-tab consumer note (Rule 11 touch points)**:
- Sprint 10 Allocator §6 KG IRR-PRIORITY SIGMOID QUEUE will read R51 (`Lunar Mars total kg reserved off-top (kg-to-LEO)`) by canonical label as the kg-off-top subtraction. Sprint 7 publishes this row; Sprint 10 consumes.

#### §3.3.6 — Surface payload + labour units + hardware mass (BV engine inputs, rows 57-80)

Computes labour unit counts (per Architecture §11.4) for both Lunar and Mars.

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 57 | `BV ENGINE INPUTS (Architecture §11.4 — labour units + hardware)` | section header | charcoal/white | text |
| 58 | `Labour unit mass (kg)` | `=INDEX(Assumptions!$B:$B, MATCH("Labour unit mass (kg)", Assumptions!$A:$A, 0))` | `Reads Assumptions R209 = 60 kg. Optimus-class proxy.` | `#,##0` |
| 59 | `Labour unit useful life (yrs)` | `=INDEX(Assumptions!$B:$B, MATCH("Labour unit operational lifespan on surface (years)", Assumptions!$A:$A, 0))` | `Reads Assumptions R214 = 5 yrs. Cohort retirement input.` | `0.0` |
| 60 | `Labour unit base hourly output ($/hr)` | `=INDEX(Assumptions!$B:$B, MATCH("Labour unit base hourly output ($/hr; burdened $22/0.7)", Assumptions!$A:$A, 0))` | `Reads R210 = $31.43/hr burdened.` | `$#,##0.00` |
| 61 | `Labour unit daily working hours` | `=INDEX(Assumptions!$B:$B, MATCH("Labour unit daily working hours", Assumptions!$A:$A, 0))` | `R211 = 22 hrs.` | `0` |
| 62 | `Labour unit productivity factor` | `=INDEX(Assumptions!$B:$B, MATCH("Labour unit productivity factor vs human baseline", Assumptions!$A:$A, 0))` | `R212 = 1.0.` | `0.00` |
| 63 | `Labour unit productivity learning rate (%/yr)` | `=INDEX(Assumptions!$B:$B, MATCH("Labour unit productivity learning rate (%/yr)", Assumptions!$A:$A, 0))` | `R213 = 5%.` | `0.0%` |
| 64 | `Labour annual output per unit base year ($mm/yr)` | `=D60*D61*365/1000000` | `Hourly × daily hrs × 365 days / 1e6 → $mm. = $31.43 × 22 × 365 / 1e6 ≈ $0.2523M/yr per unit.` | `#,##0.000` |
| 65 | `Productivity multiplier (year-row, anchor-and-offset)` | `=POWER(1+$D$63, E$5)` | `(1 + learning)^year_offset. Per Rule 23 anchor-and-offset.` | `0.00` |
| 66 | `Labour annual output per unit this year ($mm/yr)` | `=D64*D65*D62` | `Base output × productivity multiplier × productivity factor. Compounds 5%/yr.` | `#,##0.000` |
| 67 | (blank for spacing) | | | |
| 68 | `LUNAR labour units landed (count this year)` | `=D34/D58` | `Lunar labour mass landed / labour unit mass.` | `#,##0` |
| 69 | `MARS labour units landed (count this year)` | `=D42/D58` | `Mars labour mass landed / labour unit mass.` | `#,##0` |
| 70 | (blank for spacing) | | | |
| 71 | `LUNAR labour units retired this year (cohort lookback)` | `=IF(E$5-D$59+1<1, 0, INDEX($D68:$AC68, 1, E$5-D$59+1))` | `Year-chained Rule 23 EXCEPTION: cohort retirement reads N years prior to this year's labour units landed. IF guard handles col_num<1 spill per memory feedback-index-col-zero-spills (modern Excel INDEX(range, 1, 0) returns whole-row spill; IFERROR doesn't catch). Useful life = 5 yrs → 2030 retires 2025 cohort, 2031 retires 2026 cohort, etc. Pre-2030 retirements = 0 (column index would be negative).` | `#,##0` |
| 72 | `MARS labour units retired this year (cohort lookback)` | `=IF(E$5-D$59+1<1, 0, INDEX($D69:$AC69, 1, E$5-D$59+1))` | `Same pattern, Mars cohort.` | `#,##0` |
| 73 | (blank for spacing) | | | |
| 74 | `LUNAR active labour fleet EoY (running sum, net retirements)` | `=IF(E$5=0, D68-D71, INDEX($D74:$AC74, 1, E$5)+D68-D71)` | `Year-chained Rule 23 EXCEPTION: EoY active = prior EoY + new landings − retirements. D74 (year-offset 0 = 2025) initializes with first-year landings − retirements (retirements = 0 in 2025). E74 onwards reads prior column. Per Architecture §11.4 "Active labour fleet (running sum, net of retirements at lifespan)."` | `#,##0` |
| 75 | `MARS active labour fleet EoY (running sum, net retirements)` | `=IF(E$5=0, D69-D72, INDEX($D75:$AC75, 1, E$5)+D69-D72)` | `Same as Lunar.` | `#,##0` |

**Verification (Rule 4 + Rule 16)**:
- D58 = 60, D59 = 5, D60 = 31.43, D61 = 22, D62 = 1.0, D63 = 0.05.
- D64 = $0.2523M/yr.
- D65 = (1.05)^0 = 1, I65 = (1.05)^5 = 1.276, S65 = (1.05)^15 = 2.079, AC65 = (1.05)^25 = 3.386.
- D66 = $0.2523M × 1 × 1 = $0.2523M. AC66 = $0.2523M × 3.386 × 1 = $0.854M (year 2050 per-unit annual output).
- D68 = D34 / 60 ≈ 25500 / 60 ≈ 425 Lunar units landed in 2025.
- D69 = 0 / 60 = 0 Mars units in 2025.
- D71 (2025): E$5-5+1 = 0-5+1 = -4 < 1 → IF guard returns 0. ✓
- I71 (2030): I$5-5+1 = 5-5+1 = 1 → INDEX($D68:$AC68, 1, 1) = D68 ≈ 425 (2025 cohort retiring). ✓
- D72 = 0 (Mars cohort 2025 = 0, no retirements anyway).
- D74 = D68 − D71 = 425 − 0 = 425 active in 2025.
- E74 = D74 + E68 − E71 = 425 + (next year landings) − 0.
- Halt if D74 < 0 (negative fleet — impossible).

**Critical INDEX col_num=0 guard verification**: spot-check that row 71 + 72 formulas return 0 for years where E$5 − useful_life + 1 < 1 (i.e., D-G for years 2025-2029 with useful_life=5; year-offset 0-4 → col_num=−4 to 0). Plugin reads D71, E71, F71, G71, H71 — all must return 0. Then I71 reads D68 (2025 cohort). Halt if any pre-2030 retirement row non-zero.

#### §3.3.7 — BV engine: production output + hardware value-add + accumulated BV (rows 82-110)

Per Architecture §11.4:
```
Annual production output ($mm) = active_labour_fleet × labour_annual_output × productivity_learning
Annual hardware value add ($mm) = hardware_mass_landed × hardware_$/kg
Annual book value contribution = production_output + hardware_value_add
Accumulated book value (year) = contribution(year) + prior_year_BV × (1 − 1/capital_lifetime)
```

Per Vlad lock: capital_lifetime = 10 yrs from Sprint 0 R205.

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 82 | `BV ENGINE OUTPUT (Architecture §11.4)` | section header | charcoal/white | text |
| 83 | `Capital lifetime — book value straight-line dep (yrs)` | `=INDEX(Assumptions!$B:$B, MATCH("Capital lifetime — book value straight-line depreciation (years)", Assumptions!$A:$A, 0))` | `Reads R205 = 10 yrs.` | `0.0` |
| 84 | (blank for spacing) | | | |
| 85 | `LUNAR annual production output ($mm/yr)` | `=D74*D66` | `Active Lunar labour fleet × per-unit annual output. = 425 × $0.2523M = $107M in 2025.` | `#,##0` |
| 86 | `MARS annual production output ($mm/yr)` | `=D75*D66` | `Active Mars labour fleet × per-unit annual output. = 0 in 2025.` | `#,##0` |
| 87 | (blank for spacing) | | | |
| 88 | `LUNAR annual hardware value add ($mm/yr)` | `=D35*D23/1000000` | `Lunar hardware mass landed (kg) × hardware $/kg / 1e6 → $mm. 59,500 kg × $15K / 1e6 ≈ $893M in 2025.` | `#,##0` |
| 89 | `MARS annual hardware value add ($mm/yr)` | `=D43*D23/1000000` | `Mars hardware × hardware $/kg / 1e6. = 0 in 2025.` | `#,##0` |
| 90 | (blank for spacing) | | | |
| 91 | `LUNAR annual BV contribution ($mm/yr)` | `=D85+D88` | `Production output + hardware value-add.` | `#,##0` |
| 92 | `MARS annual BV contribution ($mm/yr)` | `=D86+D89` | `Same for Mars.` | `#,##0` |
| 93 | (blank for spacing) | | | |
| 94 | `LUNAR accumulated book value (year)` | `=IF(E$5=0, D91, INDEX($D94:$AC94, 1, E$5)*(1-1/D$83)+D91)` | `Year-chained Rule 23 EXCEPTION: BV(year) = contribution(year) + prior_year_BV × (1 − 1/capital_lifetime). 2025 initializes with first-year contribution. 2026+ depreciates prior BV by 1/10 = 10% and adds new contribution. Architecture §11.4 verbatim.` | `#,##0` |
| 95 | `MARS accumulated book value (year)` | `=IF(E$5=0, D92, INDEX($D95:$AC95, 1, E$5)*(1-1/D$83)+D92)` | `Same as Lunar.` | `#,##0` |
| 96 | (blank for spacing) | | | |
| 97 | `Total Lunar + Mars accumulated BV ($mm)` | `=D94+D95` | `Memo total. Sprint 11 Valuation reads this × 1.5 multiplier for SoTP terminal anchor per Architecture §14.2.` | `#,##0` |

**Verification**:
- D83 = 10.
- D85 = D74 × D66 = 425 × $0.2523M = $107M.
- D86 = 0.
- D88 = D35 × D23 / 1e6 = 59,500 × $15,000 / 1e6 = $893M (assuming $15K/kg starting value).
- D89 = 0.
- D91 = D85 + D88 = $107M + $893M = $1,000M.
- D92 = 0.
- D94 = D91 = $1,000M (year-offset 0 → IF branch returns D91 directly).
- D95 = D92 = 0.
- D97 = $1,000M.

**Calibration conflict surfaced + resolved (see §9 amendment 3)**: naive §3.3.3 + §3.3.4 deployment formulas (without first-mission-year gate) produce D30 = 1.7 Lunar missions in 2025 → D94 = ~$1,000M Lunar BV 2025 → violates §6.6 calibration (Lunar BV 2025 = $0 exact; halt threshold any >$100M). Q4'25 anchor §5 confirms: "Mars & Moon mission cash spend 2025 = $0; first physical launches Q4'25 has at 2028 transfer window." Both Lunar + Mars are gated to first-mission year 2028+. Architecture §11.2 "Lunar continuous, Mars window-bound" applies once first-mission year activates. **Resolution: add first-mission-year gate** — see §3.1.e below adding a NEW Assumptions input `First mission year (Lunar Mars)` = 2028. The §3.3.3 + §3.3.4 deployment formulas gate against this year per the corrected formulas below.

---

### §3.1.e — NEW Assumptions amendment: `First mission year (Lunar Mars)` (calibration fix)

Per Q4'25 anchors §5 "Mars & Moon mission cash spend 2025 = $0; First physical launches Q4'25 has at 2028 transfer window" + Sprint Roadmap §6.6 calibration (Lunar BV 2025 = $0 exact, Mission CapEx 2025 = $0 exact). Sprint 7 needs a first-mission-year gate to align deployment with Q4'25 anchors. Per Rule 14 (no hardcoded constants), this gate value must live on Assumptions.

Append at row `N+3` (after §3.1.a at N+1, §3.1.b at N+2). Columns:

- **A**: `First mission year (Lunar Mars)`
- **B**: `2028`
- **C**: `Calibration anchor — Q4'25 §5: Mars & Moon mission cash spend 2025 = $0; first physical launches at 2028 Mars transfer window. Both Lunar + Mars gated to 2028+ pre-launch (consistent with Q4'25 methodology that treated 2025-2027 as carve-out accumulation only, no physical missions). Architecture §11.2 "Lunar continuous, Mars window-bound" applies once first-mission year activates.`
- **D:AC**: blank (single-value input)
- **AG**: `2026`
- **AH**: `2032`
- **AI**: `discrete`
- **AJ**: `MC range — first-mission year could plausibly slip to 2030 or 2032 (Starship development), or pull forward to 2026-2027 if Mars window-irrelevant Lunar program accelerates. Discrete distribution samples year integer.`

Plugin write structure (Rule 1): 4 discrete writes (A label, B value, C note, AG:AJ MC fields), then format `0` integer on B.

**Verification**:
- A{N+3} = `First mission year (Lunar Mars)`.
- B{N+3} = 2028.
- AG{N+3} = 2026, AH{N+3} = 2032, AI{N+3} = `discrete`.
- Halt on any mismatch.

---

### §3.3.3 (REVISED) — Lunar mission deployment with first-mission-year gate

Replace §3.3.3 row 30 formula above with:

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 30 | `Lunar surface missions deployed (count)` | `=IF(D$4 < INDEX(Assumptions!$B:$B, MATCH("First mission year (Lunar Mars)", Assumptions!$A:$A, 0)), 0, IFERROR(D15/D26, 0))` | `Gated by Assumptions first-mission year (2028). Pre-2028: $0 missions (Q4'25 anchor §5). 2028+: Lunar cash allocation / per-ship cost Lunar. Inner IFERROR guards against zero-divide if per-ship cost goes 0 (defensive). Outer IF reads D$4 (year header = 2025 for D-col) vs Assumptions first-mission-year value.` | `0.00` |

Same gate pattern applies to **§3.3.4 row 38 (Mars surface missions)**:

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 38 | `Mars surface missions deployed (count)` | `=IF(D$4 < INDEX(Assumptions!$B:$B, MATCH("First mission year (Lunar Mars)", Assumptions!$A:$A, 0)), 0, IFERROR(D16/D27, 0))` | `Same gate. Pre-2028: $0 Mars missions; 2028+: $300M / per-ship cost Mars ≈ 0.24 missions/yr.` | `0.00` |

**Verification re-anchored (with gate)**:
- D30 = 0 (2025 < 2028 → gate returns 0). ✓ matches §6.6 Mission CapEx 2025 = $0 exact.
- E30 = 0 (2026 < 2028). F30 = 0 (2027 < 2028).
- G30 (2028) = $700M / $589M ≈ 1.2 missions. ✓ first-mission year activates.
- I30 = 1.2-1.5 (depending on cost trajectory).
- Same for D38 = 0, G38 = ~0.24.

**Downstream cascade (Rule 11 touch points)**:
- D31 = D30 × 2 = 0. D32 = 0. D34 = 0. D35 = 0. (Lunar surface payload, labour mass, hardware mass all = 0 in 2025.)
- D39 = 0. D40 = 0. D42 = 0. D43 = 0. (Mars same.)
- D49 = 0. D50 = 0. D51 = 0 (kg reservation off-top = 0 in 2025). ✓
- D68 = 0 (Lunar labour units landed 2025 = 0). D69 = 0.
- D85 = D74 × D66 with D74 = D68 − D71 = 0 − 0 = 0 → D85 = 0.
- D88 = D35 × D23 / 1e6 = 0 × $15K / 1e6 = 0. → D88 = 0.
- D91 = 0. D94 = 0. ✓ Lunar BV 2025 = $0 exact (matches §6.6).
- D95 = 0. ✓ Mars BV 2025 = $0 exact.
- D97 = 0.

**Out-year activation (2030 sanity, Rule 11)**:
- I30 (2030) ≈ 1.2 (Lunar surface missions). I32 ≈ 60,000 kg payload.
- I38 (2030) ≈ 0.24 (Mars surface missions). I40 ≈ 24,000 kg payload.
- I94 (2030) = accumulated Lunar BV after 2028+2029+2030 contributions, depreciated 10%/yr per capital_lifetime.
- 2030 calc sanity: 3 yrs of Lunar contributions (~$1B/yr each pre-depreciation) → 2030 Lunar BV ≈ $2.5-3B range.
- Halt if I94 < $500M or > $10B (would indicate formula bug or wildly off-trajectory).

#### §3.3.8 — Lunar Mars P&L (rows 112-130)

Per Architecture §11.5. Revenue = 0 every year. COGS = mission ops + BV depreciation. Module EBITDA = Gross Profit = negative. CapEx = actual mission cash spend (gated 2028+). Module FCF = heavily negative.

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 112 | `LUNAR MARS P&L (Architecture §11.5)` | section header | charcoal/white | text |
| 113 | `Total Revenue ($mm)` | `=0` | `Pre-revenue throughout horizon per Architecture §11 framing note. Hardcoded literal zero — vending-machine framing simplification (no revenue line items to sum).` | `#,##0` |
| 114 | (blank) | | | |
| 115 | `Mission ops cost — Lunar ($mm)` | `=D30*D26*INDEX(Assumptions!$B:$B, MATCH("Module operating cost — Lunar (% of Lunar CapEx)", Assumptions!$A:$A, 0))` | `Lunar missions × per-ship cost × mission ops % (R206 = 5%). Pre-2028 gate → $0 in 2025-2027.` | `#,##0.0` |
| 116 | `Mission ops cost — Mars ($mm)` | `=D38*D27*INDEX(Assumptions!$B:$B, MATCH("Module operating cost — Mars (% of Mars CapEx)", Assumptions!$A:$A, 0))` | `Mars missions × per-ship cost × mission ops % (R207 = 5%).` | `#,##0.0` |
| 117 | `BV depreciation — Lunar ($mm/yr)` | `=IF(E$5=0, 0, INDEX($D94:$AC94, 1, E$5)/D$83)` | `Prior-year accumulated Lunar BV / capital_lifetime (10 yrs). Year-chained Rule 23 EXCEPTION: reads prior column's BV. 2025: prior BV=0 → dep=0. INDEX col_num = E$5 (year offset). For D=2025, E$5=0 → IF guard returns 0 (avoids INDEX col_num=0 spill per memory feedback-index-col-zero-spills). For E=2026 onwards, col_num = 1+ → reads D94 (2025 BV) which is 0 pre-2028.` | `#,##0.0` |
| 118 | `BV depreciation — Mars ($mm/yr)` | `=IF(E$5=0, 0, INDEX($D95:$AC95, 1, E$5)/D$83)` | `Same pattern, Mars BV.` | `#,##0.0` |
| 119 | `Total COGS ($mm)` | `=D115+D116+D117+D118` | `Mission ops + BV depreciation. NO R&D, SG&A, overhead, taxes per Rule 13 vending-machine test.` | `#,##0.0` |
| 120 | (blank) | | | |
| 121 | `Gross Profit ($mm)` | `=D113-D119` | `Revenue − COGS = 0 − COGS = negative.` | `#,##0.0` |
| 122 | `Module EBITDA ($mm)` | `=D121` | `= Gross Profit per vending-machine framing (Architecture §3). Single canonical EBITDA — no "True"/"after-overhead" variants per Principle 7.` | `#,##0.0` |
| 123 | `Module EBITDA Margin %` | `=IFERROR(D122/D113, 0)` | `IFERROR guard for pre-revenue zero-divide per Rule 20. Returns 0 since Revenue = 0 every year.` | `0.0%` |
| 124 | (blank) | | | |
| 125 | `Module CapEx ($mm)` | `=D30*D26+D38*D27` | `Total mission cash spend = (Lunar surface missions × per-ship Lunar) + (Mars surface missions × per-ship Mars). Pre-2028 gate → $0 in 2025-2027. NOT total carve-out cash (which is reserved by Allocator §3 regardless of spend); only ACTUAL mission spend that lands surface ships. Cash flow gap pre-2028 (carve-out reserved but not spent) is documented in §7 Open thread for Sprint 9/10 to resolve.` | `#,##0.0` |
| 126 | `Capital deployed ($mm)` | `=D125` | `Per Architecture §4.2: equilibrium-equal to Module CapEx (row 205). Lunar Mars has no CapEx lag.` | `#,##0.0` |
| 127 | (blank) | | | |
| 128 | `Module D&A add-back ($mm)` | `=D117+D118` | `BV depreciation Lunar + Mars (non-cash; added back to recover cash for FCF).` | `#,##0.0` |
| 129 | `Module FCF ($mm)` | `=D122+D128-D125` | `= EBITDA + D&A add-back − Module CapEx. Pre-tax pre-corp per Architecture §3. Pre-2028: 0 + 0 − 0 = 0. 2028+: −mission ops − CapEx (heavily negative).` | `#,##0.0` |

**Plugin pacing**: 17 rows (112-129). One row at a time per Rule 3.

**Verification (Rule 4 + Rule 16)**:

Pre-2028 (D=2025):
- D113 = 0 (Revenue exact, halt threshold: any non-zero).
- D115 = D30 × D26 × 0.05 = 0 × 589 × 0.05 = 0 ✓.
- D116 = 0 ✓.
- D117 = IF(E$5=0, 0, ...) — for D, E$5=0 → returns 0 ✓.
- D118 = 0 ✓.
- D119 = 0.
- D121 = 0 − 0 = 0.
- D122 = 0 (Module EBITDA 2025 = 0 — calibration check).
- D123 = IFERROR(0/0, 0) = 0 ✓.
- D125 = 0 × 589 + 0 × 1242 = 0 ✓ (matches §6.6 Mission CapEx 2025 = $0 exact).
- D126 = 0.
- D128 = 0.
- D129 = 0 + 0 − 0 = 0 (Module FCF 2025 = 0).

2030 (I col):
- I113 = 0 (Revenue still 0).
- I115 = ~1.2 × ~$580M × 0.05 = ~$35M Lunar mission ops.
- I116 = ~0.24 × ~$1200M × 0.05 = ~$14M Mars mission ops.
- I117 = prior Lunar BV (~$3B by 2029) / 10 = ~$300M Lunar BV depreciation.
- I118 = prior Mars BV (~$300M by 2029) / 10 = ~$30M.
- I119 = $35M + $14M + $300M + $30M = ~$380M COGS.
- I121 = −$380M Gross Profit.
- I122 = −$380M EBITDA.
- I125 = 1.2 × 580 + 0.24 × 1200 = ~$985M Module CapEx.
- I128 = $300M + $30M = $330M D&A add-back.
- I129 = −$380M + $330M − $985M = −$1,035M Module FCF (heavily negative as expected).

Sanity halt: I122 > 0 (positive EBITDA — would mean BV gains exceed cost; impossible in pre-revenue module). I129 > 0 (positive FCF — impossible pre-revenue).

#### §3.3.9 — Memo rows + diagnostics (rows 132-145)

For Sprint 11 + Sprint 9 diagnostic consumption. Italic per Rule 17.

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 132 | `MEMO: DIAGNOSTICS` | section header | charcoal/white | text |
| 133 | `Memo: Total carve-out reserved this year ($mm)` | `=D12` | italic | `Allocator §3 R35 read. Pre-2028: $1,000M floor. Diagnostic of total reserve regardless of mission spend.` | `#,##0` |
| 134 | `Memo: Carve-out vs Module CapEx gap ($mm)` | `=D12-D125` | italic | `Carve-out reserved by Allocator §3 minus actual Module CapEx. Pre-2028: $1,000M − 0 = $1,000M gap (cash reserved but not spent). 2028+: approximate zero in equilibrium. Sprint 9/10 will need to reconcile this in cash flow identity (Group P&L R109).` | `#,##0` |
| 135 | `Memo: Lunar surface missions cumulative` | `=IF(E$5=0, D30, INDEX($D135:$AC135, 1, E$5)+D30)` | italic | `Year-chained Rule 23 EXCEPTION: running sum of Lunar missions to date. Diagnostic of total Lunar program scale.` | `#,##0.0` |
| 136 | `Memo: Mars surface missions cumulative` | `=IF(E$5=0, D38, INDEX($D136:$AC136, 1, E$5)+D38)` | italic | `Same for Mars.` | `#,##0.0` |
| 137 | `Memo: Total Lunar + Mars vehicle launches this year` | `=D31+D39` | italic | `Total Starship launches consumed by Lunar Mars program. Sprint 10 will read kg reservation R51 directly (more precise — multiplies by LEO payload per launch); this memo is just the launch count.` | `#,##0.0` |
| 138 | `Memo: Lunar labour annual output ($mm/yr)` | `=D85` | italic | `Lunar fleet production output. Feeds R97 total BV.` | `#,##0` |
| 139 | `Memo: Mars labour annual output ($mm/yr)` | `=D86` | italic | `Same for Mars.` | `#,##0` |

**Plugin pacing**: 8 rows (132-139). Italic formatting on rows 133-139 per Rule 17.

**Verification (Rule 4 + Rule 16)**:
- D133 = 1000 (= D12 carve-out 2025).
- D134 = 1000 − 0 = 1000 (carve-out reserved but not spent in 2025 — gap flagged).
- D135 = 0 (no Lunar missions deployed in 2025).
- D136 = 0 (no Mars missions).
- D137 = 0 + 0 = 0.
- D138 = 0.
- D139 = 0.
- I135 (2030) = cumulative Lunar missions through 2030 = ~0 + 0 + 0 + 1.2 + 1.2 + 1.2 ≈ 3.6 missions.

---

### §3.4 — Allocator OUT contract overwrite (rows 200-212)

Sprint 1 wrote literal 0s. Sprint 7 OVERWRITES with module-derived values. Rule 22 stale-ref scan first: confirm Sprint 1's published labels still match (per §3.0 step 4 pre-flight).

**Per Rule 14 + Architecture §11.6 lock**: IRR rows R207/R208/R209 written as literal `=0` (NOT `=IFERROR(IRR(...), -1)` formulas). Pre-empts plugin pattern-matching against Sprint 5's IRR engine.

| Row | A label (Sprint 1 — verbatim) | D formula (Sprint 7) | C note |
|---|---|---|---|
| 200 | `CENTRAL ALLOCATOR OUTPUTS` | (section header — keep as-is) | (Sprint 1 note kept) |
| 201 | `Total Revenue ($mm)` | `=D113` | `Reads §3.3.8 R113. Always 0 (pre-revenue Lunar Mars).` |
| 202 | `Module EBITDA ($mm)` | `=D122` | `Reads §3.3.8 R122. = Gross Profit per vending-machine.` |
| 203 | `Module EBITDA Margin %` | `=IFERROR(D202/D201, 0)` | `IFERROR guard for zero-revenue divide per Rule 20.` |
| 204 | `Module FCF ($mm)` | `=D129` | `Reads §3.3.8 R129. Pre-tax pre-corp.` |
| 205 | `Module CapEx ($mm)` | `=D125` | `Reads §3.3.8 R125. Cash outlay this year on actual missions deployed (gated 2028+).` |
| 206 | `Capital deployed ($mm)` | `=D126` | `Reads §3.3.8 R126. Equilibrium-equal to R205 — Lunar Mars no CapEx lag.` |
| 207 | `Spot IRR` | `=0` | `Hardcoded literal 0 per Architecture §11.6: per-mission marginal IRR deferred. Vlad: "we can change this later. Not in rebuild scope." NOT an IFERROR(IRR(...), -1) formula.` |
| 208 | `Forward IRR (Y+2)` | `=0` | `Hardcoded literal 0 per Architecture §11.6.` |
| 209 | `Blended IRR` | `=0` | `Hardcoded literal 0 per Architecture §11.6. Lunar Mars never enters IRR queue (Architecture §6.2 — strategic carve-out off-the-top).` |
| 210 | `Capacity Demand (kg-to-LEO)` | `=D51` | `Reads §3.3.5 R51 — Lunar Mars total kg reserved off-top. Sprint 10 §6.4 reads this row by canonical label to subtract from Total Starship capacity BEFORE running kg sigmoid queue. NOT a competing demand claim (Lunar Mars not in kg queue per Architecture §6.4 framing).` |
| 211 | `Lunar Accumulated Book Value ($mm)` | `=D94` | `Reads §3.3.7 R94. Sprint 11 Valuation §14.2 reads this row + R212 at 2050 (AC col) for SoTP terminal anchor = 1.5 × (Lunar+Mars BV at 2050). ITALIC per Rule 17 (memo row — does not feed any P&L sum on this tab).` |
| 212 | `Mars Accumulated Book Value ($mm)` | `=D95` | `Reads §3.3.7 R95. Sprint 11 same.` |

**Plugin write structure (Rule 1)**:
1. Read existing labels A200:A212 — confirm verbatim match against Sprint 1's published strings (Rule 22 stale-ref scan checkpoint).
2. For each row 201-212, write column D formula (one tool call per row).
3. copyToRange source D{row}, destination E{row}:AC{row} (one tool call per row).
4. Number formats already applied by Sprint 1 (`#,##0` for $mm rows, `0.0%` for IRR + margin rows).
5. Italic on rows 211, 212 column A (Sprint 1 already applied per §3.3.2 — confirm preserved).

**Sprint 1 placeholder OVERWRITE per Rule 17 — superseded values**: this is a Rule-17 supersession: literal 0 placeholders REPLACED by live formulas. No leftover residue.

**Verification (Rule 4 + Rule 16)**:

Pre-2028 reads (D=2025):
- D201 = 0 (Revenue). D202 = 0 (EBITDA). D203 = 0% (margin IFERROR).
- D204 = 0 (FCF). D205 = 0 (CapEx). D206 = 0.
- D207 = 0. D208 = 0. D209 = 0 (all IRR hardcoded 0).
- D210 = 0 (kg reserved — gate pre-2028 → 0).
- D211 = 0 (Lunar BV). D212 = 0 (Mars BV).

2030 reads (I col):
- I201 = 0. I202 = ~−$380M. I203 = 0%.
- I204 = ~−$1,035M. I205 = ~$985M. I206 = ~$985M.
- I207 = 0. I208 = 0. I209 = 0.
- I210 = (I30 × 2 + I38 × 6) × 150K kg ≈ (2.4 + 1.44) × 150K = ~575,000 kg.
- I211 = ~$3B (3 years of contributions, depreciated 10%/yr).
- I212 = ~$300M.

2050 reads (AC col):
- AC201 = 0. AC202 = significantly negative.
- AC210 = same pattern — Lunar Mars kg consumption growing as carve-out scales with Group FCF growth.
- AC211 + AC212 = the canonical 2050 BV values Sprint 11 SoTP terminal reads. Expected range: AC211 in $20-100B / AC212 in $5-30B depending on FCF growth trajectory.

---

## §4 — Verification gate (universal + §6.6 Sprint 7 calibration)

### §4.1 — Workbook-wide error scan (Rule 4 + Principle 19)

Read every cell on every tab. Count occurrences of: `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`.

**Expected:**
- Zero new errors introduced by Sprint 7.
- PRE-EXISTING errors inherited (do NOT halt on these; document in Claude Log):
  - **Customer Launch G16:AC16 returns #N/A** — inherited from Sprint 5 §4.1; root cause is missing Assumptions row `Starship customer launch margin — CAGR (% change/yr from 2027 anchor)`. Per memory `project-sprint-3-6-micro-patch-needed`, Sprint 3.6 micro-patch resolves; not Sprint 7's scope.

Any NEW error in Sprint 7's written cells (Allocator R32-R37, Lunar Mars R11-R212 in §3.3 blocks, Assumptions R{N+1}/R{N+2}/R{N+3}) → halt, trace, fix before declaring complete.

### §4.2 — Edge-year read-back on Lunar Mars tab (Rule 16)

Read these cells in 4 edge years (D=2025, I=2030, S=2040, AC=2050). Document landed vs expected.

| Cell | 2025 (D) | 2030 (I) | 2040 (S) | 2050 (AC) | Halt if |
|---|---|---|---|---|---|
| R12 (total carve-out) | 1000 | 1000 (Sprint 9 will activate prior-FCF growth → 2030+ may grow) | 1000 | 1000 (Sprint 7 stays at floor) | <1000 |
| R30 (Lunar missions) | 0 | ~1.2 | varies | varies | D≠0 |
| R38 (Mars missions) | 0 | ~0.24 | varies | varies | D≠0 |
| R51 (kg reserved) | 0 | ~575K | varies | varies | D≠0; D<−1 |
| R94 (Lunar BV) | 0 | $2-4B | $5-15B | $15-50B | D≠0; D>100 |
| R95 (Mars BV) | 0 | $200-500M | $1-3B | $5-20B | D≠0; D>100 |
| R122 (Module EBITDA) | 0 | negative | more negative | most negative | D≠0; D>0 in any year |
| R125 (Module CapEx) | 0 | ~$985M | varies | varies | D≠0; D>10 |
| R129 (Module FCF) | 0 | ~−$1B | more negative | most negative | D≠0; D>0 in any year |
| R201 (Total Revenue) | 0 | 0 | 0 | 0 | any non-zero |
| R209 (Blended IRR) | 0 | 0 | 0 | 0 | any non-zero |
| R210 (Capacity Demand kg) | 0 | ~575K | varies | varies | D≠0 |
| R211 (Lunar Acc BV) | 0 | $2-4B | $5-15B | $15-50B | D≠0; D>100 |
| R212 (Mars Acc BV) | 0 | $200-500M | $1-3B | $5-20B | D≠0; D>100 |

### §4.3 — Conservation trivial check

Pre-Sprint-9: Group P&L conservation block (R99-R110) was set up by Sprint 1 §3.5 as literal 0 = 0. Sprint 7's writes to Lunar Mars don't affect any of these checks (Sprint 9 will activate full Group P&L walk + conservation). Trivial pass.

Sprint 7's contributions that DO feed Sprint 9 conservation:
- R201 (Total Revenue 0) → Group P&L Revenue check (R99) sums Lunar Mars 0 with other modules. OK.
- R202 (Module EBITDA) → R100. Sprint 9 sums.
- R205 (Module CapEx) → R101. Sprint 9 sums.
- R204 (Module FCF) → R102. Sprint 9 sums.

### §4.4 — Round-trip stability (Rule 22 / Principle 22)

After all §3 writes complete:
1. Recalc workbook 5 times (full rebuild — F9 with Ctrl-Shift-F9 or equivalent).
2. Capture: Lunar Mars R94 (Lunar BV), R95 (Mars BV), R125 (Module CapEx), R129 (Module FCF), R210 (kg reserved) at I (2030) and AC (2050).
3. Confirm no value moves >$1M across the 5 recalcs.

Sprint 7 introduces ONE cross-year dependency (Allocator R34 reads prior-year Group P&L FCF via IFERROR). Pre-Sprint-9, Group P&L doesn't have GROUP FCF row populated → IFERROR returns 0 every recalc → stable.

Sprint 7 within-year cycles: none introduced. Pre-existing within-year cycles (Sprint 4 Starlink ↔ Starlink Capacity; Sprint 5 ODC IRR ↔ bandwidth) remain ON; iterative calc handles per memory `project-iterative-calc-enabled-2026-05-20`.

Halt if any captured value swings >$1M across 5 recalcs (would indicate new bistability — diagnose which Sprint 7 formula is interacting with iterative calc).

### §4.5 — Stale-reference scan (Rule 22)

Three scan checkpoints:

**Scan 1 — Sprint 7's Allocator §3 reads on Lunar Mars module body**:
- Lunar Mars R12 reads Allocator R35 by label `Mars/Moon strategic carve-out ($mm/yr)`. Confirm Allocator!A35 string matches Lunar Mars R12 formula's MATCH literal.
- Lunar Mars R13 reads Allocator R36 by label `Lunar share of carve-out (% — year-row)`. Confirm match.
- Lunar Mars R14 reads Allocator R37 by label `Mars share of carve-out (% — year-row)`. Confirm match.

**Scan 2 — Sprint 7's Lunar Mars OUT block writes match Sprint 1's published labels**:
- Read A200:A212 — confirm verbatim Sprint 1 strings: `CENTRAL ALLOCATOR OUTPUTS`, `Total Revenue ($mm)`, `Module EBITDA ($mm)`, `Module EBITDA Margin %`, `Module FCF ($mm)`, `Module CapEx ($mm)`, `Capital deployed ($mm)`, `Spot IRR`, `Forward IRR (Y+2)`, `Blended IRR`, `Capacity Demand (kg-to-LEO)`, `Lunar Accumulated Book Value ($mm)`, `Mars Accumulated Book Value ($mm)`. Halt on any drift.

**Scan 3 — Assumptions §8 amendment dedupe (re-confirmation)**:
- After §3.1 writes complete, MATCH probes:
  - `MATCH("Lunar labour share of surface payload — year-row", Assumptions!$A:$A, 0)` → returns row N+1 (new amendment).
  - `MATCH("Mars labour share of surface payload — year-row", Assumptions!$A:$A, 0)` → returns row N+2.
  - `MATCH("First mission year (Lunar Mars)", Assumptions!$A:$A, 0)` → returns row N+3.
- Confirm Sprint 0 labels R218 `Lunar % payload as labour units` + R222 `Mars % payload as labour units` STILL resolve to their original rows (just orphan now, not deleted). Confirm C218 + C222 contain `[LEGACY` substring per §3.1.d.

### §4.6 — Sprint 7 calibration table (Sprint Roadmap §6.6)

| Output | 2025 target | Tolerance | Halt if |
|---|---|---|---|
| Lunar Mars revenue (R201) | $0 | exact | any >$0 |
| Mission CapEx 2025 (R205) | $0 | exact | any >$10M |
| Lunar BV accumulated 2025 (R211) | $0 | exact | any >$100M |
| Mars BV accumulated 2025 (R212) | $0 | exact | any >$100M |
| Module FCF 2025 (R204) | $0 | exact | any non-zero (since CapEx + EBITDA + D&A all 0 pre-2028) |

Out-year sanity (informational, not halt):
- 2030+ Mars fleet > 0 sanity: I38 (Mars missions 2030) > 0. If I38 = 0 with Mars share = 30%, formula bug → halt.
- BV memo row monotonicity: R211 + R212 should be monotonically non-decreasing once deployments start (2028+). If any I/S/AC year reads less than prior year, BV depreciation may be over-eating contribution; diagnose.

Per Rule 13 — confirm NO R&D row anywhere on Lunar Mars tab. Plugin scans Lunar Mars column A for `R&D` substring: must return zero results. Mars/Moon R&D $700M 2025 lives on OpEx tab Sprint 8.

### §4.7 — Claude Log entry (Rule 4 + Sprint Roadmap §5.7)

Append one row to Claude Log tab:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-05-{DD} | 7 | Lunar Mars, Allocator, Assumptions | Lunar Mars module body built (rows 11-145). 5 canonical Allocator OUT rows live (R201, R202, R204, R205, R210) + 2 BV memo rows (R211, R212) live. IRR rows R207/R208/R209 hardcoded =0 per Architecture §11.6. Allocator §3 carve-out section live (R31-R37): Mars carve-out = MAX($1B floor, prior-year FCF × 15%); pre-Sprint-9 hits floor $1B every year. Lunar share = 100% pre-2028, 70% 2028+ (Vlad lock: Lunar/Moon focus over Mars). 3 new Assumptions amendments: Lunar + Mars labour share year-rows (0.3 → 0.7 ramp); First mission year (2028 gate). Sprint 0 R227/R228 stub year-rows filled. R218/R222 single-value 0.3 flagged as orphan. Calibration verified: 2025 Lunar Mars revenue = $0 exact, Mission CapEx = $0 exact, Lunar BV = $0 exact, Mars BV = $0 exact (all hit halt thresholds). Vending-machine test passes: zero R&D rows on Lunar Mars tab (Mars/Moon R&D $700M flows OpEx Sprint 8). | (1) Carve-out vs Module CapEx gap pre-2028 ($1B/yr reserve mismatch) — Sprint 9/10 cash flow identity needs to reconcile. (2) Customer Launch G16:AC16 #N/A inherited from Sprint 5 — Sprint 3.6 micro-patch awaiting. (3) Architecture §11.4 ambiguity on "ships deployed / (1+depot)" — Sprint 7 interpreted as surface missions (consistent with §11.2 per-ship cost formula); flagged as §11.4 amendment candidate. | Sprint 8 (OpEx + CapEx tabs) per Roadmap §3 — Sprint 8 reads Lunar Mars Module CapEx R205 for Group CapEx aggregation. AI Stack (Sprint 6) remains deferred per `project-sprint-6-deferred`. |

---

## §5 — Claude Log entry template

See §4.7 above.

---

## §6 — Don't touch (out of scope)

- **Sprint 5 ODC tab** — Sprint 7 reads ODC for sanity (pre-flight step 6) but writes nothing. ODC's 5 canonical labels + IRR engine + bandwidth flow remain untouched.
- **Sprint 4 Starlink + Starlink Capacity** — Sprint 7 doesn't touch these tabs.
- **Sprint 3 Customer Launch** — Sprint 7 doesn't touch. Customer Launch G16:AC16 #N/A inherited error remains; Sprint 3.6 micro-patch separately resolves.
- **Sprint 2 Launch Capacity** — Sprint 7 READS by canonical label only (vehicle cost per ship per §3.3.2, Starship LEO payload per §3.3.5). Writes nothing.
- **Sprint 1 Allocator skeleton** — Sprint 7 fills RESERVED rows 32-37 (Mars/Moon strategic carve-out section) but does NOT touch §1 Cash Pool Tracker (R7-15), §2 Queue Gate (R17-29 — Sprint 10), §4 Cash Sigmoid Queue (R39-80 — Sprint 10), §6 Kg Sigmoid Queue (R89-130 — Sprint 10), §8 Vehicle Build Claim (R139-150 — Sprint 10), §9 Central IRR Display (R152-165 — Sprint 10).
- **Allocator §5 Module Cash Allocations (R83-87) + §7 Module Kg Allocations (R133-137)** — Sprint 7 leaves Sprint 1 placeholders (Lunar Mars cash + kg allocation rows = literal 0) as-is. Lunar Mars module reads carve-out directly from Allocator §3 R35, NOT from §5/§7. The §5/§7 0-placeholders for Lunar Mars are architecturally redundant (Architecture §4.1: "hardcoded zeros — Lunar Mars outside IRR queue") but Sprint 1 set them up for consistency with the other 4 modules; Sprint 7 leaves untouched.
- **R&D / SG&A / overhead / taxes on Lunar Mars tab** — Rule 13 vending-machine test. Sprint 7 writes ZERO R&D rows. Mars/Moon R&D $700M 2025 flows OpEx (Sprint 8 owns).
- **Per-mission IRR engine** — Architecture §11.6 lock: deferred. Sprint 7 writes R207/R208/R209 = literal 0; no IFERROR(IRR(...), -1) formulas.
- **Group P&L conservation block (R99-R110)** — Sprint 1 set up trivial 0=0. Sprint 9 activates. Sprint 7 trivially passes.
- **Valuation tab SoTP terminal** — Sprint 11 reads Lunar Mars R211/R212 × 1.5 multiplier. Sprint 7 publishes R211/R212; doesn't touch Valuation tab.

---

## §7 — Open thread (post-Sprint-7 considerations)

1. **Carve-out vs Module CapEx gap pre-2028** — Sprint 7 reserves $1B/yr carve-out 2025-2027 (Allocator R35) but Module CapEx 2025-2027 = $0 (gated). Per Q4'25 anchor, this is correct: $1B/yr accumulates as Mars/Moon program reserve, doesn't actually spend until 2028. **Sprint 9/10 cash flow identity (Group P&L R109) needs to handle the gap**: either (a) treat carve-out as a real cash drain regardless of mission spend (carve-out × 3 yrs = $3B disappears 2025-2027), or (b) carry the unspent $3B as Mars program reserve that gets deployed 2028+. Vlad to lock the accounting in Sprint 9/10 spec.

2. **Architecture §11.4 ambiguity on "Surface-landed Starships = ships deployed / (1+depot)"** — Sprint 7 interpreted "ships deployed" as surface missions (consistent with §11.2 per-ship cost formula). The §11.4 division by (1+depot) is inconsistent with §11.2 + §11.3 framing. Flagged as Architecture §11.4 amendment candidate; resolve in Sprint 10/11 audit or pre-Sprint-9 Architecture refresh.

3. **Customer Launch G16:AC16 #N/A inherited from Sprint 5** — Sprint 3.6 micro-patch awaiting. Not Sprint 7's scope, but Sprint 7 §4.1 documents the inherited #N/A. Sprint 3.6 prep: add Assumptions row `Starship customer launch margin — CAGR (% change/yr from 2027 anchor)`.

4. **R218 + R222 orphan single-value rows** — Sprint 7 marked as `[LEGACY — Sprint 7 superseded by year-row...]`. Future audit may want to formally delete (would require row-insertion downstream rewires, contraindicated). Recommended: leave orphan indefinitely; trust the column-C flag.

5. **Hardware $/kg year-row sensitivity (R225)** — Sprint 0 R225 declining profile drives Lunar BV trajectory heavily (via R88 hardware value-add). MC range is wide. Sprint 12 MC overlay may want to add a CORRELATED-MC link between R225 and the labour share trajectories (high hardware $/kg + low labour share → hardware-dominated BV; low hardware $/kg + high labour share → labour-dominated BV).

6. **Lunar Mars terminal valuation (Architecture §14.2)** — Sprint 11 will read R211/R212 at AC col × 1.5 multiplier. Vlad to consider whether 1.5× BV is the right terminal multiplier in Sprint 11 prep — could be replaced by (a) Gordon Growth on BV, (b) revenue multiple once Lunar Mars exits pre-revenue (per Architecture §11 framing note "Revenue = 0 throughout horizon" — would need horizon extension).

7. **Lunar/Mars share trajectory smoothing** — Sprint 7 wrote R227 as step function (100% pre-2028 → 70% 2028+). Smoother transition (e.g., 80% 2028 → 70% 2030 → 65% 2040) could better reflect program ramp. Vlad to consider Sprint 12 MC overlay for this trajectory.

---

## §8 — Execution sequence

Plugin executes in this order. Verification gate after each section before proceeding.

1. **§3.0 Pre-flight checks** (10 items). Halt on any miss.
2. **§3.1 Assumptions amendments** (4 sub-sections):
   - §3.1.a `Lunar labour share of surface payload — year-row` (row N+1, 4-block write).
   - §3.1.b `Mars labour share of surface payload — year-row` (row N+2, 4-block write).
   - §3.1.c Fill R227 + R228 year-row stubs (Lunar = 100% pre-2028 / 70% 2028+; Mars = 1 − R227 via formula).
   - §3.1.d Mark R218 + R222 with `[LEGACY` flag in column C (orphan-tag).
   - §3.1.e `First mission year (Lunar Mars)` = 2028 single-value (row N+3).
   - Verification: read each new row's D / I / S / AC / B (single-value rows) per §4.2 pattern.
3. **§3.2 Allocator §3 carve-out section** (rows 32-37, 6 rows × 5 blocks = 30 writes). Verification: read D-row + I/S/AC edge years for each row.
4. **§3.3 Lunar Mars tab body** — execute sub-sections IN ORDER (each with verification gate per Rule 4):
   - §3.3.1 Carve-out cash inflow (rows 11-16). Verify D11-D16.
   - §3.3.2 Per-ship cost build (rows 17-27). Verify D17-D27.
   - §3.3.3 Lunar mission deployment (rows 29-35, gated). Verify D30=0, G30>0, I30>0.
   - §3.3.4 Mars mission deployment (rows 37-43, gated). Verify D38=0, G38>0.
   - §3.3.5 Kg reservation off-top (rows 47-51, CANONICAL R51). Verify D51=0, I51>0.
   - §3.3.6 BV engine inputs (rows 57-75). Verify D68/D69/D74/D75 = 0 in 2025.
   - §3.3.7 BV engine output (rows 82-97). Verify D94=0, D95=0, D97=0.
   - §3.3.8 Lunar Mars P&L (rows 112-129). Verify D113=0, D125=0, D129=0.
   - §3.3.9 Memo rows + diagnostics (rows 132-139). Verify D133=1000, D134=1000.
5. **§3.4 Allocator OUT contract overwrite** (rows 201-212). Rule 22 stale-ref scan FIRST (confirm labels intact), then overwrite. Verify D201=0 through D212=0 (all 2025 outputs hit calibration zeros).
6. **§4.1-§4.6 Universal verification**: workbook-wide error scan, edge-year reads, conservation trivial, round-trip stability, stale-ref scan, calibration table.
7. **§4.7 Claude Log entry** — append single row to Claude Log tab.

---

## §9 — Amendment log

- **2026-05-20 amendment 1 (Architecture §11.4 "ships deployed / (1+depot)" interpretation)** — Architecture §11.2 says `Per-ship cost = vehicle × (1+depot) + payload`, implying "ships deployed" = surface missions (each mission consumes (1+depot) vehicle launches + payload). §11.3 kg reservation formula `(Lunar + Mars ships) × LEO payload × (1+depot)` is consistent with surface-missions reading. §11.4 BV engine "Surface-landed Starships = ships deployed / (1+depot)" contradicts: would understate surface landings by factor (1+depot). Sprint 7 resolves by treating "ships deployed" = surface missions throughout (§11.4 division skipped). Flagged as Architecture §11.4 amendment candidate for pre-Sprint-9 refresh — recommend updating §11.4 to `Surface-landed Starships (year) = ships deployed` (no division) for consistency.

- **2026-05-20 amendment 2 (Per-ship cost payload value proxy for labour units)** — Architecture §11.2 per-ship cost formula uses "payload value (labour units + hardware) per ship." The cost basis for labour units is not separately specified in Architecture §11. Sprint 7 implements: payload value (per ship) = surface payload kg × (1 − labour share) × hardware $/kg / 1e6. This treats labour units as having the same per-kg cost basis as general hardware for the per-ship cost calculation. The VALUE basis (production output) is computed separately in BV engine §3.3.7 (active fleet × per-unit annual output). Defensible since Optimus-class manufacturing cost basis ≈ general spacecraft hardware $/kg; both are mfg-cost-anchored. MC range on R225 hardware $/kg captures the uncertainty.

- **2026-05-20 amendment 3 (First-mission-year gate added — calibration anchor fix)** — Initial spec draft had Lunar/Mars deployment ungated, producing D30 = 1.7 Lunar missions in 2025 → D94 = $1,000M Lunar BV → violation of §6.6 halt threshold (Lunar BV 2025 = $0 exact). Per Q4'25 anchor §5 "Mars & Moon mission cash spend 2025 = $0; first physical launches at 2028 transfer window," gated deployment to first-mission year. Added §3.1.e new Assumptions input `First mission year (Lunar Mars)` = 2028 (single value, MC discrete [2026, 2032]). §3.3.3 R30 + §3.3.4 R38 formulas wrap base deployment formula with `IF(D$4 < INDEX(Assumptions!..., MATCH("First mission year (Lunar Mars)", ...)), 0, ...)`. Downstream cascade verifies: D32 = D34 = D35 = 0 (Lunar 2025), D40-D43 = 0 (Mars 2025), D49-D51 = 0 (kg reserved), D68/D69 = 0 (labour units landed), D85-D91/D94/D95 = 0 (BV contributions, accumulated BV), D125 = 0 (Module CapEx), D129 = 0 (Module FCF). Matches §6.6 calibration exactly.

- **2026-05-20 amendment 4 (Carve-out vs Module CapEx accounting gap pre-2028)** — Pre-2028 gate: Allocator §3 R35 reserves $1B/yr carve-out (per Architecture §11.1) but Lunar Mars Module CapEx R205 = $0 (no missions deployed). The $1B/yr "Mars/Moon program reserve" accumulates 2025-2027 = $3B unspent. Sprint 7 flags in §7 Open thread for Sprint 9/10 cash flow identity to reconcile. Two options: (a) carve-out is real cash drain regardless of mission spend (Mars program offsets group cash by $3B 2025-2027), (b) unspent carve-out carries forward as Mars program reserve deployed 2028+. Sprint 7 doesn't lock either; publishes R134 (`Memo: Carve-out vs Module CapEx gap`) as diagnostic.

- **2026-05-20 amendment 5 (R218 + R222 orphan via column-C flag, not deletion)** — Sprint 0 R218 `Lunar % payload as labour units` = 0.3 + R222 `Mars % payload as labour units` = 0.3 superseded by §3.1.a + §3.1.b new year-row amendments. Per Principle 17 (delete superseded rows in same spec), ideal cleanup = delete. Per Rule 10 (no row insertions in cross-ref tabs), deletion would require row-insertion downstream rewires. Compromise: flag column-C with `[LEGACY — Sprint 7 superseded...]` prefix. Orphan rows remain in place; BV engine reads new year-row labels only. Future Sprint 12 MC cleanup or post-build audit can delete formally.

- **2026-05-20 amendment 6 (Carve-out terminology retained — "Mars carve-out" despite Lunar emphasis)** — Vlad locked 2026-05-20: shifting focus to Moon/Lunar over Mars vs first iteration. Lunar share = 100% pre-2028, 70% 2028+ (70/30 Lunar-heavy). Architecture §11.1 + §6.2 + Sprint 0 §2 names the carve-out variable `Mars/Moon strategic carve-out` / `Mars carve-out %`. Per Principle 7 (no renames mid-build), Sprint 7 retains original naming; the Lunar emphasis is captured via R227 70% year-row trajectory. Future rename to `Lunar/Mars` or `Moon program carve-out` would require constitutional doc amendment (Architecture §11 + Sprint 0 §2 + 9 cross-tab references); deferred.

---

## §10 — Pre-execution checklist for plugin

Before plugin chat starts writing:

- [ ] Constitutional docs read (00, 01, 02 §§1-17, 03, 04, Model Execution Rules, 2025 Anchors).
- [ ] This spec's §1 Rule Compliance Preamble — all 12 boxes ticked (confirmed by spec author 2026-05-20).
- [ ] §1.5 Pre-execution setup — confirmed: Sprint 3.6 not landed (inherited #N/A documented), iterative calc ON workbook-wide, no workbook-name confirmation needed.
- [ ] §3.0 Pre-flight checks (10 items) — to be run by plugin BEFORE any write.
- [ ] Plugin understands Lunar Mars is NOT in IRR queue; R207/R208/R209 hardcoded `=0`.
- [ ] Plugin understands first-mission-year gate (D$4 < first-mission-year → 0) applies to BOTH Lunar (R30) AND Mars (R38) deployment.
- [ ] Plugin understands cross-year dependencies (Allocator R34 reads Group P&L via IFERROR) and within-year cycles (none introduced by Sprint 7).
- [ ] Vlad will handle all saving; plugin issues no save commands.
- [ ] Vlad handles workbook versioning outside the spec; spec names no workbook files.

