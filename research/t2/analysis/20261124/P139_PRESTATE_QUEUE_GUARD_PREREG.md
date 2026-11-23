# P139 — Frozen pre-intervention queue guard versus calendar-only selector

Date 2026-11-24 KST. Registered before P139 seeds are run. Built from actual P136/P137 source, not from imagined traffic sensors.

## Question

Can a **pre-intervention, t=84** queue observation yield additional decision value beyond the P136-trained calendar-only baseline? Previous P136 and P137 compared **post-treatment** local denial metrics measured by running BOTH policies; such a selector is NOT deployable online. This is a **prospective within-T2 falsification**, not a field traffic-controller claim. The P137 results have already been seen, so P137 is not reused as a 'clean' test.

## Locked design and sample independence

- Fresh timestamp seeds **88801, 88802** (disjoint from 88601/88602 of P136, 88701/88702 of P137 and 88401–88408 of P135/XR1). Source-random label seeds 86001,86002 reused, which limits independence.
- Two families stochastic_uniform / stochastic_platoon4; left-share .50 / .75; 2×2×2×2 = **16 demand tapes**, 8 distinct timestamp vectors per share. Same timestamp vector reused across left-share is a matched design and **not 16 independent temporal draws**.
- 4 **pre-frozen** phase packages (phi30,phi60) = (0,30),(15,0),(7,15),(23,45); 16 tapes ×4 offsets×2 policies = **128 new full-T2 arms, 64 comparisons**.
- Existing P130 link-separated 2+2 receiver with one global 2-second downstream exit headway and S-first exit tie; original P130 source/geometry unchanged. Same t84 checkpoint across 30/60 arms per tape and 4800-second full clearance.
- The checkpoint is observed through the already-existing public `checkpoint_observation(cp)` **before invoking either policy**. Exclude all future tape entries, RNG state, future denial counters and post-policy frames. Use only `outside_A/B`, `approach_A/B`, `pocket_vehicles`, `receiver_vehicles`. Do not use route-label seed, timing seed, or upcoming arrivals as decision features.

## Two fixed rules — no fitting on P139 data

- Calendar-only baseline trained on P136 and frozen for P137: (0,30)→60, (15,0)→30, (7,15)→60, (23,45)→30.
- **Queue-guard**: start with same calendar choice. Only for (phi30,phi60)=(7,15), flip choice from 60 to 30 *iff* `receiver_vehicles >=3` AND `outside_A+outside_B+approach_A+approach_B+pocket_vehicles >=6`. Else retain 60. The numerical thresholds are prespecified heuristic hypotheses, NOT calibrated physical queue thresholds; only tested as frozen rules.
- Fixed30 and fixed60 as supplementary references; hindsight oracle for regret calculation only. Explicitly compare regret and exact-policy accuracy. The guard offers a putative benefit only for the (7,15) stratum; report its triggered count and conditional confusion, not just pooled results.

## Primary gate and falsifier

1. Integrity: all 60 vehicle IDs exit in each of 128 arms; all denial attempts / distinct denied ticks reconcile to trace events; both policy arms share exact same t84 state, its observation unchanged before and after either run; 16 unique tape identities across shares and offset reuse controlled.
2. Primary: queue-guard must reduce **pooled total regret by >=10% relative to calendar-only** on these P139 tapes and avoid a >10% excess regret in any share or family stratum. If the calendar-only regret is zero, require exact zero regret from the guard instead, and mark improvement 'not estimable'.
3. Secondary: paired per-tape regret differences (four offsets grouped under each of 16 original tapes); report better/equal/worse cases. Do NOT treat 64 outcomes as 64 independent intersection samples.
4. If no guard triggers, classify as **UNINFORMATIVE_NO_TRIGGERS**, not a validation. If any invariant fails, classify INVALID and do not claim success.

## Limitations

A state-based rule is 'available at decision time' **within the synthetic simulator**, but the modeled outside/approach/receiver measurements are not proven to be available from real sensors. This candidate alters both cycle and offset package together, not pure cycle-length optimization. The public rule is a preregistered counterexample test, and a failure must not be rescued by tuning on P139 data; any changed threshold requires separately registered P140 on new seeds. No SUMO equivalence has been established (XR3 E0e still failed).
