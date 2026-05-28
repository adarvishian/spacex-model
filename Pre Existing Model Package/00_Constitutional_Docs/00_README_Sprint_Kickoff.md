# SpaceX Model Rebuild v2 — Sprint Kickoff README

**Status**: Authoritative. Read this BEFORE any sprint work.
**Last updated**: 2026-05-19

This is the single navigation doc for the SpaceX modular valuation model rebuild. Every sprint chat (spec-author or plugin execution) starts by reading this file and the four constitutional docs it points to.

## Standing process rules (locked 2026-05-20)

These rules apply to every sprint spec from Sprint 0 onwards. Non-negotiable.

1. **Specs are fully self-contained.** A sprint spec references no external XLSX, no external markdown driver files, no filesystem paths. Every input value, every formula, every cell write, every verification anchor lives in the spec body. The plugin executes against the spec alone — it has no filesystem access and cannot read other workbooks or docs. Build Plan content (or any equivalent input table) is inlined as a numbered section within the spec.
2. **Vlad handles all saving.** The plugin does NOT issue save / save-as commands. Vlad pre-names the workbook via Save-As before sending the kickoff prompt; Vlad saves during/after execution. Specs do not include "save the workbook" steps in the execution sequence. Plugin operates on the live open workbook session; verification reads cells from the session directly.
3. **Kickoff prompt includes a setup-confirmation block** confirming (a) the target workbook is open with the correct name, (b) Vlad will handle saving. Plugin's §3.0 pre-flight verifies this block is present.

These three rules came out of the Sprint 0 execution attempt on 2026-05-20: the plugin halted at pre-flight per Rule 9 because the original spec assumed filesystem reads and plugin-issued saves. Resolved by inlining the Build Plan and removing save instructions. Codified here so Sprint 1+ specs don't repeat the failure.

---

## TL;DR — what's happening

The original 35-spec V30.5 build accumulated too much stale residue (Sprint 5 sigmoid, Layer 3 sweep, AI Stack ghost rows, OFFSET formulas, methodology drift, etc.). Rather than refine V30.5, we are **rebuilding from scratch** starting 2026-05-19.

Inputs to the rebuild: V30.5 (architectural reference), Q4'25 CLEANUP model (2025 historicals), and the four constitutional docs in this folder.

Workflow: spec-author chat writes a sprint spec → fresh plugin execution chat runs the plugin against the spec → spec-author chat reviews + iterates.

---

## Required reading (in this order)

Every sprint chat reads these five docs before any work. No exceptions.

| Order | Doc | Purpose | ~Length |
|---|---|---|---|
| 1 | **`00_README_Sprint_Kickoff.md`** (this doc) | Navigation + protocol | 5 min |
| 2 | **`01_Lessons_Learned.md`** | 23 principles synthesized from V30.5 failure modes. What NOT to repeat. | 15 min |
| 3 | **`02_Architecture_and_Methodology.md`** | Structural design + math conventions. The source of truth on every cross-tab connection, IRR formula, conservation identity. | 30 min |
| 4 | **`03_Sprint_Roadmap_and_Verification.md`** | 12-sprint plan + per-sprint acceptance criteria + universal verification protocol. | 20 min |
| 5 | **`04_Assumptions_Tab_Spec.md` + `04_Assumptions_Tab_Build_Plan.xlsx`** | Cell-by-cell input plan for the Assumptions tab. The XLSX is the actionable build plan; the markdown is the wrapper. | 15 min + reference |

Plus these supporting docs as needed:

- `Model Execution Rules.md` — the 23 plugin-side operational rules + Rule Compliance Preamble template. Mandatory for every spec.
- `2025 Anchors from Q4_25.md` — locked 2025 historical anchors from Q4'25 CLEANUP.
- `Stale_Row_Map.md` — what to AVOID rebuilding (the residue map from V30.5).

---

## Rule Compliance Preamble (MANDATORY at the top of every sprint spec)

Every sprint spec, including patch sprints (X.5 numbering), opens with this 12-box checklist filled in. Plugin execution chats refuse to start work if any box is unchecked without justification.

```markdown
## Rule Compliance Preamble (mandatory)

This spec follows `Model Execution Rules.md` and the four constitutional docs. Confirm each before execution:

- [ ] **Rule 1** (one concept per write) — section structure separates labels, formulas, formats.
- [ ] **Rule 3 / 23** (formula pattern) — bounded-CAGR / ramp formulas use anchor-and-offset. Year-chained formulas explicitly flagged as Rule 23 exceptions with one-line justification.
- [ ] **Rule 4** (verification gate) — every section has explicit read-back cells (D, I, S, AC) + expected values.
- [ ] **Rule 6** (inline formulas) — every cell write specified with the full Excel formula, not a convention reference.
- [ ] **Rule 10** (no row insertions) — confirm no `insert_row` operations; all new content appended below existing data.
- [ ] **Rule 11** (touch points) — every new line item lists its SUM range / aggregator / conservation check / Valuation pulls.
- [ ] **Rule 12** (label-based cross-tab refs) — any Allocator / Valuation / Group P&L pulls use INDEX/MATCH on label.
- [ ] **Rule 13** (vending-machine test) — no module tab gets R&D / SG&A / overhead / taxes added.
- [ ] **Rule 14** (no hardcoded constants) — every behaviour input lives on Assumptions.
- [ ] **Rule 15** (sanity check halt thresholds) — every sanity check has a quantitative halt condition.
- [ ] **Rule 19** (save-as) — spec names target workbook explicitly.
- [ ] **Rule 22** (stale-ref scan) — Valuation + Allocator + Group P&L scan listed in §Verification (Dashboard does not exist in rebuild).

Architecture & Methodology compliance:
- [ ] Module P&L follows vending-machine framing (Architecture §3).
- [ ] Per-sat / per-launch marginal IRR engine (Architecture §5), not fleet-level MFW-IRR.
- [ ] Allocator OUT contract uses canonical 11 labels (Architecture §4.2).
- [ ] Year-offset helper row at row 5 + year header at row 4 on every tab with year columns.
- [ ] ZERO `OFFSET()` formulas; INDEX:INDEX patterns used for dynamic ranges (Principle 11).

If any box is unchecked, the spec author justifies or amends before execution starts.
```

---

## Kickoff prompt template (PASTE AT TOP OF EVERY NEW SPRINT CHAT)

Copy-paste verbatim at the start of every new sprint chat:

```
We are running Sprint N of the SpaceX Model Rebuild v2.
Sprint name: [Sprint name]

Before any work in this chat:

1. Read these files in order:
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/00_README_Sprint_Kickoff.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/01_Lessons_Learned.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/02_Architecture_and_Methodology.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/03_Sprint_Roadmap_and_Verification.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/04_Assumptions_Tab_Spec.md
   - /Users/vladsaigau/Documents/Claude/Projects/Starlink Module/Model Execution Rules.md

2. Confirm you understand the constitutional structure:
   - Lessons Learned codifies WHY (23 principles tied to V30.5 incidents).
   - Architecture & Methodology codifies WHAT (structural design + math conventions).
   - Sprint Roadmap codifies WHEN (12-sprint phase plan) and acceptance criteria.
   - Assumptions Tab Spec codifies inputs (Q4'25-anchored 2025 values + MC ranges).
   - Model Execution Rules codifies HOW (plugin-side discipline, 23 rules).

3. Open this sprint with the Rule Compliance Preamble (template in 00_README §"Rule Compliance Preamble").

4. Reference Sprint Roadmap §X for this sprint's scope, dependencies, and acceptance criteria.

5. Reference Architecture §X for any structural choices this sprint touches.

6. Only after the preamble is filled in and constitutional docs are read: proceed with the sprint work.

If you are a plugin execution chat: do not write a single cell until the Rule Compliance Preamble is confirmed in the spec you are executing.

If you are a spec author chat: do not finalize a spec without the Rule Compliance Preamble at the top.

Current sprint scope: [paste sprint scope summary here]
```

---

## What goes in a Claude Log entry (per sprint)

Sprint Roadmap §5.7 mandates one row appended to the Claude Log tab on the workbook after every sprint. Format:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-MM-DD | N | tab list | One paragraph: what landed, what changed, calibration check results | Any deferred items / open questions | Sprint N+1 name |

Plus the spec-author chat (this chat or future spec chats) maintains a log of constitutional doc amendments — see "Amendment log" at the bottom of each constitutional doc.

---

## When to update constitutional docs

Constitutional docs are not immutable. They get amended when:

- An architectural decision changes (e.g., AI Stack rolls into ODC after all → update Architecture §10 + §1 tab list)
- A new failure mode surfaces during a sprint that warrants a new Principle in Lessons Learned
- Sprint roadmap shifts (e.g., a sprint splits into two)
- An input's MC range needs revision based on new data
- Calibration targets adjust (e.g., Q4'25 anchors get refreshed)

Amendment protocol:
1. Edit the relevant constitutional doc + add an entry to its Amendment Log (bottom of doc).
2. Update related memory entries (`project-rebuild-architecture`, `project-anchored-assumptions-2025`, etc.).
3. Note the amendment in the Claude Log for the sprint that triggered it.

Never amend silently. Future sprint chats need to see what changed and why.

---

## Memory entries that future sprint chats will see automatically

These memories are indexed in `MEMORY.md` and load into every new conversation in this project:

- `project-rebuild-v2-status` — context for the rebuild
- `project-anchored-assumptions-2025` — locked 2025 input values
- `project-rebuild-architecture` — locked architectural decisions
- `project-sprint-kickoff-protocol` — pointer to this README + reading order

Plus load-bearing principle memories (carried from V30.5 build, still apply):

- `reference-execution-rules` — the 23 Model Execution Rules
- `feedback-anchor-and-offset` — Rule 23 pattern
- `feedback-allocator-contract-by-label` — Rule 12 pattern
- `feedback-queue-gate-for-non-module-claims` — load-bearing queue gate
- `feedback-per-sat-irr-no-seed` — per-sat marginal IRR rule
- `feedback-arbitrary-inputs-are-mc` — MC discipline
- `project-scenarios-after-mc` — scenarios post-MC, not before
- `project-vending-machine-framing` — module P&L structure
- `project-dashboard-retired` — Dashboard deleted, don't reference

---

## Folder organization

```
/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/
├── 00_README_Sprint_Kickoff.md              ← read first, every sprint
├── 01_Lessons_Learned.md                     ← constitutional
├── 02_Architecture_and_Methodology.md        ← constitutional
├── 03_Sprint_Roadmap_and_Verification.md     ← constitutional
├── 04_Assumptions_Tab_Spec.md                ← constitutional (wrapper)
├── 04_Assumptions_Tab_Build_Plan.xlsx        ← constitutional (executable)
├── Model Execution Rules.md                  ← supporting (mandatory ref)
├── 2025 Anchors from Q4_25.md                ← supporting (calibration targets)
├── Stale_Row_Map.md                          ← supporting (what to avoid)
├── Assumptions Review V30.5.xlsx             ← supporting (V30.5 input catalogue)
├── SpaceX Model V30.5.xlsx                   ← reference (the old model)
├── SpaceX Valuation Model Q4'25 CLEANUP.xlsx ← reference (anchor source)
└── archive/legacy-build-2026-05-08-to-05-19/ ← 36 superseded spec docs (don't re-introduce)
```

When a sprint runs:
- Spec author writes `Sprint_N_Spec.md` in the workspace folder
- Plugin execution chat saves output workbook as `SpaceX_Model_v2_S[N].xlsx` (or similar) in the workspace folder
- Both chats append a row to the Claude Log tab on the workbook

---

## If you are starting fresh and feel lost

Read this README (you're doing it).
Then read constitutional doc 02 (Architecture & Methodology) — that's the structural anchor for everything.
Then check `project-rebuild-v2-status` memory for current sprint progress.
Then ask Vlad what sprint we're on.

Do not start writing cells, drafting specs, or making architectural decisions until you have read 02_Architecture_and_Methodology.md and confirmed the Rule Compliance Preamble in any spec you're executing.
