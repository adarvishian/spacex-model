# Sprint 11c Spec — Recovery sprint with $20B Pre-IPO Bridge Loan + Block 2 redo

**Sprint name**: Sprint 11 recovery. Block 2 (V2.14 → V2.14.5) triggered the deployment chicken-and-egg trap — Architecture §6.5 MIN-bind on cash starved module deployment in 2026+ because Available cash = $0 pre-IPO. Group Revenue 2050 collapsed $583B (Block 1 PASS) → $16B (Block 2). Recovery: revert to V2.14-a1636d7f (Block 1 PASS state) + wire **$20B Pre-IPO Bridge Loan per S-1 disclosure** as Cash Pool Tracker inflow + then execute Block 2-equivalent writes against the now-non-starved cash pipeline.

**Status**: spec-author chat, drafted 2026-05-26 after Sprint 11 Block 2 collapse + Vlad note "S1 told us they did a 20B bridge loan or something". Architecture §20.9 amendment updated 2026-05-26 with $20B Base Case (was $5B pre-S-1).

**Starting workbook state**: V2.14-a1636d7f (Sprint 11 Block 1 PASS) restored. Pre-flight verifies:
- Assumptions R350 V2 phase-out year = 2028 ✓
- Allocator R88-R91 4-row insertion intact; §6/§7/§8/§9 headers shifted +4 ✓
- Allocator §4 cash queue rewritten to 7 sub-blocks compact form ✓
- Allocator R83-R91 canonical labels (5 module + 4 vehicle) populated ✓
- Allocator §6 kg queue 5 sub-blocks ✓
- Allocator §7 R137-R143 kg canonical labels populated ✓
- Group Revenue 2050 = $583,059M (intact baseline)
- Conservation R108 = "OK" all years

**What Sprint 11c does in order**:
1. **§3.1.5 NEW** — Pre-IPO Bridge Loan wiring (Assumptions input + Allocator Cash Pool Tracker row + Cash BoY formula update) — MUST land FIRST before any deployment binding
2. Sprint 11 §3.5b — Starlink Module IN expand
3. Sprint 11 §3.6 — Per-vehicle deployment formula rewire (with 3 gates + MIN bind, NOW non-starved)
4. Sprint 11 §3.7 — Retire R43 + Assumptions R320
5. Sprint 11 §3.8 — Customer Launch + ODC + AI Stack R205 deployment binding
6. Sprint 11 §3.9 — Launch Capacity endogenous Starship fleet wiring
7. Sprint 11 §3.10 — F9 fleet (mostly skip; label only per Decision A)
8. Sprint 11 §3.11 — LM BV depreciation REMOVED from Group D&A (HIGHEST STAKES)
9. Sprint 11 §3.12 — ODC unit-economics audit (read-only)
10. Sprint 11 §3.13 — Customer Launch R210 wire

---

## §0 Rule Compliance Preamble

- [x] Rule 1 — separate writes per concept (use execute_office_js for multi-row sections)
- [x] Rule 3 / 23 — bridge loan is single-year flag input (anchor-and-offset compatible); Cash BoY chain is existing Rule 23 EXCEPTION (extended to include bridge loan term)
- [x] Rule 4 — every §3 section ends with D/I/S/AC read-backs
- [x] Rule 6 — full Excel formulas inline below
- [x] Rule 10 — no row insertions on cross-tab sheets. Assumptions APPEND at R351 (next available after Sprint 11a R350). Allocator §1 Cash Pool Tracker has space (R11-R14 currently empty between R10 and R15); insert new bridge loan row at R11.
- [x] Rule 11 — every touch point enumerated for new bridge loan row
- [x] Rule 12 — INDEX/MATCH by canonical label
- [x] Rule 14 — bridge loan amount + draw year are MC inputs on Assumptions, not hardcoded
- [x] Rule 15 — halt thresholds: Allocator D29 Available cash 2025 must be > $5B (currently $0 pre-fix); R108 = "OK" all years; Group Revenue 2050 must stay > $300B (must NOT collapse like V2.14.5)
- [x] Rule 19 — Vlad handles saving
- [x] Rule 22 — Rule 22 stale-ref scan in §4
- [x] Architecture §20.9 + §6.1 amendment compliance (bridge loan in Cash Pool Tracker)

---

## §1 Scope summary

| Section | What ships | Tabs touched |
|---|---|---|
| §3.0 Pre-flight | Confirm V2.14-a1636d7f restored + Block 1 PASS intact | read-only |
| **§3.1.5 NEW: Pre-IPO Bridge Loan setup** | Assumptions R351 input + Allocator R11 new row + Cash BoY R15 formula update | Assumptions, Allocator |
| §3.5b Starlink Module IN expand | per Sprint 11 §3.5b verbatim | Starlink R7-R14 |
| §3.6 Per-vehicle deployment rewire | per Sprint 11 §3.6 verbatim — NOW non-starved | Starlink R33/R37/R39/R41 |
| §3.7 Retire ratchets | per Sprint 11 §3.7 verbatim | Starlink R43, Assumptions R320 |
| §3.8 Module-level deployment binding | per Sprint 11 §3.8 verbatim | Customer Launch R205, ODC R205, AI Stack R205 |
| §3.9 Launch Capacity Starship endogenous | per Sprint 11 §3.9 verbatim | Launch Capacity R8/R9/R25/R34 |
| §3.10 F9 label-only | per Sprint 11 §3.10 Decision A — label update only | Launch Capacity R61 col A |
| §3.11 LM BV depreciation removal | per Sprint 11 §3.11 verbatim | Group P&L R28/R36, Lunar Mars R117/R118/R120 |
| §3.12 ODC audit | per Sprint 11 §3.12 (read-only) | none |
| §3.13 Customer Launch R210 wire | per Sprint 11 §3.13 verbatim | Customer Launch R210 |

---

## §2 Constitutional reference

- Architecture §20.9 — Pre-IPO Bridge Loan (NEW 2026-05-26)
- Architecture §20.1-§20.8 — Sprint 11 amendments (already in §20 block)
- Architecture §6.1 — Cash Pool Tracker (amended via §20.9)
- Architecture §6.5 — Deployment binding (now feasible with non-starved cash via bridge loan)
- Architecture §11 — Lunar Mars (BV is SoTP terminal value, NOT P&L D&A)
- Sprint 11 spec — §3.5b through §3.13 referenced verbatim (this Sprint 11c spec adds §3.1.5 BEFORE these and does not modify their content)

---

## §3 Execution

### §3.0 Pre-flight (READ-ONLY — halt if any check fails)

Confirm workbook is V2.14-a1636d7f restored OR equivalent Block 1 PASS state (Vlad handles file management):

```
Read Assumptions R350 expect 2028 ("V2 phase-out year")
Read Allocator R83-R91 expect 5 module labels + 4 vehicle labels populated
Read Allocator D88 expect $1,116M (V2 BB cash allocation, first-year override)
Read Allocator D89 expect $68M (V2 DTC)
Read Allocator D90 expect $18M (V3 BB facility CapEx per Decision B)
Read Allocator D91 expect $0 (V3 DTC)
Read Allocator D84 expect $1,202.54M (Starlink rollup = sum of vehicles)
Read Group P&L D10 expect $13,855M (Group Revenue 2025)
Read Group P&L AC10 expect $583,059M (Group Revenue 2050 — BLOCK 1 PASS BASELINE)
Read Group P&L D108-AC108 expect "OK" all years
Read Allocator §6/§7/§8/§9 header positions: R93, R136, R143, R156
Read Allocator §6 kg queue 5 sub-blocks at R98-R122 with Σ at R134
Read Lunar Mars R117/R118 BV depreciation values (baseline before §3.11 removal)
```

If any check fails: HALT and push back to Vlad — workbook may not be properly restored to V2.14-a1636d7f.

**Critical halt**: if Group Revenue 2050 < $500B → workbook is V2.14.5 (broken) not V2.14-a1636d7f (Block 1 PASS). Vlad must re-attach the correct workbook.

---

### §3.1.5 NEW — Pre-IPO Bridge Loan setup ($20B per S-1 disclosure)

**Step 1**: Append Assumptions R351 (next available row after R350 V2 phase-out year):

| Row | Col A label (verbatim) | Col B value | Col C MC Min | Col D MC Max | Col E Dist | Col F Notes |
|---|---|---|---|---|---|---|
| R351 | `Pre-IPO bridge loan drawdown ($mm, drawn in 2025)` | 20000 | 15000 | 25000 | triangle | Per S-1 disclosure (Vlad note 2026-05-26). $20B bridge loan drawn 2025 to fund pre-IPO operations + V2 fleet deployment. MC range reflects uncertainty in actual draw timing + size. Single draw 2025; bridge to IPO 2027. |

Number format: B = `#,##0`, C/D = `#,##0`, E = text.

**Step 2**: Add new Cash Pool Tracker row on Allocator at R11 (between existing R10 Prior-year Group FCF and R15 Cash BoY):

The Cash Pool Tracker §1 currently spans R7-R15 with empty rows R11-R14 between the inputs and Cash BoY at R15. Insert the new row at R11.

| Row | Col A label (verbatim) | Col D formula |
|---|---|---|
| R11 | `Pre-IPO bridge loan inflow this year ($mm)` | `=IF(D$4 = 2025, INDEX(Assumptions!$B:$B, MATCH("Pre-IPO bridge loan drawdown ($mm, drawn in 2025)", Assumptions!$A:$A, 0)), 0)` |

Copy D across E:AC. R11 will = $20,000M in 2025 (D-col) and $0 in all other years.

**Note on year-mapping**: The IF condition checks year 2025 directly (`D$4 = 2025`) rather than year-offset, since the bridge loan is a one-time event in a specific calendar year. If S-1 disclosure indicates draws across multiple years, replace the IF with an INDEX into a new Assumptions year-row input.

**Step 3**: Update Cash BoY R15 formula to include the bridge loan term:

**Current R15 formula** (per Sprint 10 §3.1):
```
D15: =D8+D9+D10            (initial Cash BoY 2025 = Starting + IPO + Prior FCF)
E15: =D15+E10+E9            (next year = prior Cash BoY + this year FCF + this year IPO)
F15:AC15: copy of E15 pattern
```

**Sprint 11c amended R15 formula**:
```
D15: =D8+D9+D10+D11         (add D11 bridge loan to 2025 starting state)
E15: =D15+E10+E9+E11         (next year's Cash BoY adds this year's bridge loan, IPO, prior FCF)
F15:AC15: same pattern; E11/F11/etc. will all be 0 except 2025
```

Copy E across F:AC.

**Verification reads (post-write)**:
- Assumptions B351 = 20000 exact
- Allocator D11 = $20,000M (2025 only)
- Allocator E11 = $0 (2026, no bridge draw)
- Allocator F11 = $0 (2027, IPO covers)
- **Allocator D15 Cash BoY 2025 = $5,000 + $0 IPO + $0 prior FCF + $20,000 bridge = $25,000M** (was $5,000M baseline)
- Allocator D28 Year-N non-module claims 2025 = ~$11,654M (unchanged)
- **Allocator D29 Available cash for IRR queue 2025 = MAX(0, $25,000 − $11,654) = $13,346M** (was $0 baseline) — sufficient to fund Starlink + Customer Launch deployment
- Allocator E15 Cash BoY 2026 = $25,000 + 2025 FCF (~−$3,050M) + $0 IPO + $0 bridge = ~$21,950M
- Allocator E29 Available cash 2026 ≈ $21,950 − ~$15,400M claims = ~$6,550M — sufficient for V2 BB internal ramp
- Allocator F15 Cash BoY 2027 = $21,950 + 2026 FCF + $30B IPO + $0 bridge = ~$50B+
- Allocator F29 Available cash 2027 ≈ $50B − ~$13.6B claims = ~$36B — sufficient for V3 BB launch ramp

**Halt conditions**:
- D29 ≤ $0 → HALT (bridge loan didn't unstarved Available cash; check formula or value)
- D29 > Cash BoY → HALT (math violation)
- E29 ≤ $0 → HALT (2026 still starved; bridge loan inflow not carrying year-to-year via Cash BoY chain)

---

### §3.5b through §3.13 — execute per Sprint 11 spec verbatim

These sections are unchanged from `Sprint_11_Spec.md`. Plugin executes them in order:

1. **§3.5b** — Starlink Module IN block expand to 4 cash + 2 kg reads (R7-R14)
2. **§3.6** — Per-vehicle deployment formula rewire (R33/R37/R39/R41 with 3 gates + MIN bind). Per Sprint 11 §3.6 — V2 phase-out gate uses Assumptions R350 = 2028; V3 trigger gate uses Launch Capacity R56 = 2027. **CRITICAL**: with bridge loan active, Available cash > $0 in 2025-2027 → MIN bind no longer starves modules → Starlink deployment 2026+ should be non-zero (vs V2.14.5 collapse to 0).
3. **§3.7** — Retire Starlink R43 ratchet flag + Assumptions R320 V2 DTC permanent cap (clear values + retirement-note labels)
4. **§3.8** — Customer Launch + ODC + AI Stack R205 deployment binding
5. **§3.9** — Launch Capacity Starship endogenous fleet wiring (R8/R9 replicate; R25 = f(R150 Vehicle build claim); R33/R34 endogenous)
6. **§3.10** — F9 label-only update (Decision A; mostly skip per Sprint 11a finding)
7. **§3.11** — LM BV depreciation REMOVED from Group D&A (Group P&L R28 + R36 amendments; new Lunar Mars R120 Module D&A row; LM R117/R118 col A retirement labels)
8. **§3.12** — ODC audit (read-only documentation)
9. **§3.13** — Customer Launch R210 Capacity Demand wire

Reference Sprint_11_Spec.md sections for full formula details.

---

## §4 Verification

### §4.1 Workbook-wide error scan
Zero `#REF!` / `#VALUE!` / `#DIV/0!` / `#NAME?` / `#N/A` across all 15 tabs.

### §4.2 Conservation
Group P&L R108 = "OK" all 26 years 2025-2050. R109 = 0 ±$1M all years.

### §4.3 Bridge loan calibration

| Check | Expected | Halt if |
|---|---|---|
| Allocator D11 Bridge loan 2025 | $20,000M | ≠ $20,000M |
| Allocator E11 Bridge loan 2026 | $0 | ≠ $0 |
| Allocator D15 Cash BoY 2025 | $25,000M | ≠ $25,000M |
| Allocator D29 Available cash 2025 | ~$13,346M | <$8B or >$18B |
| Allocator E29 Available cash 2026 | ~$6,000-8,000M | <$2B or >$15B |
| Allocator F29 Available cash 2027 (post-IPO) | ~$36B+ | <$25B |

### §4.4 Deployment trajectory (post §3.6)

| Cell | Expected | vs V2.14.5 collapsed |
|---|---|---|
| Starlink E33 V2 BB launches 2026 | non-zero (cash sufficient post-bridge) | 0 (V2.14.5) → fixed |
| Starlink F39 V3 BB launches 2027 | non-zero (V3 trigger + kg + cash) | 0 → fixed |
| Starlink G33 V2 BB launches 2028 | 0 (V2 phase-out gate) | 0 → unchanged |
| Starlink R98 Module CapEx I (2030) | ~$3,000-5,000M | unknown |

### §4.5 §3.11 LM BV correction calibration

| Cell | Expected post-§3.11 | vs V2.14 baseline |
|---|---|---|
| Group P&L AC28 Group D&A 2050 | ~$6,000M | $484,076M (baseline before fix) |
| Group P&L AC10 Group Revenue 2050 | $400-650B range | $583B baseline |
| Group P&L AC26 EBITDA 2050 | likely negative still (OpEx-revenue ratio issue) | -$44,521M |
| Lunar Mars D120 Module D&A 2025 | $0 or small | new row |
| Lunar Mars AC120 Module D&A 2050 | small ($100-500M range; proper cash-cap depreciation of cumulative carve-out CapEx) | NEW |

**Halt condition**: AC28 Group D&A > $20B → HALT (LM BV depreciation refs may not have been fully removed from R28/R36 formulas).

### §4.6 Group Revenue trajectory must NOT collapse

| Check | Expected | Halt threshold |
|---|---|---|
| Group P&L AC10 Group Revenue 2050 | > $300B (was $583B baseline) | <$200B → HALT (deployment binding may still be starving) |
| Group P&L I10 Group Revenue 2030 | > $80B | <$50B → HALT |
| Group P&L D10 Group Revenue 2025 | ~$13,855M | <$10B or >$17B |

This is the critical Sprint 11c success metric: bridge loan + deployment binding must produce a model that PRESERVES the revenue trajectory from V2.14-a1636d7f baseline, not collapse it like V2.14.5.

### §4.7 Round-trip stability + Rule 22 stale-ref scan

5x recalc; no value moves >$1M. Rule 22 scan enumerates new bridge loan refs + all Sprint 11 §3.5b-§3.13 cross-tab refs.

### §4.8 Claude Log entry

Append row 16 (after Sprint 11a row 14 + Sprint 11 Block 1 row 15):

| Date | Sprint | Tabs touched | Summary | Outstanding |
|---|---|---|---|---|
| 2026-MM-DD | 11c | Assumptions R351, Allocator R11/R15, Starlink R7-R14/R33-R41/R43, Customer Launch R205/R210, ODC R205, AI Stack R205, Launch Capacity R8-R9/R25/R34/R61, Group P&L R28/R36, Lunar Mars R117/R118/R120 | Sprint 11 recovery PASS: $20B Pre-IPO Bridge Loan (per S-1) unstarved cash pipeline → deployment binding viable → Starlink revenue trajectory preserved (AC10 ~$500B+ vs V2.14.5 collapse to $16B). LM BV correction landed (Group D&A 2050 $484B → ~$6B). V30.5 Lessons §2 + Architecture §6.5 deployment binding finally land end-to-end. | Bridge loan repayment mechanic (defer to Sprint 11.5); interest expense modeling (defer); Sprint 9 §6.8 calibration target revision (post-Sprint-11c); ODC unit-economics revision (Vlad-pending) |

---

## §5 Outstanding items

1. **Bridge loan repayment mechanic** — Sprint 11c models $20B inflow 2025 only; doesn't model repayment. Real-world: IPO 2027 refinances; bond proceeds repay bridge. Defer to Sprint 11.5 unless Vlad locks now.
2. **Bridge loan interest expense** — $20B at ~10%/yr = $2B/yr OpEx 2025-2027. Sprint 11c does not model this. Defer to Sprint 11.5.
3. **Sprint 9 §6.8 calibration revision** — Group D&A + FCF 2050 swing dramatically post-§3.11; new targets locked by Vlad post-Sprint-11c.
4. **ODC unit-economics revision** — Vlad-pending decision.
5. **R110 Σ Module FCF residual** — module-owner audit pending.
6. **AC_2050 EBITDA negativity** — Sprint 12 audit pending.

---

## §6 Amendment log

- **2026-05-26 (initial draft)** — Sprint 11c spec authored as recovery sprint after Sprint 11 Block 2 collapse. Triggered by Vlad surfacing S-1 disclosure of $20B bridge loan. Architecture §20.9 amended in parallel. Recovery path: restore V2.14-a1636d7f Block 1 PASS state, apply §3.1.5 bridge loan wiring first, then execute Sprint 11 §3.5b-§3.13 with non-starved cash pipeline.

---

## End of Sprint 11c Spec
