# P90 — Matched onset interaction audit and scientific counter-arguments (2026-11-23)

## Design and lineage
Source: `P87_RESULT.json` from the 2026-11-23 cohort; exact analysis `p90_onset_interaction.py`; preserved independent recomputation `P90_RESULT.json`. P87 starts each tape at a **common checkpoint t=84**, then varies the 30/60-second downstream cycle and green/red onset. There are 96 distinct synthetic arrival tapes, each evaluated under two onset conditions, **not 192 independent tapes**. Signed delta means 30-second minus 60-second cycle.

The paradox indicator requires *both* `delta.denied<0` and `delta.cost>0`. Its matched green-onset versus red-onset table is:
- Neither: 41/96
- Red only: 43/96
- Green only: 12/96
- Both: **0/96**

For just cost>0, independently of denied, the table is neither 38; red only 45; green only 13; both **0**. These are exact descriptive properties of this frozen simulation cohort.

By turn share (32 distinct tapes each): at 0.25, green paradox 11 / red paradox 0; at 0.50, green 1 / red 11; at 0.75, green 0 / red 32. Under red onset, **all** 32 high-left-share tapes satisfy the paradox indicator. With green onset, **none** do.

The within-tape onset interaction `(delta_cost_red - delta_cost_green)` totals +131,518 vehicle-seconds across the 96 paired tapes, mean +1,369.9791666667. This is not a causal estimate of field effectiveness, nor a confidence interval, nor evidence of independence across share/clock conditions.

## Research meaning: competing explanations, not asserted mechanisms
**Hypothesis A — alignment:** Initial 15/30-second downstream red intervals interact with upstream left-first scheduling and arrival platoons, changing *which* movement waits where, without requiring larger upstream receiver-denied time.
**Hypothesis B — spatial delay migration:** A lower one-bit denied-seconds signal can coexist with more simultaneous vehicle-seconds elsewhere. P88 must locate these seconds in outside, A/B lanes, pocket and receiver.
**Hypothesis C — end-window/scheduling artifact:** A 1,356-second post-84 observation window has unequal nominal green seconds by period and onset, and green phase startup loss could further change rankings. P89 must distinguish displayed green, effective green, and actual receiver discharge.
**Hypothesis D — model structure:** Four one-cell-per-second receiving slots, deterministic headway, simplified upstream lane access, and omitted pedestrian/conflicting traffic may produce a pattern that is absent in field/independent engine.

## Explicit rejection gates
1. **No mechanism from aggregate counts.** Do not conclude a particular queue or vehicle class caused the +43,652 summed vehicle-seconds in the paradox cohort without spatial decomposition and ID-level event comparison.
2. **Paired independence.** Do not treat each onset of the same tape as an independently sampled arrival tape; seed, turn share and arrival family are design factors.
3. **Spatial exactness.** Verify for **each** of 192 P88 pairs that the sum of signed five-zone differences equals exactly the original signed P87 cost difference; verify source scalar components and network-out accounting.
4. **Startup censoring.** For P89 report nominal displayed green, startup-blocked green, service-eligible green and actual downstream departures separately. A theoretical effective-green signal is not throughput.
5. **Scientific transport.** No recommendation for real intersections without simultaneous verified signals, movements, upstream and downstream crossing/exit events, and competing pedestrian/vehicle delay.

## External methodological reading
- FHWA, *Traffic Signal Timing Manual*, chapter 3: defines start-up lost time as queue release headways above saturation headway; discusses approximately 2-second assumption and effective green, saturation flow, and `capacity = s(g/C)`. https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter3.htm
- FHWA, *Traffic Signal Timing Manual*, chapter 6: progression depends on coordination offsets and arrival platoons rather than the single-node green ratio. https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter6.htm
- FHWA, *Signal Timing Under Saturated Conditions*, guidance: explicitly disputes an unconditional claim that longer cycles necessarily improve throughput by reducing lost-time fraction; congestion and residual queues affect optimization. https://ops.fhwa.dot.gov/publications/fhwahop09008/guidance.htm
- FHWA, *Signal Timing on a Shoestring*, local controller parameters: gap-out requires a minimum-green and detection timing constraints; pedestrian timing cannot be ignored. https://ops.fhwa.dot.gov/publications/signal_timing/04.htm

**Important model-to-literature distinction:** P89's extra 0/1/2/3-second binary service veto is a deliberately simplified **sensitivity intervention**. It is NOT a validated queue-headway measurement or the full HCM start-up + clearance adjustment. Neither FHWA's 2-second rough assumption nor P89's discrete gate proves the field delay response.

## Priority audit after P90
- 0.97: independent simultaneous upstream/downstream field evidence, signal/head-to-movement mapping and pedestrian/conflicting flows (external validity gate).
- 0.96: P88 exact spatial and downstream-departure conservation (raised from 0.94 because the matched-onset contrast leaves mechanism underidentified).
- 0.93: P89 full startup-veto cost rerun (raised from 0.90 because shorter cycles have more onsets and nominal capacity is not equal).
- 0.91: zero-loss horizon alignment control using a whole number of 60-second cycles / balanced endpoints; avoids misattributing observation-window calendar differences.
- 0.89: movement-based full-user objective and pedestrian safety/clearance, not vehicle delay only.
- 0.86: actuated gap-out with detection errors and minimum green.
- 0.85: additional platoon-offset holdout tapes beyond the current seeds.
Scores are **ordinal research management heuristics**, not posterior probabilities. Revisit after **each** validated experiment.
