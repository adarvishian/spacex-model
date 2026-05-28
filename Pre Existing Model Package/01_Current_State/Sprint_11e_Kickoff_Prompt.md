# Sprint 11e — Kickoff Prompt (paste in new plugin execution chat tomorrow)

**Read STATUS_2026_05_26.md FIRST** before this kickoff — it tells you where we are.

**Workbook setup**: Open `SpaceX Model V2.17.xlsx` (clean merged baseline; in workspace folder). Save-As to V2.19. Plugin operates against V2.19. DO NOT use V2.16 (wrong base) or V2.18 (collapsed by deployment binding circular dep). V2.17 + bridge loan partial is the correct starting state.

---

We are running **Sprint 11e** of the SpaceX Model Rebuild v2 — the FINAL reduced Sprint 11 landing. Sprint 11d (V2.18) collapsed Group Revenue 2050 from $583B to $17B because the §3.5b/§3.6 deployment binding architecture I specified has a circular dependency at zero attractor. **That's a real spec error on my side, diagnosed by the prior plugin chat tonight.** The fix requires architectural rework (decouple sigmoid demand from sigmoid output) deferred to Sprint 11f.

**Sprint 11e scope** (reduced, 5 meaningful sections — within sprint sizing convention §10.1):
- §3.0 Pre-flight (calc engine sanity + V2.17 baseline probes)
- §3.1.5 Step 3 — Cash BoY R15 amendment (+D11 bridge loan; partial work from V2.17 completes)
- §3.9 — Launch Capacity Starship endogenous fleet wiring (R8/R9 across years; R25 = f(Allocator vehicle build claim))
- §3.10 — F9 R61 col A label update (Decision A; label-only)
- §3.11 — **LM BV depreciation REMOVED from Group D&A** (the biggest single win: AC28 $484B → ~$6B)
- §3.12 — ODC unit-economics audit (read-only doc)
- §3.13 — Customer Launch R210 Capacity Demand wire

**Sprint 11e DOES NOT execute**:
- §3.5b Starlink Module IN expand (defer to 11f)
- §3.6 Per-vehicle deployment rewire (defer — circular dependency)
- §3.7 Retire R43 ratchet / R320 V2 DTC cap (paired with §3.6; defer)
- §3.8 Module-level deployment binding for CL/ODC/AIS (same circular pattern; defer)

Starlink continues to deploy via old hardcoded ramp logic. Allocator stays "advisory not binding" per `project_allocator_advisory_not_binding_2026_05_26`. Known compromise; documented.

## Read these files in order

1. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/STATUS_2026_05_26.md` — **READ FIRST**
2. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/00_README_Sprint_Kickoff.md`
3. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/02_Architecture_and_Methodology.md` — particularly §20.5 LM BV correction + §20.9 bridge loan + §10 sprint sizing
4. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/03_Sprint_Roadmap_and_Verification.md` — particularly §10 sprint sizing convention
5. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Model Execution Rules.md`
6. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_11e_Spec.md` — the spec

## §3.0 Pre-flight protocol (per Roadmap §10.3)

1. **Calc engine sanity probe FIRST** — write `=Assumptions!$A$2` to scratch cell (e.g., Allocator!Z200). Force calculate(full) + sync. Read scratch cell. Expected: matches Assumptions!A2 text. If 0 or empty → HALT, demand Vlad to fully quit Excel + reopen V2.19. Clear scratch cell.

2. **V2.17 baseline sanity** (per Sprint 11e Spec §3.0):
   - Assumptions B350 = 2028; B351 = 20000
   - Allocator A88 = "Starlink V2 BB cash allocation"; D88 = 1116
   - Allocator D11 evaluates to 20000 (bridge loan formula intact)
   - Group P&L AC10 = $583,059M
   - Group P&L AC28 = $484,076M (baseline phantom D&A; §3.11 will remove)
   - Conservation R108 = "OK" all years

3. **HALT if Group P&L AC10 < $400B** — wrong workbook; investigate.

## Sprint sizing + halt conditions

- 5 meaningful sections, ~4 tabs touched (Allocator, Launch Capacity, Lunar Mars, Group P&L, Customer Launch). Within hard cap.
- Halt-at-clean-boundary if context tightens. Natural boundaries: after §3.10 (before §3.11 LM BV) or after §3.11 (before §3.13).
- §3.11 is the highest-stakes single write — handle with care, verify AC28 < $20B before declaring success.

## Standing rules

- Vlad handles all saving
- Spec self-contained
- Kickoff confirms workbook open with correct name

## Open architectural threads (deferred — NOT 11e scope)

- **Sprint 11f**: Vehicle-level deployment binding architectural rework. Fix circular dependency. R48/R52/R58/R63 sigmoid demand reads UNCAPPED target (anchor × learning × unit cost), not actual CapEx. Decouples demand from output. Spec-author task tomorrow OR after 11e PASS.
- **Sprint 11.5 ODC + bridge repayment + interest expense**
- **Sprint 9 §6.8 calibration revision** post-11e once FCF 2050 settles at new level
- **R110 Σ Module FCF residual**, **AC_2050 EBITDA**, etc. — Sprint 12 audits

Setup confirmation:
- Target workbook: SpaceX Model V2.19.xlsx is open (Vlad pre-named via Save-As from V2.17 baseline this morning)
- Vlad handles all saving during/after execution
- DO NOT use V2.16 (wrong base) or V2.18 (collapsed)

## Why Sprint 11e is different from Sprint 11d

Sprint 11d tried to do EVERYTHING including deployment binding. Sprint 11e ships the SAFE parts (the changes that don't introduce circular dependencies). Sprint 11f handles deployment binding properly with architectural rework.

This is the right move: capture the high-value win (LM BV correction) without compounding architectural debt. Defer the deployment binding to a clean spec authoring pass.

