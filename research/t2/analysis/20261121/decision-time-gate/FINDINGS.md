# Decision-time information gate: a real sensor is not a future oracle

Date: 2026-11-21. This supplements the synthetic [bypass-window experiment](../bypass-windows/FINDINGS.md) and [new-seed panel](../timing-generalization/FINDINGS.md).

## Research decision

**Keep the phase-order reversal as the explanatory counterexample, but demote perfect knowledge of future lane-change opportunities to an oracle upper bound.** A controller must receive a timestamped, lawful pre-commitment measurement or forecast before it can use that information. The simulator's complete future arrival order and realized gap calendar must not silently enter a field-feasible policy.

This distinction sharpens, rather than weakens, our exhibition result: exactly the same present observation can be compatible with opposite optimal phase orders. Which *prospective* signal can resolve that ambiguity, within a cost and latency budget, is the next engineering question.

## Exact two-world calculation

Define Δ(w) = total cost of left-first minus total cost of through-first in world w. A negative Δ favors left-first, a positive Δ favors through-first. For compatible worlds D, the worst regret of each fixed order is

- left-first: max(0, max D)
- through-first: max(0, −min D)
- deterministic minimax: min of those two quantities.

The results below come from **preselected synthetic examples** under terminal penalty 60. They are not field counts, empirical forecast accuracy, or prevalence estimates.

| Matched example | Δ early gap | Δ late gap | Fixed deterministic minimax regret | Complete future-gap oracle |
| --- | ---: | ---: | ---: | ---: |
| Original (terminal-sensitive) | −3 | +35 | 3 | 0 |
| New seed 337 (persists at penalty 0) | −113 | +31 | 31 | 0 |

In each example the paired worlds have the same predecision arrival bits, stored-queue counts, and signal history. Consequently any observation that is strictly a deterministic function of those identical inputs has exactly the **same** branch for both worlds and cannot reduce regret. The oracle labels “early” and “late” separate the two, but they refer to future events, not automatically to a usable sensor.

## A bounded-error forecast can help, but only if it arrives

Consider a binary forecast issued before commitment, with conditional error probability no greater than ε **in each of the two true worlds**. The simple deterministic policy that follows the forecast has worst expected regret at most max(−Δearly, Δlate) ε; ignoring it and selecting the fixed minimax order is always permitted. The sensor itself may have cost c measured in the same cost units.

For the new seed-337 witness, the bounds are

- fixed deterministic minimax: 31
- best fixed randomized mix without sensing: 3503/144 ≈ 24.33 (separate benchmark)
- follow-forecast bound: 113 ε + c
- guaranteed improvement over the fixed deterministic order requires **113 ε + c < 31**
- with c=0, the error threshold is ε < 31/113 ≈ 27.43%, or at least 72.57% conditional correctness in both worlds
- at ε=10%, the forecast-following bound is 11.3 and must cost less than 19.7 to beat the fixed policy
- against the randomized no-sensor baseline, deterministic follow-forecast with c=0 needs ε < 31/144 ≈ 21.53%
- in the original sensitive witness, beating fixed requires ε < 3/35 ≈ 8.57%, illustrating that an attractive sign reversal need not be an economically useful sensing target.

These are **sufficient bounds for a specified deterministic forecast-following rule in a restricted two-world problem**. They do not assert global optimality over randomized sensor-conditioned policies. They are not a measured classification accuracy, confidence interval, or deployable traffic control.

## Causal timing gate

A direct observation made at t_obs with processing and actuation-related reporting latency ℓ can be used for a commitment at t_dec only when t_obs + ℓ ≤ t_dec. A forecast issued before commitment can be admitted if none of its input features use subsequently realized future events. Forecast provenance remains an empirical audit requirement; a timestamp by itself cannot establish that fact.

Here t_dec = 84. An opening first seen at tick 84 may discriminate early vs late in the *two-world* toy case only with zero latency. An observation reported one tick later is too late for that decision, even if its label is perfect. Real systems also have phase-transition and minimum-green constraints; those are not yet encoded by this two-world certificate.

### Implementation and checks

`research/t2/efficiency_loop/decision_time_gate.py` contains deterministic action regret, conditional partitioning, admissibility checks, an error/cost decision and a small forecast frontier. `test_decision_time_gate.py` covers input rejection, prefix indistinguishability, late reports, threshold arithmetic and fallback behavior.

Reproduce from `research/t2/efficiency_loop`:

```sh
python -m unittest -v test_decision_time_gate
python decision_time_gate.py ../analysis/20261121/decision-time-gate/certificate.json
```

Five self-contained tests passed in a local clean Python execution. This is **not** a claim that the full repository test suite, SUMO, physical driver maneuvers, or a browser renderer ran in the current execution environment.

## Next two research cycles

**A — feasible input:** From the students' first eight consecutive signal cycles, record the frame/video timestamp, candidate car's position, receiver space, gap opening/closing and the exact time each variable becomes available. Mark hidden events unknown, not zero. Produce the first feature/latency matrix; do not train a field predictor on eight hand-selected cycles.

**B — choice under uncertainty:** In an independent synthetic panel fix a forecast-generating rule based solely on precommitment features, then compare fixed order, simple forecast-following with fallback, and perfect-information oracle *on exactly the same arrival traces*. Add an action-latency boundary and pedestrian safety constraints before recommending any operational controller.

K047 remains a discharge and visibility reference, not a confirmed pocket spillback field demonstration. Its sealed 18:00–18:30 UTC evaluation window remains unopened.
