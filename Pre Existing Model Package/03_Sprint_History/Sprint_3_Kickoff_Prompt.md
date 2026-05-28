# Sprint 3 Kickoff Prompt — Copy-paste into a NEW chat

This is the kickoff prompt for the Sprint 3 spec-author chat. Copy everything between the `---PROMPT START---` and `---PROMPT END---` markers verbatim into a fresh chat. Before pasting:
1. Confirm V2.4 is the latest workbook with Sprint 2 PASS.
2. Save-As V2.4 → V2.5 so the plugin chat has a clean target.
3. Have the patch doc `Sprint_2_to_3_Patch_F9_Retirement_and_Starship_Ops.md` saved in the workspace folder (the spec author chat will read it).

---PROMPT START---

We are running Sprint 3 of the SpaceX Model Rebuild v2.
Sprint name: Customer Launch module body — F9 + Starship external customer launches, per-launch marginal IRR engine, at-cost internal transfer pricing wired to Sprint 2's Launch Capacity outputs.

Before any work in this chat:

1. Read these files in order:
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/00_README_Sprint_Kickoff.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/01_Lessons_Learned.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/02_Architecture_and_Methodology.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/03_Sprint_Roadmap_and_Verification.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/04_Assumptions_Tab_Spec.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Model Execution Rules.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/2025 Anchors from Q4_25.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_0_Spec.md   (reference — already executed)
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_1_Spec.md   (reference — already executed)
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_2_Spec.md   (reference — already executed PASS; V2.3 → V2.4)
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_2_to_3_Patch_F9_Retirement_and_Starship_Ops.md   (MANDATORY — 5 patches Sprint 3 absorbs into its spec)
   Memory auto-loads the project index (MEMORY.md). Tell me when you've finished reading.

2. Confirm you understand the constitutional structure:
   - Lessons Learned codifies WHY (23 principles tied to V30.5 incidents).
   - Architecture & Methodology codifies WHAT (structural design + math conventions).
   - Sprint Roadmap codifies WHEN (12-sprint phase plan) and acceptance criteria.
   - Assumptions Tab Spec codifies inputs (Q4'25-anchored 2025 values + MC ranges).
   - Model Execution Rules codifies HOW (plugin-side discipline, 23 rules).
   - The 00_README "Standing process rules" section (locked 2026-05-20) is mandatory: specs are fully self-contained (inline every value, no external XLSX/MD reads), Vlad handles all saves (no plugin save commands), kickoff prompt carries a setup-confirmation block.

3. Open the Sprint 3 spec with the Rule Compliance Preamble (12-box checklist template in 00_README §"Rule Compliance Preamble").

4. Sprint 3 scope: full build of the Customer Launch module body per Sprint Roadmap §3 Sprint 3. Per Architecture §1, §3, §4 this is the SECOND module (tab #4 in sheet order, after Launch Capacity). It IS a P&L module — vending-machine framing applies (Revenue → COGS → Module EBITDA → CapEx → Module FCF, NO R&D / SG&A / overhead / taxes). Allocator IN/OUT contract is the canonical 11 rows (Architecture §4.1, §4.2). Per-launch marginal IRR engine per Architecture §5 (external customer launches only, not internal at-cost transfers — §5.2). Internal transfer revenue line is built but reads 0 until Sprints 4 + 5 + 7 populate consuming-module launch services COGS rows (Architecture §7.1 four-step pattern).

   **Acceptance per Sprint Roadmap §6.2:**
   - F9 customer launches 2025 = 38.58 ±2 (Q4'25 anchor)
   - F9 customer revenue 2025 = $4,290M ±5% (Q4'25 anchor — drives Group Revenue 2025 calibration in Sprint 9)
   - F9 customer launch price 2025 = $111M ±5% (Q4'25 Earth!R132)
   - Starship customer revenue 2025 = $0 exact (pre-commercial; first commercial flight H2 2026 at earliest, full reusability from 2027)
   - Per-launch Blended IRR 2025 in 8-25% range (external customer economics, not fleet-level)
   - Module FCF 2025 captured (pre-tax, pre-corp per vending-machine framing)

5. **Patches to absorb into Sprint 3 spec (FROM `Sprint_2_to_3_Patch_F9_Retirement_and_Starship_Ops.md`):**
   - **Patch D (FIRST in execution sequence — Sprint 2 execution fixes)**: extend R71 on Launch Capacity to E:AC flat (was D-only — caused R77 Blended $/kg = 0 in 2026+); extend Starship year-chained rows R24/R27/R28 to E:AC (D-only currently — masks Sprint 10's vehicle build claim). 6 plugin operations, <5 min.
   - **Patch A (F9 retirement engine overhaul)**: replace flat 6/yr R62 with launch-driven retirement mirroring Q4'25 Earth!$B$30 = 0.01 retirement rate per launch. New Assumptions row `F9 retirement rate (% of launches/year)` = 0.01 (Base) with MC [0.005, 0.02].
   - **Patch B (F9 demand-driven launch wiring)**: replace R64 2027+ linear decay stub with `MIN(fleet × cadence, F9 customer demand + Starlink V2 internal demand)`. Customer Launch publishes `F9 customer launches per year` as a canonical output row. Starlink (Sprint 4) will publish V2 BB/DTC internal launches; IFERROR-0 wrapper handles the Sprint 3-only state.
   - **Patch C (Starship per-launch ops cost)**: SUPERSEDED by Patch E §6.13. Do NOT add a standalone $5M ops row to Assumptions.
   - **Patch E §6.13 (LAST in execution sequence — Starship cost mechanic overhaul)**: split-cost-curve canonical formulation. Two separate Wright's Law curves: manufacturing ($90M anchor, 15% learning, amortized over reuses) + ops+fuel+refurb ($12M anchor, 10% learning, per-launch). Both decline with scale. Booster/ship split (60/40 Mach33). Exposes TWO at-cost rates: R40 fully-reusable (canonical, LEO ops — Sprint 3 reads this for external Starship customer launches) + R41 ship-expended booster-only (Sprint 7 Lunar Mars). Includes Q4'25 §6.12 amendments: variant mix R46 step function at 2027, payload year-row (100K → 200K → 250K cap), MC ranges throughout. DELETES R34 ship refurb % from Assumptions (folded into ops+fuel+refurb curve). Updates R32 to $54M, R33 to $36M (Mach33 booster/ship split).

   The Sprint 3 spec author MUST integrate all five patches into the Sprint 3 spec at draft time per §5.1–§5.5 of the patch doc. Plugin executes Patches D → A → B → E §6.13 → Sprint 3 module body in that order.

6. Reference Architecture §1 (Customer Launch tab function), §3 (vending-machine framing — no R&D / SG&A / overhead / taxes on Customer Launch tab), §4.1 + §4.2 (Allocator IN block at top + 11 canonical OUT rows at bottom — Sprint 1 shells in place, Sprint 3 fills the body in between), §5.1 + §5.2 (per-launch marginal IRR engine — formulation, what goes in net_marginal_revenue_per_launch), §5.4 (strict IRR > 0 cutoff for allocator queue), §7.1 (Customer Launch ↔ consuming modules at-cost transfer — 4-step Rule 21 pattern: source books internal-transfer revenue, consumers book Launch services cost in COGS, Group P&L eliminates once, conservation row verifies). Reference Sprint Roadmap §3 Sprint 3 (scope, dependencies, day budget = 1 day), §5 (universal verification), §6.2 (sprint-specific calibration), §8 (sprint-spec template).

7. Workbook flow: source is `SpaceX Model V2.4.xlsx` (Sprint 2 output, verified PASS per Sprint 2 Claude Log entry — Launch Capacity tab end-to-end, F9 + Starship sections, canonical labels locked, 2025 calibration: F9 launches 171 ✓ F9 fleet EoY 39 ✓ F9 manufactured 17 ✓ Starship launches 0 ✓ Blended $/kg $778 ✓). Target is `SpaceX Model V2.5.xlsx`. Vlad does the Save-As from V2.4 → V2.5 before the plugin chat starts; the plugin operates on the live open workbook and does not save.

8. Known deviations to handle in pre-flight:
   - Assumptions tab year header at row 1 + offset at row 2 (Sprint 0 deviation, locked). Other tabs use row 4 + row 5.
   - Sprint 2 V2.4 has two execution gaps Patch D fixes BEFORE Sprint 3 module body work: R71 D-only (extend to E:AC), R24/R27/R28 D-only (extend to E:AC). Plugin verifies V2.4 state in pre-flight before patching.
   - R34 `Ship refurb % of manufacturing` row will be DELETED from Assumptions as part of Patch E §6.13. Single DELETE operation, plugin executes per Rule 1 as a discrete write before the appends.

9. Standing self-containment rules apply to this spec: inline every Assumptions value the plugin needs (don't tell the plugin to "read Customer Launch §4"; write the canonical label + Base Case + MC range inline). Per Rule 14 no hardcoded behaviour constants in formulas — every parameter resolves to an Assumptions row by label. Customer Launch §4 inputs (Sprint 0 R63 F9 customer launch price year-row, R64 Starship customer launch price year-row, plus Sprint 3-new inputs for customer-launches-per-year year-row, F9-customer-launch-market-growth, Starship-customer-launch-Starlink-vs-customer-split) all inlined in the spec body with labels + values.

10. Before drafting the Sprint 3 spec, surface any open architectural questions the spec needs to answer. Likely questions:
    a. **F9 customer launch demand trajectory** — Q4'25 Earth!R51 has F9 Customer launches 2024 = 45. Sprint Roadmap §6.2 anchors 2025 = 38.58. Trajectory post-2025: declines as Starship displaces F9 customer launches per Q4'25 R56 mechanic. Is this a hardcoded year-row on Assumptions, or derived from market_growth + Starship displacement endogenously? Recommend: year-row anchored to 2025 = 38.58 with annual growth rate input + Starship-displacement carve-out (mirroring Q4'25 R51/R56 logic).
    b. **Starship customer launch price trajectory** — Sprint 0 R64 has $100M starting 2027 declining 8%/yr (V30.5 R196 trajectory). Q4'25 Earth!R133 had $266M in 2025 (pre-commercial synthetic) declining to $77M by 2035. Confirm Sprint 0 R64 baseline or adjust to Q4'25 trajectory?
    c. **Starship customer launches per year mechanic** — Q4'25 R56 has Starship Customer = MIN(market demand, Starship Unused Capacity post-Starlink-and-Compute). Sprint 4 (Starlink) and Sprint 5 (ODC) haven't fired yet at Sprint 3 time — so unused capacity for Sprint 3 verification reads as max-Starship-capacity (Sprint 4/5 demand = 0). Recommend: same MIN mechanic, with Sprint 3 placeholder Sprint 4/5 demand = 0 via IFERROR wrappers (will light up endogenously in those sprints).
    d. **Per-launch IRR engine for Customer Launch — external launches only** (per Architecture §5.2 + §7.1: "Customer Launch IRR: per-launch marginal IRR on external customer launches only. External economics; internal at-cost transfers don't contribute IRR signal"). Confirm: IRR cashflow stream uses (external_market_price − at_cost_rate) as net marginal revenue per launch, with N = endogenous launch service life (e.g., booster lifetime reuses ÷ cadence).
    e. **At-cost transfer rate reads** — Customer Launch's `Launch services cost` line (internal-transfer COGS for Sprint 4/5/7 to read) — does it equal the at-cost rate from Launch Capacity (R71 for F9, R40 for Starship LEO, R41 for Starship Moon/Mars), or does Customer Launch add a markup? Per Architecture §7.1: "Customer Launch P&L: External revenue at market price + Internal transfer revenue (sum of internal launches consumed × at-cost rate)." No markup — passes the at-cost rate through unchanged. Sprint 4/5/7 read from Customer Launch by canonical label, not from Launch Capacity directly. This is the conservation invariant for Group P&L eliminations.
    f. **Lifetime N for the per-launch IRR cashflow stream** — Architecture §5.1 says "Customer Launch endogenous from cadence × lifetime reuses." For F9 customer launches: F9 cadence per booster (R51 = 12/yr) × booster lifetime reuses (R50 = 50) = 600 launches over the booster's life, ÷ 12/yr = 50 years. Too long for an IRR cashflow stream. Recommend: clamp N at 10 years (or use the assumption-level cap `MFW-IRR economic life clamp MIN` from Sprint 0 R22 = 1 / MAX yet TBD). Confirm with Vlad before locking.

    Use AskUserQuestion to clarify with me before locking the spec.

11. Only after the preamble is filled in and constitutional docs are read: proceed with drafting Sprint_3_Spec.md to the workspace folder. Mirror the Sprint 0 / Sprint 1 / Sprint 2 spec structure: §1 Rule Compliance Preamble, §1.5 Pre-execution setup, §2 Framing, §3 Scope (with §3.0 pre-flight, §3.1 patch-absorption summary, §3.2 patches D + A + B + E §6.13 execution, §3.3 Customer Launch module body cell-by-cell build, §3.4 per-launch IRR engine, §3.5 Allocator OUT contract wiring), §4 Verification gate (universal + §6.2 Sprint 3 calibration), §5 Claude Log entry template, §6 Don't touch, §7 Open thread, §8 Execution sequence (Patch D → A → B → E §6.13 → Customer Launch module body → verification), §9 Amendment log.

If you are a spec author chat: do not finalize a spec without the Rule Compliance Preamble at the top and without confirming with me that the load-bearing methodology choices in step 10 are locked, especially question (f) — IRR cashflow stream lifetime N. The 5 patches are LOCKED (Vlad reviewed + approved 2026-05-20) — do not re-litigate them, just absorb into Sprint 3.

Current sprint scope: Customer Launch module body — F9 + Starship external customer launch volumes + prices + revenue, internal at-cost transfer revenue placeholder (lights up when Sprint 4/5/7 populate Launch services COGS), per-launch marginal IRR engine (external customers only), full Allocator OUT contract wired. Plus Patches D/A/B (Launch Capacity tab amendments) + Patch E §6.13 (Starship cost mechanic overhaul on Launch Capacity + Assumptions). 2025 calibration: F9 customer launches 38.58 ±2, F9 customer revenue $4,290M ±5%, Starship customer revenue $0 exact, per-launch Blended IRR 8-25% range.

---PROMPT END---
