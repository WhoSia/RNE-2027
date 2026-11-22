# T2 P32 — Aggregate observational equivalence does not determine individual crossing histories

2026-11-22. [Precommitted P32 protocol](P32_PER_VEHICLE_EXIT_RECONSTRUCTION_PREREG_20261122.md) at `23d74b03a0573b33b84fa754d90a14b6e5124837`. Experimental interpretation is **exploratory** after P30/P31. **No original physical engine was modified.**

## Data, method and exact results
- Full unchanged simulator `dual_lane_v11.py` and finite receiving-cell process `receiving_cells_v15.py`, same P30 (64) + P31 (128) worlds with 4 + 8 **unique** complete arrival tapes; not 192 independent traffic days.
- From original `service_events`, collect `(vehicle_id,t)` for each stopline crossing. From consecutive `frames`, infer vehicle-specific exit time when an ID present in the preceding receiving-link snapshot disappears from the next. This is valid under the frozen *deterministic cellular assumptions*, **not an independent microscopic physics model**. Reconstructed S/L network exit counts agree with the simulator's aggregate counters in all evaluated paths, with conserved vehicle IDs, right-censoring at t240 for non-exits and adversarial corruption checks.
- Two phase alternatives (abstract L-stage 6s vs10s) start from the exact same physical checkpoint t84 in each world. Aggregate score is `physical_transfer_screen.score(...,60)`. Complete output JSON SHA-256 `fa0e1447377e2aa716dd12e348e3a8a2c17dc4a165913da2883b22110e3f636e`, reproduction bundle contains all 192 world-level rows and raw exact code.
- [11 tests](test_p32_id_corridor_exit_audit.py) **11/11 passed**. Remote exact source blobs for [runner](p32_id_corridor_exit_audit.py) `dea56149c017cfd49116d53f98385eb0294bce30`, test `9f2a0d0f4b0ea0fc590fd9124405eeba3f33dd66`; log SHA256 `391c2eee83e43d66bb570ecca4d83760f79a8c96c089da0d6025b04bde8f6e48`.

| Cohort | Cost equal | **All aggregate cost/count measures equal but ID/time record different** | Different receiving exit ID set | Different downstream exit times among common IDs |
|---|---:|---:|---:|---:|
| P30 64 reused worlds | 64 | **16** | 2 | 2 |
| P31 128 fresh-clock worlds | 119 | **31** | 27 | 25 |
| Total | 183 | **47** | 29 | 27 |

A slightly broader condition uses *score equality alone*: 16 P30 and 32 P31 worlds have changed crossing/exit histories. The difference between 31 and 32 occurs because one P31 world has identical score but at least one aggregate count differs.

**Strong illustrative case:** P30 key `[1650,0.5,112,4,0,14.0,0.0]`: six- vs ten-second stage gives **equal aggregate cost, total discharge and remaining**, while at least one vehicle's *stopline crossing* is **27s earlier** under the 10s scenario. Its **downstream exit times are unchanged** among common exiting IDs. Do not misstate crossing advantage as completed trip time improvement.

## Independent reviewer / hostile checks and corrections
1. **Construct-validity reviewer:** distinguish denial attempts, unique rejected IDs, crossing events, downstream receiver exits, completed door-to-door travel times (unobserved). A reconstructed receiver exit is not an independently observed field detector event.
2. **Measurement reviewer:** initial P32 code incorrectly said `left-censored`; corrected to **right-censored** t240, reran. Initial group label incorrectly implied *complete vehicle event histories*; renamed to `identical_crossing_and_downstream_exit_histories`. Both are separate fix commits; do not attribute changed semantics to unchanged model physics.
3. **Data quality reviewer:** archived P31 output `baseline_score` mistakenly equals `baseline["remaining"]` in **128/128** rows, not `score(...,60)`. Historical P31 is left byte-identical. New P32 output explicitly preserves **both** `baseline_true_score` and `baseline_remaining`. Never report old label as a score.
4. **Statistics reviewer:** 192 model geometry pairings use just 12 independent complete arrival tapes. Avoid binomial confidence intervals, p-values, or '47 separate days' rhetoric.
5. **Causality reviewer:** the same frozen checkpoint within each policy pair supports a conditional *model* intervention contrast. Different clock families have different predecision states; do not attribute between-family differences solely to stage choice.
6. **Paper-novelty reviewer:** neither a new proof of optimal traffic control nor a demonstrated policy **sign reversal under one detector observation** has been established. P31 found 9 worlds with 10s−6s score −189, the others zero; no positive sign. Aggregation aliasing alone is a valid *measurement counterexample*, but not yet a policy-ranking impossibility theorem.

## Separate practical research axes
**Science-fair / exhibition:** observable 'green but no discharge' must be differentiated from missing demand, downstream blockage, yielding to other road users, pocket spillback and sensor non-detection. Use DLR map/signal/trajectory synchronized observation and positive-control movement, not synthetic claims as field facts. Follow existing LR-J and LR-K Notion Harvest; existing K047 counts are not proven zero-discharge events.

**Paper candidate (test before claiming originality):** For coarsened detector observation `Y=h(X)`, finite-storage feasible microhistories `X(Y)`, and two matched simulated action costs, define
`L(Y)=inf_{x in X(Y)}[J_10(x)-J_6(x)]`, `U(Y)=sup_{x in X(Y)}[J_10(x)-J_6(x)]`.
Do not assume sharpness or observation-constrained physical feasibility merely from a finite enumerated sample. A sign-changing interval (L<0<U) would disallow unambiguous action ranking on Y alone; current P32 **does not demonstrate such a pair**. A zero-to-negative interval could already identify strict-benefit ambiguity, not a reversal. Compare complete stopline-count-only, queue-count, receiving-cell and lane-occupancy observation tiers with identical base model physics. The proposed method is a deterministic **identified-set and value-of-information audit**, not unexplained reinforcement learning.

**Literature context / non-novelty checks:** Daganzo (1994) cell transmission / finite supply; Varaiya (2013) max-pressure / finite storage limitation, DOI 10.1016/j.trc.2013.08.014; Emtenan & Day (2021) left-turn storage and oversaturated through movement, DOI 10.1177/03611981211017139; Manski's policy choice under ambiguity (e.g. https://doi.org/10.1146/annurev-economics-061109-080359) gives a *decision theoretic framing* but **does not prove this traffic model result**. Recently published finite-capacity network work (https://www.sciencedirect.com/science/article/abs/pii/S0191261523002011) and sensor-limited signal control (https://www.nature.com/articles/s41598-025-89626-5) narrow any claim of novelty. Read those papers' full methods and verify dataset overlap before a novelty claim.

## Operational and branch decision
`main` includes the complete old T2 branch ancestry (336 commits ahead, zero unique commits on old branch). [Branch audit](P32_MAIN_ONLY_BRANCH_CONSOLIDATION_AUDIT_20261122.md). No automatic merge needed; remote old branch deletion **not executed** because the available GitHub connection exposes no delete-ref action. Retain all official P19–P32 result and source hashes. No Actions/bot commits.

## P33 minimum viable falsifier
Choose **one** sensor observation definition available at decision time, generate at least two physically admissible hidden histories with equal observed Y, then find a *policy-difference discordance* and independent microphysical comparison. If all permitted histories agree, publish a **null identifiability result** and prioritize DLR/SUMO empirical calibration. Do not train on or show to a decision rule future arrival timestamps as if a sensor knew them.
