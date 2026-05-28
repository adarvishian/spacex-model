# Sprint 10 Spec — Allocator brain light-up

**Sprint name**: Allocator brain light-up — Cash Pool Tracker + Queue Gate + Cash IRR sigmoid + Kg IRR sigmoid + Vehicle build claim + Central IRR display + First-year override + R108/R109 activation.

**Status**: spec-author chat, drafted 2026-05-26 from Sprint Roadmap §3 Sprint 10 + Architecture §6.1–§6.6 + Architecture §15.2 + Vlad locks 2026-05-26 (7 architectural decisions).

**Dependencies landed**: Sprint 1 (Allocator skeleton — reserved row ranges R7–R165). Sprint 7 (Allocator §3 Mars/Moon carve-out R32–R37, post-Sprint-9 R34 fix in place). Sprint 8 + Sprint 8.5 (OpEx + CapEx tabs; CapEx R44 vehicle build placeholder = $0 awaiting this sprint). Sprint 9 (Group P&L full walk + R99–R110 conservation block; PASS exact 2026-05-22 — D26=$4,904M, D50=−$2,569M, D108="OK", D110=−$454M memo).

**Sprint 6 (AI Stack) deferred**: IFERROR-0 wraps throughout this spec. AI Stack module's R207/R208/R209 IRR reads = 0; AI Stack R210 Capacity Demand = 0; AI Stack kg demand = 0 (Architecture §10.4 — terrestrial).

**Iterative calc**: ON workbook-wide (confirmed pre-flight). Sprint 10 introduces the largest within-year cycle to date: Available cash → Module cash allocation → Module CapEx → Module COGS → Module FCF → Group FCF (next year via prior-year FCF read at R34). Cycle is broken by prior-year FCF in cash pool tracker (Mars carve-out uses prior-year FCF per Assumptions R14 = 1).

---

## §0 Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md` and the four constitutional docs. Each box ticked or justified before plugin execution.

- [x] **Rule 1** (one concept per write) — every §3.x section structures writes as separate blocks: column-A labels, formulas (D-col then E-col copy-across), number formats. Cash Pool Tracker, Queue Gate, Cash sigmoid, Kg sigmoid, Vehicle build claim, Central IRR display each ship as discrete write blocks.
- [x] **Rule 3 / 23** (formula pattern) — Cash Pool Tracker Cash BoY chain is a Rule 23 EXCEPTION (year-chained: `Cash BoY(N) = Cash BoY(N−1) + Group FCF(N−1) + IPO(N)`); justification inline in §3.1. All other ramp formulas use anchor-and-offset against Assumptions §2 inputs. Sigmoid weight formulas use `MAX(IRR, 0)^k` against Assumptions!R16 anchor.
- [x] **Rule 4** (verification gate) — every §3.x section ends with explicit D / I / S / AC read-backs + expected values. §4 Verification protocol consolidates the full §6.9 calibration check.
- [x] **Rule 6** (inline formulas) — every cell write in §3.1–§3.9 is specified with the full Excel formula. No convention references.
- [x] **Rule 10** (no row insertions) — all Sprint 10 writes land in Sprint 1's reserved row ranges (R8–R15, R18–R29, R40–R80, R90–R130, R140–R150, R153–R165) + R83–R87 + R133–R137. No `insert_row` anywhere. R108 amendment replaces existing formula in place (single-cell edit). R109 amendment replaces placeholder in place.
- [x] **Rule 11** (touch points) — every new canonical row enumerates: (1) section Total / sigmoid Σ row (where applicable), (2) downstream consumer (Group P&L R109 cash identity reads Cash BoY; CapEx R44 reads Vehicle build claim; Module IN R8/R9 read R83–R87 + R133–R137), (3) conservation check (R108 extended to R109), (4) §6.9 calibration line.
- [x] **Rule 12** (label-based cross-tab refs) — every cross-tab pull resolves via `INDEX(Sheet!D:D, MATCH("Canonical Label", Sheet!$A:$A, 0))`. Year-row offset reads use `INDEX(Sheet!$D:$AC, MATCH(label, Sheet!$A:$A, 0), D$5+1)` pattern. Canonical labels enumerated in §3 each section header.
- [x] **Rule 13** (vending-machine test) — N/A. Sprint 10 is allocator-only. No module-tab writes. Per Lock (e) audit-only, defer R110 fix to module-owner sprint (Principle 10).
- [x] **Rule 14** (no hardcoded constants) — every behaviour input lives on Assumptions §2 ALLOCATOR (R8 Starting cash, R9 IPO amount, R10 IPO year, R12 Mars %, R13 Mars floor, R14 carve-out prior-year flag, R16 Sigmoid_k, R17 Forward_weight w, R18 Forward horizon, R19–R23 per-module N, R25 vehicle build toggle, R26 lead time, R27 launches per vehicle per year, R28 masked-demand default, R29 demand growth cap). First-year override (Lock a): Allocator R83–R87 column D reads each module's `Module CapEx ($mm)` row at column D via INDEX/MATCH — module-tab-sourced historical actual, not a behaviour constant. Inline numeric literals: only `0` (kg override column D for all 5 modules + AI Stack kg demand structural 0) and `1` (R108 boolean ABS<1 threshold). Both flagged as structural in spec text.
- [x] **Rule 15** (sanity check halt thresholds) — every sanity check in §4 has a quantitative halt threshold. Cash BoY 2025 = $5,000M exact (halt if differs); Mars carve-out 2025 = $1,000M floor exact (halt if differs); Available cash 2025 ≥ 0 and ≤ Cash BoY (halt if negative or >Cash BoY); Σ cash sigmoid shares ≤ 1 within rounding (halt if >1.01 or any module's share < 0); R108 = "OK" every year 2025–2050 (mandatory halt); Group P&L D26 EBITDA = $4,904M ±5% post-allocator-light-up (halt if drift); Group P&L D50 FCF = −$2,569M ±10% (halt if drift).
- [x] **Rule 19** (save-as) — standing rule locked 2026-05-20: Vlad handles all saving. Spec does NOT name target workbook. Plugin operates on the live open workbook session.
- [x] **Rule 22** (stale-ref scan) — §4 Verification §4.4 explicit Rule 22 scan: every cross-tab pull (Allocator → Group P&L, Allocator → OpEx, Allocator → CapEx, Allocator → Launch Capacity, Allocator → 5 module tabs for IRR + Capacity Demand reads) verified against source column-A label. Plus reverse direction: 5 module IN cells (R8, R9 on each of 5 module tabs) verified to resolve to non-zero values post-Sprint-10.

**Architecture & Methodology compliance:**

- [x] Cash Pool Tracker follows Architecture §6.1 verbatim: Starting cash + IPO injection + prior-year Group FCF = Cash BoY. Mars carve-out uses prior-year FCF (R14 flag = 1).
- [x] Queue Gate follows Architecture §6.2 verbatim: Available cash = MAX(0, Cash BoY − Σ year-N non-module claims). Non-module claims = OpEx + Corp CapEx + Spectrum CapEx + Taxes + Mars carve-out + Vehicle build claim (this sprint).
- [x] Cash sigmoid follows Architecture §6.3 verbatim: `masked_demand_M = IF(IRR_M > 0, demand_M, 0); weight_M = MAX(IRR_M, 0)^k; share_M = weight_M / Σ; allocation_M = MIN(masked_demand_M, Available × share_M)`. Strict IRR > 0 cutoff. Σ shares ≤ 1 by construction.
- [x] Kg sigmoid follows Architecture §6.4 verbatim: same architecture, same k, on Starship kg-to-LEO. Lunar Mars kg reserved off-the-top (Architecture §11.3). AI Stack kg demand = 0 (Architecture §10.4). Customer Launch kg demand = external customer Starship only.
- [x] Vehicle build claim follows Architecture §6.6 verbatim: `forward_demand(T) = Σ module Capacity Demand at year T+lead; lead = Assumptions!R26 = 2 yrs; projected_capacity(T+lead) = Launch Capacity!R34 at T+lead; capacity_gap = MAX(0, forward_demand − projected_capacity); required_vehicles = capacity_gap / payload_per_launch / launches_per_vehicle_per_year; claim = required_vehicles × blended_build_cost`. Sized claim feeds Queue Gate and CapEx R44.
- [x] Central IRR display follows Architecture §6 + §11.6 verbatim: reads each module's R207/R208/R209 Spot/Forward/Blended IRR; Lunar Mars hardcoded 0 (no IRR engine per §11.6).
- [x] R108 amendment follows Architecture §15.2 verbatim: `AND(ABS(R99:R107)<1, ABS(R109)<1)` — Lock (c).
- [x] R109 simplified follows Sprint 9 Lock 'a' logic: Mars carve-out + Module CapEx already inside Group FCF per Group walk; single subtraction at Cash EoY only — Lock (d).
- [x] First-year override (Lock a): Allocator R83–R87 column D + R133–R137 column D pre-empted by historical actuals; allocator drives E:AC (2026+) only.
- [x] Year-offset helper row at row 5 on Allocator (D5=0, E5=1, …, AC5=25). All year-row formulas use the offset. Allocator!D4:AC4 = year headers 2025..2050.
- [x] ZERO `OFFSET()` formulas in Sprint 10 writes. Cumulative running-sum reads use `SUMIF($D$5:D$5, "<="&D$5, [range])` or `SUM(INDEX(range, 1) : INDEX(range, D$5+1))`. Year-row INDEX reads use `INDEX(Sheet!$D:$AC, MATCH(label, Sheet!$A:$A, 0), D$5+1)`. Prior-year reads use `INDEX(..., D$5)` with `IF(D$5=0, 0, ...)` guard for col_num=0.

If any box is unchecked, spec author justifies or amends before plugin execution begins.

---

## §1 Scope summary

| Section | Allocator rows | Architecture ref | What ships |
|---|---|---|---|
| §3.0 Pre-flight | n/a | Sprint 9 PASS check + Sprint 7 §3 audit + iterative calc + canonical labels | Plugin halts if any pre-flight check fails |
| §3.1 Cash Pool Tracker | R8–R15 | Architecture §6.1 | Starting cash; IPO injection; prior-year Group FCF read; Cash BoY year-chained |
| §3.2 Queue Gate | R18–R29 | Architecture §6.2 | OpEx claim; Corp CapEx claim; Spectrum CapEx claim; Taxes claim; Mars carve-out claim; Vehicle build claim read; Total non-module claims; Available cash for IRR queue |
| §3.3 Cash IRR sigmoid queue | R40–R80 | Architecture §6.3 | Per-module Blended IRR read; cash demand; masked demand; weight; share; allocation (5 modules × ~8 rows = 40 rows in queue) |
| §3.4 Module cash allocation canonical rows | R83–R87 | Architecture §4 + §6.3 | 5 canonical labels (Customer Launch, Starlink, ODC, AI Stack, Lunar Mars cash allocation). Column D = first-year override; E:AC = sigmoid output. Module IN R8 reads these. |
| §3.5 Kg IRR sigmoid queue | R90–R130 | Architecture §6.4 | Total Starship capacity read; Lunar Mars kg reserved (Architecture §11.3); Capacity available for queue; per-module sub-blocks (4 modules in queue × ~9 rows; Lunar Mars OUTSIDE queue) |
| §3.6 Module kg allocation canonical rows | R133–R137 | Architecture §4 + §6.4 | 5 canonical labels. Column D = 0 (no 2025 Starship kg); E:AC = sigmoid output (or 0 for Lunar Mars off-the-top + AI Stack terrestrial). Module IN R9 reads these. |
| §3.7 Vehicle build claim | R140–R150 | Architecture §6.6 | Forward aggregate kg demand at T+2; projected capacity at T+2; capacity gap; required vehicles; vehicle build claim ($mm) |
| §3.8 Central IRR display | R153–R165 | Architecture §6 + §11.6 | Per-module Spot / Forward / Blended IRR memo rows; sigmoid share memo rows; allocation summary |
| §3.9 R108 + R109 activation | Group P&L R108, R109 | Architecture §15.2 | R108 extended to include R109; R109 cash flow identity activated per Lock (d) simplified form |

**Publishes 6 canonical label classes** (Rule 12 — verbatim case-sensitive, halt on drift):
1. `Cash BoY ($mm)` — Allocator R15 (read by Sprint 11 Valuation, R109 cash identity)
2. `Available cash for IRR queue ($mm)` — Allocator R29 (read by Sprint 11 deployment audit)
3. `Vehicle build claim ($mm)` — Allocator R150 (read by CapEx R44 to switch from $0 placeholder to live)
4. `[Module] cash allocation` × 5 — Allocator R83–R87 (read by 5 module IN R8 cells)
5. `[Module] kg allocation` × 5 — Allocator R133–R137 (read by 5 module IN R9 cells)
6. `Year-N non-module claims ($mm)` — Allocator R28 (read by Sprint 11 deployment audit)

---

## §2 Constitutional reference

Sprint 10 reads from but does not modify (Principle 10):
- **Architecture §6.1 Cash Pool Tracker** — Cash BoY year-chain (Rule 23 EXCEPTION).
- **Architecture §6.2 Queue Gate** — Available cash = MAX(0, Cash BoY − Σ non-module claims).
- **Architecture §6.3 Cash IRR sigmoid** — `masked_demand_M = IF(IRR_M > 0, demand_M, 0); weight_M = MAX(IRR_M, 0)^k`.
- **Architecture §6.4 Kg IRR sigmoid** — same architecture on Starship kg-to-LEO; Lunar Mars off-the-top.
- **Architecture §6.6 Vehicle build claim** — forward-aggregate kg demand at T+lead.
- **Architecture §11.3 Lunar Mars kg reservation** — `(Lunar ships + Mars ships) × payload × (1 + depot_multiplier)`.
- **Architecture §11.6 Lunar Mars IRR rows = 0** — strategic carve-out, no IRR engine.
- **Architecture §15.2 Conservation block** — R108 boolean; R109 cash flow identity.
- **Lessons §4** — Queue gate non-module claims LOAD-BEARING. Year-N OpEx + Corp CapEx + Spectrum + Taxes + Mars carve-out + Vehicle build reserved before module CapEx allocation.
- **Lessons §22** — Within-year cycle bistability. Sprint 10 introduces the biggest cycle yet: module CapEx ← Allocator allocation ← module IRR ← module FCF ← module CapEx. Per-sat IRR is fleet-independent so cycle should converge — verify <10 iter post-write + 5x round-trip stability test.

---

## §3 Execution

### §3.0 Pre-flight (READ-ONLY — halt if any check fails)

Plugin executes 9 pre-flight checks. All must pass before any write.

**Check 1 — Sprint 9 Group P&L PASS values intact:**
```
Read Group P&L D10  expect $15,137M ±$50M (Group Revenue net of elims)
Read Group P&L D18  expect $9,463M ±$50M (Group Gross Profit)
Read Group P&L D26  expect $4,904M ±$50M (Group EBITDA)
Read Group P&L D28  expect $1,261M ±$50M (Group D&A)
Read Group P&L D50  expect -$2,569M ±$50M (GROUP FCF)
Read Group P&L D108 expect "OK" exact
Read Group P&L D110 expect -$454M ±$50M (Σ Module FCF residual memo; Lock e baseline)
```
If any value drifts beyond tolerance: HALT, push back to Vlad with actual vs expected.

**Check 2 — Sprint 7 Allocator §3 R32–R37 audit (Lock b):**
```
MATCH-probe Allocator A32 expect "Mars carve-out % of prior-year Group FCF (input)"
MATCH-probe Allocator A33 expect "Mars carve-out floor ($mm/yr) (input)"
MATCH-probe Allocator A34 expect "Prior-year Group FCF read ($mm/yr)"
MATCH-probe Allocator A35 expect "Mars/Moon strategic carve-out ($mm/yr)"
MATCH-probe Allocator A36 expect "Lunar share of carve-out (% — year-row)"
MATCH-probe Allocator A37 expect "Mars share of carve-out (% — year-row)"
Read formula text Allocator D34 expect substring "D$5" AND substring "GROUP FCF ($mm)"
Read Allocator D34 value expect 0 exact
Read Allocator E34 value expect -$2,569M ±$50M (= prior-year 2025 GROUP FCF)
Read Allocator D35 value expect $1,000M exact (floor)
```
If any check fails: HALT, push back to Vlad — Sprint 7 §3 must be re-fixed before Sprint 10 proceeds.

**Check 3 — Iterative calc workbook setting:**
```
Read workbook calculation.iterate expect True
(iterateCount + iterateDelta = Excel defaults are acceptable per Sprint 4 lock)
```
If iterate = False: HALT, push back — workbook setting must be ON.

**Check 4 — 7 Sprint 9 canonical labels on Group P&L resolve verbatim:**
```
MATCH Group P&L "GROUP REVENUE NET OF ELIMS ($mm)" expect row 10
MATCH Group P&L "Group Gross Profit ($mm)" expect row 18
MATCH Group P&L "Group EBITDA ($mm)" expect row 26
MATCH Group P&L "Group D&A ($mm)" expect row 28
MATCH Group P&L "Group EBIT ($mm)" expect row 30
MATCH Group P&L "Taxes ($mm)" expect row 32
MATCH Group P&L "Total Group CapEx ($mm)" expect row 46
MATCH Group P&L "GROUP FCF ($mm)" expect row 50
```
If any returns #N/A: HALT — label drift since Sprint 9. Run Sprint 9 §3.5 canonical label list audit before proceeding.

**Check 5 — Module IRR rows R207/R208/R209 resolve on all 5 module tabs:**
```
For each tab in {Customer Launch, Starlink, ODC, AI Stack, Lunar Mars}:
  MATCH tab!"Spot IRR" expect row 207
  MATCH tab!"Forward IRR (Y+2)" expect row 208
  MATCH tab!"Blended IRR" expect row 209
  MATCH tab!"Capacity Demand (kg-to-LEO)" expect row 210
  MATCH tab!"Module CapEx ($mm)" expect row 205
```
If any returns #N/A: HALT — module Allocator OUT block drift since Sprint 7. Audit module tab before proceeding.

**Check 6 — Launch Capacity canonical labels resolve:**
```
MATCH Launch Capacity!"Total Annual Capacity (kg-to-LEO)" expect row 34
MATCH Launch Capacity!"Per-launch upmass (kg)" expect row 29
MATCH Launch Capacity!"Super Heavy manufacturing cost ($mm/unit)" expect row 8
MATCH Launch Capacity!"Starship 2nd-stage manufacturing cost ($mm/unit)" expect row 9
```
If any returns #N/A: HALT — Sprint 2 Launch Capacity label drift.

**Check 7 — OpEx + CapEx + Taxes canonical labels resolve:**
```
MATCH OpEx!"Total OpEx ($mm)" expect row 53
MATCH CapEx!"Total Corporate CapEx ($mm)" expect row 25
MATCH CapEx!"EchoStar mid-band CapEx ($mm)" expect row 39
MATCH CapEx!"Vehicle build claim ($mm) — placeholder for Sprint 10" expect row 44 (Sprint 10 amends this label below)
MATCH Group P&L!"Taxes ($mm)" expect row 32
```
If any returns #N/A: HALT.

**Check 8 — Assumptions §2 ALLOCATOR inputs intact:**
```
Read Assumptions!B8 expect 5000 (Starting cash)
Read Assumptions!B9 expect 30000 (IPO amount)
Read Assumptions!B10 expect 2027 (IPO year)
Read Assumptions!B12 expect 0.15 (Mars %)
Read Assumptions!B13 expect 1000 (Mars floor)
Read Assumptions!B14 expect 1 (prior-year FCF flag)
Read Assumptions!B16 expect 2 (Sigmoid_k)
Read Assumptions!B17 expect 0.70 (Forward_weight)
Read Assumptions!B25 expect 1 (Vehicle build claim toggle)
Read Assumptions!B26 expect 2 (Vehicle build lead time)
Read Assumptions!B27 expect 24 (Launches per Starship vehicle per year)
Read Assumptions!B29 expect 2 (demand growth cap)
```
If any drifts: HALT, push back — Sprint 10 sigmoid + queue gate + vehicle build sizing depends on these.

**Check 9 — Sprint 1 Allocator skeleton intact:**
```
Read Allocator R7 col A expect "§1 CASH POOL TRACKER"
Read Allocator R17 col A expect "§2 QUEUE GATE"
Read Allocator R31 col A expect "§3 MARS/MOON STRATEGIC CARVE-OUT"
Read Allocator R39 col A expect "§4 CASH IRR-PRIORITY SIGMOID QUEUE"
Read Allocator R82 col A expect "§5 MODULE CASH ALLOCATIONS (canonical labels — read by module IN blocks)"
Read Allocator R89 col A expect "§6 KG IRR-PRIORITY SIGMOID QUEUE"
Read Allocator R132 col A expect "§7 MODULE KG ALLOCATIONS (canonical labels — read by module IN blocks)"
Read Allocator R139 col A expect "§8 VEHICLE BUILD CLAIM"
Read Allocator R152 col A expect "§9 CENTRAL IRR DISPLAY"
Read Allocator R83 col D expect 0 (placeholder)
Read Allocator R134 col D expect 0 (placeholder)
```
If section headers missing or placeholders altered: HALT.

If all 9 checks pass: proceed to §3.1.

---

### §3.1 Allocator §1 Cash Pool Tracker (R8–R15)

**Architecture §6.1 verbatim.** Year-chained Rule 23 EXCEPTION (Cash BoY recursion). Justification: cash position carries year-to-year by definition; anchor-and-offset would require a cumulative running-sum that's mathematically equivalent but less readable. Per Architecture §6.1, prior-year reads break the Mars-carve-out circularity (R14 = 1 flag).

**Writes (one write block per row; Rule 1):**

| Row | Col A label (verbatim) | Col D formula | Col E formula | Copy E across F:AC | Number format |
|---|---|---|---|---|---|
| R7 | (existing) `§1 CASH POOL TRACKER` | — | — | — | bold section header |
| R8 | `Starting cash position EoY 2024 ($mm)` | `=IF(D$5=0, INDEX(Assumptions!$B:$B, MATCH("Starting cash position EoY 2024 ($mm)", Assumptions!$A:$A, 0)), 0)` | `=0` | yes | `#,##0;[Red](#,##0)` |
| R9 | `IPO injection this year ($mm)` | `=IF(D$4=INDEX(Assumptions!$B:$B, MATCH("IPO injection year", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("IPO injection amount ($mm)", Assumptions!$A:$A, 0)), 0)` | `=IF(E$4=INDEX(Assumptions!$B:$B, MATCH("IPO injection year", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("IPO injection amount ($mm)", Assumptions!$A:$A, 0)), 0)` | yes | `#,##0;[Red](#,##0)` |
| R10 | `Prior-year Group FCF read ($mm)` | `=IFERROR(IF(D$5=0, 0, INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF ($mm)", 'Group P&L'!$A:$A, 0), D$5)), 0)` | `=IFERROR(IF(E$5=0, 0, INDEX('Group P&L'!$D:$AC, MATCH("GROUP FCF ($mm)", 'Group P&L'!$A:$A, 0), E$5)), 0)` | yes | `#,##0;[Red](#,##0)` |
| R15 | `Cash BoY ($mm)` | `=D8+D9+D10` | `=D15+E10+E9` | yes — formula references prior column R15 + current column R10 (prior-year FCF) + current column R9 (this year's IPO) | `#,##0;[Red](#,##0)` |

**Cash BoY year-chain formula explained (Rule 23 EXCEPTION inline justification):**
- D15 (2025) = D8 ($5,000M starting) + D9 ($0 IPO in 2025) + D10 ($0 prior-year FCF — 2024 not in horizon) = **$5,000M exact** (matches §6.9 calibration target).
- E15 (2026) = D15 ($5,000M prior Cash BoY) + E10 (-$2,569M = 2025 Group FCF) + E9 ($0 IPO in 2026) = **$2,431M**.
- F15 (2027) = E15 ($2,431M) + F10 (= 2026 Group FCF) + F9 ($30,000M IPO in 2027) ≈ **$30,371M** (pre-flight Group P&L 2026 FCF = -$2,060M → F15 ≈ $30,371M, within §6.9 "~$15–25B" range — slightly above due to IPO landing same year).
- Pattern continues: each year's BoY = prior BoY + prior-year FCF + this-year IPO. IPO is a one-time event in 2027 only.

**Note**: R10 (Prior-year Group FCF read) duplicates Allocator R34 by-design — Sprint 7 already wrote R34 with the same formula structure. R10 is the canonical Cash Pool Tracker input; R34 is the Mars carve-out input. Both read Group P&L R50 with year-offset lookback. Pre-flight Check 2 confirms R34 is intact; this sprint adds R10 as a parallel read. R10 + R34 differ only in their downstream consumers — not a duplicate logic concern.

**Verification reads (Rule 4 + Rule 16):**
- D15 expect **$5,000M** exact (§6.9 calibration anchor)
- E15 expect **$2,431M** ±$100M
- F15 expect **~$30,371M** ±$500M (depends on 2026 FCF)
- I15 (2030) expect **~$45,000M–$55,000M** range (cumulative cash buildup post-IPO)
- AC15 (2050) expect terminal cash position — informational

**Halt condition (Rule 15)**: D15 ≠ $5,000M exact → HALT.

---

### §3.2 Allocator §2 Queue Gate (R18–R29)

**Architecture §6.2 verbatim.** Available cash = MAX(0, Cash BoY − Year-N non-module claims).

**Writes:**

| Row | Col A label (verbatim) | Col D formula | Col E formula | Copy E across F:AC | Number format |
|---|---|---|---|---|---|
| R17 | (existing) `§2 QUEUE GATE` | — | — | — | bold section header |
| R18 | `OpEx claim ($mm)` | `=IFERROR(INDEX(OpEx!$D:$AC, MATCH("Total OpEx ($mm)", OpEx!$A:$A, 0), D$5+1), 0)` | `=IFERROR(INDEX(OpEx!$D:$AC, MATCH("Total OpEx ($mm)", OpEx!$A:$A, 0), E$5+1), 0)` | yes | `#,##0;[Red](#,##0)` |
| R19 | `Corporate CapEx claim ($mm)` | `=IFERROR(INDEX(CapEx!$D:$AC, MATCH("Total Corporate CapEx ($mm)", CapEx!$A:$A, 0), D$5+1), 0)` | `=IFERROR(INDEX(CapEx!$D:$AC, MATCH("Total Corporate CapEx ($mm)", CapEx!$A:$A, 0), E$5+1), 0)` | yes | `#,##0;[Red](#,##0)` |
| R20 | `Spectrum CapEx claim ($mm)` | `=IFERROR(INDEX(CapEx!$D:$AC, MATCH("EchoStar mid-band CapEx ($mm)", CapEx!$A:$A, 0), D$5+1), 0)` | `=IFERROR(INDEX(CapEx!$D:$AC, MATCH("EchoStar mid-band CapEx ($mm)", CapEx!$A:$A, 0), E$5+1), 0)` | yes | `#,##0;[Red](#,##0)` |
| R21 | `Taxes claim ($mm)` | `=IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("Taxes ($mm)", 'Group P&L'!$A:$A, 0), D$5+1), 0)` | `=IFERROR(INDEX('Group P&L'!$D:$AC, MATCH("Taxes ($mm)", 'Group P&L'!$A:$A, 0), E$5+1), 0)` | yes | `#,##0;[Red](#,##0)` |
| R22 | `Mars/Moon carve-out claim ($mm)` | `=D35` | `=E35` | yes — reads Sprint 7 R35 canonical row directly (same-tab read, no INDEX/MATCH needed) | `#,##0;[Red](#,##0)` |
| R23 | `Vehicle build claim ($mm)` | `=D150` | `=E150` | yes — reads Allocator §8 R150 (this sprint's §3.7 output) | `#,##0;[Red](#,##0)` |
| R28 | `Year-N non-module claims ($mm)` | `=SUM(D18:D23)` | `=SUM(E18:E23)` | yes | `#,##0;[Red](#,##0)` — **CANONICAL LABEL** (Sprint 11 reads) |
| R29 | `Available cash for IRR queue ($mm)` | `=MAX(0, D15 - D28)` | `=MAX(0, E15 - E28)` | yes | `#,##0;[Red](#,##0)` — **CANONICAL LABEL** (Sprint 11 reads) |

**Verification reads:**
- D18 (OpEx 2025) expect **$4,560M** ±$50M
- D19 (Corp CapEx 2025) expect **$110M** ±$10M
- D20 (Spectrum 2025) expect **$5,000M** exact
- D21 (Taxes 2025) expect **$934M** ±$50M
- D22 (Mars carve-out 2025) expect **$1,000M** exact (floor)
- D23 (Vehicle build claim 2025) expect **~$60M** ±$100M (pre-computed; see §3.7)
- D28 (Total non-module claims 2025) expect **~$11,664M** ±$200M
- D29 (Available cash for IRR queue 2025) expect **$0 exact** (claims $11.7B > Cash BoY $5B → MAX(0, neg) = 0; matches §6.9 "likely 0")
- I29 (Available cash 2030) expect **substantial > $20B** range (Cash BoY ~$45–55B − claims ~$15–25B)

**Halt conditions (Rule 15):**
- D22 ≠ $1,000M exact → HALT (Mars carve-out floor breach indicates R35 read drift).
- D29 < 0 → HALT (MAX should clip to 0).
- D29 > D15 → HALT (Available cash cannot exceed Cash BoY).

---

### §3.3 Allocator §4 Cash IRR sigmoid queue (R40–R80)

**Architecture §6.3 verbatim.** Per-module sub-blocks (8 rows each × 4 in-queue modules = 32 rows + 1 Σ row at R80). Lunar Mars OUTSIDE queue (Architecture §11).

**Layout (per module sub-block, 8 rows):**
```
Row N+0: [Module] sub-block header (col A label only, italic)
Row N+1: [Module] Blended IRR (live read)
Row N+2: [Module] cash demand ($mm)
Row N+3: [Module] masked demand ($mm) = IF(IRR > 0, demand, 0)
Row N+4: [Module] weight = MAX(IRR, 0)^k
Row N+5: [Module] share = weight / Σ weights
Row N+6: [Module] proposed allocation = MIN(masked demand, Available × share)
Row N+7: (spacer / memo)
```

**Sub-block row ranges:**
- R40–R47: Customer Launch
- R48–R55: Starlink (uses MODULE-LEVEL Blended IRR R209 — per-vehicle V2 BB/V2 DTC/V3 BB/V3 DTC IRRs are memo R213/R218/R223/R228 on Starlink tab; cash queue allocates to Starlink as a single module)
- R56–R63: ODC
- R64–R71: AI Stack (IFERROR-0 wrap throughout — Sprint 6 deferred)
- R72–R79: (spacer / future expansion)
- R80: Σ weights (denominator for shares) = `=SUM(D44, D52, D60, D68)` (sum of all 4 module weight rows)

**Cash demand source** (cash_demand_M reads each module's `Module CapEx ($mm)` row R205 — this is the module's internal CapEx ask in the absence of allocator constraint):

| Module | Cash demand formula (D-col; copy E:AC) |
|---|---|
| Customer Launch | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Module CapEx ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1), 0)` |
| Starlink | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("Module CapEx ($mm)", Starlink!$A:$A, 0), D$5+1), 0)` |
| ODC | `=IFERROR(INDEX(ODC!$D:$AC, MATCH("Module CapEx ($mm)", ODC!$A:$A, 0), D$5+1), 0)` |
| AI Stack | `=IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Module CapEx ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)` |

**Detailed writes per sub-block (template — Customer Launch as exemplar; repeat for Starlink, ODC, AI Stack with row offset + tab name swap):**

| Row | Col A | D formula | Number format |
|---|---|---|---|
| R40 | `▸ Customer Launch (in-queue module)` | — (label only) | italic |
| R41 | `Customer Launch Blended IRR` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Blended IRR", 'Customer Launch'!$A:$A, 0), D$5+1), 0)` | `0.0%` |
| R42 | `Customer Launch cash demand ($mm)` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Module CapEx ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1), 0)` | `#,##0` |
| R43 | `Customer Launch masked demand ($mm)` | `=IF(D41>0, D42, 0)` | `#,##0` |
| R44 | `Customer Launch weight` | `=MAX(D41, 0)^INDEX(Assumptions!$B:$B, MATCH("Sigmoid IRR-blend exponent k", Assumptions!$A:$A, 0))` | `0.0000` |
| R45 | `Customer Launch share` | `=IFERROR(D44/D80, 0)` | `0.0%` |
| R46 | `Customer Launch proposed allocation ($mm)` | `=MIN(D43, D29*D45)` | `#,##0` |
| R47 | (spacer) | — | — |

**Starlink sub-block (R48–R55):** same structure, swap tab name `Starlink`, swap module name `Starlink` in col A labels. R52 = weight row referenced by Σ R80.

**ODC sub-block (R56–R63):** same structure, swap to `ODC`. R60 = weight row.

**AI Stack sub-block (R64–R71):** same structure with **explicit IFERROR-0 wrap** on EVERY formula (Sprint 6 deferred — Module CapEx + IRR + Capacity Demand all return 0; ensure no #DIV/0 propagation):
- R65 (AI Stack Blended IRR): `=IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Blended IRR", 'AI Stack'!$A:$A, 0), D$5+1), 0)`
- R66 (cash demand): same with IFERROR
- R67 (masked demand): `=IF(D65>0, D66, 0)` — returns 0 either way since D65 = 0
- R68 (weight) = `=MAX(D65, 0)^INDEX(Assumptions!$B:$B, MATCH("Sigmoid IRR-blend exponent k", Assumptions!$A:$A, 0))` — returns 0
- R69 (share) = `=IFERROR(D68/D80, 0)` — returns 0
- R70 (proposed allocation) = `=MIN(D67, D29*D69)` — returns 0

**Σ weights row R80:**
`=D44 + D52 + D60 + D68` (sum of 4 module weights — Customer Launch + Starlink + ODC + AI Stack; Lunar Mars excluded per Architecture §11)

**Verification reads:**
- D41 (Customer Launch Blended IRR 2025) expect **2.7270** (pre-flight read; positive → in queue) ±0.05
- D49 (Starlink Blended IRR 2025) expect **0.7624** ±0.05
- D57 (ODC Blended IRR 2025) expect **-0.2969** (negative → masked to 0 → no allocation)
- D65 (AI Stack Blended IRR 2025) expect **0** exact (deferred)
- D44 (Customer Launch weight 2025) expect `2.7270^2 ≈ 7.4366` ±0.5
- D52 (Starlink weight 2025) expect `0.7624^2 ≈ 0.5813` ±0.05
- D60 (ODC weight 2025) expect **0** (negative IRR → MAX(IRR,0)^k = 0)
- D68 (AI Stack weight 2025) expect **0**
- D80 (Σ weights 2025) expect **~8.02** ±0.5
- D45 (Customer Launch share 2025) expect **~0.927** (= 7.4366 / 8.02)
- D53 (Starlink share 2025) expect **~0.072** (= 0.5813 / 8.02)
- D46 (Customer Launch proposed allocation 2025) expect **0** exact (D29 Available cash = 0 → D29 × share = 0; MIN(masked, 0) = 0)
- D54 (Starlink proposed allocation 2025) expect **0**

**Halt conditions (Rule 15):**
- D45 + D53 + D61 + D69 > 1.01 → HALT (shares should sum to ≤ 1 by construction; 1.0 exact when all in-queue modules have IRR > 0, less otherwise).
- D46 + D54 + D62 + D70 > D29 → HALT (Σ allocations cannot exceed Available cash).

---

### §3.4 Allocator §5 Module cash allocation canonical rows (R83–R87)

**Canonical labels Sprint 1 already wrote at R83–R87 (col A intact, col D:AC currently literal 0). Sprint 10 replaces col D:AC with live formulas.**

**First-year override convention (Lock a)**: column D = each module's Module CapEx 2025 read from module tab (historical actual, S-1-anchored via Vlad's module-tab values). Column E:AC = live sigmoid allocation from R46/R54/R62/R70.

| Row | Col A label (verbatim — DO NOT CHANGE; Sprint 1 published) | Col D formula | Col E formula | Copy E across F:AC | Note |
|---|---|---|---|---|---|
| R83 | `Customer Launch cash allocation` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Module CapEx ($mm)", 'Customer Launch'!$A:$A, 0), 1), 0)` | `=D46` | yes — column E reads sigmoid output cell directly (same-tab read, relative ref shifts F→F46, …, AC→AC46) | First-year override on column D reads Customer Launch D205 directly (col_num=1 → D-col → 2025 value). Vlad's S-1 import work on Customer Launch tab determines this value. |
| R84 | `Starlink cash allocation` | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("Module CapEx ($mm)", Starlink!$A:$A, 0), 1), 0)` | `=D54` | yes | Same pattern; reads Starlink D205. |
| R85 | `ODC cash allocation` | `=IFERROR(INDEX(ODC!$D:$AC, MATCH("Module CapEx ($mm)", ODC!$A:$A, 0), 1), 0)` | `=D62` | yes | Same pattern. ODC 2025 historical = 0 (pre-revenue). |
| R86 | `AI Stack cash allocation` | `=IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Module CapEx ($mm)", 'AI Stack'!$A:$A, 0), 1), 0)` | `=D70` | yes | Same pattern. AI Stack 2025 = 0 (deferred). |
| R87 | `Lunar Mars cash allocation` | `=D35*D36` | `=E35*E36` | yes — reads Sprint 7 R35 (strategic carve-out total) × R36 (Lunar share — but Lunar Mars allocation = TOTAL carve-out, not Lunar-only; revisit) | **NOTE**: Lunar Mars module cash allocation = total Mars/Moon strategic carve-out = R35 (Sprint 7 carved out full $1B in 2025 → $1B allocated to Lunar Mars module). Architecture §11 has Lunar + Mars sharing the carve-out cash via R36/R37 shares. For Sprint 10 simplicity: R87 = D35 (total carve-out reaches Lunar Mars module; module internally splits Lunar vs Mars via Sprint 7's R36/R37 already wired). |

**Reconsidering R87 (Lunar Mars cash allocation)**: Sprint 7 already routed Mars/Moon carve-out cash into the Lunar Mars module via the carve-out value in R35. The Lunar Mars module tab internally splits R35 between Lunar and Mars deployment using R36/R37 shares. Sprint 10's Allocator R87 should just publish the canonical label for Module IN R8 to read — which equals R35. **Final R87 formula: `=D35` (D-col) / `=E35` (E-col, copy across F:AC).**

Updated row R87:

| R87 | `Lunar Mars cash allocation` | `=D35` | `=E35` | yes | Strategic carve-out total — same value as Allocator §3 R35; Lunar Mars module tab splits internally via Sprint 7 R36/R37. |

**Verification reads:**
- D83 (Customer Launch cash allocation 2025) expect **$32.86M** (= Customer Launch!D205 historical)
- D84 (Starlink cash allocation 2025) expect **$1,202.54M** (= Starlink!D205 historical)
- D85 (ODC cash allocation 2025) expect **$0** (= ODC!D205 historical = 0; pre-revenue)
- D86 (AI Stack cash allocation 2025) expect **$0** (deferred)
- D87 (Lunar Mars cash allocation 2025) expect **$1,000M** (= D35 floor)
- E83–E87 (2026) expect live sigmoid values from R46/R54/R62/R70/E35 — informational
- AC83–AC87 (2050) expect live sigmoid values — informational

**Touch points (Rule 11):**
- Customer Launch tab R8 reads R83 → Customer Launch module IN cell switches from $0 placeholder to **$32.86M in 2025**, live sigmoid 2026+.
- Starlink tab R8 reads R84 → **$1,202.54M in 2025**, live 2026+.
- ODC tab R8 reads R85 → **$0 in 2025**, live 2026+.
- AI Stack tab R8 reads R86 → **$0 in 2025**, live 2026+ (but AI Stack deferred → reads return 0 via IFERROR).
- Lunar Mars tab R8 reads R87 → **$1,000M in 2025**, live 2026+.

---

### §3.5 Allocator §6 Kg IRR sigmoid queue (R90–R130)

**Architecture §6.4 verbatim.** Same architecture as cash queue (§3.3) applied to Starship kg-to-LEO. Lunar Mars OUTSIDE queue — kg reserved off-the-top per Architecture §11.3.

**Layout:**

| Row | Col A label (verbatim) | Col D formula | Col E formula | Number format |
|---|---|---|---|---|
| R89 | (existing) `§6 KG IRR-PRIORITY SIGMOID QUEUE` | — | — | bold section header |
| R90 | `Total Starship capacity (kg-to-LEO)` | `=IFERROR(INDEX('Launch Capacity'!$D:$AC, MATCH("Total Annual Capacity (kg-to-LEO)", 'Launch Capacity'!$A:$A, 0), D$5+1), 0)` | same with E$5+1 | `#,##0` |
| R91 | `Lunar Mars kg reserved (off-the-top)` | `=IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("Capacity Demand (kg-to-LEO)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)` | same with E$5+1 | `#,##0` |
| R92 | `Capacity available for IRR queue (kg-to-LEO)` | `=MAX(0, D90 - D91)` | `=MAX(0, E90 - E91)` | `#,##0` |
| R94–R101 | Customer Launch sub-block (8 rows; same template as §3.3) | — | — | — |
| R102–R109 | Starlink sub-block | — | — | — |
| R110–R117 | ODC sub-block | — | — | — |
| R118–R125 | AI Stack sub-block (kg demand = 0; terrestrial per Architecture §10.4) | — | — | — |
| R126–R129 | (spacer) | — | — | — |
| R130 | `Σ kg weights` | `=D98 + D106 + D114 + D122` | — | `0.0000` |

**Per-module kg sub-block template (rows R94–R101 = Customer Launch; offset for Starlink, ODC, AI Stack):**

| Row | Col A | D formula | Notes |
|---|---|---|---|
| R94 | `▸ Customer Launch kg sub-block (external Starship demand only)` | — (label) | Customer Launch kg demand = external customers buying Starship launches — read R210. Internal Starlink launches use F9, not external Starship demand. |
| R95 | `Customer Launch Blended IRR` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Blended IRR", 'Customer Launch'!$A:$A, 0), D$5+1), 0)` | Same IRR as cash queue (R41); could reference R41 directly for cleanliness — but explicit re-read avoids cross-section coupling. |
| R96 | `Customer Launch kg demand (kg-to-LEO)` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Capacity Demand (kg-to-LEO)", 'Customer Launch'!$A:$A, 0), D$5+1), 0)` | Customer Launch R210 currently = 0 across all years; pre-flight confirmed. |
| R97 | `Customer Launch kg masked demand` | `=IF(D95>0, D96, 0)` | — |
| R98 | `Customer Launch kg weight` | `=MAX(D95, 0)^INDEX(Assumptions!$B:$B, MATCH("Sigmoid IRR-blend exponent k", Assumptions!$A:$A, 0))` | Same k = 2 as cash queue |
| R99 | `Customer Launch kg share` | `=IFERROR(D98/D130, 0)` | — |
| R100 | `Customer Launch kg proposed allocation` | `=MIN(D97, D92*D99)` | — |
| R101 | (spacer) | — | — |

**Starlink sub-block R102–R109:** same structure; tab swap to `Starlink`. R106 = weight.

**ODC sub-block R110–R117:** same structure; tab swap to `ODC`. R114 = weight.

**AI Stack sub-block R118–R125:** kg demand = 0 (Architecture §10.4 — terrestrial). IFERROR wraps. R122 = weight = 0.
- R119 (AI Stack Blended IRR) = IFERROR INDEX read returns 0 (Sprint 6 deferred).
- R120 (AI Stack kg demand) = **explicitly set to 0** (`=0`) with col A note "AI Stack terrestrial — no Starship kg demand per Architecture §10.4". This overrides any future AI Stack tab activation; Sprint 10 locks AI Stack at 0 kg demand regardless of module-tab state.
- R121 (masked) = 0; R122 (weight) = 0; R123 (share) = 0; R124 (allocation) = 0.

**Verification reads:**
- D90 (Total Starship capacity 2025) expect **0** exact (Launch Capacity!R34 = 0 pre-flight; Starship fleet not yet endogenously sized)
- I90 (2030) expect **0** still (fleet wiring out-of-scope for Sprint 10)
- D91 (Lunar Mars kg reserved 2025) expect **0** (Lunar Mars R210 D = 0; first deployment 2028)
- I91 (2030) expect **5,460,843 kg** (Lunar Mars R210 I read)
- D92 (Capacity available 2025) expect **0** = MAX(0, 0 - 0)
- I92 (Capacity available 2030) expect **0** = MAX(0, 0 - 5,460,843) — negative clipped to 0
- D95 (CL Blended IRR 2025) expect **2.7270**
- D103 (Starlink Blended IRR 2025) expect **0.7624**
- D111 (ODC Blended IRR 2025) expect **-0.2969**
- D119 (AI Stack Blended IRR 2025) expect **0**
- D106 (Starlink kg weight 2025) expect **~0.5813**
- D130 (Σ kg weights 2025) expect **~8.02** (same as cash queue — same IRRs)
- D100 + D108 + D116 + D124 (Σ kg allocations 2025) expect **0** (D92 = 0 → MIN returns 0)

**Halt conditions (Rule 15):**
- D92 < 0 → HALT (MAX clip should prevent).
- Σ allocations > D92 → HALT (sigmoid math violation).

**Architectural caveat documented in §5 Outstanding** (Sprint 10 carries forward): Launch Capacity!R34 = 0 across all years because Starship fleet build is hardcoded zero in pre-Sprint-10 Launch Capacity rows. Sprint 10 sizes the vehicle build CLAIM (§3.7) but does NOT wire the cash claim → endogenous fleet build. Until that wiring lands (likely Sprint 11/12), the kg queue allocates 0 to all modules. Module deployment 2026+ binds on cash constraint only.

---

### §3.6 Allocator §7 Module kg allocation canonical rows (R133–R137)

**Canonical labels Sprint 1 already wrote at R133–R137 (col A intact, col D:AC currently literal 0). Sprint 10 replaces col D:AC with live formulas.**

**First-year override (Lock a applied to kg side)**: column D = 0 for all 5 modules (no module launched on Starship in 2025; everything used F9 — kg-via-Starship 2025 = 0 historical actual). Column E:AC = live sigmoid allocation from R100/R108/R116/R124 (R137 Lunar Mars = R91 reserved-off-the-top).

| Row | Col A label (verbatim — Sprint 1 published) | Col D formula | Col E formula | Note |
|---|---|---|---|---|
| R133 | `Customer Launch kg allocation` | `=0` | `=D100` | First-year override D = 0 (no 2025 external Starship customer launches). Live sigmoid 2026+. |
| R134 | `Starlink kg allocation` | `=0` | `=D108` | First-year override D = 0 (V2 BB + V2 DTC launched on F9 in 2025, not Starship). |
| R135 | `ODC kg allocation` | `=0` | `=D116` | First-year override D = 0 (ODC pre-revenue 2025). |
| R136 | `AI Stack kg allocation` | `=0` | `=0` | Structural lock per Architecture §10.4 — AI Stack terrestrial, no Starship kg demand ever. E:AC also 0. |
| R137 | `Lunar Mars kg allocation` | `=D91` | `=E91` | Lunar Mars kg reserved-off-the-top (Architecture §11.3); reads R91 directly. D91 = 0 in 2025 (no 2025 Lunar Mars launches); R210 ramps from 2028. |

Copy E across F:AC for R133–R135 + R137. R136 column E = 0 directly + copy across.

**Verification reads:**
- D133 (CL kg allocation 2025) expect **0** exact
- D134 (Starlink kg allocation 2025) expect **0** exact (override)
- D135 (ODC kg allocation 2025) expect **0** exact
- D136 (AI Stack kg allocation 2025) expect **0** exact (structural)
- D137 (Lunar Mars kg allocation 2025) expect **0** (= D91 = 0)
- I134 (Starlink kg allocation 2030) expect **0** (D92 Capacity available = 0 → sigmoid returns 0)
- I137 (Lunar Mars kg allocation 2030) expect **5,460,843 kg** (= I91 reserved)
- AC137 (2050) expect **10,072,312 kg** (= AC91)

**Touch points (Rule 11):**
- Customer Launch tab R9 reads R133 → switches from $0 placeholder to **0 kg in 2025**, live 2026+.
- Starlink tab R9 reads R134 → **0 kg in 2025**, live 2026+ (returns 0 until fleet wiring lands).
- ODC tab R9 reads R135 → same pattern.
- AI Stack tab R9 reads R136 → permanent 0.
- Lunar Mars tab R9 reads R137 → 0 in 2025, ramps to 5.46M kg in 2030, 10M kg in 2050.

---

### §3.7 Allocator §8 Vehicle build claim (R140–R150)

**Architecture §6.6 verbatim.** Forward-aggregate kg demand sized at T+lead. Lead = Assumptions!R26 = 2 years.

**Layout:**

| Row | Col A label (verbatim) | Col D formula | Number format | Note |
|---|---|---|---|---|
| R139 | (existing) `§8 VEHICLE BUILD CLAIM` | — | section header | — |
| R140 | `Vehicle build lead time (years)` | `=INDEX(Assumptions!$B:$B, MATCH("Vehicle build lead time (years)", Assumptions!$A:$A, 0))` | `0` | reads Assumptions R26 = 2 |
| R141 | `Starlink forward kg demand at T+lead` | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("Capacity Demand (kg-to-LEO)", Starlink!$A:$A, 0), D$5+1+$D$140), 0)` | `#,##0` | INDEX col_num = current year-offset + 1 + lead = current col + 2; D-col reads 2027 (=D$5+1+2 = 0+1+2 = 3 → Starlink F-col 2027) |
| R142 | `ODC forward kg demand at T+lead` | `=IFERROR(INDEX(ODC!$D:$AC, MATCH("Capacity Demand (kg-to-LEO)", ODC!$A:$A, 0), D$5+1+$D$140), 0)` | `#,##0` | Currently 0 (ODC R210 = 0); will activate when Sprint 5 ODC module publishes kg demand |
| R143 | `Customer Launch forward kg demand at T+lead` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Capacity Demand (kg-to-LEO)", 'Customer Launch'!$A:$A, 0), D$5+1+$D$140), 0)` | `#,##0` | Currently 0 (CL R210 = 0); will activate when CL module publishes external Starship demand |
| R144 | `Lunar Mars forward kg demand at T+lead` | `=IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("Capacity Demand (kg-to-LEO)", 'Lunar Mars'!$A:$A, 0), D$5+1+$D$140), 0)` | `#,##0` | LM R210 reads forward — 2025 reads 2027 = 0; 2026 reads 2028 = 3,326,910; 2030 reads 2032 = (further LM trajectory) |
| R145 | `Forward aggregate kg demand` | `=D141 + D142 + D143 + D144` | `#,##0` | Σ of 4 modules' forward demand |
| R146 | `Projected capacity at T+lead (kg-to-LEO)` | `=IFERROR(INDEX('Launch Capacity'!$D:$AC, MATCH("Total Annual Capacity (kg-to-LEO)", 'Launch Capacity'!$A:$A, 0), D$5+1+$D$140), 0)` | `#,##0` | Currently 0 (Launch Capacity!R34 = 0 endogenous fleet not yet wired) |
| R147 | `Capacity gap (kg-to-LEO)` | `=MAX(0, D145 - D146)` | `#,##0` | Forward demand - projected capacity, clipped at 0 |
| R148 | `Required launches (count)` | `=IFERROR(D147 / INDEX('Launch Capacity'!$D:$AC, MATCH("Per-launch upmass (kg)", 'Launch Capacity'!$A:$A, 0), D$5+1), 0)` | `0.0` | gap / per-launch payload (Launch Capacity R29) |
| R149 | `Required vehicles (count)` | `=IFERROR(D148 / INDEX(Assumptions!$B:$B, MATCH("Launches per Starship vehicle per year (cadence × variant blend, ", Assumptions!$A:$A, 0)), 0)` | `0.0` | launches / launches per vehicle per year (Assumptions R27 = 24). **NOTE**: MATCH literal must match Assumptions R27 exact label; pre-flight Check 8 verified this label exists. If MATCH literal truncation is needed due to spec doc formatting, use exact verbatim per pre-flight read. |
| R150 | `Vehicle build claim ($mm)` | `=D149 * (INDEX('Launch Capacity'!$D:$AC, MATCH("Super Heavy manufacturing cost ($mm/unit)", 'Launch Capacity'!$A:$A, 0), D$5+1) + INDEX('Launch Capacity'!$D:$AC, MATCH("Starship 2nd-stage manufacturing cost ($mm/unit)", 'Launch Capacity'!$A:$A, 0), D$5+1))` | `#,##0` | required vehicles × blended build cost (SH + Ship per-unit costs from Launch Capacity R8 + R9). **CANONICAL LABEL** — CapEx R44 reads this. |

Copy D-col formulas across E:AC for R141–R150 (single-row copies; Rule 2 compatible — single-row source).

**Verification reads (pre-computed):**
- D140 (lead time) expect **2** exact
- D141 (Starlink forward kg demand 2025 → reads 2027) expect **2,000,000 kg** (Starlink R210 F-col)
- D142 (ODC forward 2025 → 2027) expect **0**
- D143 (CL forward 2025 → 2027) expect **0**
- D144 (LM forward 2025 → 2027) expect **0**
- D145 (forward aggregate 2025) expect **2,000,000 kg** ±100k
- D146 (projected capacity 2025 → 2027) expect **0** (Launch Capacity R34 = 0)
- D147 (capacity gap 2025) expect **2,000,000 kg**
- D148 (required launches 2025) expect `2,000,000 / 100,000 = 20` launches ±2
- D149 (required vehicles 2025) expect `20 / 24 = 0.833` vehicles ±0.1
- D150 (vehicle build claim 2025) expect `0.833 × ($54M SH + $36M Ship) = 0.833 × $90M ≈ $75M` ±$20M

**E-col (2026 reads 2028):**
- E141 expect **4,200,000 kg** (Starlink 2028)
- E144 expect **3,326,910 kg** (LM 2028)
- E145 expect **7,526,910 kg**
- E150 expect `7,526,910 / 100k / 24 × $90M ≈ $282M` ±$50M

**F-col (2027 reads 2029):**
- F141 expect **6,400,000 kg**
- F144 expect **3,404,225 kg**
- F150 expect `9,804,225 / 100k / 24 × $90M ≈ $368M` ±$50M

**I-col (2030 reads 2032 — Starlink R210 = 10,000,000 kg; LM 2032 from trajectory):**
- I145 expect ~**13M kg**
- I150 expect ~**$488M**

**Halt conditions (Rule 15):**
- D150 > $5,000M in any year before 2040 → HALT (claim too aggressive; check formula).
- D150 < 0 → HALT (must be non-negative).
- D149 not approximately D148 / 24 → HALT (formula structure check).

**Touch points (Rule 11):**
- CapEx!R44 placeholder `Vehicle build claim ($mm) — placeholder for Sprint 10` reads `=INDEX(Allocator!$D:$AC, MATCH("Vehicle build claim ($mm)", Allocator!$A:$A, 0), D$5+1)`. Sprint 10 §3.7 publishes R150 with verbatim canonical label `Vehicle build claim ($mm)`. CapEx R44 should resolve via MATCH to non-zero values. **Pre-flight Check 7 verified CapEx R44 placeholder label exists; this sprint amends CapEx R44 col A to canonical `Vehicle build claim ($mm)` (verbatim — drops the " — placeholder for Sprint 10" suffix) AND amends D44:AC44 formula to the INDEX/MATCH read above.**
- Allocator R23 (Queue Gate Vehicle build claim line) reads R150 directly via same-tab `=D150`.

**Note on CapEx R44 amendment**: This is a 2-cell amendment (col A label + col D:AC formula) on the CapEx tab. Per Principle 10 (Sprint 10 doesn't write modules), CapEx tab is a CROSS-CUTTING TAB, not a module tab — module-owner restriction does not apply. Sprint 8 owns the CapEx tab; this amendment was anticipated by Sprint 8 (the placeholder labeled itself "for Sprint 10"). Spec-author judgment: CapEx R44 amendment is in-scope for Sprint 10.

---

### §3.8 Allocator §9 Central IRR display (R153–R165)

**Architecture §6 + §11.6 verbatim.** Per-module IRR memo panel for at-a-glance review.

| Row | Col A label (verbatim) | Col D formula | Number format | Note |
|---|---|---|---|---|
| R152 | (existing) `§9 CENTRAL IRR DISPLAY` | — | section header | — |
| R153 | `Customer Launch Spot IRR` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Spot IRR", 'Customer Launch'!$A:$A, 0), D$5+1), 0)` | `0.0%` | reads R207 |
| R154 | `Customer Launch Forward IRR (Y+2)` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Forward IRR (Y+2)", 'Customer Launch'!$A:$A, 0), D$5+1), 0)` | `0.0%` | reads R208 |
| R155 | `Customer Launch Blended IRR` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Blended IRR", 'Customer Launch'!$A:$A, 0), D$5+1), 0)` | `0.0%` | reads R209 |
| R156 | `Starlink Spot IRR` | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("Spot IRR", Starlink!$A:$A, 0), D$5+1), 0)` | `0.0%` | — |
| R157 | `Starlink Forward IRR (Y+2)` | same with E$5+1 etc. | `0.0%` | — |
| R158 | `Starlink Blended IRR` | — | `0.0%` | — |
| R159 | `ODC Spot IRR` | — | `0.0%` | — |
| R160 | `ODC Forward IRR (Y+2)` | — | `0.0%` | — |
| R161 | `ODC Blended IRR` | — | `0.0%` | — |
| R162 | `AI Stack Spot IRR` | IFERROR-0 wrap | `0.0%` | Sprint 6 deferred → returns 0 |
| R163 | `AI Stack Forward IRR (Y+2)` | IFERROR-0 wrap | `0.0%` | — |
| R164 | `AI Stack Blended IRR` | IFERROR-0 wrap | `0.0%` | — |
| R165 | `Lunar Mars Blended IRR (hardcoded 0 per Architecture §11.6)` | `=0` | `0.0%` | Architecture §11.6 — Lunar Mars strategic carve-out, no IRR engine. Hardcoded 0 across all years. |

Copy D across E:AC for R153–R164 (R165 copy `0` across — `0` is allowed inline per Rule 14 structural lock + §11.6 reference inline).

**Verification reads:**
- D153 (CL Spot IRR 2025) expect **2.8693**
- D154 (CL Forward IRR 2025) expect **2.6660**
- D155 (CL Blended IRR 2025) expect **2.7270** (matches R41 pre-flight read)
- D156 (Starlink Spot 2025) expect **0.9956**
- D158 (Starlink Blended 2025) expect **0.7624**
- D159 (ODC Spot 2025) expect **-0.3902**
- D161 (ODC Blended 2025) expect **-0.2969**
- D162–D164 (AI Stack) expect **0** all years
- D165 (LM Blended IRR) expect **0** all years
- I158 (Starlink Blended 2030) expect **0.8604**
- I161 (ODC Blended 2030) expect **-0.0742**

---

### §3.9 R108 boolean amendment + R109 cash flow identity activation

**Per Lock (c) + Lock (d) — single-cell amendments on Group P&L tab.**

**R108 amendment (Lock c — amend in-place to include R109):**

Replace existing Group P&L D108 formula with:
```
=IF(AND(ABS(D99)<1,ABS(D100)<1,ABS(D101)<1,ABS(D102)<1,ABS(D103)<1,ABS(D104)<1,ABS(D105)<1,ABS(D106)<1,ABS(D107)<1,ABS(D109)<1),"OK","CHECK")
```

Copy D108 across E108:AC108 — relative refs shift correctly to E99:E107 + E109 → F99:F107 + F109 → ... → AC99:AC107 + AC109.

**Note on R110**: R110 is the memo `Σ Module FCF reconciliation residual` (-$454M baseline; Lock e audit-only). NOT included in R108 AND — it's a diagnostic memo, not a conservation check. Future module-owner sprint may close R110 to 0; until then R108 ignores it.

**R109 activation (Lock d — simplified per Sprint 9 Lock 'a' logic):**

Replace existing Group P&L D109 formula with simplified form:
```
=IFERROR(
   INDEX(Assumptions!$B:$B, MATCH("Starting cash position EoY 2024 ($mm)", Assumptions!$A:$A, 0))
 + SUMIF($D$5:D$5, "<="&D$5, INDEX($D9:$AC9, 0))    [Σ IPO injection cumulative through year T; reads Allocator R9 via cross-tab below]
 + SUMIF($D$5:D$5, "<="&D$5, INDEX($D50:$AC50, 0))  [Σ Group FCF cumulative through year T; reads own row 50]
 - INDEX(Allocator!$D:$AC, MATCH("Cash BoY ($mm)", Allocator!$A:$A, 0), D$5+2)
, 0)
```

**Cleaner replacement (recommended formulation — single row formula text):**

```
=IFERROR(
  INDEX(Assumptions!$B:$B, MATCH("Starting cash position EoY 2024 ($mm)", Assumptions!$A:$A, 0))
+ SUMPRODUCT(($D$5:D$5<=D$5) * IFERROR(INDEX(Allocator!$D:$AC, MATCH("IPO injection this year ($mm)", Allocator!$A:$A, 0), 0), 0))
+ SUMPRODUCT(($D$5:D$5<=D$5) * $D$50:D50)
- IFERROR(INDEX(Allocator!$D:$AC, MATCH("Cash BoY ($mm)", Allocator!$A:$A, 0), D$5+2), 0)
, 0)
```

Where:
- Term 1: Starting cash = $5,000M (Assumptions R8)
- Term 2: Σ IPO injection cumulative through year T (reads Allocator R9 across years; sums where year-offset ≤ current year-offset)
- Term 3: Σ Group FCF cumulative through year T (reads own Group P&L R50)
- Term 4 (subtracted): Cash BoY at year T+1 (= Cash EoY for year T) reads Allocator R15 at next column. For T = 2050 (AC col, col_num = AC$5+2 = 27), reads col 27 of Allocator $D:$AC = Allocator AD-col which doesn't exist → IFERROR returns 0 → R109 at 2050 effectively measures `Starting + Σ IPO + Σ FCF − 0 = terminal cumulative cash` (non-zero by definition). **For 2050, R109 will NOT be zero** — it equals the cumulative cash position. R108 AND check excludes 2050 column from "OK" requirement OR R109 formula special-cases the terminal year.

**Resolved approach for terminal year**: R109 reads `Cash BoY at year T+1` via INDEX with `D$5+2`. For 2050 (D$5 = 25, col_num = 27), Allocator!$D:$AC has only 26 columns (D=1 to AC=26) → INDEX returns #REF! → IFERROR returns 0 → R109 in AC col = (Starting + Σ IPO + Σ FCF) ≠ 0.

**Solution**: Cash EoY at year T = Cash BoY at year T + Group FCF year T + IPO year T+1. For 2050 (terminal), we extrapolate: Cash EoY 2050 = Allocator AC15 + Group P&L AC50 + 0 (no IPO in 2051).

Simpler resolution: amend R109 formula to compute Cash EoY explicitly rather than reading next-year Cash BoY. Replace term 4 with:

```
- IFERROR(
    INDEX(Allocator!$D:$AC, MATCH("Cash BoY ($mm)", Allocator!$A:$A, 0), D$5+1)
  + D50
  + IF(D$4 + 1 = INDEX(Assumptions!$B:$B, MATCH("IPO injection year", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("IPO injection amount ($mm)", Assumptions!$A:$A, 0)), 0)
  , 0)
```

That is: Cash EoY year T = Cash BoY year T (= current Allocator R15) + this year's Group FCF + (next year's IPO injection if applicable).

**Final R109 formula (cleaner — D109 first, copy across):**

```
=IFERROR(
   INDEX(Assumptions!$B:$B, MATCH("Starting cash position EoY 2024 ($mm)", Assumptions!$A:$A, 0))
 + SUMPRODUCT(($D$5:D$5<=D$5) * IFERROR(INDEX(Allocator!$D:$AC, MATCH("IPO injection this year ($mm)", Allocator!$A:$A, 0), 0), 0))
 + SUMPRODUCT(($D$5:D$5<=D$5) * $D$50:D50)
 - (IFERROR(INDEX(Allocator!$D:$AC, MATCH("Cash BoY ($mm)", Allocator!$A:$A, 0), D$5+1), 0) + D50 + IF(D$4+1=INDEX(Assumptions!$B:$B, MATCH("IPO injection year", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("IPO injection amount ($mm)", Assumptions!$A:$A, 0)), 0))
, 0)
```

**Mathematical check on R109 = 0:**

R109 = (Starting + Σ_{t≤T} IPO_t + Σ_{t≤T} FCF_t) − (Cash BoY_T + FCF_T + IPO_{T+1})

By definition of Cash BoY chain: Cash BoY_T = Starting + Σ_{t<T} FCF_t + Σ_{t≤T} IPO_t

So: Cash BoY_T + FCF_T = Starting + Σ_{t≤T} FCF_t + Σ_{t≤T} IPO_t

Then: R109 = (Starting + Σ_{t≤T} IPO_t + Σ_{t≤T} FCF_t) − (Starting + Σ_{t≤T} FCF_t + Σ_{t≤T} IPO_t + IPO_{T+1})
      = −IPO_{T+1}

That's not zero! The R109 formula has an IPO offset error. Let me re-derive.

**Correct identity**: Starting cash + Σ IPO + Σ FCF − Cash EoY = 0 where Cash EoY = Cash BoY next year.

Cash BoY_{T+1} = Cash BoY_T + FCF_T + IPO_{T+1}
              = (Starting + Σ_{t<T} FCF + Σ_{t≤T} IPO) + FCF_T + IPO_{T+1}
              = Starting + Σ_{t≤T} FCF + Σ_{t≤T+1} IPO

R109 should equal: (Starting + Σ_{t≤T} IPO + Σ_{t≤T} FCF) − Cash BoY_{T+1}
                 = (Starting + Σ_{t≤T} IPO + Σ_{t≤T} FCF) − (Starting + Σ_{t≤T} FCF + Σ_{t≤T+1} IPO)
                 = Σ_{t≤T} IPO − Σ_{t≤T+1} IPO
                 = −IPO_{T+1}

Still not zero. The identity needs to be: **R109 = Starting + Σ_{t≤T+1} IPO + Σ_{t≤T} FCF − Cash BoY_{T+1} = 0**. That is: cumulative IPO must extend to T+1 (next year's IPO already "earned" by Cash BoY chain definition).

OR re-define: Cash BoY_T = Starting + Σ_{t<T} (FCF + IPO_t). Then Cash BoY chain definition becomes Cash BoY_T = Cash BoY_{T-1} + FCF_{T-1} + IPO_T (current year IPO).

Let me re-read Sprint Roadmap + Architecture §6.1: "Cash BoY(N) = Cash BoY(N-1) + Group FCF(N-1) + IPO injections(N)". This says current-year IPO contributes to current-year Cash BoY. So IPO_T is added at the start of year T (consistent with Sprint 1 Allocator R8/R9/R15 formula).

By that definition: Cash BoY_T = Starting + Σ_{t<T} FCF_t + Σ_{t≤T} IPO_t

Then Cash EoY_T = Cash BoY_T + FCF_T = Starting + Σ_{t≤T} FCF_t + Σ_{t≤T} IPO_t

R109 = (Starting + Σ_{t≤T} IPO_t + Σ_{t≤T} FCF_t) − Cash EoY_T = 0 ✓

So Cash EoY_T = Cash BoY_T + FCF_T (NO IPO_{T+1} term — IPO is added at start of NEXT year's BoY chain). The formula in §3.9 must NOT add the IPO_{T+1} term.

**Corrected R109 formula:**

```
=IFERROR(
   INDEX(Assumptions!$B:$B, MATCH("Starting cash position EoY 2024 ($mm)", Assumptions!$A:$A, 0))
 + SUMPRODUCT(($D$5:D$5<=D$5) * IFERROR(INDEX(Allocator!$D:$AC, MATCH("IPO injection this year ($mm)", Allocator!$A:$A, 0), 0), 0))
 + SUMPRODUCT(($D$5:D$5<=D$5) * $D$50:D50)
 - (IFERROR(INDEX(Allocator!$D:$AC, MATCH("Cash BoY ($mm)", Allocator!$A:$A, 0), D$5+1), 0) + D50)
, 0)
```

Term 4 = Cash BoY current year + current FCF = Cash EoY current year.

**Verification math (year-by-year):**

| Year T | Starting | Σ IPO ≤T | Σ FCF ≤T | Cash BoY_T | FCF_T | Cash EoY_T = BoY + FCF | R109 = (Start + ΣIPO + ΣFCF) − EoY |
|---|---|---|---|---|---|---|---|
| 2025 | 5000 | 0 | -2569 | 5000 | -2569 | 2431 | 5000+0−2569−2431 = 0 ✓ |
| 2026 | 5000 | 0 | -4629 | 2431 | -2060 | 371 | 5000+0−4629−371 = 0 ✓ |
| 2027 | 5000 | 30000 | -2569 | 30371 | 2060 | 32431 | 5000+30000−2569−32431 = 0 ✓ |
| 2028 | 5000 | 30000 | 3527 | 32431 | 6096 | 38527 | 5000+30000+3527−38527 = 0 ✓ |

R109 = 0 every year ✓.

**Copy D109 across E109:AC109** — relative refs shift correctly. SUMPRODUCT range expands: D5:E5, D5:F5, …, D5:AC5. Σ FCF range: $D$50:D50, $D$50:E50, …, $D$50:AC50.

**Halt conditions (Rule 15):**
- D109 ≠ 0 (within ±$1M) → HALT.
- I109, S109, AC109 ≠ 0 (within ±$1M) → HALT.
- Any R109 in any column 2025–2050 > $1M absolute → HALT.
- D108 ≠ "OK" → HALT.
- I108, S108, AC108 ≠ "OK" → HALT.

---

## §4 Verification (universal protocol + §6.9 calibration)

Run after all §3.x sections complete. Halt + push back if any check fails.

### §4.1 Workbook-wide error scan

Scan all 15 tabs for `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#N/A`. Zero results required. Halt + report first failure.

### §4.2 Conservation block — all years 2025–2050

Read Group P&L R108 column D through column AC. Every cell must equal `"OK"`. If any cell = `"CHECK"`, halt and identify which conservation row failed (R99–R107 or R109).

### §4.3 §6.9 Sprint 10 calibration

| Check | Target | Tolerance | Halt if |
|---|---|---|---|
| Allocator D15 (Cash BoY 2025) | $5,000M | exact | ≠ $5,000M |
| Allocator E15 (Cash BoY 2026) | $2,431M | ±$200M | <$2,000M or >$2,800M |
| Allocator F15 (Cash BoY 2027) | ~$30,371M | ±$2,000M | <$25,000M or >$35,000M (depends on 2026 FCF chain — wider tolerance) |
| Allocator I15 (Cash BoY 2030) | ~$45–55B range | informational | <$30B or >$70B |
| Allocator D22 (Mars carve-out claim 2025) | $1,000M | exact | ≠ $1,000M |
| Allocator D28 (Year-N non-module claims 2025) | ~$11,664M | ±$300M | <$11,000M or >$12,500M |
| Allocator D29 (Available cash for IRR queue 2025) | $0 | exact (clipped by MAX) | ≠ $0 |
| Allocator D80 (Σ cash weights 2025) | ~8.02 | ±1.0 | <5 or >12 |
| Allocator D150 (Vehicle build claim 2025) | ~$75M | ±$50M | <$0 or >$200M |
| Allocator E150 (Vehicle build claim 2026) | ~$282M | ±$100M | <$0 or >$500M |
| Allocator F150 (Vehicle build claim 2027) | ~$368M | ±$100M | <$0 or >$600M |
| Allocator D83 (Customer Launch cash allocation 2025) | $32.86M | ±$1M (first-year override read) | ≠ Customer Launch!D205 |
| Allocator D84 (Starlink cash allocation 2025) | $1,202.54M | ±$5M (first-year override read) | ≠ Starlink!D205 |
| Allocator D85 (ODC cash allocation 2025) | $0 | exact | ≠ 0 |
| Allocator D86 (AI Stack cash allocation 2025) | $0 | exact | ≠ 0 |
| Allocator D87 (Lunar Mars cash allocation 2025) | $1,000M | exact (= D35 floor) | ≠ $1,000M |
| Allocator D133–D137 (kg allocations 2025) | $0 all 5 | exact | any ≠ 0 |
| Allocator D137 (Lunar Mars kg allocation, any year) | = R91 (reserved off-the-top) | exact | drift |
| Group P&L D108 | "OK" | exact | ≠ "OK" |
| Group P&L D109 | 0 | ±$1M | >$1M absolute |
| Group P&L D26 (Group EBITDA post-Sprint-10) | $4,904M | ±5% ($245M) | <$4,659M or >$5,149M |
| Group P&L D50 (Group FCF post-Sprint-10) | -$2,569M | ±10% ($257M) | <-$2,826M or >-$2,312M |
| Group P&L D10 (Group Revenue post-Sprint-10) | $15,137M | ±5% ($757M) | <$14,380M or >$15,894M |
| CapEx R44 (Vehicle build claim) | = D150 | exact (= match Allocator R150 by canonical label read) | drift |
| 5 module IN R8 cells (cash) | resolve to non-zero values per §3.4 expected | ±$5M | any ≠ expected |
| 5 module IN R9 cells (kg) | resolve to 0 for 2025 (override); live 2026+ | exact | D-col any ≠ 0 |

### §4.4 Rule 22 stale-reference scan

For every cross-tab pull written in §3.1–§3.9, verify source column-A label matches consumer's labeled concept:

| Consumer cell | Source label expected | Source row found by MATCH | Result |
|---|---|---|---|
| Allocator R10 D-col | `GROUP FCF ($mm)` on Group P&L | 50 | should match |
| Allocator R18 | `Total OpEx ($mm)` on OpEx | 53 | should match |
| Allocator R19 | `Total Corporate CapEx ($mm)` on CapEx | 25 | should match |
| Allocator R20 | `EchoStar mid-band CapEx ($mm)` on CapEx | 39 | should match |
| Allocator R21 | `Taxes ($mm)` on Group P&L | 32 | should match |
| Allocator R42 | `Module CapEx ($mm)` on Customer Launch | 205 | should match |
| Allocator R50 | `Module CapEx ($mm)` on Starlink | 205 | should match |
| Allocator R58 | `Module CapEx ($mm)` on ODC | 205 | should match |
| Allocator R66 | `Module CapEx ($mm)` on AI Stack | 205 | should match |
| Allocator R41/R49/R57/R65 | `Blended IRR` on each module | 209 | should match all 4 |
| Allocator R90 | `Total Annual Capacity (kg-to-LEO)` on Launch Capacity | 34 | should match |
| Allocator R91 | `Capacity Demand (kg-to-LEO)` on Lunar Mars | 210 | should match |
| Allocator R141 | `Capacity Demand (kg-to-LEO)` on Starlink | 210 | should match |
| Allocator R142/R143/R144 | same on ODC / CL / LM | 210 | should match all 3 |
| Allocator R146 | `Total Annual Capacity (kg-to-LEO)` on Launch Capacity | 34 | should match |
| Allocator R148 | `Per-launch upmass (kg)` on Launch Capacity | 29 | should match |
| Allocator R150 (cost components) | `Super Heavy manufacturing cost ($mm/unit)` + `Starship 2nd-stage manufacturing cost ($mm/unit)` on Launch Capacity | 8 + 9 | should match both |
| Allocator R153/R156/R159/R162 (Spot IRR) | `Spot IRR` on each module | 207 | should match all 4 |
| Allocator R154/R157/R160/R163 (Forward IRR) | `Forward IRR (Y+2)` on each module | 208 | should match all 4 |
| CapEx R44 (post-amendment) | `Vehicle build claim ($mm)` on Allocator | 150 | should match |
| Module IN R8 (5 module tabs) | `[Module] cash allocation` on Allocator | 83/84/85/86/87 | should match all 5 |
| Module IN R9 (5 module tabs) | `[Module] kg allocation` on Allocator | 133/134/135/136/137 | should match all 5 |
| Group P&L R109 | `Cash BoY ($mm)` on Allocator | 15 | should match |

If any MATCH returns #N/A or wrong row: halt and identify drift.

### §4.5 Round-trip stability test (Principle 22 / Lesson 22)

After all §3 writes land + R108/R109 amendments: trigger 5 full recalcs (Excel F9 × 5). Read Group P&L D26, D50, D108 and Allocator D15, D29, D80, D150 after each recalc. No value should move >$1M across recalcs. If any value drifts: bistability — halt + push back.

### §4.6 Edge-year reads (Rule 16)

Read Group P&L + Allocator at D (2025), I (2030), S (2040), AC (2050) for key rows:
- Group P&L D26, I26, S26, AC26 — EBITDA trajectory
- Group P&L D50, I50, S50, AC50 — FCF trajectory  
- Group P&L D108, I108, S108, AC108 — conservation "OK" every edge year required
- Allocator D15, I15, S15, AC15 — Cash BoY trajectory
- Allocator D29, I29, S29, AC29 — Available cash for IRR queue
- Allocator D150, I150, S150, AC150 — Vehicle build claim trajectory

**Documentation requirement (Lock f — AC_2050 negative EBITDA open thread)**: if Group P&L AC26 < 0, document in §5 Outstanding for Sprint 11 audit. Do not attempt fix in Sprint 10.

**Documentation requirement (Lock e — R110 residual)**: read Group P&L D110, I110, S110, AC110 post-Sprint-10. Document trajectory. R110 should remain a memo (not in R108 AND); if R110 swings beyond pre-Sprint-10 baseline (-$454M) by >$200M, flag for Sprint 11 audit.

### §4.7 Claude Log entry

Append one row to the Claude Log tab on the workbook:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-MM-DD | 10 | Allocator (R8–R165), Group P&L (R108, R109), CapEx (R44) | Allocator brain lit up. Cash Pool Tracker R8–R15, Queue Gate R18–R29, Cash IRR sigmoid R40–R80, Kg IRR sigmoid R90–R130, Vehicle build claim R140–R150, Central IRR display R153–R165. 5 module cash allocation canonical rows R83–R87 + 5 kg allocation canonical rows R133–R137 published. Module IN cells (cash + kg) switched from $0 placeholders to live IRR-driven (cash) / $0 first-year override + sigmoid 2026+ (kg). First-year override applied: Allocator R83–R87 col D reads each module's Module CapEx historical actuals. CapEx R44 vehicle build claim placeholder switched to live INDEX/MATCH read of Allocator R150. R108 conservation boolean extended to include R109. R109 cash flow identity activated per simplified Lock 'd' formulation (Starting + Σ IPO + Σ FCF − Cash EoY = 0). PASS/FAIL on §6.9 calibration. | (a) Σ Module FCF residual R110 = -$454M baseline, audit trace deferred to module-owner sprint per Lock e. (b) Launch Capacity!R34 = 0 across all years — Starship fleet wiring (cash → endogenous build) deferred to Sprint 11/12. Until then, kg queue allocates 0 to all modules; module deployment 2026+ binds on cash constraint only. (c) AC_2050 negative EBITDA open thread from Sprint 9 carried forward per Lock f. (d) Out-year vehicle build claim 2028+ trajectory needs verification against Sprint 11 deployment audit. | Sprint 11 — Valuation (DCF + terminal value + SoTP football field; consumes Allocator Cash BoY + module FCF trajectories; audits R110 leak; possibly Sprint 11.5 closes Launch Capacity endogenous fleet wiring). |

---

## §5 Outstanding items (carry forward to Sprint 11 / Claude Log)

1. **R110 Σ Module FCF residual leak (-$454M baseline)** — per Lock e, audit-only in Sprint 10; trace deferred to module-owner sprint. Candidate sources: Customer Launch R204 D&A add-back not consistent with module D&A in COGS; Starlink/ODC bandwidth flow accounting at module vs Group level; AI Stack pre-revenue floor R&D inside vs outside Module FCF. Sprint 11 Valuation audit decides whether to fix or document as structural.
2. **Launch Capacity!R34 = 0 across all years** — Starship fleet endogenous build wiring (cash claim → boosters built per year → Total Annual Capacity) is out-of-scope for Sprint 10. Sprint 10 sizes the cash CLAIM only. Likely Sprint 11.5 or Sprint 12 wires `boosters_built(T) = vehicle_build_claim(T) / blended_build_cost` and feeds R25 + R27 + R33 + R34 on Launch Capacity tab.
3. **AC_2050 negative EBITDA (Sprint 9 open thread #2)** — per Lock f, surface in §4.6 Verification only. Document trajectory; defer fix to Sprint 11 audit after allocator-driven deployment equilibrium settles.
4. **2025 historical actuals on Allocator R83–R84 source from module-tab Module CapEx D-col** — Vlad's S-1 import work updates Customer Launch + Starlink tab Module CapEx values; Allocator override inherits automatically via INDEX/MATCH. If S-1 import lands between Sprint 10 finalization and execution, Vlad's update flows through.
5. **Customer Launch R210 + ODC R210 = 0 across all years** — module-published kg demand. Vehicle build claim sizes off Starlink + Lunar Mars demand only. When CL + ODC publish real kg demand (likely Sprint 11/12 module audit), vehicle build claim re-sizes automatically.
6. **R109 column AC (2050) terminal year behavior** — R109 formula reads Cash BoY at year T+1 via INDEX D$5+1. For 2050 (AC col), reads next column which exists (col 27 of $D:$AC range = AC col itself since the range D:AC has 26 columns; col_num = 26 = AC). Re-verify behavior — col_num = D$5+1 = 26 in AC col means INDEX returns AC-col value (= Cash BoY 2050). Cash EoY 2050 = Cash BoY 2050 + FCF 2050. Mathematical identity holds. (Note: original derivation had col_num = D$5+2 = 27 which would be out-of-range; corrected to D$5+1.) Spec author confirms final formula uses D$5+1 in §3.9.

7. **Demand Curves tab built incorrectly — architecture refactor required (surfaced 2026-05-26 mid-Sprint-10 spec authoring)** — The current Demand Curves tab (V2.11) is laid out as two year-rows per product (Total BB Gbps demand R9 + Total BB price R10; Total DTC Gbps demand R11 + Total DTC price R12), with NO functional link between quantity and price. The structural error: quantity-rise and price-fall happen on parallel time-series tracks rather than as a single market mechanism moving along a curve. A real demand curve is `Revenue = f(Q_supplied)` — given year-T Gbps supplied (computed endogenously by Starlink module from fleet × per-sat Gbps), revenue is read by interpolating the curve. **Form locked (Vlad 2026-05-26): piecewise-linear lookup table** — two columns per product (Q breakpoint, Revenue at that breakpoint); 8–12 breakpoints per product; modules read via bracket-interpolation Excel formula `=IF(Q>=MAX(Q_col), MAX(Rev_col), IF(Q<=MIN(Q_col), MIN(Rev_col), FORECAST(Q, Rev_col, Q_col)))`. **Implications:** (a) Architecture §18 item 5 needs amendment to specify P=f(Q) piecewise-linear form (currently silent or wrong); (b) Sprint 4 Starlink BB + DTC revenue formulas wired against year-row $/Gbps × Gbps_supplied stubs — must be repointed to call the demand-curve lookup against module-computed Gbps supplied; (c) Starshield revenue (Assumptions R96 = $164,699/Gbps flat) — decision needed in 10.5 whether to land on a curve or stay flat (treated as procurement-driven flat-rate); (d) post-refactor must re-run Sprint 9 §6.8 calibration confirming Group Revenue stays at $14.65B ±5% (calibrate the curve breakpoints to hit 2025 anchor). **Slot: Sprint 10.5 patch sprint after Sprint 10 lands.** Sprint 11 (Valuation) MUST run against the corrected revenue mechanics — flat-price revenue model dramatically over-states out-year Starlink revenue (no price erosion as fleet scales). Out of Sprint 10 scope per Principle 1 (don't cascade retrofit + architectural changes together) — Sprint 10 already introduces the largest within-year cycle yet via Allocator brain. Sprint 10.5 spec authored in a separate chat after Sprint 10 PASS.

---

## §6 Amendment log

- **2026-05-26 (initial draft)** — Sprint 10 spec authored. Rule Compliance Preamble all boxes ticked; pre-flight checks (9 in §3.0) defined; 7 architectural locks confirmed (a override → S-1 historical actuals via module-tab reads; b §3.0 pre-flight Sprint 7 §3 audit READ-ONLY; c R108 amend in-place; d R109 simplified per Sprint 9 Lock 'a'; e R110 audit-only, defer to module-owner sprint; f AC_2050 surface-only, defer to Sprint 11; g vehicle build claim 2025 sized naturally at ~$75M, no override). 6 canonical labels published. §6.9 calibration enumerated with Cash BoY 2025 = $5,000M exact + Mars carve-out 2025 = $1,000M exact + Available cash 2025 = $0 exact halt thresholds. Spec is fully self-contained per standing rule locked 2026-05-20.

- **2026-05-26 (amendment — Demand Curves architecture error surfaced mid-spec-authoring)** — Vlad surfaced that current V2.11 Demand Curves tab is laid out as parallel time-series stubs (Q year-row + P year-row) with no functional Q→Revenue link. Architecture error; affects Sprint 4 Starlink BB+DTC revenue formula. Confirmed out-of-Sprint-10-scope per Principle 1 (don't cascade architectural changes). Form locked: piecewise-linear lookup table (Q breakpoint, Revenue) per product; bracket-interpolation lookup. Captured as Outstanding item #7 §5 for Sprint 10.5 patch sprint after Sprint 10 PASS. Sprint 11 Valuation runs against corrected revenue mechanics post-10.5.

---

## End of Sprint 10 Spec
