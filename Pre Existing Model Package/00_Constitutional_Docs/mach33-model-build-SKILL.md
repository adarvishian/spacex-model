---
name: mach33-model-build
description: "Use whenever Vlad or a Mach33 team member is building, rebuilding, scoping, or executing any modular financial valuation model (SpaceX, Portal, ASTS, future builds). Triggers: rebuild the model, scope this sprint, draft the architecture spec, write a sprint spec, execute Sprint N, sprint kickoff, Rule Compliance Preamble, constitutional docs, plugin execution, vending-machine framing, anchor-and-offset, allocator OUT contract, queue gate, per-sat IRR, INDEX/MATCH by label, no OFFSET, calibration target, stale-ref scan. Use in BOTH spec-author and plugin execution chats. Embeds constitutional framework (Lessons Learned, Architecture, Sprint Roadmap, Execution Rules) — no external doc reads required. Do NOT use for one-off Excel cleanup, weekly analyses (use mach33-weekly-analysis), or thesis framing (use mach33-thesis-library)."
---

# Mach33 Model Build: The Rebuild-v2 Approach

This skill encodes how Mach33 builds modular financial valuation models after the V30.5 → Rebuild-v2 reset in May 2026. It's the load-bearing approach for any new model build (SpaceX, Portal, future ASTS, etc.) and any rebuild of an existing model that has accumulated drift.

The skill works in two modes:
1. **Spec-author mode** — Claude is helping Vlad scope a sprint, write a sprint spec, or design architecture. Use sections II–VI.
2. **Plugin execution mode** — Claude is the plugin executing a sprint spec against a workbook. Use sections V–VII as a non-negotiable discipline contract.

If the user is starting a brand-new model (not a sprint inside one), see Section I on the **bootstrap protocol** — the five constitutional docs must be drafted before any sprint runs.

---

## I. The bootstrap protocol — building from scratch

A new Mach33 model build (or a rebuild after drift) starts with five constitutional documents in the project folder. **Sprints don't begin until all five exist.** This is the single biggest lesson from V30.5: load-bearing methodology arrived late (vending-machine framing at spec 12, per-sat IRR at spec 30), forcing retrofit cascades that took 11+ days of build time.

**The five docs:**

| # | Doc | Purpose | Status |
|---|-----|---------|--------|
| 00 | `00_README_Sprint_Kickoff.md` | Navigation + protocol + kickoff prompt template | Authoritative entry point |
| 01 | `01_Lessons_Learned.md` | The 23 principles (WHY) — each tied to a specific V30.5 incident | Constitutional |
| 02 | `02_Architecture_and_Methodology.md` | Structural design + math conventions (WHAT + HOW) | Constitutional |
| 03 | `03_Sprint_Roadmap_and_Verification.md` | 12-sprint phase plan + acceptance criteria (WHEN) | Constitutional |
| 04 | `04_Assumptions_Tab_Spec.md` + `_Build_Plan.xlsx` | Cell-by-cell input plan (INPUTS) | Constitutional |

Plus `Model Execution Rules.md` — the 23 plugin-side operational rules + Rule Compliance Preamble template.

**Bootstrap checklist** (when starting a new build):
1. Confirm with the user what's being built and the deadline.
2. Identify the predecessor/reference workbook (e.g. V30.5 + Q4'25 anchors for SpaceX). Use it for **historical anchors and architectural inspiration only** — never as a starting point to be refined.
3. Lock the architectural decisions BEFORE drafting any sprint:
   - Module list (which tabs exist; AI Stack standalone vs rolled-in resolved upfront)
   - Vending-machine framing (every module: Revenue → COGS → Gross Profit = Module EBITDA → CapEx → Module FCF)
   - IRR engine scope (terrestrial only? Per-unit marginal? Strategic carve-outs for moonshots?)
   - Allocator architecture (cash pool + queue gate + IRR sigmoid; non-module claims reserved before module CapEx)
   - Year horizon (e.g. 2025–2050, columns D:AC)
   - Cross-tab discipline (INDEX/MATCH on labels; no OFFSET; anchor-and-offset for ramps)
   - Calibration targets (locked pre-build, from disclosed financials or the Q4 anchor model)
4. Draft the four constitutional docs in the order above (01 → 02 → 03 → 04). Each cross-references the others.
5. Sprint 0 is the architecture spec itself — it writes the Assumptions tab skeleton and tab list to the workbook. No module work until Sprint 0 is verified.

**The "rebuild from scratch vs refine" decision rule:** If a model has accumulated load-bearing methodology drift across 10+ specs — vending-machine retrofit, IRR engine refactor, allocator circle, OFFSET purge — **rebuild from scratch**. Refining costs more than rebuilding once the stale residue map exceeds 200 cells. The SpaceX V30.5 → Rebuild v2 decision (2026-05-19) is the canonical case study.

---

## II. The five constitutional docs — what each contains

### 01_Lessons_Learned.md — the 23 principles

Synthesized from V30.5 failure modes. Each principle traces to a specific incident. The doc explains *why* the operational rules exist.

**I. Architectural lockings (decide day one or pay cascading retrofit cost)**

1. **Postponed architectural decisions create retrofit cascades.** Lock vending-machine framing, allocator circle, per-sat IRR, Mars/strategic carve-out, internal-transfer mechanics on day one.
2. **Per-sat marginal IRR is the only IRR that works for pre-revenue modules.** Fleet-level IRR traps modules at zero (no fleet → no FCF → no IRR signal → no allocation → no fleet). Per-unit marginal IRR from physics inputs breaks the chicken-and-egg.
3. **Allocator IN/OUT contract is by label, not row number.** `INDEX(Module!D:D, MATCH("label", Module!$A:$A, 0))` — zero hardcoded `=Module!Dxxx` refs anywhere.
4. **The cash queue reserves year-N non-module claims before module CapEx.** Available cash = `Cash BoY − Mars carve-out − OpEx − Corp CapEx − Spectrum CapEx − Taxes`. Module allocation runs AFTER subtraction.
5. **Strategic priority weights are not allocation mechanisms.** The IRR + carve-out architecture does all the work. Strategic preference encodes through which modules are in the queue and how the carve-out is sized — not via a weight knob.

**II. Tab + naming discipline**

6. **Don't build a tab without a locked function.** If a module's function isn't defined and load-bearing in the architecture spec, the tab doesn't exist.
7. **Lock names day one; no renames mid-build.** Tab names, canonical row labels, key concepts named in the architecture spec.

**III. Module conventions (vending-machine framing)**

8. **Module COGS contains direct production costs only.** Constellation/fleet D&A, internal launch services, ground ops, spectrum amortization, terminal COGS, bandwidth services cost, insurance, catch-all. No R&D, SG&A, overhead, taxes, facilities D&A.
9. **Internal transfers count gross at module IRR; eliminate only at Group P&L.** Source books internal transfer revenue, consumer books cost in COGS, Group P&L eliminates the flow once, conservation check verifies match.
10. **Module tabs are owned by module sprints; cross-cutting specs only read.** Group P&L, OpEx, CapEx-aggregation, Valuation all pull from module tabs via INDEX/MATCH but never write to them.

**IV. Formula patterns**

11. **Zero OFFSET formulas, ever.** Dynamic ranges use `INDEX(range, 1) : INDEX(range, N+1)`. OFFSET is volatile, fragile under row moves, opaque, and doesn't compose with LAMBDA/dynamic arrays.
12. **Year-row formulas use anchor-and-offset, not recursive prior-column references.** `$D$anchor × (1+rate)^E$offset` — never `E14 = D14 × (1+rate)` chains.
13. **Year-offset helper row on every tab with year columns.** Static integers 0 through N (D=0, E=1, ..., AC=25). Hardcoded, not chained.
14. **Cross-tab references via INDEX/MATCH on labels.** Same as Principle 3, restated as a formula pattern.

**V. Execution discipline (plugin-side)**

15. **One concept per write; never mix labels, formulas, and formats.** Separate tool calls for column-A labels, year-row formulas, number formats.
16. **`copyToRange` sources are single cells or single contiguous rows only.** Non-contiguous source dicts have undefined tiling behavior.
17. **Delete superseded rows in the same spec that supersedes them.** Never "leave for later cleanup." This is the single largest source of stale residue.
18. **MC ranges captured at input creation; never retrofitted.** Every Assumptions input has its MC range column populated when the row is created (or flagged "structural, locked").

**VI. Verification discipline**

19. **Sanity check failures halt execution. No "proceed and document."** Every sanity check has a quantitative threshold; failure = stop + push back.
20. **Read edge years (2025, 2030, 2040, 2050) at every verification gate.** Never spot-check a single year — edge bugs survive mid-year-only verification.
21. **Label-vs-source scan on every Allocator / Valuation pull.** Every spec ends with a stale-ref scan: each cross-tab cell's source column-A label must match the consumer's labeled concept.
22. **Iterative-calc bistability is real; design within-year cycles deliberately.** Every within-year cycle documented in architecture spec, justified, verified to converge in <10 iterations. Prefer prior-year refs to break circularity.
23. **Calibration targets locked pre-build; outputs hit them within tolerance.** Anchored Q4 figures (or equivalent) form the 2025 calibration set; ±5% tolerance per target; deviation triggers retune, not "audit later."

### 02_Architecture_and_Methodology.md — structural conventions

The single source of truth on every cross-tab connection, IRR formula, conservation identity. Spec authors reference this for structural choices; the doc never gets paraphrased into a spec.

Contains:
- **Tab list** with one-paragraph function statement per tab
- **Module P&L structure** (vending-machine: Revenue → COGS → Gross Profit = Module EBITDA → CapEx → Module FCF)
- **Allocator OUT contract** — the canonical 11 labels every module tab must expose (Total Revenue, COGS, Gross Profit / Module EBITDA, EBIT, CapEx, Module FCF, Spot IRR, Forward IRR Y+2, Blended IRR, Capacity Demand, Capital Deployed)
- **IRR engine** — per-sat / per-launch marginal CF stream: `[−CapEx_per_unit, +FCF_yr1, ..., +FCF_yrN]`. Spot IRR = current year. Forward IRR Y+2 = shifted 2 years. Blended IRR = `(1−w)·Spot + w·Forward`, w = 0.7. Strict IRR>0 cutoff for queue.
- **Cash pool tracker** — `Cash BoY(N) = Cash BoY(N−1) + Group FCF(N−1) + IPO(N)`. FCF already nets OpEx + Corp CapEx + Module CapEx + Taxes.
- **Queue gate** — `Available_for_queue = MAX(0, Cash BoY − Strategic carve-out − OpEx − Corp CapEx − Spectrum CapEx − Taxes)`
- **Strategic carve-out** (e.g. Moon/Mars) — `MAX(floor, prior_FCF × pct)`. Deducted BEFORE queue runs. Pct + floor are MC inputs.
- **IRR-priority sigmoid blend** — `share_i = MAX(IRR_i, 0)^k / Σ MAX(IRR_j, 0)^k`, k = 2. On cash AND kg/capacity queues.
- **Deployment** — `MIN(cash_allocated / per-unit cost, capacity_allocated / per-unit mass, internal demand)`
- **Internal transfers** — at-cost; eliminated at Group P&L; conservation row verifies source = sum of consumers.
- **Vehicle/launch build cost** (if applicable) — forward-aggregate demand-sized non-module cash claim at queue gate. NOT in any module's CapEx.
- **Year-offset helper row** + **Year header** position (e.g. row 4 = year header, row 5 = offset 0..25)
- **Iterative calc** settings: on, with documented iteration count + tolerance + 5x round-trip stability test

### 03_Sprint_Roadmap_and_Verification.md — phase plan

The 12-sprint sequence (or however many the build needs) with per-sprint scope, dependencies, acceptance criteria, and the universal verification protocol.

Contains:
- Sprint sequence (typical SpaceX template):
  - Sprint 0: Architecture spec + Assumptions skeleton + tab list
  - Sprint 1: Assumptions tab populated
  - Sprint 2–N: Module sprints (one module at a time — Starlink, Customer Launch, ODC, AI Stack, etc.)
  - Sprint N+1: Cross-cutting tabs (OpEx, CapEx aggregation)
  - Sprint N+2: Allocator (cash + capacity queues, queue gate, internal flows)
  - Sprint N+3: Group P&L (consolidation, eliminations, conservation checks)
  - Sprint N+4: Valuation (DCF, terminal value)
  - Sprint N+5: Monte Carlo (range layered on every Assumptions input)
  - Sprint N+6: Scenarios (thesis-conditional cuts of the MC distribution — NOT pre-MC point estimates)
- Per-sprint acceptance criteria (read-back cells, calibration targets, conservation checks)
- **Universal verification protocol** (run end of every sprint):
  1. Workbook-wide `#REF!` / `#VALUE!` / `#DIV/0!` scan — zero results
  2. All conservation checks across all years = "OK"
  3. Internal flow conservation (if any) passes
  4. Allocator OUT label-based references resolve correctly
  5. Module Allocator OUT EBITDA = Gross Profit per vending-machine test
  6. Stale-reference scan: every cross-sheet pull's source column-A label matches the consumer's labeled concept
  7. 5x round-trip recalc stability (no value moves >$1mm)
  8. Calibration targets hit within ±5% tolerance
  9. Claude Log entry written to the Claude Log tab on the workbook

### 04_Assumptions_Tab_Spec.md + Build_Plan.xlsx

Cell-by-cell input plan. The xlsx is the actionable build plan; the markdown is the wrapper that explains the structure.

Assumptions tab has 7 columns:
1. Cell ref (e.g. `B14`)
2. Label
3. Base Case value (point estimate)
4. MC Min
5. MC Max
6. MC Distribution (triangle / lognormal / uniform / discrete)
7. Notes (source, calibration anchor, "structural — no MC" flag if applicable)

Every input has its MC range populated **at creation**. Sprint N+5 (MC sprint) wires the engine against the existing register; it does not retro-populate ranges.

### Model Execution Rules.md — the 23 plugin-side rules

See Section V below. These are mandatory for every spec; every spec opens with the Rule Compliance Preamble (Section IV).

---

## III. The standing process rules (locked, non-negotiable)

These rules apply to every sprint spec. Locked 2026-05-20 after the Sprint 0 execution attempt revealed gaps in the original protocol.

1. **Specs are fully self-contained.** A sprint spec references no external XLSX, no external markdown driver files, no filesystem paths. Every input value, every formula, every cell write, every verification anchor lives in the spec body. The plugin executes against the spec alone — it has no filesystem access and cannot read other workbooks or docs. Build Plan content (or any equivalent input table) is inlined as a numbered section within the spec.

2. **Vlad handles all saving.** The plugin does NOT issue save / save-as commands. Vlad pre-names the workbook via Save-As before sending the kickoff prompt; Vlad saves during/after execution. Specs do not include "save the workbook" steps in the execution sequence. Plugin operates on the live open workbook session; verification reads cells from the session directly.

3. **Kickoff prompt includes a setup-confirmation block** confirming (a) the target workbook is open with the correct name, (b) Vlad will handle saving. Plugin's §3.0 pre-flight verifies this block is present.

4. **Don't over-specify the layout.** Leave file-versioning and year-column letter mapping to the plugin's judgement. Spec rows + labels; let the plugin map to year columns. Don't write file-save instructions. Over-prescription forces conflict-resolution round-trips that wouldn't exist if the spec stayed at the logical level.

5. **Spec author chat ≠ Plugin execution chat.** Spec authoring and plugin execution happen in separate Claude chats. Spec chats produce `Sprint_N_Spec.md` in the workspace folder. Plugin chats execute against the live workbook. Both chats append a row to the Claude Log tab when done.

---

## IV. The Rule Compliance Preamble (MANDATORY)

Every sprint spec opens with this 12-box checklist. Plugin execution chats refuse to start work if any box is unchecked without justification. Copy-paste verbatim:

```markdown
## Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md` and the four constitutional docs. Confirm each before execution:

- [ ] **Rule 1** (one concept per write) — section structure separates labels, formulas, formats.
- [ ] **Rule 3 / 23** (formula pattern) — bounded-CAGR / ramp formulas use anchor-and-offset. Year-chained formulas explicitly flagged as Rule 23 exceptions with one-line justification.
- [ ] **Rule 4** (verification gate) — every section has explicit read-back cells (D, I, S, AC) + expected values.
- [ ] **Rule 6** (inline formulas) — every cell write specified with the full Excel formula, not a convention reference.
- [ ] **Rule 10** (no row insertions) — confirm no `insert_row` operations; all new content appended below existing data.
- [ ] **Rule 11** (touch points) — every new line item lists its SUM range / aggregator / conservation check / Valuation pulls.
- [ ] **Rule 12** (label-based cross-tab refs) — any Allocator / Valuation / Group P&L pulls use INDEX/MATCH on label.
- [ ] **Rule 13** (vending-machine test) — no module tab gets R&D / SG&A / overhead / taxes added.
- [ ] **Rule 14** (no hardcoded constants) — every behaviour input lives on Assumptions.
- [ ] **Rule 15** (sanity check halt thresholds) — every sanity check has a quantitative halt condition.
- [ ] **Rule 19** (save-as) — spec names target workbook explicitly. (Reminder: Vlad does the actual save; this just names the target.)
- [ ] **Rule 22** (stale-ref scan) — Valuation + Allocator + Group P&L scan listed in §Verification.

Architecture & Methodology compliance:
- [ ] Module P&L follows vending-machine framing (Architecture §3).
- [ ] Per-sat / per-launch marginal IRR engine (Architecture §5), not fleet-level MFW-IRR.
- [ ] Allocator OUT contract uses canonical 11 labels (Architecture §4.2).
- [ ] Year-offset helper row at row 5 + year header at row 4 on every tab with year columns.
- [ ] ZERO `OFFSET()` formulas; INDEX:INDEX patterns used for dynamic ranges (Principle 11).

If any box is unchecked, the spec author justifies or amends before execution starts.
```

A box ticked "N/A" requires a one-line justification. Plugin execution refuses to write a single cell against an unticked-or-unjustified preamble.

---

## V. The 23 Model Execution Rules (plugin-side discipline)

Grouped into seven sections. Group A is the most-violated; Group G is "as the model grows, this will bite."

### A. Atomic-write discipline

**Rule 1 — One concept per write.** Never mix labels + formulas + formats in a single tool call. Separate writes for: label changes, formula writes, number-format changes, reference rewires.

**Rule 2 — `copyToRange` contract.** Source must be a single cell or single contiguous row. Never a non-contiguous dict.

**Rule 3 — Bounded-CAGR row construction.** Three-step pattern, one row at a time:
1. Write column D anchor explicitly.
2. Write column E with the bounded-CAGR formula referencing D.
3. Copy E across F:AC.
Confirm before starting the next row. **Combined with Rule 23, this becomes the anchor-and-offset pattern.**

**Rule 6 — Inline formulas in spec.** Every cell write specified with the full Excel formula, not a convention reference. Plugin doesn't infer.

### B. Verification gates

**Rule 4 — Mandatory verification gate after each section.** Read back D / I / S / AC for cells just written. Read Group P&L conservation row across all years — every cell must be "OK". Document landing values in spec terms. **This is the single most important rule.**

**Rule 5 — Conservation gate is non-negotiable.** Before declaring section done: conservation row across all years = "OK". Before declaring spec done: full conservation block, document any non-zero residual (target = exact zero within $1mm). Conservation breakage = highest-priority fault. Never accumulate unresolved breakage.

**Rule 16 — Edge-year verification.** Always include 2025, 2030, 2040, 2050. Don't spot-check just the middle.

### C. Order and recovery

**Rule 7 — Deterministic execution order.** Within a spec: (1) Assumptions additions, (2) Module tab changes one module at a time, (3) Cross-cutting tabs, (4) Group P&L rewires, (5) Conservation checks, (6) Diagnostics. If a later step uncovers an earlier-stage error, stop, return, fix, re-verify everything downstream.

**Rule 8 — Pre-existing out-year breakage is its own scope.** Specs don't fix pre-existing issues unless explicitly targeting them. But specs document whether their changes interact with out-year breakage.

**Rule 9 — When in doubt, ask.** A cell doesn't match the spec, a conservation break the spec didn't anticipate, a formula that requires interpretation → STOP and ask. Don't guess. Cost of a back-and-forth << cost of silent corruption.

### D. Reference safety

**Rule 10 — Row insertions are forbidden in cross-referenced tabs.** Never `insert_row` on any tab referenced by another tab. Append below existing data. Cross-sheet absolute refs break silently when rows shift.

**Rule 11 — Updating a section means updating its SUM ranges and conservation check.** Five touch points per new line item: (1) section Total row, (2) any module aggregator on Group P&L, (3) corresponding conservation check, (4) diagnostic memo rows that derive from the section, (5) downstream tabs with pointers.

**Rule 12 — Allocator OUT references by label, not row number.** `INDEX(Module!D:D, MATCH("label", Module!$A:$A, 0))`. Don't rewrite this with absolute row refs ever.

### E. Architectural guardrails

**Rule 13 — Vending-machine framing is a structural test.** No module tab contains R&D, SG&A, customer service/billing, corporate overhead, taxes. A spec putting any of these on a module tab is rejected. Single exception: Launch internal transfer revenue (intercompany, not OpEx).

**Rule 14 — No hardcoded constants in formula cells.** Any behaviour input (rate, threshold, share, multiplier) lives on Assumptions. True math constants (π, 1e6 unit conversions) allowed inline.

### F. Calibration discipline

**Rule 15 — Sanity check failures halt execution.** Quantitative halt threshold required. Failure = STOP + push back to user with the specific check that failed and actual vs expected. Never "proceed and document."

**Rule 16 — Edge-year verification.** (See Group B.)

### G. Conventions and robustness

**Rule 17 — Memo rows flagged.** Start with "Memo:" in column A, excluded from any SUM range, italic font.

**Rule 18 — Format inheritance.** New rows inherit format from the most similar existing row in the section. Currency-line new row → match existing currency format. Don't leave new rows in "General" format.

**Rule 19 — Source workbook preservation.** Spec names target workbook (e.g. `SpaceX_Model_v2_S03.xlsx`). Vlad handles the actual Save-As. Never overwrite the source.

**Rule 20 — Pre-revenue modules need IFERROR guards on ratios.** Margin / IRR / ROIC / per-unit ratios on pre-revenue modules wrapped in `IFERROR(..., 0)`.

**Rule 21 — Internal flows need elimination + conservation.** Four-step pattern: (1) source books internal transfer revenue, (2) consumer books cost in COGS, (3) Group P&L elimination row subtracts the flow once, (4) conservation check verifies source = sum of consumer COGS for the flow.

**Rule 22 — Stale-reference scan every spec.** End-of-spec scan: every cross-sheet pull's source column-A label matches the consumer's labeled concept. Catches Forward IRR labelled as Blended IRR, pre-tax FCF labelled as Group FCF, etc.

**Rule 23 — Anchor-and-offset formula pattern.** Year-row deterministic ramps reference `$D$anchor` + year-offset cell `E$5`. Never `E14 = D14 × (1+rate)` chains. Genuinely year-chained logic (cumulative CapEx, EoY = BoY + adds − retires, ratchet latches) flagged inline as Rule 23 exception with one-line justification.

---

## VI. Architectural patterns (embed in every spec)

### Vending-machine module framing

Every module's P&L:
```
Revenue
COGS                    ← direct production costs only
Gross Profit
Gross Margin %
─── CapEx
Module FCF (pre-tax, pre-corp-overhead)
```

**Module EBITDA = Gross Profit.** One EBITDA per module. No "True EBITDA" / "EBITDA after corporate overhead" / "EBITDA-after-fleet-D&A" variants.

**In module COGS:** Constellation/fleet D&A, internal launch services cost (at-cost), ground ops, spectrum amortization, terminal COGS, bandwidth services cost (when consuming from another module), insurance, per-launch variable cost (Launch only), other COGS catch-all.

**At Group P&L:** Corporate R&D, corporate SG&A, customer service/billing, facilities & IT D&A, taxes, inter-module eliminations.

### Allocator OUT contract — canonical labels

Every module exposes these rows (Allocator OUT block, typically near bottom of module tab):

1. Total Revenue
2. COGS Total
3. Gross Profit / Module EBITDA
4. EBIT
5. CapEx
6. Module FCF
7. Spot IRR
8. Forward IRR Y+2
9. Blended IRR
10. Capacity Demand (kg or sat-count)
11. Capital Deployed (cumulative)

Cross-tab consumers reference these by `INDEX(Module!D:D, MATCH("label", Module!$A:$A, 0))`. Row numbers may drift; references stay correct.

### Queue gate — the load-bearing cash constraint

```
Available_for_queue(N) =
    MAX(0,
        Cash BoY(N)
      − Strategic carve-out(N)
      − OpEx(N)
      − Corp CapEx(N)
      − Spectrum CapEx(N)
      − Taxes(N)
    )
```

Where `Cash BoY(N) = Cash BoY(N−1) + Group FCF(N−1) + IPO injections(N)`.

The queue gate prevents modules from over-claiming against a phantom capital pool. Without it, the model implicitly finances OpEx from undocumented debt or negative cash.

Iteration: the gate creates a small circular dependency (Module CapEx → Revenue → EBITDA → Taxes → claims → queue → Module CapEx). Excel's iterative-calc handles it; convergence is bounded because OpEx and Taxes have weak marginal sensitivity to incremental CapEx. Verify 5x round-trip stability (no value moves >$1mm).

### Per-sat / per-unit marginal IRR

Module IRR engines compute marginal economics from physics inputs, independent of current fleet count:

```
IRR_per_sat = IRR(
    [ −cost_per_sat,
       +(marginal_revenue_per_sat_per_year − marginal_opex − bandwidth_cost),
       ...repeat for N years (typically N=5 for sat-based modules)
    ]
)
```

**Never seed pre-revenue modules with hardcoded fleet anchors as a workaround for "IRR=0 → no allocation" bugs.** The structural fix is always to refactor IRR to per-unit marginal from physics.

### Anchor-and-offset for ramps

```
Year header row:     row 4    D4=2025, E4=2026, ..., AC4=2050
Year offset row:     row 5    D5=0,    E5=1,    ..., AC5=25     ← hardcoded integers
Anchor cell:         row 14   D14 = =Assumptions!$B$14 (start anchor)

Bounded-CAGR row:
E14 = =IF(Assumptions!$B${cagr}>=0,
            MIN(Assumptions!$B${end}, $D$14*(1+Assumptions!$B${cagr})^E$5),
            MAX(Assumptions!$B${end}, $D$14*(1+Assumptions!$B${cagr})^E$5))
F14:AC14 = copy E14 across (E$5 shifts to F$5, G$5, ... correctly)
```

Every cell in the row references only `$D$14` (locked anchor) and `E$5` (year offset). No `D14`, `E14` cross-column chasing.

### Strategic carve-out (Moon/Mars or equivalent)

For modules that don't earn returns within the modelled horizon but represent strategic intent:

```
Carve-out(N) = MAX(floor, prior_FCF(N−1) × strategic_pct)
```

Floor and strategic_pct are MC inputs (Base Case: $1B/yr floor, 15% strategic pct for SpaceX Mars). Carve-out deducted from cash pool BEFORE the IRR queue runs. NOT in the IRR queue.

Strategic modules do not have IRR engines. Per-mission IRR is a deferred enhancement, not in initial scope.

### Internal transfer mechanics

When module A buys from module B at-cost:

1. **Source module B** books `Internal Transfer Revenue` in its revenue stack (contributes to B's IRR).
2. **Consumer module A** books matching cost in its COGS (reduces A's IRR).
3. **Group P&L Inter-Module Eliminations block** subtracts the flow once.
4. **Conservation check row** verifies `Internal Transfer Revenue (B) = Σ Internal COGS (consumers of B)` at every year.

Module IRR engines see gross flows. Consolidation sees netted flows. Both views are correct.

### Vehicle / launch build cost (when applicable)

If the model has a launch vehicle that serves multiple consumers (Customer Launch, Starlink, ODC, etc.), vehicle build cost is a **forward-aggregate-demand-sized non-module cash claim at the allocator queue gate**. NOT in any single module's CapEx.

```
Vehicle_build_claim(N) =
    SUM(forward-N kg demand across consumers)
  / payload_per_launch
  / launches_per_vehicle_per_year
  × build_cost_per_vehicle
```

Vehicle D&A flows back to consumer modules via at-cost launch services transfer pricing.

### Year horizon

Standard Mach33 horizon: **2025 → 2050, columns D:AC (26 columns).** Locked workbook-wide. Buy-side 5–10 year window is the problem we're modelling around; 25 years gives terminal-value sensitivity room.

Year mapping: D=2025, E=2026, F=2027, I=2030, N=2035, S=2040, X=2045, AC=2050.

### MC discipline

Every Assumptions input has its MC range populated **at creation**. Assumptions tab columns: Cell ref, Label, Base Case, MC Min, MC Max, MC Distribution, Notes.

**Anything arbitrary is MC.** Stubs, assumed economic lives, blend weights, growth rates, multipliers, overhead %, initial seeds — all become MC ranges. If a stub is truly grounded (disclosed financial, regulatory cap, physical constant), flag it "structural — no MC" and skip the range.

Distributions allowed: triangle (default for bounded), lognormal (multiplicative growth), uniform (bounded ignorance), discrete (small finite set). No ad-hoc additions without architecture-spec amendment.

### Scenarios AFTER Monte Carlo, not before

Bear / Base / Bull as point-estimate scenarios pre-MC are arbitrary — three guesses dressed up. **Build MC ranges first; cut scenarios from the distribution.**

Post-MC, scenarios become thesis-conditional cuts of a defensible distribution (e.g. "the world where Starship $/kg lands above $400 AND Starlink ARPU decays at 8%/yr"). Two-step ordering: (1) MC ranges populated for every arbitrary stub, (2) scenarios as named cuts of those ranges.

---

## VII. The kickoff prompt template

Paste verbatim at the start of every new sprint chat (works for both spec-author and plugin execution chats):

```
We are running Sprint N of the [Model Name] Rebuild v2.
Sprint name: [Sprint name]

Before any work in this chat:

1. Read these files in order:
   - /Users/vladsaigau/Documents/Claude/Projects/[Project Folder]/00_README_Sprint_Kickoff.md
   - /Users/vladsaigau/Documents/Claude/Projects/[Project Folder]/01_Lessons_Learned.md
   - /Users/vladsaigau/Documents/Claude/Projects/[Project Folder]/02_Architecture_and_Methodology.md
   - /Users/vladsaigau/Documents/Claude/Projects/[Project Folder]/03_Sprint_Roadmap_and_Verification.md
   - /Users/vladsaigau/Documents/Claude/Projects/[Project Folder]/04_Assumptions_Tab_Spec.md
   - /Users/vladsaigau/Documents/Claude/Projects/[Project Folder]/Model Execution Rules.md

2. Confirm you understand the constitutional structure:
   - Lessons Learned codifies WHY (23 principles tied to V30.5 incidents).
   - Architecture & Methodology codifies WHAT (structural design + math conventions).
   - Sprint Roadmap codifies WHEN (12-sprint phase plan) and acceptance criteria.
   - Assumptions Tab Spec codifies inputs (anchored historical values + MC ranges).
   - Model Execution Rules codifies HOW (plugin-side discipline, 23 rules).

3. Open this sprint with the Rule Compliance Preamble (template in 00_README §"Rule Compliance Preamble").

4. Reference Sprint Roadmap §X for this sprint's scope, dependencies, and acceptance criteria.

5. Reference Architecture §X for any structural choices this sprint touches.

6. Only after the preamble is filled in and constitutional docs are read: proceed with the sprint work.

If you are a plugin execution chat: do not write a single cell until the Rule Compliance Preamble is confirmed in the spec you are executing.

If you are a spec author chat: do not finalize a spec without the Rule Compliance Preamble at the top.

Current sprint scope: [paste sprint scope summary here]

Setup confirmation:
- Target workbook: [name].xlsx is open with the correct name
- I (Vlad) will handle all saving during/after execution
```

---

## VIII. Plugin execution checklist (quick reference)

Before starting:
- [ ] Read this skill end-to-end + the constitutional docs the kickoff names.
- [ ] Spec has the Rule Compliance Preamble at the top, all 16 boxes ticked (or justified N/A).
- [ ] Confirm target workbook name (Rule 19) — but do NOT save; Vlad saves.
- [ ] Confirm spec lists touch points for every new line item (Rule 11) and halt conditions for sanity checks (Rule 15).
- [ ] Confirm spec is fully self-contained (Standing Rule 1) — no external XLSX or markdown references.

During each section:
- [ ] One concept per write (Rule 1).
- [ ] copyToRange source is single cell or single row only (Rule 2).
- [ ] Ramp formulas use anchor-and-offset (Rule 23) — no prior-column chasing.
- [ ] Bounded-CAGR rows: D anchor → E formula → F:AC copy, one row at a time (Rule 3 + Rule 23).
- [ ] No row insertions in cross-ref tabs (Rule 10).
- [ ] No hardcoded constants (Rule 14).

After each section:
- [ ] Read back D, I, S, AC for the cells just written (Rule 4 + Rule 16).
- [ ] Read Group P&L conservation row across all years — all "OK" (Rule 5).
- [ ] If sanity check fails, halt and push back (Rule 15).
- [ ] Pre-revenue modules: confirm IFERROR guards on ratios (Rule 20).

Before declaring done:
- [ ] Workbook-wide `#REF!` / `#VALUE!` / `#DIV/0!` scan — zero results.
- [ ] All conservation checks across all years = OK.
- [ ] Internal flow conservation (if any) passes (Rule 21).
- [ ] Allocator OUT label-based references still resolve (Rule 12).
- [ ] Module Allocator OUT EBITDA = Gross Profit per vending-machine test (Rule 13).
- [ ] Stale-reference scan: Valuation + Allocator + Group P&L cross-sheet refs verified against labels (Rule 22).
- [ ] 5x round-trip recalc stability test (no value moves >$1mm).
- [ ] Calibration targets hit within ±5% tolerance.
- [ ] Claude Log entry written to the Claude Log tab on the workbook.

---

## IX. Spec authoring checklist (quick reference)

When drafting a sprint spec in a spec-author chat:

- [ ] Open with the Rule Compliance Preamble. Tick all 16 boxes (or justify N/A).
- [ ] Inline ALL inputs, formulas, cell writes, verification anchors. No external file references.
- [ ] Use canonical labels for cross-tab pulls — not row numbers.
- [ ] Specify full Excel formulas (Rule 6), not convention references.
- [ ] Specify D / I / S / AC verification cells with expected values per section.
- [ ] Specify quantitative halt conditions for every sanity check (Rule 15).
- [ ] Enumerate touch points for every new line item (Rule 11): section Total row, Group P&L aggregator, conservation check, diagnostic memo rows, downstream tabs.
- [ ] Enumerate internal flow conservation row if the spec adds an internal flow (Rule 21).
- [ ] Include §Verification at the end with the universal protocol (8 items + Claude Log).
- [ ] Leave year-column letter mapping abstract ("year columns" / "year column for 2025"); the plugin maps.
- [ ] Do NOT include "save the workbook" steps.

---

## X. The Claude Log entry

After every sprint, append a row to the Claude Log tab on the workbook. Format:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| YYYY-MM-DD | N | tab list | One paragraph: what landed, what changed, calibration check results | Deferred items / open questions | Sprint N+1 name |

The Claude Log is the workbook's own history — it survives across spec chats and tracks what each sprint actually accomplished vs what the spec said it would.

---

## XI. When to amend the constitutional docs

The constitutional docs are amendable. They get amended when:

- An architectural decision changes (e.g., AI Stack rolls into ODC after all → update Architecture §10 + §1 tab list).
- A new failure mode surfaces during a sprint that warrants a new Principle in Lessons Learned.
- Sprint roadmap shifts (e.g., a sprint splits into two).
- An input's MC range needs revision based on new data.
- Calibration targets adjust (e.g., new quarterly anchor refreshes).

**Amendment protocol:**
1. Edit the relevant constitutional doc + add an entry to its Amendment Log (bottom of doc).
2. Update related memory entries.
3. Note the amendment in the Claude Log for the sprint that triggered it.

**Never amend silently.** Future sprint chats need to see what changed and why.

---

## XII. Things this skill is NOT for

- One-off Excel cleanup, single-tab spreadsheet work → use the `xlsx` skill.
- Weekly research analyses (research.33fg.com pieces) → use `mach33-weekly-analysis`.
- Thesis framing on existing SpaceX models → use `mach33-thesis-library`.
- Chart/visualisation work → use `mach33-chart-style`.
- Audit/fact-check of model outputs in narrative form → use `mach33-audit`.
- Portal-specific modelling context → use `portal-context` in addition to this skill.

This skill is the load-bearing model-construction methodology. It pairs with the above on a per-task basis but never replaces them.
