# Sprint 10.8 — Spectrum CapEx → Recurring License Fee Reclassification

**Status**: Spec draft, awaits fresh plugin chat execution
**Author**: Vlad lock 2026-05-26
**Predecessor**: Sprint 10.7 (deployment binding + vehicle-level allocator)
**Successor**: Sprint 11 (Valuation) — must land first if license-fee tail affects terminal value
**Related memory**: `project_spectrum_license_fee_amendment_2026_05_26.md`

---

## Rule Compliance Preamble (mandatory open)

Per modelling constitution `Model_Execution_Rules.md`:
- **Rule 1** (anchor-and-offset): all new year-row formulas use $D$X anchor + offset pattern, no neighbour-chasing
- **Rule 2** (multi-row writes): use `execute_office_js` for multi-row formula fills, not `set_cell_range copyToRange` with multi-row bounding boxes
- **Rule 12** (Allocator OUT contract): all cross-tab references INDEX/MATCH by canonical label, not row number
- **Rule 23** (Assumptions-write-then-reference footgun): if any new Assumptions row is written and immediately referenced cross-tab in the same plugin chat, save + fully quit Excel + reopen between writes and cross-tab reads, OR force `worksheet.calculate()` after Assumptions writes

Iterative calc must remain ON (100 iter / 0.001 tol) per `[[project_iterative_calc_enabled_2026_05_20]]`.

US English throughout per `[[feedback_mach33_us_english]]` (modelling, optimisation are wrong; modeling, optimization are right).

---

## §1 Background — what V2.16 currently does (deprecated)

| Year | Assumptions R267 (CapEx $mm) | CapEx R40 cumul. ($mm) | CapEx R41 amort ($mm) | Allocator R20 claim ($mm) |
|---|---|---|---|---|
| 2025 | 5,000 | 5,000 | 333 | 5,000 |
| 2026 | 8,000 | 13,000 | 867 | 8,000 |
| 2027 | 5,000 | 18,000 | 1,200 | 5,000 |
| 2028 | 2,000 | 20,000 | 1,333 | 2,000 |
| 2029+ | 0 | 20,000 | 1,333 | 0 |

**Problem**: Allocator R29 (Available cash for IRR queue) reads **$0 in 2025 + 2026** — entire cash pool consumed by OpEx claim + Spectrum claim + Taxes + Mars carve-out. No module receives IRR-queue cash. V2 BB / V2 DTC / Customer Launch all sit at proposed allocation $0 in those years regardless of IRR signal.

**Secondary bug**: Starlink R160 (Spectrum amortization BB-only) intended to charge BB-only amort into Starlink Module COGS, but label-match looks for "Annual Spectrum amortization ($mm/yr)" while CapEx tab label is "Annual spectrum amortization ($mm)" (capitalisation + suffix). Returns 0 every year. Spectrum amort sits only at Group level, not in Starlink Module EBITDA. Sprint 10.8 retires this row, side-stepping the bug.

---

## §2 New treatment — recurring license fee

**Cash schedule** (year-row, $mm/yr):
- 2025: 0
- 2026: 0
- 2027-2041: 1,333.33 (= $20B / 15yr, preserves nominal continuity with old amort)
- 2042-2050: 0 (license expires; renewal optional, flag as open thread)

**Classification**: Operating expense, BB-only, charged into Starlink Module COGS. Mirrors original BB-only intent (and restores the broken R160 wiring).

**P&L flow**:
- Hits **Starlink Module EBITDA** (not below as amort) — Starlink EBITDA drops by $1.33B/yr from 2027 onward vs. old treatment
- No intangible asset on balance sheet (license, not purchase)
- No D&A line (fully expensed each year)
- Group D&A row 28 drops by the spectrum amort component
- Group P&L R38 memo retires (or repurposes as "Memo: Spectrum license fee ($mm)")

**Allocator queue gate**: Spectrum CapEx claim R20 → 0 every year. License fee folds into OpEx claim R18 starting 2027 (via Starlink Module COGS feeding OpEx ↑ — verify whether OpEx claim R18 reads OpEx tab R53 directly or computes separately; if separately, add explicit license-fee line).

---

## §3 Cascade — what to edit, in order

### §3.1 Assumptions tab

**Edit A — zero existing CapEx schedule**:
- R267 (EchoStar mid-band CapEx ($mm) — year-row): D267:AC267 → all 0
- Keep label and row intact for diff-traceability; add comment "DEPRECATED 2026-05-26 — replaced by spectrum license fee row, see §13"

**Edit B — add license-fee block at end of Assumptions (use empty rows R352+ to avoid shifting row numbers; do NOT insert rows that move §11 Valuation rows)**:
- R352: `§13 SPECTRUM LICENSE FEE (Vlad amendment 2026-05-26)`
- R353: `▸ EchoStar mid-band — recurring license fee (supersedes R267)`
- R354: `Spectrum license fee start year` | B = 2027
- R355: `Spectrum license fee end year` | B = 2041
- R356: `Spectrum license fee ($mm/yr) — year-row` | D356:AC356 — anchor-and-offset pattern:
  - D356 (2025): =IF(AND(D$6>=$B$354, D$6<=$B$355), 20000/( $B$355 - $B$354 + 1), 0)
  - E356:AC356 copy across — same formula with relative year reference D$6 → E$6 etc.
  - Cross-check: 20000 / (2041 - 2027 + 1) = 20000 / 15 = 1,333.33; rows 2027-2041 should read 1,333.33; rows 2025-2026 and 2042-2050 should read 0.
- R357: `Spectrum license fee — total commitment ($mm) (memo)` | B = `=SUMPRODUCT(D356:AC356)` — should equal 20,000
- R358: `Spectrum license fee classification (memo)` | B = "Starlink BB COGS — BB-only, mirrors deprecated R160 intent"
- R359: `Spectrum useful life (years) — DEPRECATED 2026-05-26 (license, no amort)` — leave R268 as-is but add this deprecation memo

### §3.2 CapEx tab §3

- R39 (EchoStar mid-band CapEx) — formula already reads Assumptions R267 via INDEX/MATCH; will auto-flow to 0. No edit needed.
- R40 (Cumulative spectrum intangible) — will auto-flow to 0. No edit needed.
- R41 (Annual spectrum amortization) — will auto-flow to 0. No edit needed.
- R47 (Memo: Group D&A contribution = Corporate D&A + Spectrum amort) — will auto-update; spectrum component drops out cleanly.
- **Add R42 (or use existing empty row in §3)**: `Spectrum license fee ($mm) — for Group P&L tracking` — formula `=INDEX(Assumptions!$D:$AC, MATCH("Spectrum license fee ($mm/yr) — year-row", Assumptions!$A:$A, 0), D$5+1)` across D42:AC42. This gives downstream tabs a clean canonical reference.

### §3.3 Starlink tab

- R160 (Spectrum amortization BB-only) — retire. Replace with:
  - **New row R160**: `Spectrum license fee — BB-only ($mm)` | formula `=INDEX(CapEx!$D:$AC, MATCH("Spectrum license fee ($mm)", CapEx!$A:$A, 0), D$5+1)` across D160:AC160
  - Keep R160 in the COGS aggregator R152 stack — license fee now hits Starlink BB COGS as intended

### §3.4 OpEx tab

- **Question**: does OpEx claim R18 in Allocator read OpEx tab R53 (Total OpEx) directly, OR compute from a separate non-COGS bucket?
- If R53 already includes Starlink COGS, license fee flows automatically through Starlink R160 → Module COGS → Group OpEx. No OpEx tab edit needed.
- If R53 excludes module COGS (corporate OpEx only), add new line in §2 SG&A bucket: `Spectrum license fee — Starlink BB ($mm)` referencing CapEx R42. Sum into R50 Total SG&A → R53 Total OpEx.
- **Plugin to verify R53 composition before editing**.

### §3.5 Allocator tab

- R20 (Spectrum CapEx claim) — formula reads CapEx R39 which now reads 0 from Assumptions R267. Will auto-flow to 0. Verify no orphan references.
- R18 (OpEx claim) — verify it picks up the license fee via OpEx tab. If OpEx claim is computed separately from OpEx tab R53, add explicit reference to Spectrum license fee CapEx R42.
- R29 (Available cash for IRR queue) — recompute; should be substantially positive in 2025 + 2026 now (was $0).

### §3.6 Group P&L tab

- R28 (Group D&A) — formula was `Σ Module D&A in COGS + Lunar Mars BV dep + Corporate D&A + Spectrum amort`. Spectrum amort term goes to 0 via CapEx R41 → R47 cascade. No edit needed if formula reads R47.
- R38 (Memo: Spectrum amort) — repurpose to `Memo: Spectrum license fee ($mm)` referencing CapEx R42. Or retire entirely.
- R46 (Group CapEx note) — update comment text: "$5B EchoStar 2025 / $8B 2026 / $5B 2027 / $2B 2028" replaced with "Spectrum reclassed to OpEx license fee starting 2027 — see Assumptions §13".
- R103 conservation block — verify Group D&A = Σ components still balances after spectrum amort drops to 0.
- R110 (Group FCF residual diagnostic) — recompute; the $454M residual from Sprint 9 may shift.

---

## §4 Calibration targets — what changes

| Anchor | Old target | New target | Δ |
|---|---|---|---|
| 2025 Group FCF | -$2,569M | -$2,569M + $5,000M ≈ +$2,431M | +$5B (spectrum CapEx removed) |
| 2026 Group FCF | (compute from V2.16) | + $8,000M | +$8B |
| 2027 Group FCF | (compute) | + $5,000M − $1,333M = +$3,667M net | net +$3.67B |
| 2028 Group FCF | (compute) | + $2,000M − $1,333M = +$667M | +$667M |
| 2029+ Group FCF | (compute) | − $1,333M | -$1.33B/yr through 2041 |
| 2025 Group D&A | $1,261M (Sprint 9 exact) | $1,261M − $333M = $928M | -$333M (spectrum amort drops) |
| 2025 Total OpEx | $4,757M (Sprint 8 overshoot) | unchanged in 2025 ($0 license fee) | 0 |
| 2027 Total OpEx | (Sprint 8 number) | +$1,333M (license fee added to OpEx) | +$1.33B/yr 2027-2041 |
| 2025 Group EBITDA | (Sprint 9) | unchanged in 2025 | 0 |
| 2027 Group EBITDA | (Sprint 9) | -$1,333M/yr 2027-2041 (license now in OpEx, hits EBITDA) | -$1.33B/yr |

**Halt threshold**: Group FCF 2025 swing of +$5B should be sign-flipped from negative to positive — exactly what Vlad asked for ("not all spent immediately"). If post-execution 2025 Group FCF is not positive, investigate.

**Allocator R29 anchor**: Available cash for IRR queue 2025 should jump from $0 to ~$5,000M; 2026 should jump from $0 to ~$8,000M − OpEx + Mars carve-out delta. Verify before signing off.

---

## §5 Open threads (carry to Sprint 11 / later)

1. **License fee rate**: $1,333M/yr (nominal continuity) vs. annuity-equivalent at WACC (~$2.63B/yr, captures time-value-of-money of a 15-yr license vs. an upfront purchase). Default = nominal continuity; flag for Sprint 11 valuation discussion.
2. **Tail treatment 2042-2050**: $0 (default — license expires) vs. perpetual $1,333M/yr (renewal). Affects terminal value materially. Decide before Sprint 11 closes valuation.
3. **DTC allocation**: BB-only charge (default, preserves R160 original intent). If V3 DTC scales materially on mid-band, split BB/DTC proportional to subs or Hz used. Build with BB-only flag; leave split toggle as a future amendment.
4. **Deal-close year sensitivity**: Hardcoded 2027 default. R354 is Assumptions input (Spectrum license fee start year) so flexes by changing one cell. Document for Monte Carlo registration.
5. **Architecture §13.3 amendment**: rebuild architecture doc references the old CapEx treatment. Author a §13.3 amendment paragraph after Sprint 10.8 PASS.
6. **Starlink R160 label-bug retro**: log to lessons that label-match formulas should be unit-tested at build time, not assumed wired.

---

## §6 PASS criteria

1. Assumptions R267 D:AC = 0
2. Assumptions R356 reads 0 / 0 / 1,333.33 / 1,333.33 / ... / 1,333.33 / 0 / 0 ... in correct year cells
3. Assumptions R357 (total commitment memo) = 20,000 exactly
4. CapEx tab R39, R40, R41 all read 0 every year
5. CapEx tab R42 (new license fee tracker) matches Assumptions R356 every year
6. Starlink tab R160 reads license fee year-row (matches CapEx R42)
7. Allocator R20 = 0 every year
8. Allocator R29 (Available cash for IRR queue) > 0 in 2025 and 2026
9. Group P&L R28 (Group D&A) drops by old spectrum amort component every year (verifiable from CapEx R47)
10. Group P&L R103 conservation block stays "OK" every year
11. Group P&L R108 conservation block stays "OK" every year
12. 2025 Group FCF sign-flips from negative to positive
13. No #REF!, #N/A, #DIV/0! errors anywhere
14. Stale-ref scan clean (no formulas reference deprecated R267 schedule downstream of CapEx tab)

---

## §7 Plugin execution notes

- **Split into two passes** per `[[feedback_assumptions_write_then_reference_footgun]]`:
  - **Pass 1**: write Assumptions §13 rows (R352-R359). Save + fully quit Excel + reopen.
  - **Pass 2**: write CapEx R42, Starlink R160 rewire, Group P&L R38 repurpose, all cross-tab references. Save + reopen.
- **Iterative calc**: confirm ON pre-flight.
- **Diff-traceability**: leave deprecated R267 schedule row visible with comment, do not delete. Same for old Starlink R160 if repurposing — annotate.
- **No workbook names**: spec does not pin source/target file per `[[feedback_no_workbook_names_in_specs]]`.

---

End of spec.
