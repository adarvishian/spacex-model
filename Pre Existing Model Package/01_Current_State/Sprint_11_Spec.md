# Sprint 11 Spec — Combined cleanup before Valuation (vehicle-level allocator + endogenous fleet + LM BV correction + ODC audit)

**Sprint name**: Pre-Valuation architecture closure. ONE combined sprint absorbing former Sprint 10.7 (vehicle-level allocator + 3 physical gates + module deployment binding), former Sprint 10.7+ (Launch Capacity endogenous Starship + F9 fleet build wiring), former Sprint 10.8 (D&A audit — Lunar Mars BV depreciation removed from Group D&A), former Sprint 10.9 (ODC unit-economics audit), and Sprint 9 §6.8 calibration revision conversation.

**Status**: spec-author chat, drafted 2026-05-26 immediately after Sprint 10.5 PASS (V2.13). Triggered by Vlad lock 2026-05-26: "give me all of these in one sprint. and change whatever you need to architecture and methodology". Architecture & Methodology constitutional doc amended in parallel (new §20 amendments block + §19 amendment log entry).

**Dependencies landed**: Sprint 10 PASS (Allocator brain skeleton). Sprint 10.5 PASS (Demand curves rebuilt; finite-diff per-vehicle marginal IRR live; per-vehicle Blended IRR R215/R220/R225/R230 economically reliable).

**Architecture reference**: `02_Architecture_and_Methodology.md` §20 (Sprint 11 amendments block) — read by spec; supersedes earlier §4.1, §6.3, §6.4, §6.5, §6.6, §8.2, §11.4, §11.5 conventions. Specifically §20.1-§20.8.

**Big upfront flag**: Sprint 11 introduces significant calibration shifts:
- **2050 Group D&A drops $484B → ~$6B** (LM BV depreciation removed)
- **2050 Group FCF drops +$337B → roughly −$90B** (D&A add-back was inflated by phantom LM BV)
- **Starlink V3 BB / V3 DTC deployment becomes endogenous to Starship fleet build** (R34 Total Annual Capacity non-zero post-trigger)
- **V2 BB / V2 DTC retire by 2028 phase-out gate; V3 ramps via sigmoid + Starship kg**
- **ODC stays at zero deployment** (per-sat IRR negative; allocator correctly refuses)

**Sprint 9 §6.8 calibration target revision conversation TRIGGERED post-Sprint-11**. Group Revenue 2025 = $13,855M (drift from $14,650M target — mechanic-driven post-Sprint-10.5). Group FCF 2050 swings −$427B from V2.13 baseline. New targets locked by Vlad before Sprint 12 Valuation.

---

## §0 Rule Compliance Preamble (mandatory)

- [x] **Rule 1** — every §3 section structures writes as separate blocks (labels, formulas, formats). Multi-row writes use execute_office_js (per `feedback_execute_office_js_safer_for_multirow_writes`).
- [x] **Rule 3 / 23** — 3 physical gates use Rule 23-compliant `IF(D$4 >= year_input, ...)` against Assumptions cells. Cash BoY chain (§3.1 from Sprint 10) is the only Rule 23 EXCEPTION; not touched in this sprint.
- [x] **Rule 4** — every §3 section has D / I / S / AC read-backs + expected values. §4 consolidates calibration drift surface for the major architectural changes.
- [x] **Rule 6** — every cell write specified with full Excel formula (long canonical labels quoted verbatim per `feedback_quote_canonical_labels_verbatim`).
- [x] **Rule 10** — Allocator tab section headers may relocate via SHIFT (NOT row insertion); all cross-tab refs use INDEX/MATCH by canonical label (Rule 12), immune to row shifts. Per-vehicle canonical labels R88-R91 APPEND below existing R83-R87 — plugin relocates §6/§7/§8/§9 headers downward to accommodate. Module tabs touched in-place (R205 formula REPLACE; no row insertions on cross-referenced tabs).
- [x] **Rule 11** — every new canonical label enumerates downstream consumers + conservation check + calibration line.
- [x] **Rule 12** — every cross-tab pull uses INDEX/MATCH by label. 6 new vehicle-level canonical labels enumerated.
- [x] **Rule 13** — vending-machine framing preserved. LM BV depreciation removal corrects a pre-existing violation (BV depreciation in COGS wasn't really following vending-machine — was decoration value, not capital depreciation).
- [x] **Rule 14** — V2 phase-out year added as Assumptions MC input. V3 trigger year reads existing Launch Capacity R56. No hardcoded constants in formulas.
- [x] **Rule 15** — quantitative halt thresholds for: 3 gates (V3 launches D-col E-col = 0; V2 launches G-col = 0; F9 internal + customer ≤ F9 capacity); LM BV depreciation refs absent from Group D&A R28; Group D&A 2050 ≤ $20B (drops from $484B baseline; halt if still >$20B post-fix); R108 = "OK" all years; round-trip stability < $1M.
- [x] **Rule 19** — Vlad handles all saving.
- [x] **Rule 22** — §4 stale-ref scan enumerates all new + modified cross-tab pulls.

**Architecture compliance** (per §20 amendments block in updated 02_Architecture_and_Methodology.md):
- [x] §20.1 vehicle-level Allocator IN/OUT for Starlink
- [x] §20.2 cash + kg sigmoid per-vehicle for Starlink; 3 physical gates
- [x] §20.3 deployment binding MANDATORY (every IRR-positive module's R205 binds on Allocator IN)
- [x] §20.4 Launch Capacity endogenous fleet wiring (R25 boosters built = f(R150 vehicle build claim); F9 build rate decay)
- [x] §20.5 LM BV depreciation REMOVED from Group D&A — BV is SoTP terminal value INPUT, not P&L D&A flow
- [x] §20.6 V2/V3 ratchet flag retired
- [x] §20.7 Customer Launch R210 Capacity Demand exposed for vehicle build claim sum
- [x] §20.8 ODC negative IRR is model verdict (audit-only)

---

## §1 Scope summary

| Section | What ships | Tabs touched |
|---|---|---|
| §3.0 Pre-flight | 11 halt-bearing checks | read-only |
| §3.1 Assumptions §12 new input | V2 phase-out year (Base Case 2028, MC) | Assumptions append R350 |
| §3.2 Allocator §4 cash queue expand | 7 sub-blocks (compact 5-row form); 3 gates in demand formulas | Allocator R40-R80 |
| §3.3 Allocator §5 canonical labels expand | 6 new vehicle-level labels (4 cash R88-R91 + 2 kg R138-R139); section header relocations | Allocator R83-R91, R137-R142 |
| §3.4 Allocator §6 kg queue expand | 5 sub-blocks (V2 NOT in kg queue) | Allocator R94-R130 (post-relocation) |
| §3.5 Starlink Module IN block expand | 4 cash + 2 kg vehicle-level reads | Starlink R7-R14 |
| §3.6 Per-vehicle deployment formula rewire | R33 / R37 / R39 / R41 with 3 gates + MIN bind | Starlink R33, R37, R39, R41 |
| §3.7 Retire hardcoded ratchets | R43 ratchet flag + Assumptions R320 V2 DTC cap | Starlink R43, Assumptions R320 |
| §3.8 Module-level deployment binding | CL + ODC + AIS R205 MIN(cash/cost, internal) | Customer Launch R205, ODC R205, AI Stack R205 |
| §3.9 Launch Capacity endogenous Starship fleet wiring | R8/R9 cost across years; R25 = f(R150 vehicle build claim); R33/R34 endogenous | Launch Capacity R8-R9, R25, R33-R34 |
| §3.10 Launch Capacity endogenous F9 fleet wiring | R61 F9 manufactured per year as endogenous decay | Launch Capacity R61 |
| §3.11 LM BV depreciation removal from Group D&A | Group P&L R28 + R36 formulas amended (drop LM BV refs); LM module D&A as proper cash-cap depreciation | Group P&L R28, R36; Lunar Mars module tab COGS structure |
| §3.12 ODC unit-economics audit | Probe + document (no auto-fix; Vlad decision pending) | read-only |
| §3.13 Customer Launch R210 Capacity Demand | Wire R210 = R24 Starship customer launches × per-launch upmass (canonical label resolves for vehicle build claim) | Customer Launch R210 |

**Publishes 6 new canonical labels** (verbatim, Rule 12):
1. `Starlink V2 BB cash allocation` (Allocator R88)
2. `Starlink V2 DTC cash allocation` (Allocator R89)
3. `Starlink V3 BB cash allocation` (Allocator R90)
4. `Starlink V3 DTC cash allocation` (Allocator R91)
5. `Starlink V3 BB kg allocation` (Allocator R138)
6. `Starlink V3 DTC kg allocation` (Allocator R139)

---

## §2 Constitutional reference

Read these from updated `02_Architecture_and_Methodology.md`:
- §20.1 Allocator IN/OUT vehicle-level for Starlink
- §20.2 Cash + kg sigmoid per-vehicle; 3 physical gates
- §20.3 Module deployment binding MANDATORY
- §20.4 Launch Capacity endogenous fleet wiring
- §20.5 LM BV correction (SoTP input, not P&L flow)
- §20.6 V2/V3 ratchet retired
- §20.7 CL R210 Capacity Demand
- §20.8 ODC negative IRR is model verdict

Plus standing references: Lessons §2 (per-sat IRR finally lands end-to-end), §22 (within-year cycle bistability — Sprint 11 introduces deployment-bound cycles).

---

## §3 Execution

### §3.0 Pre-flight (READ-ONLY — halt if any check fails)

**Check 1 — Sprint 10.5 PASS values intact:**
```
Allocator D15 = $5,000M; D29 = $0; D35 = $1,000M; D108 = "OK"; D109 ≈ 0
Starlink D120 ~ $6,746M (BB Rev from curve); D131 ~ $142M
Demand Curves D141 = 1.000 (TAM shift); AC141 ~ 3.85
Group P&L D10 ~ $13,855M; D26 ~ $4,358M; D50 ~ -$3,050M; D108 = "OK" all years
Group P&L AC26 = -$44,521M; AC28 = $484,076M (BASELINE — Sprint 11 §3.11 will reduce AC28 dramatically)
```

**Check 2 — Per-vehicle IRR + CapEx + launch routing rows:**
```
Starlink memo IRR rows R213-R230 resolve verbatim
Starlink per-vehicle CapEx rows R88-R95 resolve
Starlink R33/R37/R39/R41 deployment rows resolve
Starlink R45-R48 F9/Starship internal launch routing rows resolve
Starlink R43 V2/V3 ratchet flag resolves (to retire)
Assumptions R320 V2 DTC permanent cap = 1 (to retire)
```

**Check 3 — V3 trigger + V2 phase-out availability + F9 supply:**
```
Launch Capacity R56 "V3 Starlink launch trigger year" = 2027
Launch Capacity R55 "F9 base booster build rate" = 8; R57 decay window = 8 years
Launch Capacity R64 F9 launches per year = 171 (2025), ~49 (2030)
Launch Capacity R8 "Super Heavy manufacturing cost ($mm/unit)" = 54 (D-only — Sprint 11 §3.9 replicates across years)
Launch Capacity R9 "Starship 2nd-stage manufacturing cost ($mm/unit)" = 36 (D-only)
Launch Capacity R25 "Boosters built per year (units)" = 0 (Sprint 11 §3.9 wires endogenously)
Launch Capacity R34 "Total Annual Capacity (kg-to-LEO)" = 0 throughout (Sprint 11 §3.9 lights up)
Customer Launch R25 "F9 customer launches per year" = 38.6 (2025)
Customer Launch R24 "Starship customer launches per year" = 0 (will populate when CL external Starship demand sized)
```

**Check 4 — LM BV depreciation rows + Group D&A formula:**
```
Lunar Mars R117 "BV depreciation — Lunar ($mm/yr)" — current value (probe): AC117 = $368,015M
Lunar Mars R118 "BV depreciation — Mars ($mm/yr)" — AC118 = $109,005M
Group P&L R28 Group D&A formula — confirm contains substring "BV depreciation — Lunar" and "BV depreciation — Mars" (to remove)
Group P&L R36 Σ Module D&A in COGS formula — same
```

**Check 5 — ODC per-sat IRR values (audit baseline):**
```
ODC R155/R207 Spot IRR = -0.39 (2025), -0.10 (2030), -0.15 (2050)
ODC R102 Per-sat external compute revenue = $0 (2025), $0.5M (2030), $0.5M (2050)
ODC R154 Per-sat net marginal revenue = $0 (2025), $0.5M (2030), $0.5M (2050)
```

**Check 6 — Allocator current layout (pre-relocation):**
```
Allocator R39 "§4 CASH IRR-PRIORITY SIGMOID QUEUE"
Allocator R82 "§5 MODULE CASH ALLOCATIONS"
Allocator R83-R87 module canonical labels (Customer Launch, Starlink, ODC, AI Stack, Lunar Mars)
Allocator R89 "§6 KG IRR-PRIORITY SIGMOID QUEUE"
Allocator R132 "§7 MODULE KG ALLOCATIONS"
Allocator R139 "§8 VEHICLE BUILD CLAIM"
Allocator R152 "§9 CENTRAL IRR DISPLAY"
```

**Check 7 — Module IN block on each module + Starlink Module IN (pre-expansion):**
```
Customer Launch R8 reads Allocator "Customer Launch cash allocation"
Starlink R7-R10 currently — R8 reads single "Starlink cash allocation" (Sprint 11 §3.5 expands to R8-R14)
ODC R8 reads Allocator "ODC cash allocation"
AI Stack R8 same
Lunar Mars R8 reads Allocator "Lunar Mars cash allocation" (carve-out)
```

**Check 8 — Module deployment formulas (current state — to bind on Allocator IN):**
```
Customer Launch R205 Module CapEx — read formula; confirm does NOT bind on R8
ODC R205 — same (currently = D135 internal)
AI Stack R205 — same (= 0; Sprint 6 deferred)
```

**Check 9 — Assumptions §2 ALLOCATOR + last filled row:**
```
Assumptions R8 Starting cash $5,000; R10 IPO year 2027; R16 Sigmoid_k = 2; R17 Forward weight w = 0.7
Assumptions R25 Vehicle build claim toggle = 1; R26 lead time = 2; R27 launches per vehicle = 24
Last filled Assumptions row = R349 (Sprint 10.5 ended; GNI growth at R349). Append R350.
```

**Check 10 — Iterative calc setting:**
```
workbook.calculation.iterate = True
```

**Check 11 — Sprint 9/10/10.5 canonical labels (sanity):**
```
Group P&L canonical labels resolve (GROUP REVENUE NET OF ELIMS, Group EBITDA, GROUP FCF, etc.)
Allocator canonical labels resolve (Cash BoY, Available cash for IRR queue, Vehicle build claim, Customer Launch cash allocation, etc.)
Demand Curves canonical labels resolve (Starlink BB Revenue from curve, Annual TAM shift multiplier, etc.)
```

If all 11 checks pass: proceed.

---

### §3.1 Assumptions §12 new input — V2 phase-out year

Append at R350:

| Row | Col A label (verbatim) | Col B value | Col C MC Min | Col D MC Max | Col E Dist | Col F Notes |
|---|---|---|---|---|---|---|
| R350 | `V2 phase-out year (no V2 BB / V2 DTC launches from this year)` | 2028 | 2026 | 2032 | triangle | Base Case 2028; physical/production decision (V2 line shut down once V3 dominates); MC stress: 2026 (V3 ramps faster, V2 ends earlier) — 2032 (V2 production stays open longer) |

Verification: B350 = 2028 exact.

---

### §3.2 Allocator §4 cash queue — expand to 7 sub-blocks with 3 gates

**Layout decision**: switch existing §4 queue (R40-R80) from 4 sub-blocks × 8 rows + spacers to **7 sub-blocks × 5 rows compact**:
- Row N: vehicle/module name (italic header)
- Row N+1: Blended IRR (live read)
- Row N+2: cash demand (with gate multiplier)
- Row N+3: weight = `MAX(IRR, 0)^k × IF(demand > 0, 1, 0)`
- Row N+4: proposed allocation = `MIN(IF(IRR > 0, demand, 0), Available × weight / Σ_weights)`

7 sub-blocks × 5 rows = 35 rows. Layout in R41-R75. R80 = Σ weights.

**Sub-block order** (plugin chooses exact row positions):
1. Customer Launch (R41-R45)
2. Starlink V2 BB (R46-R50)
3. Starlink V2 DTC (R51-R55)
4. Starlink V3 BB (R56-R60)
5. Starlink V3 DTC (R61-R65)
6. ODC (R66-R70)
7. AI Stack (R71-R75)
8. (Σ weights at R80)

**Per-Starlink-vehicle sub-block formula template** (V2 BB shown; same pattern for V2 DTC, V3 BB, V3 DTC):

```
R46 (label): "▸ Starlink V2 BB"
R47 (Blended IRR D-col):
  =IFERROR(INDEX(Starlink!$D:$AC, MATCH("Memo: V2 BB Blended IRR", Starlink!$A:$A, 0), D$5+1), 0)
R48 (cash demand D-col):
  =IF(D$4 >= INDEX(Assumptions!$B:$B, MATCH("V2 phase-out year (no V2 BB / V2 DTC launches from this year)", Assumptions!$A:$A, 0)), 0,
     IFERROR(INDEX(Starlink!$D:$AC, MATCH("V2 BB sat CapEx ($mm)", Starlink!$A:$A, 0), D$5+1) + INDEX(Starlink!$D:$AC, MATCH("V2 BB facility CapEx ($mm)", Starlink!$A:$A, 0), D$5+1), 0)
  )
R49 (weight D-col):
  =MAX(D47, 0)^INDEX(Assumptions!$B:$B, MATCH("Sigmoid IRR-blend exponent k", Assumptions!$A:$A, 0)) * IF(D48 > 0, 1, 0)
R50 (proposed allocation D-col):
  =MIN(IF(D47 > 0, D48, 0), $D$29 * D49 / IFERROR($D$80, 1))
```

Copy each row D across E:AC.

**V2 DTC sub-block (R51-R55)**: same pattern, swap "V2 BB" → "V2 DTC". Phase-out gate applies.

**V3 BB sub-block (R56-R60)**: same pattern, swap "V2 BB" → "V3 BB". REPLACE phase-out gate with V3 STARTUP gate:
```
R58 (V3 BB cash demand D-col):
  =IF(D$4 < INDEX('Launch Capacity'!$D:$AC, MATCH("V3 Starlink launch trigger year", 'Launch Capacity'!$A:$A, 0), 1), 0,
     IFERROR(INDEX(Starlink!$D:$AC, MATCH("V3 BB sat CapEx ($mm)", Starlink!$A:$A, 0), D$5+1) + INDEX(Starlink!$D:$AC, MATCH("V3 BB facility CapEx ($mm)", Starlink!$A:$A, 0), D$5+1), 0)
  )
```

**V3 DTC (R61-R65)**: same V3 trigger gate.

**Customer Launch sub-block (R41-R45)**, **ODC (R66-R70)**, **AI Stack (R71-R75)**: no gates; read per-module Blended IRR from each module's R209.

**Σ weights at R80**:
`=D45 + D49 + D53 + D57 + D61 + D69 + D73`
(Sum of all 7 weight rows. Plugin enumerates exact row references.)

**Verification reads:**
- D47 V2 BB IRR = ~0.75
- D48 V2 BB demand 2025 = $1,116M + $0 facility = $1,116M (V2 BB R88 D + R89 D)
- D49 V2 BB weight 2025 ≈ 0.56
- D50 V2 BB proposed allocation 2025 (Available cash = $0) → 0; first-year override on R88 will pull D directly (see §3.3)
- D52 V2 DTC IRR = ~0.14
- D57 V3 BB demand D 2025 = 0 (V3 trigger gate; D$4 = 2025 < 2027)
- F57 V3 BB demand 2027 = R92 + R93 V3 BB CapEx ≈ $4M (early V3 build)
- G48 V2 BB demand 2028 = 0 (phase-out gate fires)
- D80 Σ weights ≈ 8.0 (Customer Launch dominates with weight ~7.4)

**Halt conditions:**
- D57 V3 BB demand ≠ 0 → HALT (V3 gate failed)
- G48 V2 BB demand ≠ 0 → HALT (V2 phase-out failed)
- Σ proposed allocations > D29 → HALT (sigmoid math violation)

---

### §3.3 Allocator §5 canonical labels expand — 4 new per-vehicle cash labels

**Section header relocation** (plugin executes BEFORE writing new labels):
- §6 header MOVES from R89 → R93 (shift +4)
- §7 header MOVES from R132 → R136 (shift +4)
- §8 header MOVES from R139 → R143 (shift +4)
- §9 header MOVES from R152 → R156 (shift +4)
- All §6/§7/§8/§9 content rows shift +4 accordingly (R90 → R94, R130 → R134, etc.)

Cross-tab consumers use INDEX/MATCH by label — relocations safe.

**Post-relocation R83-R91 layout (canonical labels):**

| Row | Col A label (verbatim) | Col D formula (first-year override) | Col E formula (sigmoid) |
|---|---|---|---|
| R82 | `§5 MODULE CASH ALLOCATIONS (canonical labels — read by module IN blocks)` (existing header) | — | — |
| R83 | `Customer Launch cash allocation` (unchanged) | (existing first-year override formula from Sprint 10) | (existing sigmoid read) |
| R84 | `Starlink cash allocation` (now SUM rollup) | `=D88+D89+D90+D91` | `=E88+E89+E90+E91` |
| R85 | `ODC cash allocation` (unchanged) | (existing) | (existing) |
| R86 | `AI Stack cash allocation` (unchanged) | (existing) | (existing) |
| R87 | `Lunar Mars cash allocation` (unchanged) | `=D35` | `=E35` |
| R88 | `Starlink V2 BB cash allocation` (NEW) | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("V2 BB sat CapEx ($mm)", Starlink!$A:$A, 0), 1) + INDEX(Starlink!$D:$AC, MATCH("V2 BB facility CapEx ($mm)", Starlink!$A:$A, 0), 1), 0)` | `=D50` (V2 BB §4 proposed allocation row) |
| R89 | `Starlink V2 DTC cash allocation` (NEW) | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("V2 DTC sat CapEx ($mm)", Starlink!$A:$A, 0), 1) + INDEX(Starlink!$D:$AC, MATCH("V2 DTC facility CapEx ($mm)", Starlink!$A:$A, 0), 1), 0)` | `=D55` (V2 DTC §4 proposed allocation row) |
| R90 | `Starlink V3 BB cash allocation` (NEW) | `=0` (V3 trigger gate; 2025 < 2027) | `=D60` (V3 BB §4 proposed allocation row) |
| R91 | `Starlink V3 DTC cash allocation` (NEW) | `=0` | `=D65` (V3 DTC §4 proposed allocation row) |

Copy E:AC for R84-R91 from E column.

**Verification reads:**
- D88 V2 BB cash alloc 2025 = $1,116M (first-year override = Starlink R88 historical)
- D89 V2 DTC cash alloc 2025 = $68M
- D90 V3 BB cash alloc 2025 = $0
- D91 V3 DTC cash alloc 2025 = $0
- D84 Starlink rollup 2025 = $1,184M (sum of 4 vehicles)

---

### §3.4 Allocator §6 kg queue — expand to 5 sub-blocks (V2 NOT in kg queue)

**Post-relocation §6 header at R93.** Sub-blocks span R94-R128 (compact 5-row form):
1. Customer Launch external Starship (R95-R99) — reads CL R210
2. Starlink V3 BB (R100-R104)
3. Starlink V3 DTC (R105-R109)
4. ODC (R110-R114)
5. AI Stack (R115-R119) — kg demand structural 0; weight 0

Plus Σ kg weights at R134.

**Capacity available** at R94:
```
=MAX(0, INDEX('Launch Capacity'!$D:$AC, MATCH("Total Annual Capacity (kg-to-LEO)", 'Launch Capacity'!$A:$A, 0), D$5+1)
     - IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("Capacity Demand (kg-to-LEO)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0))
```

(Lunar Mars kg reserved off-the-top per Architecture §11.3.)

**Per-vehicle V3 sub-block template (V3 BB shown):**

```
R100 (label): "▸ Starlink V3 BB"
R101 (Blended IRR): =IFERROR(INDEX(Starlink!$D:$AC, MATCH("Memo: V3 BB Blended IRR", Starlink!$A:$A, 0), D$5+1), 0)
R102 (kg demand): 
  =IF(D$4 < INDEX('Launch Capacity'!$D:$AC, MATCH("V3 Starlink launch trigger year", 'Launch Capacity'!$A:$A, 0), 1), 0,
     IFERROR(INDEX(Starlink!$D:$AC, MATCH("V3 BB Starship kg demand", Starlink!$A:$A, 0), D$5+1), 0)
  )
R103 (kg weight): =MAX(D101, 0)^Assumptions!Sigmoid_k * IF(D102 > 0, 1, 0)
R104 (kg proposed allocation): =MIN(IF(D101 > 0, D102, 0), $D$94 * D103 / IFERROR($D$134, 1))
```

V3 DTC (R105-R109): same pattern, read R50 V3 DTC Starship kg demand.

CL (R95-R99): reads Customer Launch R210 Capacity Demand (kg-to-LEO) — see §3.13.

ODC (R110-R114), AI Stack (R115-R119): read per-module R210.

Σ kg weights R134: `=D99 + D103 + D107 + D113 + D117` (CL + V3 BB + V3 DTC + ODC + AI Stack).

---

### §3.5 Allocator §7 kg canonical labels — 2 new per-vehicle kg labels

Post-relocation §7 header at R136. Layout R137-R142:

| Row | Col A label | D formula | E formula |
|---|---|---|---|
| R137 | `Customer Launch kg allocation` (unchanged, position shifted) | (existing) | (existing) |
| R138 | `Starlink V3 BB kg allocation` (NEW) | `=0` | `=D104` |
| R139 | `Starlink V3 DTC kg allocation` (NEW) | `=0` | `=D109` |
| R140 | `Starlink kg allocation` (rollup, was R134) | `=D138+D139` | `=E138+E139` |
| R141 | `ODC kg allocation` (was R135) | (existing) | (existing) |
| R142 | `AI Stack kg allocation` (was R136) | `=0` (structural) | `=0` |
| R143 | `Lunar Mars kg allocation` (was R137) | (existing reads R91 reserved) | (existing) |

---

### §3.5b Starlink Module IN block expand to 4 cash + 2 kg

Starlink tab R7-R14:

| Row | Col A label | Col D formula |
|---|---|---|
| R7 | `INPUTS FROM CENTRAL ALLOCATOR` (header) | — |
| R8 | `Starlink V2 BB cash allocation ($mm)` | `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("Starlink V2 BB cash allocation", Allocator!$A:$A, 0), D$5+1), 0)` |
| R9 | `Starlink V2 DTC cash allocation ($mm)` | same pattern, swap label |
| R10 | `Starlink V3 BB cash allocation ($mm)` | same |
| R11 | `Starlink V3 DTC cash allocation ($mm)` | same |
| R12 | `Starlink V3 BB kg allocation (kg-to-LEO)` | `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("Starlink V3 BB kg allocation", Allocator!$A:$A, 0), D$5+1), 0)` |
| R13 | `Starlink V3 DTC kg allocation (kg-to-LEO)` | same pattern |
| R14 | `Total Capital Available ($mm)` | `=D8+D9+D10+D11` |

Copy D:AC.

---

### §3.6 Per-vehicle deployment formula rewire

**R33 V2 BB launches per year:**

```
=IF(D$4 >= INDEX(Assumptions!$B:$B, MATCH("V2 phase-out year (no V2 BB / V2 DTC launches from this year)", Assumptions!$A:$A, 0)), 0,
   IF(D$5 = 0,
      INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Sats Launched 2025", Assumptions!$A:$A, 0)),
      MIN(
         IFERROR(D8 / INDEX(Starlink!$D:$AC, MATCH("V2 BB sat unit cost ($mm/sat)", Starlink!$A:$A, 0), D$5+1), 0),
         <internal_uncapped_demand_V2_BB — plugin resolves from existing E33:AC33 if any, else default to D33 anchor>
      )
   )
)
```

**R37 V2 DTC launches per year**: same template, "V2 BB" → "V2 DTC", reads D9 / R79.

**R39 V3 BB launches per year:**

```
=IF(D$4 < INDEX('Launch Capacity'!$D:$AC, MATCH("V3 Starlink launch trigger year", 'Launch Capacity'!$A:$A, 0), 1), 0,
   MIN(
      IFERROR(D10 / INDEX(Starlink!$D:$AC, MATCH("V3 BB sat unit cost ($mm/sat)", Starlink!$A:$A, 0), D$5+1), 0),
      IFERROR(D12 / INDEX(Assumptions!$B:$B, MATCH("V3 Mass (kg)", Assumptions!$A:$A, 0)), 0),
      <internal_uncapped_demand_V3_BB>
   )
)
```

**R41 V3 DTC**: same, "V3 BB" → "V3 DTC", D11 / R81 / D13.

**Verification reads:**
- D33 V2 BB = 2,987 (first-year override)
- D39 V3 BB = 0 (gate)
- F39 (2027) V3 BB > 0 if D34 V3 BB cash + D12 V3 BB kg both non-zero AND Launch Capacity R34 capacity > 0 post-§3.9 wiring
- G33 V2 BB (2028) = 0 (phase-out)

---

### §3.7 Retire hardcoded ratchets

**Starlink R43**: Clear D43:AC43 values. Update col A label:
`V2/V3 ratchet flag — RETIRED 2026-05-26 (replaced by V2 phase-out + V3 trigger gates per §20.6 Architecture amendments)`

**Assumptions R320**: Clear B320 value. Update col A label:
`V2 DTC permanent cap flag — RETIRED 2026-05-26 (replaced by V2 phase-out year R350 per §20.6 Architecture amendments)`

---

### §3.8 Module-level deployment binding (CL + ODC + AI Stack)

**Customer Launch R205 Module CapEx:**

```
=IF(D$5 = 0,
   (existing first-year historical value),
   IFERROR(
      MIN(D8 / INDEX(Assumptions!$B:$B, MATCH("F9 booster (1st stage) mfg cost ($mm/unit)", Assumptions!$A:$A, 0)),
          <existing internal CL demand formula>)
      * INDEX(Assumptions!$B:$B, MATCH("F9 booster (1st stage) mfg cost ($mm/unit)", Assumptions!$A:$A, 0)),
      <existing internal>
   )
)
```

**ODC R205**: ODC currently has D205 = 0 because D135 internal demand = 0. After binding:
```
=IF(D$5 = 0, 0,
   MIN(D8 / <ODC per-sat cost canonical label, plugin resolves>,
       D9 / <ODC per-sat mass>,
       <existing internal demand>)
   * <ODC per-sat cost>
)
```

Plugin pre-flight resolves ODC per-sat cost + mass canonical labels.

**AI Stack R205**: Sprint 6 deferred — leaves R205 stub = 0. AI Stack tab not amended in Sprint 11 (deferred scope).

---

### §3.9 Launch Capacity endogenous Starship fleet wiring

**R8 + R9 cost components across years**: Currently D-only static. Replicate across E:AC OR apply Wright's Law decay (Assumptions R14 = 0 currently; no decay → flat replication).

```
Launch Capacity E8:AC8 = =$D$8  (or apply Wright's Law if anchor cum-units cross learning threshold)
Launch Capacity E9:AC9 = =$D$9  (same)
```

**R25 Boosters built per year (units) — new endogenous formula:**

```
=IFERROR(
   INDEX(Allocator!$D:$AC, MATCH("Vehicle build claim ($mm)", Allocator!$A:$A, 0), D$5+1)
   / (D8 + D9),
   0
)
```

Vehicle build claim cash / blended cost per vehicle = required vehicles built.

**R24 Booster fleet beginning-of-year**: year-chained — existing formula or `=prior_year EoY R27`. Verify.

**R27 Booster fleet end-of-year** = R24 + R25 (built) − R26 (retired). Verify existing formula.

**R33 Total Starship launches per year** = R27 fleet × R23 launches per Starship vehicle per year.

**R34 Total Annual Capacity (kg-to-LEO)** = R33 × R29 per-launch upmass.

**Verification reads:**
- D25 R25 boosters built 2025 = (D150 vehicle build claim / (D8 + D9)) = $50M / $90M = 0.56 boosters (small; first-year underutilized)
- F25 (2027) = forward demand at I=2029 / $90M (depends on Starlink V3 ramping) — likely 5-15 boosters
- I27 (2030) fleet EoY > 0 (cumulative builds 2025-2030)
- I33 (2030) total launches > 0
- I34 (2030) Total Annual Capacity > 0 (V3 kg constraint becomes binding via real capacity, not 0)

---

### §3.10 Launch Capacity endogenous F9 fleet wiring

**R61 F9 manufactured per year (units) — was hardcoded `=17`:**

```
R61 = IF(D$4 < INDEX('Launch Capacity'!$D:$AC, MATCH("V3 Starlink launch trigger year", 'Launch Capacity'!$A:$A, 0), 1),
        INDEX(Assumptions!$B:$B, MATCH("F9 base booster build rate (boosters/year, pre-V3-trigger)", Assumptions!$A:$A, 0)),
        INDEX(Assumptions!$B:$B, MATCH("F9 base booster build rate (boosters/year, pre-V3-trigger)", Assumptions!$A:$A, 0))
        * MAX(0, 1 - (D$4 - INDEX('Launch Capacity'!$D:$AC, MATCH("V3 Starlink launch trigger year", 'Launch Capacity'!$A:$A, 0), 1))
             / INDEX(Assumptions!$B:$B, MATCH("F9 build-rate decay window (years)", Assumptions!$A:$A, 0)))
     )
```

Pre-trigger (year < 2027): F9 built at base rate (8/yr). Post-trigger: linear decay over 8-year window to zero by 2035.

---

### §3.11 LM BV depreciation REMOVED from Group D&A (THE BIG FIX)

**Group P&L R28 Group D&A formula amendment:**

Current formula (from probe):
```
=D23+D24+D25
 +IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Lunar ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)
 +IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Mars ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)
 +INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)  -- corporate D&A
```

**Sprint 11 replacement:**

```
=D23+D24+D25
 +IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("Lunar Mars Module D&A ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)
 +INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)
```

Replaces TWO separate LM BV depreciation reads with ONE Lunar Mars Module D&A read (the proper cash-cap depreciation).

**Group P&L R36 Σ Module D&A in COGS — same amendment**: remove the two LM BV depreciation reads; replace with single Lunar Mars Module D&A.

**Lunar Mars tab — new row needed: `Lunar Mars Module D&A ($mm)`**

Formula (at next available LM row, e.g., R119):
```
=IFERROR(
   SUMIF($D$5:D$5, "<="&D$5, $D$13:D$13)  -- cumulative Lunar Mars CapEx through year T (read LM Module CapEx R205 across years; depending on LM tab layout, may need to read R13 carve-out cash inflow instead)
   / INDEX(Assumptions!$B:$B, MATCH("Lunar Mars capital lifetime (years)", Assumptions!$A:$A, 0)),
   0
)
```

Plugin pre-flight resolves the canonical label for LM cumulative CapEx (could be R205 Module CapEx running sum, or LM module body has a dedicated row).

**Lunar Mars R117 (BV depreciation — Lunar) + R118 (BV depreciation — Mars)**: keep formulas (BV decay is still relevant for Valuation tab terminal anchor per Architecture §11.4 retained). Update col A labels to flag SoTP-only usage:
- R117 → `Memo: BV decay — Lunar ($mm/yr) — Valuation input only, NOT in Group D&A`
- R118 → same for Mars

**Lunar Mars COGS structure (§11.5 amendment)**: LM Module COGS = mission ops only. Remove BV depreciation from LM Module COGS. LM Module D&A appears in Group D&A via the new R119 row read.

**Verification reads:**
- Group P&L D28 Group D&A 2025: should drop from $1,261M baseline (which already excluded LM BV early years; LM BV starts low) to roughly same range (LM BV early years was small) — verify ±5%
- Group P&L AC28 Group D&A 2050: should drop from $484,076M to ~$6-7B (Constellation $5.1B + CL $267M + Corp $307M + LM Module D&A ~$200-500M depending on cumulative LM CapEx)
- Group P&L AC50 Group FCF 2050: should DROP from +$337,548M to roughly -$90B (correct; was illusory)
- R108 = "OK" all years (mandatory)

**Halt condition**: AC28 Group D&A > $20B → HALT (LM BV depreciation refs may not have been fully removed; structural error remains).

---

### §3.12 ODC unit-economics audit (read-only, no auto-fix)

Read + document per-sat IRR trajectory + per-sat economics:

```
Read ODC R102 Per-sat external compute revenue: D=0, I=$0.5M, AC=$0.5M
Read ODC R150 ODC fleet design life: 5 years
Read ODC R154 Per-sat net marginal revenue: D=0, I=$0.5M, AC=$0.5M
Read ODC per-sat cost components from Assumptions: R151 solar gen 156kW × R154 $/W $8 = $1.25M; R152 thermal mass 480kg × R155 $/kg $3000 = $1.44M; R175 chip cost per chip × chip count per sat
Read ODC R207 Spot IRR: -0.39 (2025), -0.10 (2030), -0.15 (2050)
```

**Document in Claude Log**: ODC per-sat economics — lifetime revenue ~$2.5M (= $0.5M × 5yr) vs per-sat cost ~$3-5M = negative IRR. Sprint 11 accepts as model verdict per Vlad lock 2026-05-26. Sprint 11.5 unit-economics pass may revise per-sat revenue (compute pricing) OR per-sat cost (chip cost trajectory) inputs. No spec body changes in Sprint 11.

---

### §3.13 Customer Launch R210 Capacity Demand wire

Add R210 formula on Customer Launch tab:

```
R210 Capacity Demand (kg-to-LEO) = IFERROR(R24 Starship customer launches per year * INDEX('Launch Capacity'!$D:$AC, MATCH("Per-launch upmass (kg)", 'Launch Capacity'!$A:$A, 0), D$5+1), 0)
```

If CL R24 Starship customer launches = 0 (currently), R210 = 0 still. But canonical label resolves for Allocator vehicle build claim sum (R143 in Sprint 10 spec).

---

## §4 Verification

### §4.1 Workbook-wide error scan

Zero `#REF!` / `#VALUE!` / `#DIV/0!` / `#NAME?` / `#N/A`.

### §4.2 Conservation R108 = "OK" all years 2025-2050; R109 = 0 all years

Mandatory. If LM BV depreciation removal causes conservation breach, HALT.

### §4.3 Three-gate verification

- V3 BB launches D, E (2025, 2026) = 0; F (2027) > 0 (post-fleet-wiring + post-trigger)
- V2 BB launches D, E, F (2025-2027) > 0; G (2028) = 0
- V2 DTC same pattern

### §4.4 Calibration drift surface

| Metric | V2.13 baseline | V2.14 expected (Sprint 11) | Halt range |
|---|---|---|---|
| Group D10 Revenue 2025 | $13,855M | ~$13,800-14,200M (small drift from deployment-binding tightening) | <$10k or >$17k |
| Group D26 EBITDA 2025 | $4,358M | ~$4,200-4,500M | <$2.5k or >$6k |
| Group D28 Group D&A 2025 | $1,261M | ~$1,200-1,400M (LM BV impact small in 2025) | <$800 or >$2k |
| Group D50 FCF 2025 | -$3,050M | ~-$2,800 to -$3,500M | <-$5k or >-$1k |
| Group I10 Revenue 2030 | $135,898M | ~$130-150B (with V3 deployment now ramping via endogenous fleet) | <$80k or >$200k |
| Group AC10 Revenue 2050 | $583,059M | ~$500-650B | informational |
| **Group AC28 Group D&A 2050** | **$484,076M** | **~$6-7B** ⬇⬇⬇ massive drop | <$2B or >$20B (HALT if >$20B) |
| **Group AC50 FCF 2050** | **+$337,548M** | **~-$90B to +$50B** depending on EBITDA × D&A interplay | informational |
| Allocator D88 V2 BB cash alloc | n/a | $1,116M | <$1,000 or >$1,300 |
| Allocator F90 V3 BB cash alloc 2027 | n/a | non-zero (V3 trigger fires) | =0 (HALT) |
| Allocator G88 V2 BB cash alloc 2028 | n/a | 0 (V2 phase-out fires) | ≠0 (HALT) |
| Launch Capacity D25 Starship built 2025 | 0 | ~0.5 vehicles ($50M / $90M) | informational |
| Launch Capacity I34 Total Annual Capacity 2030 | 0 | non-zero (endogenous fleet wired) | =0 (HALT — wiring failed) |
| Starlink D33 V2 BB launches 2025 | 2,987 | 2,987 (first-year override) | ≠ 2,987 |
| Starlink F39 V3 BB launches 2027 | 0 | non-zero (post-trigger + fleet wired) | =0 (HALT) |
| Starlink G33 V2 BB launches 2028 | undefined post-Sprint-11 | 0 (V2 phase-out) | ≠0 (HALT) |
| Allocator D108-AC108 R108 conservation | "OK" all 26 yrs | "OK" all 26 yrs | any "CHECK" |

**Sprint 9 §6.8 calibration revision triggered**: Group D&A 2050 from $484B → $6B; Group FCF 2050 from +$337B → ~-$90B. New targets to be locked by Vlad post-Sprint-11 before Sprint 12 Valuation.

### §4.5 Rule 22 stale-ref scan

Verify all NEW cross-tab refs resolve to canonical labels:
- Starlink R8-R13 → Allocator vehicle canonical labels (R88-R91, R138-R139)
- Allocator §4 V2 BB/V2 DTC/V3 BB/V3 DTC sub-blocks → Starlink memo IRR rows R215/R220/R225/R230 + per-vehicle CapEx R88-R95
- Allocator §6 V3 BB/V3 DTC kg sub-blocks → Starlink R49/R50 + V3 trigger from Launch Capacity R56
- Launch Capacity R25 endogenous → Allocator R150 Vehicle build claim
- Group P&L R28 → Lunar Mars `Lunar Mars Module D&A ($mm)` NEW row + Corporate D&A (Confirm REMOVED: LM BV depreciation refs)
- Starlink R33/R37/R39/R41 deployment → Allocator IN R8-R13 + Assumptions phase-out / Launch Capacity trigger
- Customer Launch R205 / ODC R205 / AI Stack R205 deployment binding refs

### §4.6 Round-trip stability test (5x recalc)

No value movement >$1M. Key cells: Group P&L D10, D26, D50, AC10, AC28, AC50 + Allocator D88-D91, F90, G88 + Starlink D33, F39, G33 + Launch Capacity D25, I34.

### §4.7 Claude Log entry

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-MM-DD | 11 | Allocator (§4 cash queue → 7 sub-blocks; §5 R83-R91 expanded with 4 new vehicle labels; §6/§7/§8/§9 headers relocated +4 rows; §6 kg queue → 5 sub-blocks; §7 R137-R143 expanded with 2 new V3 kg labels), Starlink (R7-R14 Module IN expanded; R33/R37/R39/R41 deployment rewired with 3 gates + MIN bind; R43 ratchet retired), Customer Launch (R205 deployment binding; R210 Capacity Demand wired), ODC (R205 deployment binding), AI Stack (R205 binding stub), Launch Capacity (R8/R9 cost components across years; R25 boosters built = f(R150); R61 F9 build endogenous decay), Lunar Mars (R117/R118 col A retirement labels; new R119 Lunar Mars Module D&A), Assumptions (R350 V2 phase-out year; R320 V2 DTC cap retired), Group P&L (R28 + R36 LM BV depreciation refs REMOVED) | Combined Sprint 11 PASS: vehicle-level allocator LIVE; 3 physical gates working; deployment binding mandatory; endogenous Starship + F9 fleet wired; LM BV depreciation correction landed (Group D&A 2050 dropped $484B → ~$6B); ODC verdict accepted as model output. V30.5 Lessons §2 + §6.5 deployment binding finally land end-to-end. Architecture §20 amendments block now load-bearing. | Sprint 9 §6.8 calibration target revision (mandatory before Sprint 12 — Group D&A + FCF 2050 swings dramatically); Sprint 11.5 ODC unit-economics revision (Vlad-pending decision on per-sat compute revenue OR per-sat cost inputs); R110 Σ Module FCF residual still pending (now -$1,640M baseline); R150 vehicle build claim 2026+ should now size correctly post-§3.9. | Sprint 12 (Valuation) — per-vehicle DCF for Starlink (4 vehicles); per-module DCF for CL/ODC/AIS; SoTP football field (8 entries); LM BV terminal value (NOT depreciated into D&A); WACC; sensitivity table. |

---

## §5 Outstanding items

1. **Sprint 9 §6.8 calibration revision conversation TRIGGERED** — mandatory before Sprint 12. Group D&A 2050 swings from $484B → $6B; Group FCF 2050 swings from +$337B → ~-$90B. Vlad locks new targets reflecting corrected mechanics.
2. **Sprint 11.5 ODC unit-economics revision (Vlad decision pending)** — per-sat compute revenue ~$0.5M/yr × 5yr = $2.5M lifetime vs per-sat cost ~$3-5M. Negative IRR is current model verdict. Vlad to decide: accept verdict (ODC stays at zero forever), revise revenue inputs (Mach33 thesis position higher), or add ODC strategic carve-out (Architecture §11 amendment to make ODC a strategic line like Lunar Mars).
3. **R110 Σ Module FCF residual** — still pending; -$1,640M baseline in V2.13. May resolve with LM BV correction (if residual was tied to LM BV double-counting); audit post-Sprint-11.
4. **AC_2050 Group EBITDA still negative** — Lock f finding. Was -$44.5B; will be similar post-Sprint-11 (LM BV wasn't in COGS; EBITDA negativity tied to OpEx-vs-revenue ratio in late years — separate concern). Sprint 12 Valuation surfaces.
5. **Starlink module-level R209 Blended IRR rollup formula** — currently reads aggregate; with vehicle-level allocator, this becomes informational only. Update R209 to capital-weighted average of per-vehicle IRRs OR remove as decorative (allocator no longer reads R209). Plugin judgment at execution.

---

## §6 Amendment log

- **2026-05-26 (initial draft)** — Sprint 11 spec authored as combined cleanup absorbing former Sprint 10.7 + 10.7+ + 10.8 + 10.9. Vlad lock 2026-05-26: "give me all of these in one sprint. change whatever you need to architecture and methodology". Architecture & Methodology constitutional doc amended in parallel — new §20 amendments block (lines 873-1077) + §19 amendment log entry. 13 §3 sections; 6 new canonical labels; 8 architectural amendments captured in Architecture §20.1-§20.8.

---

## End of Sprint 11 Spec
