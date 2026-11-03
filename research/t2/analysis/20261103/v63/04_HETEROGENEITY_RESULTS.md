# T2 v6.3-P0 — Heterogeneity and fixed-guard limitations

Date: 20261103. Reproducible experiment on the unchanged v6.2-P2 single-junction simulator: 3 demand scenarios (balanced, main-heavy, side-heavy) × 3 braking bounds (2,3,4 m/s²) × 2 lateral acceleration bounds (1.2,2.4 m/s²) × 8 seeded arrivals (400..407) × 2 green-end guards (0s,1s) = 288 executions; 144 matched policy pairs.

## Observations
- Mean 1s-guard minus 0s-guard exposure: **+58.873 vehicle·seconds per matched pair**.
- Positive delta: 64/144 pairs; equal 80/144; negative 0/144.
- Total completed vehicle delta across all pairs: **−83** (sum across repeated synthetic configurations, not distinct vehicles in one system).
- 0s guard: **852 repeated braking-warning ticks** in just **3 matched scenario pairs** (2 distinct seed IDs); 1s guard: zero recorded braking-warning ticks in these finite trials.
- **61 of the 64 exposure-increasing pairs** had zero braking warnings even in their no-guard counterpart. Thus the fixed guard may impose service-time cost where the monitored failure was absent.
- By braking bound, mean guard exposure delta: b=2: +46.323; b=3: +39.656; b=4: +90.641 vehicle·seconds. Non-monotonic performance; do not infer population parameter effects from these selected scenarios.
- By demand: balanced +56.552, main-heavy +59.323, side-heavy +60.745 vehicle·seconds.
- Other checked warnings (sampled-pose overlaps, queue, state membership, pose jumps) were zero in these runs.

## Interpretation and limitations
This test set is **not** an independent real-world population. Several configurations share the same seed; 852 is a count of diagnostic time steps, not 852 independent risky situations. A fixed 1s guard is a service-suppressing heuristic, not a mathematically sufficient stopping controller. Results do not prove a state-dependent guard would improve safety *and* throughput: that is a follow-up falsifiable hypothesis, requiring implementation, explicit missed-safety tests, and paired comparisons.

Proposed next factor: (v,d,g,b,tau) state-variable boundary and conditionally reachable stop/go actions; compare zero guard vs fixed guard vs viability filter **only over states admitted into the viable set**, track initial-state infeasibility separately. Follow with swept-body geometry and SUMO/field data before promotion.
