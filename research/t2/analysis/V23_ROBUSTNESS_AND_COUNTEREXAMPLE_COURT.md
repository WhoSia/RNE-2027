# T2 v2.3 — Robustness sweep and apparent monotonicity counterexample

Executed local archived FIXED v2.2 engine, NOT GitHub remote head. All observations SYNTHETIC. Design seeds 0..2 × through_B_share 0/.5 × receiver_slots 2/8 × pocket 14/70m × lane_changes false/true. Constant duration 720s, demand 2100 veh/h, left share .45. 48 runs, 24 length-pairs.

Network exits long-minus-short: 23 positive, 0 ties, 1 negative; mean +37.125; range [-1,+87]. Negative case: seed=1, through_B_share=0, receiver_slots=8, lane_changes=true. Delta network exits=-1; delta stopline exits=-1; pocket-denial events=-253. This is a finite-horizon MODEL-INTERNAL counterexample candidate; not a claim of real-world harm or a proof of steady-state nonmonotonic capacity.

Important: lower pocket-entry denial counts need not imply higher final network exit count. Must inspect vehicle-level traces, stopline service, receiver occupancy and boundary truncation. Compare shifted time horizons 720,1440,3600 seconds, initial queue conditions, and same exact exogenous arrival stream, not merely seed. Verify stochastic consumption coupling across configurations.

Next expand: critical-gap acceptance, noncompliance, lane utilization, heavy vehicle mixture, variable lost time, permitted left service, pedestrian phases, bus stops, parking obstruction, detector noise, coordinated offsets, platoon overdispersion and time-varying demand. Every model extension needs an observational proxy, identifiable parameters, tests and sensitivity/holdout.

Shared Drive files: T2_v23_robustness_48_runs.csv and T2_v23_robustness_24_pairs.csv. No Actions or bot commits.
