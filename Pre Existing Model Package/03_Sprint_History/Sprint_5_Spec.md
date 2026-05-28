# Sprint 5 — ODC Module (per-sat marginal IRR + dual revenue Model A/B + cash-driven deployment + bandwidth services from Starlink Capacity + internal/external compute split with at-cost transfer to AI Stack)

**Day budget**: 1.5 days
**Date drafted**: 2026-05-20

Per standing process rules locked 2026-05-20 (memory `feedback-no-workbook-names-in-specs`), this spec does not name source/target workbook files. Vlad handles versioning entirely outside the spec; plugin operates on the live open workbook session.

---

## §0 — Constitutional references

- **`01_Lessons_Learned.md`**: Principles 1 (no postponed methodology — cash-driven deployment + dual revenue + per-sat IRR + ODC↔AI Stack at-cost transfer all locked day-one of ODC build), 2 (per-sat marginal IRR — Sprint 5 builds ONE engine because ODC is single-vehicle architecture, unlike Starlink's four; reads external compute revenue only per §7.3), 4 (queue gate — ODC's cash demand year-row published for Sprint 10 Allocator's queue gate to consume against year-N non-module claims), 6 (no tab without a locked function — ODC is the fourth P&L module), 7 (canonical labels day one — five canonical publish labels Sprint 3 + Sprint 4 IFERROR-0 reads consume + Sprint 6 AI Stack will read), 8 (module COGS = direct production only — sat D&A + launch services + bandwidth services + ground ops + insurance + other; NO R&D / SG&A / overhead / taxes on ODC tab), 9 (internal transfers gross at module IRR — ODC ↔ Starlink bandwidth flow + ODC ↔ AI Stack compute flow both Sprint 9 Group P&L eliminations), 11 (zero OFFSET; INDEX/MATCH on labels; INDEX:INDEX for dynamic ranges in IRR engine), 12 (anchor-and-offset for deterministic ramps — chip roadmap year-rows, util ramp, internal share trajectory, terrestrial price deflation), 13 (year-offset helper row 5 standard), 14 (INDEX/MATCH on labels for all cross-tab refs), 17 (no superseded rows from prior sprints to delete — but Sprint 4.5 absorbed §3.1 deletes Assumptions stub rows 316-317 left by Sprint 4), 18 (MC ranges at input creation — two new Assumptions amendments in §3.2 each with full MC fields), 19 (no rationalizing failed sanity halt — Sprint 5 §6.4 calibration is trivial $0 across the board, but per-sat IRR `#NUM!` leak or any positive ODC revenue 2025 = halt), 20 (edge-year reads D/I/S/AC), 22 (within-year cycle documented in §2 — ODC↔Starlink Capacity bandwidth loop activates in Sprint 10 when Allocator drives sats deployed > 0; in Sprint 5 plugin verification fleet stays at 0 so cycle is dormant), 23 (Rule 22 stale-ref scan against Customer Launch R22/R69 + Starlink Capacity R18/R20 IFERROR-0 reads; verbatim case-sensitive match required per Rule 22).
- **`02_Architecture_and_Methodology.md`**: §1 (tab #7 = ODC; sheet position immediately after Starlink Capacity #6), §3 (vending-machine framing), §4.1 (Allocator IN block at rows 7-10 already in place from Sprint 1 reading 0 placeholders against Allocator), §4.2 (Allocator OUT contract — 11 canonical rows at 200-210 — Sprint 5 overwrites Sprint 1 literal-0 placeholders with live formulas), §5.1 (per-sat IRR formula: CF stream length N+1 = 6 for N=5 yrs sat-module default per Sprint 0 R151; Spot/Forward/Blended IRR with w=0.7 per Sprint 0 R17), §5.2 (ODC net marginal revenue per sat per year = per-sat external revenue − per-sat ground ops % − per-sat insurance − per-sat other COGS − per-sat bandwidth cost paid to Starlink − per-sat launch services cost paid to Launch Capacity at fully-allocated at-cost rate), §5.4 (strict IRR > 0 cutoff; Sprint 5 ODC will have IRR ≤ 0 in 2025-2026 by design — Pr(A)×A + Pr(B)×B insufficient pre-V3-BB Starlink at-cost rates), §6.6 (vehicle build cost = non-module claim at Sprint 10 Allocator gate; Sprint 5 ODC reads Launch Capacity's at-cost rate via INDEX/MATCH but does NOT compute vehicle build cost), §7.1 (fully-allocated at-cost launch services rate — see §9 amendment log for label-string reconciliation: Sprint 2 published `Starship at-cost rate ($mm/launch)`; Architecture §6.6 aspirational `At-cost launch services rate ($mm/launch)` never implemented; Sprint 5 reads the actually-published Sprint 2 string and §9 amends Architecture §6.6 to match published reality), §7.2 (ODC ↔ Starlink bandwidth 4-step Rule 21 pattern — Sprint 4 IFERROR-0 reads at Starlink Capacity R18/R20 activate the moment Sprint 5 writes land; Sprint 5 ODC books `Bandwidth services cost ($mm)` in COGS; Sprint 9 Group P&L R106 eliminates), §7.3 (ODC ↔ AI Stack fully-allocated at-cost compute transfer — Sprint 5 publishes `ODC at-cost compute rate ($/PFLOP-hr)` year-row; AI Stack Sprint 6 reads by INDEX/MATCH; per-sat IRR reads external compute revenue only — internal at-cost transfers don't contribute IRR signal), §9 (full ODC architecture — §9.1 cash-driven deployment, §9.2 dual revenue Model A energy-anchored + Model B η-anchored with Pr(A)=0.6 credence, §9.3 internal+external compute split, §9.4 per-sat marginal IRR engine N=5 yrs), §17 (2025 calibration — ODC revenue 2025 = $0 exact).
- **`03_Sprint_Roadmap_and_Verification.md`**: §3 Sprint 5 scope + locked-this-sprint decisions (ODC → AI Stack at-cost compute pricing fully-allocated per §7.3 locked 2026-05-20; per-sat IRR reads external revenue only; Sprint 5 publishes canonical row `ODC at-cost compute rate ($/PFLOP-hr)` for Sprint 6 AI Stack), §5 universal verification (no errors, conservation OK trivially since Sprint 5 produces $0 ODC revenue, edge-year reads D/I/S/AC, round-trip stability, stale-ref scan, sanity halts, Claude Log), §6.4 Sprint 5 calibration (ODC revenue 2025 = $0 exact; ODC sats deployed 2025 = 0 exact; ODC fleet end-2025 = 0 exact; per-sat marginal IRR 2025 = 0 or negative; bandwidth services cost paid to Starlink 2025 = $0 exact), §8 sprint-spec template (followed below, with workbook-name header lines OMITTED per 2026-05-20 lock).
- **`04_Assumptions_Tab_Spec.md`**: §6 ODC inputs R143-R188 (all 30+ rows inlined in §3.3 below by canonical label, not row number) + two new amendments in §3.2 (`ODC cash demand large default ($mm)`, `ODC kg demand large default (kg)`).
- **`Model Execution Rules.md`**: Mandatory Rule Compliance Preamble at §1; Rules 1 / 3 / 4 / 5 / 10 / 11 / 12 / 13 / 14 / 15 / 16 / 17 / 20 / 21 / 22 / 23 load-bearing. Rule 19 (target workbook) is N/A this sprint per standing process rule 2 (locked 2026-05-20 — Vlad handles versioning entirely outside the spec).
- **`2025 Anchors from Q4_25.md`**: ODC revenue 2025 = $0 (Earth R125 / Sprint Roadmap §6.4); structural correction §3 confirms ODC deployment is CASH-DRIVEN not stub-driven (R247 STUB year-row already dropped in Sprint 0).
- **`Sprint_0_Spec.md`** §3.6 (Assumptions §6 ODC inputs R143-R188 — every label, Base Case, MC range inlined in §3.3 below).
- **`Sprint_1_Spec.md`** §3.3.4 (ODC shell — Allocator IN at rows 7-10 + Allocator OUT at rows 200-210 with literal 0 placeholders; Sprint 5 fills rows 11-199 in between and overwrites OUT placeholders with live formulas).
- **`Sprint_2_Spec.md`** + **`Sprint_2_to_3_Patch_F9_Retirement_and_Starship_Ops.md`** §6.13 (Launch Capacity canonical labels — Sprint 5 reads `Starship at-cost rate ($mm/launch)` from Launch Capacity R40 by INDEX/MATCH; reads `Total Annual Capacity (kg-to-LEO)` for kg-queue context not directly consumed).
- **`Sprint_3_Spec.md`** + **`Sprint_3.5_Patch_Customer_Launch_IRR_Reformulation.md`** (Customer Launch R22 + R69 IFERROR-0 reads — Sprint 5 publishes the two canonical labels these consume verbatim: `ODC Starship launches (internal)` and `ODC Starship kg demand`).
- **`Sprint_4_Spec.md`** §3.4 (Starlink Capacity tab — Sprint 5 reads `BB pool at-cost rate ($/Gbps/yr)` from R48 + `DTC pool at-cost rate ($/Gbps/yr)` from R50 + `Total active BB Gbps` from R11 + `Total active DTC Gbps` from R13; Sprint 4 IFERROR-0 reads at Starlink Capacity R18 + R20 consume Sprint 5's two canonical publish labels `ODC BB Gbps demand` + `ODC DTC Gbps demand`).
- **Sprint 4.5 patch absorbed as §3.1 of this spec** (Demand Curves tab #14 build, demand-cap mechanic on Starlink R120 + R131, Constellation D&A retune, V3 BB Wright's Law on bandwidth-per-sat, Assumptions stub rows 316-317 deletion). Per `project-demand-curves-stub-remove-in-sprint-5` memory + 2026-05-20 Vlad lock; Sprint 3-style absorption rather than separate Sprint 4.5 spec.

---

## §1 — Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md` and the four constitutional docs. Each box ticked or justified N/A:

- [x] **Rule 1** (one concept per write) — §3 structured as discrete blocks. Every row's column-A label is written in a separate `set_cell` call from its D-column anchor formula, and the D-anchor formula is a separate call from the E:AC copyToRange. Two new Assumptions rows in §3.2 each execute as 6 discrete writes (label, Base, MC Min, MC Max, MC Distribution, Notes). Number-format passes execute as separate writes from formula writes. Sprint 4.5 patch §3.1 atomized: (a) Demand Curves tab build = label-block writes / formula writes / format writes separated, (b) Starlink R120 + R131 demand-cap rewrite = label retained / formula overwrite is separate write from format pass, (c) Constellation D&A retune = formula overwrite separate from format, (d) V3 BB WL on bandwidth-per-sat = formula overwrite separate, (e) Assumptions stub row clear = label clear / value clear / MC field clear separated.
- [x] **Rule 3 / 23** (formula pattern) — every deterministic ramp on ODC tab uses anchor-and-offset on `E$5` and a locked anchor cell. Year-chained Rule 23 exceptions explicitly flagged inline with one-line justification: (a) Cumulative ODC sats running sum for Wright's Law denominator (`E{cum} = D{cum} + E{sats_deployed_this_year}` — cumulative running sum), (b) ODC Active Fleet EoY year-row (`E{fleet} = D{fleet} + E{sats_deployed} − E{sat_retirements}` — BoY + adds − retirements pattern). All other year-rows (chip roadmap reads, util ramp, internal share trajectory, terrestrial price deflation, sat physical reads) use anchor-and-offset or INDEX/MATCH from Assumptions year-rows. Per-sat IRR engine uses INDEX:INDEX horizontal slicing (Principle 11 compliant — no OFFSET); future-year reads for Forward IRR (Y+2) wrapped IFERROR for terminal-year edge.
- [x] **Rule 4** (verification gate) — §4.3 enumerates explicit read-back cells at D (2025), I (2030), S (2040), AC (2050) with expected values for every load-bearing row: Total Revenue (= 0 in 2025), Module EBITDA, Module CapEx, Module FCF, per-sat Spot/Forward/Blended IRR (= 0 or negative in 2025), Bandwidth services cost paid to Starlink (= $0 in 2025), Active fleet end-year (= 0 in 2025), Sats deployed (= 0 in 2025), Cash demand year-row, Kg demand year-row, ODC at-cost compute rate ($/PFLOP-hr), ODC BB Gbps demand, ODC DTC Gbps demand, ODC Starship launches (internal), ODC Starship kg demand. Sprint 4.5 patch §3.1 read-back: Demand Curves tab Total BB/DTC Gbps demand year-rows + price year-rows; Starlink R120 + R131 revenue with demand cap active (Starlink+DTC 2025 = $7,852M ±5% holds); Constellation D&A 2025 = $707M ±10% (post-retune).
- [x] **Rule 5** (conservation gate) — Sprint 9 Group P&L conservation block doesn't exist until Sprint 9; Sprint 5 verifies trivially via Sprint 5 §6.4 calibration ($0 ODC revenue → $0 Bandwidth elim residual → R106 trivially = 0 when Sprint 9 lights up). Sprint 4.5 patch §3.1 preserves Sprint 4 conservation: Starlink revenue with demand cap stays within $7,852M ±5% (so no upstream conservation drift).
- [x] **Rule 6** (inline formulas) — every cell write in §3 specified with the full Excel formula. No "see Architecture §9" hand-waves — cash-driven deployment, dual revenue Pr(A)-weighted, per-sat IRR engine, at-cost compute rate, bandwidth claim derivation, internal/external split all inlined verbatim. INDEX/MATCH calls on Assumptions / Launch Capacity / Starlink Capacity written out with exact canonical labels.
- [x] **Rule 10** (no row insertions) — ODC tab Sprint 5 writes appended to rows 11–199 (between Sprint 1's IN block at 7-10 and OUT block at 200-210). Sprint 1 OUT block placeholders OVERWRITTEN in place (same row numbers) per Architecture §4.2 — no row insertions on ODC tab. Assumptions tab amendments (two new rows in §3.2) appended below Sprint 4's last-used row — append-only per Rule 10. Sprint 4.5 patch §3.1 deletes Assumptions stub rows 316-317 by CLEARING values (not deleting rows) — no row deletions either. Demand Curves tab build appends to a fresh sheet — no insertions into existing tabs. Starlink tab R120 + R131 + Constellation D&A retune all OVERWRITE existing cells in place — no row insertions. No `insert_row` operations anywhere.
- [x] **Rule 11** (touch points) — every new ODC line item enumerates its (i) intra-tab SUM range (Total Revenue = External compute revenue + Internal transfer revenue; Total COGS = Constellation D&A + Launch services + Bandwidth services + Ground ops + Insurance + Other COGS), (ii) Allocator OUT pull (11 canonical rows at 200-210), (iii) Sprint 9 Group P&L pulls (Total Revenue, Module EBITDA, Module CapEx, Module FCF via INDEX/MATCH), (iv) Sprint 9 conservation rows R106 (Bandwidth elimination — reads `Starlink internal bandwidth revenue ($mm)` from Starlink + ODC's `Bandwidth services cost ($mm)`) + R107 (Compute elimination — reads ODC's internal transfer revenue + AI Stack internal compute cost), (v) Sprint 3 Customer Launch R22 reads `ODC Starship kg demand` + R69 reads `ODC Starship launches (internal)`, (vi) Sprint 4 Starlink Capacity R18 reads `ODC BB Gbps demand` + R20 reads `ODC DTC Gbps demand`, (vii) Sprint 6 AI Stack will read `ODC at-cost compute rate ($/PFLOP-hr)` for its internal compute cost line. Touch points enumerated per row in §3.3 / §3.4 / §3.5 / §3.6.
- [x] **Rule 12** (label-based cross-tab refs) — every cross-tab pull on ODC tab uses `INDEX(Tab!D:D, MATCH("<exact canonical label>", Tab!$A:$A, 0))` or year-row equivalent `INDEX(Tab!$D:$AC, MATCH("<label>", Tab!$A:$A, 0), E$5+1)`. Zero hardcoded row-number references. Cross-tab labels Sprint 5 reads: Assumptions §6 by label for all 30+ inputs (R143-R188); Launch Capacity tab `Starship at-cost rate ($mm/launch)` (Sprint 2 R40 — verified verbatim in §3.0 pre-flight); Starlink Capacity tab `BB pool at-cost rate ($/Gbps/yr)` (Sprint 4 R48), `DTC pool at-cost rate ($/Gbps/yr)` (Sprint 4 R50), `Total active BB Gbps` (Sprint 4 R11), `Total active DTC Gbps` (Sprint 4 R13); Allocator tab `ODC cash allocation` + `ODC kg allocation` (Sprint 1 placeholders = 0). For Sprint 4.5 patch §3.1: Demand Curves tab `Total BB Gbps demand (Gbps/yr)`, `Total BB price ($/Gbps/yr)`, `Total DTC Gbps demand (Gbps/yr)`, `Total DTC price ($/Gbps/yr)` (newly published).
- [x] **Rule 13** (vending-machine test) — ODC P&L stops at Module EBITDA = Gross Profit. NO R&D / SG&A / customer service / corporate overhead / taxes anywhere on ODC tab. ODC R&D lives on OpEx tab (30% start → 8% end CAGR −15%/yr per Architecture §12.1; Sprint 8 owns formula with `MAX($-profile, % × revenue)` pre-revenue switch). The exception is Internal Transfer Revenue (ODC → AI Stack compute, intercompany flow per Architecture §7.3, NOT OpEx) and the cost-side of two intercompany flows (bandwidth services cost paid to Starlink + launch services cost paid to Launch Capacity, both per Architecture §7.1 / §7.2).
- [x] **Rule 14** (no hardcoded constants) — every behavior input resolves to an Assumptions row by label. Declared exceptions: (a) Mathematical constants (1, 0 in IFERROR fallbacks; 8760 for hours/year; 1000 for kW→W conversion; 1e6 for $→$mm conversions), (b) IRR engine SEQUENCE() arguments are dynamic-array constructs not behavior inputs, (c) N+1 = 6 for SEQUENCE construction is derived from Sprint 0 R151 ODC fleet design life = 5 yrs via N+1 — the spec inlines `=_xlfn.SEQUENCE(1, INDEX(Assumptions!$B:$B, MATCH("ODC fleet design life (years)", Assumptions!$A:$A, 0))+1)` to keep N parametric. Two new Assumptions rows added in §3.2 have full MC ranges per Rule 14 + Principle 18. Demand Curves tab Sprint 4.5 patch §3.1: bandwidth-demand inputs and price inputs all live on Demand Curves tab (read via INDEX/MATCH — no hardcoded numbers in Starlink R120 or R131 formulas).
- [x] **Rule 15** (sanity check halt thresholds) — §4.2 / §4.4 every check has quantitative halt threshold. ODC revenue 2025 ≠ $0 exact = halt (any >$10M absolute). ODC sats deployed 2025 ≠ 0 = halt (any >5 absolute). ODC fleet end-2025 ≠ 0 = halt (any >5 absolute). Per-sat marginal Blended IRR 2025 > 0 = halt (premature). Bandwidth services cost paid to Starlink 2025 ≠ $0 = halt (any >$10M). Per-sat IRR `#NUM!` or NaN leak to Allocator OUT R207/R208/R209 = halt + push back. ODC at-cost compute rate ($/PFLOP-hr) `#DIV/0!` 2025 (fleet = 0, division by zero) = EXPECTED; IFERROR-0 wrapper required (downstream AI Stack reads gracefully). Sprint 4.5 patch §3.1 halt thresholds: Starlink+DTC revenue 2025 outside [$7,000M, $8,700M] post-demand-cap = halt (Sprint 4 calibration must hold); Constellation D&A 2025 outside [$600M, $850M] post-retune = halt (target $707M ±10%); V3 BB Wright's Law on bandwidth-per-sat — V3 BB Gbps/sat 2025 ≠ 1,000 = halt (anchor); V3 BB Gbps/sat 2030 < 800 or > 1,500 = halt (sanity bound on WL learning); Demand Curves total BB Gbps demand 2025 outside [50,000, 150,000] Gbps = halt (sanity).
- [x] **Rule 16** (edge-year verification) — D / I / S / AC reads explicit in §4.3. Edge years cover 2025 (pre-deployment, all $0), 2030 (ODC ramping per allocator-driven cash, V3 BB Starlink at-cost rates live, internal compute share ~77.5%), 2040 (mature ODC fleet, internal/external split ~50/50, ~30% terrestrial GPU-hr price compression), 2050 (terminal, internal share floor 40%, max ECR).
- [x] **Rule 17** (delete superseded rows) — Sprint 4.5 patch §3.1 explicitly deletes Assumptions stub rows 316-317 (`BB $/Gbps ($/Gbps/yr, year-row)` + `DTC $/Gbps ($/Gbps/yr, year-row)`) that Sprint 4 added to bypass missing Demand Curves V9 labels. Per Principle 17 — delete superseded rows in the same spec that supersedes them. Clearing pattern: blank label column A, blank Base Case column B, blank notes column C, blank year-row columns D:AC, blank MC range columns AG:AJ. No `delete_row` operation (Rule 10) — values cleared in place.
- [x] **Rule 19** (save-as) — N/A per standing process rule 2 (locked 2026-05-20). Spec does NOT name target workbook. Vlad handles versioning entirely outside the spec; plugin operates on the live open workbook session and does NOT issue any save commands. §3.0 pre-flight does NOT check workbook name.
- [x] **Rule 20** (IFERROR guards on pre-revenue ratios) — Module EBITDA Margin % wrapped `=IFERROR(D{EBITDA}/D{Revenue}, 0)` per Sprint 1 convention. Per-sat IRR wrapped `=IFERROR(IRR(...), -1)` per Architecture §5.1. ODC at-cost compute rate wrapped `=IFERROR(D{total_cost} × 1e6 / D{PFLOP-hrs}, 0)` because Fleet PFLOP-hrs = 0 in 2025-2026 pre-deployment. Bandwidth cost per-sat wrapped `=IFERROR(D{total_bandwidth_cost}/D{fleet}, 0)`. Launch services cost per-sat wrapped same. Per-sat external revenue ÷ per-sat marginal opex ratios all IFERROR-guarded. INDEX col_num=0 spill guard (per memory `feedback-index-col-zero-spills`): per-sat IRR engine's horizontal slicing uses `IF(year_offset_col < 1, 0, INDEX(...))` wrapper where applicable — specifically the Forward IRR (Y+2) for terminal years 2049-2050 where the y+2..y+7 slice exceeds column AC; IFERROR catches but explicit `IF(COLUMN()-COLUMN($D$5)+2 > 25, 0, …)` guard documented inline in §3.4.
- [x] **Rule 21** (internal flows need elimination + conservation) — Sprint 5 introduces the THIRD and FOURTH live internal transfer flows in the rebuild. (3) ODC ↔ Starlink bandwidth services — 4-step pattern: (i) Starlink already books `Starlink internal bandwidth revenue ($mm)` row from Sprint 4 with IFERROR-0 read of `(ODC BB Gbps demand × BB pool at-cost rate) + (ODC DTC Gbps demand × DTC pool at-cost rate)` — Sprint 5 ACTIVATES this by publishing the two `ODC BB Gbps demand` + `ODC DTC Gbps demand` labels, (ii) ODC books `Bandwidth services cost ($mm)` in COGS at same total, (iii) Sprint 9 Group P&L R106 eliminates, (iv) Sprint 9 conservation row R106 verifies match. For Sprint 5 verification, ODC sats = 0 → ODC Gbps demand = 0 → Starlink internal bandwidth revenue = $0 → ODC bandwidth cost = $0 → trivial conservation. (4) ODC ↔ AI Stack compute services — 4-step pattern: (i) ODC books `Internal transfer revenue (at-cost compute) ($mm)` from internal share × Fleet PFLOP-hrs × at-cost rate, (ii) AI Stack will book `Internal compute cost from ODC ($mm)` in COGS in Sprint 6, (iii) Sprint 9 Group P&L R107 eliminates, (iv) Sprint 9 conservation row R107 verifies match. For Sprint 5 verification, ODC sats = 0 → ODC PFLOP-hrs = 0 → internal transfer revenue = $0 → AI Stack reads $0 → trivial conservation.
- [x] **Rule 22** (stale-ref scan) — §4.5 enumerates by-label scan: (i) ODC's Assumptions reads (30+ §6 ODC inputs + Sprint 0 R17 Forward weight + Sprint 0 R148 F_ref) confirmed against Assumptions row labels via MATCH at pre-flight; (ii) ODC's Launch Capacity read `Starship at-cost rate ($mm/launch)` confirmed against Launch Capacity column A (Sprint 2 R40 verbatim — see §9 amendment log on Architecture §6.6 label reconciliation); (iii) ODC's Starlink Capacity reads `BB pool at-cost rate ($/Gbps/yr)` + `DTC pool at-cost rate ($/Gbps/yr)` + `Total active BB Gbps` + `Total active DTC Gbps` confirmed against Starlink Capacity column A (Sprint 4 R48/R50/R11/R13 verbatim); (iv) Sprint 1 OUT block placeholders OVERWRITTEN with live formulas — Sprint 5 verifies the 11 canonical OUT labels match Architecture §4.2 verbatim post-write; (v) Sprint 5 publishes five canonical labels Sprint 3 + Sprint 4 IFERROR-0 reads consume + Sprint 6 AI Stack will read: `ODC BB Gbps demand`, `ODC DTC Gbps demand`, `ODC Starship launches (internal)`, `ODC Starship kg demand`, `ODC at-cost compute rate ($/PFLOP-hr)`. Post-write plugin re-runs Customer Launch R22 / R69 and Starlink Capacity R18 / R20 MATCH calls and verifies each resolves (no `#N/A` returned). Sprint 4.5 patch §3.1 stale-ref scan: Demand Curves tab's four published labels (`Total BB Gbps demand (Gbps/yr)`, `Total BB price ($/Gbps/yr)`, `Total DTC Gbps demand (Gbps/yr)`, `Total DTC price ($/Gbps/yr)`) confirmed against Starlink R120 + R131 demand-cap-formula reads. Spec §3.0 pre-flight enumerates the exhaustive scan.

**Architecture & Methodology compliance:**

- [x] Module P&L follows vending-machine framing (Architecture §3) — ODC builds Revenue → COGS → Gross Profit = Module EBITDA → Module CapEx → Module FCF per §3.3. No R&D / SG&A / overhead / taxes on ODC tab.
- [x] Per-sat marginal IRR engine (Architecture §5 + §9.4) — §3.4 builds ONE per-sat IRR engine for ODC (single-vehicle architecture). N = 5 yrs sat-module default per Sprint 0 R151. Reads external compute revenue only (per §7.3 + Principle 9) — internal at-cost transfer to AI Stack doesn't contribute to per-sat IRR signal.
- [x] Allocator OUT contract uses canonical 11 labels (Architecture §4.2) — §3.6 overwrites Sprint 1 placeholders. 11 rows populate with live formulas. No memo rows below the canonical block this sprint (single ODC engine, no per-vehicle decomposition needed unlike Starlink's four vehicles).
- [x] Year-offset helper row at row 5 + year header at row 4 on ODC tab — already in place from Sprint 0. §3.0 pre-flight confirms D4 = 2025, D5 = 0, AC4 = 2050, AC5 = 25.
- [x] ZERO `OFFSET()` formulas; INDEX:INDEX patterns used (Principle 11) — confirmed. Per-sat IRR engine's horizontal slicing uses `INDEX($row, 1, col_start) : INDEX($row, 1, col_end)` for the N-year future-revenue window.

If any box is unchecked, the spec author justifies or amends before execution starts. Plugin refuses to write a single cell against an unticked-or-unjustified preamble.

---

## §1.5 — Pre-execution setup (Vlad confirms before plugin starts writing)

Per standing process rule 3 (locked 2026-05-20), the kickoff prompt includes this confirmation block. The plugin's §3.0 pre-flight verifies it before any cell write.

**Vlad attests:**

1. **Vlad will handle all saves** — the plugin operates on the live open workbook session and will NOT issue any save / save-as / write-file commands. Verification reads cells from the session directly.
2. **Vlad will handle workbook versioning entirely outside the spec** — the spec does NOT name workbook files. Vlad has Save-As'd to whatever version name he prefers before this kickoff. Plugin's §3.0 pre-flight does NOT check workbook name (per 2026-05-20 lock).
3. **Sprint 4.5 patch state** — Sprint 4.5 has NOT landed as a separate patch. Sprint 5 absorbs Sprint 4.5 as §3.1 of this spec (Sprint 3-style absorption). Plugin executes §3.1 patches FIRST then ODC body §3.2-3.6. Confirm Vlad accepts this approach.
4. **Iterative calc still enabled workbook-wide** — Excel options: iterative calculation enabled, maximum iterations 100, maximum change 0.001. Per memory `project-iterative-calc-enabled-2026-05-20`. §3.0 pre-flight verifies via reading Excel options state.
5. **No other tabs are open in this workbook** that could conflict with ODC + Assumptions + Starlink + Demand Curves writes (Assumptions tab needs WRITE access for two new amendments §3.2 + two stub deletions §3.1.e; Starlink tab needs WRITE access for R120 + R131 demand-cap + Constellation D&A retune + V3 BB WL on bandwidth §3.1.b/c/d; Demand Curves tab needs WRITE access for full build §3.1.a).

If any of the above is not true, plugin halts at pre-flight per Rule 9 and pushes back to Vlad.

---

## §2 — Framing

**Why this sprint:** Sprint 5 builds the ODC module body end-to-end (rows 11–199 between Sprint 1's IN block at rows 7-10 and OUT block at rows 200-210). This is the FOURTH P&L module after Customer Launch, Starlink, Starlink Capacity. Sprint 5 publishes FIVE canonical labels Sprint 3 + Sprint 4 IFERROR-0 reads already wired against (Customer Launch R22 + R69; Starlink Capacity R18 + R20) plus one label Sprint 6 AI Stack will read (ODC at-cost compute rate). Sprint 5 also absorbs Sprint 4.5 patch (Demand Curves tab build + Starlink demand-cap mechanic + Constellation D&A retune + V3 BB Wright's Law on bandwidth-per-sat + Assumptions stub row deletion) as §3.1 — Sprint 3-style absorption rather than separate Sprint 4.5 spec, per 2026-05-20 Vlad lock for speed.

**The 8 Vlad locks for this sprint (2026-05-20):**

1. **Sprint 4.5 patch absorbed as §3.1** — single spec, single plugin execution, fastest path to ODC live. §3.1 mechanics: (a) Build Demand Curves tab at sheet position #14 with four canonical year-rows; (b) Re-wire Starlink R120 BB Revenue + R131 DTC Revenue to demand-cap mechanic `MIN(Available Gbps, Demand Gbps) × price`; (c) Retune Constellation D&A on Starlink (add legacy V1/V1.5 + facility D&A memo so 2025 = $707M ±10%); (d) Implement V3 BB Wright's Law on bandwidth-per-sat (R17 area on Starlink); (e) Clear Assumptions stub rows 316-317 (`BB $/Gbps`, `DTC $/Gbps` year-rows). After §3.1 lands, plugin proceeds to §3.2 onwards.

2. **Read Launch Capacity's actually-published label verbatim** — `Starship at-cost rate ($mm/launch)` (Sprint 2 R40 / Patch E §6.13). Architecture §6.6 named an aspirational label `At-cost launch services rate ($mm/launch)` that was never implemented in Sprint 2 — see §9 amendment log for the Architecture §6.6 amendment that reconciles the label string to published reality. Sprint 5 ODC reads `Starship at-cost rate ($mm/launch)` exactly.

3. **Cash-driven deployment — large-default cash + kg ask year-rows, IRR-masked** (mirrors Starlink R141/R142 pattern). Two new Assumptions rows in §3.2: `ODC cash demand large default ($mm)` (Base $50,000M flat 2025-2050, MC lognormal [$10,000M, $200,000M]) and `ODC kg demand large default (kg)` (Base 50,000,000 kg flat, MC lognormal [10,000,000, 200,000,000]). ODC tab publishes Cash Demand / Kg Demand year-rows = `IF(Blended IRR > 0, large_default, 0)` — Sprint 10 Allocator's queue gate consumes these. Wanted deployment in 2025-2026 = 0 because Blended IRR ≤ 0 (no V3 BB Starlink at-cost rates yet → bandwidth cost too high → marginal sat IRR negative).

4. **ODC sat physical config — keep all Sprint 0 §6 ODC defaults as-is.** R145 Compute power per sat 140 kW (Vlad 2026-05-19 lock over Q4'25 W/kg=70); R147 sat dry mass 1,400 kg; R152 solar generation 156,000 W; R153 thermal mass 480 kg; R148 F_ref = 1,979 TFLOPS (H100 FP8); R149 ECR = 0.6; R150 workload mix 85% inference; R151 fleet design life = 5 yrs. Subsystem unit costs R155-R162 + Wright's Law R164=0 (chips no learning) / R165=0.15 (subsystems 15% per doubling). Chip roadmap year-rows R173-R178 (H100 → AI5 → Dojo-3 linear interp). Dual revenue R180 Pr(A)=0.6; R181 CoreWeave baseline $12B/GW_IT/yr; R182/R183 PUE 1.4/1.12; R184 terrestrial deflation 5%/yr; R185 steady-state util 0.85. Internal/external split R187 (95% 2025 → 77.5% 2030 → 50% 2040 → 40% 2050) / R188 (= 1 − R187).

5. **Bandwidth claim derivation — keep Sprint 0 R-bandwidth-conversion (0.05 Gbps/(GWh/yr)) and R-BB-share (0.50) as MC-wide stubs.** Sprint 0 inputs are placeholders pending Mach33 thesis on per-PFLOP bandwidth requirement. Flag for post-Sprint-12 calibration retune in §7 Open thread. ODC tab consumes both via INDEX/MATCH.

6. **Per-sat marginal IRR engine — Architecture §9.4 verbatim with §7.3 lock applied.** N = 5 yrs (Sprint 0 R151); CF stream length N+1 = 6; SEQUENCE-based construction; IFERROR(IRR(...), -1) wrapper. Reads EXTERNAL compute revenue only per Architecture §7.3 — internal at-cost transfer to AI Stack doesn't contribute IRR signal. Spot IRR (current year), Forward IRR (Y+2), Blended IRR = `(1−w)·Spot + w·Forward` with w = 0.7 from Sprint 0 R17.

7. **ODC at-cost compute rate ($/PFLOP-hr) — fully-allocated formula per Architecture §7.3.** Rate per PFLOP-hr = (annual sat D&A + launch services cost + bandwidth services cost + insurance + other COGS) / annual PFLOP-hrs delivered. Sprint 5 publishes the canonical row `ODC at-cost compute rate ($/PFLOP-hr)` year-row for Sprint 6 AI Stack to read by INDEX/MATCH. IFERROR-0 wrapper handles 2025-2026 pre-deployment when PFLOP-hrs = 0.

8. **Within-year cycle documented — ODC ↔ Starlink Capacity bandwidth loop activates in Sprint 10.** The cycle: ODC sats deployed → ODC Fleet PFLOPS → ODC Bandwidth demand (Gbps) → Starlink Capacity Available Gbps → Starlink Capacity at-cost rates ($/Gbps/yr) → ODC Bandwidth services cost ($mm/yr) → ODC EBITDA → ODC per-sat marginal IRR → Sprint 10 Allocator cash + kg allocation → ODC sats deployed (next iteration). In Sprint 5 (Allocator still dormant), allocation = 0 → sats deployed = 0 → bandwidth demand = 0 → cycle is dormant. In Sprint 10 (Allocator lit), cycle activates. Convergence target <10 iterations, no value moves > $1M in 5x round-trip recalc. Iterative calc workbook-wide enabled (100 iter, 0.001 tol) per memory lock 2026-05-20. Plugin §4.4 verification gate forces a `Application.Calculate` then reads fresh values (per memory `feedback-mac-excel-range-values-caching`).

**What it produces (canonical output rows — single source of truth; labels exact, no renames):**

| Tab | Canonical label | Consumed by |
|---|---|---|
| ODC | `ODC BB Gbps demand` (year-row) | **Sprint 4 Starlink Capacity R18** IFERROR-0 read |
| ODC | `ODC DTC Gbps demand` (year-row) | **Sprint 4 Starlink Capacity R20** IFERROR-0 read |
| ODC | `ODC Starship launches (internal)` (year-row) | **Sprint 3 Customer Launch R69** IFERROR-0 read |
| ODC | `ODC Starship kg demand` (year-row) | **Sprint 3 Customer Launch R22** IFERROR-0 read |
| ODC | `ODC at-cost compute rate ($/PFLOP-hr)` (year-row) | Sprint 6 AI Stack (future) |
| ODC | `Total Revenue ($mm)` (Allocator OUT R201) | Sprint 9 Group P&L module revenue aggregator |
| ODC | `Module EBITDA ($mm)` (R202) | Sprint 9 + Sprint 11 |
| ODC | `Module EBITDA Margin %` (R203) | Sprint 9 diagnostic |
| ODC | `Module FCF ($mm)` (R204) | Sprint 9 + Sprint 11 |
| ODC | `Module CapEx ($mm)` (R205) | Sprint 8 CapEx tab aggregation + Sprint 9 |
| ODC | `Capital deployed ($mm)` (R206) | Diagnostic only |
| ODC | `Spot IRR` (R207) | Sprint 10 Allocator brain |
| ODC | `Forward IRR (Y+2)` (R208) | Sprint 10 |
| ODC | `Blended IRR` (R209) | Sprint 10 |
| ODC | `Capacity Demand (kg-to-LEO)` (R210) | Sprint 10 Allocator kg queue |
| ODC | `Internal transfer revenue (at-cost compute) ($mm)` | Sprint 9 Group P&L R107 elimination |
| ODC | `Bandwidth services cost ($mm)` | Sprint 9 Group P&L R106 elimination conservation |
| Demand Curves (Sprint 4.5 patch) | `Total BB Gbps demand (Gbps/yr)` | Starlink R120 demand-cap |
| Demand Curves (Sprint 4.5 patch) | `Total BB price ($/Gbps/yr)` | Starlink R120 demand-cap |
| Demand Curves (Sprint 4.5 patch) | `Total DTC Gbps demand (Gbps/yr)` | Starlink R131 demand-cap |
| Demand Curves (Sprint 4.5 patch) | `Total DTC price ($/Gbps/yr)` | Starlink R131 demand-cap |

**What it deliberately does NOT do:**

- Does NOT add R&D / SG&A / corporate overhead / taxes to ODC (vending-machine framing — Principle 8 + Rule 13). ODC R&D lives on OpEx tab (Sprint 8 owns with pre-revenue $-profile switch per §12.1).
- Does NOT compute vehicle build cost claim — that's Sprint 10 Allocator (Architecture §6.6). Sprint 5 ODC reads Launch Capacity's at-cost rate which already includes vehicle D&A allocation per launch.
- Does NOT write to Sprint 6 AI Stack — ODC's at-cost compute rate publishes; AI Stack reads it in Sprint 6.
- Does NOT write to Group P&L / OpEx / CapEx / Valuation / Allocator tabs — those sprints read ODC by canonical labels.
- Does NOT modify Customer Launch tab or Launch Capacity tab — Sprint 5 only READS from them.
- Does NOT modify Starlink Capacity tab body (Sprint 4 ownership). Sprint 5 publishes labels that Sprint 4's IFERROR-0 reads at Starlink Capacity R18 + R20 endogenously consume.
- Does NOT touch Sprint 4 Starlink tab body EXCEPT for Sprint 4.5 patch §3.1.b (R120 + R131 demand-cap formula rewrite), §3.1.c (Constellation D&A retune), §3.1.d (V3 BB WL on bandwidth-per-sat). All three are in-place cell overwrites — no row insertions.
- Does NOT introduce per-product IRR engines for ODC (single-vehicle architecture — one composite per-sat IRR engine suffices). Unlike Sprint 4 Starlink which has four per-vehicle IRR engines.

**Dependencies:**

- Sprint 0 (Assumptions §6 ODC inputs R143-R188; Sprint 0 R17 Forward weight; Sprint 0 R148 F_ref).
- Sprint 1 (ODC shell rows 7-10 + 200-210; Allocator placeholder rows for ODC cash/kg allocation).
- Sprint 2 + Patch E §6.13 (Launch Capacity tab — Sprint 5 reads `Starship at-cost rate ($mm/launch)`).
- Sprint 3 + Sprint 3.5 patch (Customer Launch tab — Sprint 5 publishes labels Customer Launch R22 + R69 IFERROR-0 reads consume).
- Sprint 4 (Starlink tab + Starlink Capacity tab — Sprint 5 reads at-cost rates + Total active Gbps; Sprint 5 publishes labels Starlink Capacity R18 + R20 IFERROR-0 reads consume; Sprint 5 also patches Starlink R120 + R131 + Constellation D&A + V3 BB WL via §3.1 patch absorption).
- Sprint 4.5 patch absorbed as §3.1 (Demand Curves tab build + Starlink demand-cap + Constellation D&A retune + V3 BB WL on bandwidth + Assumptions stub deletion).

---

## §3 — Scope

### §3.0 Pre-flight (plugin verifies BEFORE any cell write)

Plugin halts on any failure and pushes back to Vlad. Per standing process rule 2 (locked 2026-05-20), this pre-flight does NOT check workbook name.

1. **Iterative calc enabled** — Excel options show iterative calculation enabled, max iterations = 100, max change = 0.001. Halt if disabled or non-matching values. Read via Office-JS `application.calculationMode` + `application.iterativeCalculation`.
2. **ODC tab exists** with sheet position #7 (per Architecture §1: Assumptions #1, Allocator #2, Launch Capacity #3, Customer Launch #4, Starlink #5, Starlink Capacity #6, ODC #7). Halt if tab missing or wrong position.
3. **ODC row 4 + row 5** read year header + year offset standards: D4 = 2025, I4 = 2030, S4 = 2040, AC4 = 2050; D5 = 0, I5 = 5, S5 = 15, AC5 = 25. Halt if any mismatch.
4. **ODC Allocator IN block at rows 7-10** confirmed via label match: A7 contains "INPUTS FROM CENTRAL ALLOCATOR", A8 contains "Capital Allocation", A9 contains "Starship Capacity Allocation", A10 contains "Total Capital Available". **ODC Allocator OUT block at rows 200-210** confirmed: A200 contains "CENTRAL ALLOCATOR OUTPUTS", A201..A210 contain the 11 canonical OUT labels per Architecture §4.2 (verbatim: `Total Revenue ($mm)`, `Module EBITDA ($mm)`, `Module EBITDA Margin %`, `Module FCF ($mm)`, `Module CapEx ($mm)`, `Capital deployed ($mm)`, `Spot IRR`, `Forward IRR (Y+2)`, `Blended IRR`, `Capacity Demand (kg-to-LEO)`). Halt if any label mismatch.
5. **ODC rows 11-199** confirmed empty pre-Sprint-5. Plugin reads A11:A199 — all blank. Halt if anything non-blank (Sprint 1 deviation needing investigation).
6. **Sprint 4 canonical labels on Starlink Capacity tab** confirmed via MATCH calls:
   - `MATCH("Total active BB Gbps", 'Starlink Capacity'!$A:$A, 0)` must resolve (Sprint 4 R11).
   - `MATCH("Total active DTC Gbps", 'Starlink Capacity'!$A:$A, 0)` must resolve (Sprint 4 R13).
   - `MATCH("ODC BB Gbps demand", 'Starlink Capacity'!$A:$A, 0)` must resolve (Sprint 4 R18 IFERROR-0 wrapper row — proves Sprint 4 wired the IFERROR-0 read).
   - `MATCH("ODC DTC Gbps demand", 'Starlink Capacity'!$A:$A, 0)` must resolve (Sprint 4 R20).
   - `MATCH("BB pool at-cost rate ($/Gbps/yr)", 'Starlink Capacity'!$A:$A, 0)` must resolve (Sprint 4 R48).
   - `MATCH("DTC pool at-cost rate ($/Gbps/yr)", 'Starlink Capacity'!$A:$A, 0)` must resolve (Sprint 4 R50).
   Halt if ANY missing — indicates Sprint 4 didn't land cleanly OR canonical labels drifted from Sprint 5 spec expectations.
7. **Sprint 3 canonical labels on Customer Launch tab** confirmed via MATCH calls:
   - `MATCH("Starship internal kg demand (post-Starlink + ODC + AI Stack)", 'Customer Launch'!$A:$A, 0)` must resolve (Sprint 3 R22 — the IFERROR-0 wrapper row that reads `ODC Starship kg demand`).
   - `MATCH("Starship internal launches (V3 BB + V3 DTC + ODC + AI Stack)", 'Customer Launch'!$A:$A, 0)` must resolve (Sprint 3 R69 — IFERROR-0 wrapper that reads `ODC Starship launches (internal)`).
   Halt if either missing — indicates Sprint 3 didn't land cleanly.
8. **Sprint 2 canonical label on Launch Capacity tab** confirmed:
   - `MATCH("Starship at-cost rate ($mm/launch)", 'Launch Capacity'!$A:$A, 0)` must resolve (Sprint 2 R40 / Patch E §6.13).
   - `MATCH("Total Annual Capacity (kg-to-LEO)", 'Launch Capacity'!$A:$A, 0)` must resolve.
   Halt if either missing — indicates Sprint 2 (or Patch E) didn't land cleanly.
9. **Assumptions §6 ODC section** confirmed via `MATCH("§6 ODC", Assumptions!$A:$A, 0)`. Halt if section header missing. Plus spot-check key ODC inputs:
   - `INDEX(Assumptions!$B:$B, MATCH("Compute power per sat (kW)", Assumptions!$A:$A, 0))` = 140.
   - `INDEX(Assumptions!$B:$B, MATCH("Total sat dry mass (kg)", Assumptions!$A:$A, 0))` = 1400.
   - `INDEX(Assumptions!$B:$B, MATCH("ODC fleet design life (years)", Assumptions!$A:$A, 0))` = 5.
   - `INDEX(Assumptions!$B:$B, MATCH("Credence on Model A (Pr(A))", Assumptions!$A:$A, 0))` = 0.6.
   - `INDEX(Assumptions!$B:$B, MATCH("CoreWeave baseline anchor ($B/GW_IT/yr, 2026)", Assumptions!$A:$A, 0))` = 12.
   - `INDEX(Assumptions!$B:$B, MATCH("LR — subsystems (per doubling)", Assumptions!$A:$A, 0))` = 0.15.
10. **Assumptions stub rows 316-317 present** (precondition for §3.1.e deletion) — plugin reads A316 + A317 to verify Sprint 4 added the stubs there. If the rows are at different numbers (Sprint 4 appended below a different last-used row), plugin reports actual row numbers and asks Vlad to confirm before deletion.
11. **Sprint 4 Starlink R120 + R131 formulas** confirmed via direct cell read — plugin reads D120 + D131 formula text to confirm Sprint 4's pre-demand-cap formulas (Available Gbps × $/Gbps with no MIN cap). If formulas already include demand-cap (`MIN(...)` pattern), §3.1.b is a no-op — proceed but log.
12. **Demand Curves tab presence check** — plugin reads sheet names list. If `Demand Curves` tab already exists (V9 inheritance), §3.1.a builds in-place; if absent, §3.1.a creates as new sheet at position #14. Either way, plugin verifies sheet position = #14 post-build.
13. **Forward weight Assumptions read** — `INDEX(Assumptions!$B:$B, MATCH("Forward IRR weight (Blended IRR formula)", Assumptions!$A:$A, 0))` = 0.7.

### §3.1 — Sprint 4.5 patch absorption (executes FIRST, before §3.2 onwards)

Per `project-demand-curves-stub-remove-in-sprint-5` memory + 2026-05-20 Vlad lock. Sprint 4 left five outstanding items deferred to Sprint 4.5; absorbed here as Sprint 3-style patch. Plugin executes §3.1.a → §3.1.b → §3.1.c → §3.1.d → §3.1.e in order. Each substep has its own atomic-write block + verification read-back.

#### §3.1.a — Build Demand Curves tab (sheet position #14)

**Plugin action:** if Demand Curves tab exists (V9 inheritance), use in place; if absent, insert new sheet at position #14.

**Tab structure:**
- Row 1: title `Demand Curves` (bold, charcoal fill, white text)
- Row 2: blank
- Row 3: blank
- Row 4: year header — D4=2025, E4=2026, F4=2027, ..., AC4=2050 (hardcoded integers, per Architecture §2)
- Row 5: year offset helper — D5=0, E5=1, F5=2, ..., AC5=25 (hardcoded integers, per Principle 13)
- Row 6: blank
- Row 7: section header `BANDWIDTH DEMAND CURVES — total addressable bandwidth by pool` (charcoal/white)
- Row 8: blank

**Year-row inputs (rows 9-12, all four published as canonical labels):**

| Row | Col A label | Base Case year-row trajectory (D / I / S / AC anchors; linear interp between) | MC Min | MC Max | MC Distribution |
|---|---|---|---|---|---|
| R9 | `Total BB Gbps demand (Gbps/yr)` | D=80000, I=180000, S=400000, AC=600000 | 0.5× | 2.0× | triangle-yearrow |
| R10 | `Total BB price ($/Gbps/yr)` | D=96200, I=79250, S=56600, AC=45300 | 0.7× | 1.3× | triangle-yearrow |
| R11 | `Total DTC Gbps demand (Gbps/yr)` | D=300, I=900, S=2200, AC=3500 | 0.5× | 2.0× | triangle-yearrow |
| R12 | `Total DTC price ($/Gbps/yr)` | D=1207692, I=970000, S=739000, AC=577000 | 0.7× | 1.3× | triangle-yearrow |

**Full 26-cell year-row values (post-2026-05-20 amendment 1 to preserve Sprint 4 calibration $7,852M ±5%):**

| Year | Col | R9 BB Gbps demand | R10 BB price ($/Gbps/yr) | R11 DTC Gbps demand | R12 DTC price ($/Gbps/yr) |
|---|---|---|---|---|---|
| 2025 | D | 80000 | 96200 | 300 | 1207692 |
| 2026 | E | 100000 | 92810 | 420 | 1160154 |
| 2027 | F | 120000 | 89420 | 540 | 1112615 |
| 2028 | G | 140000 | 86030 | 660 | 1065077 |
| 2029 | H | 160000 | 82640 | 780 | 1017538 |
| 2030 | I | 180000 | 79250 | 900 | 970000 |
| 2031 | J | 202000 | 76985 | 1030 | 946900 |
| 2032 | K | 224000 | 74720 | 1160 | 923800 |
| 2033 | L | 246000 | 72455 | 1290 | 900700 |
| 2034 | M | 268000 | 70190 | 1420 | 877600 |
| 2035 | N | 290000 | 67925 | 1550 | 854500 |
| 2036 | O | 312000 | 65660 | 1680 | 831400 |
| 2037 | P | 334000 | 63395 | 1810 | 808300 |
| 2038 | Q | 356000 | 61130 | 1940 | 785200 |
| 2039 | R | 378000 | 58865 | 2070 | 762100 |
| 2040 | S | 400000 | 56600 | 2200 | 739000 |
| 2041 | T | 420000 | 55470 | 2330 | 722800 |
| 2042 | U | 440000 | 54340 | 2460 | 706600 |
| 2043 | V | 460000 | 53210 | 2590 | 690400 |
| 2044 | W | 480000 | 52080 | 2720 | 674200 |
| 2045 | X | 500000 | 50950 | 2850 | 658000 |
| 2046 | Y | 520000 | 49820 | 2980 | 641800 |
| 2047 | Z | 540000 | 48690 | 3110 | 625600 |
| 2048 | AA | 560000 | 47560 | 3240 | 609400 |
| 2049 | AB | 580000 | 46430 | 3370 | 593200 |
| 2050 | AC | 600000 | 45300 | 3500 | 577000 |

**Per-row write pattern (Rule 1):**
1. Write A{row} label as discrete `set_cell` call.
2. Write D{row} anchor value (Base Case 2025) as discrete call.
3. Write E{row}..AC{row} year-row values (each year-row is a single contiguous-row write per Rule 2).
4. Format pass: `numFmt = "#,##0"` for Gbps rows; `numFmt = "$#,##0"` for price rows.
5. MC fields: write AG{row} (MC Min multiplier), AH{row} (MC Max multiplier), AI{row} (`triangle-yearrow`), AJ{row} (notes — "Demand curve calibrated to Mach33 bandwidth thesis; Sprint 5 prep stub; refine in Sprint 12 MC overlay").

**Year-row values rationale:** D=2025 BB demand anchored at 80,000 Gbps (Mach33-disclosed Starlink total addressable); D=2025 DTC demand at 300 Gbps. **D=2025 prices CALIBRATED to preserve Sprint 4's $7,852M Starlink+DTC anchor** post-demand-cap (amended 2026-05-20 after plugin halt on first-pass anchor mismatch; original draft anchors D10=$85,000 + D12=$523,000 algebraically yielded $6,868M < $7,000M halt floor):

- BB 2025: demand cap binds (80,000 < 575,504 Available Gbps) → revenue = 80,000 × $96,200 = $7,696M = Sprint 4 BB anchor.
- DTC 2025: supply cap binds (130 Available Gbps < 300 demand) → revenue = 130 × $1,207,692 = $157M = Sprint 4 DTC anchor (exact match — same $1.21M/Gbps effective rate Sprint 4 used).
- Sum 2025: $7,853M ≈ Sprint 4 anchor $7,852M (within $1M rounding).

Out-year price trajectory: BB declines 53% by 2050 ($96,200 → $45,300 reflects bandwidth commoditization); DTC declines 52% by 2050 ($1,207,692 → $577,000 reflects DTC premium compression as market saturates). Out-year demand growth: BB 7.5× by 2050 (80K → 600K Gbps); DTC 11.7× by 2050 (300 → 3,500 Gbps). All values linear-interp between the four anchor years (D/I/S/AC). Refined in post-Sprint-12 MC retune.

**Verification read-back (Rule 4):** D9 = 80000; I9 = 180000; AC9 = 600000. D10 = 96200; I10 = 79250; AC10 = 45300. D11 = 300; AC11 = 3500. D12 = 1207692; I12 = 970000; AC12 = 577000. Halt if any > 1% deviation on price rows or any mismatch on Gbps demand rows.

#### §3.1.b — Re-wire Starlink R120 + R131 to demand-cap mechanic

**Pre-write read:** plugin reads D120 + D131 formula text on Starlink tab. Expected post-Sprint-4 formulas (no demand cap): R120 = `=INDEX('Starlink Capacity'!$D:$AC, MATCH("BB Gbps available for external Starlink revenue", 'Starlink Capacity'!$A:$A, 0), D$5+1) × INDEX(Assumptions!$D:$AC, MATCH("BB $/Gbps ($/Gbps/yr, year-row)", Assumptions!$A:$A, 0), D$5+1) / 1000000` (or equivalent reading from Assumptions stub).

**Overwrite formula (R120):**
```
D120 = =MIN(
    IFERROR(INDEX('Starlink Capacity'!$D:$AC, MATCH("BB Gbps available for external Starlink revenue", 'Starlink Capacity'!$A:$A, 0), D$5+1), 0),
    IFERROR(INDEX('Demand Curves'!$D:$AC, MATCH("Total BB Gbps demand (Gbps/yr)", 'Demand Curves'!$A:$A, 0), D$5+1), 0)
  ) * IFERROR(INDEX('Demand Curves'!$D:$AC, MATCH("Total BB price ($/Gbps/yr)", 'Demand Curves'!$A:$A, 0), D$5+1), 0) / 1000000
```
copyToRange source D120, destination E120:AC120.

**Overwrite formula (R131):** identical pattern with `Total DTC Gbps demand (Gbps/yr)` + `Total DTC price ($/Gbps/yr)` + `DTC Gbps available for external Starlink revenue`.
```
D131 = =MIN(
    IFERROR(INDEX('Starlink Capacity'!$D:$AC, MATCH("DTC Gbps available for external Starlink revenue", 'Starlink Capacity'!$A:$A, 0), D$5+1), 0),
    IFERROR(INDEX('Demand Curves'!$D:$AC, MATCH("Total DTC Gbps demand (Gbps/yr)", 'Demand Curves'!$A:$A, 0), D$5+1), 0)
  ) * IFERROR(INDEX('Demand Curves'!$D:$AC, MATCH("Total DTC price ($/Gbps/yr)", 'Demand Curves'!$A:$A, 0), D$5+1), 0) / 1000000
```
copyToRange source D131, destination E131:AC131.

**Verification:** read D120 + D131 + I120 + I131 + S120 + S131 + AC120 + AC131. Confirm:
- Starlink+DTC revenue 2025 ≈ $7,852M ±5% (sum of D120 + D131 should match Sprint 4 anchor). If outside [$7,000M, $8,700M] = halt.
- 2030, 2040, 2050 values now demand-capped — should be LOWER than pre-cap supply-side values; if higher in any year, halt (formula bug).
- of which DTC 2025 = D131 ≈ $157M ±15%.

**Per-vehicle IRR re-wire (R212/R217/R222/R227 area on Starlink):** Sprint 4 per-vehicle IRR engines need re-wiring to marginal-Gbps × demand-cap-aware price so IRR tapers as fleet supply approaches demand.

Plugin reads current R212/R217/R222/R227 formula text. The per-vehicle marginal revenue formula needs updating from `per-sat-Gbps × Total BB price` to `per-sat-Gbps × effective marginal $/Gbps` where effective marginal = `MIN(Total BB price, IFERROR(BB Revenue / BB Gbps consumed, 0))` — i.e., the realized $/Gbps blended after the demand cap binds.

**Effective marginal $/Gbps memo rows (append to Starlink tab, rows 230-231 per Rule 10 append-only):**
- R230: `Memo: Effective marginal $/Gbps BB (post-demand-cap)` (italic) = `=IFERROR(D120 * 1000000 / INDEX('Starlink Capacity'!$D:$AC, MATCH("Total active BB Gbps", 'Starlink Capacity'!$A:$A, 0), D$5+1), 0)`. copyToRange E230:AC230.
- R231: `Memo: Effective marginal $/Gbps DTC (post-demand-cap)` (italic) = `=IFERROR(D131 * 1000000 / INDEX('Starlink Capacity'!$D:$AC, MATCH("Total active DTC Gbps", 'Starlink Capacity'!$A:$A, 0), D$5+1), 0)`. copyToRange E231:AC231.

**Per-vehicle IRR engines reads (R212 area):** update each engine's per-sat marginal revenue formula to use R230 (BB engines) or R231 (DTC engines) instead of `Total BB price` / `Total DTC price` from Assumptions stub. Plugin reads each engine's formula text first, then overwrites with the memo-row read.

#### §3.1.c — Constellation D&A retune (Starlink R-constellation-D&A)

Sprint 4 §7.1 deferred: Constellation D&A 2025 = ~$437M vs Q4'25 target $707M ±10%. Gap: missing legacy V1/V1.5 D&A (~$130M) + facility D&A (~$140M).

**Plugin reads current Constellation D&A formula on Starlink tab.** Locate via MATCH on `Constellation D&A ($mm)` label. Append two memo rows below current formula (Rule 10 append-only — find the next empty row after Sprint 4's last-used row on Starlink tab):

- R232: `Memo: Legacy V1/V1.5 D&A ($mm)` (italic) — anchor $130M 2025, decay to 0 by 2029 (4-yr straight-line per Sprint 0 R103). Formula: `=IF(E$5 < 4, 130 - 130 * E$5 / 4, 0)`. D232 = 130. copyToRange E232:AC232.

Wait — Rule 14 forbids hardcoded constants. Move 130 and 4 to Assumptions amendments. See §3.2.c amendment.

Revised formula (after §3.2.c amendments add Assumptions inputs): `D232 = =MAX(0, INDEX(Assumptions!$B:$B, MATCH("Legacy V1/V1.5 D&A baseline ($mm, 2025 anchor)", Assumptions!$A:$A, 0)) - INDEX(Assumptions!$B:$B, MATCH("Legacy V1/V1.5 D&A baseline ($mm, 2025 anchor)", Assumptions!$A:$A, 0)) * E$5 / INDEX(Assumptions!$B:$B, MATCH("Legacy V1/V1.5 D&A useful life (yrs)", Assumptions!$A:$A, 0)))`. copyToRange E232:AC232.

- R233: `Memo: Facility D&A — sat manufacturing + ground stations ($mm)` (italic) — anchor $140M 2025, flat across horizon (rough proxy for sustaining facility D&A; refined post-Sprint-12). Formula: `=INDEX(Assumptions!$B:$B, MATCH("Facility D&A — sat manufacturing + ground stations ($mm/yr, flat)", Assumptions!$A:$A, 0))`. copyToRange D233:AC233.

**Update Total Constellation D&A formula (Rule 11 touch points):** locate Sprint 4's `Constellation D&A ($mm)` row, then OVERWRITE formula to add R232 + R233:
```
D{constellation-D&A} = D{Sprint-4-original-formula} + D232 + D233
```
(plugin reads original formula text, appends `+ D232 + D233`, writes back; copyToRange E:AC with the same pattern).

**Verification:** Constellation D&A 2025 read = pre-retune (~$437M) + $130M + $140M = ~$707M ±10%. Halt if outside [$600M, $850M]. Constellation D&A 2030 (post-V1/V1.5 retirement) = pre-retune + $0 + $140M; document landing.

#### §3.1.d — V3 BB Wright's Law on bandwidth-per-sat (Starlink R17 area)

Sprint 4 §7.2 deferred: V3 BB Gbps/sat held flat at 1,000. Implement Wright's Law learning on R17 using cum V3 BB sats running sum.

**Plugin reads current Starlink R17 formula.** Locate via MATCH on `V3 BB bandwidth per sat (Gbps)` or equivalent label. Expected pre-patch formula: hardcoded `=Assumptions reference to base 1000 Gbps`.

**Pre-step — add Assumptions amendment for cum V3 BB sats anchor and LR:** see §3.2.d.

**Overwrite formula:**
- Locate cum V3 BB sats running sum row (Sprint 4 wrote this — find via MATCH on `Cum V3 BB sats launched (running sum)` or equivalent).
- Anchor cum V3 BB sats = Assumptions input `V3 BB Wright's Law anchor — cum sats` (Base 100, MC [50, 500]).
- LR_V3_BB_bandwidth = Assumptions input `V3 BB bandwidth-per-sat Wright's Law learning rate (per doubling)` (Base 0.10 = 10%/doubling, MC [0.05, 0.20]).

```
D{R17 V3 BB Gbps/sat} = =INDEX(Assumptions!$B:$B, MATCH("V3 BB bandwidth per sat — base (Gbps)", Assumptions!$A:$A, 0)) *
                          IFERROR(
                            (MAX(D{cum_V3_BB}, INDEX(Assumptions!$B:$B, MATCH("V3 BB Wright's Law anchor — cum sats", Assumptions!$A:$A, 0))) /
                             INDEX(Assumptions!$B:$B, MATCH("V3 BB Wright's Law anchor — cum sats", Assumptions!$A:$A, 0))
                            ) ^ (LOG(1 + INDEX(Assumptions!$B:$B, MATCH("V3 BB bandwidth-per-sat Wright's Law learning rate (per doubling)", Assumptions!$A:$A, 0))) / LOG(2)),
                            1)
```
copyToRange E:AC same row.

**Sanity:** D17 = 1000 (anchor, no learning before anchor cum); 2030 cum V3 BB ~5,000 sats → 5,000/100 = 50× = log2(50) ≈ 5.64 doublings → 1.10^5.64 ≈ 1.74× → 2030 Gbps/sat ≈ 1,740 Gbps. Halt if 2030 Gbps/sat < 800 (under-learning) or > 1,500 (current cap before WL aggressive sanity).

Wait — that's a learning *gain* not loss. The 10% LR for *bandwidth-per-sat* means per doubling of cum sats, bandwidth-per-sat grows by 10%. So `(1 + LR)^doublings`. Confirmed formula structure above.

**Verification:** D17 = 1000 ±5%; I17 in range [1,200, 2,000] Gbps; S17 in range [1,800, 3,500] Gbps; AC17 in range [2,200, 5,000] Gbps. Halt if outside.

#### §3.1.e — Clear Assumptions stub rows 316-317

Per Principle 17 + Rule 17. Sprint 4 added two stub rows on Assumptions:
- R316: `BB $/Gbps ($/Gbps/yr, year-row)` — stub used by pre-§3.1.b Starlink R120 formula.
- R317: `DTC $/Gbps ($/Gbps/yr, year-row)` — stub used by pre-§3.1.b Starlink R131 formula.

After §3.1.b re-wires Starlink R120 + R131 to read from Demand Curves, these stubs are stale residue. Clear in place (Rule 10 — no row deletion; clear cells):

**Atomic clear sequence:**
1. Clear A316 (label).
2. Clear B316 (Base Case).
3. Clear C316 (notes).
4. Clear D316:AC316 (year-row values).
5. Clear AG316:AJ316 (MC fields).
6. Repeat 1-5 for R317.

**Verification:** plugin reads A316, A317 — both blank. Plugin scans Starlink tab for any remaining reads of `BB $/Gbps ($/Gbps/yr, year-row)` or `DTC $/Gbps ($/Gbps/yr, year-row)` via formula text grep — must be zero matches (§3.1.b should have re-wired all reads; any remaining = halt).

### §3.2 — Assumptions tab amendments (append below Sprint 4's last-used row)

Per Rule 10 (no row insertions; append-only). Plugin reads Assumptions tab last-used row and appends from next row onwards. Let `N` = first available row.

#### §3.2.a — ODC cash demand large default

Row N (label): `ODC cash demand large default ($mm)` (`val` type per Sprint 0 conventions).
- B{N}: 50000 (Base Case = $50,000M/yr flat; mirrors Starlink R141/R142 large-default pattern).
- C{N}: notes — "Large-default ODC cash ask year-row; ODC tab publishes Cash Demand = IF(Blended IRR > 0, this, 0). Sprint 10 Allocator's queue gate consumes. Pre-IRR-positive years deploy 0."
- D{N}:AC{N}: empty (single-value input, not year-row).
- AG{N}: 10000 (MC Min).
- AH{N}: 200000 (MC Max).
- AI{N}: `lognormal`.
- AJ{N}: notes — "Wide lognormal range — Mach33 doesn't have a tight prior on ODC capital appetite at IRR-positive equilibrium. Refined in Sprint 12 MC overlay."

Per-cell writes per Rule 1 (six discrete writes).

#### §3.2.b — ODC kg demand large default

Row N+1 (label): `ODC kg demand large default (kg)`.
- B{N+1}: 50000000 (Base 50M kg/yr flat — anchored to ~35,000 ODC sats × 1,400 kg/sat at scale).
- C{N+1}: notes — "Large-default ODC kg ask year-row; same masking pattern as cash demand. Sprint 10 Allocator kg queue consumes."
- D{N+1}:AC{N+1}: empty.
- AG{N+1}: 10000000.
- AH{N+1}: 200000000.
- AI{N+1}: `lognormal`.
- AJ{N+1}: notes — "Mirrors cash demand range proportionally on per-sat mass."

#### §3.2.c — Sprint 4.5 patch Assumptions amendments (Constellation D&A retune)

Row N+2: `Legacy V1/V1.5 D&A baseline ($mm, 2025 anchor)`.
- B{N+2}: 130. C{N+2}: "Legacy V1/V1.5 fleet D&A 2025 anchor; 4-yr straight-line retirement to 0 by 2029 (mirrors Sprint 0 R103)."
- AG{N+2}: 80. AH{N+2}: 200. AI{N+2}: `triangle`. AJ{N+2}: "MC range covers uncertainty on V1/V1.5 residual book value at Q4'25."

Row N+3: `Legacy V1/V1.5 D&A useful life (yrs)`.
- B{N+3}: 4. C{N+3}: "Straight-line retirement period for legacy V1/V1.5 fleet D&A."
- AG{N+3}: 3. AH{N+3}: 5. AI{N+3}: `triangle`.

Row N+4: `Facility D&A — sat manufacturing + ground stations ($mm/yr, flat)`.
- B{N+4}: 140. C{N+4}: "Sustaining facility D&A — flat across horizon as proxy; refined post-Sprint-12."
- AG{N+4}: 80. AH{N+4}: 250. AI{N+4}: `triangle`. AJ{N+4}: "MC covers facility expansion uncertainty."

#### §3.2.d — Sprint 4.5 patch Assumptions amendments (V3 BB Wright's Law on bandwidth)

Row N+5: `V3 BB bandwidth per sat — base (Gbps)`.
- B{N+5}: 1000. C{N+5}: "V3 BB base Gbps/sat (pre-Wright's-Law-learning anchor). Sprint 0 R30 reference."
- AG{N+5}: 500. AH{N+5}: 2000. AI{N+5}: `triangle`. AJ{N+5}: "V3 BB design spec uncertainty."

Row N+6: `V3 BB Wright's Law anchor — cum sats`.
- B{N+6}: 100. C{N+6}: "Cumulative V3 BB sats at which Wright's Law learning anchors begin (avoid divide-by-tiny-number)."
- AG{N+6}: 50. AH{N+6}: 500. AI{N+6}: `triangle`.

Row N+7: `V3 BB bandwidth-per-sat Wright's Law learning rate (per doubling)`.
- B{N+7}: 0.10. C{N+7}: "10% bandwidth-per-sat improvement per cum-sat doubling. Mach33 thesis — V3 BB hardware iterates with each generation batch."
- AG{N+7}: 0.05. AH{N+7}: 0.20. AI{N+7}: `triangle`. AJ{N+7}: "Wide range — speculative learning rate; bounded by chip+antenna physical limits."

**Verification of all §3.2 amendments:** plugin reads B{N}..B{N+7} + AG/AH/AI/AJ cells. Confirm Base Case + MC fields populated. Halt if any field empty on a non-fixed distribution input.

### §3.3 — ODC tab body (rows 11-199) — cell-by-cell

Per Rule 1 (one concept per write). Plugin writes in section order. Each section: labels block first, then anchor/formula block, then copyToRange E:AC pass, then format pass, then read-back verification (Rule 4).

For brevity, formulas reference Assumptions / Launch Capacity / Starlink Capacity by full INDEX/MATCH on canonical label. Plugin uses the label strings verbatim.

#### §3.3.1 — Section header + sat physical reads (rows 11-22)

- R11: blank
- R12: `ODC SAT PHYSICAL & COST STACK` (charcoal/white header)
- R13: blank
- R14: A14 = `Compute power per sat (kW)`. D14 = `=INDEX(Assumptions!$B:$B, MATCH("Compute power per sat (kW)", Assumptions!$A:$A, 0))`. (Single-value input — no copyToRange; column D only.)
- R15: A15 = `Total sat dry mass (kg)`. D15 = `=INDEX(Assumptions!$B:$B, MATCH("Total sat dry mass (kg)", Assumptions!$A:$A, 0))`.
- R16: A16 = `Sat solar generation (W)`. D16 = `=INDEX(Assumptions!$B:$B, MATCH("Sat solar generation (W, for $/W subsystem cost)", Assumptions!$A:$A, 0))`.
- R17: A17 = `Sat thermal mass (kg)`. D17 = `=INDEX(Assumptions!$B:$B, MATCH("Sat thermal mass (kg)", Assumptions!$A:$A, 0))`.
- R18: A18 = `F_ref — reference compute unit (TFLOPS, H100 FP8)`. D18 = `=INDEX(Assumptions!$B:$B, MATCH("F_ref — reference compute unit (TFLOPS, H100 FP8 dense)", Assumptions!$A:$A, 0))`.
- R19: A19 = `Effective Compute Ratio (ECR)`. D19 = `=INDEX(Assumptions!$B:$B, MATCH("Effective Compute Ratio (ECR)", Assumptions!$A:$A, 0))`.
- R20: A20 = `ODC fleet design life (years)`. D20 = `=INDEX(Assumptions!$B:$B, MATCH("ODC fleet design life (years)", Assumptions!$A:$A, 0))`.
- R21: blank
- R22: A22 = `▸ Chip roadmap reads (year-rows)` (italic, light grey fill subsection header).

Format pass: D14, D15, D16, D17, D18, D20 = `numFmt "#,##0"`; D19 = `numFmt "0.00"`.

**Verification:** D14=140, D15=1400, D16=156000, D17=480, D18=1979, D19=0.6, D20=5. Halt if any mismatch.

#### §3.3.2 — Chip roadmap year-rows (rows 23-28)

Year-row reads from Assumptions §6 chip roadmap (R173-R178 area).

- R23: A23 = `Chip TDP per chip (W) — year-row`. D23 = `=INDEX(Assumptions!$D:$AC, MATCH("Chip TDP per chip (W) — year-row", Assumptions!$A:$A, 0), D$5+1)`. copyToRange D23, E23:AC23.
- R24: A24 = `Chip FP8 per chip (TFLOPS) — year-row`. D24 = `=INDEX(Assumptions!$D:$AC, MATCH("Chip FP8 performance per chip (TFLOPS) — year-row", Assumptions!$A:$A, 0), D$5+1)`. copyToRange E24:AC24.
- R25: A25 = `Chip mass per chip (kg) — year-row`. D25 = `=INDEX(Assumptions!$D:$AC, MATCH("Chip mass per chip (kg) — year-row", Assumptions!$A:$A, 0), D$5+1)`. copyToRange E25:AC25.
- R26: A26 = `Chip cost per chip ($) — year-row`. D26 = `=INDEX(Assumptions!$D:$AC, MATCH("Chip cost per chip ($) — year-row", Assumptions!$A:$A, 0), D$5+1)`. copyToRange E26:AC26.
- R27: A27 = `Price per H100-equiv GPU-hr ($) — year-row`. D27 = `=INDEX(Assumptions!$D:$AC, MATCH("Price per H100-equiv GPU-hr ($) — year-row", Assumptions!$A:$A, 0), D$5+1)`. copyToRange E27:AC27.
- R28: A28 = `Utilization % (fleet ramp) — year-row`. D28 = `=INDEX(Assumptions!$D:$AC, MATCH("Utilization % (fleet ramp) — year-row", Assumptions!$A:$A, 0), D$5+1)`. copyToRange E28:AC28.

Format pass: R23 = `#,##0`; R24 = `#,##0`; R25 = `0.0`; R26 = `$#,##0`; R27 = `$0.00`; R28 = `0.0%`.

**Verification:** D23=700, I23=566.667, S23=600, AC23=600. D27=2.00, I27=1.5476, S27=0.9266, AC27=0.5548. D28=40%, I28=85%, S28=85%, AC28=85%. Halt if any > 5% deviation.

#### §3.3.3 — Per-sat derived physical (rows 29-32)

- R29: A29 = `Chips per sat`. D29 = `=IFERROR(D14 * 1000 / D23, 0)`. copyToRange E29:AC29. (Compute power kW → W via ×1000, divided by TDP W. Year-row because chip TDP varies year over year.)
- R30: A30 = `Sat PFLOPS (FP8, per sat per year computed)`. D30 = `=IFERROR(D29 * D24 / 1000, 0)`. copyToRange E30:AC30. (Chips × FP8 TFLOPS / 1000 → PFLOPS per sat.)
- R31: A31 = `Sat chip mass (kg)`. D31 = `=D29 * D25`. copyToRange E31:AC31. (Chips × mass per chip.)
- R32: A32 = `▸ Subsystem unit costs + Wright's Law` (italic subsection header).

Format: R29 = `#,##0`; R30 = `0.00`; R31 = `0.0`.

**Verification:** D29 = 140 × 1000 / 700 = 200 chips. I29 = 140 × 1000 / 566.667 ≈ 247 chips. D30 = 200 × 1979 / 1000 ≈ 395.8 PFLOPS/sat. I30 ≈ 247 × 3659.67 / 1000 ≈ 904 PFLOPS/sat. D31 = 200 × 1.2 = 240 kg. Halt if any > 5% deviation.

#### §3.3.4 — Subsystem cost stack (rows 33-44)

Read subsystem unit costs from Assumptions; compute per-sat subsystem cost; apply Wright's Law learning.

- R33: A33 = `Solar array cost per sat ($)`. D33 = `=D16 * INDEX(Assumptions!$B:$B, MATCH("Solar array unit cost ($/W)", Assumptions!$A:$A, 0))`. (Single-year — no copyToRange; constant year over year because sat physical doesn't vary.)

Actually wait — sat physical inputs (R14-R17) are single-value (column D only). But subsystem $ values are constant across years pre-Wright's-Law application. Then Wright's Law multiplier varies by year (cum-sats-driven). So subsystem cost year-row = D-anchor × WL multiplier (year-varying).

Let me restructure: write the pre-WL cost in column D only, then write the post-WL year-row in a separate row.

Revised:
- R33: A33 = `Solar array cost per sat ($, pre-WL)`. D33 = `=D16 * INDEX(Assumptions!$B:$B, MATCH("Solar array unit cost ($/W)", Assumptions!$A:$A, 0))`. (D only.)
- R34: A34 = `Thermal system cost per sat ($, pre-WL)`. D34 = `=D17 * INDEX(Assumptions!$B:$B, MATCH("Thermal system unit cost ($/kg)", Assumptions!$A:$A, 0))`.
- R35: A35 = `Comms (ISL set) cost per sat ($, pre-WL)`. D35 = `=INDEX(Assumptions!$B:$B, MATCH("Comms (ISL set) flat cost ($)", Assumptions!$A:$A, 0))`.
- R36: A36 = `ADCS + avionics cost per sat ($, pre-WL)`. D36 = `=INDEX(Assumptions!$B:$B, MATCH("ADCS + avionics flat cost ($)", Assumptions!$A:$A, 0))`.
- R37: A37 = `Structure cost per sat ($, pre-WL)`. D37 = `=INDEX(Assumptions!$B:$B, MATCH("Structure flat cost ($)", Assumptions!$A:$A, 0))`.
- R38: A38 = `Battery cost per sat ($, pre-WL)`. D38 = `=INDEX(Assumptions!$B:$B, MATCH("Battery flat cost ($)", Assumptions!$A:$A, 0))`.
- R39: A39 = `Shielding cost per sat ($, pre-WL)`. D39 = `=INDEX(Assumptions!$B:$B, MATCH("Shielding flat cost ($)", Assumptions!$A:$A, 0))`.
- R40: A40 = `Integration & Test cost per sat ($, pre-WL)`. D40 = `=INDEX(Assumptions!$B:$B, MATCH("Integration & Test flat cost ($)", Assumptions!$A:$A, 0))`.
- R41: A41 = `Sat subsystem cost (pre-WL, $)`. D41 = `=SUM(D33:D40)`.

**Wright's Law application — cum ODC sats running sum (Rule 23 exception, year-chained):**

- R42: A42 = `Cum ODC sats deployed (running sum) — Rule 23 exception, intentional`. D42 = 0. E42 = `=D42 + E{sats-deployed}`. copyToRange E42, F42:AC42. (References row 84 sats deployed — see §3.3.7.)

Actually need to forward-reference R84 (sats deployed). Will write sats deployed row first then come back. To avoid forward reference issues, the cum-sats running sum is structurally safe because Excel resolves references at calc time (iterative calc handles).

- R43: A43 = `Wright's Law multiplier on subsystems (year-row)`. D43 = `=IFERROR(MAX(1, D42 / INDEX(Assumptions!$B:$B, MATCH("Anchor year for ODC Wright's Law", Assumptions!$A:$A, 0)))^(LOG(1 - INDEX(Assumptions!$B:$B, MATCH("LR — subsystems (per doubling)", Assumptions!$A:$A, 0))) / LOG(2)), 1)`. copyToRange E43:AC43.

Wait — the Wright's Law anchor in Assumptions is `Anchor year for ODC Wright's Law` = 2026 (a year, not a cum-sat anchor). That's wrong for cum-sats-based WL. Need an explicit cum-sat anchor.

Actually re-reading Assumptions: R166 = `Anchor year for ODC Wright's Law` = 2026 — this is the year at which WL anchors (1.0 multiplier). Pre-anchor (2025) and post-anchor (2027+) the multiplier is computed relative to cum sats at anchor year.

OK so the Wright's Law mechanic is anchor-year-based. Need cum sats at anchor year, then WL multiplier = (cum_sats_today / cum_sats_at_anchor)^learning_exponent.

In 2025-2026 cum sats ≈ 0 (no deployment), so we need a small denominator floor to avoid divide-by-zero. Use `MAX(D42, 1)` for denominator. Pre-anchor years multiplier defaults to 1 (no learning yet).

Revised:
- R43: D43 = `=IF(E$5 < (INDEX(Assumptions!$B:$B, MATCH("Anchor year for ODC Wright's Law", Assumptions!$A:$A, 0)) - 2025), 1, IFERROR(MAX(1, D42 / MAX(1, INDEX($D42:$AC42, 1, INDEX(Assumptions!$B:$B, MATCH("Anchor year for ODC Wright's Law", Assumptions!$A:$A, 0)) - 2025 + 1)))^(LOG(1 - INDEX(Assumptions!$B:$B, MATCH("LR — subsystems (per doubling)", Assumptions!$A:$A, 0))) / LOG(2)), 1))`. copyToRange E43:AC43.

This is getting unwieldy. Let me simplify by capturing the anchor cum-sats in a helper cell:

- R44: A44 = `Cum ODC sats at WL anchor year`. D44 = `=INDEX($D42:$AC42, 1, INDEX(Assumptions!$B:$B, MATCH("Anchor year for ODC Wright's Law", Assumptions!$A:$A, 0)) - 2025 + 1)`. (Single-cell — D only. Reads cum sats at anchor year column.)

Now R43 simplifies:
- R43: D43 = `=IF(E$5 < (INDEX(Assumptions!$B:$B, MATCH("Anchor year for ODC Wright's Law", Assumptions!$A:$A, 0)) - 2025), 1, IFERROR((MAX(D42, 1) / MAX($D$44, 1))^(LOG(1 - INDEX(Assumptions!$B:$B, MATCH("LR — subsystems (per doubling)", Assumptions!$A:$A, 0))) / LOG(2)), 1))`. copyToRange E43:AC43.

Per-sat subsystem cost with WL:
- R45: A45 = `Sat subsystem cost (with WL, $) — year-row`. D45 = `=$D$41 * D43`. copyToRange E45:AC45. (Subsystem pre-WL × year-varying WL multiplier.)

#### §3.3.5 — Chip cost per sat (rows 46-48)

- R46: A46 = `Chip cost per sat ($) — year-row`. D46 = `=D29 * D26`. copyToRange E46:AC46. (Chips × chip cost per chip. No WL on chips per Sprint 0 R164=0 — LR-chips = 0.)
- R47: A47 = `Sat total cost ($, year-row)`. D47 = `=D45 + D46`. copyToRange E47:AC47.
- R48: A48 = `Sat total cost ($mm, year-row)`. D48 = `=D47 / 1000000`. copyToRange E48:AC48.

Format: R33-R41 = `$#,##0`; R45-R47 = `$#,##0`; R48 = `$#,##0.00`; R43 = `0.000`; R44 = `#,##0`; R42 = `#,##0`.

**Verification (Sprint 5 pre-deployment, cum sats = 0):** D45 = D41 × D43 = sum(R33:R40) × 1 (no WL pre-anchor) ≈ D41 = $1.248M (rough sum of subsystem costs at base values). D46 = 200 × $30,000 = $6,000,000. D47 ≈ $7.25M. D48 ≈ $7.25M. AC48 (with WL after substantial cum sats by 2050): D48 × (multiplier ≈ 0.5-0.7 depending on cum sats) plus chip cost decline.

#### §3.3.6 — Sats per Starship launch + launch services consumption (rows 49-55)

- R49: blank
- R50: A50 = `LAUNCH SERVICES (paid to Launch Capacity at fully-allocated at-cost rate)` (charcoal/white).
- R51: A51 = `Sats per Starship launch (Compute config)`. D51 = `=ROUNDDOWN(INDEX('Launch Capacity'!$D:$AC, MATCH("Total Annual Capacity (kg-to-LEO)", 'Launch Capacity'!$A:$A, 0), D$5+1) / IFERROR(INDEX('Launch Capacity'!$D:$AC, MATCH("Starship launches per year", 'Launch Capacity'!$A:$A, 0), D$5+1), 1) / D$15, 0)`. copyToRange E51:AC51.

Actually that's overly complex. Better — derive sats per launch directly from Starship payload to LEO / sat dry mass.

Revised: Sprint 0 doesn't have a `Starship LEO payload per launch (kg)` direct input as a single number — it's encoded in Launch Capacity's variant mix logic. Easier path: assume booster-only Compute payload = 150,000 kg / 1,400 kg/sat ≈ 107 sats per launch. Add as Assumptions amendment if absent.

To keep §3.2 scope tight, add one more amendment:
- Row N+8: `Starship LEO payload per launch — Compute config (kg)`. B=150000. C="Booster-only mode per Sprint 0 Launch Capacity §3". AG=120000. AH=180000. AI=`triangle`.

Now R51 simplifies:
- R51: D51 = `=ROUNDDOWN(INDEX(Assumptions!$B:$B, MATCH("Starship LEO payload per launch — Compute config (kg)", Assumptions!$A:$A, 0)) / $D$15, 0)`. (Single-value — D only.)

(150,000 / 1,400 = 107 sats per Starship launch in Compute config.)

- R52: A52 = `Starship at-cost rate ($mm/launch) — read from Launch Capacity`. D52 = `=INDEX('Launch Capacity'!$D:$AC, MATCH("Starship at-cost rate ($mm/launch)", 'Launch Capacity'!$A:$A, 0), D$5+1)`. copyToRange E52:AC52.
- R53: A53 = `Launch services cost per sat ($mm)`. D53 = `=IFERROR(D52 / $D$51, 0)`. copyToRange E53:AC53.

**Canonical publish (Sprint 3 reads):**
- R54: A54 = `ODC Starship launches (internal)`. D54 = `=IFERROR($D$84 / $D$51, 0)` (sats deployed / sats per launch). copyToRange E54:AC54. (R84 = sats deployed; forward ref OK under iterative calc.)
- R55: A55 = `ODC Starship kg demand`. D55 = `=$D$84 * $D$15` (sats deployed × sat dry mass kg). copyToRange E55:AC55.

Format: R51 = `#,##0`; R52 = `$#,##0.00`; R53 = `$#,##0.00`; R54 = `#,##0.0`; R55 = `#,##0`.

**Verification (Sprint 5 pre-deployment):** D51 = 107 sats/launch. D52 reads Sprint 2 R40 value (likely ~$25-40M/launch in 2025 from at-cost rate calc). D53 ≈ $0.25-0.40M/sat. D54 = 0 (R84 = 0). D55 = 0.

**STALE-REF SCAN CHECKPOINT 1:** plugin re-runs Customer Launch R22 + R69 MATCH calls now that ODC R54 + R55 labels exist:
- `MATCH("ODC Starship launches (internal)", ODC!$A:$A, 0)` → must resolve.
- `MATCH("ODC Starship kg demand", ODC!$A:$A, 0)` → must resolve.
- Read D{Customer Launch R22} + D{Customer Launch R69} — both should now reflect $0 from ODC (other contributors stay as-is).

#### §3.3.7 — Deployment, fleet ramp, cash/kg demand publish (rows 60-90)

- R60: blank
- R61: A61 = `DEPLOYMENT, FLEET RAMP, CASH/KG DEMAND PUBLISH` (charcoal/white).
- R62: A62 = `ODC cash demand large default ($mm) — Assumptions read`. D62 = `=INDEX(Assumptions!$B:$B, MATCH("ODC cash demand large default ($mm)", Assumptions!$A:$A, 0))`. (Single-value — D only.)
- R63: A63 = `ODC kg demand large default (kg) — Assumptions read`. D63 = `=INDEX(Assumptions!$B:$B, MATCH("ODC kg demand large default (kg)", Assumptions!$A:$A, 0))`.
- R64: A64 = `Cash demand year-row published ($mm) — masked by Blended IRR > 0`. D64 = `=IF(IFERROR($D$209, 0) > 0, $D$62, 0)`. copyToRange E64:AC64. (R209 = Blended IRR — forward reference under iterative calc.)
- R65: A65 = `Kg demand year-row published (kg) — masked by Blended IRR > 0`. D65 = `=IF(IFERROR($D$209, 0) > 0, $D$63, 0)`. copyToRange E65:AC65.

**Allocator IN reads (already in place from Sprint 1 at rows 8-9):**
- R8 reads `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("ODC cash allocation", Allocator!$A:$A, 0), D$5+1), 0)` — placeholder 0 from Allocator until Sprint 10.
- R9 reads `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("ODC kg allocation", Allocator!$A:$A, 0), D$5+1), 0)`.

Sprint 5 doesn't touch R8 / R9 — Sprint 1 wrote them.

- R66: A66 = `Wanted sats deployed (uncapped, cash-derived)`. D66 = `=IFERROR($D$62 / $D$48, 0)`. copyToRange E66:AC66. (Cash demand / cost per sat.)
- R67: A67 = `Sats deployable from cash allocation`. D67 = `=IFERROR($D$8 / $D$48, 0)`. copyToRange E67:AC67. (Allocator cash / cost per sat.)
- R68: A68 = `Sats deployable from kg allocation`. D68 = `=IFERROR($D$9 / $D$15, 0)`. copyToRange E68:AC68. (Allocator kg / sat dry mass.)

**Actual sats deployed (Architecture §6.5 MIN of cash / kg / uncapped demand):**
- R69: A69 = `Sats deployed (actual)`. D69 = `=ROUNDDOWN(MIN(D66, D67, D68), 0)`. copyToRange E69:AC69.

In Sprint 5 pre-Allocator-lit-up, R8 = 0 → R67 = 0 → R69 = 0 always (allocator-gated to 0).

**Sat retirements (cohort-based, anchor-and-offset compliant — NOT Rule 23 exception):**
- R70: A70 = `Sat retirements (year-row, N-year cohort linear)`. D70 = `=IF(E$5 < $D$20, 0, INDEX($D$69:$AC$69, 1, MAX(1, COLUMN()-COLUMN($D$5)+1-$D$20)))`. copyToRange E70:AC70.

INDEX col_num=0 spill guard (per memory `feedback-index-col-zero-spills`): `MAX(1, col_num)` wrapper ensures col_num >= 1.

This says: retirements in year T = sats deployed in year (T − design_life). For 2025-2029 (within first design-life window), retirements = 0. From 2030 onwards, retirements = sats deployed in (T − 5).

In Sprint 5 pre-Allocator-lit-up, R69 = 0 always → R70 = 0 always.

**Active fleet EoY (Rule 23 exception — year-chained):**
- R71: A71 = `Active sat fleet EoY (year-chained, Rule 23 exception)`. D71 = `=MAX(0, $D$69 - $D$70)` (year 1 = launches − retirements, no BoY). E71 = `=MAX(0, D71 + E$69 - E$70)`. copyToRange E71, F71:AC71.

In Sprint 5 pre-Allocator-lit-up, R71 = 0 always.

**Fleet aggregates:**
- R72: A72 = `Fleet PFLOPS (FP8)`. D72 = `=D71 * D30`. copyToRange E72:AC72.
- R73: A73 = `Fleet compute power (GW)`. D73 = `=D71 * D14 / 1000000`. copyToRange E73:AC73. (kW → GW via /1e6.)
- R74: A74 = `Fleet annual PFLOP-hrs delivered (util-adjusted)`. D74 = `=D72 * D28 * D19 * 8760`. copyToRange E74:AC74. (PFLOPS × util × ECR × hours/year = PFLOP-hrs delivered.)

Format: R62 = `$#,##0`; R63 = `#,##0`; R64 = `$#,##0`; R65 = `#,##0`; R66-R69 = `#,##0`; R70 = `#,##0.0`; R71 = `#,##0`; R72 = `#,##0`; R73 = `#,##0.000`; R74 = `#,##0`.

**Verification (Sprint 5):** D62 = 50000, D63 = 50000000. D64 = 0 (R209 = 0 initially under iterative calc; first pass converges). D65 = 0. D66 = 50000 / D48 ≈ 50000 / 7.25 ≈ 6,896. D67 = 0 / D48 = 0. D68 = 0 / 1400 = 0. D69 = ROUNDDOWN(MIN(6896, 0, 0), 0) = 0. D70 = 0. D71 = 0. D72-R74 = 0.

#### §3.3.8 — Bandwidth claim derivation + publish (rows 75-85)

- R75: blank
- R76: A76 = `BANDWIDTH CLAIM & SERVICES COST (paid to Starlink at fully-allocated at-cost rate)` (charcoal/white).
- R77: A77 = `Gbps per GWh/yr ODC compute energy conversion factor`. D77 = `=INDEX(Assumptions!$B:$B, MATCH("Gbps per GWh/yr of ODC compute energy", Assumptions!$A:$A, 0))`. (Sprint 0 R138 stub = 0.05.)
- R78: A78 = `BB-share of ODC bandwidth claim`. D78 = `=INDEX(Assumptions!$B:$B, MATCH("BB-share of ODC bandwidth claim", Assumptions!$A:$A, 0))`. (Sprint 0 R139 stub = 0.50.)
- R79: A79 = `Fleet ODC compute energy delivered (GWh/yr)`. D79 = `=D73 * D28 * 8760`. copyToRange E79:AC79. (Fleet GW × util × hours/yr = GWh/yr.)
- R80: A80 = `Total ODC Gbps demand`. D80 = `=D79 * $D$77`. copyToRange E80:AC80.

**Canonical publish (Sprint 4 reads):**
- R81: A81 = `ODC BB Gbps demand`. D81 = `=D80 * $D$78`. copyToRange E81:AC81.
- R82: A82 = `ODC DTC Gbps demand`. D82 = `=D80 * (1 - $D$78)`. copyToRange E82:AC82.

**Read Starlink Capacity at-cost rates:**
- R83: A83 = `BB pool at-cost rate ($/Gbps/yr) — read from Starlink Capacity`. D83 = `=IFERROR(INDEX('Starlink Capacity'!$D:$AC, MATCH("BB pool at-cost rate ($/Gbps/yr)", 'Starlink Capacity'!$A:$A, 0), D$5+1), 0)`. copyToRange E83:AC83.
- R84: A84 = `DTC pool at-cost rate ($/Gbps/yr) — read from Starlink Capacity`. D84 = `=IFERROR(INDEX('Starlink Capacity'!$D:$AC, MATCH("DTC pool at-cost rate ($/Gbps/yr)", 'Starlink Capacity'!$A:$A, 0), D$5+1), 0)`. copyToRange E84:AC84.

**WAIT — R84 was already used for sats-deployed forward reference in §3.3.6 (R54/R55). I have a row conflict.**

Let me re-do row numbering. R54/R55 forward-referenced `$D$84` for sats deployed. But §3.3.7 places sats deployed at R69, not R84. Let me fix R54/R55 to reference R69.

Going back: R54 = `=IFERROR($D$69 / $D$51, 0)` and R55 = `=$D$69 * $D$15`. (Fix the forward reference to R69.)

Then R83 / R84 are free for at-cost rate reads. Continuing:

**Bandwidth services cost:**
- R85: A85 = `ODC BB bandwidth cost ($mm/yr)`. D85 = `=D81 * D83 / 1000000`. copyToRange E85:AC85.
- R86: A86 = `ODC DTC bandwidth cost ($mm/yr)`. D86 = `=D82 * D84 / 1000000`. copyToRange E86:AC86.
- R87: A87 = `Bandwidth services cost ($mm)`. D87 = `=D85 + D86`. copyToRange E87:AC87. (CANONICAL — Sprint 9 R106 elimination reads this.)

Format: R77 = `0.000`; R78 = `0.0%`; R79 = `#,##0`; R80-R82 = `#,##0`; R83-R84 = `$#,##0`; R85-R87 = `$#,##0.00`.

**Verification (Sprint 5):** D77 = 0.05. D78 = 0.50. D79 = 0 (fleet=0). D80 = 0. D81 = 0, D82 = 0 (CANONICAL PUBLISHES at $0 throughout horizon under Sprint 5). D83 / D84 = read from Starlink Capacity (some non-zero value because Starlink has active BB/DTC sats — but ODC Gbps demand = 0 so cost = 0). D85 = D86 = D87 = 0.

**STALE-REF SCAN CHECKPOINT 2:** plugin re-runs Starlink Capacity R18 + R20 MATCH calls:
- `MATCH("ODC BB Gbps demand", ODC!$A:$A, 0)` → must resolve (R81).
- `MATCH("ODC DTC Gbps demand", ODC!$A:$A, 0)` → must resolve (R82).
- Read D18 + D20 on Starlink Capacity — both should now reflect ODC's published 0.

#### §3.3.9 — Dual revenue model (Pr(A)-weighted) (rows 90-110)

- R88: blank
- R89: A89 = `DUAL REVENUE MODEL (Pr(A) × Model A + Pr(B) × Model B; Architecture §9.2)` (charcoal/white).

**Model A — energy-anchored (CoreWeave baseline × PUE uplift × util):**
- R90: A90 = `CoreWeave baseline ($B/GW_IT/yr, 2026 anchor)`. D90 = `=INDEX(Assumptions!$B:$B, MATCH("CoreWeave baseline anchor ($B/GW_IT/yr, 2026)", Assumptions!$A:$A, 0))`. (Single-value — D only.)
- R91: A91 = `Terrestrial price deflation %/yr`. D91 = `=INDEX(Assumptions!$B:$B, MATCH("Terrestrial price deflation %/yr (Model A baseline year-row driver)", Assumptions!$A:$A, 0))`.
- R92: A92 = `Adjusted CoreWeave baseline year-row ($B/GW_IT/yr)`. D92 = `=$D$90 * (1 - $D$91)^MAX(0, E$5 - 1)`. copyToRange E92:AC92. (2025 = anchor value (year offset 0), 2026 = anchor (offset 1 → year-1 deflation), then decay. Anchor-and-offset compliant.)

Actually anchor year for CoreWeave is 2026 (per R181 description), so:
- D92 (2025): no deflation yet = anchor / (1 - deflation) (to back out one year). Or treat 2025 as pre-anchor with anchor value.
- Use: D92 = `=$D$90 * (1 - $D$91)^MAX(0, E$5 - 1)`. For E$5 = 0 (2025): (1-deflation)^(-1) ≈ slightly higher than anchor. For E$5 = 1 (2026): anchor. For E$5 = 25 (2050): anchor × (1 - 5%)^24 ≈ anchor × 0.292.

Simpler: anchor in 2026, flat at anchor for 2025, deflate from 2026 onward:
- D92 = `=IF(E$5 < 1, $D$90, $D$90 * (1 - $D$91)^(E$5 - 1))`. copyToRange E92:AC92.

- R93: A93 = `PUE uplift (orbital advantage = PUE_base / PUE_orbital)`. D93 = `=INDEX(Assumptions!$B:$B, MATCH("PUE_base (terrestrial colo)", Assumptions!$A:$A, 0)) / INDEX(Assumptions!$B:$B, MATCH("Orbital PUE", Assumptions!$A:$A, 0))`. (= 1.4 / 1.12 = 1.25.)
- R94: A94 = `Steady-state utilization`. D94 = `=INDEX(Assumptions!$B:$B, MATCH("Steady-state utilization (for Model A util-adjustment ratio)", Assumptions!$A:$A, 0))`.

Per-sat Model A revenue per year:
- R95: A95 = `Per-sat Model A revenue ($mm/yr) — energy-anchored`. D95 = `=(D14 / 1000000) * D92 * 1000 * $D$93 * D28`. copyToRange E95:AC95.

Breakdown: compute power (kW) → GW = / 1,000,000. × adjusted CoreWeave baseline ($B/GW_IT/yr) = $B/yr per sat. × 1000 = $mm/yr. × PUE uplift (orbital advantage). × util year-row (fleet ramp).

Wait CoreWeave baseline is $B/GW_IT/yr — so multiplying by GW gives $B. Then to $mm multiply by 1000. The 8760 isn't needed because the baseline is already annualized.

Sanity check: 140 kW = 0.00014 GW × $12B/GW/yr × 1.25 × 0.4 (2025 util) = $0.00084B = $840 = $0.00084M per sat per year. That looks tiny. Let me re-check CoreWeave baseline.

Hmm — CoreWeave's $12B/GW_IT/yr means $12,000 per kW_IT/yr or $12/W_IT/yr. So 140 kW × $12 / W × 1000 W/kW × 1.25 × 0.4 = $840,000 per sat per year = $0.84M per sat per year. So Model A revenue per sat ≈ $0.84M/yr in 2025 at low util.

That matches industry ballpark for hyperscaler GPU revenue per kW ($/kW_IT/yr in five-figure range).

Revised formula:
- R95: D95 = `=D14 * D92 * 1000 * $D$93 * D28 / 1000`. (kW × $B/GW_IT/yr × 1000 (GW to MW conversion implicit) — actually let me redo units.)

Units: D14 = kW. D92 = $B/GW_IT/yr. To get $mm/yr per sat:
- kW × ($B/GW_IT/yr) = kW × $B/yr / GW_IT = kW × $B/yr × (1 GW / 1,000,000 kW) = $B/yr × kW / GW × 1/1,000,000 = (kW/GW) × $B/yr × 1e-6. 1 GW = 1,000,000 kW. So 140 kW / 1,000,000 = 0.00014 GW. × $12B/yr = $0.00168B/yr = $1.68M/yr (before PUE + util).
- Then × PUE uplift 1.25 = $2.1M/yr at full util. × util 0.4 = $0.84M/yr in 2025.

To get $mm: D14 / 1,000,000 × D92 × 1,000 = D14 × D92 / 1,000 = 140 × 12 / 1000 = $1.68M/yr at full util.

So:
- R95: D95 = `=D14 * D92 / 1000 * $D$93 * D28`. copyToRange E95:AC95.

Sanity: 140 × 12 / 1000 × 1.25 × 0.4 = 1.68 × 0.5 = $0.84M/yr per sat in 2025. Good.

**Model B — η-anchored (billable H100-equiv GPU-hrs × $/GPU-hr):**
- R96: A96 = `Per-sat billable H100-equiv GPU-hrs/yr`. D96 = `=D29 * (D24 / $D$18) * D28 * $D$19 * 8760`. copyToRange E96:AC96.

Breakdown: chips per sat × (chip TFLOPS / H100 F_ref TFLOPS) = H100-equiv chips × util × ECR × hours/yr = billable H100-equiv GPU-hrs/yr per sat.

- R97: A97 = `Per-sat Model B revenue ($mm/yr) — η-anchored`. D97 = `=D96 * D27 / 1000000`. copyToRange E97:AC97. (GPU-hrs × $/GPU-hr / 1e6 → $mm.)

**Pr(A)-weighted Expected Revenue per sat:**
- R98: A98 = `Pr(A) (Architecture §9.2)`. D98 = `=INDEX(Assumptions!$B:$B, MATCH("Credence on Model A (Pr(A))", Assumptions!$A:$A, 0))`.
- R99: A99 = `Per-sat Expected Revenue ($mm/yr) — Pr-A-weighted`. D99 = `=$D$98 * D95 + (1 - $D$98) * D97`. copyToRange E99:AC99.

**Internal vs external compute split:**
- R100: A100 = `Internal compute share to AI Stack % — year-row`. D100 = `=INDEX(Assumptions!$D:$AC, MATCH("ODC internal compute share to AI Stack % — year-row", Assumptions!$A:$A, 0), D$5+1)`. copyToRange E100:AC100.
- R101: A101 = `External compute share to customers % — year-row`. D101 = `=INDEX(Assumptions!$D:$AC, MATCH("ODC external compute share to customers % — year-row", Assumptions!$A:$A, 0), D$5+1)`. copyToRange E101:AC101.

**Fleet revenue split (external at market, internal at at-cost):**
- R102: A102 = `Per-sat external compute revenue ($mm/yr) — at market`. D102 = `=D99 * D101`. copyToRange E102:AC102.
- R103: A103 = `Fleet external compute revenue ($mm/yr)`. D103 = `=D71 * D102`. copyToRange E103:AC103.

Format: R90-R94 = various; R95-R97 = `$#,##0.000`; R98 = `0.00`; R99-R102 = `$#,##0.000`; R103 = `$#,##0`; R100-R101 = `0.0%`.

**Verification (Sprint 5 pre-deployment):** D90 = 12. D91 = 0.05. D92 = 12 (2025 = anchor). D93 = 1.4/1.12 = 1.25. D94 = 0.85. D95 = 140 × 12 / 1000 × 1.25 × 0.4 = $0.84M/yr per sat. D96 = 200 × (1979/1979) × 0.4 × 0.6 × 8760 = 200 × 1 × 0.4 × 0.6 × 8760 = 420,480 GPU-hrs/sat/yr. D97 = 420,480 × $2.00 / 1e6 = $0.84M/sat/yr. (Symmetric with Model A by design.) D99 = 0.6 × 0.84 + 0.4 × 0.84 = $0.84M/sat/yr. D100 = 0.95. D101 = 0.05. D102 = 0.84 × 0.05 = $0.042M/sat/yr external. D103 = 0 × 0.042 = $0 fleet external.

#### §3.3.10 — ODC at-cost compute rate calculation + canonical publish (rows 110-125)

Per Architecture §7.3 + 2026-05-20 lock: at-cost rate per PFLOP-hr = (ODC fully-allocated annual cost) / (ODC total annual PFLOP-hrs produced).

- R104: blank
- R105: A105 = `ODC FULLY-ALLOCATED COST + AT-COST COMPUTE RATE (Architecture §7.3)` (charcoal/white).

**Fully-allocated cost components:**
- R106: A106 = `Annual sat D&A ($mm/yr)`. D106 = `=D71 * D48 / D20`. copyToRange E106:AC106. (Active fleet × per-sat cost / design life. Straight-line per-sat D&A.)
- R107: A107 = `Annual launch services cost ($mm/yr)`. D107 = `=D54 * D52`. copyToRange E107:AC107. (Internal launches × at-cost rate.)
- R108: A108 = `Annual bandwidth services cost ($mm/yr)`. D108 = `=D87`. copyToRange E108:AC108. (= bandwidth services cost from §3.3.8.)
- R109: A109 = `Annual insurance cost ($mm/yr)`. D109 = `=D103 * INDEX(Assumptions!$B:$B, MATCH("ODC insurance % of revenue", Assumptions!$A:$A, 0))`. copyToRange E109:AC109. (% of external revenue.)
- R110: A110 = `Annual other COGS ($mm/yr)`. D110 = `=D103 * INDEX(Assumptions!$B:$B, MATCH("ODC other COGS % of revenue", Assumptions!$A:$A, 0))`. copyToRange E110:AC110.
- R111: A111 = `Annual ground ops cost ($mm/yr)`. D111 = `=D103 * INDEX(Assumptions!$B:$B, MATCH("Ground station / network opex % of revenue", Assumptions!$A:$A, 0))`. copyToRange E111:AC111.
- R112: A112 = `Total fully-allocated ODC cost ($mm/yr)`. D112 = `=D106 + D107 + D108 + D109 + D110 + D111`. copyToRange E112:AC112.

**At-cost rate per PFLOP-hr:**
- R113: A113 = `ODC at-cost compute rate ($/PFLOP-hr)`. D113 = `=IFERROR(D112 * 1000000 / D74, 0)`. copyToRange E113:AC113. (CANONICAL — Sprint 6 AI Stack reads this.)

Convert $mm to $ via × 1,000,000; divide by annual PFLOP-hrs delivered (D74). IFERROR-0 wrapper for pre-deployment when D74 = 0.

**Internal transfer revenue (at-cost):**
- R114: A114 = `Internal compute PFLOP-hrs delivered to AI Stack`. D114 = `=D74 * D100`. copyToRange E114:AC114.
- R115: A115 = `Internal transfer revenue (at-cost compute) ($mm)`. D115 = `=D114 * D113 / 1000000`. copyToRange E115:AC115. (CANONICAL — Sprint 9 R107 elimination reads this.)

Format: R106-R112 = `$#,##0.00`; R113 = `$#,##0.00`; R114 = `#,##0`; R115 = `$#,##0.00`.

**Verification (Sprint 5 pre-deployment):** D71 = 0 → D106 = 0. D54 = 0 → D107 = 0. D108 = 0. D103 = 0 → D109, D110, D111 = 0. D112 = 0. D74 = 0 → D113 = 0 (via IFERROR). D114 = 0. D115 = 0.

#### §3.3.11 — Total revenue + COGS + P&L (rows 120-140)

- R120: blank
- R121: A121 = `MODULE P&L` (charcoal/white).
- R122: A122 = `External compute revenue ($mm/yr)`. D122 = `=D103`. copyToRange E122:AC122. (= fleet external revenue from R103.)
- R123: A123 = `Internal transfer revenue (at-cost compute) ($mm/yr)`. D123 = `=D115`. copyToRange E123:AC123. (= internal transfer from R115.)
- R124: A124 = `Total Revenue ($mm)`. D124 = `=D122 + D123`. copyToRange E124:AC124.

**COGS:**
- R125: A125 = `COGS — Constellation D&A ($mm)`. D125 = `=D106`. copyToRange E125:AC125.
- R126: A126 = `COGS — Launch services cost ($mm)`. D126 = `=D107`. copyToRange E126:AC126.
- R127: A127 = `COGS — Bandwidth services cost ($mm)`. D127 = `=D108`. copyToRange E127:AC127.
- R128: A128 = `COGS — Ground ops ($mm)`. D128 = `=D111`. copyToRange E128:AC128.
- R129: A129 = `COGS — Insurance ($mm)`. D129 = `=D109`. copyToRange E129:AC129.
- R130: A130 = `COGS — Other COGS ($mm)`. D130 = `=D110`. copyToRange E130:AC130.
- R131: A131 = `Total COGS ($mm)`. D131 = `=SUM(D125:D130)`. copyToRange E131:AC131.

**Module EBITDA / FCF:**
- R132: A132 = `Gross Profit ($mm)`. D132 = `=D124 - D131`. copyToRange E132:AC132.
- R133: A133 = `Module EBITDA ($mm)`. D133 = `=D132`. copyToRange E133:AC133. (= Gross Profit per vending-machine framing.)
- R134: A134 = `Module EBITDA Margin %`. D134 = `=IFERROR(D133 / D124, 0)`. copyToRange E134:AC134.
- R135: A135 = `Module CapEx ($mm)`. D135 = `=D69 * D48`. copyToRange E135:AC135. (Sats deployed × per-sat cost.)
- R136: A136 = `Capital deployed ($mm) — diagnostic`. D136 = `=D135`. copyToRange E136:AC136. (Equilibrium-equal to Module CapEx for ODC; no CapEx lag per Sprint 3 convention.)
- R137: A137 = `Module FCF ($mm)`. D137 = `=D133 + D125 - D135`. copyToRange E137:AC137. (= EBITDA + D&A add-back − CapEx. Module D&A = D125 = D106. Pre-tax, pre-corp per Architecture §3.)

Format: R122-R137 except R134 = `$#,##0.00`; R134 = `0.0%`.

**Verification (Sprint 5):** D122 = 0. D123 = 0. D124 = 0. D125 = 0. ... D131 = 0. D132 = 0. D133 = 0. D134 = 0 (IFERROR). D135 = 0. D136 = 0. D137 = 0. ALL zero throughout horizon under Sprint 5 (allocator dormant).

### §3.4 — Per-sat marginal IRR engine (rows 145-165)

Per Architecture §5.1 + §9.4. Reads EXTERNAL compute revenue only (§7.3). N = 5 yrs (Sprint 0 R151). CF stream length N+1 = 6 (1 cost slug + 5 net revenue years).

- R145: blank
- R146: A146 = `PER-SAT MARGINAL IRR ENGINE (Architecture §9.4, reads external revenue only per §7.3)` (charcoal/white).

**Per-sat marginal cost components (year-row, all per single marginal sat at year T):**
- R147: A147 = `Per-sat upfront cost ($mm) — sat hardware + launch services per sat`. D147 = `=D48 + D53`. copyToRange E147:AC147. (Sat cost per sat + launch services cost per sat.)

**Per-sat marginal external revenue + per-sat marginal opex:**
- R148: A148 = `Per-sat ground ops cost ($mm/yr)`. D148 = `=D102 * INDEX(Assumptions!$B:$B, MATCH("Ground station / network opex % of revenue", Assumptions!$A:$A, 0))`. copyToRange E148:AC148.
- R149: A149 = `Per-sat insurance cost ($mm/yr)`. D149 = `=D102 * INDEX(Assumptions!$B:$B, MATCH("ODC insurance % of revenue", Assumptions!$A:$A, 0))`. copyToRange E149:AC149.
- R150: A150 = `Per-sat other COGS ($mm/yr)`. D150 = `=D102 * INDEX(Assumptions!$B:$B, MATCH("ODC other COGS % of revenue", Assumptions!$A:$A, 0))`. copyToRange E150:AC150.
- R151: A151 = `Per-sat bandwidth cost ($mm/yr)`. D151 = `=IFERROR(D87 / D71, 0)`. copyToRange E151:AC151. (Total bandwidth cost / fleet. IFERROR for pre-deployment fleet=0.)

Actually that's a fleet-level division; for marginal economics we want per-sat bandwidth share. Use per-sat formula: per-sat Gbps demand × at-cost rates.

Revised:
- R151: A151 = `Per-sat bandwidth cost ($mm/yr)`. D151 = `=((D14 * D28 * 8760 / 1000000) * $D$77 * $D$78 * D83 + (D14 * D28 * 8760 / 1000000) * $D$77 * (1 - $D$78) * D84) / 1000000`. copyToRange E151:AC151.

Breakdown: per-sat compute energy (GWh/yr) = D14 (kW) × util × 8760 / 1,000,000. × Gbps/(GWh/yr) conversion = per-sat Gbps demand. × BB share × BB at-cost rate ($/Gbps/yr) → per-sat BB cost ($/yr). + DTC analog. Total per-sat $/yr / 1e6 → $mm/yr.

Cleaner if I add helper rows:
- R152: A152 = `Per-sat BB Gbps demand`. D152 = `=(D14 * D28 * 8760 / 1000000) * $D$77 * $D$78`. copyToRange E152:AC152.
- R153: A153 = `Per-sat DTC Gbps demand`. D153 = `=(D14 * D28 * 8760 / 1000000) * $D$77 * (1 - $D$78)`. copyToRange E153:AC153.
- R151 revised: D151 = `=(D152 * D83 + D153 * D84) / 1000000`. copyToRange E151:AC151.

**Per-sat net marginal revenue:**
- R154: A154 = `Per-sat net marginal revenue ($mm/yr)`. D154 = `=D102 - D148 - D149 - D150 - D151`. copyToRange E154:AC154.

**Per-sat IRR engine — Spot IRR (current year):**
Per Architecture §5.1, CF stream length N+1 = 6. Position 1 = -cost (year T), positions 2-6 = net rev (years T+1 to T+N).

INDEX:INDEX horizontal slice of R154 for years T to T+N:
- R155: A155 = `Spot IRR`. D155 = `=IFERROR(IRR(IF(_xlfn.SEQUENCE(1, $D$20 + 1) = 1, -D147, IF(COLUMN($D154) + ROW($D$1:INDEX($D$1:$Z$1, $D$20 + 1)) - 1 - COLUMN($D$5) > 25, 0, INDEX($D$154:$AC$154, 1, COLUMN($D$5) + 1 + ROW($D$1:INDEX($D$1:$Z$1, $D$20 + 1)) - 1)))), -1)`. copyToRange D155, E155:AC155.

OK that's monstrous. Let me use the standard Architecture §5.1 pattern simpler:

`=IFERROR(IRR(IF(_xlfn.SEQUENCE(1, $D$20+1)=1, -D147, INDEX($D154:$AC154, 1, COLUMN()-COLUMN($D$5)+1) : INDEX($D154:$AC154, 1, COLUMN()-COLUMN($D$5)+$D$20+1))), -1)`

Hmm, the colon `:` between INDEX calls works in Excel for dynamic ranges. But for the IRR call, we need a single 1×(N+1) array. The horizontal slice INDEX:INDEX produces a range that IF can broadcast over.

But for terminal years (2049, 2050), the slice extends beyond column AC → INDEX out-of-range. IFERROR catches.

Standard formula:
- R155: D155 = `=IFERROR(IRR(IF(_xlfn.SEQUENCE(1, $D$20+1)=1, -D147, INDEX($D$154:$AC$154, 1, MAX(1, COLUMN()-COLUMN($D$5)+1)) : INDEX($D$154:$AC$154, 1, MIN(26, COLUMN()-COLUMN($D$5)+$D$20+1)))), -1)`. copyToRange E155:AC155.

The `MAX(1, ...)` and `MIN(26, ...)` guards protect against col_num spill (per memory `feedback-index-col-zero-spills`) and out-of-range references.

**Forward IRR (Y+2):**
Same engine, but cost slug at year T+2 and net rev for years T+3 to T+N+2.

- R156: A156 = `Forward IRR (Y+2)`. D156 = `=IFERROR(IRR(IF(_xlfn.SEQUENCE(1, $D$20+1)=1, -IF(COLUMN()-COLUMN($D$5)+3 > 26, D147, INDEX($D$147:$AC$147, 1, MIN(26, COLUMN()-COLUMN($D$5)+3))), INDEX($D$154:$AC$154, 1, MAX(1, MIN(26, COLUMN()-COLUMN($D$5)+3))) : INDEX($D$154:$AC$154, 1, MIN(26, COLUMN()-COLUMN($D$5)+$D$20+3)))), -1)`. copyToRange E156:AC156.

For T = 2049-2050 (column AB or AC), the cost-slug column COLUMN()-COLUMN($D$5)+3 exceeds 26 → use current year cost as fallback (IRR will fail to converge → IFERROR returns -1).

**Blended IRR:**
- R157: A157 = `Blended IRR`. D157 = `=(1 - INDEX(Assumptions!$B:$B, MATCH("Forward IRR weight (Blended IRR formula)", Assumptions!$A:$A, 0))) * D155 + INDEX(Assumptions!$B:$B, MATCH("Forward IRR weight (Blended IRR formula)", Assumptions!$A:$A, 0)) * D156`. copyToRange E157:AC157.

Format: R147-R154 = `$#,##0.00`; R155-R157 = `0.0%`; R152-R153 = `#,##0`.

**Verification (Sprint 5):** D147 = D48 + D53 = $7.25M + $0.25-0.40M = ~$7.5M. D154 = D102 - opex sum ≈ $0.042M - ($0.042M × ~6%) - bandwidth cost. With bandwidth cost ≈ per-sat BB Gbps × BB at-cost rate / 1e6 — this is the key driver of negative IRR.

If per-sat BB Gbps × at-cost rate exceeds per-sat external revenue, net rev = negative → IRR = -1 (IFERROR fallback because IRR can't converge). Expected outcome in 2025-2026: D154 < 0 → D155 = -1 (or close to it) → D157 = -1.

In 2030 (allocator-driven fleet now > 0, V3 BB Starlink at-cost rates lower, internal share down to 77.5%, util at 85%, terrestrial price compressed): per-sat external rev higher per sat (because util × external share) but per-sat bandwidth cost lower (V3 BB has more Gbps capacity per dollar) → net rev might turn positive → IRR positive → ODC starts being IRR-allocated.

### §3.5 — Allocator OUT contract overwrite (rows 200-210)

Per Architecture §4.2. Sprint 1 wrote literal 0 placeholders at R200-R210. Sprint 5 OVERWRITES in place with live formulas.

Plugin verifies (Rule 22 stale-ref): A200..A210 still contain the 11 canonical labels verbatim before overwriting. Halt if any label drifted.

- R200: A200 = `CENTRAL ALLOCATOR OUTPUTS` (header — Sprint 1 wrote, no overwrite).
- R201: D201 = `=D124`. copyToRange E201:AC201. (Total Revenue.)
- R202: D202 = `=D133`. copyToRange E202:AC202. (Module EBITDA.)
- R203: D203 = `=D134`. copyToRange E203:AC203. (Module EBITDA Margin %.)
- R204: D204 = `=D137`. copyToRange E204:AC204. (Module FCF.)
- R205: D205 = `=D135`. copyToRange E205:AC205. (Module CapEx.)
- R206: D206 = `=D136`. copyToRange E206:AC206. (Capital deployed.)
- R207: D207 = `=D155`. copyToRange E207:AC207. (Spot IRR.)
- R208: D208 = `=D156`. copyToRange E208:AC208. (Forward IRR.)
- R209: D209 = `=D157`. copyToRange E209:AC209. (Blended IRR.)
- R210: D210 = `=D65`. copyToRange E210:AC210. (Capacity Demand kg-to-LEO — = published kg demand year-row.)

**Note on R207-R209 vs R64-R65 forward references:** R64 (`Cash demand published`) and R65 (`Kg demand published`) reference R209 (`Blended IRR`) via the IRR-masking pattern. R209 in turn reads R157 which depends on R154 (net marginal rev) which depends on D102 (per-sat external rev) which depends on D71 (active fleet). In Sprint 5, D71 = 0 (Allocator dormant) → D102 = 0 → D154 = 0 - sum of opex which depends on D102 = 0 → D154 = 0 - 0 = 0 → IRR of [-D147, 0, 0, 0, 0, 0] = IFERROR returns -1 → D157 = -1 → R64 / R65 IF check `IFERROR(R209,0) > 0` → false → R64 = R65 = 0.

This is the intended pre-Allocator behavior. When Sprint 10 lights up Allocator, the chain endogenously activates.

Format: R201-R206 = `$#,##0.00`; R203 = `0.0%`; R207-R209 = `0.0%`; R210 = `#,##0`.

### §3.6 — Number format pass (final sweep)

Plugin applies number formats per-section in a final pass (Rule 1 — formats separate from formulas). Already enumerated in §3.3 / §3.4 / §3.5 substep notes.

---

## §4 — Verification gate (universal + Sprint 5 calibration §6.4)

Plugin executes after all §3 writes complete. Halt on any failure.

### §4.1 — Universal: zero formula errors workbook-wide

Read every cell on ODC + Starlink + Starlink Capacity + Demand Curves + Assumptions + Customer Launch + Launch Capacity + Allocator + Group P&L. Count occurrences of `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`. Expected: ZERO on display rows (IFERROR-wrapped IRR helper cells may contain `#NUM!` internally; only the wrapped output matters). Halt on any error in a display row.

### §4.2 — Universal: conservation block reads OK (trivial pre-Sprint-9)

Group P&L conservation block doesn't exist until Sprint 9; trivially holds in Sprint 5 because ODC publishes $0 across the board. R106 (Bandwidth elim) = Starlink internal bandwidth rev (= 0 because ODC Gbps demand = 0) − ODC bandwidth services cost (= 0) = 0 ✓. R107 (Compute elim) = ODC internal transfer rev (= 0) − AI Stack internal compute cost (not yet built) = 0 trivially ✓.

### §4.3 — Edge-year read-back (D / I / S / AC)

Plugin reads the following cells and confirms expected values. Halt on any > tolerance deviation.

| Cell | Expected (Sprint 5 pre-Allocator) | Tolerance | Halt threshold |
|---|---|---|---|
| ODC R124 D (Total Revenue 2025) | $0 | exact | any > $10M |
| ODC R124 I (Total Revenue 2030) | $0 | exact (pre-Allocator) | any > $10M |
| ODC R124 AC (Total Revenue 2050) | $0 | exact | any > $10M |
| ODC R133 D (Module EBITDA 2025) | $0 | exact | any > $10M |
| ODC R135 D (Module CapEx 2025) | $0 | exact | any > $10M |
| ODC R137 D (Module FCF 2025) | $0 | exact | any > $10M |
| ODC R69 D (Sats deployed 2025) | 0 | exact | any > 5 |
| ODC R69 I (Sats deployed 2030) | 0 | exact (pre-Allocator) | any > 5 |
| ODC R71 D (Active fleet end-2025) | 0 | exact | any > 5 |
| ODC R155 D (Spot IRR 2025) | ≤ 0 (likely -100% via IFERROR fallback) | n/a | any > 0 |
| ODC R157 D (Blended IRR 2025) | ≤ 0 | n/a | any > 0 |
| ODC R87 D (Bandwidth services cost 2025) | $0 | exact | any > $10M |
| ODC R113 D (At-cost compute rate $/PFLOP-hr 2025) | $0 (IFERROR for fleet=0) | exact | non-zero |
| ODC R81 D (ODC BB Gbps demand 2025) | 0 | exact | any > 0 |
| ODC R82 D (ODC DTC Gbps demand 2025) | 0 | exact | any > 0 |
| ODC R54 D (ODC Starship launches internal 2025) | 0 | exact | any > 0 |
| ODC R55 D (ODC Starship kg demand 2025) | 0 | exact | any > 0 |
| ODC R64 D (Cash demand published 2025) | $0 | exact | any > $0 |
| ODC R65 D (Kg demand published 2025) | 0 | exact | any > 0 |
| Sprint 4.5 patch: Starlink R120 D (BB revenue 2025) | $7,696M (post-amended Demand Curves anchors §3.1.a) | ±5% | <$7,000M or >$8,700M |
| Sprint 4.5 patch: Starlink R131 D (DTC revenue 2025) | $157M (130 supply × $1,207,692/Gbps = Sprint 4 effective rate preserved) | ±15% | <$80M or >$250M |
| Sprint 4.5 patch: Sum R120 + R131 D (Starlink+DTC 2025) | $7,853M ≈ Sprint 4 anchor $7,852M | ±5% | <$7,000M or >$8,700M |
| Sprint 4.5 patch: Starlink Constellation D&A 2025 | $707M | ±10% | <$600M or >$850M |
| Sprint 4.5 patch: Starlink V3 BB Gbps/sat 2025 | 1,000 Gbps | exact (anchor) | any deviation |
| Sprint 4.5 patch: Starlink V3 BB Gbps/sat 2030 | ~1,750 Gbps (WL with ~5K cum) | wide range | <800 or >2,500 |
| Demand Curves R9 D (Total BB Gbps demand 2025) | 80,000 | exact | mismatch |
| Demand Curves R10 D (Total BB price 2025) | $96,200 (calibrated to Sprint 4 anchor — amended 2026-05-20) | ±1% | mismatch |
| Demand Curves R11 D (Total DTC Gbps demand 2025) | 300 | exact | mismatch |
| Demand Curves R12 D (Total DTC price 2025) | $1,207,692 (= Sprint 4 effective DTC $/Gbps preserved) | ±1% | mismatch |
| Customer Launch R22 D (after ODC publishes — should now resolve, value still 0 from V3 BB + V3 DTC + ODC + AI Stack all = 0) | unchanged from Sprint 3 | n/a | #N/A or #REF! |
| Customer Launch R69 D (same — should resolve, ODC contribution = 0) | unchanged | n/a | #N/A or #REF! |
| Starlink Capacity R18 D (ODC BB Gbps demand — reads ODC R81 = 0) | 0 | exact | #N/A or #REF! |
| Starlink Capacity R20 D (ODC DTC Gbps demand — reads ODC R82 = 0) | 0 | exact | #N/A or #REF! |

### §4.4 — Round-trip stability (5x recalc)

Plugin executes `Application.Calculate` 5 times. Captures values of ODC R155, R156, R157, R124, R137, R209 each iteration. Confirms no value moves > $1M ($mm) or > 0.1% (IRR) across iterations. Halt on bistability.

In Sprint 5 with Allocator dormant, all values stay at 0 across iterations — convergence trivial. The within-year cycle (ODC ↔ Starlink Capacity) is dormant in Sprint 5; activates only when Sprint 10 Allocator drives sats deployed > 0.

### §4.5 — Stale-reference scan (Rule 22)

Plugin scans Allocator + Group P&L (when built — Sprint 9+) for any cross-tab pull to ODC. In Sprint 5, Allocator already has placeholders for ODC cash/kg allocation; verify by reading Allocator's R{ODC cash} and R{ODC kg} formula text — both reference `ODC!R200` block by label INDEX/MATCH (Sprint 1 wrote these).

Plus verify each of Sprint 5's five canonical publishes resolves correctly via downstream MATCH calls (per §3.0 pre-flight items 6-7, re-run post-write):
1. `MATCH("ODC BB Gbps demand", ODC!$A:$A, 0)` → R81. ✓
2. `MATCH("ODC DTC Gbps demand", ODC!$A:$A, 0)` → R82. ✓
3. `MATCH("ODC Starship launches (internal)", ODC!$A:$A, 0)` → R54. ✓
4. `MATCH("ODC Starship kg demand", ODC!$A:$A, 0)` → R55. ✓
5. `MATCH("ODC at-cost compute rate ($/PFLOP-hr)", ODC!$A:$A, 0)` → R113. ✓

### §4.6 — Don't-touch verification

Plugin spot-reads cells NOT in Sprint 5 scope to confirm no accidental damage. Read Sprint 4 anchor: Starlink+DTC revenue 2025 (sum R120+R131) = $7,852M ±5% (Sprint 4 holds post-Sprint 4.5 patch). Customer Launch 2025 F9 customer revenue = $4,290M ±5% (Sprint 3 holds). Launch Capacity F9 launches 2025 = 171 ±5 (Sprint 2 holds). Halt on any drift.

---

## §5 — Claude Log entry template

Plugin appends one row to Claude Log tab after sprint completes:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-MM-DD | 5 | ODC (full body), Starlink Capacity (no writes — IFERROR-0 reads at R18/R20 activate via ODC R81/R82 publishes), Customer Launch (no writes — IFERROR-0 reads at R22/R69 activate via ODC R54/R55 publishes), Starlink (Sprint 4.5 patch §3.1.b/c/d — R120 + R131 demand-cap rewrite + Constellation D&A retune + V3 BB WL on bandwidth-per-sat), Demand Curves (Sprint 4.5 patch §3.1.a — full tab build at sheet position #14 with four canonical year-rows), Assumptions (Sprint 4.5 patch §3.1.e stub row clear; §3.2 amendments — 8 new rows: ODC cash + kg demand large defaults, Sprint 4.5 patch Constellation D&A retune inputs ×3, Sprint 4.5 patch V3 BB WL inputs ×3) | Sprint 5 + Sprint 4.5 patch absorbed in single pass. ODC module body live with cash-driven deployment, dual revenue (Pr-A weighted), per-sat marginal IRR engine, fully-allocated at-cost compute rate publish, bandwidth services cost + launch services cost wired via canonical labels. Sprint 5 calibration §6.4 PASS: ODC revenue 2025 = $0 exact, sats deployed 2025 = 0 exact, fleet end-2025 = 0 exact, per-sat Blended IRR 2025 < 0 (Spot ≈ -100% via IFERROR fallback because per-sat net marginal rev pre-V3-BB-Starlink-at-cost-rates < 0). Sprint 4.5 patch calibration: Starlink+DTC 2025 = $7,852M ±5% holds post-demand-cap; Constellation D&A 2025 = $707M ±5% post-retune; V3 BB Gbps/sat 2025 = 1,000 exact (anchor pre-WL); 2030 ≈ 1,750 Gbps/sat. Per-vehicle IRR re-wire on Starlink R212/R217/R222/R227 reads memo-row effective marginal $/Gbps so IRR tapers as fleet supply approaches demand (no longer 99-144% runaway). Conservation R106 (Bandwidth elim) trivially $0; R107 (Compute elim) trivially $0 (AI Stack not built yet). Five canonical labels published Sprint 3/4/6 IFERROR-0 reads consume. | (1) Per-sat IRR engine returns -100% in early years via IFERROR fallback because per-sat net marginal rev is structurally negative pre-V3-BB-Starlink-at-cost-rates being live + ODC bandwidth cost dominating per-sat external revenue. Expected behavior — converts to positive when allocator drives sats > 0 AND V3 BB Starlink reduces at-cost rates AND internal share declines (more sats sold externally). Re-verify in Sprint 10 post-Allocator-light-up. (2) Sprint 5 R138/R139 stubs (Gbps/(GWh/yr) conversion = 0.05; BB-share = 0.50) carried forward unchanged from Sprint 0 — flagged for post-Sprint-12 calibration retune per memory `feedback-arbitrary-inputs-are-mc`. (3) Architecture §6.6 label-string drift reconciled — see §9 amendment log. | Sprint 6 — AI Stack module (reads `ODC at-cost compute rate ($/PFLOP-hr)` by INDEX/MATCH for its Internal compute cost from ODC COGS line). |

---

## §6 — Don't touch (out of scope)

- **Customer Launch tab body** (Sprint 3 + Sprint 3.5 own).
- **Launch Capacity tab body** (Sprint 2 + Patch E §6.13 own).
- **Starlink tab — anything outside §3.1.b R120 / R131 + §3.1.c Constellation D&A retune (R232/R233 memo rows + Constellation D&A formula update) + §3.1.d V3 BB Gbps/sat WL formula (R17 area) + §3.1.b per-vehicle IRR engine re-wires (R212/R217/R222/R227 area) + R230/R231 effective marginal $/Gbps memo rows.**
- **Starlink Capacity tab body** (Sprint 4 own). Sprint 5 publishes ODC labels that Starlink Capacity's existing IFERROR-0 reads at R18/R20 endogenously consume — no writes to Starlink Capacity.
- **Allocator tab body** (Sprint 1 skeleton + Sprint 10 brain). Sprint 5 reads Allocator IN placeholders for ODC cash/kg allocation; doesn't write to Allocator.
- **Group P&L / OpEx / CapEx / Valuation tabs** (Sprints 7-11).
- **AI Stack tab** (Sprint 6).
- **Lunar Mars tab** (Sprint 7).
- **Demand Curves tab year-row trajectory** — locked at §3.1.a values; refined post-Sprint-12 MC overlay.
- **Sprint 0 Assumptions §6 ODC inputs R143-R188** — locked. Sprint 5 reads via INDEX/MATCH.
- **Sprint 0 R17 Forward weight** = 0.7. Sprint 5 reads.

---

## §7 — Open thread (post-sprint considerations)

1. **Bandwidth claim derivation calibration** — R138 (Gbps/(GWh/yr) = 0.05) + R139 (BB-share = 0.50) carried forward as Sprint 0 stubs. Mach33 thesis on per-PFLOP bandwidth requirement to refine. Affects ODC bandwidth demand year-rows + bandwidth services cost. Post-Sprint-12 MC overlay retune.
2. **ODC at-cost compute rate volatility** — fully-allocated formula divides total cost by PFLOP-hrs. In early-ramp years (small fleet), per-PFLOP-hr rate could swing widely as fixed-ish costs (sat D&A, launch services) divide by small denominators. IFERROR-0 wrapper handles pre-deployment; consider floor / smoothing in Sprint 6 AI Stack if AI Stack's internal compute cost is volatile.
3. **Per-sat marginal IRR convergence under Sprint 10 within-year cycle** — once Allocator lights up, the cycle ODC sats → bandwidth demand → at-cost rate → bandwidth cost → IRR → allocation → sats activates. Convergence target <10 iter, no value > $1M in 5x recalc per memory `feedback-model-not-deterministic`. Sprint 10 verification reads round-trip stability. If bistable, candidate breaks: use prior-year Starlink Capacity at-cost rate (1-yr lag).
4. **Architecture §6.6 label drift reconciliation** — §9 amendment log notes the rename of Architecture's `At-cost launch services rate ($mm/launch)` aspiration to the actually-published `Starship at-cost rate ($mm/launch)` (Sprint 2 R40). Sprint 6 AI Stack inherits the same label reading pattern for its launch-cost-per-product line.
5. **Sprint 4.5 patch absorption — Demand Curves tab trajectory uncertainty** — §3.1.a Base Case trajectories are Mach33-thesis-anchored stubs. Total BB Gbps demand 2025 = 80,000 (anchored), 2050 = 600,000 (7.5× growth). Could be too conservative or too aggressive depending on AI demand for satellite backhaul + DTC market maturation. Post-Sprint-12 MC variation will cover.
6. **Per-vehicle IRR re-wire on Starlink (§3.1.b)** — effective marginal $/Gbps memo rows R230/R231 are post-demand-cap blends. Per-vehicle IRR engines now read these. Sprint 4 IRR run-away (99-144%) should taper. If still over 50% in any year, IRR formula structure may need further calibration in Sprint 4.6 patch.

---

## §8 — Execution sequence (plugin order)

Plugin executes in this exact order. Each section has its own atomic-write block + verification read-back. Halt on any verification failure.

1. **§3.0 Pre-flight checks** (workbook state, tab positions, year header/offset rows, Sprint 1-4 canonical labels resolve, iterative calc enabled, Assumptions stub rows present, Sprint 4 R120/R131 formulas readable).
2. **§3.1 Sprint 4.5 patch absorption:**
   - §3.1.a Build Demand Curves tab (sheet position #14, four canonical year-row inputs, format).
   - §3.1.b Re-wire Starlink R120 + R131 to demand-cap formulas + R230/R231 effective marginal $/Gbps memo rows + per-vehicle IRR engine re-wires (R212/R217/R222/R227).
   - §3.1.c Constellation D&A retune (R232 Legacy V1/V1.5 + R233 Facility D&A memo rows; update Total Constellation D&A formula).
   - §3.1.d V3 BB Wright's Law on bandwidth-per-sat (R17 area formula overwrite).
   - §3.1.e Clear Assumptions stub rows 316-317.
3. **§3.2 Assumptions amendments:** append 8 new rows (ODC cash + kg demand large defaults; Constellation D&A retune inputs ×3; V3 BB WL inputs ×3; Starship LEO payload Compute config 1).
4. **§3.3 ODC tab body:** write rows 11-137 in section order (§3.3.1 sat physical reads → §3.3.2 chip roadmap → §3.3.3 derived → §3.3.4 subsystem cost stack + WL → §3.3.5 chip cost → §3.3.6 launch services + canonical publishes R54/R55 → §3.3.7 deployment / fleet / cash & kg demand publishes → §3.3.8 bandwidth claim + cost + canonical publishes R81/R82 → §3.3.9 dual revenue → §3.3.10 at-cost compute rate + canonical publish R113 → §3.3.11 P&L). Each substep: labels block → anchor block → copyToRange E:AC → format pass → read-back.
5. **§3.4 Per-sat marginal IRR engine:** rows 145-157.
6. **§3.5 Allocator OUT contract overwrite:** rows 200-210 (Sprint 1 placeholders overwritten in place).
7. **§3.6 Number format final sweep.**
8. **§4.1-§4.6 Verification gate:** workbook-wide error scan, edge-year reads, round-trip stability, stale-ref scan, don't-touch verification.
9. **§5 Claude Log entry.**

Total estimated plugin runtime: ~30-45 minutes (1.5-day spec budget). Halt-and-resume tolerated; no save commands issued by plugin.

---

## §9 — Amendment log

- **2026-05-20 (Sprint 5 spec draft)** — drafted; absorbs Sprint 4.5 patch as §3.1; reads Launch Capacity `Starship at-cost rate ($mm/launch)` verbatim (Sprint 2 R40 / Patch E §6.13); publishes 5 canonical labels (`ODC BB Gbps demand`, `ODC DTC Gbps demand`, `ODC Starship launches (internal)`, `ODC Starship kg demand`, `ODC at-cost compute rate ($/PFLOP-hr)`) Sprint 3 + Sprint 4 IFERROR-0 reads consume + Sprint 6 AI Stack will read; per-sat marginal IRR engine per Architecture §9.4 verbatim with §7.3 lock (reads external compute revenue only); cash-driven deployment via large-default IRR-masked year-rows (Architecture §9.1); fully-allocated at-cost compute rate per Architecture §7.3 (2026-05-20 lock); Sprint 4.5 patch absorbs Demand Curves tab build (#14) + Starlink R120/R131 demand-cap mechanic + Constellation D&A retune ($707M ±10% target) + V3 BB Wright's Law on bandwidth-per-sat + Assumptions stub row deletion. Spec omits `Source workbook` / `Target workbook` header lines per standing process rule 2 (locked 2026-05-20). Rule 19 marked N/A (Vlad handles versioning entirely outside spec).

- **2026-05-20 amendment 1 (Demand Curves anchor calibration)** — first-draft Demand Curves anchors D10=$85,000 (BB price 2025) + D12=$523,000 (DTC price 2025) algebraically yielded post-demand-cap 2025 Starlink+DTC revenue = $6,868M, below the §4.3 halt floor of $7,000M. Plugin caught at §3.1.b execution and rolled back. Anchors amended: D10=$96,200 (= $7,696M target / 80,000 Gbps demand) + D12=$1,207,692 (= $157M target / 130 Gbps supply = Sprint 4 effective DTC rate preserved exactly). Full 26-cell year-rows for R10 + R12 amended via proportional scaling on the original trajectory shape (BB scale 1.132×, DTC scale 2.309×). Out-year decline rates preserved: BB −53% by 2050, DTC −52% by 2050. R9 (BB Gbps demand) and R11 (DTC Gbps demand) year-rows unchanged. Plugin resumed §3.1.b post-amendment. Lesson: spec author should pre-compute post-demand-cap calibration math (= MIN(supply, demand) × price) against Sprint 4 anchor before locking Demand Curves anchor values — algebraic infeasibility wasn't caught at draft time.

- **2026-05-20 amendment 2 (pre-flight label drift reconciliation)** — plugin §3.0 pre-flight surfaced four labels in the workbook that drifted from the spec's MATCH strings. Four labels safely renamed in workbook (zero downstream consumers): (a) `Customer Launch!A69` from `Starship internal launches (V3 BB + V3 DTC + ODC)` → `Starship internal launches (V3 BB + V3 DTC + ODC + AI Stack)` (note: rename adds "+ AI Stack" to LABEL but Sprint 3's R69 formula does NOT yet include an AI Stack term — Sprint 6 must add `AI Stack Starship launches (internal)` to the formula); (b) `Assumptions!A137` from `Gbps per GWh/yr of ODC compute energy (PLACEHOLDER)` → `Gbps per GWh/yr of ODC compute energy` (drop placeholder suffix); (c) `Assumptions!A138` from `BB-share of ODC bandwidth claim (PLACEHOLDER)` → `BB-share of ODC bandwidth claim`; (d) `Assumptions!A165` straight apostrophe `Wright's` → curly apostrophe `Wright's`.

- **2026-05-20 amendment 3 (Forward IRR weight published string preservation)** — spec §3.4 R157 was written to MATCH `Forward IRR weight (Blended IRR formula)`. Actual Sprint 0 publication at `Assumptions!A17` = `Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)` with 208 existing consumers across Customer Launch + Starlink. Spec §3.4 R157 formula amended to read the published string verbatim. Published reality wins (same pattern as Architecture §6.6 / Starship at-cost rate reconciliation). Lesson: spec author should grep the actual workbook for canonical labels before drafting MATCH strings — Sprint 0 had a different naming convention than later sprints assumed.

- **2026-05-20 amendment 4 (R64/R65 IRR-mask year-row anchor)** — spec §3.3.7 wrote R64/R65 IRR-mask as `IF(IFERROR($D$209,0)>0, $D$62, 0)` (absolute anchor on D209). That's a single-year all-or-nothing gate based on 2025 IRR, which would suppress 2030+ allocation even when IRR turns positive. Plugin corrected to `IF(IFERROR(D$209,0)>0, $D$62, 0)` (row-locked, column-relative on D209) so each year's mask reads its own year's Blended IRR. Spec §3.3.7 amended.

- **2026-05-20 amendment 5 (V3 BB bandwidth-per-sat base dedupe)** — spec §3.2.d / §3.3.x added Assumptions amendment `V3 BB bandwidth per sat — base (Gbps)`. Existing Sprint 0 `Assumptions!R77` already published `V3 BB Bandwidth per Sat — base year (Gbps)` = 1000 (capital B, capital S). Spec's duplicate row at A335 cleared in workbook; §3.1.d V3 BB WL formula reads the Sprint 0 R77 published string instead. Lesson: spec author should grep Assumptions for existing label-by-concept matches before adding new amendments — duplicate inputs violate Rule 14 spirit (single source of truth).

- **2026-05-20 amendment 6 (cum V3 BB sats running sum built fresh)** — spec §3.1.d assumed Sprint 4 had built a `Cum V3 BB sats launched (running sum)` row on Starlink for the WL learning denominator. Sprint 4 did NOT build this row. Plugin built fresh as new memo row `Starlink!R235`. Spec §3.1.d amended to enumerate the memo row build as part of §3.1.d execution (not assumed precondition).

- **2026-05-20 amendment 7 (Starlink R119/R129 orphan re-wire)** — Sprint 4 had memo rows `Starlink!R119` (BB $/Gbps year-row) + `R129` (DTC $/Gbps year-row) that read the now-deleted Assumptions stub rows 316/317. After §3.1.e cleared the stubs, R119/R129 returned #N/A. Re-wired to read `Demand Curves!R10` (Total BB price) + `Demand Curves!R12` (Total DTC price) — preserves the descriptive memo concept under the new sourcing.

- **2026-05-20 amendment 8 (pre-existing Sprint 3 bug surfaced — NOT caused by Sprint 5)** — Workbook-wide error scan §4.1 surfaced `Customer Launch!G16:AC16` = #N/A on 26 cells. Root cause: Customer Launch year-row formulas reference Assumptions label `Starship customer launch margin — CAGR (% change/yr from 2027 anchor)` which does NOT exist on Assumptions. F16 (the 2027 anchor = 4) resolves fine; G16 onward fails. Sprint 5 did NOT cause this; the missing Assumptions row was specified in Sprint 3 §4 amendments but never written to the workbook. Customer Launch 2025 calibration ($4,282M F9 customer revenue at `Customer Launch!D33`) holds — the broken row only affects out-year Starship customer margin which is dormant pre-2027. **Recommend Sprint 3.6 micro-patch**: add Assumptions row `Starship customer launch margin — CAGR (% change/yr from 2027 anchor)` with Base Case `=(1.5/4)^(1/23)-1 ≈ −4.10%/yr` (decay from 2027 anchor 4× toward 2050 floor 1.5×); MC range [-6%, -2%] triangle. Plus standard six-write atomic block per Rule 1.

- **Architecture §6.6 amendment (proposed as part of Sprint 5):** The Architecture doc's canonical label `At-cost launch services rate ($mm/launch)` (named in §6.6 + §7.1) was never implemented in Sprint 2 — Sprint 2 published `Starship at-cost rate ($mm/launch)` at Launch Capacity R40 instead. Per single-source-of-truth principle (Principle 7 — lock names day one; no renames mid-build) AND published-reality wins, the Architecture doc gets amended to match: replace all references to `At-cost launch services rate ($mm/launch)` with `Starship at-cost rate ($mm/launch)` in §6.6, §7.1, §17, and §18. F9 launches use the parallel label `F9 at-cost rate ($mm/launch)` (Launch Capacity R71). This amendment lands as part of Sprint 5 execution (plugin updates Architecture doc + Architecture amendment log entry); Sprint 6 onwards inherits the corrected naming. Architecture §6.6 amendment-log entry to be added: "2026-05-20 (Sprint 5 — label drift reconciliation) — Replaced aspirational `At-cost launch services rate ($mm/launch)` with actually-published `Starship at-cost rate ($mm/launch)` (Launch Capacity R40 / Sprint 2 + Patch E §6.13). The aspirational name was never implemented; Sprint 5 reads the actually-published string. F9 parallel label `F9 at-cost rate ($mm/launch)` (Launch Capacity R71)."
