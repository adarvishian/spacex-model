# Sprint 11b — Kickoff Prompt (paste in new plugin execution chat)

**Workbook**: Vlad has saved as V2.15 before plugin writes. Plugin operates against the open V2.15 session; Vlad handles saving per Standing Rule 2.

---

We are running **Sprint 11b** of the SpaceX Model Rebuild v2 — continuation of the combined cleanup sprint. Sprint 11a halted very early in the prior chat (context budget); only minimal landings occurred. Sprint 11b picks up most of the spec.

## What 11a actually landed (V2.14 verified state)

Sprint 11a wrote only TWO things before halting on context budget:

1. **Assumptions R350** — `V2 phase-out year (no V2 BB / V2 DTC launches from this year)` = 2028, MC range [2026, 2032] triangle
2. **Allocator structural row insertion** — 4 empty rows inserted at R88-R91. Effect:
   - R83-R87 module canonical labels: UNCHANGED position (Customer Launch / Starlink / ODC / AI Stack / Lunar Mars cash allocations all still at R83-R87)
   - R88-R91: NOW EMPTY (placeholder for §3.3 new vehicle canonical labels)
   - R92: spacer
   - §6 KG IRR QUEUE header: shifted R89 → **R93**
   - §6 kg content rows shifted +4 (Total Starship capacity now R94; Lunar Mars kg reserved R95; Capacity available R96; sub-blocks R98+)
   - §7 MODULE KG ALLOCATIONS header: shifted R132 → **R136**
   - §8 VEHICLE BUILD CLAIM header: shifted R139 → **R143**
   - §9 CENTRAL IRR DISPLAY header: shifted R152 → **R156**
   - Cross-tab refs use INDEX/MATCH by label (Rule 12) — all still resolve correctly verified post-shift

3. **Verified intact**: R83-R87 canonical labels resolve; Group P&L D108-AC108 = "OK" all years; D109-AC109 = 0; Group Revenue 2025 = $13,855M; Group D&A 2050 = $484,076M (LM BV depreciation NOT YET removed — that's §3.11 in this chat)

## 11a decisions locked (DO NOT re-litigate in this chat)

**Decision A** — §3.10 F9 fleet wiring is MOSTLY A NO-OP. Plugin probe revealed Launch Capacity R61 already has the year-conditional formula `=MAX(0, $D$55*(1-(F$4-$D$56)/$D$57))` for F+ years; D61 + E61 = 17 hardcoded historical anchors (Q4'25). The IF-bifurcated form §3.10 prescribes is functionally equivalent. **Sprint 11b should preserve D61/E61 anchors. If the spec's IF-bifurcated form is applied, ensure it preserves the D=17, E=17 anchors via the year-trigger gate.** Otherwise just update label to note "V3-trigger-aware decay" and skip the formula rewrite. Plugin's judgment.

**Decision B** — R84 rollup drift $1,202.54M → $1,184M is STRUCTURAL and INTENDED. The $18M maps to Starlink R93 V3 BB facility CapEx 2025 = $18.1M (real pre-launch facility build). My spec gated R90 (V3 BB cash allocation D-col) = 0 hard via V3 trigger. **Optional 11b improvement**: amend R90 D-col override to include V3 BB facility CapEx + R91 D-col similarly for V3 DTC, since facility CapEx is pre-launch infrastructure spend not gated by sat deployment trigger. Drift is within ±5% tolerance — not a halt.

**Decision C** — Sprint 11 split into 11a/11b was approved. Sprint 11a was scoped to §3.2 + §3.3 + §3.5b + §3.6 + §3.7 but actually only landed §3.1 + row insertion. Sprint 11b should pick up the ENTIRE remaining scope.

## Sprint 11b scope — what to execute

**ALL remaining §3 sections from Sprint_11_Spec.md**:

- §3.0 Pre-flight (Sprint 11b subset — focused on what 11b touches; skip 11a checks)
- **§3.2 Allocator §4 cash queue rewrite to 7 sub-blocks (compact 5-row form)** — replace existing R40-R80 OLD 4-sub-block layout (CL R40-R46, SL R48-R54, ODC R56-R62, AIS R64-R70, Σ R80) with NEW 7 sub-blocks (CL + V2 BB + V2 DTC + V3 BB + V3 DTC + ODC + AIS) at R41-R75, Σ at R80. Apply V3 startup gate (Launch Capacity R56=2027) + V2 phase-out gate (Assumptions R350=2028) on respective sub-blocks.
- **§3.3 Allocator §5 canonical labels** — fill the EMPTY R88-R91 with 4 new vehicle cash allocation labels. Update R84 to SUM rollup `=D88+D89+D90+D91`. **Note Decision B above for V3 facility CapEx in D90/D91 first-year override.**
- §3.4 Allocator §6 kg queue expand to 5 sub-blocks at R94-R128 (post-shift)
- §3.5 Allocator §7 R137-R142 kg canonical labels (post-shift) — 2 new V3 vehicle kg labels
- §3.5b Starlink Module IN R7-R14 expand to 4 cash + 2 kg reads
- §3.6 Starlink R33/R37/R39/R41 deployment formula rewire
- §3.7 Retire Starlink R43 ratchet + Assumptions R320 V2 DTC cap (clear values + retirement-note labels)
- §3.8 Customer Launch / ODC / AI Stack R205 module-level deployment binding
- §3.9 Launch Capacity endogenous Starship fleet wiring (R8/R9 replicate across years; R25 = f(R150 vehicle build claim); R33/R34 endogenous)
- §3.10 F9 wiring (per Decision A: mostly skip / label-only)
- **§3.11 LM BV depreciation REMOVED from Group D&A** — HIGHEST STAKES. Group P&L R28 + R36 formula amendments. Add new `Lunar Mars Module D&A ($mm)` row on LM tab. **Group D&A 2050 should drop $484,076M → ~$6,000M.** This is the make-or-break section.
- §3.12 ODC unit-economics audit (read-only)
- §3.13 Customer Launch R210 Capacity Demand wire

Plus §4 Verification + Claude Log entry.

## Existing ramp logic — internal_uncapped_demand resolution for §3.6

Plugin probed Starlink E33-E41 formulas (V2 BB / V2 DTC / V3 BB / V3 DTC E-col deployment) — they ALREADY USE Assumptions-driven ramp logic. Use these existing patterns as `internal_uncapped_demand` in Sprint 11 §3.6's new MIN formulas:

- **V2 BB internal demand**: existing E33 formula = `$D$33 × (1 + sat_cost_learning_rate)^E$5` (compounding ramp from 2025 anchor 2,987 sats). Wrap in V2 phase-out gate.
- **V2 DTC internal demand**: existing E37 formula = `$D$37 × (1 + sat_cost_learning_rate)^E$5`. Wrap in V2 phase-out gate.
- **V3 BB internal demand**: existing E39 reads `INDEX(Assumptions, "V3 BB launches per year stub trajectory", year-offset)`. There's a year-row stub on Assumptions. Use this; wrap in V3 trigger gate.
- **V3 DTC internal demand**: same pattern reading "V3 DTC launches per year stub trajectory".

**Important**: existing E33 formula uses BOTH the V2 DTC permanent cap flag (R320) AND a different "V3 BB first launch year" Assumptions input — these are DIFFERENT from the new R350 V2 phase-out year + Launch Capacity R56 V3 trigger year. The new §3.6 formulas should use **R350 and R56** (the new canonical gate inputs) and IGNORE the old "V3 BB first launch year" + R320 inputs (which §3.7 retires).

If the existing E39 V3 BB ramp uses "V3 BB first launch year" Assumptions input (= probably 2026) and the new Launch Capacity R56 V3 trigger = 2027, there's a 1-year mismatch. **The new formula governs**: V3 BB launches start in 2027 (per R56), so E39 (2026) = 0 — current model value 200 is replaced by 0 once §3.6 lands. This is intentional per spec; surface in §4 verification.

## Pre-flight (11b subset) — read only what 11b touches

Skip 11a checks (already verified). Focus on §3.11 LM BV + §3.9 Launch Capacity + new ramp-formula stubs:

1. Lunar Mars R117 + R118 baseline values (AC117 ~$368B; AC118 ~$109B) — confirm before removal
2. Group P&L R28 + R36 formula text contains `BV depreciation — Lunar` + `BV depreciation — Mars` substrings (to remove)
3. Launch Capacity R8/R9 still D-only static; R25 = 0; R34 = 0
4. Customer Launch R210 = 0 (to wire)
5. ODC R102/R154/R207 negative IRR baseline (audit reference; no fix)
6. Assumptions "V3 BB launches per year stub trajectory" + "V3 DTC launches per year stub trajectory" year-rows exist (canonical labels)
7. Existing Sprint 11a outputs intact: R350 = 2028; Allocator R88-R91 still empty; §6 header at R93; conservation R108 = "OK" all years

## Process — read constitutional docs

1. Read these files in order:
   - `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/00_README_Sprint_Kickoff.md`
   - `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/01_Lessons_Learned.md`
   - `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/02_Architecture_and_Methodology.md` — especially **new §20 amendments block (lines 873-1077)** load-bearing for 11b. §20.5 LM BV correction is the highest-stakes amendment.
   - `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Model Execution Rules.md`
   - `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_11_Spec.md` — execute remaining §3 sections.

2. Standing rules (locked 2026-05-20): spec self-contained; Vlad handles saving; kickoff includes setup confirmation.

3. Apply 23 model execution rules. Particularly:
   - Rule 1 one concept per write (use execute_office_js for multi-row sections — `feedback_execute_office_js_safer_for_multirow_writes`)
   - Rule 12 INDEX/MATCH by canonical label (immune to row shifts from 11a)
   - Rule 22 stale-ref scan
   - Rule 23 anchor-and-offset (no year-chained recursion except documented exceptions)

4. **Post-PASS diagnostic step** per memory `feedback_late_methodology_surfaces_as_model_grows`: after §4 PASS, re-probe workbook for second-order effects:
   - Group FCF 2050: V2.14 value +$337,548M (illusory; inflated by phantom D&A add-back). Post-§3.11, expect dramatic drop to ~-$90B. Document.
   - V3 BB / V3 DTC deployment 2027+: should ramp post-§3.9 fleet wiring (was 0 because Launch Capacity R34 = 0).
   - V3 BB E33 (2026) launches: was 200 in V2.14; expect 0 post-§3.6 (trigger gate fires for 2026 < 2027).
   - V2 phase-out 2028+ : V2 BB G33 + V2 DTC G37 = 0 post-§3.6.
   - R110 Σ Module FCF residual: was -$1,640M at AC; may resolve or shift post-§3.11.

5. **Context-budget consideration** — Sprint 11 is the largest spec in the rebuild. 11a halted on context after only §3.1 + row insertion. If 11b approaches context limits, the plugin should halt at a clean section boundary (after a complete §3.x and §4-style verification) rather than mid-formula-write. Reasonable mid-sprint halt points: after §3.7 (all Starlink + Allocator §4-§5 + ratchet retire complete; before §3.8 cross-module work), or after §3.10 (Allocator + Starlink + Launch Capacity complete; before §3.11 LM BV big swing). If halting, produce a Sprint 11c handoff prompt similar to this one with what landed + what remains.

## Open architectural threads (carry forward to Sprint 12 / Sprint 11.5 — NOT 11b scope)

- Sprint 9 §6.8 calibration target revision (post-Sprint-11; Vlad locks new targets reflecting LM BV correction + V3 endogenous deployment)
- Sprint 11.5 ODC unit-economics input revision (Vlad-pending decision)
- R110 Σ Module FCF residual — module-owner audit
- AC_2050 EBITDA negativity — Sprint 12 audit

---

Current sprint scope: **Sprint 11b — continuation of combined cleanup**. Sections: §3.2 + §3.3 + §3.4 + §3.5 + §3.5b + §3.6 + §3.7 + §3.8 + §3.9 + §3.10 (mostly skip per Decision A) + §3.11 (highest-stakes) + §3.12 + §3.13. Plus §4 Verification + Claude Log.

Setup confirmation:
- Target workbook: SpaceX Model V2.15.xlsx is open with the correct name (Vlad pre-named via Save-As after 11a PASS on V2.14)
- I (Vlad) will handle all saving during/after execution
- Sprint 11a row insertion at Allocator R88-R91 already done — DO NOT re-insert. §6 header is at R93, §7 at R136, §8 at R143, §9 at R156.
