# Memory Snapshot — Critical Locks (as of 2026-05-27)

This is a distilled snapshot of the load-bearing rules, architectural decisions, and process locks that Vlad has accumulated across the SpaceX model rebuild. It replaces the auto-memory that the working Claude instance had — your fresh Claude Project won't have it.

**Read time: ~15 min.** Treat as binding. If you find yourself about to violate one of these, stop and ask Vlad.

---

## Section 1 — Architectural locks (don't re-litigate)

### 1.1 Vending-machine module framing (LOAD-BEARING)

Each module P&L is: **Revenue → COGS → Gross Profit = EBITDA → CapEx → FCF**.

R&D, SG&A, overhead, and taxes live at the **Group** level only, never inside a module. Modules surface full-IRR demand and pay at-cost for shared resources (launches, spectrum). The Group is where corporate costs and the consolidation walk live.

Why: emerged from V30.5 lessons; the original model mixed module and group costs which made attribution impossible. Don't reintroduce module-level overhead.

### 1.2 Anchor-and-offset formula pattern (Execution Rule 23)

Deterministic year-row ramps use `$D$14` (anchor cell) plus an `E$6` year-offset reference. **Never chase neighbours** (`=D14*1.05` style).

Why: lets you delete or insert a year column without breaking every formula downstream. Also makes audit trivial — every year row reads from one anchor.

### 1.3 Allocator OUT contract — by canonical label, not row number (Execution Rule 12)

When a downstream tab reads from the Allocator, it uses `INDEX/MATCH` on the canonical label, never `Allocator!R88` directly.

Why: the Allocator has been re-rowed multiple times (Sprint 10 added vehicle rows, Sprint 10.7 shifted §6/§7/§8/§9 headers). Label-based reads survive re-rowing; row-based reads silently break.

### 1.4 Queue gate for non-module claims (LOAD-BEARING)

The IRR queue must reserve year-N OpEx + Corp CapEx + Spectrum + Taxes **before** allocating module CapEx. If the queue gate is starved (cash ≤ non-module claims), every module gets zero regardless of IRR.

This is exactly what triggered the Sprint 10.8 spectrum license fee amendment — Spectrum CapEx claim was draining the 2025-26 cash pool, zeroing every module allocation.

### 1.5 Per-sat marginal IRR, no fleet-seeding

Chicken-and-egg IRR bugs get fixed by per-sat marginal IRR refactor, NOT by hardcoded fleet seeding. If you see a "fleet seed" hack proposed, push back.

### 1.6 Iterative calc ON workbook-wide

100 iterations / 0.001 tolerance. Locked since Sprint 4. Resolves the Starlink↔Starlink Capacity %×Revenue cycle. **Every sprint pre-flight must confirm iterative calc is still ON.**

### 1.7 Year horizon D:AC = 2025-2050

Locked. Specs reference this directly. Don't add columns past AC.

### 1.8 Demand is purely exogenous (Option A) — Sprint 11f architectural rework

After the Sprint 11d collapse (see Section 3.1), the locked principle is:

| Quantity | Reads from | Recursion? |
|---|---|---|
| **Demand** (sigmoid cash-demand rows) | Anchor × learning × year-mask + exogenous facility CapEx | No |
| **Output** (launches → sat CapEx → cash IN) | MIN(cash from allocator / unit cost, internal target) | Bounded by cash; never feeds demand |

Allocator reads demand + IRR → ranks → assigns cash. Cash drives output. **Output never feeds back into demand.**

### 1.9 Vehicle-level allocator (Starlink V2 BB / V2 DTC / V3 BB / V3 DTC)

Per Vlad lock 2026-05-26: Starlink V2 BB, V2 DTC, V3 BB, V3 DTC are top-level allocator entries with their own per-vehicle IRR sigmoid queue rows. Hardcoded ratchets (R43 V2/V3 flag, Assumptions R320 V2 DTC permanent cap, R33/R37/R39/R41 deployment ramps) are retired — V2→V3 transition emerges from IRR signal + cash allocation.

### 1.10 Allocator is advisory, not binding (until Sprint 11f wires it)

Sprint 10 lit up the Allocator structurally but module deployment formulas don't bind on Allocator IN. V2.12 showed $293B unallocated cash by 2050. Sprint 11f is where the deployment formulas finally bind on `MIN(cash/cost, kg/mass, internal)`. If your work touches deployment, you're likely in 11f territory.

---

## Section 2 — Excel / plugin footguns (don't repeat these)

### 2.1 Assumptions write-then-reference footgun (CRITICAL)

If you add a new Assumptions row and immediately reference it cross-tab in the same plugin chat, you trigger a session-level calc engine failure. Formulas return 0. Even `=Assumptions!A1` returns 0.

**Mitigation:** save + fully quit Excel + reopen between Assumptions writes and cross-tab references. Either split into two plugin chats, or force `worksheet.calculate()` after every Assumptions write.

This footgun killed Sprint 11 Block 2 and Sprint 11c partial.

### 2.2 INDEX with col_num = 0 spills

Modern Excel `INDEX(range, 1, 0)` returns the whole row as a spill. `IFERROR` doesn't catch it. Lookback formulas need an explicit `IF(col < 1, 0, INDEX(...))` wrapper.

### 2.3 SUMPRODUCT × INDEX(...,0) array-shape bug

Cumulative running-sum patterns must NOT use `INDEX` with `col_num=0` inside `SUMPRODUCT`. It broadcasts the entire row and bypasses the year-offset filter.

### 2.4 FORECAST is regression, not bracket-interp

`FORECAST` and `TREND` fit a regression line across ALL table points. For piecewise-linear lookup tables, use `INDEX/MATCH(..., 1)` bracket-find + manual linear interp. (Sprint 10.5 R144 gave $54k instead of $6.7k at Q=575k because of this.)

### 2.5 Quote canonical labels verbatim in spec formulas

Long canonical labels in markdown table cells can truncate visually AND corrupt `MATCH` literals. Spec authors quote labels in full or instruct the plugin to resolve at execution.

### 2.6 execute_office_js safer than set_cell_range for multi-row writes

`set_cell_range` with `copyToRange` on multi-row bounding-box sources tiles the entire box and corrupts adjacent cells. Use `execute_office_js` for complex multi-row formula fills. Restrict `copyToRange` to single-cell or single-row sources only.

### 2.7 Circular dep at zero attractor (Sprint 11d post-mortem)

`MIN`-bind on a self-referential variable can converge to **zero** as a stable fixed point in Excel's iterative calc. If you're writing a `MIN(supply, demand)` where demand reads from output, you've reintroduced this bug. See Section 1.8.

---

## Section 3 — Process meta-lessons

### 3.1 Sprint 11d collapse — late methodology surfaces as the model grows

Complex models surface load-bearing methodology late, **even with day-1 locking discipline**. Some issues only become visible when downstream consumers exist (the allocator couldn't act on per-vehicle IRR until the allocator was built at vehicle level). Others emerge from compounding (LM BV accumulated to $5.6T → $478B/yr phantom D&A).

**Process amendment:** treat post-PASS diagnostic chats as a formal step. Architecture amendments mid-build are NORMAL. Sprint scope expansion combining related fixes is fine. Constitutional discipline necessary but not sufficient — must include downstream-consumer probing.

### 3.2 No version obsession (Vlad lock 2026-05-27)

Do NOT surface model version letters or numbers in status docs, sprint kickoffs, plugin chats, or diagnostic discussion. Describe the model by **state** (what's wired, what's collapsed, what's missing), not filename. Vlad handles versioning.

(Exception: this README and STATUS_2026_05_26 reference V2.16 / V2.17 because Vlad named them directly when handing off.)

### 3.3 No workbook names in spec drafts (Vlad lock 2026-05-20)

Future sprint specs do NOT name source or target workbook files. Vlad handles versioning at file-naming time.

### 3.4 Sprint sizing protocol (Roadmap §10)

- Target: 3-5 §3 sections per sprint
- Hard cap: 7 sections / 4 tabs above which mandatory split
- Pre-flight calc engine sanity probe mandatory (§10.3)
- Assumptions write-then-reference protocol (§10.2)

### 3.5 US English lock 2026-05-26

US English everywhere for all Mach33 prose. Common slips to avoid: modelling → modeling, programme → program, behaviour → behavior, defence → defense, colour → color, centre → center, organisation → organization, optimisation → optimization, recognise → recognize, labelled → labeled, catalogue → catalog.

Note: "analyses" (plural noun) is identical in US and UK English — don't over-correct.

### 3.6 MC inputs — anything arbitrary is MC

Any stub or arbitrary-looking value becomes a Monte Carlo input range. Point-estimate scenarios are arbitrary pre-MC; thesis-conditional cuts happen post-MC.

### 3.7 Don't over-specify sprint specs

Leave file-versioning, year-column layout, and similar mechanical concerns to the plugin's judgement. Specs focus on architecture, formulas, labels, halt thresholds.

---

## Section 4 — Reading order for new collaborators

1. **This file** (15 min) — you're here
2. `00_Constitutional_Docs/00_README_Sprint_Kickoff.md` (10 min) — mandatory kickoff protocol
3. `00_Constitutional_Docs/02_Architecture_and_Methodology.md` (45 min) — the architecture spec; skim §1-5, read §6, §10, §20 carefully
4. `00_Constitutional_Docs/Model Execution Rules.md` (20 min) — the 23 rules; every spec opens with a Rule Compliance Preamble
5. `00_Constitutional_Docs/01_Lessons_Learned.md` (30 min) — 23 lessons accumulated through Sprint 9
6. `01_Current_State/STATUS_2026_05_26.md` (10 min) — where the model is right now
7. **Then** read whichever module brief Vlad assigned you (`04_Module_Briefs/`)

Total onboarding: ~2 hours. Don't skip the architecture doc — it's the single most load-bearing reference.

---

## Section 5 — Where to find what

| Need | Location |
|---|---|
| The 23 Execution Rules | `00_Constitutional_Docs/Model Execution Rules.md` |
| Architecture (§6 deployment, §20 amendments) | `00_Constitutional_Docs/02_Architecture_and_Methodology.md` |
| Sprint Roadmap + §6.8 calibration targets | `00_Constitutional_Docs/03_Sprint_Roadmap_and_Verification.md` |
| Where the model is right now | `01_Current_State/STATUS_2026_05_26.md` |
| The latest workbook | `01_Current_State/SpaceX Model V2.16.xlsx` |
| Open architectural rework | `01_Current_State/Sprint_11f_Spec.md` |
| Last shipped sprint | `01_Current_State/Sprint_11e_Spec.md` |
| Fresh-restart baseline workbook | `02_Fresh_Restart_Inputs/SpaceX Model V30.5.xlsx` |
| Q4'25 anchors | `02_Fresh_Restart_Inputs/2025 Anchors from Q4_25.md` |
| AI Stack scoping (Sprint 6 deferred) | `05_Reference_Material/AI_Stack_Module_Architecture_Scoping.md` |
| Research base (V30.5 lessons + sources) | `05_Reference_Material/Mach33 Model Build — Epistemic Base.zip` |
| The plugin skill that runs sprint chats | `00_Constitutional_Docs/mach33-model-build-SKILL.md` |
