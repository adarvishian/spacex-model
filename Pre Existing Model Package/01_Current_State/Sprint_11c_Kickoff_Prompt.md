# Sprint 11c — Kickoff Prompt (paste in new plugin execution chat)

**Workbook setup**: Open V2.14-a1636d7f.xlsx (Sprint 11 Block 1 PASS state). Save-As to V2.16 before plugin writes. **DO NOT use V2.14.5 — that's the collapsed Block 2 attempt with Starlink revenue at $16B; revert to V2.14-a1636d7f which has Group Revenue 2050 = $583B intact.**

---

We are running **Sprint 11c** of the SpaceX Model Rebuild v2 — RECOVERY sprint after Sprint 11 Block 2 (V2.14 → V2.14.5) collapsed Group Revenue 2050 from $583B to $16B due to deployment chicken-and-egg trap.

## What went wrong in Block 2

Sprint 11 §3.6 wired per-vehicle deployment as `MIN(cash/cost, kg/mass, internal_demand)` per Architecture §6.5. This is correct architecturally BUT triggered chicken-and-egg: pre-IPO Available cash = $0 (Cash BoY $5B − claims $11.6B) → modules can't deploy 2026+ → no FCF → cash never recovers → Group Revenue collapses. The Sprint 10 "allocator advisory not binding" pathology was actually PROTECTING the model from this trap.

## What Vlad disclosed 2026-05-26

S-1 disclosed **~$20B Pre-IPO bridge loan**. This is the missing capital source — real-world SpaceX funded V2 deployment via bridge loan, not just internal FCF.

## Sprint 11c recovery plan

1. Revert workbook to V2.14-a1636d7f (Sprint 11 Block 1 PASS state — Group Revenue 2050 = $583B intact)
2. Wire $20B Pre-IPO Bridge Loan as Cash Pool Tracker inflow (new §3.1.5 — MUST land FIRST)
3. Execute Sprint 11 §3.5b through §3.13 verbatim — now with non-starved cash pipeline
4. Verify Group Revenue 2050 stays in $400-650B range (NOT collapse like V2.14.5)

## Architecture amendments to read

Architecture §20.9 + §20.10 updated 2026-05-26 with $20B Bridge Loan amendment. Located in `02_Architecture_and_Methodology.md` lines 1080-1102.

## Read these files in order

1. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/00_README_Sprint_Kickoff.md`
2. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/01_Lessons_Learned.md`
3. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/02_Architecture_and_Methodology.md` — **especially new §20.9 Pre-IPO Bridge Loan amendment (lines 1080-1102) — this is the critical addition**
4. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Model Execution Rules.md`
5. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_11c_Spec.md` — recovery spec; defines §3.1.5 bridge loan then references Sprint 11 §3.5b-§3.13
6. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_11_Spec.md` — original Sprint 11 spec for §3.5b-§3.13 formula details

## Sprint 11c scope

§3.0 Pre-flight — confirm V2.14-a1636d7f restored (Group Revenue 2050 = $583B baseline)

**§3.1.5 NEW (must land FIRST)**:
- Assumptions R351: `Pre-IPO bridge loan drawdown ($mm, drawn in 2025)` = 20000 (Base Case per S-1)
- Allocator R11: new Cash Pool Tracker row `Pre-IPO bridge loan inflow this year ($mm)`
- Allocator D15 Cash BoY 2025 formula updated to include D11 bridge loan
- Verification: D29 Available cash 2025 jumps from $0 → ~$13,346M

**§3.5b through §3.13** — execute per Sprint 11 spec verbatim:
- §3.5b Starlink Module IN expand
- §3.6 Per-vehicle deployment rewire (3 gates + MIN bind, NOW non-starved)
- §3.7 Retire ratchets (R43 + R320)
- §3.8 Module-level deployment binding (CL, ODC, AIS)
- §3.9 Launch Capacity Starship endogenous fleet wiring
- §3.10 F9 label-only (Decision A; mostly skip)
- §3.11 LM BV depreciation REMOVED from Group D&A (HIGHEST STAKES)
- §3.12 ODC audit (read-only)
- §3.13 Customer Launch R210 wire

§4 Verification — particular emphasis on:
- Group Revenue 2050 stays > $400B (was $583B baseline; collapse to $16B = HALT)
- Group D&A 2050 drops to ~$6B (was $484B with phantom LM BV)
- Conservation R108 = "OK" all years
- Available cash D29 > $5B in 2025 (bridge loan effective)

## Critical halt conditions

- **HALT if Group Revenue 2050 < $200B after writes** — bridge loan didn't unstarve deployment OR deployment binding has another bug
- HALT if Allocator D29 Available cash 2025 ≤ $5B — bridge loan didn't wire correctly
- HALT if Group D&A 2050 > $20B post-§3.11 — LM BV depreciation refs not fully removed
- HALT if conservation R108 = "CHECK" any year

## Standing rules

- Spec self-contained
- Vlad handles all saving (you do NOT issue save commands)
- Kickoff confirms workbook open with correct name; Vlad handles versioning

## Context budget guidance

Previous Sprint 11 Block 2 plugin halted at §3.11 due to Office.js calc engine session issue. If similar issue surfaces in 11c, halt at clean section boundary (after §3.7 or §3.10) and produce a Sprint 11d handoff prompt. **The §3.11 LM BV section is the most context-intensive write**. Consider isolating §3.11 to its own block if context tightens.

Setup confirmation:
- Target workbook: SpaceX Model V2.16.xlsx is open with the correct name (Vlad pre-named via Save-As from V2.14-a1636d7f baseline)
- I (Vlad) will handle all saving during/after execution
- DO NOT use V2.14.5 (collapsed state)
