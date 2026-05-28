# Sprint Chat Workflow — Onboarding for plugin-new collaborators

This explains the two-chat split, the kickoff protocol, and the mechanical loop that gets a sprint from spec to PASS.

If you've already run Mach33 plugin sprints, skim and move on. If you haven't, read this end-to-end before opening your first chat.

---

## The two-chat split

Every sprint has two distinct phases, run in **separate Claude chats**:

### Chat 1 — Spec author

A planning chat. You discuss with Claude what the next sprint should do, draft the spec, debate trade-offs, and lock the architecture amendments. Output is a single `Sprint_NN_Spec.md` file.

This chat is **conversational**. Lots of "what if we…", "the V30.5 lesson here says…", "how does this interact with the queue gate…". Claude has time to think; you have time to push back.

### Chat 2 — Plugin execution

An execution chat. You attach the spec + a short kickoff prompt. Claude calls the Office.js Excel plugin to actually write formulas into the workbook. The chat is structured: pre-flight probes → §3.1 → §3.2 → … → calibration check → halt or PASS.

This chat is **mechanical**. Claude is following the spec. If you find yourself debating architecture in the execution chat, you're in the wrong chat — go back to a spec-author chat, amend the spec, then come back.

**Why the split:** the architecture debate and the execution checklist need different cognitive modes. Mixing them is how Sprint 11d collapsed — late-stage architecture amendments inside an execution chat trigger calc engine corruption + the plugin loses track of which version of the spec it's following.

---

## The mach33-model-build skill

`00_Constitutional_Docs/mach33-model-build-SKILL.md` is the skill that powers BOTH the spec-author chat and the plugin-execution chat. It embeds the 23 Execution Rules, the 23 Lessons Learned, and the architectural patterns.

When you're ready to use it in your Claude Project:

1. Open Claude Desktop, go to Settings → Custom Skills (or however your version exposes skills)
2. Add a new skill, paste in the contents of `mach33-model-build-SKILL.md`
3. The skill auto-triggers on any prompt mentioning "sprint", "rebuild the model", "anchor-and-offset", "allocator", "per-sat IRR", etc.

If your Claude Project doesn't surface custom skills, you can paste the skill contents at the top of your first message in each chat.

---

## Sprint kickoff protocol (mandatory)

Every sprint chat — spec-author OR plugin-execution — opens the same way:

1. Read `00_Constitutional_Docs/00_README_Sprint_Kickoff.md`
2. Read the relevant spec (`Sprint_NN_Spec.md`)
3. Read `00_Constitutional_Docs/Model Execution Rules.md` if you haven't recently
4. Open the chat with the **Rule Compliance Preamble** (template inside Execution Rules)

The Rule Compliance Preamble is a checklist Claude fills in at the top of its first message. It confirms which of the 23 rules apply to this sprint and how each will be honored. Don't skip it — it's how you catch spec violations before they cost you a 2-hour plugin run.

Per Vlad: `project_sprint_kickoff_protocol.md` is mandatory reading for every sprint chat. The kickoff README in this package is the canonical text.

---

## Mechanical loop — running a plugin execution chat

A typical plugin chat looks like this:

```
You:    [attach Sprint_NNf_Spec.md + SpaceX Model VX.YZ.xlsx]
        Execute Sprint NNf per the attached spec.

Claude: [reads spec]
        [posts Rule Compliance Preamble]
        [runs §5.0 pre-flight — calc engine probe, baseline reads]
        [reports baseline state]
        OK to proceed with §5.1?

You:    Proceed.

Claude: [writes §5.1 formulas via plugin]
        [posts read-back of D / I / S / AC for each new row]
        [verifies anchor + offset values match spec]
        §5.1 PASS. Proceed to §5.2?

You:    Proceed.

[…repeat for each section…]

Claude: [§6 calibration check]
        Sprint NNf PASS — N/N anchors hit
        Group Revenue 2050 = $X (target $Y)
        R108 conservation = "OK" all years
        [hands back to you with summary + open threads]

You:    Save the workbook. End chat.
```

If anything breaks mid-sprint, Claude is supposed to **halt** per Rule 15 — not improvise a fix. You decide whether to amend the spec (new spec-author chat) or roll back.

---

## Calc-engine sanity protocol (read before your first plugin chat)

Before any plugin execution chat that adds new Assumptions rows AND references them cross-tab, do this:

1. Plugin writes `=Assumptions!$A$2` to a scratch cell (e.g., `Allocator!Z200`)
2. Plugin forces `calculate(full)` + `context.sync()`
3. Plugin reads the scratch cell
4. Expected: Assumptions A2 text. If 0 or empty → calc engine corrupted → HALT, save + fully quit Excel + reopen
5. Clear scratch cell

This is the mitigation for the **assumptions write-then-reference footgun** (see Memory Snapshot Section 2.1). Skip this at your peril — it has killed two sprints.

The protocol is codified in Roadmap §10.3. The plugin skill should run it automatically when the spec opens with "if any new Assumptions row is added…", but verify your spec has the §5.0 pre-flight block.

---

## Vlad's role in the loop

- **Saving the workbook**: Vlad's job (Execution Rule 19). The plugin never auto-saves. After each section PASS the plugin posts a "ready for save" marker; Vlad saves in Excel before the next section runs.
- **File versioning**: Vlad's job. Specs do not name workbook files. Vlad handles V2.16 → V2.17 → V2.18 naming.
- **Mid-sprint architecture decisions**: Vlad calls. If the plugin surfaces an ambiguity, it asks. Don't decide for Vlad.
- **Sprint kickoff timing**: Vlad decides when a sprint is ready to execute. Don't start an execution chat without his go.

---

## Common newcomer mistakes (avoid these)

1. **Running the plugin chat without reading the spec first.** Claude has to be primed with the spec before the Rule Compliance Preamble means anything.
2. **Mixing spec authoring and execution in the same chat.** See "the two-chat split" above. This is the #1 way sprints collapse.
3. **Skipping the calc engine sanity probe.** If the spec adds Assumptions rows, the §5.0 probe is non-optional.
4. **Improvising a fix mid-sprint.** Per Rule 15, halt and go back to spec-author. Don't write your way out of a bug in the execution chat.
5. **Using row numbers instead of canonical labels.** Per Rule 12. Allocator rows have shifted multiple times; label-based reads survive, row-based reads silently break.
6. **British spelling.** Per Vlad lock 2026-05-26, US English everywhere. (See Memory Snapshot Section 3.5.)
7. **Surfacing version letters/numbers in status discussion.** Per Vlad lock 2026-05-27. Describe state, not filename.

---

## When to ask Vlad before proceeding

- You hit a halt condition the spec doesn't cover
- You think the spec has a real bug (not a typo — a logic bug)
- The calibration target seems unreachable
- A new architectural amendment seems necessary mid-sprint
- The workbook is in an unexpected state when you open it

Default: when in doubt, halt and ask. Re-running a failed sprint costs an hour; running through a real bug costs a day.
