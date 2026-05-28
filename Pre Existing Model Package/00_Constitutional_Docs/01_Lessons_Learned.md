# Lessons Learned — Constitutional Document for SpaceX Model Rebuild v2

**Status**: Constitutional. Locked 2026-05-19.
**Source**: Synthesized failure modes from the 35-spec V30.5 build (Sprint 0 through Refine Spec 09). Each principle traces to a specific incident.
**Purpose**: Every architectural decision, every sprint spec, every plugin write checks against these principles. The doc prevents repeating drift that took 11 days of build time + 9 refine specs to surface.

This doc is the *why*. `Model Execution Rules.md` is the operational *what to do*. Where they overlap, this doc explains the failure that motivated each rule.

---

## I. Architectural lockings (decide day one or pay cascading retrofit cost)

### Principle 1 — Postponed architectural decisions create retrofit cascades

**The rule:** Methodology that's load-bearing across multiple modules gets locked in the architecture spec on day one. Don't discover it through failure.

**Tied to:** Vending-machine framing arrived at Refine Spec 01 — eleven days into the build. Every module tab had to be retrofitted to strip R&D, SG&A, corporate overhead, and taxes. ODC R87/R92/R93 retained live "MOVED TO GROUP P&L" formulas computing $13B of overhead in 2030 (V26.1 audit M4). Cleanup took Spec 03.2. The Allocator circle closure arrived Spec 06+07 — Sprint 5's sigmoid + Layer 3 sweep had to be killed, rows R83-R104 cleared, the legacy R10-R21 block on Assumptions blanked. Per-sat marginal IRR arrived Spec 08/09 — fleet-level MFW-IRR had to be retired, NIC base inputs decorated. Three load-bearing methodologies, each requiring 3-5 sprints of retrofit.

**How to apply in rebuild:** The architecture spec (Sprint 0 of v2) locks: vending-machine P&L, allocator circle with queue gate, per-sat marginal IRR for all deployable-unit modules, Mars carve-out, internal-transfer mechanics. No sprint deviates without updating the architecture spec first and explaining why.

---

### Principle 2 — Per-sat marginal IRR is the only IRR that works for pre-revenue modules

**The rule:** Every module with deployable units uses per-sat / per-launch marginal IRR computed from physics inputs, independent of current fleet count.

**Tied to:** Fleet-level MFW-IRR with NIC base = `MAX(CumCapEx − CumD&A, 1)` trapped ODC at IRR = 0 forever. No fleet → no FCF → no IRR signal → no allocation → no fleet. Same trap for Starlink V3 BB pre-launch. Spec 08 Patch P and Spec 09 Patch M finally fixed by formulating IRR per marginal unit: `IRR(IF(SEQUENCE(1,N+1)=1, −cost_per_sat, net_marginal_revenue_per_sat_per_year))`. The chicken-and-egg disappears because per-unit economics don't depend on fleet count.

**How to apply in rebuild:** Starlink (per-vehicle: V2 BB, V2 DTC, V3 BB, V3 DTC), ODC (per-sat), Customer Launch (per-launch) all use this pattern. Moon/Mars is strategic carve-out (no IRR engine). AI Stack uses per-product marginal IRR if standalone. Never seed pre-revenue modules with hardcoded fleet anchors — the `feedback_per_sat_irr_no_seed` memory codifies this.

---

### Principle 3 — Allocator IN/OUT contract is by label, not row number

**The rule:** Every cross-tab reference uses `INDEX(Module!D:D, MATCH("label", Module!$A:$A, 0))`. Zero hardcoded `=Module!Dxxx` row-number references anywhere.

**Tied to:** Sprint 0 fixed every module's Allocator OUT block at rows 200-212. Sprint 3.5 inserted 8 rows on ODC, shifting its OUT block to 208-220. Every cross-tab reference using `=ODC!D210` silently pointed at the wrong concept — could be EBITDA instead of Blended IRR. Spec 03.2 S1 retrofitted Allocator's IRR pulls (R40-R44), SPW pulls (R47-R51), capacity demand pulls (R64-R68), and Layer 3 reads — five separate retrofit passes. V26.1 audit Mistake M5 — Dashboard "Blended Starlink IRR" actually pulled Forward IRR because it was hardcoded at `Starlink!F209` (Forward) when Blended sat at F210.

**How to apply in rebuild:** Sprint 0 architecture spec defines the Allocator OUT contract as a set of canonical row labels (e.g. "Total Revenue ($mm)", "Blended IRR", "Capital deployed ($mm)"). Every cross-tab pull resolves by `INDEX/MATCH` on these labels. Row numbers may shift across sprints; references stay correct.

---

### Principle 4 — The cash queue reserves year-N non-module claims before module CapEx

**The rule:** Available cash for the IRR queue = `Cash BoY − Mars carve-out − OpEx − Corp CapEx − Spectrum CapEx − Taxes`. Module CapEx allocation runs AFTER this subtraction.

**Tied to:** Sprint 5's sigmoid distributed all available cash to modules by IRR weight, ignoring that year-N also needed funding for OpEx, Corporate CapEx, Spectrum acquisition (EchoStar), and Taxes. Result: modules could over-claim against a phantom capital pool that didn't reflect real cash availability. Spec 06+07 added the queue gate at Allocator R115/R117. The `feedback_queue_gate_for_non_module_claims` memory codifies this as load-bearing.

**How to apply in rebuild:** Sprint 0 architecture locks the cash pool tracker: `Cash BoY = prior Cash BoY + prior Group FCF + IPO`. Non-module claims reserved before queue. IRR queue allocates against the remainder. Within-year circularity (OpEx depends on revenue which depends on CapEx which depends on queue) handled via iterative calc; documented in architecture spec.

---

### Principle 5 — Strategic priority weights are not allocation mechanisms; the IRR + carve-out architecture does all the work

**The rule:** The cash and capacity queues allocate by IRR-priority sigmoid blend. Strategic preferences encode through (a) which modules are in the queue at all, (b) the Mars/Moon strategic carve-out off the top.

**Tied to:** Sprint 0 introduced Strategic Priority Weights (5/4/3/2/1) for each module. Sprint 5 used them as floor multipliers in the sigmoid. Spec 06+07 retired the mechanism but kept the weight references "decorative" (Allocator R47-R51 still resolve but feed nothing). Three sprints' worth of mechanism for a concept that didn't survive the architecture review.

**How to apply in rebuild:** No SPW column on Assumptions. No SPW row on any module's Allocator OUT. Allocation is pure IRR + Mars carve-out. If a future spec wants strategic preference, it argues for adding the module to the queue or sizing the Mars carve-out — not for adding a weight knob.

---

## II. Tab + naming discipline

### Principle 6 — Don't build a tab without a locked function

**The rule:** If a module's function isn't defined and load-bearing in the architecture spec, the tab doesn't exist in the workbook.

**Tied to:** ISM tab built Sprint 0 (because it was on the original module list), cut Sprint 5. Dashboard built Sprint 0 with charts and Starlink legacy view, deleted 2026-05-19 after V26.1 audit found three bugs in its cross-tab pulls (M5, S4, S3). AI Stack tab built as decorative skeleton, stayed dormant for 35 spec days because the Mach33 submodel hadn't shipped. Each abandoned tab generated stale cross-tab refs that subsequent specs had to either route around or clean up.

**How to apply in rebuild:** Sprint 0 architecture spec enumerates the tab list. Each tab has a one-paragraph function statement. Tabs not enumerated don't get built. AI Stack standalone-vs-rolled-into-ODC must resolve in the architecture spec before Sprint 0 ships.

---

### Principle 7 — Lock names day one; no renames mid-build

**The rule:** Every tab name, canonical row label, and key concept named in the architecture spec. No renames during the build.

**Tied to:** `Starship Capacity` → `Launch Capacity` (Sprint 2 rename — broke cross-tab refs that hadn't yet been INDEX/MATCH'd). `Starlink Module` → `Starlink` (Sprint 0 rename of V9 tab — Excel auto-updated most but not all). `Launch` → `Customer Launch` (renamed 2026-05-19 — Spec 09 had to add a verification scan for `Launch!` references). Three different EBITDA labels coexisted on different module tabs: "True EBITDA" on Starlink, "EBITDA after corporate overhead" on Launch, "EBITDA-after-fleet-D&A" on ODC. V26.1 audit S4 had to relabel two Dashboard cells.

**How to apply in rebuild:** Architecture spec includes a canonical glossary: tab names (e.g. `Customer Launch` not `Launch`), Allocator OUT contract labels ("Module EBITDA" — single canonical EBITDA, no "True" or "after-overhead" variants), section headers. Every plugin sprint references the glossary. Any proposed rename requires updating the architecture spec first.

---

## III. Module conventions (vending-machine framing)

### Principle 8 — Module COGS contains direct production costs only — nothing else

**The rule:** Module P&L is Revenue → COGS → Gross Profit = Module EBITDA → CapEx → Module FCF. No R&D, SG&A, corporate overhead, taxes, or facilities D&A on any module tab.

**Tied to:** Original Sprint 2-9 build placed R&D, SG&A, and corporate overhead allocation on every module tab. Refine Spec 01 killed all of it. But ODC R87 ("MOVED TO GROUP P&L — corporate overhead") retained live formulas computing $13,041M in 2030 (V26.1 M4). Same for ODC R92 (Taxes $2,201M) and R93 (EBIT after tax $8,278M). These didn't feed Allocator OUT — but they violated the vending-machine framing structurally and risked future accidental rewiring.

**How to apply in rebuild:** Every module tab is structurally identical: Allocator IN block at top, module body (Revenue, COGS, Gross Profit = Module EBITDA, CapEx, Module FCF), Allocator OUT block at bottom. No exceptions. The `project-vending-machine-framing` memory codifies this. Module COGS contains exactly: constellation/fleet D&A (Starlink, ODC), launch services cost (internal at-cost transfer), ground ops, spectrum amortization (Starlink BB only), terminal COGS (Starlink), bandwidth services cost (ODC pays Starlink), insurance, other COGS catch-all. Nothing else.

---

### Principle 9 — Internal transfers count gross at module IRR; eliminate only at Group P&L

**The rule:** When module A buys from module B at-cost, module A books the cost in COGS (reduces A's IRR), module B books matching internal-transfer revenue (contributes to B's IRR). Group P&L eliminates the flow once so consolidated Revenue and FCF aren't double-counted.

**Tied to:** Customer Launch ↔ Starlink launch services flow (Refine Spec 01 §3). Customer Launch ↔ ODC same. Starlink ↔ ODC bandwidth flow (Refine Spec 04). Each was set up correctly at module level — gross flows on each side — and eliminated at Group P&L R42-R45. The pattern works. The failure mode: when Sprint 7.5 routed Starship vehicle build cost INTO Customer Launch CapEx, Customer Launch's per-launch IRR distorted because it absorbed all vehicle build cost while only servicing some of the demand. Spec 09 §2.7 fixed by pulling vehicle build out of Customer Launch entirely (non-module cash claim at allocator gate).

**How to apply in rebuild:** Every internal transfer follows the four-step Rule 21 pattern: (1) source module books internal transfer revenue, (2) consuming module books cost in COGS, (3) Group P&L elimination row subtracts the flow, (4) conservation check confirms `Source internal rev = Σ Consuming module COGS for the flow`. Module IRR engines see gross flows; consolidation sees netted flows.

---

### Principle 10 — Module tabs are owned by module sprints; cross-cutting specs only read

**The rule:** A sprint that writes to a module tab is that module's sprint. Cross-tab aggregation specs (Group P&L, OpEx, CapEx, Valuation) read from module tabs but never write to them.

**Tied to:** Sprint 5.6 introduced three helper rows per module (Cumulative CapEx, Cumulative D&A, Net Invested Capital) on each module tab. Refine Spec 02 then had to consolidate D&A reporting on the new CapEx tab while leaving the per-module D&A rows live. The result: D&A computed in one place, displayed in another, with conservation checks needed to reconcile. The architectural concept (separation between calculation owner and aggregation viewer) was sound but wasn't documented as a rule.

**How to apply in rebuild:** Each module's body is defined by its module sprint and only its module sprint. Calculation of D&A, CapEx, COGS, IRR all happens on the module tab. Cross-cutting tabs (Group P&L, OpEx, CapEx aggregation, Valuation) pull values via INDEX/MATCH but contain no calculation logic that drives module behavior.

---

## IV. Formula patterns

### Principle 11 — Zero OFFSET formulas in the workbook, ever

**The rule:** Dynamic ranges use `INDEX(range, 1) : INDEX(range, N+1)` syntax. OFFSET is forbidden.

**Tied to:** V28.1 had ~314 OFFSET cells across 5 module tabs — IRR engines (Pattern P1), retirement lookback (P2), cohort SUMPRODUCT (P3). Spec 05 replaced all 314 with INDEX-based equivalents. Reasons OFFSET is bad: it's volatile (recalc on every cell change anywhere), fragile under row moves (relative offsets don't translate), opaque (`OFFSET(D80, 0, 0, D$79+1, 1)` requires reading five arguments to understand), and doesn't compose with future Excel features (LAMBDA, dynamic arrays).

**How to apply in rebuild:** Architecture spec mandates INDEX-based patterns from day one. The three substitutions:
- `IRR(OFFSET(D80, 0, 0, N+1, 1))` → `IRR(INDEX(D$80:D$90, 1) : INDEX(D$80:D$90, N+1))`
- `OFFSET(D56, 0, -$B$46)` → `INDEX($D$56:$AC$56, 1, COLUMN()-COLUMN($D$56)+1-$B$46)`
- Cohort SUMPRODUCT with two OFFSETs → INDEX:INDEX slices with `MAX(1, ...)` start position

---

### Principle 12 — Year-row formulas use anchor-and-offset, not recursive prior-column references

**The rule:** Every ramp/CAGR formula references an absolute anchor cell + the year-offset row. Pattern: `$D$anchor × (1+rate)^E$offset`. No `D_prev × (1+rate)` chains.

**Tied to:** Original build chained year cells recursively: `E14 = D14 × (1+rate)`, `F14 = E14 × (1+rate)`. Row moves broke the chain. Row insertions cascaded silently. Spec 03 R&D and ODC R&D rows in V26 were stuck at start% across all years because copy-across step was skipped — the recursive chain looked locally consistent at each cell but globally broken. Spec 03.2 introduced static-integer year-offset rows on OpEx (D5=0, E5=1, …, AC5=25), CapEx, Group P&L; ramp formulas became `E14 = $D$14 × (1+rate)^E$5`. Rule 23 codifies this; `feedback_anchor_and_offset` memory codifies it as Vlad's load-bearing preference.

**How to apply in rebuild:** Every tab with year columns gets a year-offset helper row at fixed position (recommend row 5 below the year-header row 4). Every ramp formula uses the anchor-and-offset pattern. Genuinely year-chained logic (cumulative CapEx, EoY = BoY + adds − retires, ratchet latches) is flagged inline as a Rule 23 exception with one-line justification.

---

### Principle 13 — Year-offset helper row on every tab with year columns

**The rule:** Static integers 0 through 25, located directly below the year-header row. Pattern: `D=0, E=1, ..., AC=25`. Hardcoded, not chained.

**Tied to:** Same Spec 03 / Spec 06+07 retrofit history as Principle 12. Originally Assumptions Row 11 was a recursive `=D11+1, =E11+1, ..., =AB11+1` chain. Spec 04 execution accidentally wiped Row 11, cascading #DIV/0! through Assumptions R241/R242 (chip interpolations) → ODC R22 (PFLOPS/sat) → ODC R60 (Fleet PFLOPS) → ODC R64/R65/R73/R77/R82/R83/R84/R85 → Group P&L R108. Spec 04.1 surgical patch restored Row 11. Spec 06+07 Patch B finally replaced with hardcoded integers.

**How to apply in rebuild:** Architecture spec mandates hardcoded-integer year-offset rows on every tab with year columns. No recursive year counters anywhere.

---

### Principle 14 — Cross-tab references via INDEX/MATCH on labels

**The rule:** Every cross-tab pull resolves by `INDEX(Module!D:D, MATCH("Label", Module!$A:$A, 0))`. Zero hardcoded row numbers.

**Tied to:** Same Sprint 3.5 / Spec 03.2 S1 incident as Principle 3. Codified as Rule 12. The `feedback_allocator_contract_by_label` memory codifies this as Vlad's load-bearing preference.

**How to apply in rebuild:** Architecture spec defines the canonical label vocabulary. Every cross-tab pull in every spec resolves by label. If a sprint introduces a new cross-tab pull whose label doesn't exist yet, the sprint either adds the row to the source tab with the canonical label or pushes back to architecture.

---

## V. Execution discipline (plugin-side)

### Principle 15 — One concept per write; never mix labels, formulas, and formats

**The rule:** Separate `set_cell` / `copyToRange` calls for: column-A labels, year-row formulas, number formats. Never combine in one `cells` dict.

**Tied to:** Spec 03 execution disaster — a single `copyToRange` whose `cells` dict mixed column-A labels with column-D formulas. The tool interpreted the bounding box as the source pattern and tiled labels across column D, overwriting newly-written formulas. Cascaded to Bug 2 (R128 duplicate header) requiring Spec 03.1 patch. Codified as Rule 1.

**How to apply in rebuild:** Every sprint spec structures writes as discrete blocks per Rule 1. Plugin chats refuse to execute writes that mix concepts.

---

### Principle 16 — `copyToRange` sources are single cells or single contiguous rows only

**The rule:** Source for `copyToRange` must be one cell or one row. Non-contiguous source dicts have undefined tiling behavior.

**Tied to:** Same Spec 03 incident as Principle 15. Codified as Rule 2. V26 had multiple corruption cases tied to non-contiguous source dicts.

**How to apply in rebuild:** Same as Principle 15 — plugin discipline. Every spec structures `copyToRange` calls with single-cell or single-row sources.

---

### Principle 17 — Delete superseded rows in the same spec that supersedes them

**The rule:** When a methodology is superseded, the spec that supersedes it also deletes the prior rows. Never "leave for later cleanup."

**Tied to:** Sprint 5 sigmoid superseded by Spec 06+07 → rows R20-R37 left in place with cleared formulas and `[Legacy — cleared]` labels. Layer 3 sweep superseded by Spec 06+07 → rows R83-R104 cleared but still present. Sprint 5.6 NIC inputs decorated post per-sat IRR refactor. AI Stack tab decorative post-Spec 06+07. Stale residue accumulated across 35 specs; the stale-map doc catalogues 200-400 cells likely still stale in V30.5. The user's frustration with stale residue motivated the entire rebuild decision.

**How to apply in rebuild:** Every architecture / spec change that replaces a mechanism enumerates the rows to delete from the prior mechanism. Plugin executes both writes in the same sprint. No "later cleanup" sprints scheduled.

---

### Principle 18 — MC ranges captured at input creation; never retrofitted

**The rule:** Every Assumptions input has its MC range column populated when the row is created. Either it's structural (no MC range, locked) or it's MC-tagged with `[min, max, distribution]` at creation.

**Tied to:** Sprint 5.5 added 18 MC-variable inputs flagged for "MC register" → never registered. Sprint 5.6, 6, 7, 7.5, 8, 9 each added more, each deferred to "later housekeeping." Spec 08 Patch S was a narrow retroactive cleanup that still didn't catch everything. Net result in V30.5: no central source of truth for MC samples. The `feedback_arbitrary_inputs_are_mc` memory codifies "anything arbitrary is MC" but the register lag means it's never actually been comprehensive.

**How to apply in rebuild:** Assumptions tab has 5 columns: Cell ref, Label, Base Case value, MC Min, MC Max, MC Distribution, Notes. Every input populated at creation. Sprint 0 architecture spec includes the canonical MC distribution types (triangle, lognormal, uniform, discrete) — no ad-hoc additions.

---

## VI. Verification discipline

### Principle 19 — Sanity check failures halt execution. No "proceed and document."

**The rule:** Every sanity check has a quantitative halt threshold. Failure = stop, push back to user with the failing check.

**Tied to:** Spec 03 §4.2 included an explicit sanity check on implied DTC subscribers — "verify subs land in defensible range." V26 execution computed 22M implied DTC subs in 2025 (disclosed Starlink total subs ~5M, so 4× larger than total Starlink). Execution noted it, proceeded anyway. Bug survived into V26.1 audit (finding S5). Codified as Rule 15 *after* the bug shipped.

**How to apply in rebuild:** Every sanity check in every spec has a quantitative threshold (e.g., "implied DTC subs < 15M; halt above"). 2025 calibration targets from Q4'25 are the primary halt set: Group Revenue must hit $14.65B ± 5%; Group EBITDA $8.69B ± 5%; FCF $3.67B ± 5%; F9 launches 171 ± 5%; etc. Plugin refuses to declare a sprint complete if any halt threshold fires.

---

### Principle 20 — Read edge years (2025, 2030, 2040, 2050) at every verification gate

**The rule:** Every verification block reads at minimum columns D (2025), I (2030), S (2040), AC (2050). Never spot-check a single year.

**Tied to:** Spec 03 R&D + ODC R&D rows in V26 were stuck at start% across all years because copy-across step was skipped. Mid-year-only verification didn't catch it — the start% values looked plausible at 2030. Spec 03.1 patched it. Codified as Rule 16.

**How to apply in rebuild:** Every sprint spec's verification gate lists the four-column read pattern. Plugin executes those reads and records actual vs expected.

---

### Principle 21 — Label-vs-source scan on every Dashboard / Valuation / Allocator pull

**The rule:** Every spec ends with a stale-reference scan: for every cross-tab cell that pulls `=Module!Cxx`, verify the source cell's column-A label matches the consumer's labeled concept.

**Tied to:** V26.1 audit caught five material bugs that the Group P&L conservation block never flagged: Dashboard "Blended Starlink IRR" pulled `=Starlink!F209` which is Forward IRR Y+2 (Blended IRR sits at F210). Valuation "Live Group FCF" sourced from per-module FCFs (pre-tax, pre-corp) instead of Group FCF (post-tax). Valuation "Live Group D&A" pointed at Group FCF row D69. Codified as Rule 22 *after* these bugs shipped.

**How to apply in rebuild:** Every sprint spec includes a Rule 22 stale-ref scan as its final verification step. Dashboard doesn't exist in rebuild → Valuation + Allocator are the surviving consumers; scan both. Each cross-tab pull resolved to its source's column-A label; mismatch = halt.

---

### Principle 22 — Iterative-calc bistability is real; design within-year cycles deliberately

**The rule:** Every within-year cycle is documented in the architecture spec, justified, and verified to converge in <10 iterations. Break circularity with prior-year references where possible.

**Tied to:** V28.1's saved state had Valuation D11 swing 4× across 6 sequential recalcs with no formula changes. Launch S91 IRR moved 0.206 → 0.210 across recalcs. Cause: within-year cycles (Layer 3 sweep ↔ ODC IRR, Sprint 5.5 corporate overhead → revenue → overhead, Sprint 7.5 Wright's Law ↔ build rate, Spec 06+07 OpEx ↔ Module CapEx) compounded under iterative calc. Model became non-deterministic across saves. Codified as `feedback_model_not_deterministic`.

**How to apply in rebuild:** Architecture spec enumerates every within-year cycle, with justification and convergence test. Prefer prior-year references to break circularity (e.g., Mars carve-out uses prior-year FCF, not current-year). Iterative calc is on with a documented iteration count + tolerance. Every sprint verification includes round-trip stability test: recalc 5x, no value should move >$1M.

---

### Principle 23 — Calibration targets locked pre-build; outputs hit them within tolerance

**The rule:** 2025 calibration targets locked before Sprint 1 of the rebuild. Every sprint that produces 2025 outputs must hit the targets within ±5%. Deviation triggers retune, not "proceed and audit later."

**Tied to:** Original build had no anchored 2025 outputs. Sprint 11 ("audit") was supposed to retune Mars/Moon labour productivity to close the 10× BV undershoot vs spec target. But there was no Q4'25 anchor; the spec target itself was speculative. No way to know if the model was right. The user's confidence in V30.5 outputs was correspondingly low. The rebuild has Q4'25-anchored 2025 targets from day one (Group Revenue $14.65B, EBITDA $8.69B, FCF $3.67B, F9 launches 171, etc. — see `project-anchored-assumptions-2025` memory).

**How to apply in rebuild:** Architecture spec includes the 2025 calibration target table. Every module sprint's verification reads its module's 2025 contribution and compares to the target. Group P&L sprint verification reads consolidated 2025 outputs and compares to the full target set. Sprint completion requires all relevant targets hit within tolerance.

---

## How to use this doc

**Architecture spec:** Open with a reference to this doc. Every architectural decision in the spec is justified against one or more of these principles. If a decision violates a principle, the spec author either revises the decision or adds a one-paragraph justification for the exception (and the exception goes into a "Known Drift" section that future audits scan).

**Module / sprint specs:** Open with the Rule Compliance Preamble (Model Execution Rules) and a one-line reference to this doc. Sprint changes are checked against the principles before writing.

**Plugin execution chats:** Refuse to execute a spec that doesn't open with the Rule Compliance Preamble. If a write violates Principles 15-17 (one concept per write, copyToRange contract, delete superseded rows), halt and push back to spec author.

**Verification chats / audits:** Run through Principles 19-23 (sanity halt, edge-year reads, stale-ref scan, round-trip stability, calibration targets) as the standing audit checklist.

---

## Open principles to flag

These are principles I expect to emerge during the rebuild but don't yet have full incident-backing from the prior build:

- **Bandwidth flow conservation discipline** — Refine Spec 04 architecture for Starlink ↔ ODC internal bandwidth. Worked at module level but never battle-tested at scale. Watch for double-counting between bandwidth revenue (Starlink) and bandwidth cost (ODC).
- **Vehicle build cost as forward-demand-sized non-module claim** — Spec 09 architecture. Theoretically correct (vehicle build serves aggregate demand, not Customer Launch alone). May surface load-bearing edge cases when the queue gate competes with module CapEx for limited cash.
- **AI Stack on-top-of-ODC vs standalone** — open architectural question. Once resolved, the principle here probably becomes "modules with at-cost internal supply still get their own IRR engine" (if standalone) or "merging downstream revenue into upstream module simplifies allocator but loses product-level economics" (if rolled).

These get added with concrete incidents as the rebuild surfaces them.

---

## Amendment log

- **2026-05-19 (initial draft)** — Drafted as constitutional doc for Rebuild v2. Synthesized from 35-spec V30.5 build history + V26.1 audit findings + Model Execution Rules genesis history. 23 principles in 6 sections. To be updated as rebuild surfaces additional load-bearing failure modes.
