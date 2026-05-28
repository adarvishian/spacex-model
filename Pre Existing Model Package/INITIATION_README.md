# SpaceX Model Rebuild — Collaborator Initiation Package

**Prepared 2026-05-27 by Vlad.** For [Colleague A] and [Colleague B] — please read this in full before opening anything else.

---

## What this is

Vlad has been rebuilding the Mach33 SpaceX valuation model from scratch since mid-May, executing it as a sprint-by-sprint plugin build against an Excel workbook. The model is partway through Sprint 11 — Sprint 11e shipped 2026-05-26, Sprint 11f (architectural rework) is spec'd but not executed.

He's bringing you both in to help close it out by tomorrow night. This package contains everything you need to spin up your own Claude Project and start working in parallel.

**Direction (continue current state vs fresh restart) is decided tomorrow with Vlad.** This package supports either path.

---

## What's in the package

```
Initiation_Package/
├── INITIATION_README.md                  ← you are here
├── 00_Constitutional_Docs/               ← read these regardless of direction
│   ├── 00_README_Sprint_Kickoff.md       ← mandatory kickoff protocol
│   ├── 01_Lessons_Learned.md             ← 23 lessons through Sprint 9
│   ├── 02_Architecture_and_Methodology.md ← the architecture spec — most load-bearing doc
│   ├── 03_Sprint_Roadmap_and_Verification.md ← roadmap + §6.8 calibration targets
│   ├── Model Execution Rules.md          ← 23 rules every spec opens with
│   ├── mach33-model-build-SKILL.md       ← the Claude skill that powers sprint chats
│   └── Mach33 Modelling Constitution.docx ← original constitution (reference)
│
├── 01_Current_State/                     ← if continuing current model
│   ├── STATUS_2026_05_26.md              ← READ FIRST — where the model is right now
│   ├── SpaceX Model V2.16.xlsx           ← the live workbook
│   ├── Sprint_11f_Spec.md                ← next sprint to execute (architectural rework)
│   ├── Sprint_11e_Spec.md                ← what just shipped
│   ├── Sprint_11e_Kickoff_Prompt.md
│   ├── Sprint_11d_Kickoff_Prompt.md      ← the sprint that collapsed (for context)
│   ├── Sprint_11c_Spec.md / _Kickoff
│   ├── Sprint_11b_Kickoff_Prompt.md
│   ├── Sprint_11_Spec.md                 ← original combined Sprint 11 spec
│   ├── Sprint_10_8_Spectrum_License_Fee_Spec.md ← predecessor patch
│   └── Customer_Launch_IRR_Fix_Plan.md   ← adjacent open thread
│
├── 02_Fresh_Restart_Inputs/              ← if restarting from scratch
│   ├── SpaceX Model V30.5.xlsx           ← legacy baseline (architectural template)
│   ├── SpaceX Valuation Model Q4'25 CLEANUP.xlsx ← Q4'25 cleanup baseline
│   ├── Assumptions Review V30.5.xlsx
│   ├── 2025 Anchors from Q4_25.md        ← Q4'25-locked anchors for Sprint 0
│   ├── 04_Assumptions_Tab_Spec.md / .xlsx
│   ├── Sprint_0_Spec.md                  ← where the rebuild starts
│   ├── Sprint_0_Plugin_Prompt.md
│   ├── SpaceX S-1 vs Mach33 Model — Variance Analysis.xlsx
│   ├── SpaceX S-1 vs Mach33 Model — Webinar Notes.docx
│   └── S1_Import_Plan_2026_05_20.md
│
├── 03_Sprint_History/                    ← reference for either path
│   └── Sprint_1 through Sprint_10.7 specs + key kickoff prompts
│
├── 04_Module_Briefs/                     ← per-person assignments
│   ├── Colleague_A_Brief_AI_Stack.md
│   └── Colleague_B_Brief_Deployment_Binding.md
│
├── 05_Reference_Material/                ← research base + adjacent docs
│   ├── Mach33 Model Build — Epistemic Base.zip   ← full research archive
│   ├── Research_to_Model_Improvements_2026-05-20.md
│   ├── AI_Stack_Module_Architecture_Scoping.md
│   └── Mach33_Weekly_Analysis_Execution_Rules.md ← prose constitution (not modelling)
│
└── 06_Memory_Snapshot/                   ← Vlad's accumulated locks
    ├── MEMORY_SNAPSHOT_CRITICAL_LOCKS.md  ← READ SECOND — the rules you must know
    └── SPRINT_CHAT_WORKFLOW.md           ← READ THIRD — how plugin chats work
```

---

## Setting up your own Claude Project

1. Open Claude Desktop → Projects → New project. Name it something like `SpaceX Model Rebuild — [your name]`.
2. Attach the entire `Initiation_Package/` folder as project knowledge. (Alternatively, attach selectively — see "Reading order" below for the priority order.)
3. Confirm the `mach33-model-build` skill is available. If your Claude Project doesn't surface custom skills, paste the contents of `00_Constitutional_Docs/mach33-model-build-SKILL.md` at the top of your first chat in the project.
4. Confirm Cowork or Excel plugin access (you'll need it for the execution chats).

If you have any problems with project setup, ping Vlad before you start working — the skill being unavailable will silently produce wrong-shaped output.

---

## Reading order (do not skip)

In this exact order. About 2 hours total.

1. **This file** — 5 min
2. `06_Memory_Snapshot/MEMORY_SNAPSHOT_CRITICAL_LOCKS.md` — 15 min — the architectural locks + Excel footguns + process meta-lessons
3. `06_Memory_Snapshot/SPRINT_CHAT_WORKFLOW.md` — 10 min — two-chat split, sprint kickoff protocol, mechanical loop
4. `00_Constitutional_Docs/00_README_Sprint_Kickoff.md` — 10 min — mandatory kickoff protocol
5. `00_Constitutional_Docs/Model Execution Rules.md` — 20 min — the 23 rules
6. `00_Constitutional_Docs/02_Architecture_and_Methodology.md` — 45 min — skim §1-5, read §6, §10, §18, §20 carefully
7. `00_Constitutional_Docs/01_Lessons_Learned.md` — 30 min — accumulated lessons
8. `01_Current_State/STATUS_2026_05_26.md` — 10 min — where the model is right now
9. **Your assigned module brief** (`04_Module_Briefs/Colleague_[A|B]_Brief_*.md`) — 10 min

Then start reading the specific spec(s) for your assignment.

---

## Two paths — decided tomorrow with Vlad

### Path 1: Continue current state

Execute Sprint 11f (deployment binding architectural rework) against V2.16. Sprint 11f spec is already drafted; the architecture work is the highest-value open thread.

Workbook to use: `01_Current_State/SpaceX Model V2.16.xlsx`

Primary docs: everything in `01_Current_State/`, plus `00_Constitutional_Docs/`.

You can ignore `02_Fresh_Restart_Inputs/` if you go this path.

### Path 2: Fresh restart from inputs

Execute Sprint 0 → Sprint 11 from scratch using V30.5 + Q4'25 anchors as inputs. Slower (~30+ hours of sprint runtime) but produces a model with no V2.13-V2.16 cruft.

Workbooks to use: `02_Fresh_Restart_Inputs/SpaceX Model V30.5.xlsx` + `SpaceX Valuation Model Q4'25 CLEANUP.xlsx`

Primary docs: `02_Fresh_Restart_Inputs/` + `00_Constitutional_Docs/` + `03_Sprint_History/` (you'll execute these specs in order).

You can ignore `01_Current_State/` if you go this path — but read `STATUS_2026_05_26.md` anyway for context on where the prior attempt got stuck.

### How the split works either way

You and the other colleague work in parallel:

- **One** of you takes the AI Stack module (Brief A). Independent dependency path — can start regardless of which direction Vlad picks.
- **One** of you takes Sprint 11f deployment binding (Brief B). Becomes "execute Sprints 0-10 first, then 11f" if Vlad picks fresh restart.

Vlad assigns who takes which brief.

---

## What to NOT do

These are the most common ways to waste a day of sprint runtime. Memory Snapshot covers each in detail; the quick list:

- **Don't run plugin chats and spec-author chats in the same chat.** The two-chat split is non-negotiable.
- **Don't add Assumptions rows and reference them cross-tab without save+reopen.** This is the calc engine corruption footgun (Memory 2.1).
- **Don't write demand rows that read actual CapEx.** This is the Sprint 11d circular-dep bug (Memory 2.7).
- **Don't use row numbers.** INDEX/MATCH on canonical labels only (Execution Rule 12).
- **Don't surface version letters/numbers in status discussion.** Describe state, not filename (Memory 3.2). Vlad handles versioning.
- **Don't fleet-seed to escape circular deps** (Memory 1.5).
- **Don't write British English.** US English everywhere (Memory 3.5). Common slips: modelling, programme, behaviour, defence, colour, centre, organisation, optimisation, recognise, labelled. Note: "analyses" (plural noun) is identical in US/UK — don't over-correct.
- **Don't decide architecture for Vlad mid-sprint.** Halt and ask.

---

## When to ping Vlad

- Before your first plugin execution chat — confirm baseline workbook state
- If you hit a halt condition the spec doesn't cover
- If the calibration target seems unreachable
- If you think the spec has a real logic bug (not a typo)
- If the workbook is in an unexpected state when you open it

Default: when in doubt, halt and ask. Re-running a failed sprint costs an hour; running through a real bug costs a day.

---

## Exit criteria for the handoff

By end of tomorrow you should be:

- Set up in your own Claude Project with skill loaded
- Through the reading order
- Aligned with Vlad on direction (continue current vs fresh restart)
- Assigned to a specific module brief
- Ready to open your first spec-author or execution chat

By end of day after tomorrow you should have:

- (Brief A) AI Stack standalone workbook tab built per scoping doc, integration spec drafted
- (Brief B) Sprint 11f PASS — deployment binding wired, conservation = OK, no circular dep

Good luck. Read the memory snapshot before anything else.

— Prepared by Claude for Vlad, 2026-05-27
