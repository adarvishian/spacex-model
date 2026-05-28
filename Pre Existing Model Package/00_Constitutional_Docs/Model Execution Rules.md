# Model Execution Rules

**Status**: Standing document. Every refine spec from Spec 04 onwards references this at the top.
**Author**: Claude (drafted 2026-05-18, after Spec 03 execution went sideways; expanded same day)
**Purpose**: Codify the execution discipline required to make changes to the SpaceX modular valuation model without breaking adjacent cells, conservation, or downstream references.

As the model has grown (15 tabs, 400+ rows on Assumptions alone, conservation chains spanning every tab), informal "just write the changes" execution has produced predictable failure modes: bulk writes corrupting adjacent cells, partial formula propagation leaving rows stuck at start values, broken references that aren't noticed until two refines later, conservation checks that drift unobserved, sanity-check failures glossed over, and hardcoded constants that future refines can't find.

These rules eliminate those failure modes. They are mandatory for execution chats. A spec author must structure changes so the rules are followable.

Rules are grouped into seven sections. Group A is the most-violated; Group G is "as the model grows, this will bite."

---

## A. Atomic-write discipline

### Rule 1 — One concept per write

**Never mix concepts in a single tool call.** Separate writes for:

- **Label changes** (column A text, header rows). One tool call.
- **Formula writes** (a single row's year-row formulas, or a single column's stack of independent formulas). One tool call.
- **Number-format / font / fill changes.** One tool call.
- **Reference rewires** (changing one cell's source pointer). One tool call.

Never:
- Write labels and formulas in the same `cells` dict.
- Write multiple rows' formula patterns in one write (especially if some rows use bounded-CAGR and others use simple constants — these are different patterns and must be written separately).
- Mix label restorations with new formula writes.

**Why this rule.** The Spec 03 execution disaster was caused by a single `copyToRange` whose `cells` dict mixed column-A labels with column-D formulas. The tool interpreted the bounding box as the source pattern and tiled labels into column D, overwriting the new formulas. Splitting the operation into three writes (labels first, then D-column anchor formulas, then range expansions) would have prevented the cascade.

### Rule 2 — `copyToRange` contract

**The source of a `copyToRange` must be a single cell or a single contiguous row.** Never a non-contiguous dict.

Valid:
- Source `E14`, destination `F14:AC14`. Tiles the formula across the row. Relative references shift correctly.
- Source `D14:D14`, destination `D14:D17`. Tiles the formula down a column.

Invalid:
- Source dict `{"D14": ..., "D16": ..., "D18": ...}`, destination `D14:AC18`. The tool's behavior with non-contiguous source dicts is undefined and has been observed to corrupt cells outside the intended pattern.

**Why this rule.** Non-contiguous sources turn `copyToRange` into a multi-row block operation whose tiling behavior depends on the tool's bounding-box interpretation. Predictable only for single-cell or single-row sources.

### Rule 3 — Bounded-CAGR row construction pattern

Every row that uses the start-bound CAGR mechanic gets the same three-step construction:

**Step 1 — Write column D anchor explicitly.**
```
D{row} = =Assumptions!$B${start_input}
```
One tool call. Just D.

**Step 2 — Write column E with the bounded-CAGR formula referencing D.**
```
E{row} = =IF(Assumptions!$B${cagr}>=0,
              MIN(Assumptions!$B${end}, D{row}*(1+Assumptions!$B${cagr})),
              MAX(Assumptions!$B${end}, D{row}*(1+Assumptions!$B${cagr})))
```
One tool call. Just E.

**Step 3 — Copy E across F:AC.**
```
copyToRange source=E{row}, destination=F{row}:AC{row}
```

**Do these one row at a time.** Confirm before starting the next row. Do not stack four rows' worth of CAGR construction into one tool call sequence.

**Why this rule.** Spec 03 had four R&D rows requiring this mechanic (Starlink, Launch, ODC, Moon/Mars — though Moon/Mars uses a $-profile not CAGR). Only the Starlink row got the mechanic applied. Launch and ODC stayed flat at start% across all years because the propagation step was skipped. One-row-at-a-time forces the verification.

---

## B. Verification gates

### Rule 4 — Mandatory verification gate after each section

After writing a discrete section of changes (e.g. "OpEx R&D block", "Starlink COGS retune", "Spectrum amortization wiring"), execution must:

1. **Read back the cells just written** in at least four columns: D (2025), I (2030), S (2040), AC (2050). Confirm values match spec expectations.
2. **Read `Group P&L D108:AC108`.** Every cell must = "OK". If any cell shows anything else, **stop and trace** before proceeding to the next section.
3. **Document the landing values in spec terms** (e.g. "Launch R&D 2030 = 8.2%, AC year = 4.0% at floor — matches spec target").

Specs author must enumerate what to read and what to expect. Execution must do the read.

This is the single most important rule. Most bugs in V26 would have been caught by a verification gate at the end of the OpEx section, before moving to Starlink COGS.

### Rule 5 — Conservation gate is non-negotiable

The Group P&L conservation check block (R99–R108) is the model's integrity proof. After any change:

- **Before declaring a section done:** read R108 across all years. Any year ≠ "OK" → stop, trace, fix before continuing.
- **Before declaring a full spec done:** read R99 through R108 across all years. Document any non-zero residual (target = exact zero within $1mm tolerance).
- **Conservation breakage is the highest-priority fault.** A spec is not done if conservation is broken. Push back to the user with the failing check identified.

Never accumulate unresolved breakage. Never "fix it later" — the next spec's diff makes it impossible to isolate which change broke what.

### Rule 16 — Edge-year verification, not just middle years

When reading back values per Rule 4, **always include 2025, 2030, 2040, and 2050** in the verification set. Don't just spot-check the year 2030 column.

Failure modes that only surface at edges:
- 2025 — pre-Starship-commercial; many modules at zero; division-by-zero risk.
- 2040 — terminal-flow tapering; some lines flip sign as ARPU drift compounds.
- 2050 — known Demand Curves out-year breakdown (V26); useful to confirm bug is unchanged.

If a spec only reads 2030, edge bugs survive into the next refine.

---

## C. Order and recovery

### Rule 7 — Deterministic execution order

Within a spec, execution proceeds in a fixed order. Never jump back to an earlier stage without re-running downstream verification.

Standard order:
1. **Assumptions tab additions.** All new inputs first, with stub values.
2. **Module tab changes** (Starlink, Launch, ODC, Lunar Mars, AI Stack) — one module at a time.
3. **Cross-cutting tab changes** (CapEx, OpEx).
4. **Group P&L rewires** (any reference updates).
5. **Conservation checks** (validate everywhere).
6. **Diagnostics + dashboard** (only after conservation passes).

If a later step uncovers that an earlier stage was wrong, **stop the in-progress step, return to the earlier stage, fix it, and re-run verification of every stage from that point forward.** Do not push through.

### Rule 8 — Pre-existing out-year breakage is its own scope

V26 has known pre-Spec-03 issues with years 2041+ (Demand Curves model produces negative revenue, cascading to negative module EBITDA). **Spec patches are not required to fix pre-existing out-year issues** unless the spec explicitly targets them.

But:
- Specs must document whether their changes interact with out-year breakage.
- If a verification step shows out-year numbers that look wrong, document them and confirm they were already wrong in the prior workbook version. Don't blame the current spec.

### Rule 9 — When in doubt, ask

If execution encounters:
- A cell that doesn't match what the spec describes,
- A conservation break that the spec didn't anticipate,
- A formula that requires interpretation,

**Stop and ask the spec author / user.** Don't guess. Don't fix-and-hope. The cost of a back-and-forth is far smaller than the cost of a silent corruption that takes three specs to surface.

---

## D. Reference safety

### Rule 10 — Row insertions are forbidden in cross-referenced tabs

**Never insert rows in any tab that's referenced by another tab.** Append new content below existing rows instead. Specifically:

- Forbidden: `insert_row` operations on Group P&L, OpEx, CapEx, Starlink, Launch, ODC, Lunar Mars, AI Stack, Assumptions, Allocator, Valuation, Dashboard.
- Safe: appending new rows below the existing last-used row of a tab.
- Safe: writing into existing blank rows within a section, as long as no other tab points at those rows.

**Why this rule.** Cross-sheet absolute references (e.g. `Group P&L!D58 = CapEx!D31`) break silently when CapEx gets a new row inserted at R29 — D31 now points at the wrong concept. The bug shows up two refines later as a conservation miss, and tracing it is brutal. The only safe construct is append.

**Exception:** If a row insertion is unavoidable, the spec must enumerate every cross-sheet reference that needs to be repointed, and the patch sequence must update those references *before* the conservation gate. Default answer: don't insert.

### Rule 11 — Updating a section means updating its SUM ranges and its conservation check

When adding a new line item inside an existing section (e.g. a new COGS line on Starlink, a new corp cost line on OpEx), the spec must enumerate and the execution must update:

1. **The section's Total row** (e.g. Starlink R125 "Total COGS" sums R118:R124 — add a row, the SUM must expand to R118:R125).
2. **Any "by module" aggregator on Group P&L** that sums across modules (e.g. R21–R25 module EBITDA, R28–R32 module CapEx).
3. **The corresponding conservation check on Group P&L R99–R107** (e.g. adding spectrum amortization to CapEx!D31 required updating R104 "Module D&A check" to subtract spectrum from the reconciliation side).
4. **Diagnostic memo rows** that derive from the section (e.g. % margin rows, ratio rows).
5. **The Dashboard tab** if it has a pointer at the section.

A new line item lands clean only if all five touch points are updated. Spec authors must enumerate the touch points; execution must hit each one and verify.

**Why this rule.** In V26, the spectrum amortization addition to CapEx!D31 silently broke the R104 conservation check until execution noticed and patched it mid-build. Codifying the touch points up-front prevents that scramble.

### Rule 12 — Allocator OUT references are by label, not row number

The Allocator OUT contract block in each module ties IRR/EBITDA/FCF references to the allocator's capital-deployment logic. Per the load-bearing decision from earlier specs:

- **References within the Allocator tab** that point at module Allocator OUT rows use **label-based** lookups (INDEX/MATCH or named references on the row label), not absolute row numbers.
- **When a spec changes a module's Allocator OUT block** (adding rows, renaming, repositioning), the Allocator tab continues to find the right row via the label.
- **Execution must verify** that after a Allocator OUT change, the Allocator tab still pulls the correct values — read the Allocator pull rows in 2025, 2030, 2040.

Don't rewrite the label-lookup pattern with absolute row references — that defeats the rule and makes every future Allocator OUT change a row-shift hunt.

---

## E. Architectural guardrails

### Rule 13 — Vending-machine framing is a structural test

Every module's P&L stops at Gross Profit = Module EBITDA. **No module tab may contain:**

- R&D (any flavour — vehicle, constellation, ops). Lives on OpEx tab.
- SG&A (sales, marketing, G&A). Lives on OpEx tab.
- Customer service / billing. Lives on OpEx tab.
- Corporate overhead / allocations. Doesn't exist anywhere — it's been retired.
- Taxes. Group P&L only.

**A spec that puts any of these on a module tab violates vending-machine framing and must be rejected.** Spec authors check this before submission; execution checks this before write; verification checks the module Allocator OUT EBITDA = Gross Profit (not some adjusted figure).

The single exception is the Launch module's internal transfer revenue and at-cost transfer logic — that's not OpEx, it's a COGS-eliminating intercompany flow.

### Rule 14 — No hardcoded constants in formula cells

If a number appears in a formula on any tab other than Assumptions, it must instead be a reference to an Assumptions cell. Hardcoded examples that are forbidden:

```
WRONG: =D14 * 0.21                          (tax rate)
RIGHT: =D14 * Assumptions!$B$388

WRONG: =D110 / 1000000                       (unit conversion)
RIGHT: pre-compute the conversion in Assumptions or accept the magic number
       only if it's a unit-only conversion (not a behavior input)

WRONG: =IF(D14>50000000, 0.05, 0.10)         (threshold + rate)
RIGHT: both threshold and rates as Assumptions inputs
```

**Why this rule.** Future refines (especially Monte Carlo) cannot find hardcoded constants without grep. MC ranges only attach to Assumptions cells. Vlad's load-bearing rule "anything arbitrary is MC" requires that arbitrary numbers live in Assumptions where they can be MC-flagged.

**Exception:** True mathematical constants (π, conversion factors like 1e6) are allowed inline. Anything that's a behaviour assumption (rate, threshold, share, multiplier) is not.

---

## F. Calibration discipline

### Rule 15 — Sanity check failures halt execution

When a spec includes a sanity check (e.g. Spec 03 §4.2: "verify implied DTC subs land in defensible range"), and the check fails:

- **Execution does not proceed.** Stop. Document the failure.
- **Push back to the user with the specific check that failed** and the actual vs expected value.
- **Do not "proceed and document"** — that's how 22M DTC subs in 2025 survived V26 execution unchallenged.

The whole point of a sanity check is to catch a calibration miss before it propagates downstream. Ignoring the failure makes the check worthless.

**Spec authors:** When writing sanity checks, specify what "fails" means quantitatively (e.g. "if implied DTC subs > 15M in 2025, halt; the disclosed Starlink figure is ~5M total"). Don't leave the threshold to interpretation.

### Rule 16 — Edge-year verification

*(See Group B above.)*

---

## G. Conventions and robustness

### Rule 17 — Memo rows are clearly flagged

Rows that exist as diagnostics, not as operative line items in any sum, must:

- Start with **"Memo:"** in column A (e.g. `Memo: Implied blended ARPU`, `Memo: Mars/Moon R&D allocation %`).
- Be **excluded from any SUM range** in the section.
- Use **italic font** in the format (so they're visually distinct from operative rows).

**Why this rule.** Without the convention, a future refine sweeps "Mars/Moon R&D allocation memo" into a total and double-counts the dollars. The "Memo:" prefix is a single-character defense.

### Rule 18 — Format inheritance for new rows

When adding new rows in an existing section, copy formatting from the most similar existing row in that section:

- Currency-line new row → match the number format and font of an existing currency line.
- % new row → match the format of an existing % row.
- Header / divider new row → match the format of the section header above.
- Memo new row → italic + grey fill (per Rule 17).

Don't leave new rows in "General" format. Visual inconsistency is the first sign that a row was added without thinking about the section.

**Tool note:** When using `set_cell_range`, set `numFmt` and `font` properties explicitly. When using `execute_office_js`, apply `.numberFormat`, `.font`, `.fill` per cell or range. Don't rely on inheritance.

### Rule 19 — Source workbook preservation

**Never overwrite the source workbook.** Execution always works against a *copy* with the next version name:

- Source: `SpaceX Model V26.xlsx`
- Target: `SpaceX Model V27.xlsx` (or whatever the spec specifies)

If the spec doesn't name a target, the execution chat picks one and announces it. Save-as before the first write, not after the last.

**Why this rule.** Failed executions corrupt the working file. If that file is also the source-of-truth, rollback means re-deriving from an earlier version. Always have a clean source to fall back to.

### Rule 20 — Pre-revenue modules need IFERROR guards on ratios

For any module that's pre-revenue in a given year (Lunar Mars throughout; ODC pre-2030; AI Stack pre-Sprint-10), margin and ratio formulas must be guarded:

```
WRONG: =R98 / R92                            (Gross Margin % when R92 = 0)
RIGHT: =IFERROR(R98 / R92, 0)
```

Same applies to:
- EBITDA Margin %
- ROIC / IRR derivatives
- Per-unit revenue ratios
- Any division by a module revenue or sub count

Without IFERROR, the cell shows `#DIV/0!` which then cascades into Group-level diagnostics and conservation checks.

### Rule 21 — Internal flows need elimination + conservation

Whenever a spec adds a new internal flow between two modules (e.g. launch services from Launch to Starlink, or compute services from ODC to AI Stack):

1. **Source module** books the flow as Internal Transfer Revenue.
2. **Consuming module** books the same dollar value as Internal COGS (or equivalent cost line).
3. **Group P&L Inter-Module Eliminations block** subtracts the flow once (so Group Revenue doesn't double-count).
4. **A conservation check row** verifies: `Internal Transfer Revenue (source) = Sum of Internal COGS (consumers)` at every year. Mismatch = stop.

Forgetting any of the four breaks Group Revenue. The conservation check is the safety net; the spec author enumerates it explicitly.

### Rule 22 — Stale-reference scan every spec

After every spec lands, before declaring done, execution must scan the Dashboard and Valuation tabs for cross-sheet references that may have drifted as the spec's changes propagated. Specifically:

1. Read every cell on **Dashboard** that contains a `'Sheet'!Cell` reference. For each, verify the source cell still holds the concept the Dashboard label claims (e.g. if Dashboard says "Blended IRR" the source cell better be a Blended IRR, not a Forward IRR).
2. Same for **Valuation** tab — every cross-sheet pull verified against its label.
3. Same for **Allocator** tab — every per-module input row's source verified.

If any label/source mismatch is found, halt and report. This is how three material bugs survived in V26.1 (Dashboard "True EBITDA" labels, "Blended IRR" pointing at Forward IRR, Valuation DCF source pulling pre-tax instead of Group FCF).

**Why this rule.** Refine specs touch module tabs heavily. Dashboard and Valuation are downstream consumers. They drift silently across multiple refines because conservation checks live at Group P&L and don't catch label-vs-source mismatches downstream of that. The scan is cheap; the bugs it prevents are not.

### Rule 23 — Anchor-and-offset formula pattern (no neighbour-chasing for ramps)

For any year-row formula computing a deterministic ramp (start%, end%, CAGR; or step function; or any "year N from start" derivation), use the **anchor-and-offset** pattern. Forbidden: the recursive "this year = prior year × growth" form that chains every cell in the row to its left neighbour.

**Required structure:**
1. Each tab has a **Year Offset** helper row near its year header. D = 0, E = 1, F = 2, ..., AC = 25.
2. Year-row formulas reference an absolute **anchor cell** (`$D$14`, the start year) and the offset cell on the same column (`E$5`, the year index).
3. Every cell in the row has the same form. No prior-column references.

**Example — bounded-CAGR (replaces the Rule 3 pattern for deterministic ramps):**

```
D14  = =Assumptions!$B${start_input}             (anchor at start year)
E14  = =IF(Assumptions!$B${cagr}>=0,
            MIN(Assumptions!$B${end}, $D$14*(1+Assumptions!$B${cagr})^E$5),
            MAX(Assumptions!$B${end}, $D$14*(1+Assumptions!$B${cagr})^E$5))
F14:AC14 = copy E14 across (E$5 shifts to F$5, G$5, ... correctly)
```

Every cell in the row references **only** `$D$14` (locked anchor) and `E$5` (year offset). No `D14`, `E14` cross-column chasing.

**Why this rule.** Three concrete benefits:
1. **Row moves don't break formulas.** Move R14 to R30: anchor reference still works because Excel's $-locked references update on move. Recursive prior-column refs don't follow row moves.
2. **Row insertions don't break.** Excel auto-adjusts both styles, but the anchor pattern reads correctly at a glance — every cell does the same thing.
3. **Row deletions don't cascade.** Recursive chains break the whole row on a single deletion. Anchor pattern only loses the deleted row, not the propagation.

**When the recursive form is unavoidable:** Genuinely year-chained logic — `EoY subs = BoY subs + Net adds`, `Cumulative CapEx = prior cumulative + this-year CapEx`, `Net adds = EoY this year − EoY prior year`. These have to chain. Mark them explicitly with a comment in the spec ("Year-chained — Rule 23 exception, intentional").

**Existing formulas that violate Rule 23 are grandfathered** (Rule 7 says don't break working things) but new specs and any rewrites must follow the new pattern. Spec 03.2 retrofits the OpEx bounded-CAGR rows to the new pattern as a demonstration.

---

## How to use this doc

**MANDATORY: Every refine spec from Spec 03.2 onwards must open with this preamble.**

The preamble forces the spec author to attest, and the execution chat to confirm, that the spec is rule-compliant. Without the preamble, the spec is not valid for execution.

```markdown
## Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md`. Confirm each before execution:

- [ ] Rule 1 (one concept per write) — section structure separates labels, formulas, formats.
- [ ] Rule 3 / 23 (formula pattern) — bounded-CAGR / ramp formulas use anchor-and-offset (Rule 23). Year-chained formulas explicitly flagged as Rule 23 exceptions.
- [ ] Rule 4 (verification gate) — every section has explicit read-back cells + expected values.
- [ ] Rule 6 (inline formulas) — every cell write specified with the full Excel formula, not a convention reference.
- [ ] Rule 10 (no row insertions) — confirm no `insert_row` operations; all new content appended below existing data.
- [ ] Rule 11 (touch points) — every new line item lists its SUM range / aggregator / conservation check / dashboard updates.
- [ ] Rule 12 (label-based cross-tab refs) — any Allocator / Dashboard / Valuation pulls use INDEX/MATCH on label.
- [ ] Rule 13 (vending-machine test) — no module tab gets R&D / SG&A / overhead / taxes added.
- [ ] Rule 14 (no hardcoded constants) — every behaviour input lives on Assumptions.
- [ ] Rule 15 (sanity check halt thresholds) — every sanity check has a quantitative halt condition.
- [ ] Rule 19 (save-as) — spec names target workbook explicitly.
- [ ] Rule 22 (stale-ref scan) — Dashboard + Valuation + Allocator scan listed in §Verification.

If any box is unchecked, the spec author must justify or amend before execution starts.
```

**Spec authors:** Paste the preamble above at the top of every spec. Tick the boxes. If a rule doesn't apply (e.g. spec doesn't touch internal flows so Rule 21 N/A), tick it with "N/A".

**Execution chats:** Refuse to execute a spec that doesn't open with the preamble. Confirm each box is ticked before writing a single cell. If a box is "N/A" or unchecked with no justification, push back to the spec author.

**Updates:** This doc is amendable. When a new failure mode shows up, add a rule. Date the amendment.

---

## Quick-reference checklist for execution chats

Before starting:
- [ ] Read this doc.
- [ ] Spec has the Rule Compliance Preamble at the top with all 12 boxes ticked (or justified N/A).
- [ ] Confirm target workbook name (Rule 19).
- [ ] Confirm spec lists touch points for every new line item (Rule 11) and halt conditions for sanity checks (Rule 15).

During each section:
- [ ] One concept per write (Rule 1).
- [ ] copyToRange source is single cell or single row only (Rule 2).
- [ ] Ramp formulas use anchor-and-offset pattern (Rule 23) — no prior-column chasing.
- [ ] Bounded-CAGR rows: D anchor → E formula → F:AC copy, one row at a time (Rule 3 + Rule 23).
- [ ] No row insertions in cross-ref tabs (Rule 10).
- [ ] No hardcoded constants (Rule 14).

After each section:
- [ ] Read back D, I, S, AC for the cells just written (Rule 4 + Rule 16).
- [ ] Read Group P&L D108:AC108 — all "OK" (Rule 5).
- [ ] If sanity check fails, halt (Rule 15).
- [ ] Pre-revenue modules: confirm IFERROR guards on ratios (Rule 20).

Before declaring done:
- [ ] Workbook-wide #REF! / #VALUE! scan (zero results).
- [ ] All conservation checks across all years = OK.
- [ ] Internal flow conservation (if any) passes (Rule 21).
- [ ] Allocator OUT label-based references still resolve (Rule 12).
- [ ] Module Allocator OUT EBITDA = Gross Profit per vending-machine test (Rule 13).
- [ ] **Stale-reference scan**: Dashboard + Valuation + Allocator cross-sheet refs verified against labels (Rule 22).
- [ ] Claude Log entry written.

---

## Amendment log

- **2026-05-18 (initial)** — Rules 1–9 drafted after Spec 03 execution produced material bugs (Launch/ODC R&D stuck at start%, column-D label corruption on Starlink, OpEx denominator off by Hardware Revenue). All rules trace to specific failure modes observed in V26.
- **2026-05-18 (expansion)** — Added Rules 10–21 covering reference safety (Rules 10–12), architectural guardrails (Rules 13–14), calibration discipline (Rules 15–16), and conventions/robustness (Rules 17–21). Grouped rules under section headers A–G. Added Quick-reference checklist at end. Rule 16 (edge-year verification) extends Rule 4 with explicit year coverage. Rule 15 closes the loophole that let V26 ship with 22M DTC subs unchallenged.
- **2026-05-18 (V26.1 audit aftermath)** — Added Rules 22–23 after deep audit of V26.1 surfaced five material bugs that conservation didn't catch (IRR engines blow up in out-years, Valuation DCF pulls pre-tax module FCF, Valuation D&A/EBIT/CapEx refs broken or pointing at non-existent rows, ODC tab still computes "MOVED" concepts, Dashboard "Blended IRR" actually pulls Forward IRR). Rule 22 (stale-ref scan) prevents Dashboard / Valuation drift across multiple refines. Rule 23 (anchor-and-offset formula pattern) replaces neighbour-chasing in deterministic ramps so rows can be moved/reorganized without breaking formulas. Added mandatory Rule Compliance Preamble — every spec from Spec 03.2 onwards must open with the 12-box checklist; execution refuses to start without it.
