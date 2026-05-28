We are running Sprint 5 of the SpaceX Model Rebuild v2. Sprint name: **ODC module — per-sat marginal IRR + dual revenue Model A/B + cash-driven deployment + bandwidth services from Starlink Capacity + internal/external compute split with at-cost transfer to AI Stack.**

Before any work in this chat:

1. Read these files in order:
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/00_README_Sprint_Kickoff.md
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/01_Lessons_Learned.md
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/02_Architecture_and_Methodology.md
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/03_Sprint_Roadmap_and_Verification.md
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/04_Assumptions_Tab_Spec.md
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Model Execution Rules.md
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/2025 Anchors from Q4_25.md
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_0_Spec.md (reference — executed PASS)
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_1_Spec.md (reference — executed PASS)
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_2_Spec.md (reference — executed PASS)
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_3_Spec.md (reference — executed PASS)
   * /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_4_Spec.md (reference — executed PASS 14/15 anchors; Constellation D&A flagged for Sprint 4.5)
   * Any Sprint_4.5_Patch_*.md in the project folder (if present — Sprint 4.5 may have landed before Sprint 5 fires; see step 8 below)
   * Any Sprint_3.5_Patch_*.md in the project folder (Customer Launch per-launch IRR amendment — doesn't affect Sprint 5 reads)

   Memory auto-loads the project index (MEMORY.md). Tell me when you've finished reading.

2. Confirm you understand the constitutional structure:
   * Lessons Learned codifies WHY (23 principles tied to V30.5 incidents).
   * Architecture & Methodology codifies WHAT (structural design + math conventions).
   * Sprint Roadmap codifies WHEN (12-sprint phase plan) and acceptance criteria.
   * Assumptions Tab Spec codifies inputs (Q4'25-anchored values + MC ranges).
   * Model Execution Rules codifies HOW (plugin-side discipline, 23 rules).
   * The 00_README "Standing process rules" are mandatory: specs are fully self-contained (inline every value, no external XLSX/MD reads); Vlad handles all saves (no plugin save commands); **specs do NOT name source/target workbook files — Vlad handles versioning per `feedback-no-workbook-names-in-specs` memory lock 2026-05-20**.

3. Open the Sprint 5 spec with the Rule Compliance Preamble (12-box checklist template in 00_README §"Rule Compliance Preamble"). Sprint 5 spec must follow the new standing rule and **omit `Source workbook` / `Target workbook` header lines, omit Rule 19 references that require naming the file, and omit pre-flight workbook-name checks**.

4. **Sprint 5 scope per Sprint Roadmap §3 Sprint 5** (the FOURTH module after Customer Launch, Starlink, Starlink Capacity):

   * **ODC module body (tab #7) — full build.** Sat physical specs (Sprint 0 R145 V2 Compute 140 kW, R147 1,400 kg dry mass, R152 156,000 W solar, R153 480 kg thermal mass); subsystem cost stack via Wright's Law (R155-R162 unit costs + R165 LR-subsystems 15% per doubling; LR-chips = 0 per R164); chip roadmap year-rows (R173 TDP / R174 FP8 / R175 mass / R176 cost — H100 → AI5 → Dojo-3 linear interp); per-sat Model A revenue (energy-anchored CoreWeave baseline with PUE uplift); per-sat Model B revenue (η-anchored billable GPU-hrs × $/GPU-hr); Pr(A)-weighted Expected Revenue (R180 Pr(A) = 0.6); **cash-driven deployment** (NO fixed sat-count year-row — ODC reads Cash Demand from per-sat economics and competes in outer queue per Architecture §9.1); per-sat marginal IRR engine (Architecture §9.4 — N=5 yrs sat-module default per Sprint 0 R20; reads external compute revenue only per §7.3); bandwidth services cost paid to Starlink (reads Starlink Capacity `BB pool at-cost rate` + `DTC pool at-cost rate`); external vs internal compute split (R187 internal share year-row 95%→40% / R188 external share = 1−internal); ODC → AI Stack fully-allocated at-cost compute transfer (Architecture §7.3 locked 2026-05-20 — publishes `ODC at-cost compute rate ($/PFLOP-hr)` for Sprint 6 AI Stack to read); Allocator OUT contract overwrite (Sprint 1 placeholders → live formulas).

   * **Internal Starship launches consumed by ODC** — ODC reads `At-cost launch services rate ($mm/launch)` from Launch Capacity (Sprint 2 + Patch E §6.13 LOCKED canonical label) × ODC Starship launches consumed (computed on ODC tab from sats deployed / sats per Starship launch). ODC publishes `ODC Starship launches (internal)` + `ODC Starship kg demand` canonical labels (Customer Launch R22 + R69 IFERROR-0 reads activate; spec author confirms Sprint 3 reads use these exact strings).

   * **Publishes for downstream consumers** (canonical labels, EXACT strings — verbatim case-sensitive match required per Rule 22):
     - `ODC BB Gbps demand` (year-row) → activates Starlink Capacity R18 IFERROR-0 read
     - `ODC DTC Gbps demand` (year-row) → activates Starlink Capacity R20 IFERROR-0 read
     - `ODC Starship launches (internal)` (year-row) → activates Customer Launch R69 IFERROR-0 read
     - `ODC Starship kg demand` (year-row) → activates Customer Launch R22 IFERROR-0 read
     - `ODC at-cost compute rate ($/PFLOP-hr)` (year-row) → Sprint 6 AI Stack reads
     - Plus standard Allocator OUT 11 canonical rows at 200-210

5. **Acceptance per Sprint Roadmap §6.4:**
   * ODC revenue 2025 = $0 exact
   * ODC sats deployed 2025 = 0 exact
   * ODC fleet end-2025 = 0 exact
   * Per-sat marginal IRR 2025 = 0 or negative (any positive = halt — premature)
   * Bandwidth services cost paid to Starlink 2025 = $0 exact
   * Per-sat marginal IRR converges (no `#NUM!` leaks to Allocator OUT)
   * Allocator OUT 11 canonical rows populated with live formulas

6. **Reference Architecture §1** (tab #7 = ODC + tab inventory), **§3** (vending-machine framing — no R&D/SG&A/overhead/taxes on ODC tab), **§4.1 + §4.2** (Allocator IN/OUT contract — Sprint 1 shells in place, Sprint 5 fills body in between and overwrites OUT placeholders), **§5** (per-sat marginal IRR pattern), **§7.1** (Launch Capacity ↔ ODC fully-allocated at-cost launch services), **§7.2** (Starlink ↔ ODC bandwidth — 4-step Rule 21 pattern — Sprint 5 books ODC bandwidth services cost in COGS; Starlink Capacity reads ODC's bandwidth demand labels activate the Sprint 4 IFERROR-0 wrappers; Sprint 9 Group P&L R106 eliminates), **§7.3** (ODC ↔ AI Stack fully-allocated at-cost compute — ODC publishes `ODC at-cost compute rate ($/PFLOP-hr)` for AI Stack Sprint 6), **§9** (full ODC architecture — §9.1 cash-driven deployment, §9.2 dual revenue Model A energy-anchored + Model B η-anchored with Pr(A) credence, §9.3 external + internal compute split, §9.4 per-sat marginal IRR formula), **§17** (calibration — ODC revenue 2025 = $0).

7. **Workbook flow:** Sprint 5 plugin operates on whatever workbook is open in Vlad's Excel session (Vlad handles versioning entirely outside the spec). **Spec does NOT name workbook files, does NOT include `Source workbook` / `Target workbook` header lines, does NOT include workbook-name pre-flight checks.** Plugin's §3.0 pre-flight starts with: confirm tab positions, confirm year header/offset rows, confirm prior-sprint canonical labels resolve.

8. **MANDATORY PRE-SPRINT-5 SETUP — Sprint 4.5 patch must land BEFORE Sprint 5 plugin fires.** Per memory `project-demand-curves-stub-remove-in-sprint-5` (Vlad lock 2026-05-20 post-Sprint-4-execution): Sprint 4 per-vehicle IRRs run away (Spot 2025 = 99.6%, Blended = 144%, increasing out-years) because without demand-side caps every marginal sat earns the same per-Gbps revenue regardless of fleet saturation. The architectural fix is the proper Demand Curves tab. Sprint 4.5 patch scope:

   (a) **Build Demand Curves tab** at sheet position #14 (per Architecture §1) with four canonical year-rows: `Total BB Gbps demand (Gbps/yr)`, `Total BB price ($/Gbps/yr)`, `Total DTC Gbps demand (Gbps/yr)`, `Total DTC price ($/Gbps/yr)`. All MC triangle-yearrow.
   (b) **Demand-cap mechanic on Starlink revenue.** R120 BB Revenue = `MIN(Available BB Gbps, BB demand Gbps) × BB price / 1e6`; same for R131 DTC. Per-vehicle IRR engines (R212/R217/R222/R227) re-wire to marginal-Gbps × price logic so IRR tapers as fleet supply approaches demand.
   (c) **Delete Assumptions stub rows** at 316-317 (`BB $/Gbps ($/Gbps/yr, year-row)` + `DTC $/Gbps ($/Gbps/yr, year-row)`).
   (d) **Constellation D&A retune** (Sprint 4 §3.3.11 flagged): add legacy V1/V1.5 D&A (~$130M) + facility D&A (~$140M) memo lines so 2025 lands within $707M ±10%.
   (e) **V3 BB Wright's Law on bandwidth-per-sat** (Sprint 4 §3.3.1 deferred): implement WL learning on R17 using cum V3 BB sats running sum.
   (f) **Constitutional doc amendments:** Architecture §1 (re-add tab #14 Demand Curves), §8.4 (revenue = bandwidth × price WITH demand cap), §18 item 5 closed = YES Demand Curves load-bearing with demand cap, §19 amendment log.

   **Sprint 5 spec author chat: confirm with Vlad whether Sprint 4.5 has landed before Sprint 5 plugin fires. If NOT, Sprint 5 spec must either (i) wait until Sprint 4.5 lands, or (ii) absorb Sprint 4.5 as a patch section (Sprint 3-style) at the top of Sprint 5 spec. Recommended: separate Sprint 4.5 first.**

9. **Sprint 5 plugin reads from prior-sprint canonical labels** (verify by INDEX/MATCH in §3.0 pre-flight; halt on any miss):

   * Starlink Capacity tab (Sprint 4): `BB pool at-cost rate ($/Gbps/yr)`, `DTC pool at-cost rate ($/Gbps/yr)`, `Total active BB Gbps`, `Total active DTC Gbps`.
   * Launch Capacity tab (Sprint 2 + Patch E §6.13): `At-cost launch services rate ($mm/launch)` (canonical — fully-allocated per Architecture §7.1), `Total Annual Capacity (kg-to-LEO)`.
   * Customer Launch tab (Sprint 3): No reads — Sprint 5 publishes labels Customer Launch's IFERROR-0 reads consume; Sprint 5 spec author confirms Customer Launch R22/R69 still use the exact strings `ODC Starship launches (internal)` + `ODC Starship kg demand` (Sprint 3 line 585 + 780).
   * Demand Curves tab (Sprint 4.5): not read directly by Sprint 5 but pre-flight confirms tab exists post-Sprint-4.5.
   * Assumptions §6 ODC inputs: R145-R188 (all sat physical, subsystem, Wright's Law, chip roadmap, dual revenue, internal/external split parameters). Spec inlines every input by canonical label, not row number.

10. **Standing self-containment rules apply** (locked 2026-05-20): inline every Assumptions value the plugin needs (don't tell the plugin to "read Architecture §9"; write canonical labels + Base Case + MC ranges inline). Per Rule 14 no hardcoded behaviour constants in formulas. Per `feedback-no-workbook-names-in-specs` memory: spec omits all workbook filename references.

11. **Carry these execution lessons from Sprint 4** into Sprint 5 spec:
    * **INDEX col_num=0 spill bug** (per memory `feedback-index-col-zero-spills`): any backward-looking INDEX with computed `col_num` (year offset arithmetic) gets explicit `IF(col_num < 1, 0, INDEX(...))` guard. Sprint 5 ODC has launch-cohort retirement + chip roadmap year-row reads + per-sat IRR forward references — all candidates for the trap. Spec author enumerates which rows could trigger.
    * **Iterative calc ON workbook-wide** (per memory `project-iterative-calc-enabled-2026-05-20`): pre-flight verifies 100 iter / 0.001 tol still on. Sprint 5 introduces a new within-year cycle: ODC bandwidth claim (Gbps) → Starlink Capacity Available Gbps → BB pool at-cost rate → ODC Bandwidth services cost → ODC EBITDA → ODC per-sat IRR → ODC cash demand → next iteration's ODC bandwidth claim. Document in spec §2 Framing as expected cycle; convergence verified via 5x round-trip recalc.
    * **Mac Excel range.values caching** when iterative calc is off — Sprint 5 verification gate forces a `application.calculate` then reads fresh values.

12. **Open architectural questions Sprint 5 needs to lock via AskUserQuestion (BEFORE drafting the spec body):**

    a. **ODC sat physical config** — keep V2 Compute 140 kW per sat (Sprint 0 R145, Vlad-confirmed 2026-05-19 over Q4'25's 70 W/kg) or revisit? Recommended: keep 140 kW.

    b. **Cash-driven deployment ask year-row mechanic** — Architecture §9.1 says "ODC reads Cash Demand from per-sat economics and competes in outer queue. Wanted deployment in early years = 0." How does Sprint 5 publish ODC's cash demand for Sprint 10 Allocator to consume? Options: (i) large-default cash ask year-row mirroring Starlink R142 (lets allocator gate via queue), (ii) calibrated cash demand tied to forward fleet target (e.g., 1,000 sats by 2030 → cash demand = 1,000 × per-sat cost in 2027), (iii) per-sat IRR-driven (mask = IF(IRR > 0, large default, 0)). Recommended: (i) large default — same pattern as Starlink R141/R142 Sprint 0 inputs.

    c. **Bandwidth claim derivation** — Sprint 0 R138 Gbps/(GWh/yr) = 0.05 PLACEHOLDER + R139 BB-share 0.50 PLACEHOLDER. Sprint 5 either: (i) accept placeholders as MC-wide stubs, (ii) calibrate to Mach33 thesis on per-PFLOP bandwidth requirement, (iii) ask Vlad for new Base Case anchors. Recommended: (i) keep as MC-wide; flag for post-Sprint-12 calibration retune.

    d. **Per-sat marginal IRR — confirm Architecture §9.4 formula structure** with N=5 yrs CF stream, IFERROR(IRR(...), -1) wrapper, per-sat Model A revenue + per-sat Model B revenue Pr(A)-weighted, per-sat ground ops + insurance + other COGS, per-sat bandwidth cost paid to Starlink, per-sat launch services cost paid to Customer Launch (fully-allocated at-cost rate × ODC Starship launches per sat). Per Architecture §7.3 IRR reads EXTERNAL revenue only (internal AI Stack transfer at-cost; doesn't contribute to IRR signal). Confirm.

    e. **Internal vs external compute split year-row** — Sprint 0 R187 already populated as Base Case (95% internal 2025 → 40% by 2050). Confirm OK.

    f. **AI Stack at-cost compute rate formula** — fully-allocated per Architecture §7.3: rate per PFLOP-hr = (ODC annual fully-allocated cost) / (ODC total annual PFLOP-hrs produced). Fully-allocated cost = annual sat D&A + launch services cost + bandwidth services cost + insurance + other COGS. Sprint 5 publishes the canonical row `ODC at-cost compute rate ($/PFLOP-hr)` for Sprint 6 AI Stack to read. Confirm formula structure.

    g. **Within-year cycle convergence** — ODC ↔ Starlink Capacity loop documented in Architecture §22 (memory `project-iterative-calc-enabled-2026-05-20` lists the cycle). Convergence target <10 iterations, no value moves > $1M in 5x round-trip recalc. Confirm.

    Use AskUserQuestion to surface these in two passes (max 4 per call). Lock answers before drafting the spec body.

13. **Sprint 5 must publish canonical labels (verbatim, case-sensitive)** that Sprint 4's IFERROR-0 reads consume:

    | Label on ODC tab | Read by |
    |---|---|
    | `ODC BB Gbps demand` | Starlink Capacity R18 (Sprint 4) |
    | `ODC DTC Gbps demand` | Starlink Capacity R20 (Sprint 4) |
    | `ODC Starship launches (internal)` | Customer Launch R69 (Sprint 3) |
    | `ODC Starship kg demand` | Customer Launch R22 (Sprint 3) |
    | `ODC at-cost compute rate ($/PFLOP-hr)` | Sprint 6 AI Stack (future) |

    Spec author confirms exact label strings against Sprint 3 + Sprint 4 IFERROR-0 reads via Customer Launch tab line refs 583-585 + 778-780 and Starlink Capacity R18 + R20 formula reads. Label drift = stale-ref scan halt per Rule 22.

14. **Sprint 5 calibration is intentionally trivial** (2025 ODC revenue = $0; deployment = 0; IRR = 0 or negative). Real ODC dynamics fire in 2027+ after V3 BB launches give ODC bandwidth supply at Starlink's at-cost rate. Sprint 5 verification gate confirms ODC is pre-revenue with structurally correct IRR engine (no `#NUM!`, no premature positive IRR), per-sat marginal IRR converges, Allocator OUT publishes the 11 canonical rows.

15. **Only after the preamble is filled in and constitutional docs are read:** proceed with drafting Sprint_5_Spec.md to the workspace folder. Mirror the Sprint 0/1/2/3/4 spec structure: §0 Constitutional refs, §1 Rule Compliance Preamble, §1.5 Pre-execution setup (no workbook-name confirmation needed per new lock; instead confirm Sprint 4.5 patch landed + iterative calc still ON), §2 Framing, §3 Scope (§3.0 pre-flight, §3.1 patch absorption — Sprint 4.5 likely landed separately so no patches here, §3.2 Assumptions amendments if any new rows needed, §3.3 ODC tab body cell-by-cell, §3.4 per-sat marginal IRR engine, §3.5 ODC at-cost compute rate calculation, §3.6 Allocator OUT contract overwrite), §4 Verification gate (universal + §6.4 Sprint 5 calibration), §5 Claude Log entry template, §6 Don't touch, §7 Open thread, §8 Execution sequence, §9 Amendment log.

If you are a spec author chat: do not finalize a spec without the Rule Compliance Preamble at the top and without confirming with me that the load-bearing methodology choices in step 12 are locked. Sprint 5 calibration is trivial (all 2025 ODC outputs = $0) but the architectural choices on cash-driven deployment, bandwidth claim derivation, per-sat IRR formula, internal/external compute split, and AI Stack at-cost compute pricing are load-bearing for Sprint 6 AI Stack, Sprint 9 Group P&L (Bandwidth + Compute elimination conservation rows R106 + R107), and Sprint 10 Allocator brain (ODC competes for cash + kg in outer queue). Get them right before plugin fires.

Current sprint scope: ODC module body + per-sat marginal IRR (4 engines: Model A weighted, Model B weighted, blended Expected, per-sat marginal in IRR engine) + cash-driven deployment + bandwidth services cost paid to Starlink + internal/external compute split + ODC → AI Stack at-cost compute transfer + Allocator OUT contract overwrite. Publishes 5 canonical labels Sprint 3 + Sprint 4 IFERROR-0 reads consume + Sprint 6 AI Stack will read. 2025 calibration: ODC revenue $0 exact; ODC sats deployed 0 exact; per-sat IRR 0 or negative; bandwidth services cost $0 exact.

Setup confirmation:
- Sprint 4.5 patch has landed (Demand Curves tab present + Starlink IRR taper verified + Constellation D&A within $707M ±10% + Assumptions stub rows 316-317 deleted) — OR Vlad confirms it will be absorbed into Sprint 5 spec as a patch section.
- Iterative calc still enabled workbook-wide (100 iter, 0.001 tol).
- I (Vlad) will handle all saving; plugin must not issue save commands.
- I (Vlad) handle workbook versioning entirely outside the spec; spec does not name workbook files.
