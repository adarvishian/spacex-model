# The current capital allocator — what's wrong with it, and where Python helps

*Status: describes the model **as it stands today** (V4.109), before any re-architecture. Nothing here has been changed yet. Written to help a colleague see why we're considering moving the allocation engine out of Excel and into a small Python layer.*

---

## What the allocator is supposed to do

Once a year, the model has to split two scarce resources across SpaceX's businesses — **cash** and **launch capacity** (Starship kilograms to orbit) — among Starlink, Customer Launch, Orbital Data Centres (ODC), Terrestrial compute, and Lunar/Mars. It decides who gets funded, who gets launch slots, and therefore who actually deploys hardware that year. It's the brain that turns "these businesses have these returns and this demand" into "here's where the money and the rockets go."

## How it works today

There are really **two separate allocators bolted together inside one spreadsheet tab**:

- A **cash** allocator that ranks the businesses by their return (prior-year IRR), gives each a share of the cash pool, then tries to cap and redistribute the excess.
- A **launch-capacity** allocator that splits the available kilograms by a crude proportional rule.

They run on different logic, they don't talk to each other, and the whole thing is held together by Excel's *iterative calculation* (the cash pool depends on profits, which depend on spending, which depends on the pool — a deliberate circular loop Excel has to solve by repeated recalculation).

## The issues with it today

**1. The allocation doesn't actually match what businesses can spend.** The cash allocator hands out dollars by return, but a business often can't absorb what it's given. By 2040 the engine allocates about **$270B**, the businesses actually deploy about **$681B**, and the model *simultaneously* reports **$822B sitting idle** as "leftover." Those three numbers can't all be right — they're computed on different bases that don't reconcile. In plain terms: the allocator's outputs are neither binding (businesses spend more than they're given) nor meaningful (huge "idle cash" coexists with over-spending).

**2. Cash and launches are decided by unrelated rules, so they contradict each other.** A business can win a big slice of *cash* on its high return but get almost no *launch slots* (or vice versa), because the two allocators rank everyone differently. The clearest case is Customer Launch: it has high per-unit returns but a small market, so the cash allocator wants to throw ~80% of the pool at it — then has to claw it back — even though what it actually needs is launch slots, not cash.

**3. It keeps funding businesses whose returns have gone negative.** A 5% minimum-share floor props up every business regardless of economics, so a declining, negative-return Starlink cohort still draws cash and launch capacity it shouldn't.

**4. There are three different, inconsistent "demand" numbers.** The amount of launch demand used to *size* the rocket fleet, the amount used to *ration* capacity, and the amount used to *flag* whether capacity is binding are three different figures (e.g. ~139M vs ~153M vs ~527M kg in one year). One of them inflates Starlink's "wants" to its theoretical maximum, which lets Starlink crowd ODC out of launch capacity. The "is capacity binding?" indicator reads the wrong one and reports the opposite of what's actually happening.

**5. Workarounds are piling up to compensate.** Because the allocator under-serves capital-hungry businesses like ODC, separate **debt facilities** were bolted on to fund them *around* the allocator. So the businesses that need capital most are increasingly funded by side-channels the allocator doesn't see — which defeats the point of allocating by return in the first place.

**6. The safety net is broken exactly where it's needed most.** The model has a cash-conservation check that's supposed to prove no cash leaks. It was never updated when those new debt facilities were added, so it now **fails every year a facility is active** — meaning the one guardrail that would catch a real error is offline precisely where the newest, most complex money flows live.

**7. It's fragile to recalculate.** Because the engine is circular by construction, it only works with Excel's iterative calculation switched on and converged. The project has already lost debugging cycles to versions that were saved with that setting off and silently zeroed out years of results. Small changes can make it lurch or fail to settle.

## Why this is genuinely hard *in Excel*

None of these are sloppiness — they're what happens when you force an inherently **iterative, rank-ordered, multi-step algorithm** into a grid of cell formulas:

- A "rank the businesses, fund the best first, cascade the leftover to the next" procedure is a natural **loop** in code. In Excel it has to be hand-unrolled into dozens of "spillover," "headroom," and "residual" rows — one set per business, per step — which is where the bugs and the un-landed patches hide.
- The circular cash loop has to be solved by Excel's iterative calculator, which is fragile (the on/off setting, convergence, bistability) and can't be unit-tested.
- The conservation checks are themselves just more fragile formulas, so they go stale silently — as #6 shows.
- Every fix is a patch on a patch across 150+ rows, and understanding the logic means reading the whole tab. There's no single place where "the allocation rule" lives.

## Where Python helps

The allocator is the *one part of the model Excel is worst at* — and, conveniently, the part that's cleanest to lift out. A small Python layer would:

- **Put the whole allocation rule in one readable function.** Inputs: each business's prior-year return, the cash pool, the launch capacity, its demand, and its cost and mass per unit. Output: cash and launch slots per business. A colleague can read the logic top to bottom instead of reconstructing it from 150 rows.
- **Make the loop a loop.** "Fund highest return first, up to what its market can absorb, cascade the rest" is a few lines of code, not dozens of spillover rows. Cash and launch get allocated *together* in the same pass, so they can't contradict each other.
- **Remove the iteration fragility entirely.** This is the big one. The allocator's design only uses *predetermined* inputs — last year's returns, last year's cash, the fleet already built. That means in Python it's a **pure function** you can run year by year, feeding last year's outputs into this year's inputs. No circular solve, no iterative-calc setting, no bistability. The thing that's most fragile in Excel simply stops existing.
- **Be testable.** Conservation ("never allocate more cash than the pool," "never assign more launch than exists," "everything reconciles") becomes a set of assertions that run automatically — not formulas that can quietly go stale.
- **Make policy swappable.** Want to compare strict ranking vs. proportional vs. a return hurdle? That's a one-line change in Python, versus rewiring the sheet.

The boundary stays clean: **Excel keeps owning the business economics and the demand/cost/return signals; Python just reads those (prior-year), runs the allocation, and writes back how much cash and launch each business gets.** It's a one-directional handoff per year, not a co-simulation — so the model stays an Excel model with a smarter brain, rather than a full rewrite.

## Honest caveats

- Python adds a toolchain and a handoff to maintain; it's no longer "everything in one file." That cost is only worth paying for the allocator specifically, because that's the piece Excel handles worst. The module economics can stay in Excel.
- A few of these problems aren't really about Excel vs Python at all — especially the **three inconsistent demand numbers (#4)**. Those signals have to be cleaned up regardless of which engine consumes them, because any allocator is only as good as its inputs. That work is worth doing first either way.

## Bottom line

The current allocator's troubles are mostly the symptoms of running a looping, multi-resource, iterative algorithm inside a formula grid: cash and launches decided separately and contradicting each other, allocations that don't match real spending, workarounds bypassing the engine, and a safety net that's quietly off. Most of that becomes straightforward in a small Python allocation function — readable, testable, and free of the circular-recalculation fragility — while Excel keeps doing what it's good at.
