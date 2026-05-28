# Sprint 11d — Kickoff Prompt (paste in new plugin execution chat after V2.17 save+reopen)

**Workbook setup**: V2.17.xlsx is the MERGED baseline (V2.14-a1636d7f Block 1 PASS state + Sprint 11c §3.1.5 bridge loan writes from V2.16). Vlad opens V2.17 in Excel for the first time. Plugin operates against the open V2.17 session. NO save+reopen needed — V2.17 was generated programmatically from the correct base, so calc engine starts fresh on first Excel open.

**IMPORTANT — DO NOT use V2.16**: V2.16 was the wrong base (came from V2.14 plain, missing Block 1 §3.2-§3.5 vehicle-level work). V2.17 = correct base + bridge loan additions.

---

We are running **Sprint 11d** of the SpaceX Model Rebuild v2 — continuation after Sprint 11c §3.1.5 halted with workbook-baseline drift. V2.17 is the merged correct baseline (Block 1 PASS state + §3.1.5 bridge loan writes):

✅ Persisted on disk:
- `Assumptions A351:F351` — bridge loan input row, B351 = 20000 verbatim
- `Allocator A11` — Cash Pool Tracker row label
- `Allocator D11:AC11` — IF/INDEX/MATCH formula (UNKNOWN whether stored as formula or text — see §3.0 below)

❌ NOT written:
- `Allocator D15/E15:AC15` Cash BoY formula update (held pending calc engine recovery)
- §3.5b through §3.13 (entire scope from Sprint 11 spec)

## §3.0 Pre-flight (calc engine + write-mode sanity probe — NEW protocol)

The Sprint 11c halt diagnosed "calc engine session failure". TWO possibilities to discriminate before any further writes:

**Probe 1 — formula-vs-text check**:
Read the FORMULA TEXT of `Allocator D11` (not the value). Use `range.formulas` API or equivalent.
- ✓ Expected: `=IF(D$4=2025, INDEX(Assumptions!$B:$B, MATCH("Pre-IPO bridge loan drawdown ($mm, drawn in 2025)", Assumptions!$A:$A, 0)), 0)` — formula stored
- ✗ Possible bug: `"=IF(D$4=2025, ...)"` returned as a STRING value — formula was written as text via `.values` API instead of `.formulas` API

**If formula text** is present → calc engine bug (recoverable via reopen). Proceed to Probe 2.
**If text string** is present → plugin write API bug. Need to REWRITE D11:AC11 using the formulas API. Once corrected, re-read the value.

**Probe 2 — value evaluation check**:
Read `Allocator D11` value. Expected: **20000** (= $20,000M bridge loan drawn 2025).
- If 20000 ✓ → calc engine recovered after reopen. Proceed to §3.1.5 Step 3.
- If 0 → calc engine still broken OR there's a deeper issue. HALT, escalate to Vlad. Consider: (a) is calculation mode set to Automatic? (b) does `=COUNTA(Assumptions!$A:$A)` return non-zero? (c) is `Assumptions` the actual tab name (no trailing space, no hidden character)?

**Probe 3 — sanity sweep**:
Quick reads to confirm V2.17 merged baseline is complete:
- `Assumptions B351` = 20000 ✓ (bridge loan added via merge)
- `Assumptions B350` = 2028 ✓ (Sprint 11a V2 phase-out — present in Block 1 PASS base)
- `Allocator A88` = "Starlink V2 BB cash allocation" ✓ (Block 1 §3.3 vehicle label)
- `Allocator D88` value = $1,116M ✓ (Block 1 V2 BB cash allocation override)
- `Allocator A93` = "§6 KG IRR-PRIORITY SIGMOID QUEUE" ✓ (Block 1 header relocation)
- `Allocator A138` = "Starlink V3 BB kg allocation" ✓ (Block 1 §3.5 vehicle kg label)
- `Allocator A145` = "§8 VEHICLE BUILD CLAIM" ✓ (Block 1 §3.5 §8 header relocation)
- `Group P&L AC10` = $583,059M ✓ (Block 1 PASS baseline; NOT $16B V2.14.5 collapse)
- `Group P&L D108-AC108` = "OK" all years ✓
- `Allocator D11` evaluates to 20000 (gated by Probe 2)

**If Probe 3 finds Allocator R88-R91 empty (V2 BB / V2 DTC / V3 BB / V3 DTC labels missing) — HALT.** V2.17 wasn't loaded correctly. Vlad must close current Excel session and reopen V2.17 specifically.

If all probes PASS → resume §3.1.5 Step 3. If any FAIL → HALT and report.

---

## §3.1.5 Step 3 — Cash BoY R15 formula update (resumes Sprint 11c §3.1.5)

**ONLY proceed if Probe 2 returns D11 = 20000.**

Replace existing R15 formulas (which currently exclude D11):
- Current D15: `=D8+D9+D10` → New: `=D8+D9+D10+D11`
- Current E15: `=D15+E10+E9` → New: `=D15+E10+E9+E11`
- Copy E15 across F15:AC15

Use the **formulas API** (not values), and after write, force `context.workbook.application.calculate(Excel.CalculationType.full)` + reload values.

**Verification reads (post-write)**:
- D15 Cash BoY 2025 = $25,000M (was $5,000M baseline; bridge loan adds $20B) ✓
- D28 non-module claims 2025 = ~$11,289M unchanged ✓
- **D29 Available cash for IRR queue 2025 = MAX(0, $25,000 - $11,289) ≈ $13,711M (was $0)** ✓ — the critical recovery signal
- E15 Cash BoY 2026 = $25,000 + 2025 FCF (~−$3,050M) + 0 IPO + 0 bridge = ~$21,950M ✓
- F15 Cash BoY 2027 (IPO year) = $21,950 + 2026 FCF + $30,000M IPO = ~$50B+ ✓

**HALT condition**: if D29 ≤ $5B → bridge loan not effective; check D11 + D15 formula text + Cash BoY chain.

---

## §3.5b through §3.13 — execute per Sprint_11_Spec.md verbatim

After §3.1.5 Step 3 verified, proceed with the remaining Sprint 11 sections. Reference `Sprint_11_Spec.md` for exact formula details.

Halt-at-section-boundary if context tightens (per prior plugin's experience with context exhaustion). Reasonable halt points: after §3.7 (Starlink-internal complete; before cross-module work), after §3.10 (before §3.11 LM BV — the highest-stakes single section).

**CRITICAL**: §3.11 LM BV depreciation removal is the largest single architectural swing. If §3.5b-§3.10 + verification land cleanly but context is tight, halt and produce a Sprint 11e handoff for §3.11+§3.12+§3.13.

---

## Read these files in order

1. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/00_README_Sprint_Kickoff.md`
2. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/02_Architecture_and_Methodology.md` — particularly §20 amendments block (lines 873-1102) and especially **§20.9 Pre-IPO Bridge Loan (lines 1086-1097)** which is the critical addition
3. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Model Execution Rules.md`
4. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_11c_Spec.md` — recovery spec; defines §3.1.5 (partially complete) then references Sprint 11 §3.5b-§3.13
5. `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Sprint_11_Spec.md` — formula details for §3.5b-§3.13

## Architecture amendments to be aware of

- **§20.9 Pre-IPO Bridge Loan** (2026-05-26) — $20B drawn 2025, $0 from 2026+
- §20.1-§20.8 — Sprint 11 amendments (vehicle-level allocator, deployment binding, LM BV correction, etc.)

## New protocol observation (write-then-reference footgun)

Both Sprint 11 Block 2 AND Sprint 11c hit a session-level calc engine issue specifically AFTER writing a new Assumptions row + immediately referencing it cross-tab in the same session. This is now a known footgun pattern. Sprint 11d's §3.0 pre-flight probes for both possible root causes (calc engine corruption vs. write-API misuse) before proceeding.

**Going forward** in this sprint and future sprints: if writing a new Assumptions row that downstream formulas reference, prefer to:
- Write the Assumptions row in one plugin chat
- Vlad saves + reopens
- Reference it cross-tab in the NEXT plugin chat

OR, within a single chat, after writing the new Assumptions row, use `worksheet.calculate()` on the destination sheet specifically before reading any downstream values.

## Halt conditions

- Probe 1 returns text not formula → HALT, escalate (plugin write API bug, not calc engine)
- Probe 2 D11 ≠ 20000 after reopen → HALT, escalate
- Probe 3 any baseline drift → HALT (workbook may have wrong file or unexpected modifications)
- §3.1.5 D29 Available cash ≤ $5B → HALT (bridge loan not effective)
- §3.11 Group D&A 2050 > $20B after fix → HALT (LM BV refs not fully removed)
- Group Revenue 2050 < $200B → HALT (deployment chicken-and-egg still firing)
- Conservation R108 = "CHECK" any year → HALT

Setup confirmation:
- Target workbook: SpaceX Model V2.17.xlsx is open, fully reopened after save + Excel quit (NOT just close + reopen window)
- I (Vlad) will handle all saving during/after execution
- DO NOT use V2.14.5 (collapsed state)

Current sprint scope: Sprint 11d = Sprint 11c §3.1.5 Step 3 recovery + Sprint 11 §3.5b-§3.13. Plugin starts with three-probe pre-flight to determine calc engine status; proceeds only if probes PASS.
