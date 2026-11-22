# P38 — R&E 2027 evidence and decision review

## Scoring rules

Measured rates are ratios with named denominators. An unmeasured accuracy, precision or recall is NA. Evidence scores are ordinal research judgments, not calibrated probabilities: 0 = missing evidence, .25 = specification or toy test, .50 = direct repeatable evidence within one domain, .75 = independent reference or substantially different conditions within scope, 1 = independent target-domain holdout with declared error limits. Intermediate scores are reserved for partial completion of the next anchor. The current rank of future experiments uses separate estimates: relevance to signal efficiency, discriminatory power, readiness, one-week feasibility, weighted .35/.30/.20/.15. These priorities are revisable under new evidence.

## Historical results and evidential scores

| Research question | Reproducibility | Construct / physical fidelity | External validity | Evidence |
| --- | ---: | ---: | ---: | --- |
| Finite storage, service and vehicle conservation | .90 | .75 | .30 | P18 144/144 archived pair rows replayed; P19 independent shadow 512 paths, 122880 ticks without mismatch; current core tests 21/21. External vehicle-trajectory error remains NA. |
| Lane-change window and bay spillback | .85 | .60 | .25 | PHYS-01/02/03 total 704 runs; PHYS-02 early/late 25/48 reversals under penalty 60; PHYS-03 zone70 0/16 versus zone100 3/16. |
| Yellow, clearance and phase priority | .75 | .50 | .40 | November 17 same-input 24/24 vehicles across cases; point queue cost difference +110 and SUMO −99.25. Full physical-engine parity and attribution to yellow remain open. |
| Green extension and receiver supply | .85 | .60 | .25 | P26 64/64 cost ties across 6/8/10s; P27 64/128 lower cost at 24 vs 6s, exploratory; denial attempts can change with equal cost. |
| Arrival-law robustness and event identity | .80 | .60 | .25 | P31 9/128 changed phase-duration equality under new arrival tapes; P32 47/192 equal aggregates and costs with differing recorded vehicle histories. |
| Detector latency, support and policy abstention | .80 | .55 | .25 | PHYS-07/08/09 paired stress: geometry fallback failed at low turning demand; support abstention avoided that modeled loss while excluding some helpful nominal cases. |
| Signal/stopline temporal alignment | .85 | .60 | .40 | Same-source P34 match .941 at ±1s and .412 at ±.5s; P35 hindsight exposure .647. Independent crossing precision/recall NA. |
| Signal group and movement | .80 | .65 | .40 | Known daytime map Figure 1; P37 nighttime path support .800 overall, .750 straight, 1.000 left (n=1). True signal-head attribution accuracy NA. |
| Green-time blockage diagnosis | .65 | .45 | .20 | P38 selected-frame coverage .393 among 290 slots with neither a detected crossing nor a boundary-straddling crossing; simultaneous slow upstream and receiver evidence 0/114 selected frames with no detected crossing. Actual blockage precision/recall NA. |
| Real-world policy benefit / safety | .50 | .30 | .00 | Synthetic policy experiments and one historical simulator comparison. Deployment benefit, conflict rate and pedestrian delay validation NA. |
| RF-CURTAIN cause recognition | .50 | .25 | .00 | Synthetic noisy-channel and regret studies; real CSI accuracy, cause-label precision/recall and benefit NA. |

Physical fidelity by component: storage/conservation .75; lane-level geometry .65; lane-change acceptance .55; acceleration/braking .45; saturation headway .45; queue-start response .40; yellow/dilemma transition .40; yielding/permissive turn .35; pedestrians .25; wet-road sensitivity .25; transit dwell .25; external trajectory calibration .25. These are evidence maturity for the T2 engine, not geometric or engineering tolerances. Avoid averaging them into a single 'realism' percentage.

## Measured metrics with limited scope

- P34 weak time-co-presence baseline against publisher labels: precision 17/322 = .053, recall 17/17 = 1.000, specificity 571/876 = .652, accuracy 588/893 = .658. These are internal publisher-label metrics and illustrate why recall alone is misleading.
- P38: 292 half-second slots bracketed by consecutive green samples, 1 with a detected crossing, 1 with an ambiguous crossing interval, and 290 with neither. Of the 290, 114 had a selected direct frame (.393) and 176 did not (.607). Within the 114 frames, 4 had a slow upstream center without a slow receiver center (.035), and 0 had both (.000). Slots are correlated; no binomial precision, prevalence or causal blockage claim follows. Missing capture or a missing center cannot establish an empty road. The screen keeps the historical ±26 ms frame-alignment tolerance and 2 m/s slow proxy.
- P37 path support is an observed agreement fraction, with the map-based assignment and route test sharing the same underlying source. Continuously displayed signal accuracy: NA.

## Candidate comparison

| Experiment | Relevance | Discrimination | Readiness | One-week feasibility | Weighted |
| --- | ---: | ---: | ---: | ---: | ---: |
| Same geometry T2/SUMO factorial: bay spillback, receiver capacity and yellow semantics | .99 | .95 | .80 | .70 | 0.896 |
| Open green windows with independently labeled upstream demand and downstream occupancy | .99 | .93 | .67 | .75 | 0.872 |
| Held-out burst/platoon arrival with pressure, fixed-time and guarded phase extension | .96 | .86 | .80 | .85 | 0.881 |
| Replay equal-cost pairs with per-vehicle P95 delay and maximum queue | .91 | .80 | .90 | .90 | 0.874 |
| Protected/permissive turn, pedestrians and bus dwell as separate contrasts | .89 | .81 | .55 | .55 | 0.747 |
| Motorcycle/heavy-vehicle mixture and wet braking on saturation flow | .72 | .72 | .50 | .60 | 0.658 |
| Upstream offset with neighboring signal and finite receiving link | .88 | .78 | .65 | .65 | 0.769 |
| Right-turn branching and movement-specific receiver lanes | .86 | .82 | .60 | .65 | .765 |
| Pocket full versus empty-but-inaccessible: independent queue labels | .94 | .92 | .70 | .80 | .869 |
| Camera-free RF vs simple occupancy sensor on a tabletop queue | .70 | .75 | .35 | .45 | 0.607 |

Execute the already available green-window screen and preserve its missing-data denominator. Prioritize same-geometry SUMO physical contrast for the next engine answer. Run arrival-family and objective comparisons in the policy track. Screen inputs across arrival timing (renewal, platooned, bursty), pocket and storage lengths, stop-line headways, acceleration, yellow clearance, pedestrian competing demands, turn distribution, upstream offset, buses, class mix, and observation delay. Test mechanism-specific contrasts before interactions. Use matched arrival tapes and state, then vary independently across entire tapes/sites; distinguish absolute cost, regret, P95 delay, queue, throughput and receiver refusals.

## Sources

[Historical factor landscape](../V18_FACTOR_LANDSCAPE_AND_PRIORITY.md), [PHYS evidence](../20261121/decision-time-gate/PHYS_192_384_128_FINDINGS.md), [November 17 SUMO pair](../../efficiency_loop/SUMO_PHASE_PAIR.md), [P25–P29](../20261122/P25_P29_PHYSICAL_FOLLOWUP_FINDINGS_20261122.md), [P32](../20261122/P32_ID_CORRIDOR_EXIT_AUDIT_AND_PAPER_AXIS_20261122.md), [P35](P35_FORWARD_ONLY_FIELD_TIMING_FINDINGS_20261123.md), [P37](P37_NIGHT_ROUTE_FINDINGS.md), [P38 counts](P38_GREEN_OBSERVATION_RESULT.json).

## P38 exploratory arrival follow-up

Reused P31 with four new seeds and compressed four-platoon span from 15 s to 5 s. Each 6 s vs 10 s action pair shares the decision checkpoint within its world. Across 8 unique tapes and 128 worlds, modeled cost ties were 64/64 uniform (1.000) and 55/64 platoon (.859). Distinct rejected-vehicle counts increased in 36/64 uniform (.563) and 42/64 platoon (.656). These are descriptive contrasts clustered by tape. Both seed and span differ from historical P31, so historical differences do not identify a span effect. Hold the seeds fixed across spans for a mechanism-specific follow-up.

From this directory: `PYTHONPATH=../..:../20261122 python p38_burst_pilot.py`. See [pilot results](P38_BURST_PILOT.json).
