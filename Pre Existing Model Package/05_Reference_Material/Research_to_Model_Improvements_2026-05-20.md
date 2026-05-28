# Research-to-Model Improvement Audit

**Date:** 2026-05-20
**Source:** `all_posts (3).md` — full Mach33 research archive (8,249 lines)
**Model target:** SpaceX Rebuild v2 (post Q4'25 anchors + V30.5 corrections)
**Method:** Two parallel passes (lines 1–4500 recent, lines 4500–8249 older), reconciled against locked Q4'25 anchors, rebuild architecture, and the six settled/working theses.

---

## Top of the inventory — what most likely moves the model

Twelve items, ranked roughly by how much they sharpen an Assumptions input the model already has a stub for, or fill a structural gap the architecture has flagged as "open."

1. **ODC dual-revenue Model A/B has an explicit, published formula.** `Revenue/GW/yr = (η / 1,979) × 10⁹ × ECR × U × 8,760 × P` (from "How Much Revenue a Gigawatt Earns in Orbit," L815–991). Plug verbatim into the ODC tab. The four levers — η (TFLOPS/W, 2.83–6.43), ECR (0.45–0.75, base 0.60), U (utilization, base 85%), P ($/GPU-hour, $1.25–$2.50, base $2.00) — become the load-bearing MC inputs. Anthropic-Colossus 300 MW = $5B/yr ($16.5B/GW capture) anchors the 2026 wholesale rate.

2. **V3 satellite anchor: 2,000 kg dry mass, 1,000 Gbps downlink, 0.5 Gbps/kg.** Multiple sources converge ("Starship $/Gbps" Aug 2025, FCC EPFD post, Voyager IPO disclosures, Musk April 2026 X post on "20,000 sats/yr at ~2 t each"). This pins the V3 sub-vehicle on both Starlink BB and Starlink DTC IRR. V2 Mini stays at 575 kg / 96 Gbps / 0.167 Gbps/kg.

3. **AWS-4 / H-block $17B spectrum spend becomes the explicit 2025–2027 Spectrum CapEx claim.** $8.5B cash + $8.5B SpaceX equity + $2B interest coverage through Nov 2027. Currently the rebuild architecture has a "Spectrum CapEx" placeholder in the queue gate — this number, with its three-tranche structure, lifts it from placeholder to anchored. The equity tranche also implies a small dilution event the valuation tab should book.

4. **Starlink BB ARPU 2030 = $30–40/month baseline vs $90–120 today**, with marginal-revenue-per-Mbps deflation $3.50 → $1.00 (~3× compression). Pair with the 2030 capacity figure of ~20,000 Tbps base (~30–40× lift) to triangulate the BB revenue trajectory. Today's promos ($59–85/mo) are the leading indicator. This is the missing Wright's-Law slope on the Starlink revenue side.

5. **DTC TAM/SOM split with 9 supply-side MC levers and 2 demand-side levers**, from the open-source TAM model + premium model:
   - Demand: TAM 2030 = $36.6B base (bear $32.7B / bull $40.2B). Asia $13B, Africa $8B, NA/Europe/SA $5B each.
   - Supply: constellation count, η (3–4), processing BW (SpaceX 500–1,000 MHz; ASTS 8,000–12,000), saturation %, rev share, data utilization, VoIP utilization, busy-hour Mbps (1–10), oversubscription (30–100×).
   - SOM 2030: SpaceX $9.5/$12.7/$15.3B; ASTS $4.4/$7.0/$8.8B.
   Bigger than the current Starlink DTC stub. The 9-lever supply engine becomes the DTC MC input block.

6. **Bundle thesis extends from two-tier to three-tier lifetime: 33 → 51 → 61 months.** T-004 in the thesis library captures the 33→51 step (broadband + mobile). The Starlink Mobile unit-economics piece adds the third product (Grok) and extends to 61 months at three-product attach. LTV:CAC follows: 12.5× / 18.0× / 20.7×. Updating the locked thesis to three tiers gives the Starlink module a cleaner ARPU/LTV cascade.

7. **Starship $/kg cost curve: $500 expended → $61/kg fully reused at flight 10, floor ~$60/kg long-run.** Booster-only reuse intermediate ($303/kg at flight 10). Per "How Soon Does Starship Get Cheap" plus "A World With 10,000 Starships," the slope is 15% Wright's Law on launch + non-chip subsystem cost. Replaces any flat-$/kg Starship assumption with a stepped curve gated on cumulative successful flights. The terminal regime is $35/kg at 1,000 vehicles/yr and $10/kg at 10,000 vehicles/yr.

8. **IPO primary capital range $20B–$30B (not point $30B).** From Ep. 1 podcast: total raise ~$50B split as $20–30B primary + balance secondary. The locked architecture has $30B as a point estimate — this becomes an MC input range with a 2-year deployment-curve compression conditional on the high end. Same field, but Monte-Carlo'd rather than fixed.

9. **Mars hardware $/kg landed = $10,000 (2030 base).** From "How Much Does a Mars Payload Really Cost?" — direct anchor for the BV engine hardware factor under the locked carve-out architecture. Composition breakdown also given (ISRU 40% / Habitat 16% / Life Support 12% / Power 10% / Crew 7% / Construction 9%), which lets the BV engine carry sub-components rather than a single hardware lump.

10. **ODC 100 kW/sat power density confirmed by physics path; thermal mass 3 kg/kW, solar specific power 261–490 W/kg.** The StarThink V1/V2 architectures land the 100 kW/ton compute satellite as a mathematical outcome of the radiator + solar combination, not a target to be argued for. The rebuild's locked ODC compute power = 140 kW/sat is at the high end of this band — confirmed, but make solar specific power and radiator areal density MC inputs because they're the two biggest sensitivities (±30% gives ~±9% on $/GW).

11. **Cursor partnership: $10B walk-away vs $60B acquisition option.** Confirmed Cursor ARR ~$2B, doubled in months, two-thirds of Fortune 500. The AI Stack tab needs an explicit "orchestration acquisition path" — $10B as partnership cost (recurring at-cost transfer) vs $60B as one-time CapEx with full L5 revenue capture ($5B/GW). Becomes a discrete MC variable: partnership / acquisition / organic.

12. **Anthropic-Colossus = 300 MW, 220,000 GPUs, 4-year contract, ~$5B/yr** ($16.5B/GW capture, Model B wholesale). This is the cleanest 2026 calibration point for ODC Model B revenue. The bottom-up Mach33 number ($5B) sits at the top of the analyst $3.5–$5.5B range — that range is the MC input for "wholesale ODC pricing premium."

---

## Module-level findings

### Starlink (BB + DTC + Starshield)

**V3 sub-vehicle anchors.** V3 at 2,000 kg / 1,000 Gbps / 0.5 Gbps/kg. Per-beam Ku-band ~2 Gbps; V2 Mini has ~32 beams; V3 has ~1,000 beams. ~10× per-sat × ~5× sat count = ~50× total constellation lift over V2 Mini base. U.S. addressable households scale from V2 Mini ~8.6M HHs (20:1 oversubscription) to V3-era ~117M HHs (~88% of 132M total) by 2030.

**Constellation horizon and FCC headroom.** 29,988 total Gen2 filed, 15,000 currently authorized. Musk April 2026 commitment: 20,000 sats/yr at V3 mass. ~10,000 active as of March 2026. The model's cumulative sat count should accept up to 40,000–100,000 by 2030 as the bull-case ceiling.

**Bandwidth deflation as the load-bearing revenue slope.** $3.50/Mbps/mo (2025) → $1.00/Mbps/mo (2030). Pair with 2030 base capacity of ~20,000 Tbps (vs ~700 Tbps today, ~30× lift); 30,000+ Tbps bull, ~10,000 Tbps bear. Implied baseline service price 2030: $30–40/mo. Today's promos ($59–85 in select markets) confirm the curve is already pulling forward.

**Starlink Mobile bundle ladder.** Stage 1 (standalone) → Stage 2 (broadband + mobile) → Stage 3 (broadband + mobile + Grok). ARPU $119/$125/$127/$128. Lifetime 33→51→61 months. Standalone monthly churn base 3.0% (range 1.5%–3.5%). Bundle churn reduction range 20%–50%. Contribution margin ~70% across stages. Mobile attach matures 0→40% over 60 months with 12% annual cancellation. Stage-2 cost breakdown: satellite network $25, support/billing $7, bad debt 2% ARPU, hardware $1.50, regulatory $1, mobile ops $0.85, mobile carrier reg $0.21. Note that corporate G&A/R&D/brand, constellation replenishment CapEx and ground D&A are explicitly excluded from contribution margin per the locked vending-machine framing — this is already aligned.

**Capacity-side density anchors.** 2025: 0.10 Gbps/km² urban, 0.05 Gbps/km² rural. 2030 base: 5.0 Gbps/km² urban (50×), 1.6 Gbps/km² rural (32×). Saturation 126 subs/km² urban / 81 rural. LCOC compresses ~$4,976 → $1,076 per Gbps·yr (4.6×).

**Starshield calibration.** Locked $2,520M 2025 target supported by Q4'24 disclosure trail ("multi-billion-dollar revenue pillar"). Decay rate 0.25/yr (from Q4'25 R30) confirmed against the older Starshield Dec'24 disclosure narrative. No newer numerical anchor would override the locked target.

**Enterprise/hyperscaler line — not currently a module.** "Starlink + Hyperscalers" piece sizes 191,000 remote endpoints (mines, rigs, ships, polar, clinics) at $410M satellite + $4.6B cloud rev (base, 50% take-up). Cloud-to-satellite multiplier 4–12×. This is a Starlink BB enterprise tier (not AI Stack revenue). Not load-bearing for 2025–2030, but a candidate enterprise-attach line worth a sub-row on the Starlink BB tab.

### Customer Launch (F9 + Starship + P2P)

**F9 customer pricing segmentation.** Blended $111M locked anchor sits between Civil-Gov $70M, Commercial GEO/EO $67M, and Nat-Sec $140M. Rideshare separately at $6,000/kg / ~5t avg payload. The blended figure is fine; if segmentation is ever needed, $67–140M is the MC range.

**Starship per-launch cost stack.** Voyager IPO disclosed: $90M launch price, ~30% pre-sale margin → ~$60M internal cost per flight. Manufacturing $60M (Super Heavy $35M, ship $25M). Ops $2M flat, refurb $1.2M (2% of mfg). Booster:ship flight ratio 5:1.

**Reuse cost curves.** Expendable $612/kg → booster-only-reuse $303/kg at flight 10 → full-stack-reuse $61/kg at flight 10, floor ~$60/kg. Majority of cost reduction within first 10–20 flights; rapidly diminishing returns beyond. Use the curve directly as the Starship per-launch IRR cost driver.

**Terminal regime per "10,000 Starships."** $35/kg at 1,000 vehicles/yr / 200t / ~10 reuses average. $10/kg at 10,000 vehicles/yr / 250t / ~20 reuses average. 85% Wright's Law learning ratio. Ops + fuel falls $5M → $3M. Refurb $0.5M → $0.25M. Booster reuse multiplier (k) today 1, regime-1 3, regime-2 5.

**Falcon 9 internal/customer split — template for ODC.** F9 internal Starlink launches climbed from ~half of cadence to ~three-quarters as Starlink scaled. Same template likely applies to ODC vs external compute customer launches over the 2030s. Worth encoding as a Starship internal-share ramp variable rather than a fixed split.

**Customer-launch demand gap.** 2026 unmet demand $0.28–1.1B; 2030 $2.5–4.2B/yr. F9 wind-down assumed (Bear 40% / Base 20% / Bull 0% of external missions remain on F9 by 2030). Segment CAGRs through 2030: Rideshare 21%, Civil-Gov 9%, Commercial 13%, Nat-Sec 4.5%. Customer Launch module should taper accordingly.

**Mars-ready Starship MC priors.** First-flight mishap rate p₀ ≈ 25%; reliability learning floor 5%; complexity multiplier κ 2–5× Falcon; turnaround τ₀ 54-day mean (30–120 range); cadence learning λ ≈ 20% per success; pad cadence floor 14/7/5 days for 1/2/3 pads; 5–35 clean flights to qualify. Direct MC inputs for the Starship cadence ramp 2026–2028.

**Depot launches as the dominant out-year demand line.** Per ODC Ep. 2: by 2033 the largest single slice of Starship launch demand is not Starlink and not orbital compute — it is depot launches, ~5 tanker flights per Moon-bound payload. The allocator's kg queue needs to reserve significant Starship launches as internal depot services in the late 2020s and 2030s.

**P2P stays back-of-queue.** No new numerical anchor changes T-002. P2P passenger ticket at $10/kg ≈ $1,000 (NYC-Sydney 60–90 min), which competes with business class but only at the terminal regime. Wrapped into customer launches per locked thesis.

### ODC (Orbital Data Centres)

**Three-scenario cost trajectory ($/GW Year-0).** Bear $132B (2027 deploy, B200 + $500/kg). Base $46B (2028 deploy, AI5 + $300/kg). Bull $24B (2030 deploy, D3/Terafab + $100/kg). Falls to $12.5B/GW within the decade in the bull case. Per-sat base CapEx $4.6M (incl. $420K launch at $300/kg). 100 kW/sat consumed in every scenario with 29% power margin.

**Crossover dates against terrestrial.** 5-year-normalized CapEx: orbital base case starts $39B/GW in 2028, crosses Jensen ($35.9B/GW) 2029, Stargate ($29.9B/GW) 2030, Bernstein ($20.9B/GW) 2032. Bull case below all three on day one. Delivered satellite cost falls $3,479 → $1,883/kg over 10 years (~46% decline), driven by launch ($300→$115/kg) plus subsystem learning.

**Sensitivity stack for $/GW.** Thermal $9B swing ±8.9%, solar ±7.7%, compute ±7.7%, launch + other smaller. Ground segment held flat at $500M/yr (uses Starlink for backhaul — itself an internal-transfer line). Useful life of chips 3–6 years (Microsoft/Google 6, Amazon revised to 5) — each year shifts L2 by ~$1.3B/GW.

**Three-architecture satellite mass budget** (V3 vs StarThink V1 vs V2):
- Starlink V3 baseline: 20 kW, 22–26% PV, 3.0 kg/m² PV, 310 K chip, 5.0 kg/m² radiator, 36% eclipse, 1,840 kg dry, 10.87 W/kg.
- StarThink V1: 70 kW, 32% PV, 1.5 kg/m² PV, 370 K chip, 4.0 kg/m² radiator, 1% eclipse, 1,298 kg, 53.94 W/kg.
- StarThink V2: 140 kW, 40% PV, 1.0 kg/m² PV, 370 K chip, 2.5 kg/m² radiator, 1% eclipse, 1,398 kg, 100.17 W/kg.
The 100 kW/ton is the V2 outcome. Locked rebuild = 140 kW/sat sits in the V2 envelope. Radiator areal density and chip temp are the two MC inputs most worth carrying.

**Orbit choice power multipliers.** LEO ≈ 6×, standard SSO ≈ 6×, dawn-dusk SSO ≈ 9×, MEO ≈ 7–8×, HEO ≈ 7–8×, Sun-Earth L1 ≈ 9×. HEO Δv only 1.5–2 km/s above LEO; HEO delivery at ~1.5× LEO cost. Dawn-dusk SSO real estate is the binding constraint (only ~10–15% of SSO, ~1% of LEO usable volume). HEO has >500× LEO real estate; L1 effectively unlimited.

**100 GW physics-bottlenecked launch demand.** Base ("Rigid PV") ~1,200 Starship launches/yr to deliver 100 GW. Improved (thin PV + radiator stretch) ~600. Frontier ~350. Compute density doubles → launch demand halves. Use 350–1,200 as the MC bound on Starship demand from ODC at 100 GW deployment.

**xAI/SpaceX merger trajectory.** Base case (cash-in-cash-out, launch-by-launch) ~198 GW deployed and $948B revenue by 2040. "First time in >10 years of space modeling that the mean outcome exceeds the prior 75th-percentile bull level." Anchor the ODC long-run revenue distribution against this rather than the locked "option value, not 2030 revenue" framing alone.

**ODC overtakes Starlink mid-2030s.** Confirmed in ODC Report — ODC is still dwarfed by Starlink into 2030, then crosses over as the dominant cash engine in the mid-2030s. Use this for terminal-value calibration. The locked T-001 thesis (option value) and this crossover are consistent if the audience accepts the post-2030 horizon (T-005).

### AI Stack

**Layer split per gigawatt ($41.6B/GW total).** L1 Energy $0.7B (1.7%), L2 Chips $6.6B (15.9%), L3 Infrastructure $9.2B (22.1%), L4 Model + Application $20.1B (48.3%), L5 Orchestration $5.0B (12.1%). L4+L5 = $25.1B/GW total (80/20 split). Friar disclosure floor $10.5B/GW × (1 + inference share, ~65%) × 1.45 enterprise mix = $25.1B. Anthropic disclosed $30B ARR April 2026 on 1.0–1.5 GW = $20–30B/GW upper-bound cross-check.

**Three SpaceX business models with explicit per-GW capture.** Model A (full-stack, Grok + own ODC) = $41.6B/GW. Model B (wholesale, Anthropic-Colossus) = $16.5B/GW (40%). Model C (hybrid, Cursor structure) = $36.6B/GW (88%). Spread 2.5× on same physical asset. Locked architecture has AI Stack as standalone but the L4 vs L5 capture is what determines whether SpaceX participates above or below Cursor in the orchestration sandwich.

**Chip stack inputs.** Tesla AI4 cost $650 (disclosed by Musk). AI5 base case $5,000/chip, 500 W, 4,500 TFLOPS FP8, 1.0 kg, 200 chips/sat — "Hopper-class single SoC, Blackwell dual" per Musk Jan 2026. Dojo-3 / D3 bull: $2,500/chip, 250 W, 5,000 TFLOPS, 0.5 kg, 20 TFLOPS/W, radiation-hardened, Terafab-made. B200 bear: $45,000/chip, 1,000 W, 10,000 TFLOPS, 2.0 kg.

**Terafab as new corporate CapEx line.** $25B JV (Tesla/SpaceX/xAI), Austin, 2nm process, announced March 2026. Gates the Dojo-3 chip cost down to $2,500/chip. Until Terafab is operational, ODC chip cost defaults to $5,000 AI5 base. This is a 2026–2028 capital deployment line that the rebuild's CapEx tab doesn't currently include but the queue gate must reserve cash for.

**Hyperscaler revenue per GW disclosure.** Today hyperscalers run $12–17B/GW; vertically integrated inference players (OpenAI-class) closer to $20–25B/GW. Use as MC bound on AI Stack/ODC revenue.

### Lunar / Mars

**Mars hardware $/kg landed = $10,000** (2030 base case). 10-person expedition: 152 t cargo, $769M hardware, $1.5B transport at $10k/kg, $2.3B all-in, $77M/person. Robot-only precursor cuts cost 29% / mass 36%.

**Mars hardware composition for BV engine drill-down.** ISRU 40% ($308M, 10% mass), Habitat 16% ($123M), Life Support 12% ($92M, 20% mass), Power Infrastructure 10% ($77M, 24% mass), Crew & Gear 7%, Construction + Mobility 9%. Lets the BV engine carry sub-components.

**Lunar capacity ramp from the pivot webinar.** $2,500/kg in 2026 → $100/kg by 2040. 25 Starship flights and ~500 t to the Moon by 2030, scaling to 650 flights and ~85,000 t by 2040. **This is the candidate finding that may push the Moon out of pure cash-only carve-out into also claiming kg in the allocator.** Worth resolving deliberately: is Moon a cash claim (carve-out only) or a cash + kg claim (carve-out cash + kg-reservation off the top of Starship capacity)? Sprint 4 spec already calls for kg-off-the-top for Mars; mirroring that for Moon is the question.

**Mars vs Moon Δv parity.** Mars LEO→surface ~6.4 km/s vs Moon ~5.7 km/s, only ~0.7 km/s higher. Mars mass ratio 5.7 vs Moon 4.7. For 100 t dry+payload: Lunar lander ~370 t propellant, Mars ~470 t (27% extra). Mars aerocapture trims orbit-insertion Δv significantly. Confirms Mars as the dominant carve-out target.

**Per-person-equivalent transport cost.** At $10/kg: Moon $4,000, Mars $5,000 per 100 kg. At $35/kg: Moon $14,000, Mars $17,500. P2P-class economics for human transport are the same regime as the terminal Starship cost curve.

**Mars steel/energy stack.** 15.51 MWh per tonne iron from regolith. Solar Mars 50 kg/kW + 30 kg/kW BoS + 10 kg/kWh storage, CF 0.60. Fission Mars 150 kg/kW at 40 kWe, drops to 100 kg/kW at scale, CF 0.90. At 1,000 t energy hardware: Solar ~900 t/yr steel, Fission ~3,825 t/yr steel. Useful for BV engine cross-checks but probably out of scope for the rebuild horizon.

### Allocator / Cross-cutting / Corporate

**Spectrum CapEx anchor.** AWS-4/H-block $17B = $8.5B cash 2025–2026 + $8.5B equity (~40M SpaceX shares at $2T implied) + $2B interest coverage through Nov 2027. AT&T parallel deal $23B all-cash. Possible Verizon AWS-3 ~$10B rumored. Locks the Spectrum queue-gate line.

**IPO injection as MC range.** $20–30B primary + $20–30B secondary = ~$50B total. The locked $30B point estimate becomes the upper bound of an MC range. High end compresses Starlink deployment curve by ~2 years.

**Corporate G&A / brand line for Starlink Mobile bundle.** Explicitly excluded from contribution margin per the unit-economics piece — already aligned with vending-machine framing. No action needed beyond confirming the locked $0/sub Grok CAC and $0.71/sub mobile CAC.

**Active subscriber base cross-check.** 10M global subscribers Feb 2026; 13M users across 12 countries via DTC (MWC Feb 2026). ~3M domestic users out of 10M global. Useful for 2025–2026 calibration against the locked $7,852M Starlink+DTC 2025 target.

---

## Contradictions to confirm before locking

1. **V3 mass.** Older posts oscillate 2,000 / 3,000 / 4,000 kg. The Aug 2025 $/Gbps post and the 20,000 sats/yr × 2 t framing settles on 2,000 kg. Adopt 2,000 kg as the locked anchor; flag the upper range as MC ceiling.
2. **IPO primary capital.** Locked $30B point estimate vs research range $20–30B primary. Resolve as MC input rather than fixed.
3. **Moon as cash claim vs cash + kg claim.** Sprint 4 architecture reserves Mars kg off the top of Starship capacity. The lunar webinar's 25 → 650 Starship flights/yr by 2040 suggests Moon should be treated similarly. The locked architecture is currently silent on Moon kg-reservation.
4. **ODC compute power 140 kW vs StarThink V2 envelope.** Locked 140 kW/sat sits at the V2 high end (V2 = 100.17 W/kg dry at 1,398 kg = 140 kW). Confirmed consistent, but make solar specific power (261–490 W/kg) and radiator areal density (1.75–3.25 kg/m²) MC inputs.
5. **Anthropic deal capture rate ($16.5B/GW = 40% wholesale Model B).** Mach33 bottom-up $5B vs analyst range $3.5–5.5B. The implied premium is "bulk-discount lease terms typical of anchor-tenant arrangements" — make the wholesale rate an MC input ($11.7B–$18.3B/GW range bracketing the analyst floor and the bottom-up ceiling).

---

## Things older than the rebuild that should NOT carry forward

- ARK × Mach33 $2.5T 2030 base case is the pre-rebuild-v2 anchor. Q4'25 group revenue $14,650M and the current calibration set supersede.
- Mars Optimus DCF productivity proxy ("mid-range U.S. factory worker") is superseded by 60 kg labour mass / 5%/yr productivity learning / 5-yr useful life.
- 100 GW physics post promises a Part 2 that doesn't appear in the archive. Use it for launch-demand bounding only (1,200 / 600 / 350 per 100 GW); rely on the dual-revenue Model A/B formula for ODC economics, not on the physics piece.
- ISM stays cut. The archive's Starfall + DI framework adds qualitative weight but no revenue/TAM number to populate an ISM tab. ZBLAN DI = 1 only at $110/kg launch cost, DI ≈ 5.7 at $20/kg — i.e., ISM only pencils at terminal Starship economics, which is past the 5–10 year buy-side modelling horizon (T-005). No action.

---

## Candidate additions to the MC input register

Items from the research that are arbitrary or ranged and should land as MC inputs at Assumptions creation rather than retro-fit:

- η (TFLOPS/W): 2.83–6.43, base 3.96 (AI5-class)
- ECR (effective compute ratio): 0.45–0.75, base 0.60
- U (utilization): 70%–95%, base 85%
- P ($/GPU-hr): $1.25–$2.50, base $2.00
- PUE orbital: 1.05–1.15, base 1.12
- Chip useful life: 3–6 years, base 5 (Amazon FY24)
- AI inference share: 29% (2024) → 65% (Q1'26 Mach33 est); base year-by-year curve
- Anthropic-Colossus revenue: $3.5B–$5.5B (analyst) vs $5B (Mach33), MC $3.5–5.5B
- IPO primary capital: $20–30B, base $25B
- Radiator areal density: 1.75–3.25 kg/m², base 2.5
- Chip operating temp: 333–407 K, base 370 K
- Solar specific power: 261–490 W/kg, base 350
- Starlink standalone monthly churn: 1.5%–3.5%, base 3.0%
- Bundle churn reduction: 20%–50%, base 35%
- Starship payload ramp: 100 t (V3 Block 3) → 200 t (1k regime) → 250 t (10k regime)
- Starship $/kg curve: gated on cumulative flight count, 15% Wright's Law, expendable $612 → fully-reused floor $60
- 9 DTC supply-side levers (full triangulars from the premium DTC model)
- DTC TAM levers: pricing multiple, smartphone ownership %
- Off-balance-sheet xAI financing share: 25% / 30% / 35%

---

## ISM revisit assessment

Three pieces in the archive (Starfall intro, ZBLAN teaser, ISM Series intro). All published as exploration framings, not as revenue forecasts. No quantified ISM TAM/SOM at any horizon. The Disruptability Index framework requires DI ≥ 1 to be a green light; ZBLAN crosses DI = 1 only at $110/kg launch cost, which is mid-2030s minimum.

Recommendation: keep ISM cut from the rebuild. The Starfall leak is qualitative pressure to revisit later; the DI framework is the right scoping tool when that day comes. Nothing in the archive overturns the 2026-05-12 cut decision.

---

## Suggested sprint touchpoints

Mapping the top-12 findings to the sprint roadmap:

- **Sprint 1 (Assumptions tab population):** items 1, 2, 3, 4, 5, 7, 8, 9, 11, 12 land here as inputs.
- **Sprint 2 (Starlink module):** items 2, 4, 6 are the major refinements.
- **Sprint 3 (Customer Launch):** item 7 (Starship cost curve), Mars-2026 MC priors for cadence.
- **Sprint 3.5 / ODC:** items 1, 10, 12 plus the three-architecture mass budget and orbit-choice multipliers.
- **Sprint 4 (AI Stack standalone):** item 11 (Cursor partnership vs acquisition) plus the L4/L5 split and chip stack inputs.
- **Sprint 5 (Mars/Moon carve-out + BV engine):** item 9 (Mars $10k/kg) plus composition breakdown; resolve the Moon kg-reservation question.
- **Sprint 8 (Allocator queue gate):** item 3 (AWS-4/H-block as Spectrum CapEx line), item 8 (IPO MC range), depot-launch claim line.
- **Sprint MC (post-build):** all of the input register above gets layered in.

The constitutional docs (01–04) do not need amendments based on these findings. The architecture is sound — these items refine inputs and add MC ranges, but the vending-machine framing, per-sat IRR, queue gate, strategic carve-out, and dual ODC revenue all stand.
