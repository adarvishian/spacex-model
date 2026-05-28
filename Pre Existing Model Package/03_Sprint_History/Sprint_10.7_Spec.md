# Sprint 10.7 Spec — Vehicle-level allocator + deployment-binding + 3 physical gates

**Sprint name**: Vehicle-level Allocator brain — lift Starlink V2 BB / V2 DTC / V3 BB / V3 DTC to top-level allocator entries; bind deployment formulas on Allocator IN per Architecture §6.5; retire hardcoded V2/V3 ratchet logic; add 3 physical gates (V3 startup year, V2 phase-out year, F9 supply constraint for V2 deployment).

**Status**: spec-author chat, drafted 2026-05-26 after Sprint 10.5 PASS (V2.13). Triggered by Vlad surfacing that (1) Starlink module deployment doesn't bind on Allocator IN (modules deploy what they want regardless of allocator allocation); (2) Starlink's per-vehicle structure has IRR engines + per-vehicle CapEx but no per-vehicle ALLOCATION — module gets one bucket, internal V2→V3 ratchet is hardcoded. With Sprint 10.5 demand curves + finite-diff per-vehicle marginal IRR now economically reliable, vehicle-level allocator becomes possible — and V30.5 Lessons §2 (per-sat IRR breaks chicken-and-egg) finally lands end-to-end.

**Dependencies landed**: Sprint 10 (Allocator brain skeleton + Cash Pool + Queue Gate + module-level cash/kg sigmoid + Vehicle build claim). Sprint 10.5 (Demand Curves rebuilt as Q→Revenue lookup tables; finite-diff marginal revenue R212/R217/R222/R227; per-vehicle Spot/Forward/Blended IRR R213-R230 economically reliable).

**Three architectural locks confirmed by Vlad 2026-05-26**:
- **(a) F9 supply gate** — V2 BB / V2 DTC deployment binds on F9 launches available (after Customer Launch external customer F9 demand reserved)
- **(b) V3 startup gate** — V3 BB / V3 DTC demand zeroed pre-trigger year (Launch Capacity R56 = 2027) via `IF(year >= trigger, demand, 0)`. Clean physics constraint without binary ratchet flag.
- **(c) V2 phase-out year** — new Assumptions MC input (Base Case 2028); `IF(year >= V2_phase_out, V2 cash + F9 demand, 0)`. Same shape as V3 startup gate. V2 stops launching post-phase-out year regardless of IRR (physical/production decision).

**Sprint 10.5 carry-forwards** (not Sprint 10.7 scope; tracked in Outstanding §5):
- D&A 384× growth concern (Sprint 10.8 audit queued)
- ODC per-sat IRR negative throughout (Sprint 10.9 audit queued)
- R110 Σ Module FCF residual worsens through V2.13 to −$1,640M by 2050
- R150 vehicle build claim 2026+ = $0 due to Launch Capacity R8/R9 D-only static inputs
- AC_2050 Group EBITDA worsened to −$44,521M (Lock f finding got worse, not resolved)

---

## §0 Rule Compliance Preamble (mandatory)

- [x] **Rule 1** (one concept per write) — every §3.x writes labels first, formulas second, formats third. Per-vehicle sub-blocks ship as discrete write batches.
- [x] **Rule 3 / 23** — V3 startup + V2 phase-out gates use Rule 23-compliant `IF(D$4 >= year_input, ...)` against absolute Assumptions cells. No year-chained recursion. All ramp formulas use anchor-and-offset.
- [x] **Rule 4** (verification gate) — every §3.x ends with D/I/S/AC read-backs + expected values. §4 consolidates calibration check + 3-gate verification (pre-2027 V3=0; post-2028 V2=0; F9 V2 launches ≤ F9 available).
- [x] **Rule 6** (inline formulas) — every formula specified with full Excel text. Long canonical labels quoted in code fences (per `feedback_quote_canonical_labels_verbatim` memory).
- [x] **Rule 10** (no row insertions) — section headers MAY relocate on Allocator (consumer tab; all cross-tab refs use INDEX/MATCH by label per Rule 12, immune to row shifts). Per-vehicle canonical labels APPEND below existing R83-R87 at R88-R91 (within existing reserved space pre §6 header). Starlink Module IN block expands using existing reserved rows below R10. NO row insertions on Group P&L, OpEx, CapEx, or module tabs (cross-referenced).
- [x] **Rule 11** (touch points) — every new per-vehicle canonical row enumerates: (1) consumer (Starlink Module IN R8-R13); (2) downstream — Starlink R33/R37/R39/R41 deployment formulas; (3) module-level rollup (Starlink R84 cash allocation = SUM of 4 vehicle allocations; Σ kg allocation similar); (4) conservation R108 must hold; (5) Group P&L reads stay unchanged (read Starlink module Total Revenue R201 + Module CapEx R205 + Module FCF R204 — all module-level rollups still work).
- [x] **Rule 12** — every per-vehicle reference uses canonical label INDEX/MATCH. Vehicle canonical labels published verbatim in §3.4 below.
- [x] **Rule 13** — N/A. Sprint 10.7 rewires Starlink deployment + allocator structure. Module body convention unchanged (Revenue → COGS → EBITDA → CapEx → FCF; per-vehicle CapEx already exists at R88-R95).
- [x] **Rule 14** — V2 phase-out year added as Assumptions input (no hardcoded constants). V3 trigger year already exists at Launch Capacity R56. F9 supply availability read from existing Launch Capacity R64.
- [x] **Rule 15** (sanity halt thresholds) — 3-gate verification quantitative thresholds: V3 launches = 0 for year 2025, 2026 (pre-trigger 2027); V2 launches = 0 for years >= 2028 (V2 phase-out); Σ F9 internal launches (Starlink V2) ≤ F9 Annual Capacity − F9 external customer launches. Plus standard calibration: R108 = "OK" all years; round-trip stability < $1M.
- [x] **Rule 19** — Vlad handles all saving.
- [x] **Rule 22** — §4 Verification §4.4 Rule 22 scan enumerates new cross-tab pulls (Starlink Module IN per-vehicle reads from Allocator vehicle canonical labels; per-vehicle deployment reads of Allocator IN + F9 capacity + V3 trigger + V2 phase-out).

**Architecture compliance:**

- [x] Allocator §4 cash queue extends per Architecture §6.3 — same sigmoid formula `MAX(IRR, 0)^k`, k=2; sub-blocks add per-vehicle entries for Starlink only (other modules unchanged).
- [x] Allocator §6 kg queue extends per Architecture §6.4 — V3 vehicles in queue; V2 vehicles NOT in kg queue (V2 uses F9, not Starship).
- [x] Module deployment binds on Allocator IN per Architecture §6.5 — `MIN(cash_alloc / cost, kg_alloc / mass OR F9_launches_avail / sats_per_launch, internal_demand)`.
- [x] First-year override per-vehicle (Sprint 10 Lock a extended to vehicle granularity).
- [x] Module-level Allocator OUT (R201-R210) on Starlink stays for Group P&L compatibility — rollup of per-vehicle outputs.

---

## §1 Scope summary

| Section | What ships | Tabs touched |
|---|---|---|
| §3.0 Pre-flight | 9 halt-bearing checks on Sprint 10.5 PASS + per-vehicle IRR + F9 supply + V3 trigger | read-only |
| §3.1 Architecture §4 + §6 amendment | Constitutional doc edit; vehicle-level allocator contract for Starlink | constitutional doc (Vlad applies) |
| §3.2 Assumptions §12 new input | V2 phase-out year (Base Case 2028, MC range) | Assumptions append: R350 |
| §3.3 Allocator §4 cash queue expand | 3 new per-vehicle sub-blocks (V2 DTC, V3 BB, V3 DTC); existing Starlink sub-block becomes V2 BB sub-block. Layout: 5-row compact sub-blocks within R40-R80 range | Allocator R40-R80 |
| §3.4 Allocator §5 canonical labels expand | 4 NEW per-vehicle cash allocation labels at R88-R91; R83-R87 unchanged (Starlink R84 becomes SUM rollup of 4 vehicles) | Allocator R83-R91 |
| §3.5 Allocator §6 kg queue expand | 2 new per-vehicle sub-blocks (V3 BB, V3 DTC); existing Starlink kg sub-block restructures (V2 vehicles NOT in kg queue) | Allocator R90-R130 |
| §3.6 Allocator §7 kg canonical labels expand | 2 NEW per-vehicle kg labels at R138-R139 (V3 BB, V3 DTC); R134 Starlink kg = SUM rollup | Allocator R133-R139 |
| §3.7 Starlink Module IN block expand | R8 = V2 BB cash; R9 = V2 DTC cash; R10 = V3 BB cash; R11 = V3 DTC cash; R12 = V3 BB kg; R13 = V3 DTC kg; R14 = Total Capital Available rollup | Starlink R8-R14 |
| §3.8 Per-vehicle deployment formula rewire | R33 V2 BB / R37 V2 DTC / R39 V3 BB / R41 V3 DTC — MIN(cash/cost, F9-or-Starship constraint, internal_demand) × IF(gate) | Starlink R33, R37, R39, R41 |
| §3.9 Retire hardcoded ratchets | R43 V2/V3 ratchet flag → cleared with retirement note; Assumptions R320 V2 DTC permanent cap → cleared with retirement note | Starlink R43, Assumptions R320 |
| §3.10 Module-level deployment binding | Customer Launch + ODC + AI Stack module CapEx formulas (R205 on each tab) bind on Allocator IN R8 | Customer Launch R205, ODC R205, AI Stack R205 |

**Publishes 6 NEW canonical labels** (Rule 12 — verbatim case-sensitive):
1. `Starlink V2 BB cash allocation` — Allocator R88
2. `Starlink V2 DTC cash allocation` — Allocator R89
3. `Starlink V3 BB cash allocation` — Allocator R90
4. `Starlink V3 DTC cash allocation` — Allocator R91
5. `Starlink V3 BB kg allocation` — Allocator R138
6. `Starlink V3 DTC kg allocation` — Allocator R139

Existing canonical labels at R83-R87 + R133-R137 stay unchanged (Starlink module-level rollups become SUM formulas of per-vehicle).

---

## §2 Constitutional reference

- **Lessons §2** — Per-sat marginal IRR breaks chicken-and-egg. Sprint 10.7 is the END of the chain. V30.5 introduced per-sat IRR engines (R213-R230 lineage) but the allocator couldn't act on per-vehicle signals — module-level allocation was the bottleneck. With Sprint 10.5 demand curves making IRR signals economically reliable + Sprint 10.7 lifting vehicles to top-level allocator entries + deployment binding, the IRR engines finally drive deployment decisions. Memory `project_vehicle_level_allocator_2026_05_26` documents the architectural insight.
- **Lessons §22** — Within-year cycle bistability. Sprint 10.7 introduces a NEW cycle layer: per-vehicle deployment ← per-vehicle allocation ← per-vehicle IRR ← per-vehicle marginal revenue (via curve finite-diff) ← Starlink Total Gbps supplied ← per-vehicle deployment. Cycle is broken by the curve's "Q is current-year" snapshot — marginal revenue computes at CURRENT Q, then deployment adds sats, Q grows next year. Within-year shouldn't oscillate because Q is read at year-start. Verify <10 iter convergence + 5x round-trip stability.
- **Architecture §6.5** — Actual deployment = MIN(cash/cost, kg/mass, internal_demand). Sprint 10 specified this; Sprint 10 module deployment formulas didn't implement. Sprint 10.7 implements end-to-end for all 4 Starlink vehicles + 3 other modules (CL, ODC, AIS).
- **Architecture §11** — Lunar Mars stays OUTSIDE both queues (strategic carve-out). Unchanged.

---

## §3 Execution

### §3.0 Pre-flight (READ-ONLY — halt if any check fails)

**Check 1 — Sprint 10.5 PASS values intact:**
```
Read Allocator D15 expect $5,000M; D29 expect $0; D35 expect $1,000M; D108 ("OK"); D109 ≈ 0
Read Starlink D120 expect ~$6,746M (BB Rev from curve); D131 expect ~$142M (DTC Rev from curve)
Read Demand Curves D141 expect 1.000 (TAM shift t=0); AC141 expect ~3.85
Read Group P&L D10 expect ~$13,855M; D108 = "OK" all years D:AC
```
HALT if any drift.

**Check 2 — Per-vehicle IRR engines + memo rows resolve verbatim:**
```
MATCH Starlink "Memo: V2 BB Spot IRR" expect R213; "Memo: V2 BB Forward IRR (Y+2)" R214; "Memo: V2 BB Blended IRR" R215
MATCH Starlink "Memo: V2 DTC Spot IRR" R218; "Memo: V2 DTC Forward IRR (Y+2)" R219; "Memo: V2 DTC Blended IRR" R220
MATCH Starlink "Memo: V3 BB Spot IRR" R223; "Memo: V3 BB Forward IRR (Y+2)" R224; "Memo: V3 BB Blended IRR" R225
MATCH Starlink "Memo: V3 DTC Spot IRR" R228; "Memo: V3 DTC Forward IRR (Y+2)" R229; "Memo: V3 DTC Blended IRR" R230
Read Starlink D215 V2 BB Blended IRR expect ~0.75; D225 V3 BB Blended IRR expect ~3.62; D220 V2 DTC Blended IRR expect ~0.14; D230 V3 DTC Blended IRR expect ~1.31
```

**Check 3 — Per-vehicle CapEx + launch routing rows exist:**
```
MATCH Starlink "V2 BB launches per year" R33; "V2 DTC launches per year" R37; "V3 BB launches per year" R39; "V3 DTC launches per year" R41
MATCH Starlink "F9 V2 BB launches (internal)" R45; "F9 V2 DTC launches (internal)" R46; "Starship V3 BB launches (internal)" R47; "Starship V3 DTC launches (internal)" R48
MATCH Starlink "V3 BB Starship kg demand" R49; "V3 DTC Starship kg demand" R50
MATCH Starlink "V2 BB sat unit cost ($mm/sat)" R78; "V2 DTC sat unit cost ($mm/sat)" R79; "V3 BB sat unit cost ($mm/sat)" R80; "V3 DTC sat unit cost ($mm/sat)" R81
MATCH Starlink "V2 BB sat CapEx ($mm)" R88; "V2 BB facility CapEx ($mm)" R89; "V2 DTC sat CapEx ($mm)" R90; "V2 DTC facility CapEx ($mm)" R91; "V3 BB sat CapEx ($mm)" R92; "V3 BB facility CapEx ($mm)" R93; "V3 DTC sat CapEx ($mm)" R94; "V3 DTC facility CapEx ($mm)" R95
MATCH Starlink "Module CapEx ($mm)" R98
MATCH Starlink "V2/V3 ratchet flag (1 = V3 has started launching, V2 BB stops)" R43
```

**Check 4 — V3 trigger year + V2 DTC permanent cap (sources to retire):**
```
Read Launch Capacity R56 "V3 Starlink launch trigger year" expect 2027
MATCH Assumptions "V2 DTC permanent cap flag (1 = no V2 DTC launches 2026+)" expect R320; read B320 expect 1
```

**Check 5 — F9 supply mechanic:**
```
MATCH Launch Capacity "F9 Annual Capacity (kg-to-LEO)" expect R68; read D68 expect ~7,660,800
MATCH Launch Capacity "F9 launches per year" expect R64; read D64 expect ~171
MATCH Customer Launch "F9 customer launches per year" expect R25; read D25 expect ~38.6 (external customer F9 demand)
```

**Check 6 — Assumptions per-vehicle Gbps + per-sat mass:**
```
MATCH Assumptions "V2 Mini Bandwidth per Sat — BB (Gbps)" R75; read B75 expect 96
MATCH Assumptions "V2 Mini Bandwidth per Sat — DTC (Gbps)" R76; read B76 expect 0.2
MATCH Assumptions "V3 BB Bandwidth per Sat — base year (Gbps)" R77; read B77 expect 1000
MATCH Assumptions "V3 DTC Bandwidth per Sat (Gbps)" R78; read B78 expect 2.75
MATCH Assumptions "V3 Mass (kg)" R74; read B74 expect 2000
MATCH Assumptions "Sats per Starship launch — V3 BB"; MATCH "Sats per Starship launch — V3 DTC"
MATCH Assumptions "Sats per F9 launch — V2 BB"; MATCH "Sats per F9 launch — V2 DTC"
```
If any returns #N/A: HALT and resolve canonical label drift.

**Check 7 — Allocator §4 + §5 + §6 + §7 current layout positions:**
```
MATCH Allocator "§4 CASH IRR-PRIORITY SIGMOID QUEUE" expect R39
MATCH Allocator "§5 MODULE CASH ALLOCATIONS (canonical labels — read by module IN blocks)" expect R82
MATCH Allocator "Customer Launch cash allocation" R83; "Starlink cash allocation" R84; "ODC cash allocation" R85; "AI Stack cash allocation" R86; "Lunar Mars cash allocation" R87
MATCH Allocator "§6 KG IRR-PRIORITY SIGMOID QUEUE" expect R89
MATCH Allocator "§7 MODULE KG ALLOCATIONS (canonical labels — read by module IN blocks)" expect R132
MATCH Allocator "Customer Launch kg allocation" R133; "Starlink kg allocation" R134; "ODC kg allocation" R135; "AI Stack kg allocation" R136; "Lunar Mars kg allocation" R137
Read R83 through R87 D-col values; R133-R137 D-col values — should match Sprint 10 first-year override + sigmoid landings
```

**Check 8 — Iterative calc + workbook conservation:**
```
Workbook calculation.iterate = True
Group P&L D108:AC108 all "OK"
```

**Check 9 — Module deployment formulas at module-level (current state):**
```
Read formula at Customer Launch R205 (Module CapEx); ODC R205; AI Stack R205; Lunar Mars R205
Confirm NONE currently bind on Allocator IN R8 (= "Capital Allocation ($mm)" row). Per Architecture §6.5 they SHOULD bind; Sprint 10.7 §3.10 implements.
```

If all 9 checks pass: proceed to §3.1.

---

### §3.1 Architecture §4 + §6 + §11 amendment (constitutional doc edit; Vlad applies)

Update `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/02_Architecture_and_Methodology.md` §4, §6, §11 with the following amendments (Vlad pastes; plugin does NOT write to constitutional doc):

```markdown
### §4 Allocator IN/OUT contract — AMENDED 2026-05-26 (vehicle-level for Starlink)

**Status**: AMENDED. Starlink module has 4 vehicle entries (V2 BB, V2 DTC, V3 BB, V3 DTC) as
top-level allocator queue entries. Other modules (Customer Launch, ODC, AI Stack, Lunar Mars)
remain module-level. Starlink module-level Allocator OUT (R201-R210 on Starlink tab) stays
as ROLLUP of per-vehicle outputs for Group P&L compatibility.

**§4.1 Allocator IN block — per-vehicle for Starlink:**
- Starlink R8 V2 BB cash allocation (reads Allocator canonical `Starlink V2 BB cash allocation`)
- Starlink R9 V2 DTC cash allocation
- Starlink R10 V3 BB cash allocation
- Starlink R11 V3 DTC cash allocation
- Starlink R12 V3 BB kg allocation
- Starlink R13 V3 DTC kg allocation
- Starlink R14 Total Capital Available ($mm) — SUM(R8:R11)
- (V2 vehicles have no kg allocation — they fly on F9, not Starship)

Other modules retain single Capital Allocation + kg Allocation IN cells (unchanged).

**§4.2 Allocator OUT contract — module-level rollup stays:**
Starlink module-level R201-R210 rollup (Total Revenue, EBITDA, CapEx, FCF, Spot/Forward/Blended
IRR, Capacity Demand) stays as SUM/aggregate of per-vehicle outputs. Group P&L + cross-tab
consumers continue to read module-level. Per-vehicle IRR rows R213-R230 remain as memos.

### §6 Allocator architecture — AMENDED 2026-05-26 (vehicle-level cash + kg queues for Starlink)

**§6.3 Cash IRR sigmoid blend** — sub-blocks now include 4 Starlink vehicle entries:
- Customer Launch
- Starlink V2 BB
- Starlink V2 DTC
- Starlink V3 BB
- Starlink V3 DTC
- ODC
- AI Stack
- (Lunar Mars OUTSIDE queue per §11)

Per-vehicle Blended IRR reads from Starlink R215/R220/R225/R230 (memo rows already computed).
Per-vehicle cash demand reads from Starlink per-vehicle CapEx rows (R88+R89 for V2 BB; R90+R91
for V2 DTC; R92+R93 for V3 BB; R94+R95 for V3 DTC). Sigmoid weights, shares, allocations
follow §6.3 formula (k=2).

**§6.4 Kg IRR sigmoid blend** — sub-blocks now include 2 Starlink V3 vehicle entries:
- Customer Launch external Starship demand
- Starlink V3 BB
- Starlink V3 DTC
- ODC
- (AI Stack kg demand structurally 0 per §10.4)
- Lunar Mars OFF-THE-TOP per §11.3

V2 vehicles do NOT appear in kg queue (they use F9, not Starship).

**§6.5 Module actual deployment** — formula unchanged, applies per-vehicle for Starlink:
```
V2 BB deployment = IF(year >= V2_phase_out_year, 0,
  MIN(
    V2_BB_cash_alloc / V2_BB_per_sat_cost,
    F9_launches_avail × sats_per_F9_V2_BB,
    internal_uncapped_demand_V2_BB
  )
)

V3 BB deployment = IF(year >= V3_trigger_year,
  MIN(
    V3_BB_cash_alloc / V3_BB_per_sat_cost,
    V3_BB_kg_alloc / V3_mass_per_sat,
    internal_uncapped_demand_V3_BB
  ),
  0
)
```

Same pattern for V2 DTC + V3 DTC.

**F9 launches available** = Launch Capacity!R64 `F9 launches per year` − Customer Launch!R25
`F9 customer launches per year`. V2 BB + V2 DTC compete for the remainder via cash sigmoid
weights (V2 with higher IRR grabs more share if both have demand).

### §11 Strategic carve-out (Lunar Mars) — UNCHANGED

LM stays outside both queues. Cash flow via R35 carve-out floor. Kg reserved off-the-top per
§11.3.
```

After Vlad applies the amendment, plugin proceeds with §3.2.

---

### §3.2 Assumptions §12 new input — V2 phase-out year

Append at next available Assumptions row after R349 (Sprint 10.5 ended at R349 with GNI growth rate). New row R350:

| Row | Col A label (verbatim) | Col B value | Col C MC Min | Col D MC Max | Col E Dist | Col F Notes |
|---|---|---|---|---|---|---|
| R350 | `V2 phase-out year (no V2 BB / V2 DTC launches from this year)` | 2028 | 2026 | 2032 | triangle | Base Case 2028 (V3 ramps fully by then per Vlad 2026-05-26 lock); MC stress 2026 (V3 ramps faster) — 2032 (V2 production line stays open). V2 BB + V2 DTC sat demand = 0 from this year onward, regardless of IRR. Physical production decision. |

Number format col B = `0` (integer year); col C/D = `0` (integer year).

**Verification reads:**
- R350 B = 2028 exact

---

### §3.3 Allocator §4 cash queue — expand to 7 sub-blocks (4 Starlink vehicles + CL + ODC + AIS)

**Layout decision** (per `feedback_spec_specificity` memory — leave row positions to plugin judgment within existing range):

Existing §4 queue spans R40-R80 with 4 sub-blocks (8 rows each + spacers + Σ at R80). To fit 7 sub-blocks in the same range, switch to **5-row compact sub-blocks**:
- Row N: sub-block label (italic; col A only)
- Row N+1: Blended IRR (per-vehicle for Starlink; per-module for others)
- Row N+2: Cash demand (per-vehicle for Starlink; per-module for others)
- Row N+3: Weight = `MAX(IRR, 0)^k × demand_gate` (k=2 from Assumptions R16). Demand gate = IF(demand > 0, 1, 0) — ensures zero-demand modules don't grab share.
- Row N+4: Proposed allocation = `MIN(IF(IRR > 0, demand, 0), Available × MAX(IRR, 0)^k / Σ_weights)`

7 sub-blocks × 5 rows = 35 rows. Layout R41-R75 fits 7 sub-blocks; R80 Σ weights row stays at R80. Plugin chooses exact row positions and ordering.

**Per-vehicle sub-block reads (4 Starlink vehicle sub-blocks):**

For each Starlink vehicle V ∈ {V2 BB, V2 DTC, V3 BB, V3 DTC}:

| Field | Formula |
|---|---|
| Blended IRR | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("Memo: <V> Blended IRR", Starlink!$A:$A, 0), D$5+1), 0)` |
| Cash demand | `<gate> × IFERROR(INDEX(Starlink!$D:$AC, MATCH("<V> sat CapEx ($mm)", Starlink!$A:$A, 0), D$5+1) + INDEX(Starlink!$D:$AC, MATCH("<V> facility CapEx ($mm)", Starlink!$A:$A, 0), D$5+1), 0)` |
| Weight | `=MAX(<IRR_row>, 0)^INDEX(Assumptions!$B:$B, MATCH("Sigmoid IRR-blend exponent k", Assumptions!$A:$A, 0)) × IF(<demand_row> > 0, 1, 0)` |
| Proposed allocation | `=MIN(IF(<IRR_row> > 0, <demand_row>, 0), $D$29 × <weight_row> / $D$80)` |

Where `<gate>` differs by vehicle:
- V2 BB / V2 DTC: `IF(D$4 < INDEX(Assumptions!$B:$B, MATCH("V2 phase-out year (no V2 BB / V2 DTC launches from this year)", Assumptions!$A:$A, 0)), 1, 0)`
- V3 BB / V3 DTC: `IF(D$4 >= INDEX(Launch Capacity!$B:$B, MATCH("V3 Starlink launch trigger year", Launch Capacity!$A:$A, 0)), 1, 0)`
   - Wait — V3 trigger year is at Launch Capacity R56, col B has values: R56 B = ? Let me check. Per Launch Capacity probe R56 D=2027. So this reads col D not col B.
   - Corrected gate: `IF(D$4 >= INDEX('Launch Capacity'!$D:$AC, MATCH("V3 Starlink launch trigger year", 'Launch Capacity'!$A:$A, 0), 1), 1, 0)`
   - Or simpler: read from Assumptions if there's a duplicate; if not, leave the Launch Capacity ref.

**Non-Starlink sub-blocks (CL + ODC + AIS):**

Reads per-module Blended IRR (R209 on module tab) and per-module Cash demand (R205 Module CapEx) — same pattern as Sprint 10 §3.3 sub-blocks. No gate multiplications (Customer Launch operational throughout horizon; ODC/AI Stack handled by their own IRR engines being negative or zero).

**Σ weights row R80:**

`=SUM` of all 7 sub-block weight rows. Plugin enumerates the 7 weight rows at exact positions chosen.

**Verification reads (post-write):**

| Cell | Expected value |
|---|---|
| Starlink V2 BB IRR row D | ~0.75 (= R215 Blended IRR 2025) |
| Starlink V3 BB IRR row D | ~3.62 (= R225 Blended IRR 2025) |
| Starlink V2 BB demand row D | ~$1,116M (= R88 V2 BB sat CapEx 2025 + R89 facility) |
| Starlink V2 DTC demand row D | ~$68M (= R90 V2 DTC sat CapEx) |
| Starlink V3 BB demand row D | $0 (V3 trigger gate fires; D$4=2025 < trigger=2027) |
| Starlink V3 DTC demand row D | $0 (same gate) |
| Starlink V3 BB demand row F (2027) | non-zero (gate passes; reads R92 V3 BB sat CapEx + R93 facility) |
| Starlink V2 BB demand row G (2028) | $0 (V2 phase-out gate fires at year >= 2028) |
| Σ weights D80 | sum of 4 SL vehicle weights + CL + ODC + AIS weights — pre-compute: V2 BB 0.56 + V2 DTC 0.02 + V3 BB 0 (gated) + V3 DTC 0 (gated) + CL 7.44 + ODC 0 (negative IRR) + AIS 0 = ~8.02 (matches Sprint 10 baseline) |

**Halt conditions:**
- V3 BB demand D-col ≠ 0 → HALT (V3 trigger gate failed)
- V2 BB demand G-col (2028) ≠ 0 → HALT (V2 phase-out gate failed)
- Σ of all 7 proposed allocation rows > D29 → HALT (sigmoid math violation)

---

### §3.4 Allocator §5 canonical labels expand — 4 new per-vehicle labels

**Layout:** APPEND 4 new rows at R88-R91 (currently empty per pre-flight; before §6 header at R89... wait, §6 header is at R89). Conflict — R89 already has §6 header.

**Resolved layout:** Place new per-vehicle cash allocation canonical labels at **R88, plus relocate §6 header from R89 to R94** to make room for R88-R91. Plugin relocates §6 header + adjusts §6 sub-block start positions accordingly. Section R88-R91 hosts the 4 new vehicle labels.

Alternative simpler layout: skip relocation — write new labels at R88 (single row) and use multi-row block in remaining empty space. If §6 header MUST move, plugin shifts §6 + §7 + §8 + §9 down by 4 rows. Cross-tab consumers use INDEX/MATCH by label so relocation is safe (Rule 12).

**Recommendation**: shift §6 + §7 + §8 + §9 down by 4 rows. Plugin executes relocation as separate write batch BEFORE writing new canonical labels.

Post-relocation layout:
- R88: `Starlink V2 BB cash allocation`
- R89: `Starlink V2 DTC cash allocation`
- R90: `Starlink V3 BB cash allocation`
- R91: `Starlink V3 DTC cash allocation`
- R93: §6 header (was R89)
- R136: §7 header (was R132)
- R143: §8 header (was R139)
- R156: §9 header (was R152)

Per-vehicle cash allocation formula (one per row R88-R91):

`=<proposed allocation row from §4 sub-block for this vehicle>`

Plus first-year override per-vehicle (D-col only):

| Row | Col D formula (first-year override) | Col E formula (sigmoid output) |
|---|---|---|
| R88 (V2 BB) | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("V2 BB sat CapEx ($mm)", Starlink!$A:$A, 0), 1) + INDEX(Starlink!$D:$AC, MATCH("V2 BB facility CapEx ($mm)", Starlink!$A:$A, 0), 1), 0)` | `=<R88 sub-block proposed allocation in §4>` |
| R89 (V2 DTC) | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("V2 DTC sat CapEx ($mm)", Starlink!$A:$A, 0), 1) + INDEX(Starlink!$D:$AC, MATCH("V2 DTC facility CapEx ($mm)", Starlink!$A:$A, 0), 1), 0)` | same pattern |
| R90 (V3 BB) | `=0` (V3 trigger gate prevents 2025 deployment) | same pattern |
| R91 (V3 DTC) | `=0` | same pattern |

**Starlink module-level rollup R84 update:**

R84 col A label stays `Starlink cash allocation`. Formula changes from Sprint 10 (which read Starlink Module CapEx for first-year override + sigmoid sub-block for E:AC) to:

`R84 D:AC = D88 + D89 + D90 + D91` (sum of 4 vehicle allocations)

Module IN block on Starlink updates accordingly (§3.7 below).

**Verification reads:**
- D88 V2 BB cash alloc = ~$1,116M (first-year override = V2 BB 2025 historical CapEx)
- D89 V2 DTC cash alloc = ~$68M
- D90 V3 BB cash alloc = $0 (V3 gate)
- D91 V3 DTC cash alloc = $0 (V3 gate)
- D84 Starlink cash alloc (rollup) = $1,116M + $68M + 0 + 0 = $1,184M (close to Sprint 10's $1,202M; small drift from facility CapEx routing difference)
- F90 V3 BB cash alloc 2027 = sigmoid output (large — V3 BB Blended IRR ~3.62, biggest weight in cash queue post-trigger)
- G88 V2 BB cash alloc 2028 = $0 (V2 phase-out gate fires)

---

### §3.5 Allocator §6 kg queue expand — V3 vehicles only

Existing §6 kg queue had Starlink module-level sub-block. Replace with 2 vehicle-level sub-blocks (V3 BB, V3 DTC) — V2 vehicles do NOT appear in kg queue.

**Sub-block layout** (per Sprint 10 §3.5 pattern, 5-row compact form):

For each V3 vehicle:
| Field | Formula |
|---|---|
| Blended IRR | `=IFERROR(INDEX(Starlink!$D:$AC, MATCH("Memo: <V3 variant> Blended IRR", Starlink!$A:$A, 0), D$5+1), 0)` |
| Kg demand | `IF(D$4 >= V3_trigger, IFERROR(INDEX(Starlink!$D:$AC, MATCH("<V3 variant> Starship kg demand", Starlink!$A:$A, 0), D$5+1), 0), 0)` |
| Weight | `=MAX(<IRR>, 0)^k × IF(<demand> > 0, 1, 0)` |
| Proposed kg allocation | `=MIN(IF(<IRR> > 0, <demand>, 0), <Capacity available for IRR queue> × <weight> / Σ kg weights)` |

`<Capacity available for IRR queue>` = post-relocation Allocator R94+ row reading Launch Capacity!R34 Total Annual Capacity (kg-to-LEO) minus Lunar Mars kg reserved off-the-top.

**Sub-blocks in §6 kg queue (post Sprint 10.7):**
- Customer Launch (external Starship demand)
- Starlink V3 BB
- Starlink V3 DTC
- ODC
- AI Stack (kg demand structural = 0; weight = 0)
- Σ kg weights at next row

Total = 5 sub-blocks (down from current 4 — was CL/SL/ODC/AIS module-level; now CL/V3 BB/V3 DTC/ODC/AIS with Starlink expanded to 2 V3 vehicles).

**Verification reads:**
- D V3 BB kg demand = 0 (V3 trigger gate)
- F (2027) V3 BB kg demand > 0 (reads Starlink R49)
- I (2030) V3 BB kg demand expect ~7,000,000 kg (Starlink R49 I-col)
- Σ kg weights — depends on Starship capacity availability; Launch Capacity!R34 = 0 still in V2.13 → Capacity available = 0 → all proposed kg allocations = 0 until Launch Capacity fleet wiring lands (Sprint 11+ — see Outstanding §5)

---

### §3.6 Allocator §7 canonical labels expand — 2 new per-vehicle kg labels

Post-§6 header relocation, §7 header is at R136. R137-R142 host kg allocation canonical labels:

- R137: `Customer Launch kg allocation` (unchanged content, position shifted)
- R138: `Starlink V3 BB kg allocation` (NEW)
- R139: `Starlink V3 DTC kg allocation` (NEW)
- R140: `ODC kg allocation` (was R135)
- R141: `AI Stack kg allocation` (was R136)
- R142: `Lunar Mars kg allocation` (was R137)

Plus rollup: `Starlink kg allocation` at some row (e.g., R143) = D138 + D139 (sum of 2 V3 vehicles).

Per-vehicle kg allocation formula (R138-R139):

`=<proposed kg allocation row from §6 sub-block>` (D:AC)

First-year override D-col:
- R138 D = 0 (no Starship kg launches in 2025 historical)
- R139 D = 0

**Verification reads:**
- D138 V3 BB kg alloc = 0 (override + gate)
- I138 V3 BB kg alloc = 0 (Capacity available = 0 because Launch Capacity R34 = 0; carry-forward from Sprint 10)
- Same for D139 / I139 / D140-D142

---

### §3.7 Starlink Module IN block expand to 4 cash + 2 kg reads

Replace existing Starlink R7-R10 IN block with expanded R7-R14 block:

| Row | Col A label | Col D formula |
|---|---|---|
| R7 | `INPUTS FROM CENTRAL ALLOCATOR` (header, unchanged) | — |
| R8 | `Starlink V2 BB cash allocation ($mm)` | `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("Starlink V2 BB cash allocation", Allocator!$A:$A, 0), D$5+1), 0)` |
| R9 | `Starlink V2 DTC cash allocation ($mm)` | `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("Starlink V2 DTC cash allocation", Allocator!$A:$A, 0), D$5+1), 0)` |
| R10 | `Starlink V3 BB cash allocation ($mm)` | `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("Starlink V3 BB cash allocation", Allocator!$A:$A, 0), D$5+1), 0)` |
| R11 | `Starlink V3 DTC cash allocation ($mm)` | `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("Starlink V3 DTC cash allocation", Allocator!$A:$A, 0), D$5+1), 0)` |
| R12 | `Starlink V3 BB kg allocation (kg-to-LEO)` | `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("Starlink V3 BB kg allocation", Allocator!$A:$A, 0), D$5+1), 0)` |
| R13 | `Starlink V3 DTC kg allocation (kg-to-LEO)` | `=IFERROR(INDEX(Allocator!$D:$AC, MATCH("Starlink V3 DTC kg allocation", Allocator!$A:$A, 0), D$5+1), 0)` |
| R14 | `Total Capital Available ($mm)` | `=D8+D9+D10+D11` |

Copy E across F:AC for R8-R14.

**Verification reads:**
- D8 V2 BB cash = $1,116M (first-year override read)
- D9 V2 DTC cash = $68M
- D10/D11 V3 cash = 0 (gate)
- D14 Total = $1,184M (matches D84 Starlink rollup)
- D12/D13 V3 kg = 0

---

### §3.8 Per-vehicle deployment formula rewire

Replace existing Starlink R33/R37/R39/R41 single-cell hardcoded formulas with proper deployment formulas binding on Allocator IN + physical constraints + gates.

**R33 V2 BB launches per year — replacement formula:**

```
=IF(D$4 >= INDEX(Assumptions!$B:$B, MATCH("V2 phase-out year (no V2 BB / V2 DTC launches from this year)", Assumptions!$A:$A, 0)),
  0,
  IF(D$5 = 0,
    -- First-year override: read 2025 historical
    INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Sats Launched 2025", Assumptions!$A:$A, 0)),
    -- 2026+: bound on cash + F9 supply + internal demand
    MIN(
      -- Cash bound: V2 BB cash allocation / per-sat cost
      IFERROR(D8 / INDEX(Starlink!$D:$AC, MATCH("V2 BB sat unit cost ($mm/sat)", Starlink!$A:$A, 0), D$5+1), 0),
      -- F9 supply bound: (F9 launches available for V2 BB) × sats per F9 launch
      IFERROR(
        (INDEX('Launch Capacity'!$D:$AC, MATCH("F9 launches per year", 'Launch Capacity'!$A:$A, 0), D$5+1)
         - INDEX('Customer Launch'!$D:$AC, MATCH("F9 customer launches per year", 'Customer Launch'!$A:$A, 0), D$5+1))
        × <V2 BB share of internal F9 launches>
        × INDEX(Assumptions!$B:$B, MATCH("Sats per F9 launch — V2 BB", Assumptions!$A:$A, 0))
      , 0),
      -- Internal uncapped demand: prior-year + ramp (plugin resolves what Sprint 4 used)
      <internal_uncapped_demand_V2_BB>
    )
  )
)
```

**Note on F9 supply bound**: F9 launches available for V2 BB = (Total F9 launches per year − F9 customer launches) × (V2 BB's share of internal F9 launches). V2 BB and V2 DTC both compete for internal F9 capacity. Two valid approaches:

**(a) Split internal F9 capacity by IRR-weighted cash demand** — V2 BB gets `V2_BB_cash_demand / (V2_BB + V2_DTC cash demand)` of internal F9. Per Vlad's economic logic, V2 BB will dominate since its IRR + demand are larger.

**(b) Use historical anchor ratio** — V2 BB internal F9 share = 80% (historical ratio: 103/(103+26) ≈ 0.8 in 2025); V2 DTC = 20%. Sprint 4 used this implicitly via R45/R46 formulas.

Spec uses Option (b) — historical share. R45 + R46 existing formulas already encode this; Sprint 10.7 keeps R45/R46 as the F9 routing layer. V2 BB launches formula uses the share ratio.

Cleaner formulation (defer F9 split to existing R45/R46 logic): V2 BB launches formula just uses the cash + internal demand constraint; F9 supply is checked via a separate sanity assertion that R45 + R46 + Customer Launch R25 ≤ F9 total capacity.

**Simplified R33 (recommended):**

```
=IF(D$4 >= INDEX(Assumptions!$B:$B, MATCH("V2 phase-out year (no V2 BB / V2 DTC launches from this year)", Assumptions!$A:$A, 0)), 0,
  IF(D$5 = 0,
    INDEX(Assumptions!$B:$B, MATCH("V2 Mini BB Sats Launched 2025", Assumptions!$A:$A, 0)),
    MIN(
      IFERROR(D8 / INDEX(Starlink!$D:$AC, MATCH("V2 BB sat unit cost ($mm/sat)", Starlink!$A:$A, 0), D$5+1), 0),
      <internal_demand_V2_BB>  -- prior-year + ramp logic from existing E33:AC33 if any
    )
  )
)
```

F9 supply is implicitly bound via cash constraint and the F9 fleet build mechanic (Customer Launch F9 build rate scales to demand). If F9 production caps V2 deployment, that gets flagged via §4 verification sanity check.

**R37 V2 DTC** — same template, swap "V2 BB" → "V2 DTC", read R79 unit cost, R76 Gbps/sat (informational only).

**R39 V3 BB** — V3 trigger gate instead of V2 phase-out:

```
=IF(D$4 < INDEX('Launch Capacity'!$D:$AC, MATCH("V3 Starlink launch trigger year", 'Launch Capacity'!$A:$A, 0), 1), 0,
  MIN(
    -- Cash bound
    IFERROR(D10 / INDEX(Starlink!$D:$AC, MATCH("V3 BB sat unit cost ($mm/sat)", Starlink!$A:$A, 0), D$5+1), 0),
    -- Kg bound (Starship)
    IFERROR(D12 / INDEX(Assumptions!$B:$B, MATCH("V3 Mass (kg)", Assumptions!$A:$A, 0)), 0),
    -- Internal demand (uncapped)
    <internal_demand_V3_BB>
  )
)
```

**R41 V3 DTC** — same template, swap "V3 BB" → "V3 DTC", read R81 unit cost, R13 kg allocation.

**Internal uncapped demand placeholder**: Sprint 4's existing year-row deployment formulas had ramp logic for V2 BB / V2 DTC / V3 BB / V3 DTC year-by-year. Sprint 10.7 plugin pre-flight probes E33:AC33 to identify the existing ramp formula; uses that as `<internal_uncapped_demand_V2_BB>` placeholder. If E33 is hardcoded constant (e.g., 3,500/yr), plugin uses INDEX/MATCH on Assumptions for the corresponding ramp parameter. If Sprint 4 only wrote D-col anchors and E:AC ramps don't exist, internal demand defaults to D33 (historical anchor flat across years) — which would mean V2 BB launches at 2,987/yr in perpetuity (capped only by cash + F9 + phase-out gate).

**Critical**: spec author's responsibility ends with specifying the MIN formula structure + gates. Plugin resolves `<internal_demand>` reads at execution from existing Sprint 4 ramp structure or defaults to first-year anchor.

**Verification reads:**
- D33 V2 BB launches = 2,987 (first-year override — D$5=0 branch reads historical anchor)
- E33 (2026) V2 BB launches = MIN(D9 cash / R78 cost, internal_demand) — non-zero pre-phase-out
- G33 (2028) V2 BB launches = 0 (phase-out gate)
- D39 V3 BB launches = 0 (trigger gate; 2025 < 2027)
- F39 (2027) V3 BB launches = MIN(F10 cash / F80 cost, F12 kg / V3_mass, internal_demand) — non-zero post-trigger
- I39 (2030) V3 BB launches = ? (depends on Launch Capacity R34 still = 0 → kg constraint binds at 0 → V3 BB deployment = 0)

**Halt conditions:**
- D33 ≠ 2,987 → HALT (first-year override broken)
- D39 ≠ 0 → HALT (V3 trigger gate broken)
- G33 ≠ 0 → HALT (V2 phase-out gate broken)
- E33 < 0 OR > 100,000 → HALT (sanity check: V2 BB launches per year should be modest)

---

### §3.9 Retire hardcoded ratchets

**R43 V2/V3 ratchet flag — retire:**

Clear D43:AC43 cell values. Update col A label to:
`V2/V3 ratchet flag — RETIRED 2026-05-26 (replaced by V2 phase-out + V3 trigger gates per Sprint 10.7)`

Leave label in place as retirement memo. Any downstream consumer that reads R43 will get 0 (cleared). Pre-flight Check 3 should verify R43 isn't read by any deployment formula post-Sprint-10.7.

**Assumptions R320 V2 DTC permanent cap — retire:**

Clear B320 cell value (currently `1`). Update col A label to:
`V2 DTC permanent cap flag — RETIRED 2026-05-26 (replaced by V2 phase-out year R350 per Sprint 10.7)`

If Sprint 4 or other formulas read R320, plugin pre-flight scans + flags for resolution.

---

### §3.10 Module-level deployment binding (Customer Launch + ODC + AI Stack)

Per Architecture §6.5, module deployment binds on Allocator IN. Sprint 10 module deployment formulas (R205 Module CapEx on each tab) don't currently bind. Sprint 10.7 §3.10 fixes this for 3 modules.

**Customer Launch R205 — replacement formula:**

```
=IF(D$5 = 0,
  -- First-year override: read historical 2025 Customer Launch CapEx
  IFERROR(INDEX(Assumptions!$B:$B, MATCH("Customer Launch 2025 historical Module CapEx ($mm)", Assumptions!$A:$A, 0)), <existing R205 D-col value>),
  -- 2026+: MIN(cash_alloc / unit_cost, kg_alloc / per_unit_kg, internal_demand)
  MIN(
    -- Customer Launch is F9-focused; "unit" = F9 booster
    D8 / INDEX(Assumptions!$B:$B, MATCH("F9 booster (1st stage) mfg cost ($mm/unit)", Assumptions!$A:$A, 0)),
    <existing internal CL demand row>
  ) × INDEX(Assumptions!$B:$B, MATCH("F9 booster (1st stage) mfg cost ($mm/unit)", Assumptions!$A:$A, 0))
)
```

Where:
- D8 on Customer Launch tab = Customer Launch cash allocation IN (= Allocator R83)
- Unit cost = F9 booster mfg cost ($30M/booster per Assumptions R48)
- Internal demand = Customer Launch's current R205 driver (Sprint 4 formula chain)

Customer Launch Module CapEx ≈ unit count × $30M per booster. Sprint 10 D205 = $33M = 1.1 boosters × $30M. Sprint 10.7 first-year override = $33M (matches Sprint 10).

**ODC R205 — replacement formula:**

```
=IF(D$5 = 0,
  -- First-year override = 0 (ODC pre-revenue 2025)
  0,
  -- 2026+: MIN(cash, kg, internal_demand)
  MIN(
    D8 / <ODC per-sat cost from Assumptions>,
    D9 / <ODC per-sat mass>,
    <existing internal ODC demand>
  ) × <ODC per-sat cost>
)
```

Plugin resolves ODC per-sat cost + mass parameter locations from Assumptions.

**AI Stack R205 — replacement formula:**

```
=IF(D$5 = 0, 0, MIN(D8 / <AI Stack per-unit cost>, <existing internal demand>) × <per-unit cost>)
```

AI Stack module is Sprint 6 deferred; per-unit cost may not yet be defined. If Sprint 6 hasn't established per-unit cost canonical label, R205 stays as Sprint 6 stub (= 0). Sprint 10.7 only adds the MIN structure where parameters exist.

**Lunar Mars R205 — UNCHANGED** (Sprint 7 already binds on carve-out cash R35; doesn't go through IRR queue).

**Verification reads:**
- D205 CL = ~$33M (first-year override = matches Sprint 10 baseline)
- E205 CL (2026) = MIN(E8 cash / $30M, internal_demand) × $30M — should be ≤ $33M unless cash allocation grows
- D205 ODC = 0 (first-year override; pre-revenue)
- I205 ODC (2030) = 0 (ODC per-sat IRR negative → cash allocation = 0 → deployment = 0)
- D205 AIS = 0 (Sprint 6 deferred; no change)

---

## §4 Verification

### §4.1 Workbook-wide error scan

Zero `#REF!` / `#VALUE!` / `#DIV/0!` / `#NAME?` / `#N/A` across all 15 tabs.

### §4.2 Conservation block

Group P&L R108 = "OK" all 26 years 2025-2050. R109 = 0 ±$1M all years.

### §4.3 Three-gate verification

| Check | Expected | Halt if |
|---|---|---|
| Starlink R39 V3 BB launches D-col (2025) | 0 | ≠ 0 |
| Starlink R39 V3 BB launches E-col (2026) | 0 | ≠ 0 (still pre-trigger) |
| Starlink R39 V3 BB launches F-col (2027) | > 0 (trigger fires) | = 0 OR > 100,000 |
| Starlink R41 V3 DTC launches D-col, E-col | 0, 0 | ≠ 0 |
| Starlink R41 V3 DTC launches F-col | > 0 | = 0 |
| Starlink R33 V2 BB launches D-col, E-col, F-col (2025-2027) | > 0 (V2 still launching) | = 0 (gate failure) |
| Starlink R33 V2 BB launches G-col (2028) | 0 | ≠ 0 (phase-out failed) |
| Starlink R37 V2 DTC launches G-col (2028) | 0 | ≠ 0 |
| F9 V2 internal launches (Starlink R45 + R46) + F9 customer (Customer Launch R25) ≤ F9 launches per year (Launch Capacity R64) | TRUE all years | FALSE (F9 capacity breach) |

### §4.4 §6.9 calibration

Sprint 10.7 should preserve Sprint 10.5 calibration anchors for 2025 (per-vehicle first-year override holds historical actuals):

| Metric | V2.13 baseline (post-10.5) | Post-10.7 expected | Halt range |
|---|---|---|---|
| Group Revenue 2025 (D10) | $13,855M | $13,800-14,200M (no change expected; revenue mechanic untouched) | <$11k or >$17k |
| Group EBITDA 2025 (D26) | $4,358M | $4,200-4,500M | <$2.5k or >$6k |
| Group FCF 2025 (D50) | −$3,050M | −$3,000-3,200M | <-$5k or >-$1.5k |
| Starlink D205 Module CapEx 2025 | $1,202.5M | $1,184M (= D84 rollup; small drift from facility CapEx accounting) | <$1,000 or >$1,300 |
| Allocator D84 Starlink cash alloc (rollup) | $1,202.5M | $1,184M | same |
| Allocator D88 V2 BB cash alloc | n/a (new row) | $1,116M | <$1,000 or >$1,200 |
| Allocator D89 V2 DTC cash alloc | n/a | $68M | <$50 or >$100 |
| Allocator D90/D91 V3 cash alloc | n/a | 0 (gate) | ≠ 0 |
| Starlink D33 V2 BB launches | 2,987 (first-year anchor) | 2,987 | ≠ 2,987 |
| Starlink D37 V2 DTC launches | 182 | 182 | ≠ 182 |
| Starlink D39 V3 BB launches | 0 | 0 | ≠ 0 |

### §4.5 Out-year trajectory observation

Read Starlink R33/R37/R39/R41 + R98 Module CapEx + R201 Total Revenue + R209 module-level Blended IRR at D, E, F, G, I, S, AC. Document trajectories. Expected qualitative pattern:

- 2025: V2 BB 2,987 launches, V2 DTC 182, V3 BB 0, V3 DTC 0 (first-year override)
- 2026: V2 BB modest (cash + F9 bound), V2 DTC modest, V3 BB 0 (pre-trigger), V3 DTC 0
- 2027: V3 trigger fires — V3 BB ramps if cash + Starship kg available. Caveat: Launch Capacity R34 = 0 in V2.13 (Starship fleet wiring still pending) → V3 BB kg allocation = 0 → V3 BB deployment = 0 via kg constraint. **V3 BB launches likely stay 0 until Launch Capacity fleet wiring lands**.
- 2028: V2 phase-out fires → V2 BB = 0, V2 DTC = 0
- 2028 onwards (with Launch Capacity wiring still pending): V3 BB = 0, V3 DTC = 0, V2 = 0 → **Starlink module deployment goes to 0 in out-years**

This is a significant out-year revenue collapse risk. Sprint 10.7's three gates are correct; the missing piece is Launch Capacity fleet build wiring (carries over from Sprint 10 R150 issue — Vehicle build claim 2026+ = $0 because Launch Capacity R8/R9 D-only static). **Sprint 10.7 surfaces this; Sprint 10.7+ (next micro-patch) must address Launch Capacity fleet build wiring before Sprint 11 can run** — otherwise Starlink deployment 2028+ goes to zero, Group Revenue collapses, Valuation produces nonsense.

### §4.6 Rule 22 stale-reference scan

For every new cross-tab pull written:
- Starlink R8-R13 IN cells → 4 cash + 2 kg canonical labels on Allocator
- Allocator §4 sub-block IRR + demand reads → Starlink memo IRR rows R215/R220/R225/R230 + per-vehicle CapEx rows R88-R95
- Allocator §6 kg sub-block reads → Starlink R49/R50 V3 Starship kg demand
- §4 gate reads → Assumptions V2 phase-out year R350 + Launch Capacity V3 trigger year R56
- Starlink R33-R41 deployment reads → Starlink R8-R13 IN + Starlink R78-R81 unit cost + various Assumptions sat-per-launch
- Customer Launch + ODC + AI Stack R205 deployment binding reads → respective tab R8 IN + unit cost parameters

If any MATCH returns #N/A: halt + identify drift.

### §4.7 Round-trip stability

5× recalc. Group P&L D10, D26, D50, AC10 + Starlink D33, F39, G33 + Allocator D88, F90, G88. Variance < $1M.

### §4.8 Claude Log entry

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-MM-DD | 10.7 | Allocator (§4 cash queue expand to 7 sub-blocks, R83-R91 + R88-R91 new canonical labels, §5/§6/§7/§8/§9 headers relocated +4 rows, §6 kg queue expand to 5 sub-blocks, R133-R142 canonical labels expanded), Starlink (R8-R14 Module IN expand to 4 cash + 2 kg, R33/R37/R39/R41 deployment formulas rewired with 3 gates + MIN bind, R43 retired), Customer Launch (R205 deployment binding), ODC (R205 deployment binding), AI Stack (R205 deployment binding stub), Assumptions (R320 V2 DTC cap retired, R350 V2 phase-out year added) | Vehicle-level allocator LIVE. Starlink V2 BB / V2 DTC / V3 BB / V3 DTC are top-level allocator entries with per-vehicle Blended IRR sigmoid + cash + kg allocation. Hardcoded V2/V3 ratchet (R43) + V2 DTC permanent cap (Assumptions R320) RETIRED — V2→V3 transition emerges from V3 startup gate (Launch Capacity R56 = 2027) + V2 phase-out gate (Assumptions R350 = 2028). Module deployment binding extends to Customer Launch / ODC / AI Stack. PASS/FAIL on §6.9 + 3-gate calibration. V30.5 Lessons §2 (per-sat IRR breaks chicken-and-egg) finally lands end-to-end. | (a) Launch Capacity R8/R9/R34 endogenous fleet build wiring CRITICAL — without this, V3 BB / V3 DTC kg constraint binds at 0 → V3 deployment = 0 → Starlink 2028+ revenue collapses. Sprint 10.7+ micro-patch BEFORE Sprint 11. (b) Sprint 10.8 D&A audit (484× growth concern) still queued. (c) Sprint 10.9 ODC unit-economics audit. (d) R150 vehicle build claim 2026+ E:AC=0 still pending. (e) Sprint 9 §6.8 calibration revision (post all audits). | Sprint 10.7+ — Launch Capacity endogenous fleet build wiring (R8/R9 vehicle costs replicate across years; R25 boosters built per year = function of vehicle build claim cash from Allocator R150; R34 Total Annual Capacity becomes endogenous). Then Sprint 10.8 D&A audit, Sprint 10.9 ODC audit, Sprint 11 Valuation. |

---

## §5 Outstanding items

1. **Launch Capacity endogenous fleet build wiring** — CRITICAL. Without this, V3 BB + V3 DTC kg constraint = 0 → V3 launches = 0 → Starlink 2028+ revenue collapses. Sprint 10.7+ micro-patch must address before Sprint 11.
2. **Sprint 10.8 D&A audit** — 384× D&A growth vs 38× revenue growth 2025-2050. Pre-Sprint-11 audit.
3. **Sprint 10.9 ODC unit-economics audit** — per-sat IRR negative throughout (-0.39 → -0.15). Calibration vs structural?
4. **Sprint 9 §6.8 calibration revision** — Group Revenue 2025 = $13,855M (post-10.5) vs target $14,650M ±5%. Mechanic-driven drift. Lock new targets post all audits.
5. **R110 Σ Module FCF residual** — worsens through V2.13 to -$1,640M by 2050. Module-owner audit.
6. **R150 vehicle build claim 2026+** — $0 in E:AC; Launch Capacity R8/R9 D-col only static. Resolved by Launch Capacity endogenous fleet wiring (item 1).
7. **AC_2050 Group EBITDA = -$44,521M (Lock f worsens)** — Sprint 11 audit. May resolve once Launch Capacity wiring lands + V3 deployment ramps.
8. **F9 supply gate simplification** — Sprint 10.7 §3.8 uses cash + internal demand only (not explicit F9 launches available). If F9 over-utilization emerges (Σ V2 internal + customer F9 > F9 capacity), Sprint 10.7+ adds explicit F9 supply constraint per Vlad lock (a).
9. **Internal V2 BB share of F9** — Sprint 10.7 spec defers to existing R45/R46 historical share (~80/20 V2 BB / V2 DTC). If V2 DTC IRR rises faster than V2 BB late in the V2 lifecycle, F9 split should rebalance via sub-sigmoid. Probably not load-bearing given V2 phase-out 2028.

---

## §6 Amendment log

- **2026-05-26 (initial draft)** — Sprint 10.7 spec authored post-Sprint-10.5 PASS (V2.13). Triggered by Vlad surfacing (1) module deployment doesn't bind on Allocator IN, (2) Starlink module has hardcoded V2/V3 ratchet logic + per-vehicle IRR memos that drive no decisions. Three architectural locks: (a) F9 supply gate for V2; (b) V3 startup gate at Launch Capacity R56 trigger year; (c) V2 phase-out year as new Assumptions input. Spec extends deployment binding to all 4 IRR-positive modules. Architecture §4 + §6 amendment in §3.1 (Vlad applies in parallel). Per-vehicle canonical labels published. Layout: Allocator §6-§9 headers relocate +4 rows to accommodate new R88-R91 vehicle cash labels. Module IN block on Starlink expands R7-R14. Customer Launch + ODC + AI Stack R205 deployment formulas rewired with MIN(cash, kg, internal). Hardcoded R43 ratchet flag + Assumptions R320 V2 DTC cap retired with retirement-note labels.

---

## End of Sprint 10.7 Spec
