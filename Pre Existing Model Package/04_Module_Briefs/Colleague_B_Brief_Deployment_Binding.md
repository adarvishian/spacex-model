# Colleague B Brief — Sprint 11f Deployment Binding + Allocator Wiring

**Status**: Stub. Vlad edits before sending.

**Decision pending tomorrow**: whether to execute against the current model state (V2.16) or to restart from scratch (V30.5 + Q4'25 anchors). This brief assumes the continue-current path; if restart is chosen, scope shrinks to executing Sprints 0-10 first.

---

## Scope

Execute Sprint 11f — the architectural rework that decouples sigmoid demand from sigmoid output to fix the circular dependency that collapsed Sprint 11d. This is the highest-priority open work in the model.

Key reads (in order):

1. `01_Current_State/STATUS_2026_05_26.md` — where the model is, what broke in 11d, what 11e shipped, what 11f is for
2. `01_Current_State/Sprint_11f_Spec.md` — the full spec for the rework
3. `01_Current_State/Sprint_11e_Spec.md` — what just shipped (your starting baseline)
4. `01_Current_State/Sprint_10_8_Spectrum_License_Fee_Spec.md` — predecessor that unblocked the queue gate
5. `00_Constitutional_Docs/02_Architecture_and_Methodology.md` — §6.5 (deployment binding) + §20.3 (amendments)
6. `06_Memory_Snapshot/MEMORY_SNAPSHOT_CRITICAL_LOCKS.md` — Section 1.8 (demand purely exogenous), 1.9 (vehicle-level allocator), 1.10 (allocator advisory not binding), 2.7 (circular dep at zero attractor)
7. `01_Current_State/Customer_Launch_IRR_Fix_Plan.md` — adjacent open thread Vlad may slot in

---

## Current state

- Sprint 11e shipped LM BV correction + Launch Capacity wiring + CL R210
- Sprint 10.8 spectrum license fee unblocked queue gate in 2025-26
- Group Revenue 2050 = ~$583B baseline (not the collapsed $17B)
- Allocator R83-R91 canonical labels live (5 module + 4 vehicle)
- Allocator §6 cash queue 7 sub-blocks live
- **Deployment binding NOT wired** — module CapEx formulas still don't bind on Allocator IN
- V2.16 is the working workbook (Vlad will share or has shared)

## What Sprint 11f does

Per §2 of Sprint_11f_Spec.md — **Option A: demand is purely exogenous**:

| Quantity | Reads from | Recursion? |
|---|---|---|
| Demand (R48/R53/R58/R63 + R43/R68/R73) | Anchor × learning × year-mask + exogenous facility CapEx | No |
| Output (R33 launches → R88 sat CapEx → R8 cash IN) | MIN(cash from allocator / unit cost, internal target) | Bounded by cash; no longer feeds demand |

Allocator reads demand + IRR → ranks → assigns cash. Cash drives output. Output never feeds back into demand.

## Sections in Sprint 11f (per §4)

| § | What ships | Tabs touched |
|---|---|---|
| 5.0 | Pre-flight (calc engine probe + baseline) | read-only |
| 5.1 | Allocator cash demand rewrite (R48/R53/R58/R63) | Allocator |
| 5.2 | Allocator cash allocation rewrite (R88/R89/R90/R91) | Allocator |
| 5.3 | Module-level deployment binding cleanup (R43/R68/R73) | Allocator |
| 5.4 | Retire stale flags (Assumptions R320) | Assumptions, Starlink |
| 5.5 | Architecture amendments (§6.5 + §20.3) | docs only |

5 sections, ~2-3 tabs. Within sprint-sizing convention.

## Calibration targets (must hit after 11f)

- Group Revenue 2050 stays at ~$583B (no major change expected; 11f is plumbing)
- Conservation R108 = "OK" all years
- Allocator deployment formulas now bind — verify module CapEx changes when you flex Allocator IN
- No circular dep — iterative calc should converge in <10 iterations, not 100

## Adjacent threads Vlad may want to fold in

- **Customer Launch IRR fix** — F9 prints 287% IRR (artifact). See `Customer_Launch_IRR_Fix_Plan.md`. Likely a separate patch sprint OR folded into 11f if Vlad calls it.
- **Bridge loan repayment + interest expense** — current model has $20B inflow with no repayment or interest cost; Sprint 11.5 territory.
- **R110 Σ Module FCF residual** (-$1,640M trajectory) — module-owner audit pending.

## Exit criteria

- Sprint 11f PASS — all 5 sections executed, halt thresholds met
- Conservation = OK, no circular dep, deployment binding live
- Architecture §6.5 + §20.3 amendments documented
- Memory entries for any new lessons learned
- Hand-off to Vlad for sprint 11.5 / 12 planning

## Suggested workflow

1. Read prerequisite docs (~2 hours)
2. Confirm V2.16 baseline state with Vlad (run §5.0 pre-flight, post baseline numbers)
3. Open spec-author chat ONLY if you find a real bug in Sprint_11f_Spec — otherwise go straight to plugin execution
4. Open plugin-execution chat — attach Sprint_11f_Spec + V2.16
5. Execute §5.1 → §5.5 with save+reopen between any Assumptions writes
6. Hand back to Vlad with PASS report

## Things to NOT do

- Don't write demand rows that read actual CapEx (you'll reintroduce the Sprint 11d collapse — see Memory Snapshot 2.7)
- Don't fleet-seed to escape circular deps (per Memory Snapshot 1.5)
- Don't add Assumptions rows and reference them cross-tab in the same chat without save+reopen (Memory Snapshot 2.1)
- Don't use row numbers — INDEX/MATCH on canonical labels only (Execution Rule 12)
- Don't surface version letters/numbers in status discussion (Vlad lock 2026-05-27)

---

## Vlad — please edit before sending

This brief assumes Colleague B is taking 11f because they're more comfortable with the Allocator architecture. If you want to assign differently, swap with Brief A. If you're choosing the fresh-restart path tomorrow, this brief's scope shifts to executing Sprints 0 → 10 to rebuild the baseline before 11f.
