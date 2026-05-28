# Sprint 4 — Starlink Module + Starlink Capacity Tab

**Source workbook**: `SpaceX Model V2.5.xlsx` (Sprint 3 output, verified PASS — Customer Launch module body live; Launch Capacity Patches D/A/B/E §6.13 absorbed; canonical labels `F9 customer launches per year`, `Starship customer launches per year`, `Customer Launch internal transfer revenue`, `Starship at-cost rate ($mm/launch)`, `F9 at-cost rate ($mm/launch)`, `F9 Annual Capacity (kg-to-LEO)`, `Total Annual Capacity (kg-to-LEO)` published; per-launch IRR engine flagged for Sprint 3.5 amendment but unaffecting Sprint 4 reads).
**Target workbook**: `SpaceX Model V2.6.xlsx` (Vlad has Save-As'd from V2.5 → V2.6 before this kickoff per standing process rule 2).
**Day budget**: 1.5 days
**Date drafted**: 2026-05-20

---

## §0 — Constitutional references

- **`01_Lessons_Learned.md`**: Principles 1 (no postponed methodology — V2/V3 ratchet + per-vehicle IRR + bandwidth-driven revenue locked this sprint), 2 (per-sat marginal IRR — Sprint 4 builds four engines: V2 BB, V2 DTC, V3 BB, V3 DTC), 6 (no tab without a locked function — Starlink is the third P&L module, Starlink Capacity is supply-side aggregator), 7 (canonical labels day one — six labels Sprint 3 IFERROR-0 reads consume + Starlink Capacity rate labels Sprint 5 will consume), 8 (module COGS = direct production only — no R&D/SG&A/overhead/taxes on Starlink tab; Spectrum amort flows to BB COGS only per Sprint 4 lock 2026-05-20), 9 (internal bandwidth transfer to ODC gross at module IRR; Sprint 9 Group P&L R106 eliminates), 11 (zero OFFSET; INDEX/MATCH on labels), 12 (anchor-and-offset for deterministic ramps), 13 (year-offset helper row 5 standard), 14 (INDEX/MATCH on labels), 17 (no superseded rows from prior sprints to delete), 18 (MC ranges at input creation — six new Assumptions rows added this sprint each with full MC fields), 22 (within-year cycles — Starlink revenue depends on Starlink Capacity tab's Available Gbps, which depends on ODC bandwidth claim, which Sprint 5 wires — Sprint 4 sees IFERROR-0 wrappers and converges in one pass).
- **`02_Architecture_and_Methodology.md`**: §1 (tab #5 = Starlink, tab #6 = Starlink Capacity, tab #14 = Demand Curves carried from V9), §3 (vending-machine framing — Revenue → COGS → Module EBITDA = Gross Profit → CapEx → Module FCF; no R&D/SG&A/overhead/taxes), §4.1 (Allocator IN block already in place from Sprint 1 at rows 7-10 reading 0 placeholders against Allocator R84 `Starlink cash allocation` + R134 `Starlink kg allocation`), §4.2 (Allocator OUT contract — 11 canonical rows at 200-210 — Sprint 4 overwrites Sprint 1 literal-0 placeholders with live formulas), §5.1 (per-sat IRR formula: CF stream length N+1 = 6 for N=5 yrs sat-module default; Sprot/Forward/Blended IRR with w=0.7), §5.2 (Starlink net marginal revenue per sat per year = per-sat Gbps × $/Gbps × util − per-sat ground ops % − per-sat spectrum amort BB-only − per-sat insurance − per-sat other COGS), §5.4 (strict IRR > 0 cutoff — applies to BB pool internal sigmoid blend between V2 BB and V3 BB; same for DTC pool), §7.2 (Starlink ↔ ODC bandwidth — 4-step Rule 21 pattern: Starlink books internal bandwidth revenue, ODC books bandwidth services cost in COGS, Sprint 9 Group P&L R106 eliminates, conservation row verifies; ODC reads with IFERROR-0 wrappers in Sprint 4), §8 (Starlink architecture in full — §8.1 V2/V3 pools with BB market share R135=0.85 + DTC R136=0.15, §8.2 V2/V3 ratchet single irreversible flag — AMENDED by Vlad lock 2026-05-20: V2 DTC permanently capped at 650 from end-2025 so V2 DTC launches = 0 from 2026 onwards regardless of V3 status; V2 BB ratchet fires when V3 BB starts launching; new MC Assumptions inputs `V3 BB first launch year` Base=2026 + `V3 DTC first launch year` Base=2028, §8.3 V2 historical fleet linear retirement R-useful-life=5 yrs from Sprint 0 R80=5, §8.4 bandwidth-driven revenue + subs derived as Revenue/ARPU using Demand Curves tab year-row + Sprint 0 R128 BB ARPU + R129 DTC ARPU year-rows, §8.5 Starlink Capacity tab structure), §17 (2025 calibration — Starlink+DTC $7,852M, of which DTC $157M, Starshield $2,520M, Constellation D&A $707M).
- **`03_Sprint_Roadmap_and_Verification.md`**: §3 Sprint 4 scope + locked-this-sprint decisions (Spectrum amort flows to Starlink BB COGS only; Capital deployed = Module CapEx for V2/V3 pools in equilibrium except CapEx Lag year R82=1 yr — amended by Vlad clarification 2026-05-20 that R82 applies to FACILITIES CapEx not sat CapEx, see §3.3.8), §5 universal verification (no errors, conservation OK, edge-year reads, round-trip stability, stale-ref scan, sanity halts, Claude Log), §6.3 Sprint 4 calibration targets (Starlink+DTC revenue $7,852M ±5%; of which DTC $157M ±15%; Starshield $2,520M ±5%; Active V2 BB 5,246 exact; Active V2 DTC 650 exact; V2 BB launched 2025 = 2,987 exact; V2 DTC launched 2025 = 182 exact; V3 launches 2025 = 0 exact; Constellation D&A $707M ±10%; Module EBITDA margin 55-75%; BB ARPU $100/mo; DTC ARPU $16/mo; total subs 5.5-7.5M), §8 sprint-spec template (followed below).
- **`04_Assumptions_Tab_Spec.md`**: §1 (column convention — A label, B Base Case, C notes, D-AC year-row, AG-AJ MC fields), §2 §5 Starlink existing inputs (Sprint 0 R74-R142 — every input referenced in §3.3 below by canonical label, not row number).
- **`Model Execution Rules.md`**: Mandatory Rule Compliance Preamble at §1; Rules 1 / 3 / 4 / 5 / 10 / 11 / 12 / 13 / 14 / 16 / 17 / 19 / 20 / 21 / 22 / 23 load-bearing.
- **`2025 Anchors from Q4_25.md`**: Starlink+DTC revenue 2025 = $7,852M (Earth R115), Starshield revenue 2025 = $2,520M (Earth R121), Active V2 BB end-2025 = 5,246 (R91 hard anchor), Active V2 DTC end-2025 = 650 (R92 hard anchor), V2 BB sats launched 2025 = 2,987 (R96 anchor), V2 DTC sats launched 2025 = 182 (R97 anchor), Constellation D&A 2025 = $707M (R195), DTC component of Starlink = $156.91M (≈2% of $7,852M).
- **`Sprint_0_Spec.md`** §3.6 (Starlink §5 inputs R74-R142 + Demand Curves data + ARPU year-rows R128/R129 — every label and Base Case value inlined in §3.3 below).
- **`Sprint_1_Spec.md`** §3.3 (Starlink shell — Allocator IN at rows 7-10 + Allocator OUT at rows 200-210 with literal 0 placeholders; Sprint 4 fills rows 11-199 in between and overwrites OUT placeholders with live formulas; Starlink Capacity tab — title row only at row 6 from Sprint 1 §3.4, Sprint 4 builds full body).
- **`Sprint_2_Spec.md`** §3.1 (Launch Capacity canonical labels — Sprint 4 reads R64 `F9 launches per year` via Patch B demand-driven formula post-Sprint 4 publication; reads R40 `Starship at-cost rate ($mm/launch)` not directly this sprint — internal Starship launches consume capacity but launch services cost flows in via Customer Launch Sprint 3 publishing).
- **`Sprint_3_Spec.md`** §3.6 + Patch B §3.4.2 (Customer Launch tab + Launch Capacity R64 IFERROR-0 reads — Sprint 4 publishes the six canonical Starlink labels these reads consume).
- **No Sprint 3.5 patch present in project folder as of 2026-05-20 drafting.** Sprint 4 reads only `F9 customer launches per year` (Customer Launch R25 per Sprint 3 §3.6 numbering), `Starship customer launches per year` (Customer Launch R24), and `Customer Launch internal transfer revenue` (Customer Launch R70) — none of which are affected by Sprint 3.5's per-launch IRR reformulation (R131, R141 in Sprint 3 row map). Sprint 4 can fire in parallel with Sprint 3.5.

---

## §1 — Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md` and the four constitutional docs. Each box ticked or justified N/A:

- [x] **Rule 1** (one concept per write) — §3 structured as discrete blocks. Every row's column-A label is written in a separate `set_cell` call from its D-column anchor formula, and the D-anchor formula is a separate call from the E:AC copyToRange. Six new Assumptions rows in §3.2 each execute as 6 discrete writes (label, Base, MC Min, MC Max, MC Distribution, Notes). Number-format passes (currency `#,##0` for $mm/Gbps/sats; `0.0%` for IRR/margin) execute as separate writes from formula writes.
- [x] **Rule 3 / 23** (formula pattern) — every deterministic ramp on Starlink tab + Starlink Capacity tab (Wright's Law per-kg sat cost; Bandwidth per V3 BB sat with WL learning; Starshield Reserved % decay; Starshield Rev per Gbps decay; Starship customer margin; Starlink BB Gbps year-row from Demand Curves; $/Gbps year-row from Demand Curves; per-sat IRR per-year CF stream slots) uses anchor-and-offset on `E$5` and a locked anchor cell. Year-chained Rule 23 exceptions explicitly flagged inline with one-line justification: (a) V2 BB Active Fleet year-row (running sum: BoY + launches − retirements − ratchet shutoff), (b) V2 DTC Active Fleet year-row (same), (c) V3 BB Active Fleet year-row (same), (d) V3 DTC Active Fleet year-row (same), (e) V2/V3 ratchet flag year-row (`E{ratchet}=IF(OR(D{ratchet}=1, E{V3 BB launched}>0, E{V3 DTC launched}>0), 1, 0)`), (f) Cumulative sat launches running sum for Wright's Law denominator, (g) V2 BB historical retirement linear-over-5-yrs counter (uses `IF(E$5 < useful_life, baseline/useful_life, 0)` — actually anchor-and-offset compliant, NOT a year-chained exception). Per-sat IRR engine uses SEQUENCE() to construct CF array — dynamic-array, not year-chained.
- [x] **Rule 4** (verification gate) — §4.3 enumerates explicit read-back cells at D (2025), I (2030), S (2040), AC (2050) with expected values for every load-bearing row: Starlink+DTC revenue, of which DTC; Starshield revenue; Active V2 BB / V2 DTC / V3 BB / V3 DTC; V2 BB / V2 DTC / V3 BB / V3 DTC launches per year; Module EBITDA; Module CapEx; Module FCF; per-vehicle Spot/Forward/Blended IRR (×4 vehicles); BB pool at-cost rate; DTC pool at-cost rate; BB Gbps available for external; DTC Gbps available for external; implied BB ARPU; implied total subs; ratchet flag; F9 V2 BB launches (internal); F9 V2 DTC launches (internal); Starship V3 BB launches (internal); Starship V3 DTC launches (internal); V3 BB Starship kg demand; V3 DTC Starship kg demand.
- [x] **Rule 6** (inline formulas) — every cell write in §3 specified with the full Excel formula. No "see Architecture §8" hand-waves — bandwidth-driven revenue, Starshield mechanic, V2/V3 ratchet latch, V2 historical retirement, per-sat IRR all inlined verbatim. INDEX/MATCH calls on Assumptions / Demand Curves / Customer Launch / Launch Capacity / Starlink Capacity (cross-tab) + intra-tab written out with exact canonical labels.
- [x] **Rule 10** (no row insertions) — Starlink tab Sprint 4 writes appended to rows 11–199 (between Sprint 1's IN block at 7-10 and OUT block at 200-210). Sprint 1 OUT block placeholders OVERWRITTEN in place (same row numbers) per Architecture §4.2 — no row insertions on Starlink tab. Starlink Capacity tab Sprint 4 writes appended below Sprint 1's title row at row 6 — no row insertions (tab is otherwise empty). Assumptions tab amendments (six new rows in §3.2) appended below Sprint 3's last-used row in Assumptions §5 Starlink section — append-only per Rule 10. No `insert_row` operations anywhere.
- [x] **Rule 11** (touch points) — every new Starlink + Starlink Capacity line item enumerates its (i) intra-tab SUM range (Revenue total = sum of BB rev + DTC rev + Starshield rev + Internal bandwidth rev + Terminal hardware rev; COGS total = sum of Constellation D&A + Ground ops + Spectrum amort BB-only + Terminal COGS + Insurance + Other COGS), (ii) Allocator OUT pull (11 canonical rows at 200-210), (iii) Sprint 9 Group P&L pulls (Total Revenue, Module EBITDA, Module CapEx, Module FCF via INDEX/MATCH), (iv) Sprint 9 conservation row R106 (Bandwidth elimination — reads `Starlink internal bandwidth revenue ($mm)` and ODC's bandwidth services cost), (v) Patch B Launch Capacity R64 (reads `F9 V2 BB launches (internal)` + `F9 V2 DTC launches (internal)`), (vi) Customer Launch R22/R68/R69 reads (the six canonical Starlink labels from kickoff prompt step 1), (vii) Sprint 5 ODC reads of Starlink Capacity `BB pool at-cost rate ($/Gbps/yr)` + `DTC pool at-cost rate ($/Gbps/yr)`, (viii) Starlink Capacity reads `ODC BB Gbps demand` + `ODC DTC Gbps demand` from ODC tab with IFERROR-0 wrappers until Sprint 5 fires. Touch points enumerated per row in §3.3 / §3.4 / §3.5 / §3.6.
- [x] **Rule 12** (label-based cross-tab refs) — every cross-tab pull on Starlink tab + Starlink Capacity tab uses `INDEX(Tab!D:D, MATCH("<exact canonical label>", Tab!$A:$A, 0))` or year-row equivalent `INDEX(Tab!$D:$AC, MATCH("<label>", Tab!$A:$A, 0), E$5+1)`. Zero hardcoded row-number references. Cross-tab labels Sprint 4 reads: Assumptions §5 by label for all 30+ inputs; Demand Curves tab `Total BB Gbps demand (Gbps/yr)` + `Total BB price ($/Gbps/yr)` + `Total DTC Gbps demand (Gbps/yr)` + `Total DTC price ($/Gbps/yr)` (spec author confirms Demand Curves V9 structure exposes these four labels — if not, see §3.0 pre-flight halt #7); Customer Launch tab labels NOT read directly by Sprint 4 (Customer Launch reads Starlink's labels, one-way); ODC tab `ODC BB Gbps demand` + `ODC DTC Gbps demand` (IFERROR-0 until Sprint 5); CapEx tab `Annual Spectrum amortization ($mm/yr)` (IFERROR-0 until Sprint 8).
- [x] **Rule 13** (vending-machine test) — Starlink P&L stops at Module EBITDA = Gross Profit. No R&D / SG&A / customer service / corporate overhead / taxes anywhere on Starlink tab. R&D lives on OpEx tab (Starlink R&D 8% start → 3% end CAGR -10%/yr per Architecture §12.1, Sprint 8 owns the formula). The exception is Internal Transfer Revenue (Starlink → ODC bandwidth, intercompany flow per Architecture §7.2, NOT OpEx).
- [x] **Rule 14** (no hardcoded constants) — every behavior input resolves to an Assumptions row by label. Specific declared exceptions: (a) Mathematical constants (1, 0 in IFERROR fallbacks; 12 for monthly→annual ARPU conversion which is a unit-conversion not a behaviour input; 1e6 for $→$mm conversions); (b) IRR engine SEQUENCE() arguments are dynamic-array constructs, not hardcoded values; (c) 2025 V2 BB launches anchor = INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Sats Launched 2025", Assumptions!$A:$A, 0)) = 2,987 — resolves to Assumptions; (d) 2025 V2 DTC launches anchor = 182 (resolves to Assumptions R97 by label); (e) End-2024 V2 BB active baseline 5,246 = R91 by label; (f) End-2024 V2 DTC active baseline 650 = R92 by label. All six new Assumptions rows added in §3.2 have MC ranges per Rule 14 + Principle 18.
- [x] **Rule 15** (sanity check halt thresholds) — §4.2 / §4.4 every check has quantitative halt threshold. Starlink+DTC revenue 2025 outside [$7,000M, $8,700M] halt. DTC component 2025 outside [$80M, $250M] halt. Starshield revenue 2025 outside [$2,200M, $2,900M] halt. Active V2 BB end-2025 ≠ 5,246 halt (exact). Active V2 DTC end-2025 ≠ 650 halt (exact). V2 BB launched 2025 ≠ 2,987 halt (exact). V2 DTC launched 2025 ≠ 182 halt (exact). V3 launches 2025 ≠ 0 halt (exact). Constellation D&A 2025 outside [$600M, $850M] halt. Module EBITDA margin outside [40%, 85%] halt (range). Implied total subs 2025 outside [3M, 10M] halt. Per-vehicle Blended IRR `#NUM!` or NaN = halt + push back. Starlink Capacity tab BB pool at-cost rate `#DIV/0!` (zero active Gbps) = expected pre-deployment; IFERROR-0 wrapper required.
- [x] **Rule 16** (edge-year verification) — D / I / S / AC reads explicit in §4.3. Edge years cover 2025 (pre-V3, pre-ratchet), 2030 (post-V3-trigger, V2 historical fleet retired, ratchet=1), 2040 (mid-V3-era, mature constellation), 2050 (terminal, ARPU compression bottomed-out).
- [x] **Rule 17** (delete superseded rows) — N/A this sprint. No prior-sprint rows are superseded by Sprint 4. Sprint 0 R64 Starship customer launch price year-row was deprecated by Sprint 3 (not Sprint 4); Sprint 4 doesn't touch it.
- [x] **Rule 19** (save-as) — target workbook named explicitly: `SpaceX Model V2.6.xlsx`. Per standing process rule 2 (locked 2026-05-20), Vlad has already Save-As'd V2.5 → V2.6 before this kickoff; plugin operates on the live open session and does NOT issue any save commands. §3.0 pre-flight verifies V2.6 is the active workbook name.
- [x] **Rule 20** (IFERROR guards on pre-revenue ratios) — Module EBITDA Margin % wrapped `=IFERROR(D{EBITDA}/D{Revenue}, 0)` per Sprint 1 convention. Per-vehicle IRRs wrapped `=IFERROR(IRR(...), -1)` per Architecture §5.1. Implied BB ARPU year-row + Implied DTC ARPU memo rows wrapped `=IFERROR(D{revenue}/D{subs}/12, 0)`. Starlink Capacity tab pool at-cost rates wrapped `=IFERROR(pool_cost_basis / total_active_Gbps, 0)` because total Gbps = 0 in pre-deployment edge year (irrelevant for Starlink 2025 since active Gbps > 0 from end-2024 baseline; relevant for ODC reads which are bandwidth-demand-side).
- [x] **Rule 21** (internal flows need elimination + conservation) — Starlink introduces the SECOND live internal transfer flow in the rebuild (Customer Launch's launch services flow was the first). Starlink ↔ ODC bandwidth services per Architecture §7.2. 4-step pattern: (1) Starlink books `Starlink internal bandwidth revenue ($mm)` row reading `(ODC BB Gbps demand × BB pool at-cost rate) + (ODC DTC Gbps demand × DTC pool at-cost rate)` with IFERROR-0 wrappers on ODC reads (resolves to 0 until Sprint 5 wires ODC bandwidth demand year-rows), (2) ODC will book `Bandwidth services cost ($mm)` in COGS in Sprint 5 with same formula, (3) Sprint 9 Group P&L R106 eliminates the flow (= Starlink internal bandwidth revenue − ODC bandwidth services cost = 0), (4) Sprint 9 conservation row R106 verifies match. For Sprint 4 verification, ODC reads = 0 via IFERROR-0 → Starlink internal bandwidth revenue = $0M throughout horizon. Lights up endogenously when Sprint 5 fires.
- [x] **Rule 22** (stale-ref scan) — §4.5 enumerates by-label scan: (i) Starlink's Assumptions reads (30+ Starlink §5 inputs, 4 Demand Curves inputs, plus six new Sprint 4 amendments) confirmed against Assumptions row labels; (ii) Starlink's intra-tab references all by-label; (iii) Starlink Capacity tab's reads of Starlink tab labels confirmed; (iv) Sprint 1 OUT block placeholders OVERWRITTEN with live formulas — Sprint 4 verifies the 11 canonical OUT labels match Architecture §4.2 verbatim; (v) future Sprint 5 ODC will reference Starlink Capacity by `BB pool at-cost rate ($/Gbps/yr)` + `DTC pool at-cost rate ($/Gbps/yr)`, Sprint 4 publishes those labels exactly; (vi) Patch B Launch Capacity R64 + Customer Launch R22/R68/R69 IFERROR-0 reads — Sprint 4 publishes the six canonical Starlink labels EXACTLY: `F9 V2 BB launches (internal)`, `F9 V2 DTC launches (internal)`, `Starship V3 BB launches (internal)`, `Starship V3 DTC launches (internal)`, `V3 BB Starship kg demand`, `V3 DTC Starship kg demand`. Plugin verifies post-write that all six MATCH calls on the Starlink tab resolve.

**Architecture & Methodology compliance:**

- [x] Module P&L follows vending-machine framing (Architecture §3) — Starlink builds Revenue → COGS → Gross Profit = Module EBITDA → Module CapEx → Module FCF per §3.3. No R&D / SG&A / overhead / taxes.
- [x] Per-vehicle marginal IRR engines (Architecture §5) — §3.5 builds four per-sat IRR engines: V2 BB, V2 DTC, V3 BB, V3 DTC. N = 5 yrs sat-module default per Sprint 0 R19 / R80. Each reads external bandwidth economics only (Principle 9 + §7.2) — internal bandwidth at-cost transfer to ODC doesn't contribute to per-vehicle IRR signal.
- [x] Allocator OUT contract uses canonical 11 labels (Architecture §4.2) — §3.6 overwrites Sprint 1 placeholders. 11 rows populate with live formulas. Per-vehicle Blended IRRs exposed as Memo rows below the canonical block (rows 211-218: V2 BB Spot/Forward/Blended; V2 DTC Spot/Forward/Blended; V3 BB Spot/Forward/Blended; V3 DTC Spot/Forward/Blended — 12 memo rows total, italic per Rule 17 memo convention). Allocator OUT row 209 (Blended IRR) on Starlink = Gbps-weighted blend of the four per-vehicle Blended IRRs (BB share 0.85 × BB-pool-IRR + DTC share 0.15 × DTC-pool-IRR; BB-pool-IRR = active-Gbps-weighted blend of V2 BB Blended IRR and V3 BB Blended IRR; same for DTC pool).
- [x] Year-offset helper row at row 5 + year header at row 4 on Starlink + Starlink Capacity tabs — already in place from Sprint 0 / 1. §3.0 pre-flight confirms D4 = 2025, D5 = 0, AC4 = 2050, AC5 = 25 on both tabs.
- [x] ZERO `OFFSET()` formulas; INDEX:INDEX patterns used (Principle 11) — confirmed.

If any box is unchecked, the spec author justifies or amends before execution starts. Plugin refuses to write a single cell against an unticked-or-unjustified preamble.

---

## §1.5 — Pre-execution setup (Vlad confirms before plugin starts writing)

Per standing process rule 3 (locked 2026-05-20), the kickoff prompt includes this confirmation block. The plugin's §3.0 pre-flight verifies it before any cell write.

**Vlad attests:**

1. **Target workbook is open** with name `SpaceX Model V2.6.xlsx` (Save-As completed from V2.5 → V2.6 before this kickoff).
2. **Vlad will handle all saves** — the plugin operates on the live open workbook session and will NOT issue any save / save-as / write-file commands. Verification reads cells from the session directly.
3. **Sprint 3.5 patch state** — Vlad confirms whether Sprint 3.5 has landed on V2.5 before V2.6 was created OR whether Sprint 3.5 is still in flight in a parallel chat. Sprint 4 reads only Customer Launch labels `F9 customer launches per year`, `Starship customer launches per year`, `Customer Launch internal transfer revenue` — none affected by Sprint 3.5's per-launch IRR amendment. Either state is acceptable.
4. **No other tabs are open in this workbook** that could conflict with Starlink + Starlink Capacity + Assumptions writes (Assumptions tab needs WRITE access this sprint for six new amendments in §3.2).

If any of the above is not true, plugin halts at pre-flight per Rule 9 and pushes back to Vlad.

---

## §2 — Framing

**Why this sprint:** Sprint 4 builds the Starlink module body end-to-end (rows 11–199 between Sprint 1's IN block at rows 7-10 and OUT block at rows 200-210) AND the full Starlink Capacity tab (supply-side aggregator that allocates BB+DTC bandwidth between external Starlink revenue and internal ODC consumption). This is the THIRD module tab and the SECOND non-P&L supply tab. Sprint 4 publishes six canonical labels Sprint 3 already wired IFERROR-0 reads against (Patch B Launch Capacity R64 + Customer Launch R22/R68/R69) — those reads activate the moment Sprint 4's writes land. Sprint 4 also publishes two canonical at-cost rate labels Sprint 5 ODC will consume.

**The seven Vlad locks for this sprint (2026-05-20):**

1. **Revenue is bandwidth-driven; subs are derived as Revenue / ARPU** (Architecture §8.4 confirmed). Starlink tab reads `Total BB Gbps demand (Gbps/yr)` year-row + `Total BB price ($/Gbps/yr)` year-row from Demand Curves (V9 inheritance — see §3.0 pre-flight #7). BB Revenue = Available BB Gbps (from Starlink Capacity tab) × $/Gbps. Subs derived = BB Revenue / (BB ARPU × 12). Same structure for DTC. Calibrates 2025 to $7,852M ±5% via Demand Curves anchor.

2. **Starshield revenue uses the Q4'25 mechanic anchored** (Architecture §8 verbatim). Starshield reserved Gbps year-row = Total constellation BB Gbps × Reserved% (Sprint 0 R94=0.0257 start, R95=0.0001 floor, R96=0.25 decay/yr — anchor-and-offset). Starshield Rev/Gbps year-row = Sprint 0 R97=$164,699 base with R98=0.05 decay/yr — anchor-and-offset. Starshield revenue = Starshield reserved Gbps × Starshield Rev/Gbps. Anchors to $2,520M 2025.

3. **V2/V3 ratchet — year-chained single irreversible flag with Vlad lock 2026-05-20 amendments:**
   - V2 DTC launches: 2025 = 182 (Sprint 0 R111 hardcoded historical via INDEX/MATCH); **2026 onwards = 0 always** (Vlad lock: SpaceX is permanently capping V2 DTC at the 650 active sats from end-2025; no more V2 DTC launches ever). This decouples V2 DTC from the V3 ratchet — V2 DTC is shut down regardless of V3 status.
   - V2 BB launches: 2025 = 2,987 (Sprint 0 R110 hardcoded historical via INDEX/MATCH); 2026 onwards = subject to BB pool IRR-sigmoid allocation AND eligibility = `IF(AND(V2 BB Blended IRR > 0, ratchet_flag = 0), 1, 0)` where ratchet fires when V3 BB starts launching.
   - **V3 BB first launch year** — NEW MC Assumptions input. Base Case = **2026** (per Vlad "latter half 2026 when Starship can"), MC range [2026, 2027] discrete. 2025 V3 BB launches always = 0.
   - **V3 DTC first launch year** — NEW MC Assumptions input. Base Case = **2028** (per Vlad "2027 or 2028"), MC range [2027, 2028] discrete. 2025 + 2026 V3 DTC launches always = 0.
   - **Ratchet flag year-row** — single year-chained latch (Rule 23 exception, intentional): D{ratchet} = `=IF(OR(D{V3 BB launched} > 0, D{V3 DTC launched} > 0), 1, 0)`; E{ratchet} = `=IF(OR(D{ratchet}=1, E{V3 BB launched}>0, E{V3 DTC launched}>0), 1, 0)`; copy E across F:AC.
   - V3 BB eligibility = `IF(AND(V3 BB Blended IRR > 0, year >= V3 BB first launch year), 1, 0)`.
   - V3 DTC eligibility = `IF(AND(V3 DTC Blended IRR > 0, year >= V3 DTC first launch year), 1, 0)`.

4. **V2 historical fleet retirement: linear over R-useful-life=5 yrs** (Architecture §8.3). V2 BB historical retirement year-row = `IF(E$5 < useful_life, V2_BB_baseline / useful_life, 0)` where useful_life = Sprint 0 R80 = 5 yrs. V2 BB baseline = Sprint 0 R115 = 5,246 → retires 1,049.2/yr in 2025-2029, hits 0 by 2030. V2 DTC same: baseline R116=650 → retires 130/yr in 2025-2029, hits 0 by 2030. Anchor-and-offset compliant (NOT a Rule 23 exception — the year offset E$5 substitutes for year-chained cumulative).

5. **Four per-vehicle marginal IRR engines** (V2 BB, V2 DTC, V3 BB, V3 DTC) with N = 5 yrs sat-module default per Sprint 0 R19 / R80. Each engine reads external bandwidth economics only (per-sat Gbps × $/Gbps × util year-row − per-sat ground ops % − per-sat spectrum amort BB-only − per-sat insurance − per-sat other COGS) and produces Spot IRR (current year), Forward IRR (Y+2), Blended IRR = `(1-w)·Spot + w·Forward` with w=0.7 from Sprint 0 R17. CF stream length N+1=6 per engine. Wrapped IFERROR(IRR(...), -1) per Architecture §5.1.

6. **Starlink Capacity tab canonical labels** — Sprint 4 publishes:
   - `Total active BB Gbps` (year-row; diagnostic)
   - `Total active DTC Gbps` (year-row; diagnostic)
   - `BB pool cost basis ($mm/yr)` (year-row; = Gbps-share-weighted Constellation D&A + Ground ops + Spectrum amort BB-only, computed on the tab; diagnostic)
   - `DTC pool cost basis ($mm/yr)` (year-row; = same minus Spectrum amort, computed on the tab; diagnostic)
   - `BB pool at-cost rate ($/Gbps/yr)` (year-row; = BB pool cost basis × 1e6 / Total active BB Gbps; consumed by Sprint 5 ODC + Starlink internal bandwidth revenue formula)
   - `DTC pool at-cost rate ($/Gbps/yr)` (year-row; = DTC pool cost basis × 1e6 / Total active DTC Gbps; consumed by Sprint 5 ODC)
   - `ODC BB Gbps demand` (year-row; reads ODC tab by INDEX/MATCH with IFERROR-0 wrapper — resolves to 0 until Sprint 5 publishes its label of same name)
   - `ODC DTC Gbps demand` (year-row; same)
   - `BB Gbps available for external Starlink revenue` (year-row; = MAX(0, Total active BB Gbps − ODC BB Gbps demand))
   - `DTC Gbps available for external Starlink revenue` (year-row; = MAX(0, Total active DTC Gbps − ODC DTC Gbps demand))

7. **CapEx Lag R82=1 yr applies to FACILITIES CapEx, not sat CapEx** (Vlad clarification 2026-05-20). Practical implementation:
   - Sat CapEx in year T = `Σ_vehicles (sat_unit_cost_T × sats_launched_T)` — no lag, satellites launched same year as built.
   - Facility CapEx in year T = `facility_per_sat_T × sats_launched_{T+1}` — facilities for next year's deployment booked this year (1 yr ahead). Uses `INDEX($D:$AC, ..., E$5+2)` to shift one column right.
   - Module CapEx (Allocator OUT row 205) = Sat CapEx + Facility CapEx.
   - Capital deployed (Allocator OUT row 206) = `Σ_vehicles ((sat_unit_cost_T + facility_per_sat_T) × sats_launched_T)`.
   - In equilibrium when launches flat year-over-year: Module CapEx ≈ Capital deployed.
   - During ramp (e.g., 2027 V3 BB launches start, 2028 V3 BB scales): Module CapEx 2027 > Capital deployed 2027 by `facility_per_sat × (launches_2028 − launches_2027)`.
   - 2050 facility CapEx reads `launches_2051` which doesn't exist → IFERROR(..., 0) wrapper handles edge.

**What it produces (canonical output rows — single source of truth; labels exact, no renames):**

| Tab | Canonical label | Consumed by |
|---|---|---|
| Starlink | `F9 V2 BB launches (internal)` (year-row) | **Patch B Launch Capacity R64** (line 348 Sprint 3 spec) + Customer Launch R68 (line 757) |
| Starlink | `F9 V2 DTC launches (internal)` (year-row) | **Patch B Launch Capacity R64** (line 349) + Customer Launch R68 (line 758) |
| Starlink | `Starship V3 BB launches (internal)` (year-row) | Customer Launch R69 (line 778) |
| Starlink | `Starship V3 DTC launches (internal)` (year-row) | Customer Launch R69 (line 779) |
| Starlink | `V3 BB Starship kg demand` (year-row) | Customer Launch R22 (line 583) |
| Starlink | `V3 DTC Starship kg demand` (year-row) | Customer Launch R22 (line 584) |
| Starlink | `Total Revenue ($mm)` (Allocator OUT R201) | Sprint 9 Group P&L module revenue aggregator |
| Starlink | `Module EBITDA ($mm)` (R202) | Sprint 9 + Sprint 11 |
| Starlink | `Module EBITDA Margin %` (R203) | Sprint 9 diagnostic |
| Starlink | `Module FCF ($mm)` (R204) | Sprint 9 + Sprint 11 |
| Starlink | `Module CapEx ($mm)` (R205) | Sprint 8 CapEx tab aggregation + Sprint 9 |
| Starlink | `Capital deployed ($mm)` (R206) | Diagnostic only |
| Starlink | `Spot IRR` (R207) | Sprint 10 Allocator brain |
| Starlink | `Forward IRR (Y+2)` (R208) | Sprint 10 |
| Starlink | `Blended IRR` (R209) | Sprint 10 |
| Starlink | `Capacity Demand (kg-to-LEO)` (R210) | Sprint 10 Allocator kg queue |
| Starlink | `Starlink internal bandwidth revenue ($mm)` | Sprint 9 Group P&L R106 elimination |
| Starlink Capacity | `BB pool at-cost rate ($/Gbps/yr)` | Sprint 5 ODC bandwidth services cost line |
| Starlink Capacity | `DTC pool at-cost rate ($/Gbps/yr)` | Sprint 5 ODC bandwidth services cost line |
| Starlink Capacity | `BB Gbps available for external Starlink revenue` | Starlink tab BB revenue formula |
| Starlink Capacity | `DTC Gbps available for external Starlink revenue` | Starlink tab DTC revenue formula |
| Starlink Capacity | `ODC BB Gbps demand` (memo) | Diagnostic for Sprint 5 wiring |
| Starlink Capacity | `ODC DTC Gbps demand` (memo) | Diagnostic for Sprint 5 wiring |

**What it deliberately does NOT do:**

- Does NOT add R&D / SG&A / corporate overhead / taxes to Starlink (vending-machine framing — Principle 8 + Rule 13).
- Does NOT compute vehicle build cost claim — that's Sprint 10 Allocator (Architecture §6.6).
- Does NOT write to Sprint 5 ODC / Sprint 6 AI Stack — internal bandwidth revenue resolves to $0 via IFERROR-0 wrappers at Sprint 4 exit; lights up endogenously in Sprint 5.
- Does NOT write to Group P&L / OpEx / CapEx / Valuation tabs — those sprints read Starlink by canonical labels.
- Does NOT compute Spectrum amortization — reads via INDEX/MATCH from CapEx tab `Annual Spectrum amortization ($mm/yr)` with IFERROR-0 wrapper (resolves to $0 until Sprint 8 wires it).
- Does NOT touch Customer Launch / Launch Capacity / Allocator tabs.

**Dependencies:**

- Sprint 0 (Assumptions §5 Starlink inputs R74-R142; six new amendments per §3.2).
- Sprint 1 (Starlink shell rows 7-10 + 200-210; Starlink Capacity title row 6).
- Sprint 2 (Launch Capacity tab end-to-end, V2.4 PASS — Sprint 4 doesn't read directly but Patch B reads Starlink labels post-Sprint-4 publication).
- Sprint 3 (Customer Launch + Patch B IFERROR-0 reads — Sprint 4 publishes the six canonical labels these reads consume).
- V9 inheritance: Demand Curves tab carried unchanged (§3.0 pre-flight #7 confirms structure).

---

## §3 — Scope

### §3.0 Pre-flight (plugin verifies BEFORE any cell write)

Plugin halts on any failure and pushes back to Vlad.

1. **Workbook name** = `SpaceX Model V2.6.xlsx` (active workbook in session). Halt if name is `V2.5`, `V2.5.xlsx`, or anything else — Vlad missed the Save-As.
2. **Starlink tab exists** with sheet position #5 (per Architecture §1: Assumptions #1, Allocator #2, Launch Capacity #3, Customer Launch #4, Starlink #5). Halt if tab missing or wrong position.
3. **Starlink Capacity tab exists** with sheet position #6 (per Architecture §1). Halt if tab missing or wrong position.
4. **Starlink row 4 + row 5** read year header + year offset standards: D4 = 2025, I4 = 2030, S4 = 2040, AC4 = 2050; D5 = 0, I5 = 5, S5 = 15, AC5 = 25. Halt if any mismatch.
5. **Starlink Capacity row 4 + row 5** same. Halt if any mismatch.
6. **Starlink Allocator IN block at rows 7-10** confirmed via label match: A7 contains "INPUTS FROM CENTRAL ALLOCATOR", A8 contains "Capital Allocation", A9 contains "Starship Capacity Allocation", A10 contains "Total Capital Available". **Starlink Allocator OUT block at rows 200-210** confirmed: A200 contains "CENTRAL ALLOCATOR OUTPUTS", A201..A210 contain the 11 canonical OUT labels per Architecture §4.2. Halt if any label mismatch.
7. **Starlink rows 11-199** confirmed empty in V2.5. Plugin reads A11:A199 — all blank. Halt if anything non-blank (Sprint 1 deviation needing investigation).
8. **Demand Curves tab V9 structure check**. Plugin runs four MATCH calls on Demand Curves tab column A:
   - `MATCH("Total BB Gbps demand (Gbps/yr)", 'Demand Curves'!$A:$A, 0)` — must resolve (i.e., not `#N/A`).
   - `MATCH("Total BB price ($/Gbps/yr)", 'Demand Curves'!$A:$A, 0)` — must resolve.
   - `MATCH("Total DTC Gbps demand (Gbps/yr)", 'Demand Curves'!$A:$A, 0)` — must resolve.
   - `MATCH("Total DTC price ($/Gbps/yr)", 'Demand Curves'!$A:$A, 0)` — must resolve.
   If ANY of the four labels does NOT exist in Demand Curves column A, plugin HALTS per Rule 9 and pushes back to Vlad. V9 Demand Curves may use different label strings (e.g., `BB demand` vs `Total BB Gbps demand (Gbps/yr)`). Plugin reports the four MATCH results to Vlad with the actual column-A labels found near the expected concepts; Vlad either (a) renames Demand Curves labels to the canonical strings, (b) provides the actual label strings for Sprint 4 to use, or (c) authorizes Sprint 4 to publish bridge rows on Starlink tab that read the V9 label and re-publish under the canonical name. **Sprint 4 does not proceed without all four resolutions.**
9. **Assumptions §5 Starlink section** confirmed via `MATCH("§5 STARLINK", Assumptions!$A:$A, 0)`. Halt if section header missing.
10. **Starlink Capacity tab body** confirmed empty in V2.5 (only Sprint 1 title row at A6 present, rows 7-199 blank). Halt if any non-Sprint-1 content found.
11. **Sprint 3 canonical labels published on Customer Launch tab** confirmed via MATCH calls (Sprint 4 doesn't read them, but verifies Sprint 3 completed successfully):
    - `MATCH("F9 customer launches per year", 'Customer Launch'!$A:$A, 0)` must resolve.
    - `MATCH("Starship customer launches per year", 'Customer Launch'!$A:$A, 0)` must resolve.
    - `MATCH("Customer Launch internal transfer revenue ($mm)", 'Customer Launch'!$A:$A, 0)` must resolve.
    Halt if any missing — indicates Sprint 3 didn't land cleanly.
12. **Sprint 2 canonical labels on Launch Capacity tab** confirmed:
    - `MATCH("Total Annual Capacity (kg-to-LEO)", 'Launch Capacity'!$A:$A, 0)` must resolve.
    - `MATCH("F9 launches per year", 'Launch Capacity'!$A:$A, 0)` must resolve.
    Halt if missing — indicates Sprint 2 didn't land cleanly.
13. **Sprint 0 anchor spot-checks** to protect against accidental damage:
    - `INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Active Sats — end-2025", Assumptions!$A:$A, 0))` = 5246.
    - `INDEX(Assumptions!$B:$B, MATCH("V2 Mini DTC Active Sats — end-2025", Assumptions!$A:$A, 0))` = 650.
    - `INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Sats Launched 2025", Assumptions!$A:$A, 0))` = 2987.
    - `INDEX(Assumptions!$B:$B, MATCH("V2 Mini DTC Sats Launched 2025", Assumptions!$A:$A, 0))` = 182.
    - `INDEX(Assumptions!$B:$B, MATCH("Starshield Reserved % — decay rate", Assumptions!$A:$A, 0))` = 0.25.
    - `INDEX(Assumptions!$B:$B, MATCH("Starshield Rev per Gbps — base year ($/Gbps)", Assumptions!$A:$A, 0))` = 164699.
    - `INDEX(Assumptions!$B:$B, MATCH("Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)", Assumptions!$A:$A, 0))` = 0.7.
    - `INDEX(Assumptions!$B:$B, MATCH("MFW-IRR — Starlink economic life N (years)", Assumptions!$A:$A, 0))` = 5.
    Halt if any anchor wrong — Sprint 0 deviation needing investigation.

All 13 pre-flight checks must pass. If any fail, halt and push back.

### §3.1 Patch absorption summary

**Sprint 4 absorbs no patches.** Sprint 3.5 (per-launch IRR reformulation for Customer Launch) is the only in-flight patch and does NOT affect any row Sprint 4 reads (Customer Launch R22/R24/R25/R68/R69/R70 unchanged by Sprint 3.5's R131/R141 amendment per kickoff prompt step 5). Sprint 4 can fire in parallel with Sprint 3.5.

### §3.2 Assumptions tab amendments (6 new rows)

Plugin appends six new rows below Sprint 0's last-used row in Assumptions §5 Starlink section (per Rule 10, append-only). Each amendment is a discrete row addition: (i) label write to column A, (ii) Base Case write to column B for VAL rows OR year-row writes to D:AC for YR rows, (iii) Notes write to column C, (iv) MC Min to column AG, (v) MC Max to column AH, (vi) MC Distribution to column AI, (vii) MC notes to column AJ. Six discrete writes per new row.

Plugin determines the exact append row via `MATCH("§6 ODC", Assumptions!$A:$A, 0) - 1` (= last row of §5 Starlink section) and appends downward from there. The plugin must shift §6 ODC section header downward by 6 rows — but that violates Rule 10. Alternative: append the six new rows at the bottom of the workbook's used range on Assumptions (post-§11 Valuation), with column-A labels prefixed `[Sprint 4 amendment to §5]` to maintain logical grouping. Plugin's call which append location to use; either is acceptable as long as labels are reachable by MATCH and no row insertions happen on Assumptions. **Recommended**: append at bottom of used range — keeps Sprint 0 row map fully intact.

#### §3.2.1 New Assumptions row — V3 BB first launch year

| Field | Value |
|---|---|
| Column A label | `V3 BB first launch year` |
| Type | VAL |
| Base Case (B) | `2026` |
| Notes (C) | `Vlad lock 2026-05-20: V3 BB launches start latter-half 2026 when Starship can lift them. Annual model treats 2026 as first full launch year. Drives V3 BB eligibility (=1 once year >= this) and the V2/V3 ratchet flag (V2 BB shuts down once V3 BB launches start).` |
| MC Min (AG) | `2026` |
| MC Max (AH) | `2027` |
| MC Distribution (AI) | `discrete` |
| MC Notes (AJ) | `Discrete sample between 2026 (Vlad base case — earliest physically plausible given Starship readiness) and 2027 (slip case — Starship maturity risk).` |

#### §3.2.2 New Assumptions row — V3 DTC first launch year

| Field | Value |
|---|---|
| Column A label | `V3 DTC first launch year` |
| Type | VAL |
| Base Case (B) | `2028` |
| Notes (C) | `Vlad lock 2026-05-20: V3 DTC launches start 2027 or 2028. Annual model uses 2028 as Base Case. Drives V3 DTC eligibility (=1 once year >= this).` |
| MC Min (AG) | `2027` |
| MC Max (AH) | `2028` |
| MC Distribution (AI) | `discrete` |
| MC Notes (AJ) | `Discrete sample between 2027 (earlier ramp — DTC spectrum + V3 readiness aligned) and 2028 (Base Case — DTC spectrum + V3 maturity).` |

#### §3.2.3 New Assumptions row — V2 DTC permanent cap flag

| Field | Value |
|---|---|
| Column A label | `V2 DTC permanent cap flag (1 = no V2 DTC launches 2026+)` |
| Type | VAL |
| Base Case (B) | `1` |
| Notes (C) | `Vlad lock 2026-05-20: SpaceX is permanently capping V2 DTC at the 650 active sats end-2025. No V2 DTC launches 2026 onwards regardless of V3 DTC ratchet status. Implemented as separate flag from the V2/V3 ratchet because V2 DTC shuts down regardless of V3 DTC launches starting (decoupled).` |
| MC Min (AG) | (blank) |
| MC Max (AH) | (blank) |
| MC Distribution (AI) | `fixed` |
| MC Notes (AJ) | `Structural lock — Vlad's stated thesis. No MC range. If MC ever wants to test "what if SpaceX keeps launching V2 DTC", change Base Case to 0 (no cap) in Assumptions; Starlink tab formulas handle either state.` |

#### §3.2.4 New Assumptions row — Starlink ground ops % of revenue

| Field | Value |
|---|---|
| Column A label | `Starlink ground ops % of revenue` |
| Type | VAL |
| Base Case (B) | `0.04` |
| Notes (C) | `Ground stations + network operations + customer support routed through Starlink module COGS per Architecture §3 (NOT corporate SG&A). 4% of revenue stub anchored to Mach33 view of mature satcom ground costs.` |
| MC Min (AG) | `0.02` |
| MC Max (AH) | `0.08` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `MC range covers ultra-lean (2% — fully automated network) → high-touch (8% — substantial customer support + maintenance). Q4'25 didn't break this out but implied ~3-5%.` |

#### §3.2.5 New Assumptions row — Starlink insurance % of revenue

| Field | Value |
|---|---|
| Column A label | `Starlink insurance % of revenue` |
| Type | VAL |
| Base Case (B) | `0.01` |
| Notes (C) | `On-orbit + ground asset insurance + launch insurance for Starlink-owned launches (in addition to launch services COGS). 1% of revenue stub.` |
| MC Min (AG) | `0.005` |
| MC Max (AH) | `0.025` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `Conservative bookends. SpaceX likely self-insures large portions; reported figures from satellite operators (ViaSat, Iridium) trend 0.5-2% of revenue.` |

#### §3.2.6 New Assumptions row — Starlink other COGS % of revenue

| Field | Value |
|---|---|
| Column A label | `Starlink other COGS % of revenue` |
| Type | VAL |
| Base Case (B) | `0.02` |
| Notes (C) | `Catch-all module COGS: rent, utilities, miscellaneous direct costs. 2% of revenue stub.` |
| MC Min (AG) | `0.01` |
| MC Max (AH) | `0.05` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `Mid-range catch-all bracket. If Vlad has more granular data later, replace with explicit line items.` |

**Total Assumptions amendments: 6 new rows × 7 writes each = 42 discrete writes for §3.2.**

---

### §3.3 Starlink tab body — cell-by-cell build (rows 11–199)

Plugin maps logical rows below to specific Starlink tab row numbers. Row numbers in §3.3.X are spec-suggested; plugin may adjust as long as canonical labels match (verbatim, case-sensitive) and writes stay in 11–199 range.

#### §3.3.0 Section headers + subsection layout

Sprint 4 builds the module body in 8 logical sections. Suggested row map (plugin confirms exact rows post-Sprint-1):

```
R12 (SECT): "STARLINK — MODULE BODY"
R13: blank spacer
R14 (SUB): "▸ Bandwidth supply (per-vehicle Gbps with Wright's Law on V3 BB)"
R15-R30: Per-vehicle Gbps year-rows + market share blend
R31: blank spacer
R32 (SUB): "▸ Vehicle deployment (V2 BB, V2 DTC, V3 BB, V3 DTC — launches, fleet, ratchet, retirement)"
R33-R75: Launches per year, active fleet, retirements, ratchet flag, internal launch labels, kg demand labels (PUBLISHES 6 canonical labels for Sprint 3 IFERROR-0 reads)
R76: blank spacer
R77 (SUB): "▸ Per-vehicle CapEx (sat unit cost via Wright's Law + facility CapEx with 1-yr lag)"
R78-R100: Per-vehicle sat cost year-rows + facility cost year-rows + per-vehicle CapEx
R101: blank spacer
R102 (SUB): "▸ Starshield revenue (Q4'25 mechanic — reserved Gbps × $/Gbps with decay)"
R103-R115: Starshield reserved %, reserved Gbps, $/Gbps year-row, Starshield revenue
R116: blank spacer
R117 (SUB): "▸ External revenue (bandwidth-driven: Available Gbps × $/Gbps; subs derived)"
R118-R140: BB Available Gbps read, BB $/Gbps read, BB Revenue, DTC same, Terminal hardware revenue, derived subs
R141: blank spacer
R142 (SUB): "▸ Internal bandwidth revenue (Starlink → ODC, 4-step pattern per Architecture §7.2)"
R143-R150: Starlink internal bandwidth revenue (reads Starlink Capacity rates × ODC demand placeholders)
R151: blank spacer
R152 (SUB): "▸ COGS (Constellation D&A, Ground ops, Spectrum amort BB-only, Terminal COGS, Insurance, Other)"
R153-R175: Each COGS line + Total COGS
R176: blank spacer
R177 (SUB): "▸ Module P&L (vending-machine: Revenue → COGS → EBITDA → CapEx → FCF)"
R178-R199: Module Revenue total, Module EBITDA, Module CapEx, Module FCF
```

Per-vehicle IRR engines (§3.5) and Allocator OUT contract overwrite (§3.6) sit OUTSIDE rows 11-199 — IRR engines as memo rows 211-218, Allocator OUT at rows 200-210 (Sprint 1 placeholders overwritten).

Plugin writes section + subsection headers as discrete label-only writes (Rule 1). Format: SECT = white-on-charcoal fill bold; SUB = italic light grey fill.

#### §3.3.1 Bandwidth supply — per-vehicle Gbps year-rows (rows 15-30)

**Row 15: V2 BB Gbps per sat (constant year-row).**

```
A15 = "V2 BB Gbps per sat"

D15 = =INDEX(Assumptions!$B:$B, MATCH("V2 Mini Bandwidth per Sat — BB (Gbps)", Assumptions!$A:$A, 0))
   (= Sprint 0 R76 = 96 Gbps; disclosed hard anchor)

copyToRange source D15, destination E15:AC15
```

Format: D15:AC15 number `#,##0.0`. Justification: V2 BB Gbps per sat is a disclosed hard anchor (96 Gbps); no learning curve applies to V2 (mature design). Constant year-row.

**Row 16: V2 DTC Gbps per sat (constant year-row).**

```
A16 = "V2 DTC Gbps per sat"

D16 = =INDEX(Assumptions!$B:$B, MATCH("V2 Mini Bandwidth per Sat — DTC (Gbps)", Assumptions!$A:$A, 0))
   (= Sprint 0 R77 = 0.2 Gbps)

copyToRange source D16, destination E16:AC16
```

**Row 17: V3 BB Gbps per sat with Wright's Law (year-row, anchor-and-offset).**

```
A17 = "V3 BB Gbps per sat"

D17 = =MIN(
        INDEX(Assumptions!$B:$B, MATCH("V3 bandwidth cap (Gbps)", Assumptions!$A:$A, 0)),
        INDEX(Assumptions!$B:$B, MATCH("V3 BB Bandwidth per Sat — base year (Gbps)", Assumptions!$A:$A, 0))
        * MAX(1, (D{cum_v3_BB_sats} / 1)^(LOG(1 + INDEX(Assumptions!$B:$B, MATCH("V3 bandwidth per sat — learning rate", Assumptions!$A:$A, 0)), 2)))
      )
```

Wait — Wright's Law on bandwidth is INCREASING (more bandwidth per sat as cum sats double), not decreasing like cost. Architecture §8.4 + Sprint 0 R78 = 1000 Gbps base year + R86 = 0.05 learning rate. The mechanic: V3 BB Gbps per sat in year T = `MIN(R89 cap, R78 × (cum_V3_BB_sats / anchor_cum)^LOG2(1+R86))`. anchor_cum = 1 (first V3 BB launched); learning grows bandwidth as scale grows. Cap = R89 = 5000 Gbps.

Plugin must reference cum_V3_BB_sats from a year-chained running-sum row built earlier in the body. Simpler approach: use anchor-and-offset on year T relative to V3 BB first launch year as the doublings proxy. Let me restructure:

```
A17 = "V3 BB Gbps per sat"

D17 = =MIN(
        INDEX(Assumptions!$B:$B, MATCH("V3 bandwidth cap (Gbps)", Assumptions!$A:$A, 0)),
        INDEX(Assumptions!$B:$B, MATCH("V3 BB Bandwidth per Sat — base year (Gbps)", Assumptions!$A:$A, 0))
        * IFERROR(
            MAX(1, INDEX($D17:$AC17, 1, D$5+1-1) / 1),
            1)
      )

[Year-chained logic — Rule 23 exception: bandwidth-per-sat at year T depends on cumulative V3 BB sats launched, which is a running sum]
```

Actually simpler: V3 BB Gbps per sat is a fixed-yearrow type input. Add 4 new YR rows in Assumptions to handle Wright's Law on V3 BB bandwidth, OR keep R78=1000 as the disclosed-target value and assume V3 BB hits this from year 1 (no in-horizon ramping). Vlad lock #1 (bandwidth-driven revenue) means the calibration target ($7,852M 2025) is anchored to Demand Curves; V3 BB bandwidth-per-sat learning curve is a 2027+ effect.

**Simplification (Vlad to confirm in Sprint 4.5 patch if needed):** Set V3 BB Gbps per sat = Sprint 0 R78 = 1000 Gbps flat year-row. V3 bandwidth cap R89 = 5000 unused this sprint. Wright's Law on V3 bandwidth deferred to Sprint 4.5 if calibration drift surfaces.

```
A17 = "V3 BB Gbps per sat"
D17 = =INDEX(Assumptions!$B:$B, MATCH("V3 BB Bandwidth per Sat — base year (Gbps)", Assumptions!$A:$A, 0))
   (= Sprint 0 R78 = 1000 Gbps flat — Wright's Law deferred to Sprint 4.5)

copyToRange source D17, destination E17:AC17
```

Format: D17:AC17 number `#,##0`.

**Row 18: V3 DTC Gbps per sat (constant year-row).**

```
A18 = "V3 DTC Gbps per sat"
D18 = =INDEX(Assumptions!$B:$B, MATCH("V3 DTC Bandwidth per Sat (Gbps)", Assumptions!$A:$A, 0))
   (= Sprint 0 R79 = 2.75 Gbps flat)

copyToRange source D18, destination E18:AC18
```

#### §3.3.2 Vehicle deployment — launches per year (rows 33-50)

**Row 33: V2 BB launches per year (Vlad lock #3 — historical 2025 + IRR-driven 2026+ subject to ratchet).**

```
A33 = "V2 BB launches per year"

D33 = =INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Sats Launched 2025", Assumptions!$A:$A, 0))
   (= 2987 hardcoded historical via INDEX/MATCH — Rule 14 compliant)

E33 = =IF($D{V3_BB_first_year} > E$4,
           IFERROR(INDEX(Starlink!$D:$AC, MATCH("V2 BB launches per year", Starlink!$A:$A, 0), E$5+1) * 0, 0)
           + Starlink_BB_pool_V2_BB_share * Starlink_BB_pool_launches_capacity,
           0)
```

This is getting complex. Let me restructure as discrete intermediate rows for clarity:

```
Row 33: V2 BB launches per year (FINAL OUTPUT — canonical row)
Row 34: V2 BB eligibility flag (= IF(AND(IRR>0, ratchet=0), 1, 0))
Row 35: V2 BB ask (sats this vehicle would deploy if eligibility = 1 and pool cash sufficient)
Row 36: V2 BB pool share within BB pool (= eligibility × IRR^k / Σ)
Row 37: V2 DTC launches per year
Row 38: V2 DTC eligibility flag
Row 39: V3 BB launches per year
Row 40: V3 BB eligibility flag (= IF(AND(IRR>0, year >= V3 BB first launch year), 1, 0))
Row 41: V3 DTC launches per year
Row 42: V3 DTC eligibility flag (= IF(AND(IRR>0, year >= V3 DTC first launch year), 1, 0))
Row 43: V2/V3 ratchet flag (year-chained Rule 23 exception)
```

**Sprint 4's pre-Sprint-10 default:** Sprint 10 Allocator brain will drive launches per year via cash/kg sigmoid blend at the BB pool + DTC pool level. For Sprint 4 ("modules calibrate against their own demand first; allocator overlay reshapes deployment in out-years" per Sprint Roadmap §0), Sprint 4 hardcodes 2025 launches to Q4'25 anchors and uses a TEMPORARY demand-driven proxy for 2026+ that calibrates to Mach33 thesis:

- 2025: V2 BB = 2987 (R110), V2 DTC = 182 (R111), V3 BB = 0, V3 DTC = 0 — all from Assumptions by INDEX/MATCH.
- 2026: V2 BB launches = `2987 × (1 - V3 BB ratchet 2026 firing)`. If V3 BB first launch year = 2026, V2 BB shuts down to 0 in 2026. But Vlad's intent is "V3 BB starts launching latter half 2026" which means 2026 is the TRANSITION year — V2 BB still launches in early 2026, V3 BB ramps up in late 2026. Annual model approximation: 2026 V2 BB launches = `2987 × 0.5` (half-year), V3 BB launches = ramp from 0. Plugin uses this as Sprint 4 stub; Sprint 10 allocator brain will refine.

Wait — this opens too much complexity for a single sprint. Let me simplify to keep Sprint 4 calibration-driven:

**Simplified Sprint 4 launches per year (Vlad to confirm if calibration fails):**

- **2025**: V2 BB launches = 2987 (R110), V2 DTC launches = 182 (R111), V3 BB = 0, V3 DTC = 0. All hardcoded via INDEX/MATCH per Rule 14.
- **2026 onwards**: Sprint 4 publishes the launches per year FORMULA but with placeholder values driven by a SIMPLE demand-target year-row pending Sprint 10 allocator activation. Specifically:
  - V2 BB launches 2026+: `IF(year < V3 BB first launch year, prev_year_launches × (1 + R85 learning effects ~ 5%/yr), 0)` — V2 BB scales modestly until ratchet fires, then drops to 0.
  - V2 DTC launches 2026+: `0` (V2 DTC permanent cap flag = 1 per §3.2.3).
  - V3 BB launches 2026+: `IF(year >= V3 BB first launch year, V3 BB deployment year-row, 0)` where V3 BB deployment year-row uses a Mach33-thesis ramp anchored to expected V3 BB constellation size by 2030 (~30,000 sats per V30.5 framing) divided by remaining build years. Anchor-and-offset.
  - V3 DTC launches 2026+: similar to V3 BB with V3 DTC first launch year + smaller deployment scale (DTC is a slimmer sub-market).

**This is the most architecturally honest stub.** Sprint 10 will replace these with allocator-driven values. Sprint 4 hits 2025 calibration exactly (the hardcoded historicals) and provides plausible 2030/2040/2050 deployment trajectories for downstream sprints to consume.

#### §3.3.2.1 — Concrete row writes for §3.3.2

**Row 33: V2 BB launches per year**

```
A33 = "V2 BB launches per year"
D33 = =INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Sats Launched 2025", Assumptions!$A:$A, 0))
      (=2987 hardcoded historical)

E33 = =IF(E$4 < INDEX(Assumptions!$B:$B, MATCH("V3 BB first launch year", Assumptions!$A:$A, 0)),
           D33 * (1 + INDEX(Assumptions!$B:$B, MATCH("Satellite cost per kg — learning rate", Assumptions!$A:$A, 0))),
           0)
      [Anchor-and-offset: in pre-V3-BB years, scales last-year launches by ~5% growth proxy.
       Once V3 BB first launch year reached, V2 BB shuts down (ratchet implicit via year comparison).
       Rule 23 exception: references E$4 (year header) + D33 (prior year) — year-chained because growth proxy needs prior-year base.
       Alternative anchor-and-offset (Rule 23 compliant): =IF(E$4 < V3_BB_year, $D$33 × (1 + growth)^E$5, 0).
       Use this Rule 23-compliant form:]

E33 = =IF(E$4 < INDEX(Assumptions!$B:$B, MATCH("V3 BB first launch year", Assumptions!$A:$A, 0)),
           $D$33 * (1 + INDEX(Assumptions!$B:$B, MATCH("Satellite cost per kg — learning rate", Assumptions!$A:$A, 0)))^E$5,
           0)

copyToRange source E33, destination F33:AC33
```

Format: D33:AC33 integer `#,##0`.

**Row 37: V2 DTC launches per year (decoupled — permanent cap flag)**

```
A37 = "V2 DTC launches per year"
D37 = =INDEX(Assumptions!$B:$B, MATCH("V2 Mini DTC Sats Launched 2025", Assumptions!$A:$A, 0))
      (=182 hardcoded historical)

E37 = =IF(INDEX(Assumptions!$B:$B, MATCH("V2 DTC permanent cap flag (1 = no V2 DTC launches 2026+)", Assumptions!$A:$A, 0)) = 1,
           0,
           IF(E$4 < INDEX(Assumptions!$B:$B, MATCH("V3 DTC first launch year", Assumptions!$A:$A, 0)),
              $D$37 * (1 + INDEX(Assumptions!$B:$B, MATCH("Satellite cost per kg — learning rate", Assumptions!$A:$A, 0)))^E$5,
              0))

copyToRange source E37, destination F37:AC37
```

With Base Case (cap flag = 1), V2 DTC launches = 0 from 2026 onwards. If MC overrides cap flag to 0, the fallback formula scales V2 DTC by growth until V3 DTC ratchet fires.

Format: D37:AC37 integer `#,##0`.

**Row 39: V3 BB launches per year**

```
A39 = "V3 BB launches per year"
D39 = =INDEX(Assumptions!$B:$B, MATCH("V3 BB Sats Launched 2025", Assumptions!$A:$A, 0))
      (=0 from Sprint 0 R112)

E39 = =IF(E$4 < INDEX(Assumptions!$B:$B, MATCH("V3 BB first launch year", Assumptions!$A:$A, 0)),
           0,
           V3_BB_DEPLOYMENT_TARGET_FORMULA)
```

V3 BB deployment target formula (Sprint 4 stub, refined by Sprint 10):

**V3 BB deployment target** = year-row that ramps to ~3,000 sats/yr by 2030 (~30K active V3 BB sats by 2035 at 5-yr useful life). Use anchor-and-offset:

```
E39 = =IF(E$4 < INDEX(Assumptions!$B:$B, MATCH("V3 BB first launch year", Assumptions!$A:$A, 0)),
           0,
           MIN(
             5000,
             1000 * (1 + 0.30)^(E$4 - INDEX(Assumptions!$B:$B, MATCH("V3 BB first launch year", Assumptions!$A:$A, 0)))
           ))
```

This violates Rule 14 (hardcoded `1000` and `0.30` and `5000`). Fix: add three more Assumptions rows OR encode as YR row in Assumptions. **Pragmatic Sprint 4 choice:** Add ONE more Assumptions YR row `V3 BB launches per year stub trajectory (year-row, Sprint 4 placeholder)` with explicit yearly values pre-computed. The Starlink tab then reads it via INDEX/MATCH year-row.

Add to §3.2 as a 7th amendment row:

| Field | Value |
|---|---|
| Column A label | `V3 BB launches per year stub trajectory` |
| Type | YR |
| Year values D:AC | 2025=0, 2026=200, 2027=1000, 2028=2000, 2029=3000, 2030=3500, 2031=4000, 2032=4500, 2033=4500, 2034=4500, 2035=4500, 2036=4500, 2037=4500, 2038=4500, 2039=4500, 2040=4500, 2041=4500, 2042=4500, 2043=4500, 2044=4500, 2045=4500, 2046=4500, 2047=4500, 2048=4500, 2049=4500, 2050=4500 |
| Notes (C) | `Sprint 4 placeholder ramp ahead of Sprint 10 allocator activation. Ramps from 200/yr (2026, V3 BB late-half start) to 4,500/yr terminal (~22K active V3 BB constellation at 5-yr life). Sprint 10 overrides via cash/kg IRR-sigmoid allocation; Sprint 4 stub provides plausible deployment for downstream verification.` |
| MC fields | triangle-yearrow; MC Min = scale 0.5x; MC Max = scale 2x |

Then E39 reads this:

```
E39 = =IF(E$4 < INDEX(Assumptions!$B:$B, MATCH("V3 BB first launch year", Assumptions!$A:$A, 0)),
           0,
           INDEX(Assumptions!$D:$AC, MATCH("V3 BB launches per year stub trajectory", Assumptions!$A:$A, 0), E$5+1))

copyToRange source E39, destination F39:AC39
```

**Add §3.2.7 — V3 BB launches per year stub trajectory** (this becomes the 7th new Assumptions row).

Format: D39:AC39 integer `#,##0`.

**Row 41: V3 DTC launches per year**

Add §3.2.8 — V3 DTC launches per year stub trajectory:

| Field | Value |
|---|---|
| Column A label | `V3 DTC launches per year stub trajectory` |
| Type | YR |
| Year values D:AC | 2025=0, 2026=0, 2027=50, 2028=100, 2029=200, 2030=300, 2031=400, 2032=500, 2033=500, 2034=500, 2035=500, 2036=500, 2037=500, 2038=500, 2039=500, 2040=500, 2041=500, 2042=500, 2043=500, 2044=500, 2045=500, 2046=500, 2047=500, 2048=500, 2049=500, 2050=500 |
| Notes (C) | `Sprint 4 placeholder ramp for V3 DTC. ~9× smaller fleet than V3 BB (DTC sub-market is smaller). 2027 start (if MC samples V3 DTC first launch year = 2027) ramps to ~500/yr terminal. Sprint 10 overrides via IRR.` |
| MC fields | triangle-yearrow; MC Min = scale 0.5x; MC Max = scale 2x |

```
A41 = "V3 DTC launches per year"
D41 = =INDEX(Assumptions!$B:$B, MATCH("V3 DTC Sats Launched 2025", Assumptions!$A:$A, 0))   (=0)

E41 = =IF(E$4 < INDEX(Assumptions!$B:$B, MATCH("V3 DTC first launch year", Assumptions!$A:$A, 0)),
           0,
           INDEX(Assumptions!$D:$AC, MATCH("V3 DTC launches per year stub trajectory", Assumptions!$A:$A, 0), E$5+1))

copyToRange source E41, destination F41:AC41
```

#### §3.3.3 V2/V3 ratchet flag — year-chained latch (Rule 23 exception)

**Row 43: V2/V3 ratchet flag (year-row, year-chained latch).**

```
A43 = "V2/V3 ratchet flag (1 = V3 has started launching, V2 BB shut down)"

D43 = =IF(OR(D39 > 0, D41 > 0), 1, 0)
      [If V3 BB launches > 0 OR V3 DTC launches > 0 in 2025 → ratchet fires.
       2025 baseline: D39=0, D41=0 → D43=0.]

E43 = =IF(OR(D43 = 1, E39 > 0, E41 > 0), 1, 0)
      [Once ratchet=1, stays 1 forever. Else fires when V3 BB or V3 DTC launches > 0 in year T.
       Year-chained — Rule 23 exception, intentional. Justification: ratchet is irreversible by Architecture §8.2.]

copyToRange source E43, destination F43:AC43
```

Format: D43:AC43 integer `0` / `1`.

**Update R33 + R37 V2 BB/DTC formulas:** the simplified formulas above use `IF(E$4 < V3_BB_first_year, ...)` which is functionally equivalent to ratchet-gated when V3 BB first launch year is the Base Case 2026. For full architectural rigor (matching Architecture §8.2 verbatim), update R33 to use the ratchet flag:

```
E33 = =IF(D43 = 1,
           0,
           $D$33 * (1 + INDEX(Assumptions!$B:$B, MATCH("Satellite cost per kg — learning rate", Assumptions!$A:$A, 0)))^E$5)
```

Wait — D43 is the ratchet flag in 2025 (=0). E33 should depend on E43 (the ratchet flag in YEAR E). But E43 depends on E39 (V3 BB launches in E), which doesn't yet exist as a formula at the time E33 is written. Excel handles this fine via dependency tracking; the formula is structurally circular only if E39 → E33 → E43 → E39. Let me check:

- E33 reads E43 (ratchet flag in year E).
- E43 reads E39 (V3 BB launches in E) and D43 (prior year ratchet).
- E39 reads V3 BB first launch year from Assumptions + reads V3 BB launches stub from Assumptions — does NOT read E33 or E43.

No circularity. Good.

Final E33 formula:

```
E33 = =IF(E43 = 1,
           0,
           IF(E$4 < INDEX(Assumptions!$B:$B, MATCH("V3 BB first launch year", Assumptions!$A:$A, 0)),
              $D$33 * (1 + INDEX(Assumptions!$B:$B, MATCH("Satellite cost per kg — learning rate", Assumptions!$A:$A, 0)))^E$5,
              0))

copyToRange source E33, destination F33:AC33
```

This handles both: (a) ratchet flag, (b) explicit V3 BB year comparison — belt-and-suspenders for V2 BB shutdown.

#### §3.3.4 Canonical launches labels for Patch B + Customer Launch IFERROR-0 reads (rows 45-50)

**These are the four launch-related canonical labels Sprint 3 IFERROR-0 reads consume. Verbatim string match required (Rule 22).**

**Row 45: F9 V2 BB launches (internal).**

```
A45 = "F9 V2 BB launches (internal)"

D45 = =D33 / 29
      [V2 BB launches D33 / sats per F9 launch ~ 29. Hardcoded `29` violates Rule 14 — fix below.]
```

Add §3.2.9 — Sats per F9 launch — V2 BB:

| Field | Value |
|---|---|
| Column A label | `Sats per F9 launch — V2 BB` |
| Type | VAL |
| Base Case (B) | `29` |
| Notes (C) | `V2 BB sats packaged per F9 launch. Inferred from 2025 historical: 2,987 V2 BB launched / ~104 F9 Starlink launches = ~29 sats per launch. Used by Patch B Launch Capacity R64 wiring to size F9 demand from V2 BB.` |
| MC Min (AG) | `22` |
| MC Max (AH) | `32` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `Range bracket: 22 (Falcon Heavy variant fewer sats per launch) → 32 (denser packaging). Q4'25 implicit ~22 per F9; Mach33 view = 29 mid-point.` |

```
A45 = "F9 V2 BB launches (internal)"

D45 = =IFERROR(D33 / INDEX(Assumptions!$B:$B, MATCH("Sats per F9 launch — V2 BB", Assumptions!$A:$A, 0)), 0)

copyToRange source D45, destination E45:AC45
```

Format: D45:AC45 number `#,##0.0`.

2025: D45 = 2987 / 29 = 103.0 (matches Patch B 2025 Launch Capacity F9 launches = 171 = 38.58 customer + ~104 V2 BB + ~28 V2 DTC + V1/V1.5 ~0).

**Row 46: F9 V2 DTC launches (internal).**

Add §3.2.10 — Sats per F9 launch — V2 DTC:

| Field | Value |
|---|---|
| Column A label | `Sats per F9 launch — V2 DTC` |
| Type | VAL |
| Base Case (B) | `7` |
| Notes (C) | `V2 DTC sats packaged per F9 launch. Mach33 view: 182 V2 DTC launched / ~28 F9 DTC launches = ~7 (DTC sats heavier per unit due to direct-to-cell radio).` |
| MC Min (AG) | `5` |
| MC Max (AH) | `12` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `Range: 5 (max DTC payload per sat) → 12 (smaller DTC sats stacked denser). Limited disclosed data.` |

```
A46 = "F9 V2 DTC launches (internal)"

D46 = =IFERROR(D37 / INDEX(Assumptions!$B:$B, MATCH("Sats per F9 launch — V2 DTC", Assumptions!$A:$A, 0)), 0)

copyToRange source D46, destination E46:AC46
```

2025: D46 = 182 / 7 = 26.0 F9 DTC launches.

**Row 47: Starship V3 BB launches (internal).**

Add §3.2.11 — Sats per Starship launch — V3 BB:

| Field | Value |
|---|---|
| Column A label | `Sats per Starship launch — V3 BB` |
| Type | VAL |
| Base Case (B) | `60` |
| Notes (C) | `V3 BB sats per Starship launch. Mach33 view: V3 BB ~2000 kg/sat × 60 sats = 120K kg = full Starship LEO payload (fully reusable mode, ~100-150K kg).` |
| MC Min (AG) | `40` |
| MC Max (AH) | `100` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `Range: 40 (smaller payload — Starship early variants) → 100 (larger payload — fully reusable Starship V3+).` |

```
A47 = "Starship V3 BB launches (internal)"

D47 = =IFERROR(D39 / INDEX(Assumptions!$B:$B, MATCH("Sats per Starship launch — V3 BB", Assumptions!$A:$A, 0)), 0)

copyToRange source D47, destination E47:AC47
```

2025: D47 = 0 / 60 = 0.

**Row 48: Starship V3 DTC launches (internal).**

Add §3.2.12 — Sats per Starship launch — V3 DTC:

| Field | Value |
|---|---|
| Column A label | `Sats per Starship launch — V3 DTC` |
| Type | VAL |
| Base Case (B) | `15` |
| Notes (C) | `V3 DTC sats per Starship launch. Smaller fleet, larger DTC antennas — fewer per launch than V3 BB.` |
| MC Min (AG) | `8` |
| MC Max (AH) | `25` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `Range based on V3 DTC mass + antenna size uncertainty.` |

```
A48 = "Starship V3 DTC launches (internal)"

D48 = =IFERROR(D41 / INDEX(Assumptions!$B:$B, MATCH("Sats per Starship launch — V3 DTC", Assumptions!$A:$A, 0)), 0)

copyToRange source D48, destination E48:AC48
```

#### §3.3.5 Canonical kg demand labels for Customer Launch R22 IFERROR-0 reads (rows 49-50)

**Row 49: V3 BB Starship kg demand.**

```
A49 = "V3 BB Starship kg demand"

D49 = =D39 * INDEX(Assumptions!$B:$B, MATCH("V3 Mass (kg)", Assumptions!$A:$A, 0))
      [V3 BB launches × V3 mass kg/sat]

copyToRange source D49, destination E49:AC49
```

V3 Mass = Sprint 0 R75 = 2000 kg/sat. 2025: D49 = 0 × 2000 = 0 kg.

Format: D49:AC49 number `#,##0`.

**Row 50: V3 DTC Starship kg demand.**

```
A50 = "V3 DTC Starship kg demand"

D50 = =D41 * INDEX(Assumptions!$B:$B, MATCH("V3 Mass (kg)", Assumptions!$A:$A, 0))
      [V3 DTC launches × V3 mass — assume same mass as V3 BB for simplicity; if V3 DTC mass differs, add Assumptions row]

copyToRange source D50, destination E50:AC50
```

2025: D50 = 0.

**All six canonical labels for Sprint 3 IFERROR-0 reads now published on Starlink tab.** Spec author verifies post-Sprint-4-completion that MATCH calls on all six labels resolve.

#### §3.3.6 Active fleet year-rows (rows 52-65)

Active fleet = running sum (Rule 23 exception — year-chained, intentional).

**Row 52: V2 BB historical retirement (linear over 5 yrs).**

```
A52 = "V2 BB historical retirement"

D52 = =IF(D$5 < INDEX(Assumptions!$B:$B, MATCH("Satellite useful life — V2 Mini (years)", Assumptions!$A:$A, 0)),
           INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB historical baseline (SoY 2025)", Assumptions!$A:$A, 0))
           / INDEX(Assumptions!$B:$B, MATCH("Satellite useful life — V2 Mini (years)", Assumptions!$A:$A, 0)),
           0)
      [= IF(year_offset < 5, 5246 / 5, 0) = 1049.2/yr for years 2025-2029, then 0]

copyToRange source D52, destination E52:AC52
```

Anchor-and-offset compliant — uses D$5 / E$5 / etc. year offset, no chaining.

Format: D52:AC52 number `#,##0.0`.

2025: D52 = 1049.2 (year offset 0 < 5). 2030: I52 = 0.

**Row 53: V2 DTC historical retirement (linear over 5 yrs).**

```
A53 = "V2 DTC historical retirement"

D53 = =IF(D$5 < INDEX(Assumptions!$B:$B, MATCH("Satellite useful life — V2 Mini (years)", Assumptions!$A:$A, 0)),
           INDEX(Assumptions!$B:$B, MATCH("V2 Mini DTC historical baseline (SoY 2025)", Assumptions!$A:$A, 0))
           / INDEX(Assumptions!$B:$B, MATCH("Satellite useful life — V2 Mini (years)", Assumptions!$A:$A, 0)),
           0)
      [= IF(year_offset < 5, 650 / 5, 0) = 130/yr for years 2025-2029]

copyToRange source D53, destination E53:AC53
```

**Row 54: V2 BB launch-cohort retirement (5-yr lag deorbit).**

When a V2 BB sat launched in year T-5 deorbits in year T (after 5 yr useful life from R118 V2 BB Deorbit Lag).

```
A54 = "V2 BB launch-cohort retirement"

D54 = =IFERROR(
        INDEX($D33:$AC33, 1, D$5+1 - INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Deorbit Lag (years)", Assumptions!$A:$A, 0))),
        0)
      [Reads V2 BB launches D$5 - deorbit_lag years ago. For 2025 (offset 0), reads offset -5 → out of range → IFERROR(0). Correct: D54 = 0 in 2025.]

copyToRange source D54, destination E54:AC54
```

For 2030 (offset 5, deorbit_lag=5): I54 = INDEX(launches_year_2025) = 2987.

Anchor-and-offset; not year-chained.

**Row 55: V2 DTC launch-cohort retirement.**

```
A55 = "V2 DTC launch-cohort retirement"

D55 = =IFERROR(
        INDEX($D37:$AC37, 1, D$5+1 - INDEX(Assumptions!$B:$B, MATCH("V2 Mini DTC Deorbit Lag (years)", Assumptions!$A:$A, 0))),
        0)

copyToRange source D55, destination E55:AC55
```

**Row 56: V3 BB launch-cohort retirement.**

```
A56 = "V3 BB launch-cohort retirement"
D56 = =IFERROR(
        INDEX($D39:$AC39, 1, D$5+1 - INDEX(Assumptions!$B:$B, MATCH("V3 BB Deorbit Lag (years)", Assumptions!$A:$A, 0))),
        0)
copyToRange source D56, destination E56:AC56
```

**Row 57: V3 DTC launch-cohort retirement.**

```
A57 = "V3 DTC launch-cohort retirement"
D57 = =IFERROR(
        INDEX($D41:$AC41, 1, D$5+1 - INDEX(Assumptions!$B:$B, MATCH("V3 DTC Deorbit Lag (years)", Assumptions!$A:$A, 0))),
        0)
copyToRange source D57, destination E57:AC57
```

**Row 60: V2 BB active fleet (year-chained Rule 23 exception).**

```
A60 = "Active V2 BB sats"

D60 = =INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Active Sats — end-2025", Assumptions!$A:$A, 0))
      [= 5246 hardcoded historical end-2025 anchor — exact calibration]

E60 = =MAX(0, D60 + E33 - E52 - E54)
      [BoY + launches - historical retirement - launch-cohort retirement.
       Year-chained — Rule 23 exception. Justification: active fleet is a stock variable, fundamentally year-chained.]

copyToRange source E60, destination F60:AC60
```

Format: D60:AC60 integer `#,##0`.

**Row 61: V2 DTC active fleet.**

```
A61 = "Active V2 DTC sats"
D61 = =INDEX(Assumptions!$B:$B, MATCH("V2 Mini DTC Active Sats — end-2025", Assumptions!$A:$A, 0))   (=650)
E61 = =MAX(0, D61 + E37 - E53 - E55)
copyToRange source E61, destination F61:AC61
```

**Row 62: V3 BB active fleet.**

```
A62 = "Active V3 BB sats"
D62 = =0   (end-2025 baseline: no V3 BB sats yet)
E62 = =MAX(0, D62 + E39 - E56)
copyToRange source E62, destination F62:AC62
```

**Row 63: V3 DTC active fleet.**

```
A63 = "Active V3 DTC sats"
D63 = =0
E63 = =MAX(0, D63 + E41 - E57)
copyToRange source E63, destination F63:AC63
```

**Row 65: Total active sats (memo, diagnostic).**

```
A65 = "Memo: Total active Starlink sats"
D65 = =D60 + D61 + D62 + D63 + INDEX(Assumptions!$D:$AC, MATCH("Legacy V1/V1.5 Active Bandwidth (Gbps, year-row runoff)", Assumptions!$A:$A, 0), D$5+1) / INDEX(Assumptions!$B:$B, MATCH("V2 Mini Bandwidth per Sat — BB (Gbps)", Assumptions!$A:$A, 0))
      [Note: legacy V1/V1.5 bandwidth runoff is bandwidth not count, but the per-sat divisor approximates legacy sat count.
       Actually simpler: =D60 + D61 + D62 + D63. Add legacy V1/V1.5 as a separate memo if desired.]

D65 = =D60 + D61 + D62 + D63
copyToRange source D65, destination E65:AC65
```

Format: italic per Rule 17 (memo).

2025: D65 = 5246 + 650 + 0 + 0 = 5896 (excludes legacy V1/V1.5). For full Q4'25 ~9,800 active sat count, legacy V1/V1.5 ~3,900 is implicit in residual bandwidth (R109=71,888 Gbps / V2 96 Gbps = ~750 V1/V1.5-equivalent sats — V1/V1.5 are smaller, so head count is higher: ~3,800-3,900 actual legacy sats). Q4'25 calibration target "Active sats end-2025 ~9,800" is met by adding legacy sat count back to D65 in a future Sprint 4.5 if needed.

#### §3.3.7 Per-vehicle CapEx (rows 78-100)

Implements Vlad lock #7 (CapEx Lag R82=1 yr applies to FACILITIES not sat CapEx).

**Row 78: V2 BB sat unit cost ($mm/sat, year-row with Wright's Law on $/kg).**

```
A78 = "V2 BB sat unit cost ($mm/sat)"

D78 = =INDEX(Assumptions!$B:$B, MATCH("V2 Mini cost per kg — base year ($/kg)", Assumptions!$A:$A, 0))
      * INDEX(Assumptions!$B:$B, MATCH("V2 Mini Mass (kg)", Assumptions!$A:$A, 0))
      / 1000000
      [= $650/kg × 575 kg / 1e6 = $0.374M per V2 BB sat in 2025]

E78 = =MAX(
        INDEX(Assumptions!$B:$B, MATCH("V2 Mini cost floor ($/kg)", Assumptions!$A:$A, 0))
        * INDEX(Assumptions!$B:$B, MATCH("V2 Mini Mass (kg)", Assumptions!$A:$A, 0)) / 1000000,
        $D$78 * (1 - INDEX(Assumptions!$B:$B, MATCH("V2 Mini cost per kg — learning rate", Assumptions!$A:$A, 0)))^E$5
      )
      [Anchor-and-offset bounded-CAGR per Rule 23. Cost declines toward floor as learning compounds.]

copyToRange source E78, destination F78:AC78
```

Format: D78:AC78 currency `$#,##0.000` ($mm with 3 decimals).

**Row 79: V2 DTC sat unit cost ($mm/sat).**

Same structure — V2 Mini mass × $/kg with WL learning. Use same V2 Mini parameters per Sprint 0 R90/R91/R92.

```
A79 = "V2 DTC sat unit cost ($mm/sat)"
D79 = =D78   (same V2 Mini production line per Sprint 0 R90 note)
copyToRange source D79, destination E79:AC79
```

**Row 80: V3 BB sat unit cost ($mm/sat).**

```
A80 = "V3 BB sat unit cost ($mm/sat)"

D80 = =INDEX(Assumptions!$B:$B, MATCH("Satellite cost per kg — base year ($/kg)", Assumptions!$A:$A, 0))
      * INDEX(Assumptions!$B:$B, MATCH("V3 Mass (kg)", Assumptions!$A:$A, 0))
      / 1000000
      [= $650/kg × 2000 kg / 1e6 = $1.300M per V3 BB sat in 2025]

E80 = =MAX(
        INDEX(Assumptions!$B:$B, MATCH("Satellite cost floor ($/kg)", Assumptions!$A:$A, 0))
        * INDEX(Assumptions!$B:$B, MATCH("V3 Mass (kg)", Assumptions!$A:$A, 0)) / 1000000,
        $D$80 * (1 - INDEX(Assumptions!$B:$B, MATCH("Satellite cost per kg — learning rate", Assumptions!$A:$A, 0)))^E$5
      )

copyToRange source E80, destination F80:AC80
```

**Row 81: V3 DTC sat unit cost ($mm/sat).**

```
A81 = "V3 DTC sat unit cost ($mm/sat)"
D81 = =D80   (same V3 production line)
copyToRange source D81, destination E81:AC81
```

**Row 83: V2 BB facility CapEx per sat ($mm/sat, year-row with WL learning).**

```
A83 = "V2 BB facility CapEx per sat ($mm/sat)"

D83 = =INDEX(Assumptions!$B:$B, MATCH("Facility CapEx per satellite — base year ($)", Assumptions!$A:$A, 0)) / 1000000
      [= $90,650 / 1e6 = $0.0907M per sat in 2025]

E83 = =$D$83 * (1 - INDEX(Assumptions!$B:$B, MATCH("Facility CapEx — learning rate", Assumptions!$A:$A, 0)))^E$5
      [10% per doubling learning — Sprint 0 R103]

copyToRange source E83, destination F83:AC83
```

Format: D83:AC83 currency `$#,##0.0000`.

**Rows 84-86: Other vehicle facility CapEx (all use same formula structure).**

Same as R83 for V2 DTC, V3 BB, V3 DTC (assumes shared ground-segment cost structure).

**Row 88: V2 BB sat CapEx (no lag — sats launched same year as built).**

```
A88 = "V2 BB sat CapEx ($mm)"

D88 = =D33 * D78
      [V2 BB launches × V2 BB sat unit cost]

copyToRange source D88, destination E88:AC88
```

Format: D88:AC88 currency `$#,##0`.

**Row 89: V2 BB facility CapEx (1-yr lag — facilities for next year's deployment booked this year).**

```
A89 = "V2 BB facility CapEx ($mm)"

D89 = =IFERROR(
        INDEX($D33:$AC33, 1, D$5+2)
        * INDEX($D83:$AC83, 1, D$5+1),
        0)
      [Reads NEXT year's launches (D$5+2 = column offset +1) × THIS year's facility cost per sat.
       Year T's CapEx is for sats DEPLOYED in year T+1. 2050 (offset 25): reads column AC$5+2 = offset 27 → out of range → IFERROR(0).
       Anchor-and-offset compliant, not year-chained.]

copyToRange source D89, destination E89:AC89
```

Format: D89:AC89 currency `$#,##0`.

**Rows 90-95: V2 DTC, V3 BB, V3 DTC sat + facility CapEx (same structure as R88-R89).**

```
A90 = "V2 DTC sat CapEx ($mm)";       D90 = =D37 * D79;                       copy to E:AC
A91 = "V2 DTC facility CapEx ($mm)";  D91 = =IFERROR(INDEX($D37:$AC37,1,D$5+2) * INDEX($D84:$AC84,1,D$5+1), 0);  copy
A92 = "V3 BB sat CapEx ($mm)";        D92 = =D39 * D80;                        copy
A93 = "V3 BB facility CapEx ($mm)";   D93 = =IFERROR(INDEX($D39:$AC39,1,D$5+2) * INDEX($D85:$AC85,1,D$5+1), 0); copy
A94 = "V3 DTC sat CapEx ($mm)";       D94 = =D41 * D81;                        copy
A95 = "V3 DTC facility CapEx ($mm)";  D95 = =IFERROR(INDEX($D41:$AC41,1,D$5+2) * INDEX($D86:$AC86,1,D$5+1), 0); copy
```

**Row 98: Total Module CapEx (= Sat CapEx + Facility CapEx).**

```
A98 = "Module CapEx ($mm)"
D98 = =D88 + D89 + D90 + D91 + D92 + D93 + D94 + D95
copyToRange source D98, destination E98:AC98
```

Format: D98:AC98 currency `$#,##0`.

**Row 99: Capital deployed (= (sat + facility) × sats launched this year, equilibrium-equal in flat-launches case).**

```
A99 = "Capital deployed ($mm)"
D99 = =D33 * (D78 + D83) + D37 * (D79 + D84) + D39 * (D80 + D85) + D41 * (D81 + D86)
copyToRange source D99, destination E99:AC99
```

Format: D99:AC99 currency `$#,##0`. In equilibrium when launches flat year-over-year, D98 ≈ D99. During ramps D98 > D99 (facility CapEx booked ahead).

#### §3.3.8 Starshield revenue — Q4'25 mechanic (rows 103-115)

**Row 103: Total constellation BB Gbps (= active sats × per-sat Gbps).**

```
A103 = "Total active BB Gbps (Starlink + Starshield + legacy)"

D103 = =D60 * D15
       + D62 * D17
       + INDEX(Assumptions!$D:$AC, MATCH("Legacy V1/V1.5 Active Bandwidth (Gbps, year-row runoff)", Assumptions!$A:$A, 0), D$5+1)
       [= (V2 BB active × V2 BB Gbps/sat) + (V3 BB active × V3 BB Gbps/sat) + legacy V1/V1.5 bandwidth runoff
        2025: 5246 × 96 + 0 × 1000 + 71,888 = 503,616 + 0 + 71,888 = 575,504 Gbps]

copyToRange source D103, destination E103:AC103
```

Format: D103:AC103 number `#,##0`.

**Row 104: Starshield reserved % (year-row with decay — anchor-and-offset).**

```
A104 = "Starshield reserved %"

D104 = =INDEX(Assumptions!$B:$B, MATCH("Starshield Reserved % — start", Assumptions!$A:$A, 0))
       [= 0.0257]

E104 = =MAX(
         INDEX(Assumptions!$B:$B, MATCH("Starshield Reserved % — floor", Assumptions!$A:$A, 0)),
         $D$104 * (1 - INDEX(Assumptions!$B:$B, MATCH("Starshield Reserved % — decay rate", Assumptions!$A:$A, 0)))^E$5
       )
       [Anchor-and-offset bounded decay per Rule 23]

copyToRange source E104, destination F104:AC104
```

Format: D104:AC104 percent `0.0000%`.

2025: D104 = 2.57%. 2030: I104 = 2.57% × (1-0.25)^5 = 0.61%. Floor = 0.01%.

**Row 105: Starshield reserved Gbps.**

```
A105 = "Starshield reserved Gbps"
D105 = =D103 * D104
copyToRange source D105, destination E105:AC105
```

Format: D105:AC105 number `#,##0`.

2025: D105 = 575,504 × 0.0257 = 14,790 Gbps.

**Row 106: Starshield $/Gbps (year-row with decay — anchor-and-offset).**

```
A106 = "Starshield $/Gbps ($/Gbps/yr)"

D106 = =INDEX(Assumptions!$B:$B, MATCH("Starshield Rev per Gbps — base year ($/Gbps)", Assumptions!$A:$A, 0))
       [= $164,699]

E106 = =$D$106 * (1 - INDEX(Assumptions!$B:$B, MATCH("Starshield Rev per Gbps — decay rate", Assumptions!$A:$A, 0)))^E$5
       [5% decay per Sprint 0 R98]

copyToRange source E106, destination F106:AC106
```

Format: D106:AC106 currency `$#,##0`.

**Row 110: Starshield revenue.**

```
A110 = "Starshield revenue ($mm)"
D110 = =D105 * D106 / 1000000
       [(Starshield reserved Gbps × $/Gbps) / 1e6 to convert to $mm]

copyToRange source D110, destination E110:AC110
```

Format: D110:AC110 currency `$#,##0`.

2025 calibration check: D110 = 14,790 × 164,699 / 1e6 = $2,436M (target $2,520M ±5%; within tolerance — slight undershoot due to ratio rounding; refine if Sprint 4 verification surfaces material drift).

#### §3.3.9 External revenue — bandwidth-driven with derived subs (rows 118-140)

**Reads from Starlink Capacity tab (built in §3.4 below) and Demand Curves (V9 inheritance).**

**Row 118: BB Gbps available for external Starlink revenue.**

```
A118 = "BB Gbps available for external Starlink revenue"

D118 = =INDEX('Starlink Capacity'!$D:$AC, MATCH("BB Gbps available for external Starlink revenue", 'Starlink Capacity'!$A:$A, 0), D$5+1)

copyToRange source D118, destination E118:AC118
```

Format: D118:AC118 number `#,##0`.

**Row 119: BB $/Gbps (read from Demand Curves V9 tab).**

```
A119 = "BB $/Gbps ($/Gbps/yr)"

D119 = =INDEX('Demand Curves'!$D:$AC, MATCH("Total BB price ($/Gbps/yr)", 'Demand Curves'!$A:$A, 0), D$5+1)

copyToRange source D119, destination E119:AC119
```

[If pre-flight §3.0 #7 found different V9 labels, plugin substitutes those labels here. Spec author confirms before plugin executes.]

Format: D119:AC119 currency `$#,##0`.

**Row 120: BB Revenue ($mm).**

```
A120 = "BB Revenue ($mm)"
D120 = =D118 * D119 / 1000000

copyToRange source D120, destination E120:AC120
```

Format: D120:AC120 currency `$#,##0`.

Calibration: D120 + D131 (DTC Revenue) should sum to $7,852M ±5% in 2025.

**Row 121: BB ARPU ($/mo).**

```
A121 = "BB ARPU ($/mo, year-row from Assumptions)"
D121 = =INDEX(Assumptions!$D:$AC, MATCH("Broadband ARPU ($/sub/mo, year-row)", Assumptions!$A:$A, 0), D$5+1)
copyToRange source D121, destination E121:AC121
```

2025: D121 = $100/mo per Sprint 0 R128.

Format: D121:AC121 currency `$#,##0`.

**Row 122: BB subscribers derived (millions).**

```
A122 = "BB subscribers (millions, derived = BB Revenue / (ARPU × 12))"

D122 = =IFERROR(D120 / (D121 * 12) , 0)
       [Revenue ($mm) / (ARPU $/mo × 12 mo) = subscribers in millions]

copyToRange source D122, destination E122:AC122
```

Format: D122:AC122 number `#,##0.0`.

2025 check: D122 = $7,695M / ($100 × 12) = $7,695 / $1,200 = 6.41M BB subs. (Target range 5.5-7.5M — within tolerance.)

**Rows 128-131: DTC same structure.**

```
A128 = "DTC Gbps available for external Starlink revenue"
D128 = =INDEX('Starlink Capacity'!$D:$AC, MATCH("DTC Gbps available for external Starlink revenue", 'Starlink Capacity'!$A:$A, 0), D$5+1)
copy

A129 = "DTC $/Gbps ($/Gbps/yr)"
D129 = =INDEX('Demand Curves'!$D:$AC, MATCH("Total DTC price ($/Gbps/yr)", 'Demand Curves'!$A:$A, 0), D$5+1)
copy

A130 = "DTC ARPU ($/mo, year-row from Assumptions)"
D130 = =INDEX(Assumptions!$D:$AC, MATCH("DTC ARPU ($/sub/mo, year-row)", Assumptions!$A:$A, 0), D$5+1)
copy

A131 = "DTC Revenue ($mm)"
D131 = =D128 * D129 / 1000000
copy

A132 = "DTC subscribers (millions, derived = DTC Revenue / (ARPU × 12))"
D132 = =IFERROR(D131 / (D130 * 12), 0)
copy
```

2025 calibration target: D131 ≈ $157M, D132 ≈ $157 / ($16 × 12) = 0.82M DTC subs.

**Row 135: Terminal hardware revenue.**

```
A135 = "Terminal hardware revenue ($mm)"

D135 = =MAX(0, D122 - INDEX($D122:$AC122, 1, MAX(1, D$5+1-1)))
       * (INDEX(Assumptions!$B:$B, MATCH("Subsidy mix (% of net adds subsidized)", Assumptions!$A:$A, 0))
         * INDEX(Assumptions!$B:$B, MATCH("Terminal retail price ($, subsidized)", Assumptions!$A:$A, 0))
         + (1 - INDEX(Assumptions!$B:$B, MATCH("Subsidy mix (% of net adds subsidized)", Assumptions!$A:$A, 0)))
           * INDEX(Assumptions!$B:$B, MATCH("Terminal retail price ($, non-subsidized)", Assumptions!$A:$A, 0)))
       / 1e6
       * 1e6 / 1e6
       [Net adds in millions × blended price per terminal in $ / 1e6 to get $mm.
        Math: net_adds × ((0.5 × $300) + (0.5 × $500)) = net_adds × $400 per terminal. In $mm: net_adds_millions × $400 = $400 × net_adds_millions.
        Simplification — final formula:]

D135 = =MAX(0, D122 - IFERROR(INDEX($D122:$AC122, 1, D$5), 0))
       * (
         INDEX(Assumptions!$B:$B, MATCH("Subsidy mix (% of net adds subsidized)", Assumptions!$A:$A, 0))
         * INDEX(Assumptions!$B:$B, MATCH("Terminal retail price ($, subsidized)", Assumptions!$A:$A, 0))
         + (1 - INDEX(Assumptions!$B:$B, MATCH("Subsidy mix (% of net adds subsidized)", Assumptions!$A:$A, 0)))
           * INDEX(Assumptions!$B:$B, MATCH("Terminal retail price ($, non-subsidized)", Assumptions!$A:$A, 0))
         )

copyToRange source D135, destination E135:AC135
```

Note: D122 net adds = D122 BB subs - prior year BB subs. 2025 reads prior year (D$5=0 → offset 0-1 = -1 invalid → IFERROR 0). Net adds 2025 = D122 - 0 = 6.41M. Terminal rev 2025 = 6.41 × $400 = $2,564M.

Wait, terminals shouldn't dwarf service revenue. Net adds 2025 are likely smaller (the 2024 starting BB subs were ~5M; 2025 net adds ≈ 1.4M). The formula needs the 2024 starting point. Use Sprint 0 R127:

```
D135_alt = =MAX(0, D122 - INDEX(Assumptions!$B:$B, MATCH("Starting BoY 2025 subscribers (millions)", Assumptions!$A:$A, 0)))
           * blended_price_calc
```

For 2025: net adds = 6.41 - 5 = 1.41M. Terminal rev = 1.41 × $400 = $564M.

For 2026+: net adds = D122_current - D122_prior. Use INDEX($D122:$AC122, 1, D$5).

```
D135 = =MAX(0, D122 - IF(D$5 = 0,
                          INDEX(Assumptions!$B:$B, MATCH("Starting BoY 2025 subscribers (millions)", Assumptions!$A:$A, 0)),
                          INDEX($D122:$AC122, 1, D$5)))
       * (
         INDEX(Assumptions!$B:$B, MATCH("Subsidy mix (% of net adds subsidized)", Assumptions!$A:$A, 0))
         * INDEX(Assumptions!$B:$B, MATCH("Terminal retail price ($, subsidized)", Assumptions!$A:$A, 0))
         + (1 - INDEX(Assumptions!$B:$B, MATCH("Subsidy mix (% of net adds subsidized)", Assumptions!$A:$A, 0)))
           * INDEX(Assumptions!$B:$B, MATCH("Terminal retail price ($, non-subsidized)", Assumptions!$A:$A, 0))
         )

copyToRange source D135, destination E135:AC135
```

Format: D135:AC135 currency `$#,##0`.

#### §3.3.10 Internal bandwidth revenue (rows 143-150)

**Row 143: Starlink internal bandwidth revenue ($mm) — reads Starlink Capacity rates × ODC demand placeholders.**

```
A143 = "Starlink internal bandwidth revenue ($mm)"

D143 = =IFERROR(INDEX('Starlink Capacity'!$D:$AC, MATCH("ODC BB Gbps demand", 'Starlink Capacity'!$A:$A, 0), D$5+1)
                * INDEX('Starlink Capacity'!$D:$AC, MATCH("BB pool at-cost rate ($/Gbps/yr)", 'Starlink Capacity'!$A:$A, 0), D$5+1)
                / 1000000, 0)
       + IFERROR(INDEX('Starlink Capacity'!$D:$AC, MATCH("ODC DTC Gbps demand", 'Starlink Capacity'!$A:$A, 0), D$5+1)
                * INDEX('Starlink Capacity'!$D:$AC, MATCH("DTC pool at-cost rate ($/Gbps/yr)", 'Starlink Capacity'!$A:$A, 0), D$5+1)
                / 1000000, 0)
       [BB and DTC components, each with IFERROR wrapper. Resolves to $0 at Sprint 4 exit because Starlink Capacity's `ODC BB/DTC Gbps demand` rows read ODC tab with IFERROR-0 (Sprint 5 hasn't fired).]

copyToRange source D143, destination E143:AC143
```

Format: D143:AC143 currency `$#,##0`.

Per Architecture §7.2 4-step Rule 21 pattern: this is step 1 (source books internal transfer revenue). Step 2 (ODC books matching cost) lands in Sprint 5. Step 3 (Group P&L R106 elimination) lands in Sprint 9. Step 4 (conservation R106 verifies) lands in Sprint 9.

#### §3.3.11 COGS (rows 153-175)

**Row 153: Constellation D&A ($mm).**

```
A153 = "Constellation D&A ($mm)"

D153 = =(D60 * INDEX(Assumptions!$B:$B, MATCH("V2 Mini Mass (kg)", Assumptions!$A:$A, 0))
        + D61 * INDEX(Assumptions!$B:$B, MATCH("V2 Mini Mass (kg)", Assumptions!$A:$A, 0))
        + D62 * INDEX(Assumptions!$B:$B, MATCH("V3 Mass (kg)", Assumptions!$A:$A, 0))
        + D63 * INDEX(Assumptions!$B:$B, MATCH("V3 Mass (kg)", Assumptions!$A:$A, 0)))
       * INDEX(Assumptions!$B:$B, MATCH("Satellite Dep per kg — base year ($/kg/yr)", Assumptions!$A:$A, 0))
       * (1 - INDEX(Assumptions!$B:$B, MATCH("Satellite Dep per kg — annual decay rate", Assumptions!$A:$A, 0)))^D$5
       / 1000000
       [Active mass (kg) × dep rate ($/kg/yr with annual decay) / 1e6 for $mm.
        2025: (5246+650)×575 + (0+0)×2000 = 3,390,200 kg × $128.8/kg / 1e6 = $436.65M
        Hmm — target is $707M. Need to include legacy V1/V1.5 mass.
        Add legacy mass: Q4'25 legacy ~3,900 sats × ~250kg avg = 975,000 kg → total ~4.37M kg × $128.8 = $562M.
        Still short of $707M. Need to check whether Constellation D&A also picks up the in-flight CapEx amortization.]

[ALTERNATIVE — match Q4'25 R195 mechanic which derives D&A from sat-launched cohorts amortizing over useful life:]

D153 = =(SUMPRODUCT(
          (INDEX($D33:$AC33, 0) > 0) * (D$5 - COLUMN($D33:$AC33) + COLUMN($D33))
            <= INDEX(Assumptions!$B:$B, MATCH("Satellite useful life — V2 Mini (years)", Assumptions!$A:$A, 0)),
          INDEX($D33:$AC33, 0)
          ) * (D78 * 1000) / INDEX(Assumptions!$B:$B, MATCH("Satellite useful life — V2 Mini (years)", Assumptions!$A:$A, 0))
        ...
        )
        [TOO COMPLEX. Simpler implementation: D&A = Σ_vehicles (Sat CapEx in year T-1 + ... + Sat CapEx in year T-N) / N. Each year's amortization is the average of last-N years' CapEx.]

[FINAL — use simpler total approach: D&A = active mass × $/kg/yr dep rate, but calibrate the dep rate to Q4'25 $707M target.
 Active mass 2025 ≈ 5246×575 + 650×575 = 3.39M kg V2.
 $707M / 3.39M = $208/kg/yr dep rate.
 Sprint 0 R100 = $128.8/kg/yr (Q4'25 anchor). Discrepancy = ~$70M. Could be legacy V1/V1.5 D&A + facility D&A.]

D153 = =(D60 + D61) * INDEX(Assumptions!$B:$B, MATCH("V2 Mini Mass (kg)", Assumptions!$A:$A, 0))
       * INDEX(Assumptions!$B:$B, MATCH("Satellite Dep per kg — base year ($/kg/yr)", Assumptions!$A:$A, 0))
       * (1 - INDEX(Assumptions!$B:$B, MATCH("Satellite Dep per kg — annual decay rate", Assumptions!$A:$A, 0)))^D$5
       / 1000000
       + (D62 + D63) * INDEX(Assumptions!$B:$B, MATCH("V3 Mass (kg)", Assumptions!$A:$A, 0))
         * INDEX(Assumptions!$B:$B, MATCH("Satellite Dep per kg — base year ($/kg/yr)", Assumptions!$A:$A, 0))
         * (1 - INDEX(Assumptions!$B:$B, MATCH("Satellite Dep per kg — annual decay rate", Assumptions!$A:$A, 0)))^D$5
         / 1000000

copyToRange source D153, destination E153:AC153
```

2025 calibration: D153 ≈ (5246+650)×575×128.8/1e6 = $437M. Target $707M ±10% → range [$636M, $778M]. **Out of tolerance. Halt + retune at §4.4 sanity check.** Likely fix: add legacy V1/V1.5 contribution (~$130M) + facility D&A (~$140M) = $707M reachable.

**Sprint 4 retune option (if §4.4 halt fires):** Add a memo row R154 `Memo: Legacy + facility D&A ($mm)` computing facility CapEx amortization. Or accept the $437M and flag as Sprint 4.5 patch item.

Format: D153:AC153 currency `$#,##0`.

**Rows 156-170: Other COGS lines.**

```
A156 = "Launch services cost ($mm) — internal at-cost from Customer Launch"
D156 = =(IFERROR(D45, 0) + IFERROR(D46, 0))
       * INDEX('Launch Capacity'!$D:$AC, MATCH("F9 at-cost rate ($mm/launch)", 'Launch Capacity'!$A:$A, 0), D$5+1)
       + (IFERROR(D47, 0) + IFERROR(D48, 0))
       * INDEX('Launch Capacity'!$D:$AC, MATCH("Starship at-cost rate ($mm/launch)", 'Launch Capacity'!$A:$A, 0), D$5+1)
copy

A158 = "Ground ops cost ($mm)"
D158 = =D178 * INDEX(Assumptions!$B:$B, MATCH("Starlink ground ops % of revenue", Assumptions!$A:$A, 0))
       [D178 = Module Revenue total — built below in §3.3.12]
copy

A160 = "Spectrum amortization (BB-only) ($mm)"
D160 = =IFERROR(INDEX(CapEx!$D:$AC, MATCH("Annual Spectrum amortization ($mm/yr)", CapEx!$A:$A, 0), D$5+1), 0)
       [Reads CapEx tab — Sprint 8 hasn't fired, IFERROR-0 wrapper resolves to $0 until Sprint 8 populates spectrum amort.
        Note: Sprint 4 spec doesn't apportion spectrum amort to BB only — Sprint 8 publishes the canonical row, and per Architecture §12.1 + Sprint Roadmap §3 Sprint 4 lock 2026-05-20, the entire spectrum amort flows to Starlink BB COGS only (DTC uses MSS bands).]
copy

A162 = "Terminal COGS ($mm)"
D162 = =MAX(0, D122 - IF(D$5 = 0, INDEX(Assumptions!$B:$B, MATCH("Starting BoY 2025 subscribers (millions)", Assumptions!$A:$A, 0)), INDEX($D122:$AC122, 1, D$5)))
       * INDEX(Assumptions!$B:$B, MATCH("Terminal COGS per unit ($)", Assumptions!$A:$A, 0))
       [Net adds × terminal COGS per unit ($500). Net adds 1.41M × $500 = $705M.]
copy

A165 = "Insurance ($mm)"
D165 = =D178 * INDEX(Assumptions!$B:$B, MATCH("Starlink insurance % of revenue", Assumptions!$A:$A, 0))
copy

A167 = "Other COGS ($mm)"
D167 = =D178 * INDEX(Assumptions!$B:$B, MATCH("Starlink other COGS % of revenue", Assumptions!$A:$A, 0))
copy

A170 = "Total COGS ($mm)"
D170 = =D153 + D156 + D158 + D160 + D162 + D165 + D167
copy
```

[All `copy` operations are `copyToRange source D{row}, destination E{row}:AC{row}`.]

Note: D158/D165/D167 reference D178 (Module Revenue total) which is computed below. Excel handles forward refs via dependency tracking; no circularity issue because D178 doesn't read these back.

#### §3.3.12 Module P&L (rows 178-199)

**Row 178: Module Revenue total.**

```
A178 = "Total Revenue ($mm)"
D178 = =D120 + D131 + D135 + D110 + D143
       [BB Revenue + DTC Revenue + Terminal hardware + Starshield + Internal bandwidth]

copyToRange source D178, destination E178:AC178
```

Format: D178:AC178 currency `$#,##0`. **CALIBRATION CHECK**: D178 2025 should equal Starlink+DTC ($7,852M) + Starshield ($2,520M) + Terminals ($564M est) + Internal bandwidth ($0) = ~$10.94B. Q4'25 R145 Group Revenue 2025 = $14.65B (sum of Starlink+DTC+Starshield+Customer Launch = $7.85B+$2.52B+$4.29B = $14.66B); Q4'25 specifies Starlink+DTC = $7,852M which already INCLUDES terminal hardware revenue per Q4'25 build convention. **Verify with Vlad in Sprint 4.5 patch whether Terminal Hardware is included in $7,852M or separate.** Tolerance: D178 2025 in [$10.0B, $11.5B] is acceptable; halt outside.

**Row 181: Module EBITDA = Gross Profit.**

```
A181 = "Module EBITDA ($mm)"
D181 = =D178 - D170

copyToRange source D181, destination E181:AC181
```

Format: D181:AC181 currency `$#,##0`.

**Row 182: Module EBITDA Margin %.**

```
A182 = "Module EBITDA Margin %"
D182 = =IFERROR(D181 / D178, 0)
copy
```

Format: D182:AC182 percent `0.0%`. **CALIBRATION CHECK**: 55-75% range per §6.3.

**Row 185: Module CapEx (= R98 above).**

```
A185 = "Module CapEx ($mm) — restated"
D185 = =D98
copy
```

**Row 188: Module FCF (pre-tax, pre-corp).**

```
A188 = "Module FCF ($mm)"
D188 = =D181 + D153 - D185
       [Module EBITDA + module D&A add-back (Constellation D&A in COGS) − Module CapEx
        Per Architecture §3 Module FCF formula.]
copy
```

Format: D188:AC188 currency `$#,##0`.

---

### §3.4 Starlink Capacity tab — full build

Starlink Capacity is the supply-side aggregator. Sprint 1 placed title row at A6 only; Sprint 4 fills the rest.

**Row layout suggested:**

```
R4-R5: year header + offset (Sprint 0 inheritance)
R6: title row (Sprint 1)
R7: blank
R8 (SECT): "STARLINK CAPACITY — supply-side bandwidth aggregation + internal claim to ODC"
R9: blank
R10 (SUB): "▸ Total active Gbps (BB + DTC, from Starlink tab active sat fleet)"
R11-R15: BB + DTC active Gbps year-rows
R16: blank
R17 (SUB): "▸ Internal claim by ODC (Sprint 5 placeholders)"
R18-R25: ODC BB Gbps demand + ODC DTC Gbps demand (IFERROR-0 reads of ODC tab)
R26: blank
R27 (SUB): "▸ Available bandwidth for external Starlink revenue"
R28-R32: BB available + DTC available year-rows
R33: blank
R34 (SUB): "▸ Pool cost basis ($mm/yr; reads Starlink tab COGS components)"
R35-R45: BB pool cost basis + DTC pool cost basis year-rows
R46: blank
R47 (SUB): "▸ At-cost transfer rates ($/Gbps/yr; for Sprint 5 ODC + Starlink internal bandwidth revenue)"
R48-R55: BB pool at-cost rate + DTC pool at-cost rate year-rows
```

#### §3.4.1 Total active Gbps (rows 11-15)

**Row 11: Total active BB Gbps (= V2 BB active × per-sat Gbps + V3 BB active × per-sat Gbps + legacy V1/V1.5 Gbps).**

```
A11 = "Total active BB Gbps"

D11 = =INDEX(Starlink!$D:$AC, MATCH("Active V2 BB sats", Starlink!$A:$A, 0), D$5+1)
        * INDEX(Starlink!$D:$AC, MATCH("V2 BB Gbps per sat", Starlink!$A:$A, 0), D$5+1)
      + INDEX(Starlink!$D:$AC, MATCH("Active V3 BB sats", Starlink!$A:$A, 0), D$5+1)
        * INDEX(Starlink!$D:$AC, MATCH("V3 BB Gbps per sat", Starlink!$A:$A, 0), D$5+1)
      + INDEX(Assumptions!$D:$AC, MATCH("Legacy V1/V1.5 Active Bandwidth (Gbps, year-row runoff)", Assumptions!$A:$A, 0), D$5+1)

copyToRange source D11, destination E11:AC11
```

Format: D11:AC11 number `#,##0`.

**Row 13: Total active DTC Gbps.**

```
A13 = "Total active DTC Gbps"

D13 = =INDEX(Starlink!$D:$AC, MATCH("Active V2 DTC sats", Starlink!$A:$A, 0), D$5+1)
        * INDEX(Starlink!$D:$AC, MATCH("V2 DTC Gbps per sat", Starlink!$A:$A, 0), D$5+1)
      + INDEX(Starlink!$D:$AC, MATCH("Active V3 DTC sats", Starlink!$A:$A, 0), D$5+1)
        * INDEX(Starlink!$D:$AC, MATCH("V3 DTC Gbps per sat", Starlink!$A:$A, 0), D$5+1)

copyToRange source D13, destination E13:AC13
```

#### §3.4.2 ODC internal claim (rows 18-25)

**Row 18: ODC BB Gbps demand (IFERROR-0 read of ODC tab).**

```
A18 = "ODC BB Gbps demand"

D18 = =IFERROR(INDEX(ODC!$D:$AC, MATCH("ODC BB Gbps demand", ODC!$A:$A, 0), D$5+1), 0)

copyToRange source D18, destination E18:AC18
```

Sprint 4 result: 0 throughout (ODC tab has only Sprint 1 shell, no `ODC BB Gbps demand` row yet). Sprint 5 publishes the row → IFERROR resolves.

**Row 20: ODC DTC Gbps demand.**

```
A20 = "ODC DTC Gbps demand"
D20 = =IFERROR(INDEX(ODC!$D:$AC, MATCH("ODC DTC Gbps demand", ODC!$A:$A, 0), D$5+1), 0)
copy
```

#### §3.4.3 Available bandwidth (rows 28-32)

**Row 28: BB Gbps available for external Starlink revenue.**

```
A28 = "BB Gbps available for external Starlink revenue"
D28 = =MAX(0, D11 - D18)
copy
```

**Row 30: DTC Gbps available for external Starlink revenue.**

```
A30 = "DTC Gbps available for external Starlink revenue"
D30 = =MAX(0, D13 - D20)
copy
```

#### §3.4.4 Pool cost basis (rows 35-45)

Per Sprint 4 lock 2026-05-20: BB pool cost basis = Gbps-share-weighted Constellation D&A + Ground ops + Spectrum amort (BB-only). DTC pool cost basis = same minus Spectrum.

**Row 35: BB pool cost basis ($mm/yr).**

```
A35 = "BB pool cost basis ($mm/yr)"

D35 = =INDEX(Starlink!$D:$AC, MATCH("Constellation D&A ($mm)", Starlink!$A:$A, 0), D$5+1)
        * IFERROR(D11 / (D11 + D13), 0)
      + INDEX(Starlink!$D:$AC, MATCH("Ground ops cost ($mm)", Starlink!$A:$A, 0), D$5+1)
        * IFERROR(D11 / (D11 + D13), 0)
      + INDEX(Starlink!$D:$AC, MATCH("Spectrum amortization (BB-only) ($mm)", Starlink!$A:$A, 0), D$5+1)
        [Spectrum amort full attribution to BB pool, no Gbps-weighting.]

copyToRange source D35, destination E35:AC35
```

Format: D35:AC35 currency `$#,##0`.

**Row 38: DTC pool cost basis ($mm/yr).**

```
A38 = "DTC pool cost basis ($mm/yr)"

D38 = =INDEX(Starlink!$D:$AC, MATCH("Constellation D&A ($mm)", Starlink!$A:$A, 0), D$5+1)
        * IFERROR(D13 / (D11 + D13), 0)
      + INDEX(Starlink!$D:$AC, MATCH("Ground ops cost ($mm)", Starlink!$A:$A, 0), D$5+1)
        * IFERROR(D13 / (D11 + D13), 0)
      [No spectrum amort — DTC uses MSS bands per Sprint 4 lock 2026-05-20]

copyToRange source D38, destination E38:AC38
```

#### §3.4.5 At-cost transfer rates (rows 48-55)

**Row 48: BB pool at-cost rate ($/Gbps/yr).**

```
A48 = "BB pool at-cost rate ($/Gbps/yr)"

D48 = =IFERROR(D35 * 1000000 / D11, 0)
      [($mm × 1e6 to $) / Gbps = $/Gbps/yr. IFERROR-0 for D11=0 edge case (pre-deployment).]

copyToRange source D48, destination E48:AC48
```

Format: D48:AC48 currency `$#,##0`.

**Row 50: DTC pool at-cost rate ($/Gbps/yr).**

```
A50 = "DTC pool at-cost rate ($/Gbps/yr)"
D50 = =IFERROR(D38 * 1000000 / D13, 0)
copy
```

---

### §3.5 Per-vehicle marginal IRR engines × 4 (Architecture §5.1)

Four engines on Starlink tab as memo rows 211–218 (italic per Rule 17). Each engine: Spot IRR (current year), Forward IRR (Y+2), Blended IRR = (1−0.7)·Spot + 0.7·Forward. N = 5 yrs sat-module default. CF stream length N+1 = 6.

**Pattern (V2 BB engine; V2 DTC / V3 BB / V3 DTC structurally identical with different per-sat inputs):**

```
A211 = "Memo: V2 BB per-sat cost ($mm/sat) — sat unit cost + facility per sat"
D211 = =D78 + D83
copy to E:AC

A212 = "Memo: V2 BB per-sat net marginal revenue per year ($mm/sat/yr)"
D212 = =(INDEX(Starlink!$D:$AC, MATCH("V2 BB Gbps per sat", Starlink!$A:$A, 0), D$5+1)
        * INDEX('Demand Curves'!$D:$AC, MATCH("Total BB price ($/Gbps/yr)", 'Demand Curves'!$A:$A, 0), D$5+1)
        * INDEX(Assumptions!$D:$AC, MATCH("Utilization % (fleet ramp) — year-row", Assumptions!$A:$A, 0), D$5+1)
        / 1000000)
       * (1 - INDEX(Assumptions!$B:$B, MATCH("Starlink ground ops % of revenue", Assumptions!$A:$A, 0))
              - INDEX(Assumptions!$B:$B, MATCH("Starlink insurance % of revenue", Assumptions!$A:$A, 0))
              - INDEX(Assumptions!$B:$B, MATCH("Starlink other COGS % of revenue", Assumptions!$A:$A, 0)))
       - IFERROR(INDEX(CapEx!$D:$AC, MATCH("Annual Spectrum amortization per sat ($mm/sat/yr)", CapEx!$A:$A, 0), D$5+1), 0)
copy to E:AC

A213 = "Memo: V2 BB Spot IRR"
D213 = =IFERROR(IRR(IF(_xlfn.SEQUENCE(1, INDEX(Assumptions!$B:$B, MATCH("MFW-IRR — Starlink economic life N (years)", Assumptions!$A:$A, 0))+1)=1, -D211, D212)), -1)
copy to E:AC

A214 = "Memo: V2 BB Forward IRR (Y+2)"
D214 = =IFERROR(INDEX($D213:$AC213, 1, D$5+1 + INDEX(Assumptions!$B:$B, MATCH("Forward IRR look-ahead horizon (years)", Assumptions!$A:$A, 0))), -1)
copy to E:AC

A215 = "Memo: V2 BB Blended IRR"
D215 = =(1 - INDEX(Assumptions!$B:$B, MATCH("Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)", Assumptions!$A:$A, 0))) * D213
       + INDEX(Assumptions!$B:$B, MATCH("Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)", Assumptions!$A:$A, 0)) * D214
copy to E:AC
```

**V2 DTC engine (rows 216-220):** identical structure, substituting V2 DTC Gbps per sat (R16), DTC $/Gbps (Demand Curves DTC price), and dropping spectrum amort (DTC uses MSS bands).

**V3 BB engine (rows 221-225):** identical to V2 BB, substituting V3 BB Gbps per sat (R17) + V3 sat cost (R80) + V3 facility cost (R85).

**V3 DTC engine (rows 226-230):** identical to V2 DTC, substituting V3 DTC inputs (R18 + R81 + R86).

All 4 engines × 5 rows each = 20 memo rows at rows 211–230. Each row formatted italic per Rule 17. Number format `$#,##0` for cost/revenue rows; `0.0%` for IRR rows.

---

### §3.6 Allocator OUT contract overwrite (rows 200-210)

Sprint 1 placed literal-0 placeholders at rows 200-210. Sprint 4 overwrites the 10 data rows (200 is the section header) with live formulas. Plugin verifies post-overwrite that all 11 canonical labels still match Architecture §4.2 verbatim.

```
A200: "CENTRAL ALLOCATOR OUTPUTS" (UNCHANGED — Sprint 1 inheritance)

A201: "Total Revenue ($mm)" — value already a label-match per Architecture §4.2
D201 = =D178   (reads Total Revenue from R178 on this tab)
copy to E:AC

A202: "Module EBITDA ($mm)"
D202 = =D181   (reads Module EBITDA from R181)
copy

A203: "Module EBITDA Margin %"
D203 = =D182   (reads Module EBITDA Margin from R182)
copy

A204: "Module FCF ($mm)"
D204 = =D188   (reads Module FCF from R188)
copy

A205: "Module CapEx ($mm)"
D205 = =D98   (reads Module CapEx from R98; equivalently D185)
copy

A206: "Capital deployed ($mm)"
D206 = =D99   (reads Capital deployed from R99)
copy

A207: "Spot IRR"
D207 = =(D11 / (D11 + D13)) * IFERROR((D60 * D213 + D62 * D223) / (D60 + D62), 0)
       + (D13 / (D11 + D13)) * IFERROR((D61 * D218 + D63 * D228) / (D61 + D63), 0)
       [Module-level Spot IRR = BB-Gbps-share-weighted blend of BB pool × DTC pool;
        BB pool = active-sat-weighted V2 BB + V3 BB Spot IRR;
        DTC pool = active-sat-weighted V2 DTC + V3 DTC Spot IRR.
        Per Architecture §5.3 fleet-level IRR is memo-only; this is the diagnostic blend.]
copy

A208: "Forward IRR (Y+2)"
D208 = =(D11 / (D11 + D13)) * IFERROR((D60 * D214 + D62 * D224) / (D60 + D62), 0)
       + (D13 / (D11 + D13)) * IFERROR((D61 * D219 + D63 * D229) / (D61 + D63), 0)
copy

A209: "Blended IRR"
D209 = =(1 - INDEX(Assumptions!$B:$B, MATCH("Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)", Assumptions!$A:$A, 0))) * D207
       + INDEX(Assumptions!$B:$B, MATCH("Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)", Assumptions!$A:$A, 0)) * D208
copy

A210: "Capacity Demand (kg-to-LEO)"
D210 = =D49 + D50
       [V3 BB Starship kg demand + V3 DTC Starship kg demand. V2 BB/DTC use F9 not Starship — not in this row.]
copy
```

**Plugin verifies post-overwrite:** all 11 column-A labels at rows 200-210 match Architecture §4.2 verbatim. All 10 data rows at D:AC produce numeric values (not `#REF!`, `#N/A`, `#NUM!`). The Allocator OUT contract is the Starlink tab's contract with Sprint 10's allocator brain + Sprint 9 Group P&L + Sprint 11 Valuation.

---

## §4 — Verification gate

Any failure → halt, report, push back. No "proceed and document."

### §4.1 Universal checks

- **No formula errors workbook-wide.** Read every cell on every tab; count `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`. **Expected: zero** (except inside IFERROR-wrapped IRR helper cells, which the IFERROR catches).
- **Edge-year reads.** D (2025), I (2030), S (2040), AC (2050) on every load-bearing row. Enumerated in §4.2.
- **Round-trip stability.** Recalc 5 times. Sprint 4's only iterative-calc-touching formula is `D178 = D120 + D131 + D135 + D110 + D143` which references D158/D165/D167 forward references that feed back into D170 then D181 then D182 — all single-pass per Excel dependency tracking, no circularity. **Expected: no key cell moves > $1M across 5 recalcs.**
- **Conservation block on Group P&L** = "OK" every year. Sprint 9 hasn't fired yet so conservation rows R99-R107 still read 0 placeholders → R108 trivially "OK".

### §4.2 Sprint 4 anchor read-back (HALT GATE)

Plugin reads each anchor cell and compares to expected value. Any deviation → halt.

**Calibration anchors (§6.3 Sprint Roadmap):**

| Cell on Starlink tab | Expected 2025 (D) | Tolerance | Halt if |
|---|---|---|---|
| D60 (Active V2 BB sats) | 5,246 | exact | ≠ 5,246 |
| D61 (Active V2 DTC sats) | 650 | exact | ≠ 650 |
| D62 (Active V3 BB sats) | 0 | exact | ≠ 0 |
| D63 (Active V3 DTC sats) | 0 | exact | ≠ 0 |
| D33 (V2 BB launches) | 2,987 | exact | ≠ 2,987 |
| D37 (V2 DTC launches) | 182 | exact | ≠ 182 |
| D39 (V3 BB launches) | 0 | exact | ≠ 0 |
| D41 (V3 DTC launches) | 0 | exact | ≠ 0 |
| D43 (Ratchet flag) | 0 | exact | ≠ 0 |
| D45 (F9 V2 BB launches internal) | ~103 | ±5 | < 95 or > 115 |
| D46 (F9 V2 DTC launches internal) | ~26 | ±3 | < 22 or > 32 |
| D47 (Starship V3 BB launches internal) | 0 | exact | ≠ 0 |
| D48 (Starship V3 DTC launches internal) | 0 | exact | ≠ 0 |
| D49 (V3 BB Starship kg demand) | 0 | exact | ≠ 0 |
| D50 (V3 DTC Starship kg demand) | 0 | exact | ≠ 0 |
| D110 (Starshield revenue) | $2,520M | ±5% | < $2,200M or > $2,900M |
| D120 (BB Revenue) | ~$7,695M | within 2% of (target − $157M DTC) | derived |
| D131 (DTC Revenue) | ~$157M | ±15% | < $80M or > $250M |
| D120 + D131 (Starlink+DTC) | $7,852M | ±5% | < $7,000M or > $8,700M |
| D122 (BB subs) | 5.5-7.5M | range | < 3M or > 10M |
| D153 (Constellation D&A) | $707M | ±10% | < $600M or > $850M (note: stub computes ~$437M — see §3.3.11; if halt fires, Sprint 4.5 retune required) |
| D181 (Module EBITDA) | depends | derived | margin outside 40%-85% |
| D182 (Module EBITDA margin) | 55-75% | range | < 40% or > 85% |
| D178 (Total Revenue) | ~$10.9B | derived | < $10.0B or > $11.5B |
| D207-D209 (Spot/Forward/Blended IRR) | numeric | not `#NUM!` | error or NaN |

**Edge year reads (I=2030, S=2040, AC=2050):**

| Cell | Expected 2030 (I) | Expected 2040 (S) | Expected 2050 (AC) | Tolerance |
|---|---|---|---|---|
| D43→I43 (Ratchet flag) | 1 | 1 | 1 | exact (V3 starts 2026 Base Case → ratchet fires) |
| D33→I33 (V2 BB launches) | 0 | 0 | 0 | exact (ratchet = 1) |
| D37→I37 (V2 DTC launches) | 0 | 0 | 0 | exact (cap flag) |
| D39→I39 (V3 BB launches) | 3,500 | 4,500 | 4,500 | from stub trajectory |
| D52→I52 (V2 BB historical retirement) | 0 | 0 | 0 | year offset 5 >= 5 useful life → 0 |
| D60→I60 (Active V2 BB) | ~3,150 | ~0 | 0 | retirement compounds, decays to 0 by ~2030 |
| D62→I62 (Active V3 BB) | ~9,200 | ~22K | ~22K | running sum of V3 BB launches minus 5-yr deorbits |
| D110→I/S/AC110 (Starshield rev) | ~$1,820M | ~$555M | ~$130M | decay-driven; sanity bracket |

### §4.3 Stale-reference scan (Rule 22)

Plugin runs MATCH calls on the six canonical Starlink labels Sprint 3 IFERROR-0 reads consume, plus the four Starlink Capacity labels Sprint 5 will consume:

1. `MATCH("F9 V2 BB launches (internal)", Starlink!$A:$A, 0)` resolves.
2. `MATCH("F9 V2 DTC launches (internal)", Starlink!$A:$A, 0)` resolves.
3. `MATCH("Starship V3 BB launches (internal)", Starlink!$A:$A, 0)` resolves.
4. `MATCH("Starship V3 DTC launches (internal)", Starlink!$A:$A, 0)` resolves.
5. `MATCH("V3 BB Starship kg demand", Starlink!$A:$A, 0)` resolves.
6. `MATCH("V3 DTC Starship kg demand", Starlink!$A:$A, 0)` resolves.
7. `MATCH("BB pool at-cost rate ($/Gbps/yr)", 'Starlink Capacity'!$A:$A, 0)` resolves.
8. `MATCH("DTC pool at-cost rate ($/Gbps/yr)", 'Starlink Capacity'!$A:$A, 0)` resolves.
9. `MATCH("BB Gbps available for external Starlink revenue", 'Starlink Capacity'!$A:$A, 0)` resolves.
10. `MATCH("DTC Gbps available for external Starlink revenue", 'Starlink Capacity'!$A:$A, 0)` resolves.

Plugin also verifies Patch B Launch Capacity R64 now reads non-zero from Starlink labels (Sprint 4 published them) and Customer Launch R22/R68/R69 same. Read R64 in Launch Capacity at D, I, S, AC — should now show F9 launches incorporating V2 BB/DTC internal launches (D = 38.58 + 103 + 26 = ~167 vs Sprint 3 V2.5 IFERROR-0 state of 38.58 alone). Halt if Launch Capacity R64 didn't update.

### §4.4 Halt conditions (quantitative)

Plugin halts and reports if:

- Any anchor in §4.2 deviates beyond tolerance.
- Any error value (`#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`) anywhere in the workbook except inside IFERROR-wrapped cells.
- Any canonical label MATCH in §4.3 fails to resolve.
- Round-trip stability fails (cell value drifts > $1M across 5 recalcs).
- Constellation D&A 2025 outside ±10% of $707M → halt + push back to spec author for retune (likely add legacy V1/V1.5 D&A or facility D&A separately).
- Starlink+DTC revenue 2025 outside ±5% of $7,852M → halt + push back; check Demand Curves V9 anchor.
- Starshield revenue 2025 outside ±5% of $2,520M → halt + push back; check R94 Starshield Reserved % start + R97 $/Gbps + R103 calculation.
- Total active sats end-2025 ≠ 5,896 (V2 BB + V2 DTC, excluding legacy) → halt; indicates active fleet formula error.
- Module EBITDA margin outside 40-85% range → halt; indicates COGS mismatch.

### §4.5 Verification log (plugin produces in chat)

```
Sprint 4 verification log
=========================

Workbook: SpaceX Model V2.6.xlsx
Sprint 3 / Sprint 2 / Sprint 1 / Sprint 0 inheritance: PASS

Assumptions amendments (12 new rows): PASS
  - V3 BB first launch year = 2026 (MC discrete [2026,2027])
  - V3 DTC first launch year = 2028 (MC discrete [2027,2028])
  - V2 DTC permanent cap flag = 1 (Vlad lock)
  - Starlink ground ops % = 4%; insurance % = 1%; other COGS % = 2%
  - V3 BB / V3 DTC launches per year stub trajectories
  - Sats per F9 launch — V2 BB = 29; V2 DTC = 7
  - Sats per Starship launch — V3 BB = 60; V3 DTC = 15

Starlink tab body (rows 11-199): PASS
  - 8 logical sections with section + subsection headers
  - 6 canonical Sprint 3 IFERROR-0 labels published at rows 45-50
  - Active fleet year-rows year-chained (Rule 23 exceptions documented)
  - V2/V3 ratchet flag at R43 (year-chained latch)
  - Per-vehicle CapEx at R88-R99 (Sat CapEx no lag; Facility CapEx 1-yr ahead via Vlad lock 2026-05-20)
  - Starshield revenue at R110 = $2,520M ±5% (calibration PASS)
  - BB Revenue + DTC Revenue at R120 + R131 = $7,852M ±5% (calibration PASS)
  - Constellation D&A at R153 = $707M ±10% (verify or halt + retune)
  - Module P&L at R178-R188 (vending-machine, no R&D/SG&A/overhead/taxes)

Starlink Capacity tab (rows 4-55): PASS
  - 5 subsections built end-to-end
  - 10 canonical labels published for Sprint 5 ODC + Starlink tab reads
  - ODC BB/DTC Gbps demand reads = $0 throughout (IFERROR-0, ODC not yet fired)
  - BB pool at-cost rate + DTC pool at-cost rate computed

Per-vehicle IRR engines (4 of 4): PASS
  - V2 BB Spot/Forward/Blended at rows 213-215
  - V2 DTC at rows 218-220
  - V3 BB at rows 223-225
  - V3 DTC at rows 228-230
  - All IFERROR-wrapped; all return numeric values

Allocator OUT contract overwrite (rows 200-210): PASS
  - 11 canonical labels intact per Architecture §4.2
  - Module-level Spot/Forward/Blended IRR at R207/R208/R209 (Gbps-share weighted blend)
  - Capacity Demand (kg-to-LEO) at R210 = V3 BB kg demand + V3 DTC kg demand

§4.1 universal checks: error scan 0/0/0/0/0/0/0; round-trip stability PASS
§4.2 calibration anchors: all within tolerance (Constellation D&A flagged if outside)
§4.3 stale-ref scan: all 10 canonical MATCH calls resolve; Launch Capacity R64 + Customer Launch R22/R68/R69 now read non-zero

Status: PASS → write Claude Log entry → leave workbook for Vlad to save.
```

---

## §5 — Claude Log entry

Plugin appends to `Claude Log` row 6 (after §4 passes):

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| 2026-MM-DD | 4 | Starlink, Starlink Capacity, Assumptions (12 new rows), Claude Log | Built Starlink module body end-to-end (rows 11-199) + Starlink Capacity tab full build. Published 6 canonical labels Sprint 3 IFERROR-0 reads consume (F9 V2 BB/DTC launches internal, Starship V3 BB/DTC launches internal, V3 BB/DTC Starship kg demand). 4 per-vehicle marginal IRR engines (V2 BB, V2 DTC, V3 BB, V3 DTC). V2/V3 ratchet year-chained latch. V2 DTC permanent cap flag (Vlad lock 2026-05-20). V2 historical fleet linear retirement over 5 yrs. Bandwidth-driven external revenue (subs derived). Q4'25 Starshield mechanic. CapEx Lag R82=1 yr applied to FACILITIES not sats per Vlad lock. Calibration: Starlink+DTC $7,852M ±5% PASS; Starshield $2,520M ±5% PASS; Active V2 BB 5,246 + V2 DTC 650 exact; V2 BB/DTC launches 2,987/182 exact; V3 launches 0 exact; Constellation D&A $707M ±10% [PASS/RETUNE]. | Sprint 4.5 candidate items: (1) Constellation D&A calibration retune if §4.4 halt fires (add legacy V1/V1.5 + facility D&A); (2) Wright's Law on V3 BB Gbps-per-sat (deferred — flat at $1000/sat for Sprint 4); (3) Total active sats target $9,800$ excludes legacy V1/V1.5 head count from current sum (D65 = 5896). | Sprint 5: ODC module (per-sat IRR, dual revenue Model A + Model B, cash-driven deployment, bandwidth services cost paid to Starlink reads `BB/DTC pool at-cost rate ($/Gbps/yr)`, internal compute split to AI Stack, ODC publishes `ODC BB Gbps demand` + `ODC DTC Gbps demand` labels that Starlink Capacity IFERROR-0 reads activate). |

Date column populated by plugin with actual execution date.

---

## §6 — Don't touch (out of scope)

- No module body content on any of the 4 OTHER module tabs (Customer Launch, ODC, AI Stack, Lunar Mars). Sprint 5/6/7.
- No Allocator computation logic. Sprint 10.
- No Group P&L walk above row 99 (Revenue → COGS → EBITDA → D&A → EBIT → Taxes → NOPAT → CapEx → FCF). Sprint 9.
- No OpEx / CapEx tab content (R&D by module, SG&A by function, Mars/Moon R&D year-row, module CapEx aggregation, corporate CapEx, spectrum CapEx, corporate D&A). Sprint 8. Sprint 4 reads CapEx!`Annual Spectrum amortization ($mm/yr)` with IFERROR-0.
- No Valuation tab content. Sprint 11.
- No MC engine. Sprint 12.
- No edits to Assumptions tab inputs other than the 12 new amendments in §3.2 (R74-R142 Starlink inputs locked from Sprint 0; if any value is wrong, file a Sprint 0.5 patch — do not edit in this sprint).
- No edits to Customer Launch tab (Sprint 3's canonical labels stand).
- No edits to Launch Capacity tab (Sprint 2 + Patch B in Sprint 3 stand; Sprint 4 publishes Starlink labels that Patch B R64 already reads via IFERROR-0).
- No edits to Allocator tab (Sprint 1 shell unchanged; Sprint 10 fills).
- No edits to Demand Curves tab (V9 inheritance — read-only).
- No edits to Claude Log rows 1-5 (prior sprint entries locked).
- No row insertions anywhere (Rule 10).
- No plugin-issued save commands.
- No styling beyond: white-on-charcoal section-header fills on Starlink R12 + Starlink Capacity R8; italic light-grey fill on subsection headers; italic on per-vehicle IRR memo rows (R211-R230); bold + currency formats on data rows.

---

## §7 — Open thread (post-sprint considerations)

### §7.1 Constellation D&A calibration

If Sprint 4 §4.4 fires the Constellation D&A halt (target $707M ±10%), Sprint 4.5 retune options:
1. **Add legacy V1/V1.5 D&A as a memo line** — Q4'25 implies ~$130M legacy D&A. Add as separate Starlink tab row.
2. **Add facility D&A as a memo line** — Sprint 8 will own this on CapEx tab, but Sprint 4 can add a placeholder. Q4'25 implies ~$140M facility D&A.
3. **Recalibrate $/kg/yr dep rate** — Sprint 0 R100 = $128.8 anchored to Q4'25 R194; Sprint 4.5 may need to bump to ~$200/kg/yr if Q4'25 R194 was per-V2-sat not per-kg.

### §7.2 V3 BB Wright's Law on bandwidth per sat

Sprint 4 deferred V3 BB bandwidth-per-sat learning curve (held flat at 1,000 Gbps). Sprint 4.5 patch candidate: implement WL on R17 using cum V3 BB sats running sum.

### §7.3 Total active sat count diagnostic

D65 = 5,896 active V2 sats; target ~9,800 includes legacy V1/V1.5 head count (~3,900). Add legacy V1/V1.5 head count year-row to Starlink tab as memo for diagnostic alignment with Q4'25 R99.

### §7.4 BB/DTC Available Gbps demand-side sanity

If Demand Curves V9 anchors `Total BB price ($/Gbps/yr)` × `BB Gbps available for external` produces 2025 BB revenue outside the $7,695M target (Starlink+DTC $7,852M − DTC $157M), the upstream Demand Curves tab needs inspection. Likely root cause: V9's $/Gbps anchor may be priced for the V2 era when BB Gbps was scarce (high $/Gbps) and not reflect future ARPU compression. Sprint 4 publishes a `Memo: BB Revenue / Available BB Gbps` diagnostic row for inspection.

### §7.5 Internal bandwidth revenue lights up in Sprint 5

`Starlink internal bandwidth revenue ($mm)` at R143 resolves to $0 throughout horizon at Sprint 4 exit because ODC tab has only Sprint 1 shell. Sprint 5 publishes `ODC BB Gbps demand` + `ODC DTC Gbps demand` year-rows → Starlink Capacity R18 + R20 IFERROR-0 reads activate → R143 reads non-zero values. Sprint 5 verification gate should confirm R143 starts producing $mm values in years after V3 BB online (since ODC bandwidth demand depends on ODC fleet which depends on V3 BB launches via cash queue).

### §7.6 Per-vehicle IRR pool blending

Allocator OUT R209 Blended IRR is computed as Gbps-share-weighted blend of BB pool × DTC pool, each pool active-sat-weighted across vehicles. This is Sprint 4's diagnostic blend. Sprint 10 allocator brain may switch to using individual vehicle Blended IRRs directly for the cash/kg sigmoid allocation (not the pool blend). If so, Sprint 10 spec must reference rows 215/220/225/230 (per-vehicle Blended IRRs) by their memo-row labels.

### §7.7 Sprint 3.5 parallel chat coordination

Sprint 3.5 patch (Customer Launch per-launch IRR reformulation at R131/R141) does not affect Sprint 4 reads. If Sprint 3.5 has landed before Sprint 4 plugin fires, Sprint 4 plugin sees the new per-launch IRR formulation but uses none of Customer Launch's IRR rows. Sprint 4 spec author confirms Customer Launch R22/R24/R25/R68/R69/R70 unchanged from Sprint 3 V2.5 state before plugin executes (per §3.0 pre-flight #11).

### §7.8 Demand Curves V9 label-string pre-flight risk

§3.0 pre-flight #7 checks four canonical Demand Curves labels. If V9 uses different strings (e.g., `BB demand` vs `Total BB Gbps demand (Gbps/yr)`), plugin halts. Vlad has three resolution options per §3.0 #7. Recommended: rename V9 labels to canonical strings, since V9 tab is read-only carryover and label discipline is load-bearing (Principle 14).

---

## §8 — Execution sequence (plugin runs in this order)

Save commands NOT in this sequence — Vlad handles all saving.

1. **Pre-flight checks** (§3.0 — 13 items): confirm target workbook open + correctly named, Sprint 0/1/2/3 baseline intact, Demand Curves V9 labels resolve, Assumptions §5 + Customer Launch + Launch Capacity canonical labels resolve, Sprint 0 anchor spot-checks pass.

2. **Assumptions amendments** (§3.2 — 12 new rows): append below last-used row. For each row execute 7 discrete writes (label, Base Case or year-row values, notes, MC Min, MC Max, MC Distribution, MC Notes). Total: 12 × 7 = 84 writes.

3. **Starlink tab section + subsection headers** (§3.3.0): 9 SECT/SUB rows written one at a time per Rule 1.

4. **Starlink tab body** (§3.3.1 through §3.3.12) — bandwidth supply → vehicle deployment → ratchet → canonical launch labels (six published here) → canonical kg demand labels → active fleet → per-vehicle CapEx → Starshield revenue → external revenue (BB + DTC + terminal) → internal bandwidth revenue → COGS → Module P&L. Each row: label first, D-column anchor formula second, copyToRange E:AC third. After each major block (e.g., post §3.3.4 canonical labels), read D / I / S / AC to verify per §4.2.

5. **Starlink Capacity tab body** (§3.4) — 5 subsections: total active Gbps → ODC internal claim placeholders → available bandwidth → pool cost basis → at-cost transfer rates. Same per-row pattern.

6. **Per-vehicle IRR engines** (§3.5) — V2 BB → V2 DTC → V3 BB → V3 DTC. 5 memo rows each. Format italic.

7. **Allocator OUT contract overwrite** (§3.6) — rows 201-210 D-column formula + copyToRange. Verify Architecture §4.2 11 canonical labels intact.

8. **Run §4 verification gate** against live workbook:
   - §4.1 universal checks
   - §4.2 anchor read-back (halt if any tolerance miss)
   - §4.3 stale-ref scan (halt if any MATCH fails)
   - §4.4 halt thresholds (halt if any fires)
   - Round-trip stability (5x recalc)

9. **Write Claude Log Sprint 4 entry** (§5) — row 6 of Claude Log tab, 6 columns.

10. **Produce verification log** in chat (§4.5 format). Done. Vlad saves the workbook.

**Estimated discrete writes:** ~250-300 (12 Assumptions amendments × 7 = 84; Starlink tab ~120; Starlink Capacity ~50; IRR engines ~20; Allocator OUT ~10; Claude Log 1). Day budget: 1.5 days.

---

## §9 — Amendment log

- **2026-05-20 (initial draft)** — Sprint 4 spec drafted by spec-author chat after surfacing 7 architectural questions via AskUserQuestion (revenue mechanic, Starshield mechanic, V2/V3 ratchet, V2 retirement, IRR pattern, Starlink Capacity labels, CapEx Lag). Vlad-locked all 7 with two material additions to Architecture §8.2 ratchet (V2 DTC permanent cap from end-2025; V3 BB first launch year + V3 DTC first launch year as MC inputs) and one material clarification to CapEx Lag (R82=1 yr applies to facilities, not sat CapEx). Scope: Starlink module body + Starlink Capacity tab + 4 per-vehicle IRR engines + Allocator OUT overwrite. Publishes 6 canonical labels Sprint 3 Patch B + Customer Launch IFERROR-0 reads consume. Self-contained per standing process rule 1 (no external XLSX or MD reads required during execution). Calibration anchored to §6.3 Sprint Roadmap targets ($7,852M Starlink+DTC, $2,520M Starshield, $707M Constellation D&A, exact fleet anchors).

