# 2026-11-21 | Physical bypass affordance vs future arrival order — exact 16-world audit

**Status: VERIFIED mathematical computation, SIMULATED counterexample, NOT field-calibrated.** No K047 UI or replay is part of this research unit.

## Question

Which hypothetical piece of information matters more to a bounded-risk signal decision: a perfect forecast of three arrival-order bits, or knowing whether the through vehicle can bypass the blocked left-turn queue? This tests a **very narrow synthetic counterexample**, not an engineered sensor deployment.

## Source and matched variables

Reused the previously recorded exhibit input under `research/t2/analysis/20261121/exhibition-demo/demo.html`. There are eight 3-bit arrival-order patterns with a fixed sampled context, and two synthetic bypass configurations. The terminal penalty is 60 and the stage-order comparison is the same left-first-minus-through-first objective used by the archived exhibit.

- No-bypass Δ: [109,312,−27,176,145,346,9,210]
- Allow following through car to bypass Δ: [−822,−932,−720,−830,−822,−932,−720,−830]

The bypass mode here represents an entire **simulator rule**, not an observation of one real vehicle's safe gap. It is much easier to classify this rule than actual accepted lane changes; the numbers are dominated by a very large structural effect. The two mode configurations are contrasted under the same named scenario and future arrival patterns, but their full predecision microstates have NOT been proven identical. Only the exhibit's selected observation fields agree. **Do not claim fully indistinguishable real traffic trajectories or a field-feasible bypass sensor.**

## Exact decision experiment

For each possible world w let Δ_w=C_left−C_through. If a controller selects left-first with probability p, regret is max(Δ_w,0)p + max(−Δ_w,0)(1−p). To determine the worst regret with no information, minimize the maximum over 16 worlds. With a binary report k∈{0,1}, choose conditional action probabilities p_0 and p_1. The report can be wrong with any conditional probability q_w∈[0,ε], separately for each true world, even adversarially. Expected regret is affine in q_w, so its maximum is attained at 0 or ε. The finite linear program has three real variables (p_0,p_1,t); exact `Fraction` arithmetic enumerates all feasible triple-constraint vertices to minimize t. No normal approximation, equal-probability assumption, or forecast accuracy estimate is used.

| Decision-time information allowed hypothetically | Worst regret |
| --- | ---: |
| No structural bypass information, no future arrival order | 161236/639 = **252.3255** (optimal random action) |
| Perfect future arrival order but bypass mode unknown | 161236/639 = **252.3255** |
| Perfect knowledge of bypass mode but no future arrival order | 9342/373 = **25.0456** |
| Perfect knowledge of bypass mode and full future arrival order | **0** |

The no-sensor deterministic minimax is 346; permitting randomization improves it to 252.3255. The best-case oracle with both types of future/structural information has zero regret by definition, not measured traffic benefit.

| Conditional report error bound ε | Mode report: optimized worst regret | Any one arrival bit report: optimized worst regret |
| --- | ---: | ---: |
| 0 | 9342/373 = 25.05 | 161236/639 = 252.33 |
| 0.10 | 161236/2023 = 79.70 | 161236/639 = 252.33 |
| 0.30 | 483708/2609 = 185.40 | 161236/639 = 252.33 |
| 0.50 | 161236/639 = 252.33 | 161236/639 = 252.33 |

Even a perfect three-bit arrival-order forecast cannot overcome the unobserved simulator-mode uncertainty in this particular case because an adverse pair at a fixed arrival order retains the original positive and negative extreme values. The ranking is **not universal**: in an actual fixed physical road, the lane model is not an arbitrary unknown switch, and more accurate forecasts might be very valuable after that structure is established. This is a value-of-information diagnostic for a deliberately constructed uncertainty set.

## Research decision

1. **Do not turn a high ratio into a headline improvement claim.** The configurations are two different whole-model service rules, not observed random safe gaps. No measured sensor detects these modes; the 90% reduction from knowing a mode is not a predicted field gain.
2. **Keep the informative failure:** detailed future demand forecasting is insufficient when a physical opportunity decisive for both actions is not modeled or observed. Stress-test this under *time-varying admissible maneuver windows* and independent lane-changing physics next; the original 10/31 v2.2 model repair showed why even one-tick lateral-motion invariants matter.
3. **Prioritize physically grounded conditions:** constant geometry / known lane rule, random safe-gap opening windows, and a decision-time observation envelope. If the effect disappears under actual lane-change rules, report that as a negative mechanistic finding.
4. Retire K047-review.html and related scripts entirely; no empty synthetic dashboard, no fabricated field measurements. Keep the DLR 18:00–18:30 UTC holdout sealed.

## Code, test and check

```sh
cd research/t2/efficiency_loop
python -m unittest -v test_finite_sensor_information
python finite_sensor_information.py ../analysis/20261121/decision-time-gate/finite_sensor_information.json
```

**5 self-contained tests passed in local Python**, including exact 3×3 linear solver, mode-0 baseline, all-information regret 0, error monotonicity, report keys and ε=0,0.5 cases. They do not replace full project tests, independent lane-changing micro-simulation, or field trials. See [machine-readable exact rational table](finite_sensor_information.json).

Next priority: independently validate any policy rule with the physically corrected world-contact engine and report **action order and actual successful lane changes**, not only 16 candidate cost differences.
