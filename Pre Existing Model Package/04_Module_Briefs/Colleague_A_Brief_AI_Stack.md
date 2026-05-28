# Colleague A Brief — AI Stack Module

**Status**: Stub. Vlad edits before sending.

**Decision pending tomorrow**: whether to execute against the current model state (V2.16) or to restart from scratch (V30.5 + Q4'25 anchors). This brief assumes either path is open.

---

## Scope

Build the AI Stack module as a standalone tab in the model. Currently DEFERRED — Sprint 6 was paused because Vlad needed to lock 8 epistemic questions before execution. The scoping doc landed 2026-05-22 with a Stage 1 architecture-only spec; Stage 2 (the standalone workbook) is your deliverable.

Key reads:

- `05_Reference_Material/AI_Stack_Module_Architecture_Scoping.md` — the Stage 1 scoping doc. Lists the 8 open questions, the product-ramp framework, and the PFLOP-hr derivation.
- `00_Constitutional_Docs/02_Architecture_and_Methodology.md` — read §6 (deployment) and §18 (the open-question list, item 4 is AI Stack)
- `06_Memory_Snapshot/MEMORY_SNAPSHOT_CRITICAL_LOCKS.md` — Section 1 (vending-machine framing applies to AI Stack), Section 2 (Excel footguns)

---

## Current state

- Sprint 6 deferred 2026-05-20
- Scoping doc shipped 2026-05-22
- **8 open questions await Vlad sign-off** — Q3 (at-cost vs at-market internal transfer pricing) is highest priority
- No tab exists in the workbook yet
- AI Stack does NOT consume Starship kg capacity (terrestrial-only thesis per `project_ai_stack_no_launch_demand`)

## Open questions Vlad needs to close (before you execute)

These are in the scoping doc; reproduced here for visibility:

1. Standalone tab vs rolled into ODC tab
2. Product ramp curves — logistic vs piecewise vs Wright's Law
3. **At-cost vs at-market internal transfer pricing for compute consumed by AI Stack from ODC** (HIGHEST PRIORITY)
4. Revenue recognition: subscription vs usage-based
5. S&M as % of revenue (currently flagged for Group-level allocation per accounting methodology locks 2026-05-20)
6. IRR engine — finite-difference per-product, or fleet-level
7. Calibration target year (2030? 2035?)
8. Whether to model orchestration layer (Cursor / Terrafab) as a separate sub-module

## Exit criteria

- Standalone workbook with AI Stack tab built per vending-machine framing
- All 8 open questions closed with Vlad locks documented in the spec
- Calibration against scoping doc anchors
- Conservation check (R108-equivalent) = OK
- Integration spec for how AI Stack lands in the main model post-build (Sprint NN insertion point)

## Suggested workflow

1. Read prerequisite docs (~3 hours total)
2. Open spec-author chat with Vlad — close the 8 open questions
3. Draft `Sprint_AIS_1_Spec.md` against the closed answers
4. Open plugin-execution chat — execute against a fresh workbook (or a copy of V2.16 if integrating live)
5. Hand back to Vlad for integration sprint

## Things to NOT do

- Don't add Starship kg demand from AI Stack (terrestrial-only thesis)
- Don't add module-level SG&A or R&D (Group-level per vending-machine framing)
- Don't start execution before Q3 (transfer pricing) is closed — it's load-bearing for revenue calibration
- Don't surface version letters/numbers in status discussion (per Vlad lock 2026-05-27)

---

## Vlad — please edit before sending

This brief assumes Colleague A is taking AI Stack because it's a clean parallel build (no dependency on Sprint 11f deployment binding). If you want to assign differently, swap with Brief B.
