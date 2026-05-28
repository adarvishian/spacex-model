# Sprint 11f Spec — Deployment-Binding Architectural Rework (Decouple Demand from Output)

**Status**: Spec draft 2026-05-27. Pre-execution. Successor to Sprint 11d (collapsed by circular dep at zero attractor) and Sprint 11e (reduced sprint shipping the safe parts of Sprint 11). Methodology lock: **Option A — demand purely exogenous**.

**Predecessor sprints**: Sprint 10.8 (Spectrum license fee) + Sprint 11e (LM BV correction + Launch Capacity wiring + CL R210). 11f executes against a model state where both have already landed and the queue gate is unstarved in 2025-26.

**Architecture compliance**: §6.5 + §20.3 amendments included in §5.5 of this spec.

---

## §1 Background — what collapsed in Sprint 11d and why

The Allocator cash demand rows (Allocator R48 / R53 / R58 / R63 for V2 BB / V2 DTC / V3 BB / V3 DTC) read the *actual* Starlink module sat CapEx, which is itself downstream of cash. Closed ring:

```
Allocator R48 V2 BB cash demand
  ← reads Starlink R88 sat CapEx + R89 facility CapEx
  ← R88 = Starlink R33 launches × R78 unit cost
  ← R33 = MIN(Starlink R8 cash IN / R78, anchor × learning)
  ← R8 = Allocator R88 V2 BB cash allocation
  ← R88 = MIN(R50 proposed alloc, $D$29 × R49 weight / $D$80)
  ← R50 = MIN(IF(R47 IRR > 0, R48, 0), …)
  ← R48 ← (loop closed)
```

Two stable fixed points in Excel's iterative calc: the intended steady state, and zero. Zero won. Group Revenue 2050 collapsed $583B → $17B.

**Same ring repeats** for V2 DTC (R53), V3 BB (R58), V3 DTC (R63). Likely also for module-level cash demand on CL / ODC / AIS (R43 / R68 / R73 read module CapEx, which is downstream of module cash IN), though those have been masked because cash starvation in 2025-26 zeroed the queue gate anyway.

---

## §2 The fix — Option A locked: demand is purely exogenous

**Principle**: demand and output are different things.

| Quantity | Reads from | Recursion? |
|---|---|---|
| **Demand** (R48/R53/R58/R63 + module-level R43/R68/R73) | Anchor CapEx × learning × year-mask + exogenous facility CapEx | No |
| **Output** (Starlink R33 launches → R88 sat CapEx → R8 cash IN) | MIN(cash from allocator / unit cost, internal target) | Bounded by cash; no longer feeds demand |

Allocator reads demand + IRR → ranks → assigns cash. Cash drives output. Output never feeds back into demand.

**Why A and not B (capacity-capped demand) or C (vehicle-specific hybrid)**:
- Vending-machine framing already says modules surface full-IRR demand; cash is the Group-level constraint
- Capacity caps belong on output (R33 internal_target), not on demand
- B and C reintroduce recursion risk if done sloppily; A is provably non-recursive
- B and C are refinements; A is the structural fix

If you ever want capacity-bounded demand, that's a future architectural refinement on the output side — not the fix for the circular dep we just hit.

---

## §3 Rule Compliance Preamble

- [x] Rule 1 — separate writes per concept
- [x] Rule 3/23 — anchor-and-offset; all new year-row formulas use $D$X anchor + offset
- [x] Rule 4 — D/I/S/AC read-backs per section
- [x] Rule 6 — full Excel formulas inline
- [x] Rule 10 — no row insertions; in-place formula REPLACE only
- [x] Rule 11 — touch points enumerated in §5
- [x] Rule 12 — INDEX/MATCH by canonical label
- [x] Rule 14 — no hardcoded constants; all inputs resolve to Assumptions or canonical labels
- [x] Rule 15 — halt thresholds in §6
- [x] Rule 19 — Vlad handles saving
- [x] Rule 22 — stale-ref scan in §6.4

**Calc-engine sanity protocol** (per `feedback_assumptions_write_then_reference_footgun`): if any new Assumptions row is added, save + fully quit Excel + reopen before referencing cross-tab. Mitigation built into §5.0.

US English throughout (modeling, optimization — not modelling, optimisation).

Iterative calc must remain ON. Plugin verifies in §5.0.

---

## §4 Scope

| Section | What ships | Tabs touched |
|---|---|---|
| §5.0 Pre-flight | Calc engine probe + baseline state probes | read-only |
| §5.1 Allocator cash demand rewrite | R48 / R53 / R58 / R63 (Starlink V2 BB / V2 DTC / V3 BB / V3 DTC) | Allocator R48/R53/R58/R63 |
| §5.2 Allocator cash allocation rewrite | R88 / R89 / R90 / R91 (Starlink V2 BB / V2 DTC / V3 BB / V3 DTC cash allocation) read R50/R55/R60/R65 proposed allocation, not Starlink sat CapEx | Allocator R88/R89/R90/R91 |
| §5.3 Module-level deployment binding cleanup | R43 (CL) / R68 (ODC) / R73 (AIS) demand rows — verify pattern; rewrite if same circular shape | Allocator R43/R68/R73 |
| §5.4 Retire stale flags | Assumptions R320 (V2 DTC permanent cap — already labeled RETIRED but verify zero downstream refs) | Assumptions R320, Starlink R43 |
| §5.5 Architecture amendments | §6.5 deployment binding requirement + §20.3 amendment block | docs only |

5 meaningful sections, ~2-3 tabs touched. Well within sprint-sizing convention §10.1 (target 3-5 sections).

---

## §5 Execution

### §5.0 Pre-flight (READ-ONLY — halt if any check fails)

**Calc engine sanity probe** (mandatory per Roadmap §10.3):
- Write `=Assumptions!$A$2` to scratch cell Allocator!Z200
- Force `calculate(full)` + `context.sync()`
- Read scratch cell value
- Expected: Assumptions!A2 text
- If 0 or empty → calc engine corrupted; HALT, demand quit+reopen
- Clear scratch cell

**Baseline state probes** (post-Sprint-10.8 + post-Sprint-11e state expected):

```
Assumptions B350 = 2028 (V2 phase-out year)
Assumptions B351 = 20000 (Pre-IPO bridge loan)
Allocator A88 = "Starlink V2 BB cash allocation"
Allocator A48 = "Starlink V2 BB cash demand ($mm)"
Allocator D29 Available cash 2025 > $10B (post-spectrum-fix; was $0 in collapsed state)
Group P&L AC10 Group Revenue 2050 ≥ $400B (post-11e; was $16.5B in collapsed state)
Group P&L AC28 Group D&A 2050 < $20B (post-11e LM BV correction; was $484B baseline)
Group P&L R108 conservation = "OK" all years 2025-2050
```

**HALT** if any probe fails. If Group P&L AC10 < $400B → Sprint 11e didn't fully PASS; do not proceed with 11f.

**Probe the circular dep state** to confirm it still exists (or has been rolled back):

```
Allocator D48 formula contains "V2 BB sat CapEx"  → loop is wired (proceed with rewrite)
Allocator D88 formula contains "V2 BB sat CapEx"  → loop is wired here too
```

If formulas already read the exogenous demand pattern (anchor × learning) → rewrite already happened; verify §5.2 alloc rewrite still needed and proceed accordingly.

---

### §5.1 Allocator cash demand rewrite — R48 / R53 / R58 / R63

**Rewrite Allocator D48** (Starlink V2 BB cash demand) to read exogenous demand target, NOT Starlink R88 sat CapEx:

```
D48: =IF(D$4 >= INDEX(Assumptions!$B:$B, MATCH("V2 phase-out year (no V2 BB / V2 DTC launches from this year)", Assumptions!$A:$A, 0)), 0,
        INDEX(Starlink!$D:$AC, MATCH("V2 BB launches per year", Starlink!$A:$A, 0), 1)
        × (1 + INDEX(Assumptions!$B:$B, MATCH("Satellite cost per kg — learning rate", Assumptions!$A:$A, 0)))^D$5
        × INDEX(Starlink!$D:$AC, MATCH("V2 BB sat unit cost ($mm/sat)", Starlink!$A:$A, 0), D$5+1)
        + INDEX(Starlink!$D:$AC, MATCH("V2 BB facility CapEx per sat ($mm/sat)", Starlink!$A:$A, 0), D$5+1)
        × INDEX(Starlink!$D:$AC, MATCH("V2 BB launches per year", Starlink!$A:$A, 0), 1)
        × (1 + INDEX(Assumptions!$B:$B, MATCH("Satellite cost per kg — learning rate", Assumptions!$A:$A, 0)))^D$5)
```

**Key**: the formula reads `Starlink!"V2 BB launches per year"` at **column 1** (D=2025 anchor only), then applies the launches-anchor × learning rate × current-year unit cost. **Never reads the year-row launches** (which would be cash-bound). The anchor is the 2025 input from Assumptions.

Autofill D48 → E48:AC48. The `$D$5+1` shifts year offset for unit cost lookup; the anchor stays at column 1.

**Apply the same pattern to**:
- **R53 V2 DTC cash demand**: anchor = `Starlink!"V2 DTC launches per year"` col 1; unit cost = `Starlink!"V2 DTC sat unit cost ($mm/sat)"`; facility CapEx per sat = `Starlink!"V2 DTC facility CapEx per sat ($mm/sat)"`; same V2 phase-out gate.
- **R58 V3 BB cash demand**: anchor = `Assumptions!"V3 BB launches per year stub trajectory"` (year-row, exogenous); unit cost = `Starlink!"V3 BB sat unit cost ($mm/sat)"`; facility CapEx per sat = `Starlink!"V3 BB facility CapEx per sat ($mm/sat)"`; V3 trigger year gate (replace V2 phase-out check with `IF(D$4 < V3_trigger, 0, ...)`).
- **R63 V3 DTC cash demand**: anchor = `Assumptions!"V3 DTC launches per year stub trajectory"`; unit cost = `Starlink!"V3 DTC sat unit cost ($mm/sat)"`; facility CapEx per sat = `Starlink!"V3 DTC facility CapEx per sat ($mm/sat)"`; V3 trigger year gate.

**Verification reads (post §5.1, pre §5.2)**:
- Allocator D48 V2 BB demand 2025: should equal Starlink D33 × D78 + Starlink D89 (since 2025 anchor × learning^0 = anchor). Sanity-check: ~$1,116M.
- Allocator AC48 V2 BB demand 2050: should equal 0 (V2 phase-out at 2028 → 2050 > 2028).
- Allocator I48 V2 BB demand 2030: > 0 if 2030 < V2 phase-out year, else 0.
- Allocator D108 = "OK" (conservation must hold; nothing else changed yet).

**Critical**: at this point Allocator R88 (cash allocation) still reads Starlink R88 sat CapEx. The loop is HALF broken — demand is exogenous, but output→allocation→cash IN→output still loops via the allocation row. Section §5.2 closes the other half.

---

### §5.2 Allocator cash allocation rewrite — R88 / R89 / R90 / R91

**Current Allocator D88** reads Starlink R88 sat CapEx + R89 facility CapEx with column index hardcoded to 1 (so E88+ would still read 2025 values — that's a separate bug masking until autofilled). The override $1,116M at D88 was a Block 1 first-year hardcode.

**Rewrite Allocator D88** (Starlink V2 BB cash allocation) to read R50 proposed allocation directly:

```
D88: =D50
```

Apply across E88:AC88 by autofill (since R50 is per-year, this trivially propagates).

**Same pattern for**:
- **R89 V2 DTC cash allocation** = R55 (V2 DTC proposed allocation)
- **R90 V3 BB cash allocation** = R60 (V3 BB proposed allocation)
- **R91 V3 DTC cash allocation** = R65 (V3 DTC proposed allocation)

This is the canonical "Allocator OUT contract" pattern (Rule 12): the canonical-label OUT row reads the proposed-allocation row, not the module's own CapEx.

**Verification reads**:
- Allocator D88 V2 BB allocation 2025 = D50 V2 BB proposed allocation. Both should ≈ $1,116M (no change from baseline numerically since D50 already computed correctly).
- Allocator E88 V2 BB allocation 2026: was previously stuck at 2025 value (column index 1 bug); now reflects E50. Should be > 0 if cash + IRR signal positive.
- Round-trip stability: 5x recalc, no value moves > $1M.
- Conservation: R108 = "OK" all years post §5.2.

**Critical halt**: if Group Revenue 2050 falls below $400B after §5.2 → the loop is breaking the wrong way; halt and investigate. Expected: Revenue stays at ~$583B (Sprint 11e baseline) ± 5% from the cleaner cash allocation mechanism.

---

### §5.3 Module-level deployment binding cleanup — R43 / R68 / R73

**Probe the existing formulas**:
- Allocator R43 Customer Launch cash demand: reads `Customer Launch!"Module CapEx ($mm)"` — likely circular if CL Module CapEx is downstream of cash IN
- Allocator R68 ODC cash demand: reads `ODC!"Module CapEx ($mm)"` — same risk
- Allocator R73 AI Stack cash demand: reads `'AI Stack'!"Module CapEx ($mm)"` — same risk

**If any module's CapEx is downstream of cash IN** (i.e., Customer Launch R205 / ODC R205 / AIS R205 depend on cash allocation from Allocator), the same circular pattern applies. Rewrite cash demand to read an exogenous target:

```
R43 (CL): demand = forward-looking customer launch contracted revenue × cost ratio (or Assumptions-defined target)
R68 (ODC): demand = ODC fleet build target × per-sat CapEx (year-row Assumptions input)
R73 (AIS): demand = AI Stack CapEx target (year-row Assumptions input)
```

**If the modules' R205 Module CapEx already reads exogenous inputs** (not cash IN), no rewrite needed — leave R43/R68/R73 unchanged. Document the verification in Claude Log.

Decision criterion at plugin execution time: probe the relevant Module CapEx formula. If it reads from a `cash IN` row that resolves back to Allocator → rewrite. Otherwise no-op.

**Lunar Mars deployment** stays on the strategic carve-out — no rewrite (LM module has no IRR queue entry; cash flows via R35 carve-out).

---

### §5.4 Retire stale flags

- **Starlink R43 V2/V3 ratchet flag**: already labeled RETIRED 2026-05-26 in V2.16. Verify no downstream formula references R43; if any, redirect to phase-out year (R350) + V3 trigger year. Plugin grep for `Starlink!$A$43` or `Starlink!$D$43` references across all 15 tabs.
- **Assumptions R320 V2 DTC permanent cap**: already labeled RETIRED. Verify no downstream refs. Plugin grep.

If grep finds zero references → leave as-is (label retains as audit trail). If grep finds active references → redirect to R350 phase-out year as the single ratchet.

---

### §5.5 Architecture amendments

Append to `02_Architecture_and_Methodology.md`:

**§6.5 amendment**:
> Deployment binding: cash demand rows in the Allocator queue (R48/R53/R58/R63 per-vehicle; R43/R68/R73 per-module) MUST read exogenous demand targets (anchor × learning × year-mask), NOT actual module CapEx output. Output rows (Starlink R33/R37/R39/R41 launches; module R205 CapEx) MAY be cash-bound via MIN(cash/cost, internal_target). Demand and output are mathematically distinct quantities; conflating them produces zero-attractor circular dependencies under iterative calc.

**§20.3 amendment**:
> Sprint 11d's deployment binding architecture wrote cash demand = actual CapEx, which created a zero-attractor fixed point in iterative calc (Group Revenue 2050 collapsed $583B → $17B). Sprint 11f decouples by writing cash demand = exogenous anchor × learning × cost. Output side (launches MIN cash/cost) is retained — the cap stays on output, not demand.

---

## §6 Verification

### §6.1 Workbook-wide error scan

Zero #REF! / #VALUE! / #DIV/0! / #NAME? / #N/A across all 15 tabs.

### §6.2 Conservation

Group P&L R108 = "OK" all 26 years 2025-2050. R109 = 0 ± $1M all years.

### §6.3 Calibration drift surface

| Metric | Post-11e baseline | Post-11f expected | Halt range |
|---|---|---|---|
| Group D10 Revenue 2025 | $13,855M | $13,800-13,900M | <$10B or >$17B |
| Group AC10 Revenue 2050 | $583B | $570-610B | **<$400B HALT** |
| Group AC28 D&A 2050 | $6B | $6-10B | >$20B HALT |
| Allocator D29 Available cash 2025 | $13.7B+ | $13.7B+ (unchanged) | <$5B HALT |
| Allocator D48 V2 BB demand 2025 | reads R88 ($1.1B) | reads exogenous anchor ($1.1B) | exact match expected |
| Allocator E48 V2 BB demand 2026 | reads R88 (cash-bound) | exogenous anchor × learning | >$1B expected |
| Allocator AC48 V2 BB demand 2050 | 0 (V2 phase-out) | 0 | exact |
| Allocator D88 V2 BB allocation 2025 | $1,116M | = D50 (~$1,116M) | exact match |
| Group P&L R108 conservation | "OK" all years | "OK" all years | any CHECK HALT |

### §6.4 Round-trip stability + Rule 22 stale-ref scan

- 5x recalc — no value moves > $1M
- Rule 22: grep all tabs for references to `Allocator!$R$48`, `Allocator!$R$53`, `Allocator!$R$58`, `Allocator!$R$63`, `Allocator!$R$88`, `Allocator!$R$89`, `Allocator!$R$90`, `Allocator!$R$91` and `Starlink!$R$43`, `Assumptions!$R$320` — confirm no stale-ref breakage

### §6.5 Claude Log entry

| Date | Sprint | Tabs touched | Summary | Outstanding |
|---|---|---|---|---|
| 2026-MM-DD | 11f | Allocator R48/R53/R58/R63 (demand rewrite to exogenous anchor × learning); R88-R91 (alloc reads proposed alloc R50/R55/R60/R65); §5.3 module-level conditional rewrite; §5.4 stale-flag grep | Deployment binding circular dependency resolved per Architecture §6.5 + §20.3 amendments. Allocator now binds: demand exogenous, output cash-bound, no recursion. V2→V3 transition emerges from R350 phase-out year + V3 trigger year + IRR signal + cash allocation (V30.5 Lessons §2 finally lands). Group Revenue 2050 preserved at ~$583B. | Sprint 11.5 ODC unit economics; Customer Launch IRR fix (per `project_customer_launch_irr_fix_pending`); bridge loan repayment + interest expense; Sprint 9 §6.8 calibration revision post-11f |

---

## §7 Outstanding items (deferred to 11.5 / 12 / later)

1. **Customer Launch IRR fix** — per `project_customer_launch_irr_fix_pending`, F9 prints 287% IRR (artifact), Starship masked by negative margin. Three-bug fix (N units, per-launch cadence, cost slug fullness) drafted at `Customer_Launch_IRR_Fix_Plan.md`. **Sanity check flagged ~1700% IRR even after fix** — second pass needed before lock. Vlad reworking roadmap; don't auto-add. Relevant to Allocator queue priority since CL R42 / R99 IRR signals are read by the queue.
2. **Sprint 11.5 ODC unit economics** — Vlad-pending decision on per-sat compute revenue OR per-sat cost inputs.
3. **Bridge loan repayment + interest expense** — $20B inflow currently has no repayment or interest cost.
4. **Sprint 9 §6.8 calibration target revision** — post-11f, Group FCF + D&A settle at new levels; refresh targets.
5. **R110 Σ Module FCF residual** — module-owner audit.

---

## §8 Amendment log

- **2026-05-27 (initial draft)** — Sprint 11f spec authored after architectural discussion with Vlad. Locks Option A (demand purely exogenous, output cash-bound). Three-section structure: §5.1 demand rewrite, §5.2 alloc rewrite (closes the second half of the ring), §5.3 conditional module-level rewrite. Architecture §6.5 + §20.3 amendments codify the demand-vs-output separation pattern as a constitutional rule for future modules.

---

## End of Sprint 11f Spec
