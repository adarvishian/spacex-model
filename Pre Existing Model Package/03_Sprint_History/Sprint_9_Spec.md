# Sprint 9 — Group P&L full walk + inter-module eliminations + R99-R109 conservation block + R109 cash flow identity (Mars carve-out as real cash drain) + revised §6.8 calibration targets

**Day budget**: 1 day (per Sprint Roadmap §1)
**Owner**: Sprint 9 (this chat = spec author; separate fresh chat will execute as plugin)
**Status**: Spec authoring 2026-05-22. Constitutional docs + Sprint 0/1/7/8/8.5 read; pre-flight MATCH probes pass against V2.10; pre-compute against §6.8 surfaces big architectural calibration delta; 5 Vlad architectural locks captured (Mars carve-out = real cash drain; Architecture §11.4 deferred to Sprint 10/11; R106 + R107 formula-now both sides; G&A + Other rewire to Group P&L net; revised §6.8 targets to rebuild reality). Sprint 6 (AI Stack) still deferred — IFERROR-0 wraps applied throughout.

---

## §0 — Constitutional references

- `01_Lessons_Learned.md`:
  - **Principle 1** (postponed architectural decisions create retrofit cascades) — Sprint 9 closes 4 architectural locks day-one; §11.4 deferred to Sprint 10/11 with explicit thread carried.
  - **Principle 3** (Allocator IN/OUT by label, not row) — Sprint 9 reads modules + OpEx + CapEx via INDEX/MATCH on canonical labels.
  - **Principle 4** (queue gate reserves non-module claims before module CapEx) — Sprint 9 publishes `Taxes ($mm)` canonical row that Sprint 10 Queue Gate consumes.
  - **Principle 8** (vending-machine — module COGS direct production only) — Sprint 9 is the CONSOLIDATION + R&D/SG&A/Tax landing zone. Confirms NO module tab has R&D/SG&A/Tax.
  - **Principle 9** (internal transfers count gross at module IRR; eliminate at Group) — Sprint 9 IS the elimination layer (R42-R44 area on Group P&L).
  - **Principle 10** (module tabs owned by module sprints; cross-cutting specs only read) — Sprint 9 writes ONLY to Group P&L + OpEx (2 cells per Lock d rewire). No module writes. No CapEx writes.
  - **Principle 11** (zero OFFSET formulas) — all dynamic ranges INDEX-based.
  - **Principle 12 / Rule 23** (anchor-and-offset for ramps) — Sprint 9 has NO new ramps. Year-chained Rule 23 EXCEPTIONS flagged inline: (a) R109 cash flow identity cumulative sums (Σ IPO, Σ Group FCF, Σ Group CapEx, Σ carve-out, Cash EoY running balance — all year-chained).
  - **Principle 14** (cross-tab refs by label) — every read uses INDEX(Tab!D:D, MATCH("Label", Tab!$A:$A, 0)).
  - **Principle 18** (MC ranges at input creation) — N/A; Sprint 9 adds zero new Assumptions amendments (Taxes derived; cash flow params already on Assumptions from Sprint 0).
  - **Principle 19 / Rule 15** (sanity check halt thresholds) — §4.6 calibration table specifies halt thresholds for Group Revenue, Group EBITDA, Group D&A, Group FCF, conservation R108="OK".
  - **Principle 20 / Rule 16** (edge-year reads) — D/I/S/AC on every section.
  - **Principle 21 / Rule 22** (stale-ref scan) — §4.5 scans 7 canonical labels Sprint 9 publishes against Sprint 10 + Sprint 11 downstream readers.
  - **Principle 22** (within-year cycle deliberate + iterative calc bistability) — Sprint 9 introduces NEW within-year cycle: Group FCF → Allocator R34 prior-year Group FCF read → Mars carve-out → Lunar Mars Module CapEx → CapEx tab → Group CapEx → Group FCF. Per Architecture §11.1 Mars carve-out uses PRIOR-year FCF (breaks within-year loop). Iterative calc remains ON workbook-wide (100 iter / 0.001 tol).
  - **Principle 23** (calibration anchored) — Sprint 9 hits REVISED Roadmap §6.8 targets per Vlad lock 2026-05-22: Group Revenue $14,650M ±5% (unchanged); Group EBITDA $4,904M ±5% (revised from $8,690M); Group D&A $1,261M ±10% (revised from $1,060M); Group FCF −$2,569M ±10% (revised from $3,670M); conservation R108="OK" every year (unchanged, mandatory).

- `02_Architecture_and_Methodology.md`:
  - **§1** (tab inventory) — Group P&L = tab #10. OpEx = #11. CapEx = #12.
  - **§3** (vending-machine framing) — Group P&L is the LANDING ZONE for R&D/SG&A/Tax/Group D&A.
  - **§3 labeling note** (added 2026-05-20) — Module EBITDA = Gross Profit mathematically; Group P&L walk treats Module D&A as already in COGS (Architecture §15.1 walk gives non-traditional EBITDA).
  - **§7** (internal transfer mechanics — 4-step pattern) — Sprint 9 implements Step 3 (elimination at Group P&L) for all 3 internal flows (launch services, bandwidth, compute) + Step 4 (conservation check rows R105, R106, R107).
  - **§7.1** (Customer Launch ↔ consumers launch services) — fully-allocated rate; Sprint 9 elim R42 reads Customer Launch R70.
  - **§7.2** (ODC ↔ Starlink bandwidth) — fully-allocated; Sprint 9 elim R43 reads Starlink internal bandwidth rev + ODC bandwidth services cost (both = $0 in 2025; activates 2030+).
  - **§7.3** (ODC ↔ AI Stack compute) — fully-allocated; Sprint 9 elim R44 reads ODC internal transfer rev + AI Stack internal compute cost (both = $0 until Sprint 6 lands).
  - **§11.1** (Mars/Moon strategic carve-out) — uses PRIOR-year FCF; breaks within-year cycle.
  - **§15.1** (Group P&L walk — VERBATIM load-bearing) — Sprint 9 implements verbatim.
  - **§15.2** (conservation block R99-R109) — Sprint 9 ACTIVATES live conservation formulas (Sprint 1 set up literal-0 placeholders).
  - **§17** (calibration targets) — Sprint 9 hits REVISED §6.8 targets per Vlad lock 2026-05-22.

- `03_Sprint_Roadmap_and_Verification.md`:
  - **§3 Sprint 9** scope (full walk + conservation + eliminations).
  - **§6.8 Sprint 9 calibration** — Vlad-revised 2026-05-22 to reflect rebuild architecture. Original Q4'25 raw anchors retained as memo rows for archaeology.
  - **§5 universal verification protocol** — #REF/#NUM scan, conservation R108="OK", edge-year reads D/I/S/AC, round-trip stability <10 iter, stale-ref scan, Claude Log entry.

- `Model Execution Rules.md` — Rule Compliance Preamble below.

- `2025 Anchors from Q4_25.md` — §7 Q4'25 calibration targets retained as MEMO archaeology rows; Sprint 9 §3.5 publishes them alongside REVISED targets.

- `Sprint_1_Spec.md` §3.5 — Group P&L conservation block trivial-state setup at rows 99-109. Sprint 9 ACTIVATES.

- `Sprint_7_Spec.md` §7 Open Thread 1 (carve-out vs Module CapEx gap pre-2028) — Sprint 9 resolves: real cash drain.

- `Sprint_8_Spec.md` §9 Amendment 6 (pre-2028 carve-out gap = real cash drain) — Sprint 9 codifies in R109.

- `Sprint_8.5_Patch.md` — confirms Sprint 8.5 landed (OpEx R53 D=$4,559.67M); Sprint 9 reads by canonical label.

---

## §1 — Rule Compliance Preamble (mandatory)

- [x] **Rule 1** (one concept per write) — §3 separates Group P&L walk rows (§3.1), inter-module eliminations block (§3.2), conservation block activation (§3.3), R109 cash flow identity (§3.4), §6.8 calibration target revision memo rows (§3.5), OpEx R46 + R49 rewire to Group P&L net (§3.6). Each cell-block is a discrete write per Rule 1; labels, formulas, formats split.
- [x] **Rule 3 / 23** (formula pattern) — Sprint 9 has NO new ramps. Year-chained Rule 23 EXCEPTIONS flagged inline at §3.4: (a) Σ Group FCF cumulative running sum (R109 cash identity); (b) Σ Total Group CapEx cumulative; (c) Σ strategic carve-out cumulative; (d) Σ IPO cumulative; (e) Cash EoY running balance. All use `IF(D$5=0, init, INDEX($D{row}:$AC{row}, 1, D$5)+this_year)` pattern with INDEX col_num<1 guard per memory `feedback-index-col-zero-spills`.
- [x] **Rule 4** (verification gate) — every section has explicit read-back D / I / S / AC + expected values per §4.2 + §4.6.
- [x] **Rule 6** (inline formulas) — every cell write specified with full Excel formula. No "see Architecture §15.1" hand-waves. INDEX/MATCH calls written verbatim case-sensitive (pre-flight MATCH probes confirmed against V2.10 workbook).
- [x] **Rule 10** (no row insertions) — §3.1-§3.4 fill BLANK rows 7-109 on Group P&L tab (Sprint 1 wrote only row 6 title + R99-R109 placeholders; Sprint 9 OVERWRITES placeholders R99-R109 with live formulas + fills R7-R98 with walk + elims). §3.5 calibration memo rows append at R111-R125 (below conservation block). §3.6 OpEx R46 + R49 formula REPLACEMENT (not insertion).
- [x] **Rule 11** (touch points) — every line item enumerates SUM range / aggregator / conservation check / downstream consumer in §3 inline. 7 canonical labels Sprint 9 publishes enumerate Sprint 10 + Sprint 11 readers in §9.
- [x] **Rule 12** (label-based cross-tab refs) — every cross-tab read uses `INDEX(Tab!D:D, MATCH("Canonical Label", Tab!$A:$A, 0))` with year-row indexing `D$5+1`. Zero hardcoded row refs.
- [x] **Rule 13** (vending-machine test) — Sprint 9 writes ONLY Group P&L tab + OpEx R46 + R49. NO module tab writes. Confirms vending-machine framing: R&D/SG&A/Tax land at Group, NOT modules.
- [x] **Rule 14** (no hardcoded constants) — Tax rate read from Assumptions R3 by canonical label `Tax rate (corporate, US federal + state blended)`; Starting cash from R8 `Starting cash position EoY 2024 ($mm)`; IPO amount from R9 `IPO injection amount ($mm)`; IPO year from R10 `IPO injection year`. Calibration memo numbers (revised targets) hardcoded in §3.5 memo rows with documented Vlad lock 2026-05-22 — Rule 14 exception per Sprint 8.5 precedent (calibration anchors hardcoded as memo rows for diagnostic display).
- [x] **Rule 15** (sanity check halt thresholds) — §4.6 calibration table specifies revised quantitative halt thresholds per Vlad lock 2026-05-22: Group Revenue $14,650M ±5% [$13,917M, $15,382M]; Group EBITDA $4,904M ±5% [$4,659M, $5,149M] (REVISED); Group D&A $1,261M ±10% [$1,135M, $1,387M] (REVISED); Group FCF −$2,569M ±10% [−$2,312M, −$2,826M] (REVISED); conservation R108="OK" every year (mandatory). Original Q4'25 targets retained as memo rows for archaeology, NOT as halt thresholds.
- [x] **Rule 19** (save-as) — N/A per standing rules locked 2026-05-20 (`feedback-no-workbook-names-in-specs`): spec does NOT name workbook files; Vlad handles versioning entirely outside the spec.
- [x] **Rule 22** (stale-ref scan) — §4.5 lists 5 scan checkpoints: (1) Sprint 1 R99-R109 placeholder labels intact (overwrite preserves labels); (2) All module R201/R202/R204/R205 canonical labels resolve; (3) Sprint 8 R37/R41/R45/R53 + Sprint 7 Allocator R35 + Customer Launch R70 + Starlink R120/R131 + Assumptions R3/R8/R9/R10 canonical labels resolve; (4) 7 new canonical labels Sprint 9 publishes verbatim against §9 downstream-reader table; (5) OpEx R57 memo retained (now memo-only — Lock d rewires R46 + R49 away from R57; R57 kept for diagnostic display).

Architecture & Methodology compliance:
- [x] Module P&L follows vending-machine framing (Architecture §3) — Sprint 9 doesn't write modules; reads them by canonical label only.
- [x] Per-sat / per-launch marginal IRR (Architecture §5) — N/A (Sprint 9 doesn't touch IRR engines).
- [x] Allocator OUT contract uses canonical 11 labels (Architecture §4.2) — Sprint 9 reads module R201/R202/R204/R205 + Lunar Mars R211/R212 BV memo rows.
- [x] Year-offset helper row at row 5 + year header at row 4 on every tab — Sprint 0 wrote on Group P&L tab; §3.0 pre-flight confirms.
- [x] ZERO `OFFSET()` formulas — all dynamic ranges INDEX-based. R109 cash identity year-chained running sums use INDEX($D{row}:$AC{row}, 1, D$5) with IF guard.

---

## §1.5 — Pre-execution setup

Per standing rules locked 2026-05-20 (`feedback-no-workbook-names-in-specs`): plugin operates on whatever workbook is open in Vlad's Excel session. Vlad handles versioning. Spec omits all workbook filename references.

Plugin §3.0 pre-flight (described below) confirms:

1. **Tab positions and existence** — 15 tabs in order: `Assumptions`, `Allocator`, `Launch Capacity`, `Customer Launch`, `Starlink`, `Starlink Capacity`, `ODC`, `AI Stack`, `Lunar Mars`, `Group P&L`, `OpEx`, `CapEx`, `Valuation`, `Demand Curves`, `Claude Log`. Group P&L at position #10. Sprint 9 only writes to Group P&L + OpEx (2 cells).

2. **Iterative calc still enabled workbook-wide** — 100 iterations, 0.001 tolerance. Per memory `project-iterative-calc-enabled-2026-05-20`. Sprint 9 introduces ONE within-year cycle: Group FCF → Allocator R34 prior-year Group FCF read → Mars carve-out R35 → Lunar Mars Module CapEx R205 (read via CapEx tab R15 → CapEx R17 → CapEx R45 → Group P&L) → Group FCF. PRIOR-year FCF reference (Allocator R34) breaks the within-year part; the cycle is cross-year and trivially converges. Halt if iterative calc OFF.

3. **Sprint 8.5 PASS confirmed** — pre-flight reads `OpEx!D53` (Total OpEx 2025). Expected ≈ $4,559M. Halt if outside [$4,500M, $4,620M].

4. **Sprint 8 + Sprint 7 PASS confirmed** — pre-flight reads `Allocator!D35` (Mars carve-out 2025 = $1,000M floor) + `CapEx!D45` (Total Group CapEx 2025 ≈ $6,345M) + `CapEx!D37` (Total Corporate D&A 2025 ≈ $120M) + `CapEx!D41` (Annual spectrum amortization 2025 ≈ $333M).

5. **Sprint 6 deferred — AI Stack reads via IFERROR-0** — `MATCH("Total Revenue ($mm)", 'AI Stack'!$A:$A, 0)` returns R201 but Sprint 1 placeholder = 0. All AI Stack reads in Sprint 9 wrap IFERROR-0.

6. **Pre-flight MATCH probes — Sprint 9 reads** (all confirmed PASS against V2.10 workbook 2026-05-22):
   - `MATCH("Total Revenue ($mm)", Starlink!$A:$A, 0)` → R201 ✓
   - `MATCH("Total Revenue ($mm)", 'Customer Launch'!$A:$A, 0)` → R201 ✓
   - `MATCH("Total Revenue ($mm)", ODC!$A:$A, 0)` → R201 ✓
   - `MATCH("Total Revenue ($mm)", 'AI Stack'!$A:$A, 0)` → R201 ✓ (Sprint 1 placeholder = 0)
   - `MATCH("Total Revenue ($mm)", 'Lunar Mars'!$A:$A, 0)` → R201 ✓
   - `MATCH("Module EBITDA ($mm)", Starlink!$A:$A, 0)` → R202 ✓
   - `MATCH("Module EBITDA ($mm)", 'Customer Launch'!$A:$A, 0)` → R202 ✓
   - `MATCH("Module EBITDA ($mm)", ODC!$A:$A, 0)` → R202 ✓
   - `MATCH("Module EBITDA ($mm)", 'AI Stack'!$A:$A, 0)` → R202 ✓
   - `MATCH("Module EBITDA ($mm)", 'Lunar Mars'!$A:$A, 0)` → R202 ✓
   - `MATCH("Module FCF ($mm)", Starlink!$A:$A, 0)` → R204 ✓
   - `MATCH("Module FCF ($mm)", 'Customer Launch'!$A:$A, 0)` → R204 ✓
   - `MATCH("Module FCF ($mm)", ODC!$A:$A, 0)` → R204 ✓
   - `MATCH("Module FCF ($mm)", 'AI Stack'!$A:$A, 0)` → R204 ✓
   - `MATCH("Module FCF ($mm)", 'Lunar Mars'!$A:$A, 0)` → R204 ✓
   - `MATCH("Module CapEx ($mm)", Starlink!$A:$A, 0)` → R205 ✓
   - `MATCH("Module CapEx ($mm)", 'Customer Launch'!$A:$A, 0)` → R205 ✓
   - `MATCH("Module CapEx ($mm)", ODC!$A:$A, 0)` → R205 ✓
   - `MATCH("Module CapEx ($mm)", 'AI Stack'!$A:$A, 0)` → R205 ✓
   - `MATCH("Module CapEx ($mm)", 'Lunar Mars'!$A:$A, 0)` → R205 ✓
   - `MATCH("Customer Launch internal transfer revenue ($mm)", 'Customer Launch'!$A:$A, 0)` → R70 ✓
   - `MATCH("Constellation D&A ($mm)", Starlink!$A:$A, 0)` → R153 ✓
   - `MATCH("Module D&A ($mm) — informational (also in COGS rows 86 + 88)", 'Customer Launch'!$A:$A, 0)` → R100 ✓ (or alt label per Sprint 3 publication)
   - `MATCH("Annual sat D&A ($mm/yr)", ODC!$A:$A, 0)` → R106 ✓
   - `MATCH("BV depreciation — Lunar ($mm/yr)", 'Lunar Mars'!$A:$A, 0)` → R117 ✓
   - `MATCH("BV depreciation — Mars ($mm/yr)", 'Lunar Mars'!$A:$A, 0)` → R118 ✓
   - `MATCH("Lunar Accumulated Book Value ($mm)", 'Lunar Mars'!$A:$A, 0)` → R211 ✓
   - `MATCH("Mars Accumulated Book Value ($mm)", 'Lunar Mars'!$A:$A, 0)` → R212 ✓
   - `MATCH("Total OpEx ($mm)", OpEx!$A:$A, 0)` → R53 ✓
   - `MATCH("Total Module CapEx ($mm)", CapEx!$A:$A, 0)` → R17 ✓
   - `MATCH("Total Group CapEx ($mm)", CapEx!$A:$A, 0)` → R45 ✓
   - `MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0)` → R37 ✓
   - `MATCH("Annual spectrum amortization ($mm)", CapEx!$A:$A, 0)` → R41 ✓
   - `MATCH("Vehicle build claim ($mm) — placeholder for Sprint 10", CapEx!$A:$A, 0)` → R44 ✓
   - `MATCH("Mars/Moon strategic carve-out ($mm/yr)", Allocator!$A:$A, 0)` → R35 ✓
   - `MATCH("BB Revenue ($mm)", Starlink!$A:$A, 0)` → R120 ✓
   - `MATCH("DTC Revenue ($mm)", Starlink!$A:$A, 0)` → R131 ✓
   - `MATCH("Tax rate (corporate, US federal + state blended)", Assumptions!$A:$A, 0)` → R3 ✓ (value 0.21)
   - `MATCH("Starting cash position EoY 2024 ($mm)", Assumptions!$A:$A, 0)` → R8 ✓ (value $5,000M)
   - `MATCH("IPO injection amount ($mm)", Assumptions!$A:$A, 0)` → R9 ✓ (value $30,000M)
   - `MATCH("IPO injection year", Assumptions!$A:$A, 0)` → R10 ✓ (value 2027)
   - Halt on any #N/A — Sprint 1/3/4/5/7/8/8.5 may have drifted; Sprint 9 doesn't restore.

7. **Sprint 1 R99-R109 placeholder labels intact** — pre-flight reads:
   - `Group P&L!A99` = `Revenue check` ✓
   - `Group P&L!A100` = `EBITDA check` ✓
   - `Group P&L!A101` = `CapEx check` ✓
   - `Group P&L!A102` = `FCF check` ✓
   - `Group P&L!A103` = `D&A check` ✓
   - `Group P&L!A104` = `EBIT consistency` ✓
   - `Group P&L!A105` = `Launch services elimination conservation` ✓
   - `Group P&L!A106` = `Bandwidth elimination conservation` ✓
   - `Group P&L!A107` = `Compute elimination conservation` ✓
   - `Group P&L!A108` = `ALL OK boolean` ✓
   - `Group P&L!A109` = `Cash flow identity` ✓
   - Halt on any label drift — would indicate Sprint 1 amendment Sprint 9 doesn't know about.

8. **5 architectural locks confirmed via AskUserQuestion 2026-05-22** (recorded in §9 amendment log):
   - **Lock a — Mars carve-out**: REAL CASH DRAIN. R109 cash flow identity subtracts Σ strategic carve-out. Pre-2028 $3B (2025-2027) treated as Mars program pre-deployment investment.
   - **Lock b — Architecture §11.4 amendment**: DEFERRED to Sprint 10/11 audit. Sprint 7 §9 amendment 1 interpretation ("ships deployed" = surface missions) carries forward.
   - **Lock c — Internal flow eliminations R106 + R107**: FORMULA-NOW BOTH SIDES. R106 reads Starlink internal bandwidth rev − ODC bandwidth services cost (IFERROR-0 wrapped; both = $0 in 2025; activates 2030+). R107 reads ODC internal transfer rev − AI Stack internal compute cost (IFERROR-0 wrapped; both = $0 until Sprint 6 lands).
   - **Lock d — G&A + Other base re-anchor**: REWIRE TO GROUP P&L NET. Sprint 9 publishes canonical row `GROUP REVENUE NET OF ELIMS ($mm)`. OpEx R46 (G&A base) + R49 (Other base) repointed to read Group P&L net via INDEX/MATCH. OpEx R57 memo retained as diagnostic display.
   - **Lock e — Calibration target revision**: REVISE TO REBUILD REALITY. §6.8 targets revised: Group Revenue $14,650M ±5% unchanged; Group Gross Profit $9,463M ±10%; Group EBITDA $4,904M ±5%; Group D&A $1,261M ±10%; Group EBIT ~$4,450M derived; Taxes $935M derived (21%); NOPAT $3,515M derived; Group FCF −$2,569M ±10% [−$2,312M, −$2,826M]. Original Q4'25 raw anchors retained as memo rows for archaeology, not as halt thresholds.

---

## §2 — Framing

### §2.1 What this sprint does

Sprint 9 builds the **full Group P&L walk** on Group P&L tab (rows 7-98, fills blank space Sprint 1 left) + **inter-module eliminations block** at rows 42-44 + **conservation block activation** at rows 99-109 (overwrites Sprint 1 literal-0 placeholders with live INDEX/MATCH formulas) + **R109 cash flow identity with Mars carve-out as real cash drain** + **calibration memo rows R111-R125** (revised §6.8 targets + Q4'25 archaeology) + **OpEx R46 + R49 rewire** to read Group P&L net (per Lock d).

Sprint 9 publishes 7 canonical labels for downstream consumption (Sprint 10 Allocator Cash Pool + Queue Gate; Sprint 11 Valuation DCF + SoTP).

### §2.2 What this sprint does NOT do

- **No module tab writes** — Sprint 9 READS modules by canonical label only. Per Principle 10.
- **No CapEx tab writes** — Sprint 9 reads CapEx by canonical label. Sprint 8/8.5 set up everything Sprint 9 needs.
- **No Allocator brain light-up** — Sprint 10 lights up Cash Pool Tracker, Queue Gate, IRR sigmoid blends, vehicle build claim. Sprint 9 publishes the canonical rows Sprint 10 reads (especially `Taxes ($mm)` for Queue Gate + `GROUP FCF ($mm)` for Cash Pool Tracker prior-year read).
- **No Valuation tab writes** — Sprint 11 builds Valuation. Sprint 9 publishes the canonical Group P&L rows Sprint 11 reads.
- **No Assumptions amendments** — Sprint 9 adds ZERO new Assumptions inputs. All needed values (tax rate, starting cash, IPO) already on Assumptions from Sprint 0.
- **No spectrum amort wiring into Starlink R160** — Sprint 4 didn't wire (Starlink R160 = 0 confirmed pre-flight). Per Lock e + Principle 10 (Sprint 9 doesn't touch modules), Sprint 9 treats spectrum amort as separate Group D&A line in walk: Group EBIT = Group EBITDA − Corporate D&A − Spectrum amort (since spectrum amort NOT in Module D&A via Starlink COGS). Documented in §9 amendment 1.
- **No Architecture §11.4 amendment** — per Lock b, deferred to Sprint 10/11.
- **No within-year cycle break attempts** — Mars carve-out reads prior-year Group FCF (Allocator R34 formula). Within-year cycle dormant in 2025 (Group FCF doesn't exist yet); activates 2026 with prior-year 2025 FCF read. Trivially converges per Principle 22.

### §2.3 Why this matters

Sprint 9 is **THE BIG CALIBRATION MOMENT** per Sprint Roadmap §3. After 8 prior sprints building module bodies + OpEx + CapEx, Sprint 9 consolidates the full P&L walk and tests whether the rebuild architecture produces sensible 2025 outputs.

The pre-compute against V2.10 (per AskUserQuestion lock e context) showed:
- Group Revenue PASS at +3.3% vs $14,650M target
- Group EBITDA MASSIVE UNDERSHOOT at -43.6% vs $8,690M target → REVISED target $4,904M ±5% reflects rebuild architectural reality
- Group D&A PASS at +18.9% vs $1,060M target → REVISED target $1,261M ±10%
- Group FCF MASSIVE NEGATIVE at -170% vs $3,670M target → REVISED target -$2,569M ±10% reflects EchoStar $5B cash drain + Mars carve-out $1B real drain

This is the SECOND time the rebuild revises Q4'25 raw anchors (first was Sprint 8.5 Total OpEx $3,820 → $4,476M). Pattern: Q4'25 raw anchors are pre-rebuild-architecture; rebuild's fully-allocated vending-machine framing + accounting locks produce structurally different (lower margin, higher CapEx, more negative FCF) but more architecturally consistent numbers.

### §2.4 Cross-year dependencies introduced

- **NEW**: Mars carve-out reads PRIOR-year Group FCF via Allocator R34 IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF ($mm)", 'Group P&L'!$A:$A, 0), D$5), 0). Sprint 1 placeholder = 0; Sprint 7 wrote Allocator R34 formula with IFERROR-0 fallback; Sprint 9 publishes the `GROUP FCF ($mm)` canonical row Sprint 7's formula resolves to.
- **NEW**: R109 cash flow identity uses Σ cumulative running sums (Σ IPO, Σ Group FCF, Σ Group CapEx, Σ carve-out, Cash EoY). All Rule 23 year-chained exceptions per §3.4.

Within-year cycle: Group FCF this year does NOT feed into this year's Mars carve-out (prior-year read). No within-year circularity introduced. Iterative calc remains ON workbook-wide because Sprint 4/5 cycles still live.

### §2.5 7 canonical labels Sprint 9 publishes

| Label on Group P&L tab | Row | Read by |
|---|---|---|
| `GROUP REVENUE NET OF ELIMS ($mm)` | R10 | Sprint 11 Valuation (revenue multiple); OpEx R46 G&A base + R49 Other base (Lock d rewire — Sprint 9 §3.6) |
| `Group EBITDA ($mm)` | R26 | Sprint 11 EBITDA multiple cross-check |
| `Group D&A ($mm)` | R28 | Sprint 11 |
| `Group EBIT ($mm)` | R30 | Sprint 11 |
| `Taxes ($mm)` | R32 | Sprint 10 Allocator §6.2 Queue Gate (reserved before IRR queue) |
| `NOPAT ($mm)` | R34 | Sprint 11 |
| `GROUP FCF ($mm)` | R50 | Sprint 10 Allocator §6.1 Cash Pool Tracker (prior-year FCF → Cash BoY); Sprint 11 DCF; Sprint 7 Allocator §3 R34 (prior-year FCF for Mars carve-out formula) |

Verbatim case-sensitive. Stale-ref scan halt on drift per §4.5.

---

## §3 — Scope

### §3.0 — Pre-flight checks (run BEFORE any §3.x writes)

Plugin executes checks in order. Halt on any miss.

1. **Tab existence + position** — `Group P&L` tab exists at position #10. `Assumptions` at #1, `Allocator` at #2, all 5 module tabs at #4-#9, `OpEx` at #11, `CapEx` at #12, `Demand Curves` at #14, `Claude Log` at #15.

2. **Year header + offset row on Group P&L tab** — D4=2025...AC4=2050 + D5=0...AC5=25.

3. **Sprint 1 R99-R109 placeholder labels intact** — read A99:A109 verbatim per §1.5 step 7.

4. **All MATCH probes pass** — per §1.5 step 6 (37 canonical labels).

5. **OpEx + CapEx + Allocator + Customer Launch + Starlink + Assumptions canonical anchor reads** — read 2025 values:
   - `OpEx!D53` (Total OpEx) ≈ $4,559M. Halt if outside [$4,500M, $4,620M].
   - `CapEx!D17` (Total Module CapEx) ≈ $1,235M. Halt if outside [$1,200M, $1,275M].
   - `CapEx!D37` (Total Corporate D&A) ≈ $120M. Halt if outside [$110M, $130M].
   - `CapEx!D41` (Annual spectrum amortization) ≈ $333M. Halt if outside [$320M, $350M].
   - `CapEx!D44` (Vehicle build claim placeholder) = $0 exact. Halt if non-zero.
   - `CapEx!D45` (Total Group CapEx) ≈ $6,345M. Halt if outside [$6,300M, $6,400M].
   - `Allocator!D35` (Mars/Moon carve-out) = $1,000M exact (floor pre-Sprint-10). Halt if non-$1,000M.
   - `'Customer Launch'!D70` (Internal transfer rev) ≈ $2,290M. Halt if outside [$2,250M, $2,330M].
   - `Starlink!D120` (BB Revenue) ≈ $7,696M. Halt if outside [$7,500M, $7,900M].
   - `Starlink!D131` (DTC Revenue) ≈ $157M. Halt if outside [$140M, $175M].
   - `Assumptions!B3` (Tax rate) = 0.21 exact. Halt if non-0.21.
   - `Assumptions!B8` (Starting cash) = 5000 exact. Halt if non-5000.
   - `Assumptions!B9` (IPO injection amount) = 30000 exact. Halt if non-30000.
   - `Assumptions!B10` (IPO injection year) = 2027 exact. Halt if non-2027.

6. **Iterative calc setting** — confirm 100 iter / 0.001 tol. Halt if OFF.

After all 6 pre-flight steps pass, plugin proceeds to §3.1.

---

### §3.1 — Group P&L walk (rows 7-50)

Per Architecture §15.1 verbatim. Plugin fills blank rows 7-50 (Sprint 1 left blank below row 6 title).

**Layout overview:**

| Rows | Section | Concept |
|---|---|---|
| 7 | header | §1 GROUP REVENUE BUILD |
| 8-9 | §3.1.1 | Σ Module revenue gross + breakdown |
| 10 | §3.1.2 | GROUP REVENUE NET OF ELIMS (canonical) — reads Σ module revenue gross − R42 − R43 − R44 elims |
| 12 | header | §2 GROUP COGS BUILD |
| 13-14 | §3.1.3 | Σ Module COGS gross + breakdown |
| 15 | §3.1.4 | Group COGS net of elims |
| 17 | header | §3 GROUP GROSS PROFIT |
| 18 | §3.1.5 | Group Gross Profit (= Group Rev net − Group COGS net; equivalent to Σ Module EBITDA) |
| 20 | header | §4 OPEX |
| 21 | §3.1.6 | Total OpEx (read from OpEx R53) |
| 23-26 | §3.1.7 | GROUP EBITDA + Module D&A breakdown |
| 28 | §3.1.8 | Group D&A (total, including Corporate D&A + Spectrum amort) |
| 30 | §3.1.9 | Group EBIT |
| 32 | §3.1.10 | Taxes |
| 34 | §3.1.11 | NOPAT |
| 36-39 | §3.1.12 | Total D&A add-back breakdown |
| 41 | header | §5 INTER-MODULE ELIMINATIONS |
| 42 | §3.2.1 | Internal launch services eliminated |
| 43 | §3.2.2 | Internal bandwidth eliminated |
| 44 | §3.2.3 | Internal compute eliminated |
| 46 | §3.1.13 | Total Group CapEx (read CapEx R45) |
| 47 | §3.1.14 | Mars/Moon strategic carve-out (read Allocator R35) |
| 50 | §3.1.15 | GROUP FCF (canonical) |

#### §3.1.1 — Module revenue breakdown (rows 7-9)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 7 | `§1 GROUP REVENUE BUILD (Architecture §15.1)` | section header (charcoal/white fill A7:AC7, bold) | text |
| 8 | `Σ Module revenue (gross, pre-elim) ($mm)` | `=INDEX(Starlink!$D:$AC, MATCH("Total Revenue ($mm)", Starlink!$A:$A, 0), D$5+1)+INDEX('Customer Launch'!$D:$AC, MATCH("Total Revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)+INDEX(ODC!$D:$AC, MATCH("Total Revenue ($mm)", ODC!$A:$A, 0), D$5+1)+IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Total Revenue ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)+INDEX('Lunar Mars'!$D:$AC, MATCH("Total Revenue ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1)` | `Sum of 5 modules' R201 by canonical label. AI Stack IFERROR-0 wrap (Sprint 6 deferred).` | `#,##0` |
| 9 | (blank spacer) | | | |

**Plugin write structure (Rule 1) per row 8**:
1. Write row 7 column A label + charcoal/white fill A7:AC7 (one tool call).
2. Write row 8 column A label.
3. Write row 8 column C note.
4. Write row 8 column D formula (the long INDEX/MATCH SUM formula above).
5. copyToRange source D8, destination E8:AC8 (single-cell source per Rule 2; Excel shifts D$5 to E$5 correctly).
6. Apply number format `#,##0` to row 8 D:AC.

**Verification (Rule 4 + Rule 16)**:
- D8 ≈ $17,426M (= $6,572M Customer Launch + $10,854M Starlink + $0 ODC + $0 AI Stack + $0 Lunar Mars). Halt if outside [$17,300M, $17,550M].
- I8 / S8 / AC8: depends on Sprint 4/5 out-year trajectories — informational read.

#### §3.1.2 — GROUP REVENUE NET OF ELIMS (canonical row 10)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 10 | `GROUP REVENUE NET OF ELIMS ($mm)` | `=D8-D42-D43-D44` | `Σ Module revenue (gross) − inter-module eliminations. Subtracts: R42 launch services elim ($2,290M in 2025); R43 bandwidth elim ($0 in 2025, activates 2030+); R44 compute elim ($0 until Sprint 6 lands). CANONICAL — read by Sprint 11 Valuation + OpEx R46/R49 rewire (Sprint 9 §3.6).` | `#,##0` |

**Plugin write structure**: 3-block (A label, C note, D formula + copyToRange E:AC).

**Verification**:
- D10 = $17,426M − $2,290M − $0 − $0 = **$15,137M** ✓ target $14,650M ±5% [$13,917M, $15,382M] PASS at +3.3%.

#### §3.1.3 — Module COGS breakdown (rows 13-14)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 12 | `§2 GROUP COGS BUILD (Architecture §15.1 — Σ Module COGS net of elim)` | section header (charcoal/white) | bold | text |
| 13 | `Σ Module COGS (gross, pre-elim) ($mm)` | `=(INDEX(Starlink!$D:$AC, MATCH("Total Revenue ($mm)", Starlink!$A:$A, 0), D$5+1)-INDEX(Starlink!$D:$AC, MATCH("Module EBITDA ($mm)", Starlink!$A:$A, 0), D$5+1))+(INDEX('Customer Launch'!$D:$AC, MATCH("Total Revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)-INDEX('Customer Launch'!$D:$AC, MATCH("Module EBITDA ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1))+(INDEX(ODC!$D:$AC, MATCH("Total Revenue ($mm)", ODC!$A:$A, 0), D$5+1)-INDEX(ODC!$D:$AC, MATCH("Module EBITDA ($mm)", ODC!$A:$A, 0), D$5+1))+(IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Total Revenue ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)-IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Module EBITDA ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0))+(INDEX('Lunar Mars'!$D:$AC, MATCH("Total Revenue ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1)-INDEX('Lunar Mars'!$D:$AC, MATCH("Module EBITDA ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1))` | `Each module's COGS = R201 Total Revenue − R202 Module EBITDA (per Architecture §3, Module EBITDA = Gross Profit). Sum of 5 modules.` | `#,##0` |
| 14 | (blank spacer) | | | |

**Verification**:
- D13 ≈ $7,963M (= $3,500M Customer Launch + $4,463M Starlink + $0 + $0 + $0). Halt if outside [$7,850M, $8,100M].

#### §3.1.4 — Group COGS net of elim (row 15)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 15 | `Group COGS (net of elims) ($mm)` | `=D13-D42-D43-D44` | `Σ Module COGS − inter-module eliminations. Subtracts the consuming modules' COGS side of internal flows (which equals the source modules' internal transfer revenue subtracted in R10). Conservation: R10 − R15 = R8 − R13 (Revenue side elim = COGS side elim).` | `#,##0` |

**Verification**:
- D15 = $7,963M − $2,290M − $0 − $0 = **$5,673M**.

#### §3.1.5 — Group Gross Profit (row 18)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 17 | `§3 GROUP GROSS PROFIT (Architecture §15.1)` | section header (charcoal/white) | bold | text |
| 18 | `Group Gross Profit ($mm)` | `=D10-D15` | `Group Revenue (net) − Group COGS (net). Equivalent to Σ Module EBITDA = Σ Module Gross Profit (eliminations net to zero on both sides). Sanity: should equal SUM of module R202 values.` | `#,##0` |

**Verification**:
- D18 = $15,137M − $5,673M = **$9,463M**. REVISED target ~$9,463M ±10% [$8,517M, $10,409M] (Vlad lock 2026-05-22).
- Sanity sum check: Σ Module EBITDA = Customer Launch $3,072M + Starlink $6,391M + ODC $0 + AI Stack $0 + Lunar Mars $0 = $9,463M ✓ matches D18 exactly (conservation R100 EBITDA check will read 0).

#### §3.1.6 — Total OpEx (row 21)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 20 | `§4 OPEX (Architecture §15.1 — read OpEx tab by canonical label)` | section header (charcoal/white) | bold | text |
| 21 | `Total OpEx ($mm)` | `=INDEX(OpEx!$D:$AC, MATCH("Total OpEx ($mm)", OpEx!$A:$A, 0), D$5+1)` | `Reads OpEx R53 (Sprint 8 + Sprint 8.5 published; post-Sprint-8.5 retune Total OpEx 2025 ≈ $4,559M).` | `#,##0` |

**Verification**:
- D21 = $4,559M. Halt if outside [$4,500M, $4,620M].

#### §3.1.7 — Group EBITDA + Module D&A breakdown (rows 23-26)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 23 | `Memo: Starlink Constellation D&A in Starlink COGS ($mm)` | `=INDEX(Starlink!$D:$AC, MATCH("Constellation D&A ($mm)", Starlink!$A:$A, 0), D$5+1)` | italic | `Read Sprint 4 R153. ~$707M in 2025. Diagnostic.` | `#,##0.0` |
| 24 | `Memo: Customer Launch Module D&A in COGS ($mm)` | `=INDEX('Customer Launch'!$D:$AC, MATCH("Module D&A ($mm) — informational (also in COGS rows 86 + 88)", 'Customer Launch'!$A:$A, 0), D$5+1)` | italic | `Read Sprint 3 R100. ~$101M in 2025. Diagnostic.` | `#,##0.0` |
| 25 | `Memo: ODC sat D&A in COGS ($mm)` | `=INDEX(ODC!$D:$AC, MATCH("Annual sat D&A ($mm/yr)", ODC!$A:$A, 0), D$5+1)` | italic | `Read Sprint 5 R106. $0 in 2025 (ODC pre-deployment). Diagnostic.` | `#,##0.0` |
| 26 | `Group EBITDA ($mm)` | `=D18-D21` | `Architecture §15.1: Group Gross Profit − Total OpEx. NOTE: Module D&A is INSIDE Module COGS per vending-machine framing (Architecture §3 labeling note) — Group EBITDA here is the contribution-margin-after-OpEx variant, NOT traditional Operating-Income-plus-D&A EBITDA. Traditional EBITDA = D26 + Σ Module D&A in COGS (R23+R24+R25). CANONICAL — read by Sprint 11 EBITDA multiple cross-check.` | `#,##0` |

**Verification**:
- D23 ≈ $707M. D24 ≈ $101M. D25 = $0.
- D26 = $9,463M − $4,559M = **$4,904M**. REVISED target $4,904M ±5% [$4,659M, $5,149M] (Vlad lock 2026-05-22). Original Q4'25 $8,690M retained as memo at §3.5.

#### §3.1.8 — Group D&A (row 28)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 28 | `Group D&A ($mm)` | `=D23+D24+D25+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Lunar ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Mars ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)+INDEX(CapEx!$D:$AC, MATCH("Annual spectrum amortization ($mm)", CapEx!$A:$A, 0), D$5+1)` | `Σ Module D&A in COGS (Constellation R23 + Customer Launch R24 + ODC R25 + Lunar Mars BV dep) + Corporate D&A (CapEx R37) + Spectrum amort (CapEx R41). PER ARCHITECTURE §15.1 NOTE: spectrum amort "is inside Starlink COGS so don't double-count" — BUT V2.10 workbook has Starlink R160 = 0 (spectrum amort NOT yet wired into Starlink COGS). Sprint 9 treats spectrum amort as SEPARATE Group D&A line. Conservation R103 D&A check confirms no double-count (since Module D&A in COGS doesn't include spectrum). CANONICAL — read by Sprint 11.` | `#,##0` |

**Verification**:
- D28 = $707M + $101M + $0 + $0 + $0 + $120M + $333M = **$1,261M**. REVISED target $1,261M ±10% [$1,135M, $1,387M] (Vlad lock 2026-05-22).

#### §3.1.9 — Group EBIT (row 30)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 30 | `Group EBIT ($mm)` | `=D26-INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)-INDEX(CapEx!$D:$AC, MATCH("Annual spectrum amortization ($mm)", CapEx!$A:$A, 0), D$5+1)` | `Group EBITDA − Corporate D&A − Spectrum amort. Module D&A already inside Group EBITDA via Module COGS (Architecture §3 labeling note). NOT subtracting Module D&A again here (would double-count). Spectrum amort subtracted here because Sprint 4 didn't wire into Starlink R160 (R160=0 confirmed pre-flight). CANONICAL — read by Sprint 11.` | `#,##0` |

**Verification**:
- D30 = $4,904M − $120M − $333M = **$4,450M**. Derived. Sanity: D30 should equal D26 − D28 + Σ Module D&A in COGS (R23+R24+R25 = $808M) = $4,904M − $1,261M + $808M = $4,451M ✓ (rounding $1M).

#### §3.1.10 — Taxes (row 32)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 32 | `Taxes ($mm)` | `=MAX(0, D30) * INDEX(Assumptions!$B:$B, MATCH("Tax rate (corporate, US federal + state blended)", Assumptions!$A:$A, 0))` | `MAX(0, Group EBIT) × tax_rate (Assumptions R3 = 21%). MAX guard prevents negative tax credit (conservative). CANONICAL — read by Sprint 10 Allocator §6.2 Queue Gate as a reserved non-module claim.` | `#,##0.0` |

**Verification**:
- D32 = MAX(0, $4,450M) × 0.21 = **$934M**. Halt if outside [$800M, $1,050M].

#### §3.1.11 — NOPAT (row 34)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 34 | `NOPAT ($mm)` | `=D30-D32` | `Group EBIT − Taxes. CANONICAL — read by Sprint 11.` | `#,##0.0` |

**Verification**:
- D34 = $4,450M − $934M = **$3,516M**.

#### §3.1.12 — Total D&A add-back breakdown (rows 36-39)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 36 | `Memo: Σ Module D&A in COGS ($mm)` | `=D23+D24+D25+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Lunar ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Mars ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)` | italic | `Diagnostic.` | `#,##0.0` |
| 37 | `Memo: Corporate D&A ($mm)` | `=INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)` | italic | `Read CapEx R37.` | `#,##0.0` |
| 38 | `Memo: Spectrum amort ($mm)` | `=INDEX(CapEx!$D:$AC, MATCH("Annual spectrum amortization ($mm)", CapEx!$A:$A, 0), D$5+1)` | italic | `Read CapEx R41.` | `#,##0.0` |
| 39 | `Total D&A add-back ($mm)` | `=D36+D37+D38` | `Sum of Module D&A + Corporate D&A + Spectrum amort. Equals D28 Group D&A by construction (conservation R103 verifies).` | `#,##0.0` |

**Verification**:
- D36 ≈ $808M. D37 ≈ $120M. D38 ≈ $333M. D39 = $1,261M (matches D28).

#### §3.1.13 — Total Group CapEx (row 46)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 46 | `Total Group CapEx ($mm)` | `=INDEX(CapEx!$D:$AC, MATCH("Total Group CapEx ($mm)", CapEx!$A:$A, 0), D$5+1)` | `Read CapEx R45 (Module CapEx + Corporate CapEx + Spectrum CapEx + Vehicle build claim placeholder $0). Includes $5B EchoStar 2025 as cash CapEx per Sprint 8 + Lock e architectural reality.` | `#,##0.0` |

**Verification**:
- D46 = $6,345M. Halt if outside [$6,300M, $6,400M].

#### §3.1.14 — Mars/Moon strategic carve-out (row 47)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 47 | `Mars/Moon strategic carve-out ($mm)` | `=INDEX(Allocator!$D:$AC, MATCH("Mars/Moon strategic carve-out ($mm/yr)", Allocator!$A:$A, 0), D$5+1)` | `Read Allocator R35 by canonical label. Per Vlad lock 2026-05-22 (Lock a): treated as REAL CASH DRAIN regardless of Lunar Mars Module CapEx spend. Pre-2028 hits $1,000M floor (Lunar Mars actual CapEx = $0); carve-out is Mars program pre-deployment investment (ground infra, tech buy-down, Starship-Mars development). Sprint 10 will activate prior-year FCF-driven scaling.` | `#,##0.0` |

**Verification**:
- D47 = $1,000M. Halt if non-$1,000M.

#### §3.1.15 — GROUP FCF (canonical row 50)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 50 | `GROUP FCF ($mm)` | `=D34+D39-D46-D47` | `NOPAT + Total D&A add-back − Total Group CapEx − Mars/Moon strategic carve-out. Per Architecture §15.1 + Lock a (Vlad lock 2026-05-22). REVISED target $-2,569M ±10% [-$2,312M, -$2,826M]. CANONICAL — read by Sprint 10 Allocator §6.1 Cash Pool Tracker (prior-year FCF), Sprint 11 DCF, Sprint 7 Allocator §3 R34 (prior-year FCF for Mars carve-out formula).` | `#,##0` |

**Verification**:
- D50 = $3,516M + $1,261M − $6,345M − $1,000M = **−$2,568M**. REVISED target −$2,569M ±10%; PASS at exact match.

### §3.2 — Inter-module eliminations block (rows 41-44)

Per Architecture §7 + §15.1. Per Lock c — formula-now both sides for R43 + R44.

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 41 | `§5 INTER-MODULE ELIMINATIONS (Architecture §7 + §15.1)` | section header (charcoal/white) | bold | text |
| 42 | `Internal launch services eliminated ($mm)` | `=INDEX('Customer Launch'!$D:$AC, MATCH("Customer Launch internal transfer revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)` | `Reads Customer Launch R70 internal transfer rev. Sprint 9 subtracts at Group P&L R10 (revenue side) + R15 (COGS side). Per Architecture §7.1: equals Σ consuming modules' Launch services cost. Conservation R105 verifies.` | `#,##0` |
| 43 | `Internal bandwidth eliminated ($mm)` | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("Internal bandwidth revenue ($mm)", Starlink!$A:$A, 0), D$5+1), 0)` | `Reads Starlink internal bandwidth rev (Sprint 4 row TBD; IFERROR-0 wrap if label not yet published). Per Architecture §7.2: equals ODC bandwidth services cost. Both = $0 in 2025 (ODC pre-deployment); activates 2030+. Conservation R106 verifies.` | `#,##0` |
| 44 | `Internal compute eliminated ($mm)` | `=IFERROR(INDEX(ODC!$D:$AC, MATCH("Internal compute transfer revenue ($mm)", ODC!$A:$A, 0), D$5+1), 0)` | `Reads ODC internal transfer rev (Sprint 5 row TBD; IFERROR-0 wrap). Per Architecture §7.3: equals AI Stack internal compute cost. Both = $0 until Sprint 6 lands. Conservation R107 verifies.` | `#,##0` |

**Plugin write structure**: 3-block per row 42/43/44 (A label, C note, D formula + copyToRange E:AC).

**Verification**:
- D42 ≈ $2,290M (Customer Launch R70). Halt if outside [$2,250M, $2,330M].
- D43 = $0 (Sprint 4 may not have published label; IFERROR returns 0). Diagnostic: if D43 > $0 in 2025, Sprint 4 published canonical label and bandwidth flow has rate × volume product. Sprint 9 doesn't halt on $0; activates 2030+.
- D44 = $0 (Sprint 6 deferred; IFERROR returns 0).

### §3.3 — Conservation block activation (overwrites Sprint 1 literal-0 placeholders at R99-R107)

Per Architecture §15.2 verbatim. Sprint 9 OVERWRITES Sprint 1 placeholders.

| Row | A label (Sprint 1 verbatim — NO change) | D formula (Sprint 9 OVERWRITES) | C note | Format |
|---|---|---|---|---|
| 99 | `Revenue check` | `=D10-(D8-D42-D43-D44)` | `Architecture §15.2: Group Revenue net − (Σ module revenues − Σ eliminations). Expected = 0 exact by construction (D10 formula IS D8-D42-D43-D44).` | `#,##0` |
| 100 | `EBITDA check` | `=D18-(INDEX(Starlink!$D:$AC, MATCH("Module EBITDA ($mm)", Starlink!$A:$A, 0), D$5+1)+INDEX('Customer Launch'!$D:$AC, MATCH("Module EBITDA ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)+INDEX(ODC!$D:$AC, MATCH("Module EBITDA ($mm)", ODC!$A:$A, 0), D$5+1)+IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Module EBITDA ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)+INDEX('Lunar Mars'!$D:$AC, MATCH("Module EBITDA ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1))` | `Group Gross Profit (D18) − Σ Module EBITDA. Expected = 0 exact (eliminations net to zero on both Revenue + COGS sides per §7.1/§7.2/§7.3).` | `#,##0` |
| 101 | `CapEx check` | `=INDEX(CapEx!$D:$AC, MATCH("Total Module CapEx ($mm)", CapEx!$A:$A, 0), D$5+1)-(INDEX(Starlink!$D:$AC, MATCH("Module CapEx ($mm)", Starlink!$A:$A, 0), D$5+1)+INDEX('Customer Launch'!$D:$AC, MATCH("Module CapEx ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)+INDEX(ODC!$D:$AC, MATCH("Module CapEx ($mm)", ODC!$A:$A, 0), D$5+1)+IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Module CapEx ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)+INDEX('Lunar Mars'!$D:$AC, MATCH("Module CapEx ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1))` | `CapEx R17 Total Module CapEx − Σ module R205. Expected = 0 by construction (Sprint 8 §3.4.2 R17 = SUM of D11:D15 which read the 5 modules).` | `#,##0` |
| 102 | `FCF check` | `=D50-(INDEX(Starlink!$D:$AC, MATCH("Module FCF ($mm)", Starlink!$A:$A, 0), D$5+1)+INDEX('Customer Launch'!$D:$AC, MATCH("Module FCF ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)+INDEX(ODC!$D:$AC, MATCH("Module FCF ($mm)", ODC!$A:$A, 0), D$5+1)+IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Module FCF ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)+INDEX('Lunar Mars'!$D:$AC, MATCH("Module FCF ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1)-D21-D32-INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)-INDEX(CapEx!$D:$AC, MATCH("Annual spectrum amortization ($mm)", CapEx!$A:$A, 0), D$5+1)*-1-INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)*-1-D47)` | `Group FCF − (Σ Module FCF − OpEx − Taxes − Corporate CapEx − Spectrum CapEx − carve-out). NOTE: this is a SIMPLIFIED conservation: Group FCF = NOPAT + D&A − Group CapEx − carve-out; Σ Module FCF = Σ (Module EBITDA + Module D&A − Module CapEx) = Σ Module EBITDA + Σ Module D&A − Σ Module CapEx. Reconciliation: Group FCF − Σ Module FCF = (NOPAT − Σ Module EBITDA) + (D&A add-back − Σ Module D&A) + (Σ Module CapEx − Group CapEx) − carve-out = -OpEx − Taxes + (Corp D&A + Spectrum amort) + (-Corp CapEx − Spectrum CapEx − Vehicle build) − carve-out. Tolerance ±$5M (more relaxed than other checks per architectural complexity).` | `#,##0` |
| 103 | `D&A check` | `=D28-(D23+D24+D25+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Lunar ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Mars ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)+INDEX(CapEx!$D:$AC, MATCH("Annual spectrum amortization ($mm)", CapEx!$A:$A, 0), D$5+1))` | `Group D&A − (Σ module D&A in COGS + Corporate D&A + Spectrum amort). Expected = 0 by construction (D28 formula). CRITICAL — spectrum amort double-count risk if Sprint 4 wires Starlink R160 in future. If R160 becomes non-zero, this check fires and Sprint 9.5 adjusts formula.` | `#,##0` |
| 104 | `EBIT consistency` | `=D30-(D26-D28+(D23+D24+D25+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Lunar ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Mars ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)))` | `Group EBIT − (Group EBITDA − Group D&A + Σ Module D&A in COGS). Reconciles because Architecture §15.1 Group EBITDA has Module D&A inside (vending-machine framing). EBIT subtracts Corp D&A + Spectrum amort (the non-module pieces). Algebraic identity: D30 = D26 − D28 + (Σ Module D&A in COGS) = D26 − Corp D&A − Spectrum amort. Expected = 0 by construction.` | `#,##0` |
| 105 | `Launch services elimination conservation` | `=D42-(IFERROR(INDEX(Starlink!$D:$AC, MATCH("Launch services cost ($mm)", Starlink!$A:$A, 0), D$5+1), 0)+IFERROR(INDEX(ODC!$D:$AC, MATCH("Launch services cost ($mm)", ODC!$A:$A, 0), D$5+1), 0)+IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Launch services cost ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0))` | `Per Architecture §7.1 Step 4: source's internal transfer rev = Σ consuming modules' Launch services cost. Customer Launch R70 = Σ (Starlink + ODC + AI Stack launch services cost). IFERROR-0 wrap on each (Sprint 4/5/6 may publish under different label). Expected = 0 ±$1M. If non-zero, Customer Launch internal transfer revenue and consuming modules' COGS aren't symmetric — bug.` | `#,##0` |
| 106 | `Bandwidth elimination conservation` | `=D43-IFERROR(INDEX(ODC!$D:$AC, MATCH("Bandwidth services cost ($mm)", ODC!$A:$A, 0), D$5+1), 0)` | `Per Architecture §7.2 Step 4. Starlink internal bandwidth rev = ODC bandwidth services cost. Both = $0 in 2025 (ODC pre-deployment). Activates 2030+. Expected = 0 ±$1M.` | `#,##0` |
| 107 | `Compute elimination conservation` | `=D44-IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Internal compute cost from ODC ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)` | `Per Architecture §7.3 Step 4. ODC internal transfer rev = AI Stack internal compute cost. Both = $0 until Sprint 6 lands. IFERROR-0 wrap. Expected = 0 ±$1M.` | `#,##0` |
| 108 | `ALL OK boolean` | (Sprint 1's existing formula — DO NOT overwrite) `=IF(AND(ABS(D99)<1,ABS(D100)<1,ABS(D101)<1,ABS(D102)<1,ABS(D103)<1,ABS(D104)<1,ABS(D105)<1,ABS(D106)<1,ABS(D107)<1),"OK","CHECK")` | `Sprint 1's formula stays. Now that R99-R107 are live formulas, D108 should still read "OK" since all checks designed to read 0 by construction. R102 FCF check uses ±$5M tolerance (relaxed); other checks ±$1M. D108 formula's <1 threshold catches anything outside ±$1M; for R102 specifically, a separate diagnostic memo at §3.5 surfaces if magnitude > $5M.` | text |
| 109 | `Cash flow identity` | (see §3.4) | (see §3.4) | `#,##0` |

**Plugin write structure for R99-R107**: 
- Read existing A99:A107 labels — confirm Sprint 1 verbatim per §3.0 step 7.
- For each row 99-107: write D{row} formula, then copyToRange D{row} to E{row}:AC{row}. C-column note overwrite.
- 9 rows × 3 blocks per row = 27 tool calls.

R108 NOT overwritten — Sprint 1's formula is preserved and now reads live values from R99-R107.

R109 separately written in §3.4 (cash flow identity is more complex).

**Verification post-write**:
- D99-D107 each = 0 (within ±$1M tolerance for R99-R101, R103-R107; ±$5M for R102).
- D108 = "OK" exact.
- Halt if ANY year reads "CHECK" or non-zero outside tolerance.

### §3.4 — R109 cash flow identity (Mars carve-out as real cash drain — Lock a)

Per Architecture §15.2 + Lock a (Vlad lock 2026-05-22). Year-chained Rule 23 EXCEPTION: cumulative running sums for IPO + Group FCF + Group CapEx + carve-out + Cash EoY.

The cash flow identity at terminal year (AC = 2050):
```
Starting cash + Σ IPO + Σ Group FCF − Σ Total Group CapEx (already in FCF!) − Σ strategic carve-out (already in FCF!) − Cash EoY = 0
```

Wait — Architecture §15.2 cash identity has both Group FCF AND Group CapEx + carve-out subtracted. This DOUBLE-counts them since Group FCF already nets them. Sprint 9 spec clarifies: the identity is meant to verify Cash EoY = Starting cash + Σ IPO + Σ Group FCF (where Group FCF already nets CapEx + carve-out).

Architecture §15.2 verbatim: `Σ deployed CapEx − Σ strategic carve-out`. The "deployed CapEx" here is module CapEx only (not Group CapEx), since the others (OpEx, Corp CapEx, Spectrum, Taxes) are already in Group FCF. But that's not quite right either — module CapEx is ALSO in Group FCF.

**Sprint 9 resolution per Lock a**: R109 cash flow identity simplified to verify the cash pool tracker equation:
```
R109 = Starting cash (D=2025) + Σ IPO (cumulative through year) + Σ Group FCF (cumulative through year) − Cash EoY (this year)
```
Where Cash EoY (this year) = next year's Cash BoY = Allocator R12 read for next year (Sprint 10 publishes).

Pre-Sprint-10: Allocator R12 (Cash BoY) doesn't exist yet → R109 cannot validate against Cash EoY. Sprint 9 publishes R109 in IFERROR-0 form that activates when Sprint 10 lands. Pre-Sprint-10, R109 reads 0 (trivial pass — equation has no Cash EoY to compare against).

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 109 | `Cash flow identity` | `=IFERROR(INDEX(Assumptions!$B:$B, MATCH("Starting cash position EoY 2024 ($mm)", Assumptions!$A:$A, 0))+SUMPRODUCT((Assumptions!$D$10:$AC$10<=D$4)*IF($D$4<=Assumptions!$B$10, INDEX(Assumptions!$B:$B, MATCH("IPO injection amount ($mm)", Assumptions!$A:$A, 0))*(D$4>=Assumptions!$B$10), 0))+SUMIF($D$5:D$5, "<="&D$5, $D50:D50)-IFERROR(INDEX(Allocator!$D:$AC, MATCH("Cash BoY ($mm)", Allocator!$A:$A, 0), D$5+2), 0), 0)` | `Year-chained Rule 23 EXCEPTION. Pre-Sprint-10: Allocator Cash BoY row doesn't exist → IFERROR returns 0 → R109 reads 0 trivially. Post-Sprint-10: Allocator publishes Cash BoY row; R109 validates: Starting cash + Σ IPO (cumulative) + Σ Group FCF (cumulative through year T) − Cash BoY (year T+1) = 0 ±$1M. Per Lock a (Vlad lock 2026-05-22): Mars carve-out as real cash drain is ALREADY in Group FCF (D50) via D47 carve-out subtraction; cash identity doesn't double-subtract.` | `#,##0` |

**SIMPLIFIED ALTERNATIVE** (cleaner — recommended for plugin implementation):

```
D109 = =IF(D$5=0, 0, 0)
```

Just write literal 0 in D109 with copyToRange E109:AC109. Sprint 9 doesn't activate R109 fully until Sprint 10 publishes Cash BoY. R108 "OK" check still passes because R109 = 0 satisfies the AND check (R108 doesn't include R109 in its current Sprint 1 formula — only R99-R107).

**Plugin pacing**: Write D109 = 0 (literal), copyToRange E109:AC109. Column C note: `Sprint 9 placeholder = 0. Sprint 10 activates with Cash BoY read. Per Lock a (Vlad lock 2026-05-22): Mars carve-out treated as real cash drain in Group FCF D50; R109 cash identity will validate Starting cash + Σ IPO + Σ Group FCF − Cash EoY = 0 once Sprint 10 publishes Cash BoY canonical row.`

**Why this matters**: Sprint 1's R108 boolean formula reads D99-D107 only. R109 is NOT in the AND check. So R109 can stay as 0 placeholder for Sprint 9 without breaking R108. Sprint 10 will both populate R109 AND extend R108 formula to include R109 in the AND check (Sprint 10 amendment to R108 formula).

**Verification**:
- D109 = 0 every year (literal placeholder).
- Halt if non-zero in any year (would indicate plugin error).

### §3.5 — Calibration target memo rows (R111-R125) — revised §6.8 + Q4'25 archaeology

Per Lock e (Vlad lock 2026-05-22) + Sprint 8.5 precedent: revised targets hardcoded as memo rows; original Q4'25 raw anchors retained for archaeology. Per Rule 14 exception (calibration anchors are diagnostic display, not behavior inputs).

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 111 | `§6 CALIBRATION TARGETS (REVISED 2026-05-22 + Q4'25 archaeology)` | section header (charcoal/white) | bold | text |
| 112 | `Memo: Group Revenue 2025 target ($mm) — revised` | `=14650` | italic | `Unchanged from Q4'25 (rebuild revenue matches anchor +3.3%). Halt if Group Revenue D10 outside ±5%.` | `#,##0` |
| 113 | `Memo: Group Revenue 2025 delta (%)` | `=IFERROR((D10-D112)/D112, 0)` | italic | `Live calibration delta. Halt if |D113| > 5%.` | `0.0%` |
| 114 | `Memo: Group Gross Profit 2025 target ($mm) — REVISED` | `=9463` | italic | `Sprint 9 revised target per Lock e + Vlad lock 2026-05-22. Original Q4'25 implied $10,830M (different framing). Architecture §3 labeling note: Module D&A in COGS + fully-allocated launch transfer pricing produce structurally lower Gross Profit. Halt if D18 outside ±10%.` | `#,##0` |
| 115 | `Memo: Group Gross Profit 2025 delta (%)` | `=IFERROR((D18-D114)/D114, 0)` | italic | `Live delta. Halt if |D115| > 10%.` | `0.0%` |
| 116 | `Memo: Group EBITDA 2025 target ($mm) — REVISED` | `=4904` | italic | `Sprint 9 revised target per Lock e. Original Q4'25 $8,690M reflected traditional EBITDA (Operating Income + D&A). Rebuild Architecture §15.1 walk gives contribution-after-OpEx (Module D&A inside COGS via vending-machine framing). Plus pre-revenue R&D floors. Halt if D26 outside ±5%.` | `#,##0` |
| 117 | `Memo: Group EBITDA 2025 delta (%)` | `=IFERROR((D26-D116)/D116, 0)` | italic | `Live delta. Halt if |D117| > 5%.` | `0.0%` |
| 118 | `Memo: Group D&A 2025 target ($mm) — REVISED` | `=1261` | italic | `Sprint 9 revised target per Lock e. Original Q4'25 $1,060M (different attribution). Halt if D28 outside ±10%.` | `#,##0` |
| 119 | `Memo: Group D&A 2025 delta (%)` | `=IFERROR((D28-D118)/D118, 0)` | italic | `Live delta. Halt if |D119| > 10%.` | `0.0%` |
| 120 | `Memo: Group FCF 2025 target ($mm) — REVISED` | `=-2569` | italic | `Sprint 9 revised target per Lock a + Lock e. Original Q4'25 $3,670M didn't include: (i) EchoStar $5B as cash CapEx; (ii) Mars carve-out as real cash drain; (iii) Group EBITDA structurally lower. Halt if D50 outside ±10%.` | `#,##0` |
| 121 | `Memo: Group FCF 2025 delta (%)` | `=IFERROR((D50-D120)/D120, 0)` | italic | `Live delta. Halt if |D121| > 10%.` | `0.0%` |
| 122 | `Memo: Q4'25 Group EBITDA original target ($mm) — archaeology` | `=8690` | italic | `Q4'25 raw anchor. Pre-rebuild architecture. RETAINED for archaeology; NOT used as halt threshold.` | `#,##0` |
| 123 | `Memo: Q4'25 Group FCF original target ($mm) — archaeology` | `=3670` | italic | `Q4'25 raw anchor. Pre-rebuild architecture. RETAINED for archaeology; NOT used as halt threshold.` | `#,##0` |
| 124 | `Memo: Total OpEx 2025 (read from OpEx tab)` | `=D21` | italic | `Read D21 above. Verify Sprint 8.5 post-fix value $4,559M.` | `#,##0` |
| 125 | `Memo: Total Group CapEx 2025 (read from CapEx tab)` | `=D46` | italic | `Read D46 above. Verify Sprint 8 value $6,345M.` | `#,##0` |

**Plugin pacing**: 15 rows. Each is single-cell write (no copyToRange — these are single-value memos at D-col only OR live deltas at D-col with separate copyToRange E:AC for delta rows). Italic font + grey fill on memo rows per Rule 17.

Actually for live delta rows (R113, R115, R117, R119, R121), copyToRange D:AC so deltas display every year. Other memo rows (R112, R114, R116, R118, R120, R122, R123) are single-value 2025 anchors — D-col only, no copyToRange.

**Verification**:
- D112 = $14,650M. D113 = +3.3%.
- D114 = $9,463M. D115 = 0.0% (matches exact).
- D116 = $4,904M. D117 = 0.0% (matches exact).
- D118 = $1,261M. D119 = 0.0% (matches exact).
- D120 = -$2,569M. D121 = 0.0% (matches exact).
- D122 = $8,690M (Q4'25 archaeology). D123 = $3,670M (Q4'25 archaeology).
- D124 = $4,559M. D125 = $6,345M.

### §3.6 — OpEx R46 + R49 rewire to Group P&L net (Lock d)

Per Lock d: G&A + Other R&D bases repointed from OpEx-tab R57 memo to Group P&L canonical row `GROUP REVENUE NET OF ELIMS ($mm)` (R10).

**OpEx R46 G&A base — REPLACE**:

Current Sprint 8 D46 (G&A base): `=D57` (reads OpEx R57 memo).

Replacement D46: `=INDEX('Group P&L'!$D:$AC, MATCH("GROUP REVENUE NET OF ELIMS ($mm)", 'Group P&L'!$A:$A, 0), D$5+1)`

Column C note overwrite: `Sprint 9 Lock d rewire: read Group P&L R10 net of internal eliminations by canonical label. Replaces OpEx R57 memo (kept as diagnostic display). Single source of truth for net group revenue. Pre-Sprint-9: R57 returned $15,136M (correctly subtracted Customer Launch internal). Post-Sprint-9: Group P&L R10 returns same $15,137M ± rounding. G&A 2025 = 5% × $15,137M = $757M ≈ unchanged.`

**OpEx R49 Other base — REPLACE**:

Current Sprint 8 D49 formula (Other = 1% × R57): `=INDEX(Assumptions!$B:$B, MATCH("Other corporate operating — flat % of group rev", Assumptions!$A:$A, 0)) * D57`

Replacement D49: `=INDEX(Assumptions!$B:$B, MATCH("Other corporate operating — flat % of group rev", Assumptions!$A:$A, 0)) * INDEX('Group P&L'!$D:$AC, MATCH("GROUP REVENUE NET OF ELIMS ($mm)", 'Group P&L'!$A:$A, 0), D$5+1)`

Column C note overwrite: `Sprint 9 Lock d rewire: same as R46 — repoint base from R57 memo to Group P&L R10 canonical. Other 2025 = 1% × $15,137M = $151M ≈ unchanged.`

**OpEx R57 memo — KEEP** for diagnostic display per Lock d. No rewire.

**Plugin write structure**: 
- For R46: write D46 new formula + copyToRange E46:AC46 + overwrite C46 note. 3 tool calls.
- For R49: same pattern. 3 tool calls.
- R57: untouched.

**Verification post-write**:
- OpEx D46 = $15,137M (matches Group P&L D10). 
- OpEx D47 G&A = 5% × $15,137M = $757M ≈ Sprint 8.5 value $757M unchanged.
- OpEx D49 = 1% × $15,137M = $151M ≈ Sprint 8.5 value $151M unchanged.
- OpEx D53 Total OpEx ≈ $4,559M unchanged (no downstream cascade).

---

## §4 — Verification gate (universal + §6.8 Sprint 9 calibration REVISED)

### §4.1 — Workbook-wide error scan (Rule 4 + Principle 19)

Read every cell on every tab. Count `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`.

**Expected: ZERO errors**.

Pre-existing inherited errors (from Sprint 8): none (Sprint 3.6 cleared Customer Launch G16:AC16 #N/A; Sprint 8.5 caused no new errors).

Sprint 9 introduces no new errors (IFERROR-0 wraps cover Sprint 6 deferred + R43/R44/R106/R107 not-yet-published labels).

Halt on any error.

### §4.2 — Edge-year read-back on Group P&L tab (Rule 16)

Read D=2025, I=2030, S=2040, AC=2050.

| Cell | 2025 (D) | Halt if outside |
|---|---|---|
| R8 Σ Module Revenue gross | ~$17,426M | [$17,300M, $17,550M] |
| R10 GROUP REVENUE NET OF ELIMS | ~$15,137M | [$14,400M, $15,900M] (rev ±5%) |
| R13 Σ Module COGS gross | ~$7,963M | [$7,850M, $8,100M] |
| R15 Group COGS net | ~$5,673M | derived |
| R18 Group Gross Profit | ~$9,463M | [$8,517M, $10,409M] (REVISED ±10%) |
| R21 Total OpEx | $4,559M | [$4,500M, $4,620M] |
| R26 Group EBITDA | ~$4,904M | [$4,659M, $5,149M] (REVISED ±5%) |
| R28 Group D&A | ~$1,261M | [$1,135M, $1,387M] (REVISED ±10%) |
| R30 Group EBIT | ~$4,450M | derived (check) |
| R32 Taxes | ~$934M | [$800M, $1,050M] |
| R34 NOPAT | ~$3,516M | derived |
| R39 Total D&A add-back | ~$1,261M | matches R28 |
| R42 Internal launch elim | ~$2,290M | [$2,250M, $2,330M] |
| R43 Internal bandwidth elim | $0 | exact (ODC pre-deployment) |
| R44 Internal compute elim | $0 | exact (Sprint 6 deferred) |
| R46 Total Group CapEx | ~$6,345M | [$6,300M, $6,400M] |
| R47 Mars carve-out | $1,000M | exact (Allocator R35 floor) |
| R50 GROUP FCF | ~−$2,569M | [−$2,312M, −$2,826M] (REVISED ±10%) |
| R99 Revenue check | 0 | abs ≤ $1M |
| R100 EBITDA check | 0 | abs ≤ $1M |
| R101 CapEx check | 0 | abs ≤ $1M |
| R102 FCF check | 0 | abs ≤ $5M (relaxed per architectural complexity) |
| R103 D&A check | 0 | abs ≤ $1M |
| R104 EBIT consistency | 0 | abs ≤ $1M |
| R105 Launch services elim conservation | 0 | abs ≤ $1M |
| R106 Bandwidth elim conservation | 0 | abs ≤ $1M |
| R107 Compute elim conservation | 0 | abs ≤ $1M |
| R108 ALL OK boolean | "OK" | exact |
| R109 Cash flow identity | 0 | placeholder, exact |

Edge-year reads at I/S/AC also expected within their tolerance bands — informational read; halts only on 2025 anchor breaches.

### §4.3 — Conservation block validation (Rule 5 — non-negotiable)

R108 = "OK" required EVERY YEAR 2025-2050 for sprint completion.

Read `Group P&L!D108:AC108` across all 26 years.

**Expected: every cell = "OK" text string exact**.

If any year reads `"CHECK"`, `#REF!`, `#NAME?`, or any other value → HALT immediately, trace, fix before declaring complete.

Conservation breakage is the highest-priority fault per Rule 5. A spec is not done if conservation is broken. Push back to user with the failing check identified.

### §4.4 — Round-trip stability (Rule 22 / Principle 22)

After all §3 writes complete:
1. Recalc workbook 5 times (full rebuild — Ctrl-Shift-F9 or equivalent).
2. Capture: Group P&L D10, D26, D28, D50, D108 + I, S, AC equivalents (32 cells).
3. Confirm no cell moves >$1M (or no change in "OK"/"CHECK" text for D108-AC108).

Sprint 9 introduces ONE new cross-year dependency: Group FCF (R50) → Allocator R34 prior-year Group FCF read → Mars carve-out R35 → Lunar Mars Module CapEx R205 (read via CapEx tab R15 → R17 → R45 → Group P&L R46 Total Group CapEx → R50 Group FCF).

PRIOR-year FCF reference breaks within-year cycle. Convergence trivially holds (no within-year feedback).

Halt if any captured value swings >$1M across 5 recalcs (would indicate new bistability — diagnose).

### §4.5 — Stale-reference scan (Rule 22)

5 scan checkpoints:

**Scan 1 — Sprint 1 R99-R109 placeholder labels intact post-overwrite**:
- Read A99:A109 — verify Sprint 1 verbatim strings preserved.
- Halt on any drift.

**Scan 2 — Module canonical labels Sprint 9 reads still resolve**:
- 37 MATCH probes per §1.5 step 6 — re-run post-write.
- Halt on any #N/A.

**Scan 3 — 7 canonical labels Sprint 9 publishes verbatim**:
- Read Group P&L!A10 = exact `GROUP REVENUE NET OF ELIMS ($mm)`.
- Read Group P&L!A26 = `Group EBITDA ($mm)`.
- Read Group P&L!A28 = `Group D&A ($mm)`.
- Read Group P&L!A30 = `Group EBIT ($mm)`.
- Read Group P&L!A32 = `Taxes ($mm)`.
- Read Group P&L!A34 = `NOPAT ($mm)`.
- Read Group P&L!A50 = `GROUP FCF ($mm)`.
- Halt on any drift — downstream readers (Sprint 10 + Sprint 11) would fail to resolve.

**Scan 4 — Sprint 7 Allocator R34 prior-year Group FCF read resolves now**:
- Sprint 7 wrote Allocator R34 formula: `=IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF", 'Group P&L'!$A:$A, 0), E$5), 0)`.
- Wait — Sprint 7 used MATCH literal `GROUP FCF` (no `($mm)` suffix). Sprint 9 publishes `GROUP FCF ($mm)`. LABEL MISMATCH.
- **Resolution**: Sprint 9 amends Allocator R34 formula to use exact label `GROUP FCF ($mm)`. Add as §3.7 below.

**Scan 5 — OpEx R46 + R49 Lock d rewire correct**:
- Read OpEx D46 formula = matches §3.6 template.
- Read OpEx D49 formula = matches §3.6 template.
- Verify OpEx D47 G&A 2025 = $757M (unchanged from Sprint 8.5).
- Verify OpEx D49 Other 2025 = $151M (unchanged).
- Verify OpEx D53 Total OpEx 2025 = $4,559M (unchanged).

### §3.7 — Allocator R34 label fix (Scan 4 surfaced)

Per §4.5 Scan 4: Sprint 7 wrote Allocator R34 formula using MATCH literal `GROUP FCF` but Sprint 9 publishes `GROUP FCF ($mm)`. Sprint 9 amends Allocator R34 to use exact verbatim canonical label.

**Allocator R34 formula REPLACE**:

Current (Sprint 7): `=IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF", 'Group P&L'!$A:$A, 0), E$5), 0)`

Replacement: `=IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF ($mm)", 'Group P&L'!$A:$A, 0), D$5), 0)`

Note: Sprint 7 used `E$5` which is the year-offset for next column. Year-lookback by 1: column D=2025 reads year-offset D$5+1−2 = -1 → IFERROR returns 0. Sprint 9 keeps `D$5` (NOT `E$5`) which is the same idea: D-col reads `D$5 = 0` → INDEX col_num 0 → spill / error → IFERROR catches. For E-col reads `E$5 = 1` → INDEX col_num 1 → reads D-col Group FCF. 

Actually, let's reconcile: Sprint 7 wrote `E$5` because the formula is in D-col and references D34 → uses D5 not E5. Let me re-read Sprint 7 §3.2 R34 formula:

```
=IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF", 'Group P&L'!$A:$A, 0), E$5), 0)
```

Hmm — uses `E$5`. But for D-col reads, E$5 = 1, which would index col 1 = D-col of Group P&L = 2025 column. That gives CURRENT year FCF, not prior-year FCF. 

Wait, Sprint 7 §3.2 R34 says: `Year-lookback by 1: column D=2025 reads year-offset E$5+1−2 = (D$5=0)+1−2 = -1 → IFERROR returns 0.`

But the formula uses `E$5` directly, not `E$5+1-2`. Let me look at this more carefully. The formula:
`INDEX('Group P&L'!$D:$AC, MATCH(...), E$5)` 

When this formula is in cell D34, `E$5` refers to cell E5 which holds value 1. So INDEX col_num = 1 → reads `'Group P&L'!$D$X` (the D column of Group P&L where X = MATCH return). That's 2025 column of Group P&L = current year's FCF, not prior-year.

When the formula is in cell E34, `E$5` still refers to E5 (because `$` locks the row). Wait no — `E$5` has `$` on row only, not column. So when D34 formula is copied to E34, `E$5` becomes `F$5` = 2. That gives INDEX col_num=2 = E-col of Group P&L = 2026 = current year.

Actually `E$5` in cell D34 is a literal reference to cell E5 (with $ locking row). When formula copies right, the column shifts: E$5 → F$5 → G$5 etc. So the formula in column D34 reads E$5 = year-offset of NEXT column (2026); in column E34 reads F$5 = year-offset of 2027.

This gives lookback BY -1 year: D34 (2025) reads 2026 FCF (one year FORWARD). That's not what we want — we want PRIOR-year FCF.

Sprint 7's formula has a BUG. Sprint 9 fixes:

Correct prior-year lookback in D34 should read D-col of Group P&L for 2024 FCF (which doesn't exist; pre-horizon). Actually Group FCF starts at 2025. For 2025's Mars carve-out, prior-year = 2024 (no Group FCF available) → IFERROR returns 0 → carve-out hits floor.

To achieve this: 
- D34 (2025) should INDEX col_num = 0 → INDEX returns spill/error → IFERROR → 0. ✓
- E34 (2026) should INDEX col_num = 1 → reads D-col Group P&L = 2025 FCF. ✓
- ...
- AC34 (2050) should INDEX col_num = 25 → reads AB-col Group P&L = 2049 FCF. ✓

Formula: INDEX col_num = D$5 (year-offset of CURRENT column). When formula is in D34, D$5 = 0 → INDEX col_num=0 → spill → IFERROR returns 0 ✓. When in E34, E$5 = 1 → INDEX col_num=1 → reads D-col = 2025 FCF ✓.

So correct formula uses `D$5` (relative column, locked row), NOT `E$5` as Sprint 7 wrote.

**Sprint 9 fixes both**:
1. Label drift: `GROUP FCF` → `GROUP FCF ($mm)`
2. Column reference bug: `E$5` → `D$5`

**Final Allocator R34 formula**:
```
=IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF ($mm)", 'Group P&L'!$A:$A, 0), D$5), 0)
```

**Plugin write structure**: Write D34 new formula + copyToRange E34:AC34 + overwrite C34 note.

**C34 note overwrite**: `Sprint 9 fix: (1) label drift Sprint 7 used 'GROUP FCF' → Sprint 9 publishes 'GROUP FCF ($mm)' canonical; (2) column reference bug Sprint 7 used E$5 (next column year-offset) → Sprint 9 uses D$5 (current column year-offset) for correct prior-year lookback. D34 (2025) reads INDEX col_num=0 → IFERROR returns 0; E34 (2026) reads col_num=1 = 2025 FCF; ... AC34 (2050) reads col_num=25 = 2049 FCF.`

**Verification post-fix**:
- Allocator D34 = 0 (2025 has no prior-year FCF; IFERROR catches col_num=0 spill).
- Allocator E34 = Group P&L D50 (2025 FCF) = -$2,569M. 
- Wait — that activates Mars carve-out formula: D35 = MAX(D33, D32 × D34) → for E35 (2026): MAX($1,000M, 0.15 × -$2,569M) = MAX($1,000M, -$385M) = $1,000M. Floor wins.
- I34 (2030) = Group P&L H50 (2029 FCF). Depends on out-year trajectory.

This fix activates Mars carve-out scaling once Group FCF turns positive (likely 2028+ in rebuild trajectory). Pre-Sprint-9: carve-out always at $1,000M floor. Post-Sprint-9: carve-out scales as MAX(floor, 0.15 × prior FCF) once FCF > $6,667M trips the threshold.

Sprint 7 Open Thread #1 partial resolution: Sprint 9 confirms Mars carve-out is real cash drain (Lock a); fixes formula bug; pre-2028 carve-out reserve $3B = real cash drain in cash identity (R109 once Sprint 10 activates).

### §4.6 — Sprint 9 calibration table (REVISED §6.8 per Vlad lock 2026-05-22)

| Output | 2025 target | Tolerance | Halt threshold |
|---|---|---|---|
| Group Revenue (R10) | $14,650M | ±5% (unchanged) | [$13,917M, $15,382M] |
| Group Gross Profit (R18) | $9,463M (REVISED from $10,830M) | ±10% | [$8,517M, $10,409M] |
| Group EBITDA (R26) | $4,904M (REVISED from $8,690M) | ±5% | [$4,659M, $5,149M] |
| Group EBITDA Margin (R26 ÷ R10) | 32.4% (REVISED from 59.3%) | ±3pp | [29.4%, 35.4%] |
| Group D&A (R28) | $1,261M (REVISED from $1,060M) | ±10% | [$1,135M, $1,387M] |
| Group EBIT (R30) | $4,450M (derived) | within ±$50M of D26 − D28 + Σ module D&A | check |
| Taxes (R32) | $934M (derived 21%) | within ±$50M of (D30 × 0.21) | [$800M, $1,050M] |
| NOPAT (R34) | $3,516M (derived) | within ±$50M of D30 − D32 | check |
| Total D&A add-back (R39) | $1,261M | matches D28 | exact ±$1M |
| Total Group CapEx (R46) | $6,345M | ±5% (Sprint 8 anchor) | [$6,028M, $6,663M] |
| Mars carve-out (R47) | $1,000M | exact (floor) | non-$1,000M |
| Group FCF (R50) | −$2,569M (REVISED from $3,670M) | ±10% | [−$2,312M, −$2,826M] |
| Conservation block ALL OK (R108) | "OK" every year | exact | any "CHECK" |

Original Q4'25 targets retained as memo at R122/R123 for archaeology — NOT used as halt thresholds.

If Sprint 9 misses any revised target → halt and trace through which input is wrong. Most likely culprits: (a) module R201/R202/R204/R205 drifted from Sprint 4/5/7 values, (b) OpEx R53 changed post-Sprint-8.5, (c) CapEx R45/R37/R41 changed, (d) Customer Launch R70 internal transfer revenue drifted.

### §4.7 — Claude Log entry (Rule 4 + Sprint Roadmap §5.7)

Append one row to Claude Log tab:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-05-{DD} | 9 | Group P&L (full walk R7-R50 + elims R42-R44 + conservation R99-R109 + calibration memo R111-R125), OpEx (R46 + R49 Lock d rewire), Allocator (R34 label + col-ref fix per §3.7) | Group P&L full walk LIVE per Architecture §15.1 verbatim. 7 canonical labels published: GROUP REVENUE NET OF ELIMS R10 ($15,137M 2025 +3.3% vs $14,650M unchanged target), Group EBITDA R26 ($4,904M REVISED target +0.0%), Group D&A R28 ($1,261M REVISED target +0.0%), Group EBIT R30, Taxes R32, NOPAT R34, GROUP FCF R50 (-$2,569M REVISED target +0.0%). Inter-module eliminations LIVE: launch services R42 (-$2,290M Customer Launch R70 in 2025), bandwidth R43 (IFERROR-0 ODC pre-deployment), compute R44 (IFERROR-0 Sprint 6 deferred). Conservation block R99-R107 ACTIVATED: all live INDEX/MATCH formulas; R108 "OK" every year 2025-2050. R109 cash flow identity placeholder = 0 pending Sprint 10 Cash BoY activation. Lock a (Vlad 2026-05-22): Mars carve-out REAL CASH DRAIN baked into R47 + R50. Lock c: R106 + R107 formula-now with IFERROR-0 (activates 2030+ / post-Sprint-6). Lock d: OpEx R46 + R49 rewired to Group P&L R10 (single source of truth for net group rev). Lock e: §6.8 targets revised to rebuild reality (Group EBITDA $8,690M → $4,904M; Group D&A $1,060M → $1,261M; Group FCF $3,670M → -$2,569M) per same architectural-vs-Q4'25-raw-anchor pattern Sprint 8.5 hit on OpEx. Roadmap §6.8 amendment needed. Allocator R34 prior-year Group FCF formula bug fixed (label drift + column reference). | (1) Architecture §11.4 ambiguity carried (Lock b deferred to Sprint 10/11 audit). (2) AI Stack 8 open questions (Sprint 6 deferred; Stage 1 scoping shipped). (3) Sprint 10 needs to extend R108 boolean to include R109 cash identity. (4) Sprint 11 Valuation reads 7 canonical labels — verify resolution before Sprint 11 fires. (5) Roadmap §6.8 doc amendment to capture revised targets (Sprint 9 plugin appends amendment to constitutional doc analogous to Sprint 8.5 §3.4). | Sprint 10 (Allocator brain light-up) per Roadmap §3 — lights up Cash Pool Tracker (reads Group FCF), Queue Gate (subtracts OpEx + Corp CapEx + Spectrum + Taxes + Mars carve-out), IRR sigmoid blends (cash + kg), vehicle build claim sized by forward-aggregate kg demand. THEN Sprint 11 Valuation (DCF + SoTP + Comparables + Sensitivity). Sprint 12 MC overlay + Pre-IPO outputs. |

---

## §5 — Claude Log entry template

See §4.7 above.

---

## §6 — Don't touch (out of scope)

- **All 5 module tabs** — Sprint 9 READS by canonical label only. Writes NOTHING. Per Principle 10.
- **CapEx tab** — Sprint 9 reads CapEx R17/R37/R41/R44/R45 by canonical label. Writes nothing.
- **Assumptions tab** — Sprint 9 reads Assumptions R3 (tax rate), R8 (starting cash), R9 (IPO amount), R10 (IPO year). No new amendments.
- **Allocator tab §1-§2 Cash Pool Tracker + Queue Gate** — Sprint 10 lights up. Sprint 9 only touches Allocator R34 (label + col-ref fix per §3.7).
- **Allocator §4-§9 Sigmoid Queues + Vehicle Build + Central IRR Display** — Sprint 10 lights up.
- **Valuation tab** — Sprint 11 builds. Sprint 9 publishes 7 canonical labels Sprint 11 reads.
- **Demand Curves tab** — out of scope.
- **Claude Log tab** — Sprint 9 appends row 11 only (after Sprint 8.5's row 10).
- **Sprint 6 AI Stack** — deferred; Sprint 9 IFERROR-0 wraps throughout.
- **Spectrum amort wiring into Starlink R160** — out of scope per Principle 10 + Lock e (Sprint 9 treats spectrum amort as separate Group D&A line).
- **Architecture §11.4 amendment** — out of scope per Lock b (deferred to Sprint 10/11).
- **Per-mission IRR engine on Lunar Mars** — Architecture §11.6 lock; not Sprint 9 scope.
- **First-year override convention (Sprint 10)** — Sprint 10 implements per Roadmap §6.9.

---

## §7 — Open thread (post-Sprint-9 considerations)

1. **Architecture §11.4 ambiguity** — carried from Sprint 7 §9 amendment 1. Recommend Architecture refresh pre-Sprint-10 or as part of Sprint 10/11 audit.

2. **Sprint 6 AI Stack standalone build** — 8 open questions pending Vlad sign-off (per memory `project-ai-stack-parallel-build-2026-05-22`). Stage 1 scoping doc shipped 2026-05-22. Once Sprint 6 lands, Sprint 9 R44 internal compute elim activates; Sprint 9 §3.6 OpEx R46/R49 reads automatically pick up AI Stack revenue contribution.

3. **R108 boolean formula extension for R109** — Sprint 10 will extend Sprint 1's R108 formula `AND(ABS(D99:D107)<1)` to include R109: `AND(ABS(D99:D109)<1)`. Sprint 10 amendment, not Sprint 9 scope. Documented in §4.7 Claude Log Outstanding #3.

4. **Roadmap §6.8 doc amendment** — Sprint 9 plugin appends amendment to constitutional doc `03_Sprint_Roadmap_and_Verification.md` §6.8 + §9 amendment log capturing revised targets (analogous to Sprint 8.5 §3.4 doc amendment pattern). Sprint 9 plugin execution sequence step 8 below.

5. **Bandwidth elim R43 activation 2030+** — once ODC deploys (Sprint 10 IRR queue activates), Starlink internal bandwidth rev + ODC bandwidth services cost will grow. Sprint 4 published Starlink internal bandwidth rev label TBD; Sprint 5 published ODC bandwidth services cost. Sprint 9 §4.5 Scan 2 confirms reads resolve. Sprint 5 wired bandwidth flow; Sprint 9 §3.2.2 R43 IFERROR-0 wrap will activate once labels resolve.

6. **Compute elim R44 activation post-Sprint-6** — same pattern. Sprint 9 wraps IFERROR-0; activates when Sprint 6 publishes canonical labels.

7. **R109 cash flow identity activation pending Sprint 10 Cash BoY** — Sprint 9 placeholder = 0. Sprint 10 writes Allocator Cash BoY canonical row + extends R109 formula to validate.

8. **Calibration target archaeology** — Sprint 9 retains Q4'25 raw anchors at R122/R123 for archaeology. Future audit (post-Sprint-12) may want to formally decommission these (delete or move to separate archaeology tab). Defer.

9. **Allocator R34 formula bug surfaced by Sprint 9** — Sprint 7 wrote `E$5` instead of `D$5` (year-offset reference points to wrong column). Sprint 9 §3.7 fixes. Same bug pattern could affect other Sprint 7 formulas — Sprint 7 audit recommended pre-Sprint-10 to confirm no other E$5/D$5 confusions in Allocator §3 R32-R37.

---

## §8 — Execution sequence

Plugin executes in this order. Verification gate after each section before proceeding.

1. **§3.0 Pre-flight checks** (6 items including MATCH probes + anchor reads). Halt on any miss.
2. **§3.1 Group P&L walk** (rows 7-50):
   - §3.1.1 Σ Module Revenue gross (R7-R9). Verify D8.
   - §3.1.2 GROUP REVENUE NET OF ELIMS (R10). Verify D10 = $15,137M.
   - §3.1.3 Σ Module COGS gross (R12-R14). Verify D13.
   - §3.1.4 Group COGS net (R15). Verify D15.
   - §3.1.5 Group Gross Profit (R17-R18). Verify D18 = $9,463M.
   - §3.1.6 Total OpEx (R20-R21). Verify D21 = $4,559M.
   - §3.1.7 Module D&A memos + Group EBITDA (R23-R26). Verify D26 = $4,904M.
   - §3.1.8 Group D&A (R28). Verify D28 = $1,261M.
   - §3.1.9 Group EBIT (R30). Verify D30 = $4,450M.
   - §3.1.10 Taxes (R32). Verify D32 = $934M.
   - §3.1.11 NOPAT (R34). Verify D34 = $3,516M.
   - §3.1.12 Total D&A add-back memos (R36-R39). Verify D39 = $1,261M.
3. **§3.2 Inter-module eliminations block** (rows 41-44). Verify D42 = $2,290M, D43 = 0, D44 = 0.
4. **§3.1.13-§3.1.15 Group CapEx + carve-out + GROUP FCF** (rows 46-50). Verify D46 = $6,345M, D47 = $1,000M, D50 = -$2,569M.
5. **§3.3 Conservation block activation** (R99-R107 overwrite Sprint 1 placeholders). Verify D99-D107 all 0; D108 "OK" every year 2025-2050.
6. **§3.4 R109 cash flow identity placeholder** = 0. Verify.
7. **§3.5 Calibration memo rows** (R111-R125). Verify D113/D115/D117/D119/D121 all ~0.0% (matches exact).
8. **§3.6 OpEx Lock d rewire** (OpEx R46 + R49). Verify OpEx D46 = $15,137M; D47 G&A = $757M; D49 Other = $151M; D53 unchanged $4,559M.
9. **§3.7 Allocator R34 label + col-ref fix**. Verify Allocator D34 = 0; E34 onwards = prior-year Group FCF.
10. **§4.1-§4.6 Universal verification** — workbook-wide error scan, edge-year reads, conservation R108 "OK" mandatory, round-trip stability, stale-ref scan, calibration table.
11. **§4.7 Claude Log entry** — append row 11.
12. **Roadmap doc amendment** — append to `03_Sprint_Roadmap_and_Verification.md` §6.8 calibration table revision + §9 amendment log entry per Sprint 8.5 precedent.

---

## §9 — Amendment log

- **2026-05-22 amendment 1 (Spectrum amort separate Group D&A line — workbook reality vs Architecture §15.1 assumption)** — Architecture §15.1 says "Corporate D&A (CapEx tab; spectrum amort is inside Starlink COGS so don't double-count)" — assumes Sprint 4 wired spectrum amort into Starlink R160. V2.10 workbook pre-flight confirms Starlink R160 = 0 (Sprint 4 didn't wire). Sprint 9 treats spectrum amort as SEPARATE line in walk: Group D&A R28 = Σ Module D&A in COGS + Corporate D&A + Spectrum amort; Group EBIT R30 = Group EBITDA − Corporate D&A − Spectrum amort. Conservation R103 D&A check holds (no double-count). If future Sprint 9.5 or audit wires Starlink R160 to read spectrum amort, R103 will fire (Module D&A in COGS will include spectrum, but R28 formula still adds spectrum separately) → re-write R28 to exclude spectrum amort if R160 > 0. Per Principle 10 (Sprint 9 doesn't touch modules), Sprint 9 doesn't pre-emptively wire Starlink R160.

- **2026-05-22 amendment 2 (Allocator R34 formula bug surfaced — Sprint 7 wrote E$5 instead of D$5)** — Sprint 7 §3.2 R34 formula `=IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF", 'Group P&L'!$A:$A, 0), E$5), 0)` has two bugs: (a) MATCH label drift — Sprint 7 used `GROUP FCF`, Sprint 9 publishes `GROUP FCF ($mm)`; (b) column reference — Sprint 7 used `E$5` which points to NEXT column's year-offset (giving INDEX col_num shift FORWARD by one), but prior-year lookback requires `D$5` (current column's year-offset). Sprint 9 §3.7 fixes both. Sprint 7 audit recommended pre-Sprint-10 to confirm no other E$5/D$5 confusions in Allocator §3 R32-R37 (especially R36/R37 Lunar/Mars share reads which use INDEX(..., E$5+1) — those are CORRECT because they read Assumptions row not Group P&L lookback).

- **2026-05-22 amendment 3 (Revised §6.8 calibration targets per Lock e — rebuild architectural reality vs Q4'25 raw anchors)** — Per Vlad lock 2026-05-22: §6.8 calibration targets revised to reflect rebuild architecture decomposition: (i) Module D&A inside COGS via vending-machine framing reduces Group Gross Profit ~$808M; (ii) Fully-allocated launch transfer pricing flows vehicle D&A into consumers ~$1,200M COGS uplift; (iii) Pre-revenue R&D floors ODC $200M + AI Stack $50M boost OpEx; (iv) EchoStar $5B treated as cash CapEx vs Q4'25 likely financed; (v) Mars carve-out $1B as real drain (Lock a). Same pattern Sprint 8.5 hit on Total OpEx ($3,820M → $4,476M revision). Revised targets: Group Revenue $14,650M unchanged; Group Gross Profit $9,463M (was $10,830M, -12.6%); Group EBITDA $4,904M (was $8,690M, -43.6%); Group D&A $1,261M (was $1,060M, +18.9%); Group FCF -$2,569M (was $3,670M, -170%). Original Q4'25 anchors retained as memo rows R122/R123 for archaeology. Roadmap §6.8 + §9 amendment log doc edit per Sprint 8.5 §3.4 precedent.

- **2026-05-22 amendment 4 (Mars carve-out cash drain treatment per Lock a — already pre-committed by Sprint 7 + Sprint 8)** — Vlad lock 2026-05-22 confirmed via AskUserQuestion: Mars carve-out is REAL CASH DRAIN regardless of Lunar Mars Module CapEx spend. Pre-2028 $3B (2025-2027) treated as Mars program pre-deployment investment. Sprint 9 R50 GROUP FCF subtracts R47 Mars/Moon strategic carve-out ($1,000M floor pre-Sprint-10). R109 cash flow identity will validate (post-Sprint-10) that Starting cash + Σ IPO + Σ Group FCF − Cash EoY = 0. Carry-forward-as-reserve alternative explicitly rejected.

- **2026-05-22 amendment 5 (Architecture §11.4 deferred per Lock b)** — Sprint 7 §9 amendment 1 "Surface-landed Starships = ships deployed / (1+depot)" inconsistency interpretation carried forward (Sprint 7 treated "ships deployed" = surface missions). Sprint 9 spec authoring is NOT the right moment to formalize Architecture §11.4 amendment per Vlad lock 2026-05-22. Defer to Sprint 10/11 audit or pre-Sprint-9 Architecture refresh. Sprint 9 Open Thread #1 carries.

- **2026-05-22 amendment 6 (Internal flow eliminations R106 + R107 formula-now both sides per Lock c)** — Sprint 9 §3.3 R106 reads `D43 - INDEX(ODC!..., MATCH("Bandwidth services cost ($mm)", ...))` IFERROR-0 wrapped; R107 reads `D44 - INDEX('AI Stack'!..., MATCH("Internal compute cost from ODC ($mm)", ...))` IFERROR-0 wrapped. Both pre-2030 / pre-Sprint-6 = 0 = 0 (trivial conservation). Activates cleanly once ODC ramps + Sprint 6 lands. No Sprint 9.5 rewire needed. Alternative (literal-0 until activation) explicitly rejected.

- **2026-05-22 amendment 7 (G&A + Other base rewire to Group P&L net per Lock d)** — OpEx R46 G&A base + R49 Other base rewired from OpEx R57 memo to Group P&L R10 canonical row `GROUP REVENUE NET OF ELIMS ($mm)`. Single source of truth for net group revenue. R57 OpEx-tab memo retained as diagnostic display. Sprint 9 §3.6 OpEx writes 2 cells per row × 2 rows = 4 formula writes + 2 note overwrites. OpEx D47 G&A 2025 unchanged ($757M) since R10 and R57 both return $15,137M in 2025. Sprint 9 conservation: future bandwidth + compute elims at Group P&L R43 + R44 will flow through R10 automatically — Sprint 8.5 OpEx R57 wouldn't pick them up; Sprint 9 R10 will. This is the architectural fix.

---

## §10 — Pre-execution checklist for plugin

Before plugin chat starts writing:

- [ ] Constitutional docs read (00 README, 01 Lessons, 02 Architecture §§1-17 esp. §7 + §15 verbatim, 03 Roadmap §3 Sprint 9 + §6.8, 04 Assumptions, Model Execution Rules, 2025 Anchors).
- [ ] This spec's §1 Rule Compliance Preamble — all 12 boxes ticked (confirmed by spec author 2026-05-22).
- [ ] §1.5 Pre-execution setup — confirmed: tab list 15 tabs, iterative calc ON, Sprint 8.5 PASS, no workbook-name confirmation needed.
- [ ] §3.0 Pre-flight checks (6 items) — to be run by plugin BEFORE any write.
- [ ] Plugin understands 5 architectural locks (Lock a-e) — recorded in §9 amendment log.
- [ ] Plugin understands revised §6.8 calibration targets — NOT Q4'25 raw anchors (those at memo R122/R123 for archaeology).
- [ ] Plugin understands Sprint 6 deferred → AI Stack reads via IFERROR-0 throughout.
- [ ] Plugin understands R109 cash flow identity = 0 placeholder (Sprint 10 activates).
- [ ] Plugin understands Allocator R34 formula bug fix is part of Sprint 9 §3.7 (touches Allocator tab — Sprint 9 exception to "no Allocator writes" rule).
- [ ] Plugin understands Roadmap §6.8 doc amendment is part of Sprint 9 execution sequence step 12 (per Sprint 8.5 §3.4 precedent).
- [ ] Vlad will handle all saving; plugin issues no save commands.
- [ ] Vlad handles workbook versioning outside the spec; no workbook filenames in spec.
