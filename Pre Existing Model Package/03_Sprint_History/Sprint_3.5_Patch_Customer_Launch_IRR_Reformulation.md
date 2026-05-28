# Sprint 3.5 — Customer Launch per-launch IRR cadence-multiplier removal

**Source workbook**: `SpaceX Model V2.5.xlsx` (Sprint 3 output PASS; pre-flight #1 waived in Sprint 3 — Vlad's session may show V2.4.xlsx; either is acceptable, plugin verifies Sprint 3 state by cell content not by filename)
**Target workbook**: `SpaceX Model V2.5.5.xlsx` (X.5 patch convention per Sprint Roadmap §4)
**Day budget**: 0.5 hours (~10-20 plugin operations)
**Date drafted**: 2026-05-20
**Patch trigger**: Sprint 3 PASS surfaced F9 per-launch Blended IRR 2025 = 3,272% — far above the §6.2 8-25% calibration target. Root cause analysis (Vlad + spec author chat 2026-05-20): the per-launch marginal IRR formula in Architecture §5.1 multiplies per-launch margin by cadence, implicitly assuming the marginal booster captures the full 12 launches/yr at customer pricing. In reality the global customer market is capped (~38 launches/yr); the marginal booster captures roughly 1 customer launch/yr (the rest go to Starlink internal at-cost which contributes zero margin). Cadence is the wrong multiplier. This patch drops the cadence multiplier from R131 (F9) + R141 (Starship) annual margin rows. Architecture §5.2 gets a one-line amendment noted in §9.

---

## §0 — Constitutional references

- **`01_Lessons_Learned.md`**: Principles 1 (lock load-bearing methodology early), 2 (per-launch marginal IRR must be allocator-useful — comparable across modules), 8 (vending-machine framing preserved — no corporate overhead added to IRR), 17 (delete superseded formulas in same spec — old cadence-multiplied formula superseded).
- **`02_Architecture_and_Methodology.md`**: §5.1 (per-unit IRR formula — CF[0] = -cost_per_unit, CF[1..N] = +net_marginal_revenue_per_unit), §5.2 (Customer Launch per-launch margin definition — being amended this patch), §5.4 (strict IRR > 0 cutoff unchanged), §7.1 (Customer Launch internal transfer pattern unchanged).
- **`03_Sprint_Roadmap_and_Verification.md`**: §4 patch sprint pattern (X.5 numbering, same Rule Compliance Preamble + verification gate as full sprints), §6.2 Sprint 3 calibration (per-launch Blended IRR target 8-25% — flagged for Sprint 3 Open Thread item 1 reconciliation; this patch brings IRR down toward target range but does NOT hit 8-25% — see §7).
- **`Model Execution Rules.md`**: Rules 1 / 4 / 9 / 10 / 12 / 14 / 17 / 19 / 22 / 23 load-bearing.
- **`Sprint_3_Spec.md`** §3.6.6 (per-launch IRR engine row map — R130-R134 F9 + R140-R144 Starship; this patch amends R131 + R141 only).
- **Sprint 3 exec log** (2026-05-20 plugin chat) — confirmed actual R131/R141 formulas + verified F9 Spot IRR 2025 = 3,443% (=R132 D), F9 Blended IRR 2025 = 3,272% (=R134 D), Starship Spot IRR 2027 = 65% (=F142), Starship Blended IRR ~0 in 2025 (D144) ~60% in 2027 (F144). This patch's expected outcome: F9 Blended IRR 2025 drops from 3,272% to ~280%, Starship 2027 IRR unchanged at ~65% (1 × $60M margin happened to match cadence × per-launch margin coincidentally).

---

## §1 — Rule Compliance Preamble (mandatory)

- [x] **Rule 1** (one concept per write) — two discrete formula rewrites (R131 + R141), each as a single `set_cell` operation. No mixing of labels + formulas + formats.
- [x] **Rule 3 / 23** (formula pattern) — N/A; this patch rewrites two single-cell-of-year-row formulas. Each replacement preserves the existing copyToRange D→E:AC pattern.
- [x] **Rule 4** (verification gate) — §4 enumerates explicit read-back cells at D / I / S / AC for R131, R141, R132, R134, R142, R144, plus Allocator OUT R207/R208/R209 (which recalc automatically).
- [x] **Rule 6** (inline formulas) — full Excel formulas inlined in §3 below.
- [x] **Rule 10** (no row insertions) — N/A; no new rows, only in-place formula replacement at existing row numbers.
- [x] **Rule 11** (touch points) — R131 + R141 are read only by R132/R142 (Spot IRR) and R133/R143 (Forward IRR). R132-R134 + R142-R144 are read only by Allocator OUT R207-R209 (revenue-weighted blend). Allocator OUT R207-R209 are read only by Sprint 10 (not yet fired). Touch points = 6 cells recalc downstream + Allocator OUT 3 cells × all year columns. Sprint 9 Group P&L conservation block does NOT read per-launch IRR rows. Sprint 11 Valuation reads Module FCF (R101) not IRR — unaffected by this patch.
- [x] **Rule 12** (label-based cross-tab refs) — N/A for this patch; the rewrites stay intra-tab on Customer Launch. Existing INDEX/MATCH calls in R131 + R141 to Assumptions + Launch Capacity preserved (just stripped of the cadence multiplier).
- [x] **Rule 13** (vending-machine test) — preserved. No R&D / SG&A / overhead / taxes added. The patch only removes a multiplier; doesn't add new cost categories.
- [x] **Rule 14** (no hardcoded constants) — preserved. New formulas reference Assumptions inputs by label (insurance %, other COGS %, etc.) exactly as Sprint 3 did. The dropped multiplier was an Assumptions read (`F9 cadence per booster` for R131, Launch Capacity R23 cadence year-row for R141) — these labels remain in the workbook on Assumptions / Launch Capacity, just no longer consumed by the IRR engine.
- [x] **Rule 15** (sanity halt) — §4.3 halt thresholds explicit. F9 Blended IRR 2025 post-patch outside [150%, 500%] = halt + Vlad review. Starship 2027 IRR outside [40%, 100%] = halt.
- [x] **Rule 17** (delete superseded) — the cadence multiplier portion of R131 + R141 formulas is REPLACED in-place (not deleted as separate cell). The `F9 cadence per booster` Assumptions row + Launch Capacity R23 cadence year-row stay in workbook unchanged — they remain canonical labels read by other modules (Launch Capacity R31/R32/R33 launches per year formula reads cadence). No row deletes this patch.
- [x] **Rule 19** (save-as) — target workbook `SpaceX Model V2.5.5.xlsx`. Vlad handles Save-As V2.5 → V2.5.5 before kickoff. Plugin operates on live session.
- [x] **Rule 22** (stale-ref scan) — post-patch §4.5 confirms: (a) R131 + R141 still resolve correctly, no #NAME? / #REF! errors; (b) R132/R142 IRR formulas still construct CF stream correctly with new annual margin rows; (c) Allocator OUT R207-R209 still revenue-weight per Sprint 3 spec §3.8 (formulas unchanged).

**Architecture & Methodology compliance:**

- [x] **Architecture §5.1 amendment for Customer Launch** — see §3.3 below + §9 amendment log. This patch makes the per-launch IRR formula for Customer Launch literally interpret "per unit" as "per customer launch contract" rather than "per booster-year operating at full cadence". The cost slug stays the booster/stack manufacturing cost (which represents the marginal capex to enable one more customer launch slot). The annual CF stays the per-launch contribution margin (which represents one marginal customer launch's economics). N = lifetime reuses clamped at R23 = 10 (Vlad lock #4 from Sprint 3 — unchanged). This is consistent across F9 + Starship and produces comparable IRRs in the 40-300% range.
- [x] **Architecture §5.2 amendment** — Customer Launch row's "per-sat/launch revenue per year" definition gets a one-line clarification: "for Customer Launch, the annual CF entry represents ONE marginal customer launch's contribution margin, NOT cadence × per-launch margin. Customer market saturation is the binding constraint; the marginal booster captures one marginal customer launch per year over its useful life." Other modules (Starlink per-sat, ODC per-sat, AI Stack per-product) are unaffected because their "unit" is genuinely orbiting/operating continuously (one sat = one year of bandwidth per year — no cadence multiplier issue).
- [x] **Sprint 4 Starlink per-sat IRR compatible** — Sprint 4 spec author + plugin should follow Architecture §5.2 as written (annual CF per sat = per-sat bandwidth × $/Gbps × util × per-year ÷ active sats — already per-year, no cadence multiplier issue). Sprint 3.5 precedent is Customer-Launch-specific. Sprint 5 ODC same.

If any box unticked or unjustified → spec author amends before plugin execution.

---

## §1.5 — Pre-execution setup (Vlad confirms before plugin starts writing)

**Vlad attests:**

1. **Target workbook is open** with name `SpaceX Model V2.5.5.xlsx` (Save-As completed from V2.5 → V2.5.5 before this kickoff). If your local session has Sprint 3 output still labeled V2.4 (per Sprint 3 pre-flight #1 waiver), accept the equivalent — plugin verifies Sprint 3 state by cell content (Customer Launch R130 = $30M F9 cost slug, R131 = current cadence-multiplied formula, R140 = year-row reading Launch Capacity R37, R141 = current cadence-multiplied formula).
2. **Vlad will handle all saves** — plugin operates on live open workbook session, does NOT issue save commands.
3. **Sprint 4 plugin chat has NOT yet started writing** — Sprint 3.5 must land before Sprint 4 plugin fires (Sprint 4 spec author can draft in parallel, but plugin execution is sequential). If Sprint 4 plugin is in flight against the same workbook, halt and reschedule.

If any of the above is not true, plugin halts at pre-flight per Rule 9 and pushes back to Vlad.

---

## §2 — Framing

**Why this patch.** Sprint 3 verification surfaced F9 per-launch Blended IRR 2025 = 3,272% — orders of magnitude above the Sprint Roadmap §6.2 target 8-25% range. Vlad flagged as not allocator-useful. Root cause: Architecture §5.1's per-unit IRR formula multiplies per-launch margin by full cadence (12/yr for F9), implicitly assuming the marginal booster captures 12 customer launches per year at full pricing. Reality: customer launch market is globally capped at ~38 launches/yr. Marginal booster captures ~1 customer launch/yr (other 11 go to Starlink internal at-cost — zero margin contribution).

**The fix.** Drop the cadence multiplier from Customer Launch's per-launch IRR annual margin rows (R131 F9 + R141 Starship). Annual CF stream entry = per-launch contribution margin (1 customer launch per marginal booster per year). Keeps Architecture §5.1 cost slug = vehicle manufacturing cost. Keeps N = lifetime reuses clamped at R23 = 10. Produces:

- **F9 2025 Blended IRR ~280%** (down from 3,272%) — large but bounded; reflects extreme F9 commercial pricing margin
- **Starship 2027 IRR ~65% (unchanged)** — happens to match because Sprint 2's Wright's Law cadence floor of 1 made cadence × margin = 1 × $60M coincidentally equal to no-cadence-multiplier × margin
- **All IRRs decline over time** as F9 customer price compresses (-3%/yr per Sprint 0 R63) and Starship margin multiplier compresses (4.0x → 1.5x per Sprint 3 Vlad lock #2)
- **F9 + Starship comparable** at any single point in time; allocator can meaningfully weight them

**What this patch does NOT do.**
- Does NOT amend Architecture §5.2 for other modules — Starlink/ODC/AI Stack per-sat IRR is genuinely continuous (sats orbit 365 days/yr), no cadence multiplier issue.
- Does NOT touch any other Customer Launch cells (R130 cost slug unchanged, R140 cost slug unchanged, R132/R133/R134/R142/R143/R144 IRR formulas unchanged — they recalc automatically).
- Does NOT touch Allocator OUT R207-R209 formulas — they recalc downstream.
- Does NOT touch Launch Capacity / Assumptions / any other tab — strictly Customer Launch R131 + R141.
- Does NOT reconcile §6.2 calibration target 8-25% — post-patch IRR still well above that range. The §6.2 target is a V30.5 fleet-level MFW-IRR holdover and remains incompatible with marginal per-launch IRR. Sprint Roadmap §6.2 needs amendment in a future spec author session (§7 Open Thread item 1).

**Dependencies.** Sprint 3 PASS (Customer Launch module body + Allocator OUT live). No new Assumptions inputs needed — the existing labels stay; only the formula formulation changes.

---

## §3 — Scope

### §3.0 Pre-flight (plugin verifies BEFORE any cell write)

Plugin halts on any failure and pushes back to Vlad.

1. **Workbook name** = `SpaceX Model V2.5.5.xlsx` OR Vlad's equivalent post-Sprint-3 file (e.g., V2.4 if pre-flight #1 waived in Sprint 3). Plugin reads the workbook name and reports it; if it doesn't match V2.5.5, Vlad confirms equivalence explicitly per Sprint 3 waiver precedent.
2. **Customer Launch tab exists** with sheet position #4. Halt if missing or wrong position.
3. **Customer Launch R130** reads `=INDEX(Assumptions!$B:$B, MATCH("F9 booster (1st stage) mfg cost ($mm/unit)", Assumptions!$A:$A, 0))` evaluating to $30M. If R130 = `#N/A` or different value, halt — Sprint 3 cost slug not landed correctly.
4. **Customer Launch R131** currently reads the Sprint 3 cadence-multiplied formula (contains `MATCH("F9 cadence per booster (flights/year, flat)"`). Plugin reads R131 formula text via Office.js + confirms substring match `"F9 cadence per booster"`. Halt if R131 doesn't contain the cadence-multiplier reference — means Sprint 3 didn't land R131 as spec'd OR a prior patch already touched it.
5. **Customer Launch R141** currently reads the Sprint 3 cadence-multiplied formula (contains `MATCH("Launches per Starship vehicle per year (cadence)"`). Same substring check. Halt if missing.
6. **Customer Launch R132 (F9 Spot IRR)** evaluates to a large positive number (>500%) in column D. Plugin reads D132 numeric value and confirms > 5. Halt if D132 < 5 or `#NUM!`/`#DIV/0!` — Sprint 3 IRR engine not landed correctly.
7. **Customer Launch R142 (Starship Spot IRR)** evaluates correctly at F142 (column F = 2027) > 0.3 (i.e., > 30%). Plugin reads F142 and confirms. Halt if F142 < 0.3 or error — Sprint 3 Starship IRR not landed.
8. **Allocator OUT R207-R209** populated (Sprint 3 §3.8 overwrite of Sprint 1 placeholders). Plugin reads R207 column A label = "Spot IRR" (or equivalent canonical label per Architecture §4.2). Halt if labels don't match.
9. **No Sprint 4 writes in flight** — plugin reads Starlink tab rows 11-199 and confirms blank (= Sprint 4 plugin has not started). If Starlink rows 11-199 have content, halt — Sprint 4 must complete before this patch, or this patch must complete before Sprint 4 starts (sequential not parallel for the same workbook).

All 9 pre-flight checks must pass. If any fail, halt and push back.

### §3.1 Patch operation 1 — Customer Launch R131 (F9 annual margin) formula replacement

**Current Sprint 3 formula (R131):**

```
D131 = =INDEX(Assumptions!$B:$B, MATCH("F9 cadence per booster (flights/year, flat)", Assumptions!$A:$A, 0))
       * (D17 - D34 - D37)
```

Where:
- `INDEX(... MATCH("F9 cadence per booster (flights/year, flat)"))` = 12 (Sprint 0 R51)
- D17 = F9 customer launch price ($111M anchor year-row)
- D34 = F9 variable cost per launch ($13.75M from Launch Capacity R69)
- D37 = F9 per-launch insurance + other COGS ($mm/launch)

Annual CF per booster = 12 × ($111M − $13.75M − $2.22M) = 12 × $95M ≈ $1,140M (the source of the absurd IRR).

**New patch formula (R131):**

```
A131 unchanged: "F9 per-launch annual margin ($mm/yr — cadence × per-launch margin)"
   [Note: column A label retains "cadence × per-launch margin" wording for Sprint 3 traceability;
    will be updated to "per-launch contribution margin" in a future cleanup. Plugin does NOT
    rewrite the label this patch per Principle 7 (no renames mid-build) + Rule 17 (label-vs-formula
    consistency policed by spec, not by row-label.)]

D131 = =D17 - D34 - D37
   (Reads: F9 customer price − variable cost per launch − insurance/other per launch.
    NO cadence multiplier. Represents the contribution margin of ONE marginal customer launch.)

copyToRange source D131, destination E131:AC131
```

Expected post-patch values:
- D131 2025 = $111M − $13.75M − $2.22M ≈ **$95M** (was $1,140M)
- I131 2030 = $95.4M − $13.75M − ~$1.9M ≈ **$79.75M** (price declines -3%/yr)
- S131 2040 = $70.7M − $13.75M − ~$1.4M ≈ **$55.55M**
- AC131 2050 = $52.4M − $13.75M − ~$1.0M ≈ **$37.65M**

Note: D37 (per-launch insurance+other) is itself computed as `(D33/D25) × (insurance% + other%)` = per-launch revenue × combined rate ≈ 2% of price. Plugin doesn't touch D37 — it auto-recalcs as D33/D25 don't change.

### §3.2 Patch operation 2 — Customer Launch R141 (Starship annual margin) formula replacement

**Current Sprint 3 formula (R141):**

```
D141 = =INDEX('Launch Capacity'!$D:$AC, MATCH("Launches per Starship vehicle per year (cadence)", 'Launch Capacity'!$A:$A, 0), D$5+1)
       * (D18 - INDEX('Launch Capacity'!$D:$AC, MATCH("Starship ops + fuel + refurb cost per launch ($mm, this year)", 'Launch Capacity'!$A:$A, 0), D$5+1) - IFERROR(D48 / D24, 0) * (INDEX(Assumptions!$B:$B, MATCH("Customer Launch insurance % of revenue", Assumptions!$A:$A, 0)) + INDEX(Assumptions!$B:$B, MATCH("Customer Launch other COGS % of revenue", Assumptions!$A:$A, 0))))
```

Where:
- `INDEX(...MATCH("Launches per Starship vehicle per year (cadence)"))` = Launch Capacity R23 cadence year-row (= 1 throughout Sprint 3 because cum upmass = 0)
- D18 = Starship customer launch price (= margin × Launch Capacity R40 at-cost)
- Launch Capacity R38 = Starship ops + fuel + refurb per launch ($12M anchor at cum=4)
- `IFERROR(D48 / D24, 0) × (insurance% + other%)` = per-launch insurance+other on Starship side

Annual CF per Starship stack in 2025 = 0 × ($0 - $12M - $0) = $0 (multiplier zero because D18 = 0).
In 2027: 1 × ($78M - $12M - ~$0.85M) ≈ $65M (cadence happens to be 1 → no difference vs no-multiplier).

**New patch formula (R141):**

```
A141 unchanged: "Starship per-launch annual margin ($mm/yr — cadence × per-launch margin)"
   [Label retained per Principle 7; column A wording cleanup deferred.]

D141 = =D18 - INDEX('Launch Capacity'!$D:$AC, MATCH("Starship ops + fuel + refurb cost per launch ($mm, this year)", 'Launch Capacity'!$A:$A, 0), D$5+1) - IFERROR(D48 / D24, 0) * (INDEX(Assumptions!$B:$B, MATCH("Customer Launch insurance % of revenue", Assumptions!$A:$A, 0)) + INDEX(Assumptions!$B:$B, MATCH("Customer Launch other COGS % of revenue", Assumptions!$A:$A, 0)))
   (Reads: Starship customer price − ops+fuel+refurb per launch − insurance/other per launch.
    NO cadence multiplier. Represents the contribution margin of ONE marginal customer launch.)

copyToRange source D141, destination E141:AC141
```

Expected post-patch values:
- D141 2025 = $0 − $12M − $0 = **−$12M** (Starship pre-commercial; margin negative; IRR engine R142 IFERROR will catch and return -100% or 0)
- E141 2026 = $0 − $12M − $0 = **−$12M** (same; pre-commercial 2026)
- F141 2027 = $78M − $12M − ~$0.85M = **$65.15M** (was $65M with cadence=1 multiplier; effectively unchanged)
- I141 2030 = (margin × Launch Capacity at-cost) − ops − insurance ≈ $52.3M − $12M − ~$0.55M = **$39.75M**
- S141 2040 = $30.1M − $12M − ~$0.3M = **$17.8M** (margin compressing)
- AC141 2050 = $20.6M − $12M − ~$0.2M = **$8.4M** (terminal margin)

### §3.3 Architecture §5.2 amendment (documentation-only — plugin does NOT edit constitutional doc)

Per Vlad's instruction + Standing Process Rule 5 (plugin doesn't edit constitutional MDs), this patch records the Architecture §5.2 amendment text here for Vlad to integrate manually into `02_Architecture_and_Methodology.md` via spec author chat post-patch. Plugin does NOT write to the constitutional doc.

**Proposed amendment to Architecture §5.2 (Customer Launch row of the per-launch IRR table):**

> | Module | net_marginal_revenue_per_unit per year |
> |---|---|
> | Customer Launch (per launch — external customer launches only) | = (Customer Launch external price per launch) − (variable cost per launch) − (insurance + other COGS per launch). **NOT multiplied by cadence per booster.** The marginal booster captures one marginal customer launch per year because the global customer market is the binding constraint (~38 launches/yr globally vs >400 launches/yr F9 fleet capacity). Per-launch IRR represents marginal economics of one more customer launch contract over the booster's useful life (N = lifetime reuses clamped at R23 = 10). Locked 2026-05-20 (Sprint 3.5 patch). Other modules unaffected — sats/products genuinely operate continuously without cadence-multiplier ambiguity. |

Amendment log entry to add to §19:

> - **2026-05-20 (Sprint 3.5 patch)** — Amended §5.2 Customer Launch per-launch IRR row to drop cadence multiplier from annual CF formula. Root cause: Sprint 3 verification showed F9 per-launch Blended IRR 2025 = 3,272% because original formula assumed marginal booster runs full cadence at customer pricing; reality is customer market is binding constraint. Post-patch F9 IRR ≈ 280%, Starship 2027 IRR unchanged at ~65%. Sprint Roadmap §6.2 calibration target 8-25% still incompatible with marginal per-launch IRR even after this patch — separate amendment needed in next spec author session.

---

## §4 — Verification gate

### §4.1 Universal checks (per Sprint Roadmap §5)

1. **No formula errors workbook-wide** — count `#REF!` / `#VALUE!` / `#DIV/0!` / `#NAME?` / `#NUM!` / `#NULL!` / `#N/A` across all tabs. Expected: ZERO (except IFERROR-wrapped IRR helper cells).
2. **Conservation block ALL OK boolean** — Group P&L D108:AC108 still trivially OK at Sprint 3.5 stage (Sprint 9 owns full conservation; this patch doesn't touch P&L tabs).
3. **Edge-year reads** — §4.2 below.
4. **Round-trip stability** — recalc 5x, no value moves >$1M.
5. **Stale-ref scan** — §4.4 below.
6. **Sanity halt thresholds** — §4.3 below.
7. **Claude Log entry** — §5 template.

### §4.2 Sprint 3.5 calibration read-back (D / I / S / AC)

Plugin reads these cells and reports actual vs expected. Tolerance ±5% on continuous values, exact on integer-count cells.

| Cell | Label | Pre-patch (Sprint 3) | Expected post-patch | Tolerance |
|---|---|---|---|---|
| Customer Launch D131 | F9 per-launch annual margin | $1,140M | $95M | ±5% |
| Customer Launch I131 | F9 annual margin 2030 | ~$876M | $79.75M | ±5% |
| Customer Launch S131 | F9 annual margin 2040 | ~$629M | $55.55M | ±5% |
| Customer Launch AC131 | F9 annual margin 2050 | ~$359M | $37.65M | ±5% |
| Customer Launch D132 | F9 Spot IRR 2025 | 3,443% | ~310% | ±50% wide tolerance (IRR sensitive to N + margin precision) |
| Customer Launch D134 | F9 Blended IRR 2025 | 3,272% | ~280% | ±50% wide |
| Customer Launch I134 | F9 Blended IRR 2030 | ~2,713% | ~240% | ±50% wide |
| Customer Launch AC134 | F9 Blended IRR 2050 | ~372% | ~100% | ±50% wide |
| Customer Launch D141 | Starship annual margin 2025 | $0 | −$12M | exact within ±$1M |
| Customer Launch F141 | Starship annual margin 2027 | ~$65M | ~$65M (unchanged — cadence was 1) | ±10% |
| Customer Launch I141 | Starship annual margin 2030 | ~$60M | ~$40M | ±15% |
| Customer Launch AC141 | Starship annual margin 2050 | ~$10M | ~$8.4M | ±20% |
| Customer Launch D142 | Starship Spot IRR 2025 | 0 (or -100%) | 0 or -100% (negative margin) | n/a |
| Customer Launch F142 | Starship Spot IRR 2027 | 65% | ~64% | ±10% (effectively unchanged) |
| Customer Launch F144 | Starship Blended IRR 2027 | ~60% | ~60% | ±10% |
| Customer Launch AC144 | Starship Blended IRR 2050 | ~0 (margin compresses) | ~85% | wide — terminal margin / terminal cost ratio dominates |
| Allocator OUT R207 D | Spot IRR (revenue-weighted) | 3,443% | ~310% (= D132 since Starship = 0 in 2025) | ±50% |
| Allocator OUT R209 D | Blended IRR (revenue-weighted) | 3,272% | ~280% | ±50% |
| Allocator OUT R209 F | Blended IRR 2027 (revenue-weighted) | varies | varies — depends on F revenue mix (F9 + Starship customer) | informational |

### §4.3 Sanity halt thresholds (per Rule 15)

- F9 Blended IRR 2025 (D134) outside **[150%, 500%]** → halt + Vlad review. Center 280%, wide band reflects IRR sensitivity to N + margin precision.
- F9 Blended IRR 2050 (AC134) outside **[50%, 200%]** → halt.
- Starship Blended IRR 2027 (F144) outside **[40%, 90%]** → halt.
- F9 annual margin 2025 (D131) outside **[$85M, $105M]** → halt (sanity on contribution margin formula).
- Starship annual margin 2025 (D141) outside **[−$15M, −$10M]** → halt (Starship pre-commercial; margin should be slightly negative due to ops+fuel+refurb anchor with zero price).
- Any `#NUM!` / `#DIV/0!` / `#REF!` on Customer Launch R131, R141, R132-R134, R142-R144, Allocator OUT R207-R209 → halt.
- F9 annual margin column AC (R131 in 2050) > F9 annual margin column D (2025) → halt — F9 customer price decays -3%/yr so margin should be lower in 2050 than 2025; if not, the price-decay year-row read broke.
- Customer Launch tab any cell outside R131 or R141 changed from Sprint 3 pre-patch state → halt + push back. Plugin samples 10 random cells outside R131 / R141 / R132-R134 / R142-R144 / R207-R209 / R210 (recalc-driven) and confirms unchanged values.

### §4.4 Stale-ref scan (per Rule 22)

1. **R131 + R141 still reference correct sources by label.** Plugin reads R131 + R141 formula text and confirms substrings: R131 has `D17` + `D34` + `D37` (intra-tab refs); R141 has `D18` + `INDEX('Launch Capacity'!...MATCH("Starship ops + fuel + refurb cost per launch ($mm, this year)"...` + `IFERROR(D48 / D24...` + `MATCH("Customer Launch insurance % of revenue"...` + `MATCH("Customer Launch other COGS % of revenue"...`. Halt if any expected substring missing.
2. **R132/R142 IRR formulas unchanged.** Plugin reads R132 + R142 formula text and confirms each still contains `IRR(IF(_xlfn.SEQUENCE(1, ...)=1, -D130, D131))` or `=IFERROR(IRR(IF(_xlfn.SEQUENCE(1, D121+1)=1, -D140, D141)), -1)` respectively. Halt if changed.
3. **Allocator OUT R207-R209 still reference revenue-weighted blend per Sprint 3 spec §3.8.** Plugin reads R207 + R208 + R209 formulas and confirms each contains `(D132 * D33 + D142 * D48) / (D33 + D48)` or equivalent shifted year refs. Halt if changed.
4. **No `F9 cadence per booster` Assumptions reference in R131.** Plugin reads R131 formula text and confirms substring `MATCH("F9 cadence per booster"` is NOT present. Halt if still present — formula replacement failed.
5. **No `Launches per Starship vehicle per year (cadence)` Launch Capacity reference in R141.** Plugin reads R141 formula text and confirms substring `MATCH("Launches per Starship vehicle per year (cadence)"` is NOT present. Halt if still present.
6. **`F9 cadence per booster` Assumptions row + Launch Capacity R23 cadence row still exist and unchanged.** Plugin reads both via MATCH; both should still resolve (other modules / Launch Capacity R31/R32/R33 launches per year formulas still consume cadence). Halt if either deleted or value changed.

### §4.5 Don't-touch verification

Plugin confirms NO writes outside:
- Customer Launch tab R131 + R141 (formula replacements at existing rows)
- Claude Log tab: ONE new row appended (§5)

Plugin reads pre-flight cell counts of each tab, re-reads post-execution; any tab other than Customer Launch + Claude Log showing a delta = halt + push back.

---

## §5 — Claude Log entry template

Plugin appends one row to the Claude Log tab on the workbook:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-MM-DD | 3.5 | Customer Launch (R131 + R141 formula replacements), Claude Log (append) | Patch sprint amending per-launch IRR annual margin formulas to drop cadence multiplier. Root cause: Sprint 3 verification surfaced F9 per-launch Blended IRR 2025 = 3,272% — far above §6.2 8-25% target. Original Architecture §5.1 formula multiplied per-launch margin by cadence (12/yr F9), implicitly assuming marginal booster captures 12 customer launches at full pricing. Reality: customer market binding constraint at ~38 launches/yr global; marginal booster captures ~1 customer launch/yr. Patch drops cadence multiplier: R131 = (D17 − D34 − D37); R141 = (D18 − LC R38 − per-launch ins/other). N unchanged at MIN(R23=10, lifetime reuses) per Vlad lock #4. Post-patch: F9 Blended IRR 2025 = ~280% (down from 3,272%); Starship 2027 IRR = ~65% (unchanged — cadence was already 1 due to Sprint 2 Wright's Law cum-upmass floor); both IRRs decline over time as margins compress; F9 + Starship now comparable + allocator-useful. Allocator OUT R207-R209 recalc automatically downstream. | (a) Sprint Roadmap §6.2 target 8-25% per-launch Blended IRR still incompatible with marginal per-launch IRR even after this patch — Sprint Roadmap needs amendment in next spec author session (recommended: "F9 Blended IRR 2025 in range 200-500%; Starship 2027 IRR in 40-90% range; halt only outside those bands"). (b) Architecture §5.2 Customer Launch row needs documentation amendment per Sprint 3.5 spec §3.3 (plugin does NOT edit constitutional MDs — Vlad integrates manually). (c) Sprint 4 Starlink per-sat IRR + Sprint 5 ODC per-sat IRR + Sprint 6 AI Stack per-product IRR are NOT affected by this patch — those modules' "unit" is genuinely continuous (sats orbit 365 days/yr; AI products run continuously); cadence multiplier issue is Customer-Launch-specific. Sprint 4/5/6 spec authors implement per-sat IRR per Architecture §5.2 as written. (d) Customer Launch R131/R141 column A labels still read "cadence × per-launch margin" — Principle 7 (no renames mid-build) preserved; label cleanup deferred to Sprint 9 audit. | Sprint 4 — Starlink module + Starlink Capacity tab |

---

## §6 — Don't touch (out of scope)

Sprint 3.5 writes ONLY to:
- Customer Launch tab R131 + R141 (two formula replacements at existing row positions; labels at column A unchanged)
- Claude Log tab (one new row appended)

Sprint 3.5 does NOT touch:
- Any Assumptions tab row (no new inputs needed; cadence row R51 stays for Launch Capacity to consume)
- Launch Capacity tab any row (cadence year-row R23 stays for R31/R32/R33 launches formulas + other Launch Capacity internal uses)
- Customer Launch any row other than R131 + R141 (R130/R132/R133/R134/R140/R142/R143/R144 stay; recalc automatically with new R131/R141)
- Allocator OUT block (recalcs automatically)
- All other tabs (Starlink, Starlink Capacity, ODC, AI Stack, Lunar Mars, OpEx, CapEx, Valuation, Group P&L, Demand Curves) — zero writes
- Constitutional MDs (Architecture §5.2 amendment recorded in §3.3 + §9 for Vlad to integrate manually)
- Any save / save-as / file-write operation

If the plugin discovers a need to write outside the above scope, HALT per Rule 9.

---

## §7 — Open thread (post-Sprint 3.5 considerations)

1. **Sprint Roadmap §6.2 target 8-25% per-launch Blended IRR — needs amendment.** Even after this patch, F9 IRR ~280% and Starship 2027 IRR ~65% are well above the §6.2 8-25% target. That target reflects V30.5 fleet-level MFW-IRR with corporate overhead deducted — incompatible with Architecture §5's per-launch marginal IRR by design. Vlad should amend §6.2 in next spec author session: recommended new target = "F9 Blended IRR 2025: 200-500%; Starship 2027 IRR: 40-90%; both decline over time as margins compress; halt only outside those bands." This preserves §6.2's role as a calibration check (catches IRR engine bugs) without insisting on V30.5-era magnitudes.

2. **Architecture §5.2 documentation amendment.** Per §3.3 above, Architecture §5.2 Customer Launch row needs a one-line clarification that annual CF is per-launch contribution margin (NOT cadence × margin). Vlad integrates manually in spec author chat.

3. **Sprint 4/5/6 IRR engines unaffected.** Per-sat IRR (Starlink V2/V3 BB/DTC, ODC) and per-product IRR (AI Stack) don't have the cadence-multiplier issue because their "unit" is continuously operating (one sat = 1 year of bandwidth per year — no cadence multiplier). Sprint 4 spec author confirms this in §3 framing.

4. **Customer Launch R131/R141 column A label cleanup.** Labels still read "cadence × per-launch margin" — descriptively wrong post-patch. Principle 7 (no renames mid-build) preserved; cleanup deferred to Sprint 9 audit when label rationalization can happen safely across the workbook.

5. **Starship Blended IRR 2050 = ~85%.** Higher than 2027 (~64%) because manufacturing cost drops faster (Wright's Law) than margin compresses (4.0x → 1.5x multiplier). This is a real economic dynamic — Starship at full industrial scale is highly profitable per marginal launch. Sprint 11 Valuation will pick this up as a positive sensitivity to Starship cum-upmass growth (which itself depends on Sprint 10 vehicle build claim sizing). Flag for Sprint 11 spec author.

6. **F9 cost slug $30M unchanged.** F9 booster mfg cost (Sprint 0 R44 = $30M, base year) doesn't decline over time in current Sprint 0 inputs (no Wright's Law on F9 since it's mature). So F9 IRR declines purely from price compression (-3%/yr). If Sprint 11 Valuation needs a richer F9 cost trajectory (e.g., manufacturing efficiency gains), Sprint 0 spec amendment.

---

## §8 — Execution sequence (plugin order of operations)

Plugin executes in this fixed order. Each block is one or more discrete tool calls per Rule 1.

1. **Pre-flight (§3.0)** — verify all 9 checks. Halt on any failure.
2. **Patch operation 1 — R131 formula replacement (§3.1).** Single `set_cell` write to D131 with new formula. Then `copyToRange` source D131 destination E131:AC131. Confirm via read-back: D131, I131, S131, AC131 numeric values.
3. **Patch operation 2 — R141 formula replacement (§3.2).** Single `set_cell` write to D141 with new formula. Then `copyToRange` source D141 destination E141:AC141. Confirm via read-back: D141, F141, I141, AC141 numeric values.
4. **Trigger full workbook recalc** to propagate R131/R141 changes through R132-R134 (F9 IRR) and R142-R144 (Starship IRR) and Allocator OUT R207-R209.
5. **VERIFICATION GATE — calibration read-back (§4.2).** Read all cells in §4.2 table; confirm against expected values within tolerance. Halt on any variance per §4.3.
6. **§4.1 universal checks** — workbook-wide error scan, stale-ref scan §4.4, round-trip stability test (5x recalc, no value moves >$1M).
7. **§4.5 don't-touch verification** — confirm no writes outside Customer Launch R131 + R141 + Claude Log.
8. **§5 Claude Log entry** — append one row.
9. **Sprint 3.5 complete declaration** — push back to spec author with all read-back values + PASS status + flag for Architecture §5.2 amendment + Sprint Roadmap §6.2 amendment per §7 Open Thread items 1 + 2.

Total estimated discrete writes: ~5-10 plugin operations. Day budget: 0.5 hours.

---

## §9 — Amendment log

- **2026-05-20 (initial draft)** — Sprint 3.5 patch spec drafted as Sprint 3 PASS exec log review surfaced F9 per-launch Blended IRR 2025 = 3,272% (orders of magnitude above §6.2 target). Vlad + spec author chat root-cause-analysis 2026-05-20: cadence multiplier in Architecture §5.1's per-unit IRR formula was the wrong assumption for Customer Launch (customer market is binding constraint, not booster capacity). Spec: drop cadence multiplier from R131 + R141 only. Post-patch expected: F9 Blended IRR 2025 ~280% (down 92%), Starship 2027 IRR ~65% (unchanged — cadence happened to be 1 in Sprint 3's pre-Sprint-10 state due to Wright's Law cum-upmass floor), F9 + Starship comparable + allocator-useful, both decline over time. Plugin operates on V2.5 live session, target V2.5.5; Vlad handles Save-As. Architecture §5.2 amendment recorded in §3.3 + this log entry for Vlad to integrate manually into constitutional doc (plugin does NOT edit MDs per Standing Process Rule 5).
