# Sprint 11e Spec — Reduced Sprint 11 (no deployment binding; LM BV correction + Launch Capacity wiring + CL R210)

**Sprint name**: Sprint 11 final landing. Reduced scope after Sprint 11d (V2.18) collapsed Group Revenue 2050 due to circular dependency in deployment binding (§3.5b/§3.6 architecture). This sprint executes the SOUND parts of Sprint 11 (LM BV correction, Launch Capacity fleet wiring, CL R210, bridge loan completion) and DEFERS deployment binding to Sprint 11f (which needs spec architectural rework).

**Status**: spec-author chat, drafted 2026-05-26 EOD after Vlad halt + plugin diagnosis of circular dependency.

**Starting workbook**: V2.17.xlsx (merged Block 1 PASS + bridge loan partial). Vlad opens V2.17, saves-as V2.19, plugin executes against V2.19.

**Architecture compliance**: per `02_Architecture_and_Methodology.md` §20 amendments block. §20.5 LM BV correction is the highest-stakes amendment landing here. §20.3 deployment binding requirement is DEFERRED — not in 11e scope. §20.1, §20.2 (vehicle-level allocator structure) already landed in V2.17 baseline.

**What this sprint does NOT do**:
- §3.5b Starlink Module IN expand — SKIPPED (Sprint 11f scope)
- §3.6 Per-vehicle deployment formula rewire — SKIPPED (Sprint 11f scope)
- §3.7 Retire R43 ratchet + Assumptions R320 V2 DTC cap — SKIPPED (paired with §3.6; defer to 11f)
- §3.8 Module-level deployment binding (CL/ODC/AIS R205) — SKIPPED (same circular pattern; defer)

Starlink module continues to deploy via its OLD hardcoded ramp logic (R33/R37/R39/R41 with ratchet flag + V3 trigger year). Allocator remains "advisory not binding" per `project_allocator_advisory_not_binding_2026_05_26` memory. This is a known architectural compromise documented for Sprint 11f resolution.

---

## §0 Rule Compliance Preamble

- [x] Rule 1 — separate writes per concept
- [x] Rule 3/23 — anchor-and-offset; Cash BoY R15 chain remains existing Rule 23 EXCEPTION
- [x] Rule 4 — D/I/S/AC read-backs per section
- [x] Rule 6 — full Excel formulas inline
- [x] Rule 10 — no row insertions; in-place formula REPLACE only
- [x] Rule 11 — touch points enumerated for new LM Module D&A row + R28/R36 formula amendments + CL R210
- [x] Rule 12 — INDEX/MATCH by canonical label
- [x] Rule 14 — no hardcoded constants; LM capital lifetime read from Assumptions R204
- [x] Rule 15 — quantitative halt thresholds: R108 = "OK" all years; AC28 Group D&A < $20B post-§3.11; Group Revenue 2050 > $400B (NOT $200B — this is a tighter bar since we're not doing deployment binding); D29 Available cash 2025 > $5B
- [x] Rule 19 — Vlad handles saving
- [x] Rule 22 — Rule 22 stale-ref scan in §4

**Architecture compliance**:
- [x] §20.5 LM BV depreciation removal — sole architectural change in 11e
- [x] §20.4 Launch Capacity endogenous fleet wiring — partial (Starship side; F9 already wired in V2.17 baseline)
- [x] §20.7 CL R210 Capacity Demand — added
- [x] §6.1 Cash Pool Tracker bridge loan extension — Step 3 (R15 amendment) completes the partial work in V2.17

---

## §1 Scope summary

| Section | What ships | Tabs touched |
|---|---|---|
| §3.0 Pre-flight | 5 probes (calc engine sanity + V2.17 baseline + bridge loan partial state) | read-only |
| §3.1.5 Step 3 | Allocator R15 Cash BoY formula amendment (+D11 bridge loan) | Allocator R15 |
| §3.9 | Launch Capacity R8/R9 across years + R25 endogenous boosters built | Launch Capacity R8/R9/R25 |
| §3.10 | F9 R61 col A label update (Decision A — preserve D61/E61 anchors, label-only) | Launch Capacity R61 col A |
| §3.11 | **LM BV depreciation REMOVED from Group D&A** (Group P&L R28 + R36 + new LM Module D&A row + LM R117/R118 col A retirement labels) | Group P&L R28/R36, Lunar Mars R117/R118/R120 |
| §3.12 | ODC unit-economics audit (read-only) | none |
| §3.13 | Customer Launch R210 Capacity Demand wire | Customer Launch R210 |

7 sections total but §3.10 is label-only and §3.12 is read-only, so 5 meaningful writes. Well within sprint sizing convention §10.1 (target 3-5 sections).

---

## §2 Constitutional reference

- Architecture §20 amendments block (`02_Architecture_and_Methodology.md` lines 873-1102+)
- Particularly §20.5 LM BV correction (highest-stakes), §20.4 Launch Capacity fleet wiring, §20.7 CL R210, §6.1 Cash Pool Tracker (with §20.9 bridge loan)
- Sprint 11 spec sections §3.9, §3.11, §3.13 (reference for formula details)
- Sprint Roadmap §10 Sprint Sizing Convention

---

## §3 Execution

### §3.0 Pre-flight (READ-ONLY — halt if any check fails)

**Calc engine sanity probe** (mandatory per Roadmap §10.3):
- Write `=Assumptions!$A$2` to scratch cell Allocator!Z200 (or any unused cell)
- Force calculate(full) + sync
- Read scratch cell value
- Expected: matches Assumptions!A2 text (e.g., "Tax rate (corporate, US federal + state blended)")
- If value is 0 OR empty → calc engine corrupted from prior session; HALT and demand Excel quit+reopen
- Clear scratch cell before proceeding

**Baseline probes**:
```
Assumptions B350 = 2028 (V2 phase-out year, from Sprint 11a)
Assumptions B351 = 20000 (Pre-IPO bridge loan, from Sprint 11c §3.1.5)
Allocator A88 = "Starlink V2 BB cash allocation" (Block 1 §3.3 label)
Allocator D88 = 1116 (Block 1 V2 BB first-year override)
Allocator A93 = "§6 KG IRR-PRIORITY SIGMOID QUEUE" (Block 1 §3.4 shifted header)
Allocator A138 = "Starlink V3 BB kg allocation" (Block 1 §3.5 label)
Allocator A145 = "§8 VEHICLE BUILD CLAIM" (Block 1 §3.5 shifted header)
Allocator A11 = "Pre-IPO bridge loan inflow this year ($mm)" (11c §3.1.5)
Allocator D11 formula text contains "Pre-IPO bridge loan drawdown"
Allocator D11 value = 20000
Allocator D15 = 5000 (Cash BoY 2025 PRE-Step-3; will be $25,000 post-Step-3)
Group P&L AC10 = 583,059 (Sprint 10.5 PASS baseline, NOT collapsed)
Group P&L AC28 = 484,076 (LM BV depreciation phantom, to be REMOVED in §3.11)
Group P&L D108-AC108 = "OK" all 26 years
```

If Group P&L AC10 < $400B → HALT (wrong workbook; should be V2.19 from V2.17 baseline).

---

### §3.1.5 Step 3 — Cash BoY R15 formula amendment

Replace existing R15 formulas to include D11 bridge loan:

```
D15: =D8+D9+D10+D11           (was =D8+D9+D10; adds bridge loan to 2025 starting)
E15: =D15+E10+E9+E11           (was =D15+E10+E9; adds E11 bridge in subsequent years)
Copy E15 across F15:AC15
```

Write D15 as formula. Write E15 as formula. autoFill E15→F15:AC15 (single row, single column source — Rule 2 compliant).

**Verification reads**:
- D15 Cash BoY 2025 = $25,000M ✓ (was $5,000M; +$20B bridge)
- D28 Year-N non-module claims 2025 = ~$11,289M unchanged
- **D29 Available cash for IRR queue 2025 = ~$13,711M** (was $0; unstarved)
- E15 Cash BoY 2026 = $25,000 + 2025 FCF (~−$3,050M) + 0 IPO + 0 bridge = ~$21,950M
- F15 Cash BoY 2027 = $21,950 + 2026 FCF + $30,000M IPO = ~$50,000M+

**Halt**: D29 ≤ $5B → bridge loan wiring failed; investigate.

---

### §3.9 — Launch Capacity endogenous Starship fleet wiring

**Step 1**: Replicate R8/R9 (Starship cost components) across years. Currently D-only.

```
Launch Capacity E8:AC8 = =$D$8   (Super Heavy mfg cost flat at $54M; Wright's Law decay if Assumptions learning rate > 0)
Launch Capacity E9:AC9 = =$D$9   (Starship 2nd-stage flat at $36M)
```

If Assumptions R14 (manufacturing learning rate) > 0, replace flat replication with Wright's Law decay. Currently R14 = 0 per V2.13/V2.14 baseline.

**Step 2**: Wire R25 Boosters built per year as endogenous formula.

```
Launch Capacity D25:AC25 = =IFERROR(INDEX(Allocator!$D:$AC, MATCH("Vehicle build claim ($mm)", Allocator!$A:$A, 0), D$5+1) / (D8 + D9), 0)
```

Per-year, divides Allocator R150 vehicle build claim cash by blended Starship cost (R8+R9). Note: in V2.18 plugin determined Allocator's `Vehicle build claim ($mm)` canonical label resolves at R156, not R150 (due to row shifts during Block 1). Verify in pre-flight via MATCH probe; plugin uses whatever row resolves.

**Step 3**: R24 / R27 booster fleet chain — verify existing formulas intact (year-chained EoY = BoY + built − retired). No write needed if intact.

**Step 4**: R33 Total Starship launches per year — verify reads R27 × R23 cadence. R34 Total Annual Capacity (kg-to-LEO) — verify reads R33 × R29 payload. Both should be intact from prior sprints; no write needed unless probe shows drift.

**Verification reads**:
- E8 = $54M (Super Heavy cost 2026); AC8 = $54M (flat); F25 (2027) boosters built > 0 (Vehicle build claim cash / $90M); F34 Total Annual Capacity > 0 (kg-to-LEO).

Per Sprint 11d plugin's prior run: E25=0.94 boosters, I25=1.0 boosters, I34=919k kg, AC34=3.4M kg. These are reasonable orders of magnitude.

**Halt**: F34 (2027) Total Annual Capacity = 0 → HALT (Starship fleet wiring didn't take). Probe Allocator R156 Vehicle build claim — if R156 = 0, the upstream sigmoid isn't producing demand.

---

### §3.10 — F9 fleet wiring (Decision A: label-only)

Per Sprint 11a Block 2 plugin probe: Launch Capacity R61 already has correct year-conditional formula (`=MAX(0, $D$55 × (1 − (F$4 − $D$56) / $D$57))` for F+ years, D61/E61 = 17 historical anchors). No formula write needed.

Update R61 col A label only to flag V3-trigger-aware decay (informational):

```
Launch Capacity A61 = "F9 manufactured per year (boosters) — V3-trigger-aware decay schedule (Sprint 11e label note 2026-05-26)"
```

**Verification**: D61 = 17, E61 = 17 (unchanged anchors); F61+ values decay correctly via existing formula.

---

### §3.11 — LM BV depreciation REMOVED from Group D&A (HIGHEST STAKES)

The single most important section. Removes phantom $478B/yr D&A from 2050.

**Step 1**: Add new row on Lunar Mars tab: `Lunar Mars Module D&A ($mm)` at next available position (probe suggests R120; if R120 occupied, append at next free row).

```
Lunar Mars A120 = "Lunar Mars Module D&A ($mm)"
Lunar Mars D120:AC120 formula = =IFERROR(SUM($D$125:D125) / INDEX(Assumptions!$B:$B, MATCH("Capital lifetime — book value straight-line depreciation (years)", Assumptions!$A:$A, 0)), 0)
```

Where R125 = Lunar Mars Module CapEx ($mm) — verify this row exists and is the correct CapEx source. If LM Module CapEx is at a different row (Sprint 7 wrote LM tab), use the canonical label MATCH to resolve.

**IMPORTANT — Mandatory wait-and-recalc** (per `feedback_assumptions_write_then_reference_footgun`): after writing the new LM R120 row, force `worksheet.getItem("Lunar Mars").calculate()` + `context.sync()` and read R120 D-col value back. If value ≠ expected (small but non-zero for years > 2027), HALT — calc engine not picking up new row. May need to save+reopen.

**Step 2**: Amend Group P&L R28 formula. Replace existing formula text.

**Current** (per Sprint 11d plugin probe):
```
=D23+D24+D25+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Lunar ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Mars ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)+INDEX(CapEx!$D:$AC, MATCH("Annual spectrum amortization ($mm)", CapEx!$A:$A, 0), D$5+1)
```

**Replacement**:
```
=D23+D24+D25+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("Lunar Mars Module D&A ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+INDEX(CapEx!$D:$AC, MATCH("Total Corporate D&A ($mm)", CapEx!$A:$A, 0), D$5+1)+INDEX(CapEx!$D:$AC, MATCH("Annual spectrum amortization ($mm)", CapEx!$A:$A, 0), D$5+1)
```

Removes the TWO `BV depreciation — Lunar` and `BV depreciation — Mars` INDEX/MATCH reads; replaces with ONE `Lunar Mars Module D&A` read.

Copy D28 across E28:AC28.

**Step 3**: Amend Group P&L R36 formula (Σ Module D&A in COGS) — same pattern.

**Current**:
```
=D23+D24+D25+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Lunar ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("BV depreciation — Mars ($mm/yr)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)
```

**Replacement**:
```
=D23+D24+D25+IFERROR(INDEX('Lunar Mars'!$D:$AC, MATCH("Lunar Mars Module D&A ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1), 0)
```

Copy D36 across E36:AC36.

**Step 4**: Update Lunar Mars R117 + R118 col A labels (flag as SoTP-only memos):

```
Lunar Mars A117 = "Memo: BV decay — Lunar ($mm/yr) — Valuation tab input only, NOT in Group D&A"
Lunar Mars A118 = "Memo: BV decay — Mars ($mm/yr) — Valuation tab input only, NOT in Group D&A"
```

Formulas at D117:AC117 + D118:AC118 unchanged (they still compute the BV decay for Valuation tab consumption per Architecture §11.4).

**Verification reads (THE BIG ONE)**:
- Group P&L D28 Group D&A 2025 = ~$1,200-1,400M (LM contribution small in 2025)
- **Group P&L AC28 Group D&A 2050 = ~$6,000M** (massive drop from $484,076M baseline; this is the make-or-break check)
- Group P&L AC50 Group FCF 2050 swings from +$337,548M baseline to ~−$90B (illusory FCF removed)
- Lunar Mars D120 Module D&A 2025 = 0 (no cumulative CapEx yet)
- Lunar Mars AC120 Module D&A 2050 = ~$200-500M (proper cash-cap depreciation)
- Lunar Mars AC117 + AC118 still compute as memo (~$368B + ~$109B) but no longer flow into Group D&A

**HALT condition**: AC28 Group D&A > $20B post-write → LM BV refs not fully removed from R28; halt and re-investigate formula text.

---

### §3.12 — ODC unit-economics audit (read-only)

Per Sprint 11 §3.12 verbatim — read + document, no spec body changes:

```
Read ODC R102 Per-sat external compute revenue: D=0, I=$0.5M, AC=$0.5M
Read ODC R150 ODC fleet design life: 5 years
Read ODC R154 Per-sat net marginal revenue: D=0, I=$0.5M, AC=$0.5M
Read ODC per-sat cost components from Assumptions: R151 solar gen × R154 $/W; R152 thermal mass × R155 $/kg; R175 chip cost
Read ODC R207 Spot IRR trajectory: -0.39 / -0.10 / -0.15
```

Document in Claude Log: ODC verdict accepted per Vlad lock 2026-05-26 + Architecture §20.8 — Sprint 11.5 input revision pending.

---

### §3.13 — Customer Launch R210 Capacity Demand wire

```
Customer Launch D210:AC210 formula = =IFERROR(INDEX(Customer Launch!$D:$AC, MATCH("Starship customer launches per year", Customer Launch!$A:$A, 0), D$5+1) * INDEX('Launch Capacity'!$D:$AC, MATCH("Per-launch upmass (kg)", 'Launch Capacity'!$A:$A, 0), D$5+1), 0)
```

R210 = CL R24 Starship customer launches × Launch Capacity R29 per-launch upmass. Currently R24 = 0 across all years (CL external Starship business not sized in module), so R210 = 0. But canonical label resolves for Allocator vehicle build claim sum (R145 in Sprint 10 spec — currently R156 post-Block 1 shifts).

**Verification**: D210 = 0 (CL R24 = 0); E210 = 0; AC210 = 0. Canonical label resolves via MATCH.

---

## §4 Verification

### §4.1 Workbook-wide error scan
Zero #REF! / #VALUE! / #DIV/0! / #NAME? / #N/A across all 15 tabs.

### §4.2 Conservation
Group P&L R108 = "OK" all 26 years 2025-2050. R109 = 0 ±$1M all years.

**Critical**: post §3.11 LM BV correction, conservation MUST hold. The R109 cash flow identity equation:
`Starting cash + Σ IPO + Σ Group FCF − Cash EoY + Σ Bridge loan = 0`

May need R109 formula update if Sprint 10's R109 didn't include bridge loan. Probe R109 formula in pre-flight; if missing bridge loan term, amend formula to add `+ SUMPRODUCT($D$5:D$5<=D$5)*Allocator!$D$11:D$11`.

### §4.3 Calibration drift surface

| Metric | V2.17 baseline | V2.19 expected (Sprint 11e) | Halt range |
|---|---|---|---|
| Group D10 Revenue 2025 | $13,855M | $13,855M (no deployment change) | <$10B or >$17B |
| Group AC10 Revenue 2050 | $583,059M | $580-590B (small drift only) | **<$400B HALT** |
| Group D28 Group D&A 2025 | $1,261M | $1,200-1,400M (LM impact small in 2025) | <$800M or >$2B |
| **Group AC28 Group D&A 2050** | **$484,076M** | **~$6,000M ⬇⬇⬇** | **>$20B HALT** |
| Group D50 Group FCF 2025 | -$2,619M | -$2,700 to -$3,100M (small drift from bridge loan FCF accounting) | <-$5B or >-$1B |
| **Group AC50 Group FCF 2050** | **+$337,548M** | **~-$90B** (illusory removed) | informational |
| Allocator D11 bridge loan 2025 | $20,000M | $20,000M | exact |
| Allocator D15 Cash BoY 2025 | $5,000M (pre-Step-3) | $25,000M (post-Step-3) | exact |
| Allocator D29 Available cash 2025 | $0 | ~$13,711M | <$5B HALT |
| Launch Capacity F34 Total Annual Capacity 2027 | 0 | >0 | =0 HALT |
| Launch Capacity I34 Total Annual Capacity 2030 | 0 | ~919k kg | =0 HALT |
| Conservation R108 all years | "OK" | "OK" | any "CHECK" HALT |

### §4.4 Round-trip stability + Rule 22 stale-ref scan

5x recalc — no value moves >$1M. Rule 22: verify new LM Module D&A canonical label resolves on Group P&L R28 + R36; new bridge loan canonical labels resolve on R109 cash identity; CL R210 canonical label resolves on Allocator R145 (or wherever Vehicle build claim aggregator landed).

### §4.5 Claude Log entry

| Date | Sprint | Tabs touched | Summary | Outstanding |
|---|---|---|---|---|
| 2026-MM-DD | 11e | Allocator R15, Launch Capacity R8/R9/R25/R61 col A, Lunar Mars R117/R118 col A + new R120, Group P&L R28/R36, Customer Launch R210 | Sprint 11 reduced PASS: LM BV depreciation removed from Group D&A (AC28 $484B → $6B); endogenous Starship fleet wiring (R34 lit up); CL R210 canonical label wired; bridge loan Cash BoY complete; Group Revenue 2050 preserved at $583B baseline. Deployment binding deferred to Sprint 11f (architectural rework). | Sprint 11f deployment binding architectural rework; Sprint 9 §6.8 calibration revision (FCF 2050 swing); Sprint 11.5 ODC + bridge loan repayment + interest expense |

---

## §5 Outstanding items (for Sprint 11f / 11.5 / 12)

1. **Sprint 11f — Vehicle-level deployment binding architectural rework**: fix circular dependency. R48/R52/R58/R63 read uncapped target demand (anchor × learning × unit cost), not actual CapEx. Decouples sigmoid demand from sigmoid output. Requires Architecture §6.5 + §20.3 amendment + spec amendment for §3.2 cash queue + §3.6 deployment formulas.
2. **Sprint 11.5 — ODC unit-economics input revision** (Vlad-pending)
3. **Sprint 11.5 — Bridge loan repayment + interest expense**: model has $20B inflow without repayment or interest cost
4. **Sprint 9 §6.8 calibration target revision**: Group FCF 2050 swing from +$337B → ~-$90B; new targets locked post-11e
5. **R110 Σ Module FCF residual** (-$1,640M trajectory): module-owner audit
6. **AC_2050 Group EBITDA negativity** (Lock f): may persist post-LM BV correction; Sprint 12 audit

---

## §6 Amendment log

- **2026-05-26 (initial draft)** — Sprint 11e spec authored after Sprint 11d collapse via §3.6 deployment binding circular dependency. Reduced scope: skip §3.5b/§3.6/§3.7/§3.8 deployment binding entirely; ship §3.1.5 Step 3 + §3.9 fleet wiring + §3.11 LM BV correction + §3.13 CL R210. Deployment binding deferred to Sprint 11f (architectural rework with decoupled sigmoid demand pattern).

---

## End of Sprint 11e Spec
