# Patch — Sprint 2 → Sprint 3 (F9 retirement engine + F9 demand wiring + Starship ops cost)

**Status**: Patch doc. Not a standalone sprint. To be folded into the Sprint 3 spec by the Sprint 3 spec author at spec-drafting time.
**Date drafted**: 2026-05-20
**Trigger**: Sprint 2 Open Thread items #1 (Starship ops cost), #3 (F9 retirement simplification), #4 (2026 F9 carryover anchors), #5 (F9 launches demand-stub 2027+). Vlad lock 2026-05-20: F9 retirement should mirror the Q4'25 CLEANUP model's launch-driven mechanic, not Sprint 2's flat-6/yr stub. F9 drives customer launches AND most Starship launches stay internal until ~2030. F9 retires ~2030 as launches naturally decline.
**Companion**: References Q4'25 CLEANUP `Earth` tab rows 27–31 (F9 fleet dynamics), 50–56 (F9 + Starship launch breakdown), 68–72 (totals + cumulative), $B$30 (F9 retirement rate), $B$33 (Starship reusable-year flag).

---

## §1 — What this patch changes

Three discrete amendments. Each gets a numbered section in the Sprint 3 spec with its own Rule Compliance Preamble line item, Assumptions amendment (where applicable), and verification gate. They are independent and can be executed in any order within Sprint 3, but all three must land before Sprint 3 declares complete.

### §1.1 Patch A — Replace flat F9 retirement with launch-driven retirement

**Sprint 2 state**: Launch Capacity tab R62 `F9 retired per year (boosters)` = hardcoded 6/yr flat across all years (a simplification, flagged in Sprint 2 §7 Open thread item 2).

**Patch**: Launch-driven retirement mirroring Q4'25 Earth!R30. Each F9 launch consumes 1% of a booster's life (equivalent to 100-launch lifetime, vs Assumptions R55 = 50 lifetime reuses — Q4'25 is more conservative on retirement than Sprint 0 was; lock to Q4'25 for calibration alignment, MC range allows the wider $B$55 = 50 view).

### §1.2 Patch B — Replace F9 launches stub with demand-driven wiring

**Sprint 2 state**: Launch Capacity tab R64 `F9 launches per year` = 171 hardcoded for 2025 + 2026, then 2027+ uses a simple linear decay stub `=MIN(F60×D51, MAX(0, 171×(1-(F$4-D$56)/D$57)))` (a placeholder, flagged in Sprint 2 §7 Open thread item 5).

**Patch**: F9 launches = F9 Starlink internal demand (read from Sprint 4 Starlink V2 BB/DTC launches) + F9 Customer demand (read from Sprint 3 Customer Launch external) + F9 Unused capacity (memo). Mirrors Q4'25 Earth!R68 = SUM(R50, R51, R59). Demand-driven, not stub-driven. As Sprint 4's V3 ratchet fires and V2 launches dry up, F9 internal share collapses; as Sprint 3's customer demand shifts to Starship in the 2027+ window, F9 customer share also drops. F9 launches → ~0 by ~2030 endogenously.

### §1.3 Patch C — Add Starship per-launch ops cost to Assumptions §3 — **SUPERSEDED by Patch E §6.13**

**Original Sprint 2 state**: Launch Capacity tab R37 Starship variable cost formula defaults Starship ops = $0 because Assumptions §3 doesn't have a Starship ops row (only F9 R52 exists). Flagged in Sprint 2 §7 Open thread item 1.

**Original Patch**: Add one Assumptions row for Starship per-launch ops cost = $5M (mirror F9 R52). 

**SUPERSEDED 2026-05-20**: Patch E §6.13 introduces a single `Starship ops + fuel + refurb cost anchor ($mm/launch, 2024 baseline)` = $12M row that subsumes Patch C's $5M scope (and adds the fuel + refurb components Mach33 separates out). Patch C is obsolete — do NOT add a standalone $5M ops-cost row. The §6.13 row covers all per-launch non-manufacturing costs with a Wright's Law decline applied to all of them.

---

## §2 — Patch A details — F9 retirement engine

### §2.1 Q4'25 reference formula

Q4'25 Earth tab:

```
R30: -Retired Rockets   =MAX(-J29, -(J68 × $B$30))
```

Where:
- `J29` = F9 Total Available For Launch (= SoY inventory + manufactured)
- `J68` = F9 Annual Launches
- `$B$30` = 0.01 (= "Percentage of launches in the current year that result in retirement")

Reading the formula: retirements = `J68 × 0.01` (1% of launches turn into retirement), capped at fleet size so you never retire more boosters than exist. Q4'25 stores the value as a negative subtraction (`-J68 × 0.01`); the outer MAX(-J29, …) is the floor (can't retire more than fleet).

Effective F9 lifetime under this rule: 1 / 0.01 = 100 launches per booster, well above Block 5's demonstrated ~30 reuses but below the 100+ theoretical ceiling. The Q4'25 rate is a fleet-average reliability assumption, not a per-booster lifetime cap.

### §2.2 New Assumptions row

Append to Assumptions §3 Capacity section (after R64 — Rule 10, append don't insert). Sprint 3 spec author confirms exact row number based on V2.3 → V2.4 state.

| Field | Value |
|---|---|
| Column A label | `F9 retirement rate (% of launches/year)` |
| Type | VAL (single value) |
| Base Case (B-col) | `0.01` |
| Notes (C-col) | `Q4'25 Earth!$B$30. = "Percentage of launches in the current year that result in retirement." Implies ~100-launch fleet-average lifetime under steady-state. Sprint 0 R55 had lifetime reuses per booster = 50 — those two inputs are reconcilable: R55 = 50 caps any individual booster's flights (technical limit), 0.01 = 0.01 retires on average per launch (probabilistic, captures attrition + mid-life retirement decisions). Patch C amends Launch Capacity R62 to use this rate.` |
| MC Min (AG) | `0.005` |
| MC Max (AH) | `0.02` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `Bookends: 0.5%/launch (= 200-launch lifetime, ultra-conservative) → 2%/launch (= 50-launch lifetime, matches R55). Q4'25 Base Case 1% sits at the central tendency.` |

### §2.3 New Launch Capacity R62 formula

Sprint 3 amends Launch Capacity R62 (preserving Sprint 2's R62 row position; this is a formula replacement, not a row insertion):

```
A62 unchanged: "F9 retired per year (boosters)"

D62 unchanged: =6   (2025 historical anchor: 28 SoY + 17 manufactured − 39 EoY = 6 retired; locks the §6.1 calibration)

E62 = =MIN(E60 + E61, E64 * INDEX(Assumptions!$B:$B, MATCH("F9 retirement rate (% of launches/year)", Assumptions!$A:$A, 0)))
   (2026 onward: retired = MIN(BoY + manufactured, launches × retirement_rate). MIN floors at "can't retire more than fleet exists".
    No negative sign — the row stores retirements as positive count; Sprint 2 R63 formula = BoY + manufactured − retired already subtracts.)

copyToRange source E62, destination F62:AC62
```

D62 stays hardcoded at 6 per Sprint 2 calibration anchor. E62 onwards uses the Q4'25 mechanic.

Sanity check at E62 (2026): if E64 launches = 171 (Sprint 2 carryover), retired = MIN(E60+E61, 171 × 0.01) = MIN(BoY+17, 1.71) = 1.71 boosters retired. Fleet end-2026 = 50 + 17 − 1.71 = 65 — but Sprint 4 will replace E64 with demand-driven launches, which should drop as V3 ramp begins.

By 2030+ with launches naturally declining as Starship displaces F9, retirement count drops, but so does manufactured (Patch B + Sprint 2's R61 mechanic). Net flow: fleet asymptotes to 0 around 2030 as both flows trail off.

### §2.4 Backward-compat: keep R55 Assumptions row

Don't drop Sprint 0 R55 `F9 lifetime reuses per booster = 50`. R55 stays as the booster-D&A-share denominator on Launch Capacity R70 (`=$D$44/$D$50` → $30M/50 = $0.6M D&A per launch). Cost-side D&A uses the technical lifetime (50); fleet-evolution retirement uses the fleet-average rate (1%/launch). Two different concepts using two different inputs is the right architecture — don't conflate them.

---

## §3 — Patch B details — F9 launches demand-driven wiring

### §3.1 Q4'25 reference formula

Q4'25 Earth tab:

```
R68: Falcon 9 Launches    =SUM(J50:J51, J59)
  R50 = Falcon 9 Starlink         (demand from Starlink V2 deployment)
  R51 = Falcon 9 Customer         (external customer commercial + government)
  R59 = Falcon 9 Starlink (mfg)   (incremental from year's manufacturing-driven launches)
  R52 = Falcon 9 Unused Capacity  (memo, supply-side unused)
```

R50 and R51 in 2024 = 89 (Starlink) + 45 (customer) = 134 launches. By 2030+ both decay as Starship handles new constellation deployment and customers shift to Starship.

### §3.2 New Launch Capacity R64 formula

Sprint 3 amends R64 (formula replacement, not row insertion):

```
A64 unchanged: "F9 launches per year"

D64 unchanged: =171   (2025 Q4'25 historical anchor; locks §6.1 calibration)
E64 unchanged: =171   (2026 carryover anchor; pre-V3-ramp)

F64 = =MIN(
         F60 * $D$51,
         IFERROR(INDEX('Customer Launch'!D:D, MATCH("F9 customer launches per year", 'Customer Launch'!$A:$A, 0)), 0)
       + IFERROR(INDEX(Starlink!D:D, MATCH("F9 V2 BB launches (internal)", Starlink!$A:$A, 0)), 0)
       + IFERROR(INDEX(Starlink!D:D, MATCH("F9 V2 DTC launches (internal)", Starlink!$A:$A, 0)), 0)
       )
   (2027 onward: F9 launches = MIN(fleet × cadence ceiling, customer + Starlink V2 internal demand).
    IFERROR wrappers because Sprint 3 builds Customer Launch first; Starlink (Sprint 4) hasn't written its rows yet
    when Sprint 3 verification runs. Starlink rows resolve to 0 until Sprint 4 — at which point F9 internal
    demand lights up. By that point Sprint 4's V3 ratchet logic will be driving the V2 phase-out.)

copyToRange source F64, destination G64:AC64
```

### §3.3 Implied behavior trajectory

With Sprint 3 only (Customer Launch live, Starlink V2 demand at 0 because Sprint 4 hasn't fired):
- 2027 F9 customer launches: per Customer Launch sprint, Q4'25 had ~30-35 customer launches in 2027 (declining from 38.58 in 2025 as Starship displaces F9 customer demand)
- 2027 F9 Starlink internal: 0 placeholder
- Sprint 3 verification will see F9 launches drop sharply 2027+ relative to Sprint 2's stub. Acceptable — Sprint 3 produces a temporary undercount that Sprint 4 corrects.

After Sprint 4 (Starlink V2 demand wired):
- 2027 F9 Starlink V2 BB launches: ~80-100 (peak V2 deployment year)
- 2027 F9 launches total: 80-100 (V2 BB) + 30 (customer) ≈ ~130
- 2028+ as V3 ratchet fires (Architecture §8.2 — once any V3 sat deploys, both V2 lines shut down): V2 launches drop to 0, F9 launches = customer-only
- 2030+ customer demand has shifted mostly to Starship per Q4'25 R56 mechanic: F9 launches → 0
- F9 fleet drains via R62 retirements (now scaled to actual launches × 1%) — fleet self-retires gracefully as launches go to 0

### §3.4 Canonical labels that Sprint 3 + Sprint 4 must publish

For Patch B's INDEX/MATCH calls to resolve, Sprint 3 + Sprint 4 must publish these exact labels on their respective module tabs. Sprint 3 + Sprint 4 spec authors lock these as canonical output labels in their Allocator OUT contracts (per Rule 12, by-label refs):

**Customer Launch (Sprint 3 must publish):**
- `F9 customer launches per year` — year-row of external customer F9 launches; 2025 = 38.58 (Q4'25 anchor), declining trajectory per Sprint 3 input
- `Starship customer launches per year` — year-row; 2025 = 0, ramps from 2027

**Starlink (Sprint 4 must publish):**
- `F9 V2 BB launches (internal)` — year-row of F9 launches consumed by V2 BB deployment; 2025 = ~104 (derived from 2,987 V2 BB sats / V2 BB sats per F9 launch)
- `F9 V2 DTC launches (internal)` — year-row of F9 launches consumed by V2 DTC; 2025 = ~28
- `Starship V3 BB launches (internal)` — year-row; 2025 = 0, ramps post-trigger
- `Starship V3 DTC launches (internal)` — same

Sprint 4 will additionally publish `V2 BB sats per F9 launch` and `V2 DTC sats per F9 launch` as inputs but those don't feed Launch Capacity directly.

If a label drifts between sprints (e.g., Sprint 4 ships `F9 V2BB launches internal` without the parens or hyphens), Patch B's IFERROR wrapper silently swallows the 0 — verification gate catches it via stale-ref scan (Rule 22). Sprint 3 + Sprint 4 spec authors confirm label exactness against this patch doc before plugin execution.

### §3.5 Q4'25 R50/R51/R59 branching — DEFERRED

Q4'25 has a branching IF on the constellation-complete flag (Earth!R271 = "Starlink Constellation Complete"): R50 reads R340 (post-complete) vs R399 (pre-complete). This represents a "Starlink saturated → no more deployment launches" state. The rebuild's V3 ratchet (Architecture §8.2) is a simpler mechanic (single irreversible flag) that captures the same intent without branching INDEX. Defer Q4'25's constellation-complete branching to a future audit sprint if needed.

---

## §4 — Patch C details — Starship per-launch ops cost

### §4.1 New Assumptions row

Append to Assumptions §3 Capacity section (Rule 10). Sprint 3 spec author confirms exact row.

| Field | Value |
|---|---|
| Column A label | `Starship per-launch ops cost ($mm)` |
| Type | VAL (single value) |
| Base Case (B-col) | `5` |
| Notes (C-col) | `Range, propellant, recovery + catch tower ops + booster-ship integration. Mirrors F9 per-launch ops cost (Sprint 0 R52 = $5M) for the early-Starship era; may diverge once Starship achieves Block-5-equivalent operational maturity. Sprint 2 Open Thread item 1 surfaced this gap; Patch C closes it.` |
| MC Min (AG) | `3` |
| MC Max (AH) | `10` |
| MC Distribution (AI) | `triangle` |
| MC Notes (AJ) | `Lower bound (3): Starship ops achieves Falcon 9 cost parity via catch-tower automation. Upper bound (10): Starship ops carry early-era complexity premium (propellant boil-off, fleet management overhead). Wide MC because Starship ops cost has no historical anchor.` |

### §4.2 Updated Launch Capacity R37 formula

Sprint 3 amends Launch Capacity R37 (formula replacement, no row insertion):

```
A37 unchanged: "Starship variable cost per launch ($mm)"

D37 = =D9 * (1 - D20) + D9 * D10 * D20 + INDEX(Assumptions!$B:$B, MATCH("Starship per-launch ops cost ($mm)", Assumptions!$A:$A, 0))
   (2nd-stage cost portion + refurb portion + ops cost — same structure as Sprint 2's formula but with ops now resolving to the new Assumptions row instead of 0)

copyToRange source D37, destination E37:AC37
```

Effect: Starship at-cost rate R40 increases by $5M/launch across all years. D40 (2025) goes from $30.42M → $35.42M; D40 (2030) goes from $19.09M → $24.09M; D40 (2050) goes from $2.74M → $7.74M.

### §4.3 Calibration impact

Sprint 2's 2025 calibration verifies Starship launches = 0 exact, so R37 ops cost change has zero impact on Sprint 2 verification. Sprint 3's Customer Launch external Starship revenue is 0 in 2025 → no Sprint 3 calibration impact. First sprint where Starship ops matters is Sprint 11 Valuation (Starship-related EV in 2030+).

---

## §5 — How Sprint 3 spec author absorbs this patch

Three integration points in the Sprint 3 spec:

### §5.1 Sprint 3 §1 Preamble — add a line

Sprint 3 Preamble adds one row to the Architecture compliance section:

> - [x] **Patch absorbed from Sprint 2 → 3** — F9 retirement (Patch A), F9 demand wiring (Patch B), Starship ops cost (Patch C) per `Sprint_2_to_3_Patch_F9_Retirement_and_Starship_Ops.md`. Three Assumptions amendments (F9 retirement rate, Starship ops cost) inlined in Sprint 3 §3 build sections.

### §5.2 Sprint 3 §3 scope — add two Assumptions amendments

Sprint 3 §3 normally builds the Customer Launch module body (per Sprint Roadmap §3 Sprint 3). Patch adds two Assumptions amendments at the top of §3:

1. **§3.1 Assumptions amendment — add `F9 retirement rate (% of launches/year)` row** (Patch A §2.2 above)
2. **§3.2 Assumptions amendment — add `Starship per-launch ops cost ($mm)` row** (Patch C §4.1 above)

Both written by Sprint 3 plugin chat in the same Sprint 3 execution. Append below existing Assumptions §3 rows per Rule 10.

### §5.3 Sprint 3 §3 scope — add three Launch Capacity formula amendments

Sprint 3 also amends three Launch Capacity rows (formula replacement only — no row insertions, preserving Sprint 2's row map):

1. **§3.3 Launch Capacity R62 amendment — replace flat retirement with launch-driven** (Patch A §2.3 above)
2. **§3.4 Launch Capacity R64 amendment — replace 2027+ stub with demand-driven wiring** (Patch B §3.2 above)
3. **§3.5 Launch Capacity R37 amendment — pull Starship ops from Assumptions** (Patch C §4.2 above)

Each is a single discrete write per Rule 1 (label unchanged, formula replaced; followed by copyToRange E→F:AC where applicable).

### §5.4 Sprint 3 §4 verification additions

Sprint 3 verification gate adds:

- **§4.1.X Re-verify Launch Capacity 2025 calibration** — D61 (= 17), D62 (= 6), D63 (= 39), D64 (= 171), D77 (= $778) — all unchanged from Sprint 2 because D-col values are still anchors. Confirms Patch A/B don't break Sprint 2 calibration.
- **§4.1.Y Verify F9 launches drop in out-years after Sprint 3** — read I64 (2030) F9 launches. With Sprint 3 only (Customer Launch live, Starlink V2 internal = 0), expect ~30-35 customer-only. Sanity: F9 customer launches 2030 from Customer Launch should land 25–40. If outside, halt and trace Customer Launch demand year-row.
- **§4.1.Z Stale-ref scan — Patch B canonical labels** — confirm `F9 customer launches per year` published on Customer Launch tab at Sprint 3 exit. Sprint 4 will add `F9 V2 BB launches (internal)` and `F9 V2 DTC launches (internal)`; for Sprint 3 verification, IFERROR-0 is the expected resolution.

### §5.5 Sprint 3 §7 Open Thread carries forward

Sprint 3 §7 inherits these from Sprint 2 §7:

- **Sprint 2 §7 item 1** — closed by Patch C.
- **Sprint 2 §7 item 2** — partially closed by Patch A (launch-driven retirement replaces flat 6/yr); full lifetime-reuses-by-booster engine still deferred. Likely never needed if launch-driven rate proves sufficient.
- **Sprint 2 §7 item 3** — still open (Sprint Roadmap §6.1 "~450K kg Starship capacity 2025" target — Vlad confirmed 2026-05-20: 0 in 2025 is correct because first commercial Starship launch is H2 2026 at earliest). Sprint 3 Claude Log entry should flag a future amendment to Sprint Roadmap §6.1 to reflect this.
- **Sprint 2 §7 item 4** — partially closed by Patch B (2026 anchor stays at 171, then F-col onwards is demand-driven). Confirms Vlad lock: customer launches stay F9-dominant through ~2030.
- **Sprint 2 §7 item 5** — closed by Patch B.

---

---

## §5 — Patch D — Sprint 2 execution fixes (Launch Capacity tab row extensions)

**Status added**: 2026-05-20 amendment after V2.4 review surfaced two real execution gaps from Sprint 2.

### §5.1 Bug summary

V2.4 inspection of Launch Capacity tab revealed two rows where the plugin completed the D-column write but missed the copyToRange to E:AC. Sprint 2's universal verification gate didn't catch them because it spot-checked specific cells (D33, D34, D77, D80) that all evaluated correctly. Downstream impact:

1. **R71 `F9 at-cost rate ($mm/launch)` populated D-only.** D71 = $17.75M ✓. E71:AC71 = empty. R76 reference `=F64*F71+F33*F40` resolves to F64 × empty + F33 × F40 = 0 (Starship launches = 0, F71 = empty treated as 0). Result: **R76 Total launch CapEx = 0 from 2026 onward → R77 Blended $/kg = 0 from 2026 onward.** 2025 D77 = $778 reads PASS but every other year reads zero. Sprint 11 Valuation would see launch cost / kg = 0 — material distortion.

2. **R24 `Booster fleet BoY`, R27 `Booster fleet EoY`, R28 `Cum upmass`** all populated D-only. E:AC = empty. With Sprint 2's R25 boosters built = 0 placeholder, all downstream Starship outputs (R31, R32, R33, R34) resolve to 0 anyway, masking the broken year-chains. But once Sprint 10's vehicle build claim writes R25 to non-zero, R24/R27/R28 must be live year-chains or the Starship fleet mechanic silently produces incorrect values.

Spec design contributing factor for Bug 1: Sprint 2 spec called R71 "D-only single-value" intentionally because the F9 cost stack is flat across years. But R76's relative reference `D71` then breaks the cross-year propagation. Either R71 needs to be flat across all columns (matching the intent), or R76 must use absolute `$D$71` reference.

### §5.2 Fix A — extend R71 to E:AC as flat value

Cleanest fix. Patches the spec's design intent (flat F9 cost) into a live year-row.

```
Plugin operation: copyToRange source D71, destination E71:AC71
   (Tiles D71's formula =D69+D70 across all year columns. Since D69, D70, D71 are all single-cell formulas
    referencing absolute D-column inputs, the copy produces identical $17.75M in every year — flat by design.)

Alternative: rewrite each year's R71 cell to =$D$69+$D$70 (absolute references).
   Equivalent outcome. Use whichever is cleaner for the plugin's tooling.
```

Post-fix verification: read E71, I71, S71, AC71 — all should equal $17.75M. Then re-recalc and read R77 in same columns — all should equal $778.51 (because R75 upmass and R76 CapEx now both flow correctly).

### §5.3 Fix B — extend R24, R27, R28 year-chains to E:AC

These rows ARE year-chained (Rule 23 exceptions per Sprint 2 spec §3.2.5 / §3.2.6). The plugin wrote D-col anchors but missed propagating E-col formulas across F:AC.

```
Plugin operation 1 (R24): write E24 = =D27; copyToRange source E24, destination F24:AC24
Plugin operation 2 (R27): copyToRange source D27, destination E27:AC27
   (D27 formula =D24+D25-D26 propagates correctly as a relative-reference pattern;
    E27 becomes =E24+E25-E26, F27 becomes =F24+F25-F26, etc.)
Plugin operation 3 (R28): write E28 = =D28+D33*D29; copyToRange source E28, destination F28:AC28
```

For R29 (per-launch upmass — also a year-row), check if it propagated to E:AC. V2.4 inspection shows R29 IS populated across years (D=150000, I=115000, AC=102500), so R29 likely propagated correctly. If not, copyToRange D29 → E29:AC29.

Post-fix verification: read E24, I24, S24, AC24 — all 0 (boosters built R25 = 0 placeholder, so fleet stays 0). Same pattern for R27, R28. These cells now hold LIVE FORMULAS, not None values. When Sprint 10 writes R25, the year-chains will propagate cum stacks → fleet → launches → capacity correctly.

### §5.4 Where Patch D fires in Sprint 3 execution sequence

Sprint 3's plugin chat applies Patch D as the FIRST operation, before any Sprint 3 module-body work. This catches the bugs while focus is still on Launch Capacity and avoids them festering through Sprints 3–10. Three discrete writes (Fix A) + three discrete writes (Fix B) = six tool calls. Total estimated <5 minutes of plugin time.

After Patch D: verification gate confirms R71 flat at $17.75M across years; R77 flat at $778.51M across pre-2035 years (decaying to 0 only when F9 launches naturally decay to 0 from the R64 stub formula, which Patch B will then replace with demand-driven launches). Conservation block (Sprint 1 deliverable) remains "OK" since Patch D doesn't touch P&L tabs.

---

## §6 — Patch E — Starship cost mechanic (Q4'25 mirror + Mach33 anchor)

**Status added**: 2026-05-20 amendment after Vlad reviewed Sprint 2's Starship cost stack and provided the Mach33 "10,000 Starships" analysis. Sprint 2's mechanic (variant-mix-weighted ship + booster expendable/reusable split using V30.5 reusability matrix numbers) is replaced with a Wright's-Law-on-cum-stacks formula mirroring Q4'25 Earth!R159–R164, anchored to Mach33's $100M-today figure.

### §6.1 What changes and why

**Vlad's locks (2026-05-20):**

1. **Starship is 100% reusable from 2027 onwards.** Whether they fly expendable on any given mission is a separate mission-level decision (handled in Sprint 4/5 at the consuming-module level if needed). The default capability is fully reusable. R46 variant-mix year-row stops being a slow ramp (0% → 95% by 2035) and becomes a step function: 0% in 2025, 100% from 2026 onwards.

2. **Cost decline is driven by mass manufacturing (Wright's Law on cumulative stacks built), not turnaround/reuse.** Mach33's analysis (`10000 starships.pdf`, Jan 7 2026) makes the explicit case: $/kg gains are captured by ~10-20 flights per vehicle, beyond which costs asymptote — manufacturing scale and throughput dominate, reuse is a secondary lever. The Sprint 2 mechanic over-rotated on reuse via variant-mix weighting; the fix is to put Wright's Law on the front.

3. **Anchor: $100M full stack cost today (2025-2026), declining per Wright's Law as more are built.** $100M is Mach33's "today" figure ($90M mfg + $10M ops/fuel + $2M refurb). This becomes the load-bearing input to the cost stack; the V30.5 R32 = $35.1M SH + R33 = $23.4M ship breakdown (= $58.5M total) is corrected upward to match Mach33.

### §6.2 Q4'25 mechanic to mirror

Q4'25 `Earth` tab cost formulas:

```
R159: Starship Platform | B = 0.85  | "Wright's Manufacturing Learning Rate"   (= progress ratio)
R160: Total Initial Cost | B = =LOG(B159)/LOG(2) = -0.234   | "Wright's Law Exponent"
       | J (2025) = $I$160*0.2 + $I$160*0.8*(I24/4)^$B$160
       | (J = $anchor × (0.20 + 0.80 × (cum_stacks_through_this_year / 4)^WL_exp))
R161: Of Which Is Variable   | = turnaround-time-based formula   (complex; simplified to a flat % share in Patch E)
R163: Variable Cost Per Launch (COGS) | = R161 × R160
R164: Fixed Asset Value (CapEx) | = R160 × R162   (= R160 × (1 - R161))
```

Mechanic:
- 20% of the stack cost is a **non-learning floor** (captures ops + fuel + refurb that don't scale with manufacturing volume — Mach33 confirms these have physical floors).
- 80% of the stack cost scales with Wright's Law on **cumulative stacks built** (= manufacturing learning).
- Anchor cum-units = 4 (Q4'25 default — represents the integrated-flight-test campaign through 2024-end).
- Anchor cost (base year) = $100M (Mach33 today, vs Q4'25's $I$160 which is set to a similar order).

### §6.3 Calibration check against Mach33 anchors

Using the formula above:
- **Cum=4 (anchor, ~2024-2025 baseline)**: cost = $100M × (0.20 + 0.80 × 1.0^-0.234) = $100M × 1.0 = **$100M** ✓ matches Mach33 "today"
- **Cum=2048 (~1k/yr regime, ~2030-2032)**: 9 doublings from 4. cost = $100M × (0.20 + 0.80 × 0.232) = $100M × 0.386 = **$38.6M** vs Mach33 "$26M mfg + $5M ops + $0.5M refurb = $31.5M" → 22% high, defensible given 20% floor lumps ops/fuel/refurb conservatively
- **Cum=50000 (~10k/yr regime, ~2040)**: 13.6 doublings. cost = $100M × (0.20 + 0.80 × 0.106) = $100M × 0.285 = **$28.5M** vs Mach33 "$12.2M mfg + $3M ops + $0.25M refurb = $15.45M" → 84% high; the 20% floor over-captures terminal costs

The 20%-floor approximation runs heavier than Mach33 at full industrial scale. Sprint 11 Valuation can revisit if terminal Starship cost is load-bearing for EV (it likely is). For Sprint 3, mirror Q4'25 exactly and lock the 20% floor as an MC-variable input (range 10%-25% per §6.6 below) so the terminal cost has a tunable knob.

### §6.4 Assumptions §3 amendments

Sprint 3 plugin amends Assumptions §3 Capacity. Updates to existing rows + 4 new rows appended below R64.

**Updates to existing rows:**

| Row | Old value | New value | Rationale |
|---|---|---|---|
| R32 `Super Heavy manufacturing cost ($mm/unit, base year)` | 35.1 | **54** | Mach33: booster 60% × $90M total mfg = $54M today |
| R33 `Starship 2nd-stage manufacturing cost ($mm/unit, base)` | 23.4 | **36** | Mach33: ship 40% × $90M total mfg = $36M today |
| R34 `Ship refurb % of manufacturing` | 0.02 | unchanged (= 0.02) but DEPRECATED | Refurb cost now absorbed into the 20% non-learning floor of stack cost. R34 kept as memo for narrative breakdown, no longer in the cost formula path. |
| R46 `Variant mix (% fully reusable)` year-row | D=0, E=0.05, F=0.15, G=0.25, H=0.45, I=0.7, M=0.92, N=0.95, S=0.95, AC=0.95 | **D=0, E:AC = 1.0** (step function: zero in 2025, 100% in 2026 onwards) | Vlad lock 2026-05-20: Starship 100% reusable from 2026 (first commercial H2 2026). Whether expendable launches happen is a mission-level decision in Sprint 4/5. |

**New Assumptions rows (append below R64 per Rule 10):**

| Row (TBD by spec author) | Label | Base Case | MC Min | MC Max | MC Distribution | Notes |
|---|---|---|---|---|---|---|
| (new) | `Starship full-stack cost anchor ($mm, 2024 baseline)` | **100** | 80 | 130 | triangle | Mach33 "today" anchor = $90M mfg + $10M ops/fuel + $2M refurb = ~$100M. MC range covers SpaceX disclosed vs internal estimates. |
| (new) | `Starship cost WL learning rate (% reduction per doubling cum stacks)` | **0.15** | 0.10 | 0.25 | triangle | Q4'25 R159 progress ratio 0.85 (= 15% per doubling). NASA cost handbook aerospace learning rule. Mach33 uses same. MC bracket: 10% (conservative) → 25% (aggressive, post-Gigabay industrial scale). |
| (new) | `Starship cost WL anchor cum units (= cum stacks at baseline)` | **4** | 2 | 8 | triangle | Mirrors Q4'25 R160 denominator = 4. Represents successful integrated flight test campaign through end-2024. |
| (new) | `Starship variable cost share (% of stack)` | **0.20** | 0.10 | 0.25 | triangle | Q4'25 R160 floor coefficient = 0.20. Mach33 implies lower terminal floor (~8-10% at 10k/yr scale via separate ops/fuel/refurb floors); MC range captures the spread. |

### §6.5 Launch Capacity tab amendments — fits in Sprint 2's locked row map

Patch E preserves the Sprint 2 row map (no row insertions per Rule 10) by repurposing R30 (currently blank spacing) and reformulating R37–R40.

**NEW row at R30 (currently blank in V2.4):**

```
A30 = "Cum Starship stacks manufactured (end-of-year, units)"

D30 = =INDEX(Assumptions!$B:$B, MATCH("Starship cost WL anchor cum units (= cum stacks at baseline)", Assumptions!$A:$A, 0))
   (Anchor: end-2024 cum stacks = 4, locked at the Assumptions anchor value. Sprint 2's R25 boosters built = 0 in 2025
    so cum stays at the anchor; once Sprint 10 lights up R25, cum-stacks ramps.)

E30 = =D30 + D25
   (Year-chained running sum — Rule 23 exception: cum_stacks at EoY = prior cum + this year's boosters built.
    A booster + ship = one stack. Sprint 2 spec uses R25 for "boosters built per year" which equals stacks built per year
    for cost-amortization purposes (assumes one ship per booster built, which matches Q4'25 R20+R21+R22+R41 architecture).
    Sprint 4/5/7 may amend R25 to include ship-only builds; for Sprint 3 patch, R25 captures total vehicles built.)

copyToRange source E30, destination F30:AC30
```

Format: D30:AC30 integer `#,##0`.

**REPURPOSED rows R37–R40** (Sprint 2 spec §3.2.9 formulas REPLACED):

```
A37 = "Starship full-stack cost ($mm/unit, this year)"   (Sprint 2 label changed from "Starship variable cost per launch ($mm)")

D37 = =INDEX(Assumptions!$B:$B, MATCH("Starship full-stack cost anchor ($mm, 2024 baseline)", Assumptions!$A:$A, 0))
      * (
          INDEX(Assumptions!$B:$B, MATCH("Starship variable cost share (% of stack)", Assumptions!$A:$A, 0))
        + (1 - INDEX(Assumptions!$B:$B, MATCH("Starship variable cost share (% of stack)", Assumptions!$A:$A, 0)))
          * (D30 / INDEX(Assumptions!$B:$B, MATCH("Starship cost WL anchor cum units (= cum stacks at baseline)", Assumptions!$A:$A, 0)))
            ^ (LOG(1 - INDEX(Assumptions!$B:$B, MATCH("Starship cost WL learning rate (% reduction per doubling cum stacks)", Assumptions!$A:$A, 0)), 2))
        )
   (Reads: anchor × (var_share + (1-var_share) × (cum_stacks/anchor_units)^WL_exp))
   (WL_exp = LOG(1 - learning_rate, 2) = LOG(0.85, 2) ≈ -0.234 when learning_rate = 0.15)
   (For Sprint 3 with Sprint 2's R25 = 0 → D30 = 4 throughout → ratio = 1.0 → cost = anchor × (0.20 + 0.80 × 1) = $100M flat))

copyToRange source D37, destination E37:AC37
   (Once Sprint 10 lights up R25, D30 starts growing → cost declines per WL across years.)

---

A38 = "Starship variable cost per launch ($mm)"   (Sprint 2 label changed from "Starship booster D&A share per launch ($mm)")

D38 = =D37 * INDEX(Assumptions!$B:$B, MATCH("Starship variable cost share (% of stack)", Assumptions!$A:$A, 0))
   (Variable portion of stack cost — paid per launch regardless of reusability.
    Captures ops + fuel + refurb in the simplified Q4'25 lumped framing.)

copyToRange source D38, destination E38:AC38

---

A39 = "Starship D&A share per launch ($mm)"   (Sprint 2 label changed from "Starship ship D&A share per launch ($mm)")

D39 = =IFERROR(D37 * (1 - INDEX(Assumptions!$B:$B, MATCH("Starship variable cost share (% of stack)", Assumptions!$A:$A, 0))) / D21, 0)
   (Fixed-asset portion (80% of stack) amortized over lifetime reuses per booster (year-row R21).
    IFERROR wraps in case D21 = 0 in early years; defaults to 0 to avoid #DIV/0 cascade.
    At cum=4 anchor with $100M stack: D39 = $100M × 0.80 / D21 = $80M / lifetime_reuses_year_row.
    In 2025 with R21 = 5: D39 = $16M. In 2030 with R21 = 30: D39 = $2.67M. In 2050 with R21 = 100: D39 = $0.8M.)

copyToRange source D39, destination E39:AC39

---

A40 unchanged = "Starship at-cost rate ($mm/launch)"

D40 = =D38 + D39   (Sprint 2 formula =D37+D38+D39 changes to =D38+D39 because R37 now holds the FULL STACK cost, not the variable portion. R38 + R39 together capture the variable + amortized D&A per launch.)

copyToRange source D40, destination E40:AC40
```

### §6.6 Expected output trajectory

With Sprint 3 patch applied + Sprint 2's R25 = 0 placeholder unchanged (Sprint 10 still owns vehicle build):

| Year | R30 cum stacks | R37 stack cost ($M) | R38 variable ($M) | R39 D&A share ($M) | R40 at-cost ($M/launch) |
|---|---|---|---|---|---|
| 2025 | 4 | $100.0 | $20.0 | $16.0 (÷5 reuses) | $36.0 |
| 2026 | 4 | $100.0 | $20.0 | $12.5 (÷8 reuses) | $32.5 |
| 2027 | 4 | $100.0 | $20.0 | $6.7 (÷12 reuses) | $26.7 |
| 2030 | 4 | $100.0 | $20.0 | $2.67 (÷30 reuses) | $22.67 |
| 2050 | 4 | $100.0 | $20.0 | $0.80 (÷100 reuses) | $20.80 |

After Sprint 10 lights up R25 (vehicle build claim sized by forward-aggregate kg demand), R30 cum-stacks ramps and the table shifts: at cum=100 (~2030), stack cost ≈ $100M × (0.2 + 0.8 × 25^-0.234) = $100M × (0.2 + 0.8 × 0.461) = $56.9M. At cum=2048 (~1k/yr regime, ~2032+), stack ≈ $38.6M per §6.3. Terminal cost asymptotes toward $20M (= 20% floor × $100M anchor) regardless of cum-stacks growth.

### §6.7 What gets dropped from Sprint 2's mechanic

The Sprint 2 variant-mix-weighted formula (booster-only mode expendable ship + fully-reusable refurb) is fully replaced. Specifically:

- R37 old formula `=D9*(1-D20) + D9*D10*D20 + 0` → DROPPED (was computing variant-weighted variable cost; superseded)
- R38 old formula `=D8/D21` → DROPPED (was computing booster-only D&A share; superseded — D&A is now stack-level not booster-level)
- R39 old formula `=D9/$D$13*D20` → DROPPED (was computing ship D&A share variant-weighted; superseded — Mach33 says no separate ship vs booster D&A under fully-reusable default)
- R20 variant mix year-row is still pulled into Launch Capacity for memo purposes (it's referenced by R29 per-launch upmass, which still uses R20 to blend R11 booster-only payload + R12 fully-reusable payload). Sprint 4/5 missions running expendable can override R20 locally if needed.

### §6.8 Calibration impact + Sprint 11 Valuation note

**Sprint 3 verification:** D40 (Starship at-cost rate 2025) changes from Sprint 2's $30.42M to **$36.0M** under Patch E. Sprint 2's §6.1 calibration target was "Starship launches 2025 = 0 exact" — D40 doesn't enter any 2025 calibration check (Starship launches = 0 means the cost doesn't multiply through to any 2025 output). Sprint 3 verification confirms D40 ≈ $36M and notes the increase as intentional (matches Mach33's "today" anchor).

**Sprint 11 Valuation:** Patch E's terminal Starship at-cost ≈ $20M/launch (floor) drives blended $/kg at scale. At 150K kg payload (booster-only mode — but R46 = 100% reusable means we use R12 = 100K kg fully-reusable payload by default): $20M / 100K = $200/kg terminal. Vs Mach33's "$10/kg at 10k/yr fully industrial regime." The 20× delta is real and reflects Q4'25's lumped 20% floor vs Mach33's separate floors. If Vlad's investment thesis needs $10-35/kg terminal, MC the var_share input down to 5-10% (lower floor) or revisit the cost mechanic in a Sprint 11 patch with separate ops/fuel/refurb floors per Mach33's split.

### §6.9 Where Patch E fires in Sprint 3 execution sequence

Sprint 3 plugin chat executes Patch D first (execution fixes — §5), then absorbs Patches A, B, C into the Customer Launch module body (per §5.1–§5.5 above), then applies Patch E LAST (Starship cost overhaul) so that:
1. Customer Launch external Starship pricing (Sprint 3 §6.2 calibration target) inherits the corrected stack cost.
2. Sprint 4 Starlink internal Starship V3 launches inherit the corrected at-cost rate.
3. Sprint 5 ODC internal Starship launches inherit the corrected at-cost rate.

### §6.10 Open questions to confirm with Vlad before Sprint 3 plugin fires

These are flagged in case Vlad wants to override the patch's default values:

1. **Anchor cum units = 4** — Q4'25 default. Represents successful Starship integrated flight tests through end-2024. Could be 2-8 depending on which IFTs count. Confirm or adjust.
2. **Var cost share = 20%** — Q4'25 default. Mach33 separated floors imply 8-10% at terminal scale. Use 20% for Sprint 3 with MC range [10%, 25%] (locked), or push lower to match Mach33 more closely.
3. **R32 + R33 update to Mach33 split** — $54M booster + $36M ship = $90M mfg (Mach33). These become memo only post-Patch E; R37 stack cost reads the $100M anchor directly. Update R32/R33 for consistency? Or leave V30.5 values ($35.1 + $23.4 = $58.5M) and add an Open Thread note about the breakdown discrepancy?
4. **R34 ship refurb 2%** — deprecated in Patch E. Drop from Assumptions or keep as memo with deprecated flag?

Sprint 3 spec author can lock any of these before Sprint 3 plugin fires. Default values above are what the patch installs absent any override.

---

## §7 — Amendment log

- **2026-05-20 (initial draft)** — Patch doc drafted after Vlad reviewed Sprint 2 spec. Three integration points (Patch A = F9 retirement, Patch B = F9 demand wiring, Patch C = Starship ops cost). Anchored to Q4'25 CLEANUP `Earth` tab Row 30 ($B$30 = 0.01 retirement rate per launch), Row 68 (F9 launches = SUM of Starlink + Customer + manufactured), Row 56 (Starship Customer = MIN(market demand, unused capacity post-Starlink-and-Compute)). Sprint 3 spec author folds all three into Sprint 3 scope at spec-drafting time. Sprint 2 itself unchanged — Sprint 2 ships with the flat-retirement + decay-stub mechanics, then Sprint 3 supersedes both within the same workbook V2.3 → V2.4 pass.

- **2026-05-20 (amendment 1)** — Added Patch D (Sprint 2 execution fixes: extend R71 to E:AC flat, extend R24/R27/R28 year-chains to E:AC) after V2.4 inspection surfaced two real execution gaps that would have distorted Sprint 11 Valuation. Patch D fires FIRST in Sprint 3 execution sequence.

- **2026-05-20 (amendment 2)** — Added Patch E (Starship cost mechanic overhaul) per Vlad's three locks: (a) Starship 100% reusable from 2026 (variant mix R46 → step function), (b) cost decline driven by Wright's Law on cum stacks manufactured (mirroring Q4'25 Earth!R160), (c) $100M full-stack anchor (Mach33 "today" figure from `10000 starships.pdf` Jan 7 2026). Replaces Sprint 2's variant-mix-weighted ship + booster expendable/reusable mechanic with Q4'25's lumped-stack-cost structure. New Assumptions rows: stack cost anchor ($100M), WL learning rate (0.15), WL anchor cum units (4), variable cost share (0.20). Updates R32/R33 to Mach33 split. Patch E fires LAST in Sprint 3 execution sequence (after Patches D, A, B, C) so all downstream Starship cost reads inherit the corrected mechanic.

- **2026-05-20 (amendment 3)** — Added §6.11 Booster-only-mode amendment to Patch E per Vlad's 2026-05-20 clarification: Mars/Moon missions are inherently ship-expended (booster recovers, ship stays at destination until in-situ propellant + booster manufacturing matures). Boosters fly more than ships (Mach33's k multiplier: k=1 today, k=3 at 1k/yr regime, k=5 at 10k/yr). Patch E now exposes TWO at-cost rates: R40 (fully reusable, canonical, used by Sprint 3/4/5/10 for LEO) and R41 (ship-expended booster-only mode, used by Sprint 7 Lunar Mars). New Assumptions row: `Starship booster share of manufacturing cost` = 0.60 (Mach33 ship 40% / booster 60% split). R39 reformulated to use booster + ship D&A split (fully reusable). R41 new memo row computes the ship-expended variant for Moon/Mars consumption.

- **2026-05-20 (amendment 4)** — Added §6.12 Payload-capacity growth + reusable year correction per Vlad's pointer to Q4'25 `Valuation Inputs & Logic` table. Three substantive changes: (a) Variant mix R46 step year corrected from 2026 → **2027** to match Q4'25 R17 + R23 + Mach33 + Vlad's "100% reusable in 2027" lock; (b) Starship payload becomes a **year-row** computed via bounded-CAGR (2025 baseline 100K → 2030 anchor 200K → 250K cap, mirroring Q4'25 Earth!R76 + R74), replacing Sprint 2's flat R29 per-launch upmass; (c) Four new Assumptions rows for payload dynamics (2025 baseline, 2030 anchor, max cap, booster-only mode delta). NEW Launch Capacity row R35 (was blank) = `Starship payload — fully reusable mode year-row (kg)` — helper for R29. §6.12.7 surfaces 6 additional Q4'25 dynamics for downstream sprint authors (Starlink-vs-customer split 80% in 2030, bandwidth TAM factor, ODC W/kg + TOPS/W roadmap, IPO size $30-50B, compute allocation share 85%).

- **2026-05-20 (amendment 5 — CANONICAL)** — Added §6.13 Split-cost-curve canonical formulation per Vlad pushback on the "20% floor never declines" framing: "Frankly, the fraction that isn't the manufacturing should also go down over time because of learnings... but maybe at a different rate." Replaces the single-curve lumped-floor approach (§6.4–§6.5) with **two separate Wright's Law curves**: manufacturing ($90M anchor, 15% learning, amortized over reuses) + ops+fuel+refurb ($12M anchor, 10% learning, per-launch). Both decline with scale. Reverse-engineered learning rates from Mach33's three-regime anchors. Drops `Starship variable cost share` and `Starship full-stack cost anchor` inputs (lumped approach obsolete). Adds 6 split-cost inputs + 4 payload inputs (carried from §6.12). DELETES R34 ship refurb % from Assumptions (folded into ops+fuel+refurb curve per Vlad lock). Patch C (Starship ops cost) marked SUPERSEDED. Marks §6.4–§6.10 + §6.11 formulas as historical; **§6.13 is the source of truth Sprint 3 plugin executes against**. MC ranges populated for every uncertain input per Vlad's "things were not sure about should be monte carlo ranges" lock.

---

## §6.11 — Booster-only-mode amendment (Moon/Mars convention)

Added 2026-05-20 after Vlad clarified the Mars/Moon launch profile.

### §6.11.1 What this changes vs §6.5 above

Vlad's clarification: Starship's "100% reusable from 2027" capability is true for LEO operations. Mars/Moon missions, however, are structurally booster-only — the ship lands at the destination and stays there for years (until in-situ propellant production + booster manufacturing become viable). The booster returns to Earth in all cases (it never leaves Earth's neighborhood). So:

- **LEO ops (Starlink V3, ODC compute sats, customer LEO launches)**: fully reusable — both booster AND ship return. Default mode. Payload R12 = 100K kg (ship-landing-mass overhead).
- **Moon/Mars ops (Sprint 7 Lunar Mars)**: ship-expended booster-only — booster recovered, ship stays at destination. Payload R11 = 150K kg (no ship-return mass overhead). Ship is a one-way asset (expensed in full as CapEx the year it ships).

Per the Mach33 analysis: booster reuse multiplier k (= booster flights / ship flights over the booster's life) = 1 today, 3 at 1k/yr regime, 5 at 10k/yr. The Sprint 0 R21 booster lifetime year-row (5 → 100) and R13 ship lifetime cap (30) implicitly carry this multiplier — booster lifetime grows past ship lifetime in out-years (Sprint 0 R21 hits 30 at 2030 = parity with R13; ramps to 100 at 2050 = ~3.3× ship lifetime, close to Mach33's k=3 at 1k/yr). Patch E uses these existing year-rows; no separate k input needed.

### §6.11.2 New Assumptions row (one additional, appended after §6.4 list)

| Row (TBD) | Label | Base Case | MC Min | MC Max | MC Dist | Notes |
|---|---|---|---|---|---|---|
| (new) | `Starship booster share of manufacturing cost (% of stack mfg)` | **0.60** | 0.50 | 0.70 | triangle | Mach33 ship 40% / booster 60% split of manufacturing cost. Booster (Super Heavy) is heavier + more engines (33 Raptors vs ship's 6). Vlad-confirmed split. |

(Note: R32 SH mfg cost = $54M and R33 ship mfg cost = $36M in §6.4 amendments are also breakdown memos consistent with this 60/40 split; they're load-bearing for the patch's calibration story but not directly referenced in the Launch Capacity formulas — those reference the $100M stack anchor + this booster-share input.)

### §6.11.3 Launch Capacity tab row map — REVISED §6.5

The §6.5 row repurposing changes. R37 and R38 unchanged. R39 reformulated to split booster + ship D&A. R40 stays the canonical at-cost label (LEO, fully reusable). R41 (formerly blank in Sprint 2's row map between R40 and R42 = F9 section header) becomes the booster-only-mode memo row.

**REPURPOSED rows R37–R40 (revised from §6.5):**

```
A37 = "Starship full-stack cost ($mm/unit, this year)"   [unchanged from §6.5]

D37 = (same Wright's Law formula as §6.5 — reads anchor × (var_share + (1-var_share) × (D30/anchor_units)^WL_exp))

copyToRange source D37, destination E37:AC37

---

A38 = "Starship variable cost per launch ($mm)"   [unchanged from §6.5]

D38 = =D37 * INDEX(Assumptions!$B:$B, MATCH("Starship variable cost share (% of stack)", Assumptions!$A:$A, 0))
   (Variable share — ops/fuel/refurb — paid each launch regardless of mode.)

copyToRange source D38, destination E38:AC38

---

A39 = "Starship total D&A share per launch, fully reusable mode ($mm)"
   [Revised label — was "Starship D&A share per launch ($mm)" in §6.5; now scoped to "fully reusable mode" since R41 will carry the booster-only variant.]

D39 = =IFERROR(
        D37 * (1 - INDEX(Assumptions!$B:$B, MATCH("Starship variable cost share (% of stack)", Assumptions!$A:$A, 0)))
        * (
            INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0)) / D21
          + (1 - INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0))) / $D$13
          )
        , 0)
   (Reads: mfg_portion × (booster_share / booster_lifetime_year_row + ship_share / ship_lifetime_cap))
   (At anchor cum=4 with $100M stack and 2025 R21=5, $D$13=30:
    D39 = $100M × 0.80 × (0.60/5 + 0.40/30) = $80M × (0.12 + 0.0133) = $80M × 0.1333 = $10.67M.
    Booster D&A dominates ($9.6M of $10.67M) because booster has shorter lifetime in 2025; ship D&A is small ($1.07M).
    At 2030 with R21=30 (= R13): D39 = $80M × (0.60/30 + 0.40/30) = $80M × 0.0333 = $2.67M (booster + ship D&A converge as lifetimes equalize).
    At 2050 with R21=100, R13=30: D39 = $80M × (0.60/100 + 0.40/30) = $80M × (0.006 + 0.0133) = $1.55M (ship D&A dominates because booster lifetime grew faster).)

copyToRange source D39, destination E39:AC39

---

A40 = "Starship at-cost rate ($mm/launch)"   [Sprint 2's canonical label — UNCHANGED. Sprint 3/4/5/10 read this row by label for LEO ops.]

D40 = =D38 + D39
   (Fully reusable mode — variable + booster D&A + ship D&A. Both amortized over respective lifetimes.
    At anchor cum=4 in 2025: D40 = $20M + $10.67M = $30.67M (very close to Sprint 2's pre-patch $30.42M — calibration preserved).
    In 2030 with WL applied (assuming Sprint 10 lights up R25 and cum=100 by 2030): D40 = stack × var_share + stack × (1-var_share) × (lifetime-weighted D&A factor) — ramps down per WL.
    In 2050 at full industrial scale: D40 floors near (stack_floor × var_share) + lifetime-amortized terminal ≈ $25M × 0.20 + small = ~$5-8M/launch at terminal.)

copyToRange source D40, destination E40:AC40
```

**NEW row R41 (was blank in Sprint 2 row map; Patch E populates):**

```
A41 = "Memo: Starship at-cost rate, ship-expended mode (Moon/Mars, $mm/launch)"

D41 = =IFERROR(
        D38
      + D37 * (1 - INDEX(Assumptions!$B:$B, MATCH("Starship variable cost share (% of stack)", Assumptions!$A:$A, 0)))
            * INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0)) / D21
      + D37 * (1 - INDEX(Assumptions!$B:$B, MATCH("Starship variable cost share (% of stack)", Assumptions!$A:$A, 0)))
            * (1 - INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0)))
        , 0)
   (Three terms:
     1. Variable per launch (D38) — same as fully reusable mode
     2. Booster D&A per launch — mfg × booster_share / booster_lifetime (booster is recovered + reused even on Moon/Mars missions)
     3. Ship FULL COST per launch — mfg × ship_share, NOT amortized (ship stays at destination, expensed full)
    At anchor cum=4 in 2025: D41 = $20M + $9.6M (booster D&A) + $32M (ship expensed) = $61.6M/launch — much higher than fully reusable mode's $30.67M because ship is full-cost.
    At 2050 with WL applied + booster lifetime 100: D41 = $5M var + $48M_anchor × WL × 0.60/100 (small booster D&A) + $48M_anchor × WL × 0.40 (ship full cost) — terminal Moon/Mars launch dominated by ship-expensed cost, which falls per WL but stays meaningful.)

copyToRange source D41, destination E41:AC41
```

Format: D41:AC41 currency `$#,##0.00`.

### §6.11.4 Canonical labels added by Patch E

Updates the §3.4 / §5.2 of Patch B's canonical-labels list. After Patch E + §6.11 lands, Sprint 7 (Lunar Mars) reads its launch cost by label:

| Label | Row | Consumed by |
|---|---|---|
| `Starship at-cost rate ($mm/launch)` | R40 | Sprint 3 + Sprint 4 + Sprint 5 + Sprint 10 (LEO ops, fully reusable mode — canonical) |
| `Memo: Starship at-cost rate, ship-expended mode (Moon/Mars, $mm/launch)` | R41 | **Sprint 7 Lunar Mars** (ship-expended booster-only mode — Moon/Mars surface missions) |

Sprint 7 spec author confirms Lunar Mars module's per-mission cost formula reads R41 (not R40). Lunar Mars per-mission CapEx = R41 × (mission_count × (1 + depot_multiplier)) — captures the depot/refuel-ship launches at the same ship-expended rate (since depot ships also stay at destination in fuel-cycle-limited regime).

### §6.11.5 Expected D40 vs D41 trajectory

| Year | R30 cum stacks | R37 stack | R38 var | R39 D&A (LEO) | R40 LEO at-cost | R41 Moon/Mars at-cost |
|---|---|---|---|---|---|---|
| 2025 | 4 | $100.0M | $20.0M | $10.67M (5 yr booster, 30 yr ship) | **$30.67M** | $20 + $9.6 + $32 = **$61.6M** |
| 2026 | 4 | $100.0M | $20.0M | $7.07M (8 yr booster, 30 yr ship) | **$27.07M** | $20 + $6.0 + $32 = **$58.0M** |
| 2030 | 4 (Sprint 2 placeholder) or ramping post-Sprint-10 | $100.0M (anchor until R25 grows) | $20.0M | $2.67M (30 yr booster + ship) | **$22.67M** | $20 + $1.6 + $32 = **$53.6M** |
| 2050 | ramping toward 50K+ if Sprint 10 + Mars carve-out active | terminal stack ~$30M floor | $6.0M | $0.39M (100 yr booster, 30 yr ship) | **$6.4M** | $6 + $0.18 + $12 = **$18.2M** |

(2030 and 2050 figures assume Sprint 10 lights up R25 cum-stacks; Sprint 2 + Sprint 3 baseline keeps R30 = 4 throughout → stack cost flat at $100M anchor → D40 and D41 mostly driven by R21 booster lifetime year-row scaling D&A down.)

The Moon/Mars cost gap (R41 − R40) is the per-launch ship-expended premium: $32M anchor in 2025 → $12M at terminal (WL × $80M × 0.40). This is the "cost of expending a ship" each mission and it correctly captures Vlad's framing — Moon/Mars missions pay full ship cost because there's no return.

### §6.11.6 Calibration impact

D40 (2025 LEO at-cost) = **$30.67M** — within 1% of Sprint 2's pre-patch $30.42M. The fully reusable LEO at-cost rate is essentially unchanged in 2025 — Patch E's $100M anchor + 20% floor + 60/40 split happens to land at the same 2025 cost as Sprint 2's variant-mix-zero-fully-expendable formula. **Sprint 2 calibration preserved by accident, but the cost trajectory in out-years is genuinely Wright's-Law-driven now.**

D41 (2025 Moon/Mars at-cost) = **$61.6M** — new memo cell, not previously computed. Sprint 7 Lunar Mars will reference this from 2027+ when first Mars/Moon missions are flown. No Sprint 2 calibration impact.

### §6.11.7 What stays out of scope for Patch E

These deferrable items are noted in case future sprints need them:

1. **Booster-over-ship reuse multiplier k as explicit input.** Mach33 says k=1/3/5 across regimes. Patch E implicitly carries this via Sprint 0's R21 booster lifetime year-row (5 → 100) vs R13 ship cap (30 flat). If Vlad's thesis evolves to make k an explicit input, a future amendment can split R21 and R13 differently — Patch E doesn't preclude.

2. **Separate ops + fuel + refurb floors per Mach33.** Q4'25's lumped 20% floor approximates Mach33's three separate floors ($3M ops + $0.25M refurb at 10k/yr). If Sprint 11 Valuation needs the Mach33 $10/kg terminal regime, swap the lumped floor for three separate Wright's-Law-floored line items. Patch E uses lumped for simplicity.

3. **Expendable-mode LEO launches.** If a future LEO mission (heavy customer payload) chooses ship-expended mode for the extra ~50K kg payload, Sprint 4/5/3 spec author can read R41 instead of R40 for that mission's at-cost rate. Patch E exposes both, doesn't gate which gets used.

4. **Booster + ship mass-manufacturing learning at different rates.** Mach33 implies booster manufacturing might learn faster than ship (higher production volume). Patch E uses a single learning rate (15%) on the combined stack. Decomposing would require splitting R37 into separate booster + ship cost rows with independent WL formulas. Defer until Sprint 11 unless terminal cost is materially miscalibrated.

---

## §6.13 — Split-cost-curve canonical formulation (CANONICAL Patch E — supersedes §6.4 lumped-floor approach)

Added 2026-05-20 after Vlad pushback: "Frankly, the fraction that isn't the manufacturing should also go down over time because of learnings... but maybe at a different rate. Look at the 10000 analysis and add monte carlo ranges to the assumptions."

§6.4–§6.10 originally described a lumped-stack-cost formula with a 20% non-declining floor (Q4'25 R160 mirror). That over-captured the floor — Mach33's analysis shows ops+fuel+refurb DECLINE with scale, just slower than manufacturing. The canonical Patch E formulation is the **two-curve split** below, with each curve having its own Wright's Law learning rate. §6.4–§6.10 are kept as the historical evolution but **§6.13 is the source of truth Sprint 3 plugin executes against.**

### §6.13.1 Architecture

Stack cost has two components, each with its own Wright's Law curve on cumulative stacks manufactured:

```
Manufacturing portion (per stack, amortized over reuses) =
    mfg_anchor × (cum_stacks / anchor_cum_units)^(LOG(1 - mfg_learning_rate, 2))

Ops + fuel + refurb portion (per launch, paid each flight) =
    ops_anchor × (cum_stacks / anchor_cum_units)^(LOG(1 - ops_learning_rate, 2))
```

Both decline with scale. Manufacturing learns faster (~15%/doubling, Mach33 + Q4'25 + NASA aerospace standard). Ops+fuel+refurb learn slower (~10%/doubling, back-derived from Mach33's three anchors: $12M today → $5.5M at 1k/yr regime → $3.25M at 10k/yr regime).

### §6.13.2 Mach33 anchor reconciliation

Reverse-engineered per-doubling learning rates from Mach33's three regime anchors (cum ≈ 4 today → cum ≈ 2,000 at 1k/yr → cum ≈ 50,000 at 10k/yr):

| Component | Today (cum=4) | 1k/yr (cum=2000, 9 doublings) | 10k/yr (cum=50K, 13.6 doublings) | Implied learning rate |
|---|---|---|---|---|
| Manufacturing | $90M | $26M | $12.2M | ~13.5% (Mach33 states 15% / Q4'25 0.85 progress ratio) |
| Ops + fuel | $10M | $5M | $3M | ~7-10% |
| Refurb | $2M | $0.5M | $0.25M | ~14-15% |
| **Combined ops + fuel + refurb** | **$12M** | **$5.5M** | **$3.25M** | **~9-10%** |

Patch E §6.13 uses:
- Manufacturing: learning rate **0.15** (matches Mach33 stated value + Q4'25 R159 + NASA aerospace standard)
- Ops + fuel + refurb: learning rate **0.10** (lumped — Mach33's three components are similar enough at lumped level)

### §6.13.3 Assumptions §3 amendments — REPLACES §6.4 list

Sprint 3 plugin amends Assumptions §3 Capacity. The full list of amendments (replacing §6.4 + §6.11 inputs):

**Updates to existing rows:**

| Row | Old value | New value | MC Min | MC Max | MC Dist | Notes |
|---|---|---|---|---|---|---|
| R32 `Super Heavy manufacturing cost ($mm/unit, base year)` | 35.1 | **54** | 42 | 70 | triangle | Mach33: booster 60% × $90M total mfg = $54M today. ±25% MC range. |
| R33 `Starship 2nd-stage manufacturing cost ($mm/unit, base)` | 23.4 | **36** | 27 | 50 | triangle | Mach33: ship 40% × $90M total mfg = $36M today. ±25% MC range. |
| R34 `Ship refurb % of manufacturing` | 0.02 | **DROPPED FROM ASSUMPTIONS** | — | — | — | Vlad lock 2026-05-20: refurb folded into the new `Starship ops + fuel + refurb cost` curve. R34 removed entirely (not just deprecated to memo). |
| R46 `Variant mix (% fully reusable)` year-row | D=0 E=0.05 F=0.15 ... AC=0.95 | **D=0, E=0, F:AC = 1.0** (step at 2027) | n/a | n/a | fixed-yearrow | Q4'25 Valuation Inputs!R17 + R23 + Vlad lock: Starship 100% reusable from 2027. |

**New Assumptions rows (append below R64 per Rule 10):**

| Label | Base Case | MC Min | MC Max | MC Distribution | Notes |
|---|---|---|---|---|---|
| `Starship manufacturing cost anchor ($mm/stack, 2024 baseline)` | **90** | 70 | 130 | triangle | Mach33 today anchor (booster $54M + ship $36M). ±25% MC range captures SpaceX disclosed vs internal estimates. |
| `Starship manufacturing WL learning rate (% reduction per doubling cum stacks)` | **0.15** | 0.10 | 0.25 | triangle | Mach33 stated + Q4'25 R159 + NASA aerospace standard. Q4'25 Valuation Inputs!R21 has same. MC bracket: 10% (conservative aerospace) → 25% (aggressive industrial scale). |
| `Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)` | **4** | 2 | 10 | triangle | Q4'25 R160 default. Represents ~4 successful Starship integrated flight tests through end-2024. MC range covers 2-10 (varying definitions of "successful test"). |
| `Starship ops + fuel + refurb cost anchor ($mm/launch, 2024 baseline)` | **12** | 8 | 20 | triangle | Mach33 today: $10M ops+fuel + $2M refurb. MC range ±50% reflects high uncertainty on Starship ground-handling cost vs Falcon 9 maturity. |
| `Starship ops + fuel + refurb WL learning rate (% reduction per doubling cum stacks)` | **0.10** | 0.05 | 0.15 | triangle | Back-derived from Mach33's three regime anchors ($12M → $5.5M → $3.25M). MC range wider than mfg's because ops+fuel+refurb learning is less-studied than mfg learning (NASA handbook doesn't separate). |
| `Starship booster share of manufacturing cost (% of stack mfg)` | **0.60** | 0.50 | 0.70 | triangle | Mach33 booster 60% / ship 40% split. Booster is heavier + 33 Raptors vs ship's 6. MC range captures variant build complexity. |

**Payload year-row inputs (from §6.12, restated for completeness):**

| Label | Base Case | MC Min | MC Max | MC Distribution | Notes |
|---|---|---|---|---|---|
| `Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)` | **100000** | 75000 | 130000 | triangle | Sprint 0 R12 retained. Q4'25 2024 baseline = 75K. |
| `Starship payload — 2030 anchor (kg-to-LEO, fully reusable mode)` | **200000** | 150000 | 250000 | triangle | Q4'25 Valuation Inputs!R19 median + MC range. Mach33 1k/yr regime anchor. |
| `Starship payload — max cap (kg-to-LEO)` | **250000** | 200000 | 300000 | triangle | Q4'25 Earth!R74 + Mach33 10k/yr regime ceiling. |
| `Starship payload — booster-only mode delta (kg, additive to fully-reusable)` | **50000** | 30000 | 80000 | triangle | Ship-landing-mass overhead Mach33 implies. Sprint 0 R11 − R12 = 50K. |

### §6.13.4 Launch Capacity tab amendments — REPLACES §6.5 + §6.11 formulas

Three discrete sections — same row map as §6.5 + §6.11 (R30 cum stacks, R37–R41 cost stack), just refined formulas.

**R30 cum-stacks running sum (unchanged from §6.5):**

```
A30 = "Cum Starship stacks manufactured (end-of-year, units)"
D30 = =INDEX(Assumptions!$B:$B, MATCH("Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)", Assumptions!$A:$A, 0))
E30 = =D30 + D25   (Rule 23 year-chained running sum)
copyToRange source E30, destination F30:AC30
```

**REPURPOSED rows R37–R40 (REPLACES §6.5 + §6.11.3 formulas):**

```
A37 = "Starship manufacturing cost ($mm/stack, this year)"   [NEW label — was "Starship full-stack cost" in §6.5]

D37 = =INDEX(Assumptions!$B:$B, MATCH("Starship manufacturing cost anchor ($mm/stack, 2024 baseline)", Assumptions!$A:$A, 0))
      * (
          D30 / INDEX(Assumptions!$B:$B, MATCH("Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)", Assumptions!$A:$A, 0))
        )^(LOG(1 - INDEX(Assumptions!$B:$B, MATCH("Starship manufacturing WL learning rate (% reduction per doubling cum stacks)", Assumptions!$A:$A, 0)), 2))

   (Reads: $90M_anchor × (cum_stacks / 4)^WL_exp_mfg where WL_exp_mfg = LOG(0.85, 2) ≈ -0.234.
    At cum=4 anchor: $90M × 1 = $90M.
    At cum=2048 (~1k regime, 9 doublings): $90M × 0.85^9 = $20.9M. Mach33 says $26M — within 25%.
    At cum=50000 (10k regime, 13.6 doublings): $90M × 0.85^13.6 = $10.3M. Mach33 says $12.2M — within 16%.)

copyToRange source D37, destination E37:AC37

---

A38 = "Starship ops + fuel + refurb cost per launch ($mm, this year)"   [NEW label + NEW formula — replaces "Starship variable cost per launch" + lumped 20% floor]

D38 = =INDEX(Assumptions!$B:$B, MATCH("Starship ops + fuel + refurb cost anchor ($mm/launch, 2024 baseline)", Assumptions!$A:$A, 0))
      * (
          D30 / INDEX(Assumptions!$B:$B, MATCH("Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)", Assumptions!$A:$A, 0))
        )^(LOG(1 - INDEX(Assumptions!$B:$B, MATCH("Starship ops + fuel + refurb WL learning rate (% reduction per doubling cum stacks)", Assumptions!$A:$A, 0)), 2))

   (Reads: $12M_anchor × (cum_stacks / 4)^WL_exp_ops where WL_exp_ops = LOG(0.90, 2) ≈ -0.152.
    Per-launch (paid each flight). Independent Wright's Law curve from manufacturing.
    At cum=4 anchor: $12M.
    At cum=2048: $12M × 0.90^9 = $4.65M. Mach33 says $5.5M ops+refurb — within 15%.
    At cum=50000: $12M × 0.90^13.6 = $2.83M. Mach33 says $3.25M — within 13%.)

copyToRange source D38, destination E38:AC38

---

A39 = "Starship D&A share per launch, fully reusable mode ($mm)"   [Same as §6.11 label]

D39 = =IFERROR(
        D37 * (
          INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0)) / D21
        + (1 - INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0))) / $D$13
        )
        , 0)

   (Reads: mfg × (booster_share / booster_lifetime_year_row + ship_share / ship_lifetime_cap))
   (R37 is now manufacturing-only ($90M anchor), not lumped stack — D&A amortization works against the right base.)
   (At cum=4, 2025 R21=5, $D$13=30: D39 = $90M × (0.60/5 + 0.40/30) = $90M × (0.12 + 0.0133) = $90M × 0.1333 = $12.0M.
    At cum=4, 2030 R21=30: D39 = $90M × (0.60/30 + 0.40/30) = $3.0M.
    At cum=4, 2050 R21=100: D39 = $90M × (0.60/100 + 0.40/30) = $1.74M.
    Once Sprint 10 lights up cum-stacks growth, D&A scales DOWN further per WL decline of R37 manufacturing.)

copyToRange source D39, destination E39:AC39

---

A40 = "Starship at-cost rate ($mm/launch)"   [Canonical Sprint 10 read label — UNCHANGED]

D40 = =D38 + D39   (NEW formula: ops+fuel+refurb per launch + D&A share. Both declining via separate WL curves.)
   (Sprint 2 had =D37+D38+D39; §6.5 changed to =D38+D39; §6.13 same as §6.5 but with new R37/R38 semantics.)
   (At cum=4, 2025: D40 = $12M + $12M = $24M. Compared to Sprint 2's pre-patch $30.42M — 21% lower.
    At cum=4, 2030: D40 = $12M + $3M = $15M (assuming Sprint 2's R25=0 placeholder still in effect — R30 cum stays at 4).
    Once Sprint 10 lights up R25:
      At cum=2048 (~2030-32, 1k regime): D40 = $4.65M + $20.9M × (0.6/30 + 0.4/30) = $4.65M + $0.70M = $5.35M
      At cum=50000 (~2040+, 10k regime): D40 = $2.83M + $10.3M × (0.6/100 + 0.4/30) = $2.83M + $0.20M = $3.03M
      At 250K kg payload (max cap): $3.03M / 250K = **$12.1/kg → matches Mach33's "$10/kg at 10k/yr regime" anchor**)

copyToRange source D40, destination E40:AC40
```

**REPURPOSED row R41 (booster-only mode — REPLACES §6.11.3 formula):**

```
A41 = "Memo: Starship at-cost rate, ship-expended mode (Moon/Mars, $mm/launch)"   [Label unchanged from §6.11]

D41 = =D38
      + IFERROR(D37 * INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0)) / D21, 0)
      + D37 * (1 - INDEX(Assumptions!$B:$B, MATCH("Starship booster share of manufacturing cost (% of stack mfg)", Assumptions!$A:$A, 0)))

   (Three terms:
     1. Ops + fuel + refurb (D38) — same as fully reusable mode (per-launch, declining WL)
     2. Booster D&A — manufacturing × booster_share / booster_lifetime (booster recovered)
     3. Ship FULL cost expensed — manufacturing × ship_share (ship stays at destination)
    At cum=4, 2025: D41 = $12M + $90M × 0.6 / 5 + $90M × 0.4 = $12 + $10.8 + $36 = $58.8M.
    Once Sprint 10 + cum grows:
      At cum=2048: D41 = $4.65 + $20.9 × 0.6/30 + $20.9 × 0.4 = $4.65 + $0.42 + $8.36 = $13.43M
      At cum=50000: D41 = $2.83 + $10.3 × 0.6/100 + $10.3 × 0.4 = $2.83 + $0.062 + $4.12 = $7.01M
      At 250K kg cap: $7.01M / 250K = $28/kg — significantly higher than LEO mode ($12/kg) due to ship expensed full)

copyToRange source D41, destination E41:AC41
```

### §6.13.5 Expected output trajectory (replaces §6.6 + §6.11.5 tables)

Sprint 2 + Sprint 3 baseline (Sprint 10 not yet fired, R25 = 0 placeholder, cum-stacks stays at 4 anchor):

| Year | R30 cum | R37 mfg ($M) | R38 ops+fuel+refurb ($M) | R39 D&A LEO ($M) | **R40 LEO at-cost** | **R41 Moon/Mars at-cost** |
|---|---|---|---|---|---|---|
| 2025 | 4 | $90.0 | $12.0 | $12.0 (R21=5, R13=30) | **$24.0M** | $12 + $10.8 + $36 = **$58.8M** |
| 2026 | 4 | $90.0 | $12.0 | $7.95 (R21=8) | **$19.95M** | $12 + $6.75 + $36 = **$54.75M** |
| 2027 | 4 | $90.0 | $12.0 | $7.5 (R21=12) | **$19.5M** | $12 + $4.5 + $36 = **$52.5M** |
| 2030 | 4 | $90.0 | $12.0 | $3.0 (R21=30) | **$15.0M** | $12 + $1.8 + $36 = **$49.8M** |
| 2050 | 4 | $90.0 | $12.0 | $1.74 (R21=100) | **$13.74M** | $12 + $0.54 + $36 = **$48.54M** |

Post-Sprint-10 (R25 ramps, cum-stacks grows):

| Year | Cum stacks (approx) | R37 mfg | R38 ops | R39 D&A LEO | R40 LEO at-cost | R41 Moon/Mars |
|---|---|---|---|---|---|---|
| 2030 | ~50 | $59.3M | $9.6M | $1.98M | $11.6M | $9.6 + $1.19 + $23.7 = $34.5M |
| 2035 | ~500 | $32.0M | $6.6M | $1.07M | $7.7M | $6.6 + $0.64 + $12.8 = $20.0M |
| 2040 | ~5000 | $14.6M | $4.0M | $0.49M | $4.5M | $4.0 + $0.29 + $5.84 = $10.1M |
| 2050 | ~50000+ | $10.3M | $2.8M | $0.20M | $3.0M | $2.8 + $0.062 + $4.12 = **$7.0M** |

LEO terminal $/kg = $3.0M / 250K kg = **$12/kg** ✓ matches Mach33 "$10/kg at 10k/yr regime"

Moon/Mars terminal $/kg = $7.0M / 200K kg (ship-expended payload is R12+50K=150K → could be higher; assuming Mach33's 250K cap also applies to booster-only) = **$28/kg**

### §6.13.6 What gets dropped (replaces §6.7)

The Sprint 2 variant-mix-weighted formula AND the §6.4–§6.5 lumped-floor formula are both fully replaced. Specifically:

- R37 Sprint 2 formula `=D9*(1-D20) + D9*D10*D20 + 0` → DROPPED (variant-weighted variable cost; superseded twice)
- R37 §6.5 formula `=$100M × (0.20 + 0.80 × (cum/4)^WL_exp)` → DROPPED (lumped 20% floor approach)
- R38 Sprint 2 formula `=D8/D21` → DROPPED
- R38 §6.5 formula `=D37 × 0.20` → DROPPED (= variable share of lumped stack)
- R39 Sprint 2 formula `=D9/$D$13*D20` → DROPPED
- R39 §6.5 formula `=D37 × 0.80 / D21` → DROPPED (lumped D&A)
- R39 §6.11 formula (booster + ship split using lumped stack) → DROPPED
- R40 Sprint 2 formula `=D37+D38+D39` → REPLACED by `=D38+D39`
- R34 ship refurb % → DROPPED FROM ASSUMPTIONS (folded into ops+fuel+refurb anchor)

Inputs DROPPED from §6.4 Assumptions amendments:
- `Starship full-stack cost anchor ($mm, 2024 baseline)` = 100 → REPLACED by manufacturing anchor $90M + ops anchor $12M (split)
- `Starship variable cost share (% of stack)` = 0.20 → DROPPED (no longer needed under split-cost approach; both portions decline)

### §6.13.7 Calibration impact

**Sprint 3 verification:** D40 (Starship at-cost rate 2025) under §6.13 = **$24.0M** (= $12M ops + $12M D&A at 5-yr booster lifetime). Sprint 2 had $30.42M; §6.5 had $30.67M; §6.13 lands at $24.0M. The lower value reflects: (a) ops+fuel+refurb anchor $12M correctly captures per-launch costs (was $20M under lumped 20% floor — over-stated by $8M), (b) D&A correctly amortizes manufacturing-only $90M (not lumped $100M).

Sprint 2 §6.1 calibration locks 2025 only: Starship launches = 0 exact. D40 doesn't enter the 2025 calibration check (any cost × 0 launches = 0 output). The change is purely about cost trajectory in years where Starship actually flies.

**Sprint 11 Valuation:** §6.13 terminal LEO $/kg = $12/kg at cum=50,000+. This matches Mach33's "$10/kg at 10k/yr regime" within 20% (acceptable given the lumped ops+fuel+refurb anchor). If Vlad's investment thesis needs the more aggressive ~$10/kg, the MC range on ops_learning_rate (5%–15%) and mfg_learning_rate (10%–25%) provides the tunable knobs without changing the structural mechanic.

### §6.13.8 Implementation note for Sprint 3 plugin

Sprint 3 plugin executes Patch E §6.13 (not §6.4–§6.5) as the canonical Starship cost mechanic. The Assumptions table gets:
- R32 update to $54M
- R33 update to $36M
- R34 DELETED (Sprint 3 plugin removes the row; the row label `Ship refurb % of manufacturing` no longer exists on Assumptions after Patch E lands)
- R46 step function (0 → 0 → 1.0 at 2027 onwards)
- 6 new rows appended below R64 (mfg anchor, mfg WL rate, anchor cum units, ops anchor, ops WL rate, booster share)
- 4 new rows appended below those (payload baseline, payload 2030 anchor, payload max cap, booster-only payload delta)

R34 deletion is the only DELETE operation in Sprint 3's Assumptions amendments. All others are appends (Rule 10 OK). The R34 deletion is an exception that's explicitly Vlad-approved 2026-05-20 ("Yes fold refurb into floor" → updated to "fold into the ops+fuel+refurb curve"); Sprint 3 plugin executes the deletion as a single discrete operation BEFORE the appends, per Rule 1.

---

## §6.12 — Payload-capacity growth + reusable year correction (Q4'25 dynamics)

Added 2026-05-20 after Vlad pointed to the Q4'25 `Valuation Inputs & Logic` tab as a source of additional time-varying dynamics that Sprint 0 and Sprint 2 missed by anchoring R11/R12 payload as flat single values.

### §6.12.1 Q4'25 dynamics worth absorbing

| Q4'25 ref | Dynamic | Sprint 0 / Sprint 2 current state | Patch E §6.12 amendment |
|---|---|---|---|
| `Valuation Inputs & Logic`!R17, R23 | Starship fully reusable year = 2027 (commercially viable also 2027) | §6.4 R46 step at 2026 | **CORRECTED**: R46 step at 2027 (matches Q4'25 + Mach33 + Vlad's "100% reusable in 2027"). 2026 = first commercial flight (likely expendable test flights), 2027 = full reusability. |
| `Valuation Inputs & Logic`!R19 | Starship payload 2030 anchor = **200,000 kg** (median; range 150K-250K) | Sprint 0 R12 = 100K flat (fully reusable mode) | **NEW**: Add 2030 payload anchor input + bounded-CAGR year-row. Payload grows from 100K (2025) to 200K (2030) via CAGR, capped at 250K max (Q4'25 Earth!R74 + Mach33 10k/yr regime). |
| `Valuation Inputs & Logic`!R74 (via Earth tab) | Max useful payload cap = **250,000 kg** (Mach33 10k/yr regime anchor) | Not in Sprint 0 | **NEW**: Add payload max cap input. Hard ceiling on R29 per-launch upmass. |
| `Valuation Inputs & Logic`!R26 | Starship % dedicated to Starlink in 2030 = **80%** (range 70-90%) | Not in Sprint 0 | **REFERENCE for Sprint 3/4**: Sprint 3 Customer Launch + Sprint 4 Starlink should use this anchor when wiring Starship internal vs customer split. Patch B's demand-driven F9 wiring extends naturally to Starship-side split via this anchor. |
| `Valuation Inputs & Logic`!R27 | Max annual production increase = **3x** (median; range 1-4x) | Sprint 0 R44 = 2x | **DEFER**: Sprint 0 R44 = 2 stays in place for Sprint 2/3 (not load-bearing yet). Sprint 10 vehicle build claim spec author considers updating to 3 for closer Q4'25 alignment. |
| `Valuation Inputs & Logic`!R18 | Wright's Law on turnaround time = 19% per cum-upmass doubling | Sprint 0 R41 = 0.145 (= 14.5%) | **DEFER**: Sprint 0 R41 = 0.145 is close to Q4'25 R18 = 0.19 median; both within Q4'25's MC range [0.05, 0.25]. No change for Sprint 3; Sprint 11 audit can revisit. |
| `Valuation Inputs & Logic`!R21 | Wright's Law on launch cost/kg = 15% | Patch E §6.4 R66 = 0.15 | **ALREADY MATCHES**. No change. |

### §6.12.2 Corrected R46 variant mix (replaces §6.4 R46 amendment)

Supersedes the §6.4 amendment to R46. New value:

| Field | Value |
|---|---|
| Column A label | `Variant mix (% fully reusable)` (unchanged) |
| Type | YR (year-row) |
| Year values | **D (2025) = 0, E (2026) = 0, F (2027) = 1.0, G:AC (2028-2050) = 1.0** |
| Notes (C-col) | `Starship 100% reusable from 2027 per Q4'25 Valuation Inputs!R17 median (= "What year does Starship become fully reusable") + Vlad lock 2026-05-20. 2025-2026 are pre-commercial test era (no reusable launches modeled). Step function 0 → 1.0 at 2027.` |
| MC Distribution | `fixed-yearrow` (unchanged) |

Implication: 2025 and 2026 reusable share = 0 (so per-launch upmass in those years would default to R11 booster-only = 150K kg — but R33 Starship launches = 0 in those years anyway per the calibration target, so this doesn't affect 2025/2026 outputs). 2027+ uses fully reusable mode by default; Sprint 7 Lunar Mars reads the booster-only memo R41 for Moon/Mars-specific missions.

### §6.12.3 New Assumptions rows for payload growth

Append below the §6.4 + §6.11 list (Sprint 3 spec author confirms exact rows; per Rule 10 always append):

| Label | Base Case | MC Min | MC Max | MC Dist | Notes |
|---|---|---|---|---|---|
| `Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)` | **100000** | 75000 | 130000 | triangle | Sprint 0 R12 value retained as 2025 baseline anchor. Q4'25 Earth!I76 has 2024 baseline = 75K kg; Sprint 0 anchored at 100K (slightly more optimistic but defensible for 2025 V3 era). |
| `Starship payload — 2030 anchor (kg-to-LEO, fully reusable mode)` | **200000** | 150000 | 250000 | triangle | Q4'25 Valuation Inputs!R19 median = 200K. Drives the bounded-CAGR year-row. Mach33 1k/yr regime anchor. |
| `Starship payload — max cap (kg-to-LEO)` | **250000** | 200000 | 300000 | triangle | Q4'25 Earth!R74 = 250K (matches Mach33's 10k/yr regime payload anchor). Hard ceiling on R29 per-launch upmass. |
| `Starship payload — booster-only mode delta (kg, additive to fully-reusable payload)` | **50000** | 30000 | 80000 | triangle | The ~50K kg payload bonus from not landing the ship (Sprint 0 R11 − R12 = 150K − 100K = 50K). Applied to booster-only mode (Moon/Mars per §6.11). |

R11 (booster-only mode payload) and R12 (fully reusable payload) — Sprint 0 single-value rows — are **deprecated as direct payload inputs**. Their values stay on Assumptions as breakdown memos (R12 = 2025 baseline, R11 = R12 + booster-only delta), but the load-bearing payload year-row is computed dynamically on Launch Capacity per §6.12.4.

### §6.12.4 Launch Capacity tab amendments — payload year-row

NEW row at R32 (currently blank in Sprint 2 row map — between R31 Booster-only launches and the "Total Starship launches" R33 — actually wait, R31/R32 are already used in Sprint 2 for `Booster-only launches per year` and `Fully-reusable launches per year`. Can't use R32.)

Actually re-checking Sprint 2 row map: R30 (used for Patch E §6.5 NEW cum stacks), R31 = Booster-only launches, R32 = Fully-reusable launches, R33 = Total Starship launches, R34 = Total Annual Capacity. No blank rows in this range.

Need to either:
(a) Repurpose R29 (`Per-launch upmass (kg)`) with the new bounded-CAGR formula
(b) Append payload year-row at the END of the Starship section (between R34 and R35 blank/R36 subheader) — but Sprint 2 row map has R35 as blank, R36 as subheader. Could use R35.
(c) Add to Launch Capacity row 35 (currently blank).

Cleanest is (a) — R29 already exists as `Per-launch upmass (kg)` with a static-variant-weighted formula. Repurpose its formula to reference the new dynamic payload year-row inputs:

```
A29 unchanged: "Per-launch upmass (kg)"

D29 = =MIN(
        INDEX(Assumptions!$B:$B, MATCH("Starship payload — max cap (kg-to-LEO)", Assumptions!$A:$A, 0)),
        INDEX(Assumptions!$B:$B, MATCH("Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)", Assumptions!$A:$A, 0))
        * (
          INDEX(Assumptions!$B:$B, MATCH("Starship payload — 2030 anchor (kg-to-LEO, fully reusable mode)", Assumptions!$A:$A, 0))
          / INDEX(Assumptions!$B:$B, MATCH("Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)", Assumptions!$A:$A, 0))
          ) ^ (D$5 / 5)
        ) * D20
      + MIN(
        INDEX(Assumptions!$B:$B, MATCH("Starship payload — max cap (kg-to-LEO)", Assumptions!$A:$A, 0)),
        (INDEX(Assumptions!$B:$B, MATCH("Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)", Assumptions!$A:$A, 0))
         + INDEX(Assumptions!$B:$B, MATCH("Starship payload — booster-only mode delta (kg, additive to fully-reusable payload)", Assumptions!$A:$A, 0)))
        * (
          INDEX(Assumptions!$B:$B, MATCH("Starship payload — 2030 anchor (kg-to-LEO, fully reusable mode)", Assumptions!$A:$A, 0))
          / INDEX(Assumptions!$B:$B, MATCH("Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)", Assumptions!$A:$A, 0))
          ) ^ (D$5 / 5)
        ) * (1 - D20)

   (Reads: variant_mix × MIN(cap, fully_reusable_payload_2025 × (2030/2025 ratio)^(year_offset/5))
                 + (1-variant_mix) × MIN(cap, (booster_only_payload_2025) × same_CAGR_factor))
   (CAGR factor = (200K/100K)^(year_offset/5) — implicit 14.87%/yr to hit 2030 anchor; continues past 2030 capped at 250K)

copyToRange source D29, destination E29:AC29
```

This is long. Equivalent shorter pseudo-Excel using helper cells (cleaner — Sprint 3 spec author picks):
- Add R29.5 (= R30 in current map — but R30 is reserved for cum-stacks in §6.5). Use R35 instead (currently blank spacing): `A35 = "Starship payload year-row factor (CAGR applied)"` then `D35 = MIN(cap, 2025_baseline × (2030_anchor/2025_baseline)^(year_offset/5))`. Then R29 reads R35 × variant_mix + (R35 + booster_delta_capped) × (1 - variant_mix).

Actually the cleanest is to break this into two helper rows. Use R35 (currently blank):

```
A35 = "Starship payload — fully reusable mode year-row (kg)"
D35 = =MIN(
        INDEX(Assumptions!$B:$B, MATCH("Starship payload — max cap (kg-to-LEO)", Assumptions!$A:$A, 0)),
        INDEX(Assumptions!$B:$B, MATCH("Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)", Assumptions!$A:$A, 0))
        * (
          INDEX(Assumptions!$B:$B, MATCH("Starship payload — 2030 anchor (kg-to-LEO, fully reusable mode)", Assumptions!$A:$A, 0))
          / INDEX(Assumptions!$B:$B, MATCH("Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)", Assumptions!$A:$A, 0))
        )^(D$5/5)
      )
copyToRange source D35, destination E35:AC35

   Then R29 reformulates:
A29 = "Per-launch upmass (kg)"
D29 = =D35 * D20 + MIN(
        INDEX(Assumptions!$B:$B, MATCH("Starship payload — max cap (kg-to-LEO)", Assumptions!$A:$A, 0)),
        D35 + INDEX(Assumptions!$B:$B, MATCH("Starship payload — booster-only mode delta (kg, additive to fully-reusable payload)", Assumptions!$A:$A, 0))
      ) * (1 - D20)
copyToRange source D29, destination E29:AC29
```

But R35 is currently a "blank spacing" row in Sprint 2's map (between Starship section R34 and at-cost subheader R36). Using R35 for a real row breaks the spec map's visual rhythm but doesn't break references. Acceptable.

### §6.12.5 Expected R29 trajectory (fully reusable mode dominant from 2027)

With:
- 2025 baseline = 100K kg, 2030 anchor = 200K, max cap = 250K, booster-only delta = +50K
- CAGR implied = (200/100)^(1/5) − 1 = 14.87%/yr
- Variant mix step: 0 → 0 → 1.0 from 2027

| Year | Variant mix | Fully-reusable payload (R35) | Booster-only payload (R35 + 50K, capped) | Per-launch upmass (R29) |
|---|---|---|---|---|
| 2025 | 0 | 100,000 | 150,000 | 150,000 (100% booster-only) |
| 2026 | 0 | 114,870 | 164,870 | 164,870 (100% booster-only) |
| 2027 | 1.0 | 131,950 | 181,950 | **131,950** (step to fully reusable) |
| 2028 | 1.0 | 151,572 | 201,572 | 151,572 |
| 2030 | 1.0 | **200,000** | 250,000 (capped) | 200,000 ✓ Q4'25 anchor |
| 2032 | 1.0 | 250,000 (capped) | 250,000 (capped) | 250,000 (at cap) |
| 2040 | 1.0 | 250,000 | 250,000 | 250,000 |
| 2050 | 1.0 | 250,000 | 250,000 | 250,000 |

Note: 2025-2026 R29 values are immaterial because Starship launches = 0 (R33 = 0). They show up in R34 = R33 × R29 = 0 anyway. 2027+ R29 drives meaningful R34 capacity output.

### §6.12.6 Implications for Sprint 10 Total Annual Capacity

Once Sprint 10 lights up R25 cum-stacks ramp, R34 `Total Annual Capacity (kg-to-LEO)` = R33 × R29 starts producing realistic year-by-year capacity per:
- 2027: cum_stacks growing, Starship launches ramping per fleet × cadence × variant mix, payload ~131K/launch
- 2030: ~200K kg/launch — matches Q4'25 anchor at 1k/yr regime
- 2035+: 250K kg/launch cap — matches Mach33's 10k/yr regime

This adds the missing growth dynamic that Vlad pointed to. Sprint 11 Valuation outputs will reflect the increasing per-launch payload as cum-stacks scale, not a flat 100K assumption that Sprint 2 baked in.

### §6.12.7 Other Q4'25 dynamics worth noting (deferred to later sprints)

Surfaced from Q4'25 `Valuation Inputs & Logic` for Sprint 3+ spec authors:

1. **Starship % dedicated to Starlink in 2030 = 80%** (R26). Sprint 3 Customer Launch + Sprint 4 Starlink should anchor the Starship internal vs customer split to this. Pre-2027 Starship is 0 → 100% internal-stub doesn't matter. 2027-2030 ramps to 80% Starlink / 20% customer. 2030+ likely tapers as constellation completes (per Q4'25 R271 "Starlink Constellation Complete" flag mechanic). Sprint 4 spec author owns this.
2. **Bandwidth TAM realization factor = 1.0** (R20). Multiplier on modeled bandwidth TAM (range 0.7-1.3). Sprint 4 Starlink revenue formula should expose this as an MC-variable input on the Demand Curves tab read.
3. **Compute satellite W/kg in 2030 = 80 W/kg** (R35), annual growth 8%/yr (R36). Sprint 5 ODC anchors. Sprint 0 R207 = 140 kW/sat for V2 Compute reconciles to this if sat mass = 1,750 kg (140K/80 = 1,750 — close to Sprint 0 R209 = 1,400 kg dry mass; slight inconsistency to flag).
4. **Compute Chip TOPS/W in 2030 = 30** (R37), annual growth 15% (R38). Sprint 5 ODC chip roadmap input. Worth cross-checking against Sprint 0 R241-R244 chip roadmap year-rows.
5. **IPO Cash Proceeds = $30B-$50B median** (R31, $30B downside / $50B upside / $40B median). Sprint 0 Allocator §2 likely already locks at $30B; Q4'25 median is higher — flag for Sprint 10 Allocator brain spec author.
6. **Compute Allocation Share (vs Moon/Mars) = 85%** (R34). Means 85% of compute-eligible cash goes to ODC, 15% to Moon/Mars. Sprint 10 Allocator brain spec author should compare to Architecture §6.3 sigmoid mechanic.

None block Patch E or Sprint 3 — flagging here for downstream sprint authors to mine when they touch those modules.
