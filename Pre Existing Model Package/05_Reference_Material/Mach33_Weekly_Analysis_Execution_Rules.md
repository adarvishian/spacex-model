# Mach33 Weekly Analysis: Execution Rules (Constitution v1.0)

**Scope:** Long-form weekly analyses published on research.33fg.com. Downstream deliverables (X posts, newsletter intros, news briefs, client emails) are governed elsewhere and inherit some, but not all, of the rules below.

**Status:** v1.0, locked 2026-05-26. Constitutional layer above the operational skills (mach33-weekly-analysis, mach33-audit, stop-slop, mach33-bolding, tim-farrar, mach33-thesis-library). Names the load-bearing prose patterns, numbers the rules so they can be cited in chat ("Rule 17 violation"), and promotes known failure modes to named lessons.

**Parallel:** This is the prose-side equivalent of the SpaceX rebuild-v2 modeling constitution. The modeling side has Sprint Kickoff Protocol, Rule Compliance Preamble, Architecture, 23 Execution Rules, 23 Lessons Learned, Calibration Targets. This document is the same shape, applied to the writing.

---

## §0 Article Kickoff Protocol (READ FIRST)

Mandatory at the start of every weekly-analysis chat, before any scoping, charting, or drafting.

**Step 1.** Read this constitution in full. It is short.

**Step 2.** Read `mach33-weekly-analysis` SKILL.md. That is the operational pipeline. This constitution governs the prose; the skill governs the workflow.

**Step 3.** If the analysis touches any SpaceX revenue line, ODC, Starlink, Starship, P2P, AI Stack, or the SpaceX investment story generally, read `mach33-thesis-library`. Use the canonical phrasings verbatim where they fit. Do not re-derive a thesis Vlad has already signed off on.

**Step 4.** State the Voice Compliance Preamble (see §5) in the chat. This is the equivalent of the modeling Rule Compliance Preamble: it signals that the rules below are loaded and will be applied throughout.

**Step 5.** Lock the seven scoping elements before moving to charts (see §2 and the mach33-weekly-analysis skill). Do not draft prose against an unconfirmed scope.

**Step 6.** Lock the chart plan before drafting. The analysis is written around the charts, not the other way around (see Pattern 3, §3).

**Step 7.** Draft section by section, presenting each for review unless Vlad asks for a full draft at once.

**Step 8.** Run the full Publication Gate before anything ships (see §7). No exceptions.

Skipping steps is the single most common failure mode. The modeling side learned this the hard way across thirty refine specs before the rebuild. The prose side does not need to repeat the lesson.

---

## §1 Analysis Architecture

The standard weekly analysis has six sections. Each exists for a specific reason. Cross-section bleed (an Exec Summary that reads like a Body section, a Body section without its chart, a Bottom Line that restates the Exec Summary verbatim) is an architectural failure, not a style issue.

```
# Title                            Declarative, thesis-forward, contains a claim or a number.
## Summary                         3 to 6 sentences. Free preview. Standalone hook. Sells the paywall.
# Executive Summary                4 to 8 bullets. Each bullet a conclusion with a bold lead-in
                                   phrase and at least one specific number.
# Analytical Section 1             Framework or methodology setup. Chart 1 sits here.
# Analytical Section 2             Core argument with data. Chart 2 sits here.
# Analytical Section N             As many as the argument needs. Each has a chart unless the
                                   prose argument is strong enough to stand on numbers alone.
# Investor Takeaways / Bottom Line 3 to 6 numbered or bulleted points reframed for capital
                                   allocators. Forward-looking, more opinionated than the body.
# Sources & References             On deeper analyses. Properly cited, tier-graded.
```

**Vending-machine equivalent (Pattern 7).** Each analytical section is a self-contained vending machine: one argument in, one chart, one to three interpretation paragraphs, one investment-relevant conclusion out. R&D, framing, and meta-commentary live at the document level (Summary, Exec Summary, Bottom Line), not inside the analytical sections.

**Why this matters.** Institutional readers skim. A PM reads the Summary (decides whether to keep reading), reads the Exec Summary (decides whether to read the body), skims the chart titles and bolded phrases in the body (decides whether to read in full), reads the Bottom Line (decides what to do). The architecture has to support each of these read paths in isolation. The Summary that requires the Exec Summary to make sense has failed. The Exec Summary that requires reading the body to interpret has failed. The Bottom Line that doesn't connect findings to capital allocation has failed.

---

## §2 The Prose Pipeline

Five phases, sequential, in one chat thread. Each phase ends with explicit Vlad sign-off before the next begins.

```
1. SCOPE    Lock thesis, contrarian angle, scope IN/OUT, key findings,
            data foundation, series context, investor frame.
2. CHARTS   Lock chart titles, types, what each shows, the insight, data source,
            placement. The analysis will be written around these.
3. OUTLINE  Section-by-section structure with chart placement mapped. Word
            count estimate per section. Key data points named.
4. DRAFT    Write section by section. Apply all Execution Rules (§4) throughout.
5. REVIEW   Phase 5 checklist from mach33-weekly-analysis, then the full
            Publication Gate (§7).
```

**Phase locks are load-bearing.** The modeling side enforces "no formula written against an unconfirmed assumption". The prose side enforces "no prose written against an unconfirmed scope or chart plan". Drafting before the scope is locked produces beautiful sentences arguing for the wrong thesis. Drafting before the chart plan is locked produces prose that hand-waves where a chart belongs.

**The phase-lock rule has one exception.** If during drafting the writer discovers a load-bearing scope or chart change (a finding contradicts the thesis, a chart turns out to be unbuildable, a section needs to be added or cut), the writer pauses the draft, surfaces the change to Vlad, and gets a new scope or chart sign-off before resuming. The pause is mandatory. Continuing to draft against a contradicted scope is the prose equivalent of writing formulas downstream of a broken anchor cell.

---

## §3 Load-Bearing Patterns

Named patterns. Cite by name in chat ("the Thesis Anchor is doing the work here", "this section breaks Conclusion-not-Topic"). The names are deliberate. Pattern-by-name beats principle-by-paragraph for daily use.

### Pattern 1. Thesis Anchor

The thesis statement is the prose equivalent of an anchor cell. Every section, every chart, every Exec Summary bullet, every Bottom Line point should be traceable back to it. If a paragraph cannot be defended as "this advances the thesis by establishing X", the paragraph is either misplaced or unnecessary.

**Why:** Modeling drift happens when downstream cells stop referencing the anchor. Prose drift happens when downstream paragraphs stop arguing the thesis. Same failure, different medium.

**How to apply:** During the Outline phase, write the thesis statement at the top of the outline doc and explicitly state, for each section, the one sentence connecting the section back to the thesis. If the sentence is hard to write, the section is the problem.

### Pattern 2. Variant Perception Inversion

Every Mach33 analysis has a contrarian angle. The piece exists because consensus is wrong, incomplete, mis-framed, or behind the data. If the analysis cannot state what conventional wisdom it is correcting, it is a briefing, not an analysis, and it should not ship as a weekly.

**Why:** Mach33's value to a buy-side reader is variance from consensus, not summary of consensus. A piece that says what every other shop is saying gives the PM nothing actionable.

**How to apply:** Scope phase requires "contrarian angle" as one of the seven locks. The angle should appear in the Summary, be implicit in the Exec Summary bullets, and be the spine of at least one Body section.

### Pattern 3. Chart-as-Argument

Charts are scoped before writing. The analysis is written around the charts, not the other way around. Each chart exists to make a specific numerical argument visible. Prose orbits the chart and walks the reader through what the chart shows, what assumptions feed it, and what conclusion it forces.

**Why:** A chart added late as decoration is decoration. A chart that the prose was built around is an argument. The reader looks at the chart first; the prose has to earn the right to be read.

**How to apply:** Chart Plan phase comes before Outline phase. Every chart has a stated insight, written down, before any prose around it is drafted. If a chart cannot be summarized in one sentence of insight, it is the wrong chart.

### Pattern 4. Conclusion-not-Topic

Every Executive Summary bullet, every Bottom Line point, every analytical paragraph opening sentence is a conclusion. Topics are banned in load-bearing positions. "We examine chip costs" is a topic. "Chip architecture is the decisive variable, with the bear case starting at $132B per GW and never reaching parity" is a conclusion.

**Why:** A topic forces the reader to read the rest of the paragraph to find the conclusion. A conclusion lets the reader decide in three seconds whether to keep reading. Institutional time is the binding constraint.

**How to apply:** Self-check on every Exec Summary bullet and every Bottom Line point: does this sentence state what we concluded, or does it announce what we discussed? If the latter, rewrite.

### Pattern 5. Specific-Number-per-Paragraph

Every analytical paragraph carries at least one specific number. Specific means a figure with units and basis: "$226 to $233 per kg", "12.5x LTV to CAC", "40 to 50x gains by 2030", "100/20 in the busy hour for 40 percent of locations". Vague magnitudes ("over $100B", "significant gains", "high churn") fail this pattern.

**Why:** This is the prose equivalent of a model's calibration target. A paragraph without a number is a paragraph without a calibration. The reader cannot anchor.

**How to apply:** Final review walks every analytical paragraph and tags the carrying number. Paragraphs without a number get rewritten to carry one, or get cut. Methodology paragraphs and section-opening framing sentences are exempt; everything else is not.

### Pattern 6. Free-Preview Discipline

The Summary section is what non-subscribers see. It must convey the full thesis and make the paywall worth crossing on its own merits, without leaning on the Exec Summary or the body for context. It is a standalone document.

**Why:** Conversion to paid sits on this paragraph. A Summary that just teases without delivering the thesis loses the conversion. A Summary that delivers too much obviates the rest.

**How to apply:** Write the Summary last, after the rest of the analysis is locked. Read it in isolation. Ask: if I read only this, would I (a) understand the thesis, (b) want to read more, and (c) trust that Mach33 has the work behind it? If any answer is no, rewrite.

### Pattern 7. Vending-Machine Sections

Each analytical section is self-contained. One framework or argument in, one chart, one to three interpretation paragraphs, one investment-relevant takeaway out. Methodological hedging, scope caveats, and meta-commentary live at the document level, not inside the section. The section reader should be able to extract the section's contribution to the thesis without context from other sections.

**Why:** Same as the modeling vending machine. Cleanly bounded units compose into a clean whole. Sections that leak into each other produce analysis where nobody can tell what argument lives where.

**How to apply:** Each section's first sentence states the section's contribution. Each section's last sentence states the section's conclusion. The two should be traceable to each other and to the thesis.

### Pattern 8. Investor-Frame Closer

Every analysis ends in capital-allocation terms. Bottom Line / Investor Takeaways translates the analytical findings into entry timing, position sizing, risk identification, thesis validation, or competitive positioning. Without this, the analysis is academic.

**Why:** Mach33's audience is institutional. Findings that are intellectually interesting but not investment-actionable get read, admired, and not paid for.

**How to apply:** Scope phase locks the investor frame as one of the seven elements. Bottom Line section is mandatory, never an afterthought. The final point should be the broadest strategic implication, not a narrow tactical observation.

### Pattern 9. Scope Lock

Scope IN and scope OUT are named at the Scope phase and held throughout. A finding that lives outside the scope gets flagged as future work, not absorbed into the current analysis. A tangent that wants to be a paragraph gets either justified by tying it to the thesis or cut.

**Why:** Mach33 analyses are disciplined about scope. A piece that promised "the economics of orbital compute" and detoured into Mars architecture has broken faith with the reader. Scope discipline is also the only defense against analyses that swell from 1,500 to 5,000 words because every related thing seemed worth saying.

**How to apply:** Outline phase explicitly references the locked scope IN / OUT. Every section has to clear the IN test. Drafting that surfaces scope drift triggers a pause and a scope conversation, not a quiet absorption.

### Pattern 10. Series Anchor

Most Mach33 analyses sit in a series (Orbital Compute, Starlink / Connectivity, DTC, Launch Economics, Mars / Lunar, SpaceX Quarterlies, Industry / Thematic). Each analysis cross-references prior work in the series. Internal links to prior pieces appear at the points where the prior framing is doing load-bearing work.

**Why:** The series is the moat. Each piece compounds the prior pieces. A standalone analysis that ignores the series treats every reader as new and burns the compounded credibility.

**How to apply:** Scope phase locks "series context: standalone / part N of series, prior pieces". Outline phase identifies where prior pieces get cross-referenced. Draft phase places the links inline using `[title](/analysis/slug)`.

### Pattern 11. Source-Frame Fidelity

Mach33's wording is governed by the source's wording. We do not upgrade verbs ("shows" stays "shows", does not become "reveals"). We do not add modifiers the source did not write ("$400M total" does not become "$400M through the equivalent stage"). We do not promote inference to observation ("indicates" stays "indicates", does not become "confirms"). Editorial upgrades, when warranted, are explicit Mach33 framing, not silent paraphrase.

**Why:** A buy-side reader who pulls the source and compares wording loses trust if the wording has been quietly amplified. Source-frame drift is the single most insidious factual failure because each individual upgrade looks defensible.

**How to apply:** Audit phase runs a phrase-by-phrase check between Mach33 wording and source wording. Any added phrase, any verb upgrade, any scope expansion gets flagged. Either the source supports it, or Mach33 owns it as an explicit view.

### Pattern 12. Bolding-as-Scan-Path

Bolds are not emphasis. Bolds are a scan path. A reader scanning only the bolded phrases across a paragraph should be able to follow the analysis: a sequence of specific entities, magnitudes, and named claims that together carry the meaning. Short noun phrases, typically 1 to 5 words, never verbs, 1 to 3 per paragraph, average across the deck or document landing near 1 per prose paragraph.

**Why:** Most readers scan first, then choose what to read in full. The bolds are what they read in scan mode. Bolds for emphasis (random phrases bolded for drama) collapse the scan path into noise.

**How to apply:** Bolding pass runs after the prose is locked, never during drafting. Apply Aaron's Rule: short noun phrase, not the verb, anchored in concrete content. See `mach33-bolding` for canonical examples and the Apps Script template.

### Pattern 13. Voice Lock

First-person plural ("we model", "we estimate", "our analysis indicates") throughout. Never first-person singular. Never third-person Mach33 ("Mach33 found that..."). Never anonymous narrator ("the analysis shows..."). The voice is institutional, technical, confident on model outputs, measured on timing, willing to contradict consensus when the evidence supports it.

**Why:** First-person plural carries the institutional weight. First-person singular sounds like a Substack. Third-person sounds like a press release. The voice is part of the credibility.

**How to apply:** Voice Compliance Preamble (§5) names this. Final review tags any first-person singular or third-person Mach33 slips.

### Pattern 14. Confidence Calibration

Confident on findings from Mach33's own models. Measured on timing predictions, using scenario ranges rather than point forecasts. Willing to state conclusions that contradict consensus when the evidence supports it. Caveats live in methodology notes, not buried in prose between hedge words.

**Why:** Hedging on model outputs ("we believe the model may suggest...") undercuts the entire reason for running the model. Conversely, point-estimate timing predictions are a credibility risk because most are wrong.

**How to apply:** Model outputs get "our model indicates" or "we estimate". Design opinions and judgement calls get "we believe". Timing predictions get scenario ranges (bear / base / bull, with years). Caveats get stated upfront in a methodology note, not sprinkled.

### Pattern 15. Closer as Reframe

The last paragraph of the analysis zooms out to a strategic or historical reframe. The best Mach33 closers leave the reader seeing the sector differently than they did before reading. The closer is not a summary of the analysis (the Exec Summary already does that), and it is not the Bottom Line (the Bottom Line is investor takeaways). It is the final move that recontextualises the findings.

**Why:** Memorable analyses end on a frame. Forgettable analyses end on a recap. The frame is what gets quoted in client conversations.

**How to apply:** Draft the closer last. Ask: does this paragraph change how the reader thinks about the sector, or does it summarize what they just read? If the latter, rewrite. Historical parallels, strategic implications, sector-wide reframes all work; recap does not.

---

## §4 Execution Rules

Numbered, citable, load-bearing. Reference in chat by number ("Rule 17 violation", "Rule 5 needs a number here", "Rule 23 says no verbs in bolds"). Each rule states the rule, the reason, and the application context.

### Rule 1. First-person plural throughout

"We model", "we estimate", "our analysis indicates", "we believe". Never "I". Never third-person Mach33.

**Why:** Institutional voice. See Pattern 13.

**Apply:** Every analytical sentence. Methodology notes can use passive constructions ("the model was calibrated against...") where the actor is the model itself, but the analytical voice stays first-person plural.

### Rule 2. US English throughout

Color, favor, defense, modeling, analyze, behavior, center, organization, optimization, program, recognize, realize, criticize, labeled, summarized, traveled, canceled.

**Why:** Mach33 house style. Vlad lock 2026-05-26: US English everywhere, overriding any prior British-English convention (including the older `mach33-weekly-analysis` SKILL.md which still references British English).

**Apply:** Final review runs a US-English spellcheck. Common slips to catch: modeling, program, behavior, defense, color, favor, center, organization, optimization, recognize, realize, criticize, analyze, labeled, summarized. Note: the mach33-weekly-analysis skill says British English. This constitution wins.

### Rule 3. No em-dashes, no en-dashes

Em-dashes (`—`) and en-dashes (`–`) do not appear in Mach33 prose. Stop-slop bans em-dashes; Mach33 house style additionally bans en-dashes. Replace with commas, periods, colons, or the word "to" for ranges.

**Why:** Em-dashes are an AI tell and a writer crutch. En-dashes look like em-dashes done wrong and confuse number ranges with date ranges. Mach33 prose holds the bar.

**Apply:** Search every draft for `—` and `–` and replace. "2024 to 2026" not "2024–2026". "Speed, quality, cost. Pick two." not "Speed, quality, cost—pick two." Note that the stop-slop skill's own Example 4 contradicts its own rule with an em-dash. The rule wins, the example does not.

### Rule 4. No emojis in the analysis body

Ever. The Mach33 voice is institutional.

**Why:** Self-evident.

**Apply:** Final review tags any emoji. Platform-side promotional materials (X posts, newsletter intros) follow their own rules; the analysis body does not.

### Rule 5. Every analytical paragraph carries at least one specific number

Specific means a figure with units and basis. See Pattern 5.

**Why:** Calibration. A paragraph without a number is a paragraph without a calibration target.

**Apply:** Final review tags the carrying number in each analytical paragraph. Paragraphs without one get rewritten or cut. Methodology and framing paragraphs exempt.

### Rule 6. Ranges over point estimates; bolded inline

Ranges in bold: **$226 to $233 per kg**, **40 to 50x gains**, **12.5x LTV to CAC**. Point estimates are reserved for cases where the underlying calculation has near-zero variance.

**Why:** Honest about uncertainty. Defensible to a sceptical reader who will assume any point estimate is precision theatre.

**Apply:** Draft uses ranges by default. The narrow range is fine. The two-significant-figure point estimate ("$226.50 per kg") is wrong unless the underlying calculation supports it.

### Rule 7. Charts at the point of argument, never collected at the end

Each chart sits inline where the argument it makes is being made. Charts collected at the end of the document is an academic convention, not a Mach33 convention.

**Why:** The reader is scanning. A chart at the point of argument participates in the argument. A chart at the end participates in nothing.

**Apply:** Outline phase places each chart in its section. Draft phase embeds as `### Chart Title` then the image embed then 1 to 3 interpretation paragraphs.

### Rule 8. Every chart followed by 1 to 3 interpretation paragraphs

The interpretation walks the reader through what the chart shows, what the salient features are, what the implication is. "As shown above" is banned. "The chart shows..." is banned. The chart is the argument; the prose interprets it.

**Why:** A chart without interpretation forces the reader to do the analytical work the analyst was supposed to do. A chart with weak interpretation ("the line goes up") wastes the chart.

**Apply:** Self-check on every chart. Ask: what does this chart force the reader to conclude, and is that conclusion stated in the prose?

### Rule 9. Exec Summary bullets are conclusions, not topics

See Pattern 4. "We examine X" is a topic. "X is the decisive variable, with a base case of Y at price Z" is a conclusion.

**Why:** The Exec Summary is the most likely read in isolation. Topics there waste the position.

**Apply:** Self-check on every Exec Summary bullet. Reword every topic into a conclusion or cut.

### Rule 10. Each Exec Summary bullet has a bolded lead-in phrase

The bolded phrase carries the thesis of the bullet. The following one or two sentences provide the supporting numbers. The bullet should be extractable as a standalone for a busy PM.

**Why:** Scan path. The reader skims the bolded phrases first, then reads bullets that earned attention.

**Apply:** Bolding rule: short noun phrase, no verb. See Rule 23.

### Rule 11. Scope IN / OUT named at scope phase, no drift in draft

The scope locked at Phase 1 is the scope held through to Phase 5. New scope is a scope conversation, not a quiet absorption.

**Why:** See Pattern 9. Scope drift produces bloated analyses that promise less than they deliver and deliver less than they promise.

**Apply:** When drafting surfaces tempting tangent material, write it down as future work and move on. If the tangent is load-bearing for the current piece, surface to Vlad as a scope amendment.

### Rule 12. Methodology stated upfront, caveats not buried

The model, framework, or analytical approach is named at the start of the section that uses it. Caveats live in a methodology note at the start of the analytical body or in the relevant section's opening, not threaded through prose between hedge words.

**Why:** Buried caveats read as either covering-the-bases or quiet hedging. Stated caveats read as analytical discipline.

**Apply:** Each analytical section that introduces a new framework opens with one sentence naming it. Limitations and assumptions get a methodology note section if substantial, or an opening sentence in the section that uses them if narrow.

### Rule 13. Hedging banned on Mach33 model outputs

If the model says it, state it. "Our model indicates **$132B per GW**" is correct. "Our model may suggest somewhere around $100B per GW" is wrong. The model has a number. State the number.

**Why:** Hedging on the model undercuts the reason for running the model.

**Apply:** Final review tags hedge words ("may", "could", "perhaps", "somewhere around") on model output statements. Replace with the model output. If the writer is hedging because they distrust the model, that is a modeling conversation, not a prose conversation.

### Rule 14. Confidence calibration

Model outputs: "our model indicates", "we estimate", "our analysis yields". Design opinions and judgement calls: "we believe". Timing: scenario ranges, not point forecasts. See Pattern 14.

**Why:** Differentiates Mach33 findings from Mach33 views from Mach33 predictions. Each has different epistemic weight; conflating them is a credibility risk.

**Apply:** Each sentence carrying a Mach33 claim should fit one of the registers. Mixing ("we believe the model proves") is wrong because "prove" overcommits and "believe" undercommits.

### Rule 15. Closer zooms out to strategic or historical reframe

See Pattern 15. The last paragraph is not a summary.

**Why:** Recap is forgettable. Reframe is what gets quoted.

**Apply:** Draft the closer last, in isolation. Ask whether it changes the reader's mental model of the sector.

### Rule 16. Quote canonical phrasings verbatim from the thesis library

For settled Mach33 framings (ODC thermodynamic triad, vending-machine SpaceX, V3 capacity, AI Stack orchestration layer, Starlink ARPU thesis, P2P, others), use the phrasings in `mach33-thesis-library`. Do not re-derive what Vlad has signed off on.

**Why:** Consistency across the catalog. A reader who sees three different framings of the same thesis across three Mach33 pieces loses trust in all three.

**Apply:** Before drafting any SpaceX-adjacent content, scan the thesis library for relevant entries. Use the canonical phrasing verbatim or near-verbatim. If a needed framing is missing, surface to Vlad rather than inventing one.

### Rule 17. Source-frame fidelity: verbs cannot upgrade the source

See Pattern 11. Source says "shows", Mach33 says "shows". Source says "indicates", Mach33 says "indicates". Source says "$400M total", Mach33 says "$400M total", not "$400M through the equivalent stage".

**Why:** Trust failure if a reader compares sources. Single largest source of insidious factual error.

**Apply:** Audit phase runs phrase-by-phrase comparison between Mach33 wording and source wording. Any verb upgrade, any added modifier, any scope expansion gets flagged. Either source-supported, or explicitly Mach33-framed ("Mach33 view: ...", "we expect...").

### Rule 18. Subject-verb logical consistency on every sentence, opening sentence unconditional

"SpaceX disclosed X in its confidential filing" is logically impossible. A confidential filing is by definition not a disclosure. The verb has to fit the action that actually happened. Common traps: "disclosed" + "confidential"; "announced" + "according to people familiar"; "ruled" + "opened a comment period"; "published" + "internal memo"; "revealed" + "private filing reviewed by Reuters".

**Why:** The opener sets the frame. Buy-side readers catch logical impossibilities in the first sentence. Once trust is lost there, the rest of the piece reads worse.

**Apply:** Audit phase reads the opening sentence in isolation and runs the subject-verb check. Fix is usually one verb swap: "submitted", "filed", "included in", "circulated internally", "was reported by". Default to passive constructions that pin disclosure on the news outlet, not the company, when the company has not in fact disclosed.

### Rule 19. Filing-type precision

S-1 is not DRS. OTA is not contract. NPRM is not R&O. IOC is not FOC. Mishap is not failure (FAA distinguishes formally). Use the precise term the legal or regulatory framework defines, not the colloquial trade-press substitute.

**Why:** Buy-side audience knows the difference. Loose terminology fails the sceptical reader test.

**Apply:** Audit phase verifies every filing type, regulatory action, and constellation lifecycle term against its precise meaning. See mach33-audit "Filing & terminology precision reference" for the canonical list.

### Rule 20. Comparison validity: A and B measure the same thing

"$15B Starship development vs $400M Falcon 9 development" is mathematically defensible and semantically misleading because Starship is mid-development and Falcon 9 is a 15-year-mature program. Every A-versus-B comparison gets a basis check before the ratio, multiple, or "Nx" framing is allowed.

**Why:** Apples-to-apples is the test. The reader will check.

**Apply:** Audit phase confirms what A is measuring, what B is measuring, and over what scope. If the measures aren't congruent, the comparison gets reframed (explicit basis statement) or recast (different B).

### Rule 21. Stale-figure probe: verify the latest, not the once-true

A figure correct on April 1 may be superseded on April 2. Verification against the original source is not enough; the probe asks "has this been updated".

**Why:** Mach33's $1.75T SpaceX IPO figure was correct on the day Reuters published. Bloomberg reported >$2T within 24 hours. An audit that confirms the original and stops there will green-light a stale number.

**Apply:** Audit phase searches for newer reporting on any actively evolving story after the cited date. "Verified at one point" is not "verified now".

### Rule 22. Forward-looking claims framed as Mach33 view or sourced

"Pre-IPO secondary tender activity will likely reference this figure as the floor" is a prediction. Either cite a source that made the prediction or frame as explicit Mach33 view ("we expect...", "Mach33 view: ..."). Predictions presented as observations are a fidelity failure.

**Why:** The reader can argue with a labeled prediction. The reader cannot argue with what appears to be a fact.

**Apply:** Audit phase tags every "will", "should", "is likely to", "expects to" claim. Each gets either a source or an explicit Mach33 frame.

### Rule 23. Bolding: noun phrases only, 1 to 3 per paragraph, no verbs

Short noun phrases, typically 1 to 5 words. Specific entities, magnitudes, named claims. Never verbs, articles, prepositions, conjunctions, generic emphasis words. 1 to 3 per paragraph, deck average near 1.1. Topic of the document is never bolded as a sub-phrase. See Pattern 12 and `mach33-bolding`.

**Why:** Bolds are a scan path, not emphasis. See Pattern 12.

**Apply:** Bolding pass runs after prose lock, via `mach33-bolding`. Self-check before delivery on every bolded phrase: noun? specific? scannable? stops at natural noun boundary?

### Rule 24. Charts described as visible argument, never "as shown above"

The interpretation paragraph names what the chart shows in plain language: "The curves asymptote at $226 per kg with booster-only reuse but drop to sub-$100 per kg with full-stack reuse by flight 3." Not: "As shown above, costs decline with reuse."

**Why:** "As shown above" tells the reader what the analyst should be telling them. The chart needs a guide, not a pointer.

**Apply:** Final review tags every "as shown", "the chart above", "see the chart" and rewrites to a substantive description of what the chart actually demonstrates.

### Rule 25. Cross-reference prior Mach33 analyses where relevant

Inline links: `[title](/analysis/slug)`. Place at the point where the prior framing is doing load-bearing work, not collected in a reading-list block.

**Why:** Series Anchor (Pattern 10). Compounds credibility, gives the reader a path into the catalog, signals depth.

**Apply:** Outline phase identifies cross-reference points. Draft phase places the links inline. Final review checks the links resolve.

### Rule 26. Tables tight: 3 to 6 rows, 2 to 4 columns, one argument per table

Tables are for structured comparisons that prose cannot carry cleanly (scenario inputs, cost stacks, ARPU breakdowns). They are not for dumping data. Each table makes one argument.

**Why:** A table with 12 rows and 6 columns is a data dump. The reader cannot scan it. The argument disappears in the grid.

**Apply:** Each table earns its existence by stating, in the surrounding prose, what the table shows. If the table needs more than 6 rows or 4 columns, it is either two tables or it is a chart.

### Rule 27. Scenarios defined before compared

Bear, base, bull scenarios get each defined explicitly before being compared. "Bear (~year): chip at price, launch vehicle at $/kg. Implies outcome." Then the comparison.

**Why:** A scenario comparison without defined scenarios is unfalsifiable. The reader cannot evaluate which scenario assumptions they agree with.

**Apply:** Section using scenarios opens with the scenario definitions, in a defined block. Subsequent prose compares.

### Rule 28. Numbers carry units and basis

"$132B" is wrong. "$132B per GW" is right. "$132B per GW in installed capex, 2030 dollars" is better. Point-in-time vs cumulative gets stated. Peak vs busy-hour vs average gets stated. Retail vs internal vs marginal gets stated.

**Why:** Number without unit is half a number. Number without basis is misleading. Buy-side readers will assume the worst basis if it isn't stated.

**Apply:** Audit phase tags every figure for units and basis. Methodology note states the standard basis used throughout the piece if one applies.

### Rule 29. URL fetch on every citation during audit

Every URL in the document gets fetched, not just the suspicious ones. Confirm resolution, confirm the URL content supports the cited claim, flag 404s, redirects, login walls, or non-supporting content.

**Why:** Dead URLs inherit through drafts. Slug-date deception (a /2026/04/ URL published in May). Cited support that the content does not in fact support.

**Apply:** Audit phase fetches every URL. Run unconditionally on every audit pass; do not trust prior verification.

### Rule 30. No publication without the full Publication Gate

Audit, stop-slop, bolding, Farrar (satcom only), final review. In that order. No exceptions.

**Why:** See §7.

**Apply:** See §7.

---

## §5 Voice Compliance Preamble

The opening declaration in any weekly-analysis chat. Equivalent of the modeling Rule Compliance Preamble. State this verbatim in the first message of the chat after the Article Kickoff Protocol (§0):

> Voice Compliance Preamble: I will draft this weekly analysis in Mach33 house voice. First-person plural throughout. US English. No em-dashes, no en-dashes. No emojis in the body. Every analytical paragraph carries at least one specific number with units and basis. Exec Summary bullets are conclusions with bolded lead-in phrases. Every chart sits at the point of argument and is followed by one to three interpretation paragraphs. Hedging is banned on Mach33 model outputs. Scope IN and OUT are locked at the scope phase and held. Canonical phrasings from the thesis library are used verbatim where they fit. The closer zooms out to a strategic or historical reframe. Before publication, the analysis goes through Mach33 audit, stop-slop, bolding, Farrar pass (if satcom), and final review. Reference the Execution Rules by number in chat ("Rule 17 violation", "Rule 5 needs a number") so corrections are unambiguous.

Stating the preamble at chat-start is not ceremonial. It loads the rules into the working context, gives Vlad a one-glance check that the rules are loaded, and creates a referenceable artifact so a mid-chat correction ("Rule 18, opening sentence subject-verb") lands without explanation.

---

## §6 Lessons Learned

Failure modes promoted to named lessons. Each lesson links back to the Rule it promoted (or that should govern it). Cite in chat ("this is the disclosure-verb trap, Lesson 1, Rule 18").

### Lesson 1. Disclosure-verb trap

"SpaceX disclosed X in its confidential filing" is logically impossible because confidential filings are by definition not disclosures. Reuters disclosed (by reporting); SpaceX submitted. Common variants: "announced" + "according to people familiar"; "ruled" + "opened a comment period"; "published" + "internal memo"; "revealed" + "private filing reviewed by Reuters".

**Promoted to:** Rule 18 (subject-verb logical consistency on every sentence, opening sentence unconditional).

**Origin:** May 2026 SpaceX comp-package audit. The audit verified the contents of the filing but waved through the verb describing how those contents reached the public.

### Lesson 2. Editorial verb creep

Source says "shows", Mach33 says "reveals". Source says "first hard public number", Mach33 says "now exceeds". Source says "indicates", Mach33 says "confirms". Each upgrade adds drama or certainty the source did not claim. Not always wrong, but every upgrade should be a deliberate Mach33 choice.

**Promoted to:** Rule 17 (source-frame fidelity).

**Origin:** Recurring. Identified during multiple audit passes on news briefs and weekly analyses.

### Lesson 3. Source-frame drift

"$400M through the equivalent stage of its program". Reuters said "$400M total Falcon 9 development cost". The "equivalent stage" qualifier was a Mach33 addition that distorted the comparison. Phrase-by-phrase check between Mach33 wording and source wording catches this.

**Promoted to:** Rule 17 (source-frame fidelity).

**Origin:** SpaceX comp-package audit. Single most insidious factual failure because the underlying number was correct.

### Lesson 4. Filing-type imprecision

Calling a Draft Registration Statement an "S-1", calling an OTA award a "contract", calling an NPRM an "R&O". The buy-side knows the difference.

**Promoted to:** Rule 19 (filing-type precision).

**Origin:** SpaceX DRS coverage, multiple FCC orders. Always default to the precise regulatory term until the public document exists.

### Lesson 5. Stale-figure-was-once-correct

A figure correct on April 1 may be wrong on April 2. The $1.75T SpaceX IPO target was correct on the day Reuters published. Bloomberg reported >$2T within 24 hours. Audit that stops at the original source green-lights a stale number.

**Promoted to:** Rule 21 (stale-figure probe).

**Origin:** April-May 2026 SpaceX IPO coverage.

### Lesson 6. Topic vs substance (bolding)

Bolding "frontier model training" as a sentence opener when the substance is "multiple gigawatts per training run" later in the paragraph. Bolding the topic of the document anywhere in the prose (do not bold "orbital compute" in a report titled "The Economics of Orbital Compute").

**Promoted to:** Rule 23 (bolding: noun phrases only).

**Origin:** Bolding-pass testing on past Mach33 reports. Single biggest mistake in bolding when reasoning from intuition rather than the canonical examples.

### Lesson 7. Over-bolding default

Bolding 3 phrases per paragraph by default. Correct rate is closer to 1.1 bolds per paragraph across a full deck. Start tight and add only if a paragraph genuinely has multiple scannable beats.

**Promoted to:** Rule 23 (bolding: 1 to 3 per paragraph, deck average near 1.1).

**Origin:** Bolding-pass testing.

### Lesson 8. Forecast laundering

A bank's price target or analyst forecast repeated as if it were a Mach33 view. Be explicit about whose forecast it is and where it came from.

**Promoted to:** Rule 22 (forward-looking claims framed as Mach33 view or sourced).

**Origin:** Recurring across newsletter intros and weekly analyses.

### Lesson 9. Comparison distortion

"$15B Starship vs $400M Falcon 9 = 38x" is mathematically correct but semantically misleading. Starship is mid-development. Falcon 9 is 15 years mature. The ratio either gets reframed as an explicit Mach33 view ("by this measure...") or recast against a like-for-like comparison.

**Promoted to:** Rule 20 (comparison validity).

**Origin:** SpaceX coverage. Common Mach33 trap because the firm builds ratios out of the available numbers without basis checks.

### Lesson 10. Wire service inheritance

Trade press repackages a Reuters story but adds an interpretive flourish. The flourish gets cited as fact. Always trace back to the original wire.

**Promoted to:** Source tier discipline (§8) and Rule 29 (URL fetch on every citation).

**Origin:** Recurring across audits.

### Lesson 11. Pseudo-precision

"Exactly 1,618 satellites" when the underlying count fluctuates. False precision implies certainty that does not exist.

**Promoted to:** Rule 28 (numbers carry units and basis); use ranges per Rule 6.

**Origin:** Amazon Leo (formerly Kuiper) coverage and similar.

### Lesson 12. Quote stitching

Two sentences from different parts of an interview combined into one quote. Always check the full context.

**Promoted to:** Source fidelity (audit Step 3).

**Origin:** Executive quote handling across multiple weekly analyses.

### Lesson 13. URL slug deception

A URL with `/2026/04/` in the path may have been published in early May. Do not infer publication date from the slug; fetch the page and check the actual date.

**Promoted to:** Rule 29 (URL fetch on every citation).

**Origin:** Audit pass on a news brief that miscounted the time window.

### Lesson 14. Forum-as-source

Refuge Forums, Reddit, or Tiger Droppings speculation gets picked up as fact through repeated quotation. If the trail dead-ends at a forum, the claim is rumor and must be labeled.

**Promoted to:** Source tier discipline (§8); rumors labeled per Audit edge case.

**Origin:** Recurring. SpaceX rumor cycle especially.

### Lesson 15. Title drift

"Remi El-Ouazzane, President" reads differently from "Remi El-Ouazzane, Group President of Microcontrollers, Digital ICs and RF Products". The shorter version implies CEO-level authority. Be specific about the scope of role.

**Promoted to:** Source fidelity (audit Step 3).

**Origin:** Executive quote handling.

### Lesson 16. Unit smuggling

"100 TW" reads as a number but means 100 trillion watts. Verify unit accuracy especially for unfamiliar quantities. Watch kg vs lb, MT vs short tons, GHz vs MHz, Mbps vs MBps.

**Promoted to:** Rule 28 (numbers carry units and basis).

**Origin:** ODC, Starlink capacity, and launch coverage. Recurring.

### Lesson 17. Implicit claim creep

"First major failure" sneaks in the assumption that prior flights had no failures. Often technically accurate but worth verifying against the full launch history. "Largest land deal in SpaceX history" implies a basis for comparison that may not survive scrutiny.

**Promoted to:** Rule 18 (subject-verb logical consistency) and Rule 20 (comparison validity).

**Origin:** Audit passes on news briefs about flight tests and corporate filings.

### Lesson 18. Speculation dressed as analysis

"Pre-IPO secondary tender activity will likely reference this figure as the floor" reads as observation but is actually a Mach33 prediction with no source. Fix is usually one or two words: "Mach33 view: ..." or "we expect...".

**Promoted to:** Rule 22 (forward-looking claims framed as Mach33 view or sourced).

**Origin:** SpaceX IPO coverage.

### Lesson 19. Position inversion

Eutelsat / OneWeb operates an NGSO constellation but on regulatory questions often aligns with the GSO side because Eutelsat owns GSO assets. Do not infer policy positions from operator type alone.

**Promoted to:** Source tier discipline (§8) and Pattern 11 (source-frame fidelity).

**Origin:** Regulatory coverage. Recurring trap.

### Lesson 20. Date precision creep

A source says "earlier this week"; the draft says "May 2 and 3". Either find the specific dates from a primary source, or stay vague.

**Promoted to:** Rule 17 (source-frame fidelity) and Rule 28 (numbers carry units and basis).

**Origin:** News brief audits.

### Lesson 21. Dead URL inheritance

A URL that worked in a prior draft has since 404'd. Re-fetch every URL on every audit pass.

**Promoted to:** Rule 29 (URL fetch on every citation).

**Origin:** Recurring.

### Lesson 22. Stop-slop "After" example contradicts its own rule

Stop-slop Example 4 shows "Speed, quality, cost—pick two." which contains an em-dash, contradicting its own ban on em-dashes. If a writer cites the example as a defense for an em-dash, the rule wins, not the example.

**Promoted to:** Rule 3 (no em-dashes, no en-dashes).

**Origin:** Stop-slop usage. Mach33 house style overrides the example.

### Lesson 23. En-dash misses

Stop-slop bans em-dashes but is silent on en-dashes. Mach33 house style additionally bans en-dashes. Catch in number ranges, score lines, and any spot a writer used an en-dash as an em-dash substitute. Search `–` on every audit pass.

**Promoted to:** Rule 3 (no em-dashes, no en-dashes).

**Origin:** Audit pass extension after stop-slop missed en-dashes.

### Lesson 24. Hedging on model outputs

"Our model may suggest somewhere around $100B per GW" undercuts the model. The model has a number. State the number.

**Promoted to:** Rule 13 (hedging banned on Mach33 model outputs).

**Origin:** ODC weekly analyses. Recurring when the analyst was uncertain about the model and let the uncertainty leak into the prose.

### Lesson 25. Chart-without-interpretation

A chart embedded with "as shown above, costs decline" or with no interpretation at all. The chart is the argument; the prose has to walk the reader through it.

**Promoted to:** Rule 8 (every chart followed by 1 to 3 interpretation paragraphs) and Rule 24 (charts described as visible argument, never "as shown above").

**Origin:** Recurring in early drafts; review pass usually catches.

### Lesson 26. Exec Summary topics

"We examine X" bullets that should be "X is Y, with implication Z" conclusions. The Exec Summary position is too valuable to waste on topic statements.

**Promoted to:** Rule 9 (Exec Summary bullets are conclusions, not topics).

**Origin:** Recurring. Default failure mode when bullets are written before the analysis is locked.

---

## §7 Publication Gate

The mandatory pre-publication chain. Ordered. No skipping, no reordering, no exceptions.

```
Step 1. Mach33 Audit              skill: mach33-audit
Step 2. Stop-slop pass            skill: stop-slop
Step 3. Bolding pass              skill: mach33-bolding
Step 4. Farrar pass (satcom only) skill: tim-farrar
Step 5. Final review              against Phase 5 checklist in mach33-weekly-analysis
Step 6. Publish
```

**Order matters.** Audit first because the other skills act on the words. If the words are wrong, polishing them is wasted effort. Stop-slop second because clean prose is the input to bolding. Bolding third because bolds are scan path, not emphasis, and need the locked prose to anchor on. Farrar fourth (satcom only) because Farrar's job is to pressure-test framing on already-clean prose. Final review last to catch anything the upstream passes missed.

**Equivalent of the modeling PASS criteria.** The modeling side ships a sprint when all anchored calibration targets are hit. The prose side ships an analysis when the audit produces a clean "verified clean" report with all major claims enumerated, stop-slop scores at or above 35/50 on all five dimensions, bolding passes the density and scan-path checks, Farrar (if invoked) finds no would-engage corrections that survive recommended fixes, and the Phase 5 checklist passes in full.

**Step-by-step details:**

**Step 1 — Mach33 Audit.** Run `mach33-audit` end to end. Inventory the deliverable; catalog every claim (hard facts, comparative claims, time-sensitive claims, source attributions, URLs, internal calculations, implicit claims, terminology, framing verbs, subject-verb pairs, comparison structures, forward-looking claims); verify each systematically (numbers, quotes, URLs, comparatives, attributions, terminology, source-frame fidelity, subject-verb logical consistency, forward-looking framing); cross-check internal consistency (number consistency, date logic, arithmetic, chart-vs-prose, footnote alignment, cross-document coherence, opening sentence); grade source quality (Tier 1 to 5); run domain-specific checkpoints; severity-grade findings; present findings with bolded key terms, verbatim replacement text, and explicit verified-clean enumeration.

**Step 2 — Stop-slop pass.** Read prose against the canonical phrase and structure lists. Score 1 to 10 on Directness, Rhythm, Trust, Authenticity, Density. Below 35 / 50 triggers revision. Apply the Mach33 overrides on top: no en-dashes (Rule 3, Lesson 23), no em-dashes regardless of stop-slop example contradiction (Rule 3, Lesson 22). Quick checks before delivery: adverbs killed, passive voice replaced, no inanimate-thing-doing-human-verb, no Wh- sentence starters, no throat-clearing, no "not X but Y" contrasts, varied rhythm, no em-dashes anywhere.

**Step 3 — Bolding pass.** Run `mach33-bolding`. Walk every paragraph, classify prose vs styled elements (callouts, tables, captions, headers, sources — all skipped), generate 0 to 3 bolds per paragraph following Aaron's Rule. Self-check: no verbs, no bolds over 5 words (very rare 6-word exception), density near 1.1 average, no clustered-in-one-sentence bolds, no bolds inside styled elements, document topic not bolded as sub-phrase. Output as review list or as Apps Script with per-slide scoping. Recommend version-history snapshot before any script run.

**Step 4 — Farrar pass (satcom only).** Triggered when the analysis touches Starlink, ASTS, AST SpaceMobile, D2D, MSS spectrum, FCC actions, RDOF, BEAD, satcom unit economics, or LEO constellation economics. Run `tim-farrar`. Four passes: load-bearing numbers, definition slippage, physics / spectrum walls, hype-evidence delta. Output includes would-engage assessment, findings in Farrar voice, lines that survive, and recommended fixes in Mach33 house voice. Recommended fixes are the actual deliverable; the Farrar voice is the pain that justifies each fix.

**Step 5 — Final review.** Phase 5 checklist from `mach33-weekly-analysis`. Title declarative and thesis-forward. Summary 3 to 6 sentences, standalone hook. Exec Summary 4 to 8 bullets, bold lead, specific numbers. Every analytical paragraph carries a number. All charts: H3 title, image embed, 1 to 3 interpretation paragraphs. Chart placement matches outline. Scope respected. Scenarios defined before compared. Assumptions named and sourced. Investor takeaways connect to capital decisions. US English. No stop-slop anti-patterns. No emojis, no promotional language, no hedging filler. Cross-references to prior Mach33 analyses where relevant. First-person plural throughout. Closing paragraph zooms out.

**Step 6. Publish.** Only after Steps 1 to 5 are complete and any flagged issues are resolved.

**Calibration target equivalent.** The modeling side ships when calibration targets are hit exactly (or with documented overshoot). The prose side ships when the audit's verified-clean enumeration covers every major claim by topic, stop-slop scores at or above 35 / 50 across all five dimensions, the bolding density check passes, Farrar finds nothing that survives recommended fixes (if invoked), and the Phase 5 checklist passes in full. A piece that passes some steps and skips others is not publishable.

---

## §8 Source Discipline

Five tiers. Cited explicitly in audit output so the reader sees confidence at a glance.

```
Tier 1. Primary           SEC filings, FCC orders, NASA procurement notices, FAA mishap
                          reports, ITU publications, company SEC-filed press releases,
                          official earnings transcripts, court filings.
Tier 2. Direct journalism Reuters, Bloomberg, WSJ, FT, AP. Original reporting, not
                          aggregation, not opinion.
Tier 3. Trade press       SpaceNews, Via Satellite, Aviation Week, Ars Technica, Spaceflight
                          Now. Usually reliable, check for repackaging of company PR.
Tier 4. Aggregators       Yahoo Finance reposts, content farms, Substack, branded company
                          blogs, X posts from journalists.
Tier 5. Speculation       Forum posts (Reddit, Refuge Forums, Tiger Droppings, Tesla Motors
                          Club), anonymous tips, Discord screenshots.
```

**Rule:** Any claim resting solely on Tier 4 or Tier 5 is either (a) explicitly labeled as unconfirmed / rumor in the document, or (b) flagged for upgrade to a better source or removal.

**Independence:** Two articles citing the same Reuters wire is one source. Find genuinely independent confirmation.

**Recency:** Fast-moving figures (subscriber counts, satellite counts, market caps, chip shipments) demand the latest data, not just "a correct figure from sometime". See Rule 21.

**No graceful failures:** A claim that cannot be verified gets flagged. Pass-through with hedge words ("reportedly", "sources suggest") is not acceptable unless the source itself is named.

**Primary fidelity:** Verifying that a fact is true is not the same as verifying that the document represents the source faithfully. See Pattern 11 and Rule 17.

---

## §9 Anti-Patterns Register

Watch these. Catch in draft if possible, in audit always.

**Generic AI prose.** "In the rapidly evolving landscape of...", "at its core", "deep dive", "unpack", "navigate", "lean into", "double down", "circle back", "moving forward", "game-changer". Stop-slop has the full list.

**Promotional language.** "Groundbreaking", "game-changing", "must-read", "transformational" without unit economics, "massive" without a number, "set to dominate" without a share trajectory. State the finding. Let the reader decide if it is groundbreaking.

**Hedging filler.** "Could be argued", "perhaps", "may suggest", "somewhere around", "in some sense", "to a degree". Either state the finding or do not. On model outputs, banned (Rule 13).

**Vague methodology.** "We used a model" without naming the model, its structure, its inputs. Methodology gets stated upfront (Rule 12).

**Chart without interpretation.** Chart embedded with no walk-through, or with "as shown above". Rule 8, Rule 24.

**Missing investor frame.** Section that does not connect back to a capital allocation decision. Cut, tighten, or move to a different deliverable.

**Tangents beyond scope.** Paragraph that wandered out of scope IN and was not flagged or cut. Rule 11.

**Three-item lists everywhere.** Default AI pattern. Use two items or one. Stop-slop.

**Em-dashes anywhere.** Rule 3. Search `—` on every audit.

**En-dashes anywhere.** Rule 3, Lesson 23. Search `–`.

**Smart quotes in slide-deck applications.** Apps Script gotcha. Phrases not found in deck because the deck uses `’` where the source text uses `'`. Use unicode escapes in the JS string.

**Pull-quote phrasing.** If a sentence sounds like it was written to be a pull-quote, it is the wrong sentence. Stop-slop.

**False agency.** "The complaint becomes a fix", "the data tells us", "the market rewards". Name the human. Stop-slop.

**Narrator-from-a-distance.** "Nobody designed this", "People tend to...". Put the reader in the room. Stop-slop.

**Wh- sentence starters.** "What makes this hard is...", "Why this matters is...". Lead with the subject. Stop-slop.

**Bolding the topic.** Bolding "orbital compute" in a report titled "The Economics of Orbital Compute". Lesson 6.

**Bolding fragments with verbs.** "Rose 72% year-over-year" includes "rose". Tighten to the magnitude. Lesson on bolding mechanics in `mach33-bolding`.

**Subject-verb logical impossibility.** "Disclosed" + "confidential", "announced" + "people familiar". Lesson 1, Rule 18.

**Filing-type imprecision.** S-1 used for DRS, OTA called a contract, NPRM called an R&O. Lesson 4, Rule 19.

**Comparison distortion.** A vs B where A and B measure different things. Lesson 9, Rule 20.

**Speculation dressed as analysis.** Forward-looking claim presented as observation. Lesson 18, Rule 22.

---

## §10 Companion Skill Map

The skills are the tools. This constitution is the framework that governs their use.

| Skill | When | Phase |
|---|---|---|
| `mach33-weekly-analysis` | Every weekly. The pipeline. | §0, §2 |
| `mach33-thesis-library` | Any SpaceX-adjacent content. | §0, Pattern 10, Rule 16 |
| `mach33-audit` | Pre-publication. Always. | §7 Step 1 |
| `stop-slop` | Pre-publication. Always. | §7 Step 2 |
| `mach33-bolding` | When the piece will be bolded for scannability (weekly analyses, decks). | §7 Step 3, Pattern 12, Rule 23 |
| `tim-farrar` | Pre-publication. Satcom content only. | §7 Step 4 |
| `mach33-newsletter-intro` | After the weekly is locked. Promotional. | Downstream |
| `mach33-x-post` | After the weekly is locked. Promotional. | Downstream |
| `mach33-thumbnail-prompt` | After the weekly is locked. Promotional. | Downstream |
| `mach33-chart-style` | During Chart phase. | §2 Phase 2 |
| `mach33-chart-data-csv` | When chart data needs to be platform-formatted. | §2 Phase 2 |
| `mach33-brand` | Any visual or design output. | Cross-cutting |

---

## §11 Maintenance

The constitution is alive. New lessons get promoted to numbered Rules. Stale patterns get amended or retired. The modeling-side discipline applies: every meaningful surprise during a weekly produces a candidate Lesson; every Lesson that recurs across two or more analyses gets promoted to a numbered Rule; every Rule that becomes obviously wrong gets amended with a dated note.

**How to add a Lesson.** Vlad flags during or after a weekly ("the audit caught this and we should remember it"). Draft the Lesson entry in his voice, show him the diff, update §6. If the Lesson maps to an existing Rule, link it. If it doesn't, draft the new Rule and add to §4.

**How to add a Rule.** Two paths: (1) a recurring Lesson gets promoted to a Rule when it has bitten more than once; (2) Vlad locks a new editorial standard. Either way, draft in his voice, number sequentially, link Lessons that drove the promotion.

**Versioning.** v1.0 is the current version. Material additions or amendments bump the minor version (v1.1, v1.2). Material restructures (architecture change, pipeline change) bump the major version (v2.0). Date the change in this section.

**Periodic review.** Suggest quarterly. Walk the Lessons, prune the ones that no longer fire. A Lessons register full of formerly-true cautions is worse than no register; it gives false confidence in the constitution.

**Sign-off.** Vlad. The constitution is his editorial standard expressed as a referenceable artifact. No additions or amendments without his lock.

---

## §12 Quick Reference

**Article Kickoff Protocol (§0):** Read this doc, read `mach33-weekly-analysis`, read `mach33-thesis-library` if SpaceX-adjacent, state the Voice Compliance Preamble (§5), lock scope before charts, lock charts before outline, lock outline before draft, run the Publication Gate (§7) before publishing.

**Voice Compliance Preamble (§5):** First-person plural, US English, no em-dashes, no en-dashes, no emojis, specific number per analytical paragraph, exec summary bullets are conclusions with bolded lead-in phrases, charts at point of argument with 1-3 interpretation paragraphs, hedging banned on model outputs, scope IN / OUT locked, canonical phrasings from thesis library used verbatim, closer reframes.

**Publication Gate (§7):** Audit → stop-slop → bolding → Farrar (satcom) → final review → publish. No skipping.

**Rule citation:** "Rule N" in chat, where N is the rule number from §4. "Lesson M" for lessons in §6. "Pattern P" for load-bearing patterns in §3.

**The most-cited Rules.** Rule 5 (number per paragraph), Rule 9 (conclusions not topics), Rule 13 (no hedging on model outputs), Rule 17 (source-frame fidelity), Rule 18 (subject-verb logical consistency), Rule 23 (bolding mechanics), Rule 30 (Publication Gate).

**The most-cited Lessons.** Lesson 1 (disclosure-verb trap), Lesson 3 (source-frame drift), Lesson 5 (stale-figure-was-once-correct), Lesson 6 (topic vs substance bolding), Lesson 22 / 23 (em- and en-dash discipline), Lesson 24 (hedging on model outputs).

---

*Constitution v1.0. Locked 2026-05-26. Sign-off: Vlad. Next review: 2026-08-26.*
