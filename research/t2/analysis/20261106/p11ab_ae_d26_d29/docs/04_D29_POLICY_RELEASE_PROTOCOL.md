# D29 — Numerical negative result and the next policy axis (sandbox-only)

**Core negative result.** With 22 synthetic cars, a 2-link corridor, fixed receiving closure until 20s and unchanged demand, the last completion timestamp varies severely with `dt`: 109.0s at 1.0s; 87.0s at .5s; 81.5s at .25s; 78.625s at .125s. Do not use such numbers directly as a ranking of realistic signal policies.

Next version may begin separate research units on **exploratory signal-policy methods**, because the user explicitly authorized policy research resumption. However the old `P12-A/B` research remains historically sealed and frozen, and no production optimizer or live traffic actuation can be promoted from this uncalibrated model.

**Before policy ranking is supportable:** (1) original P10 replay reproducible (PASS), (2) new event engine causal and finite-dt stable (FAIL/UNKNOWN), (3) matched independent SUMO (HOLD), (4) observed field/holdout fit (HOLD), (5) strong heuristic baselines and uncertainty bands (HOLD).

Exploratory next-study design: fixed-time candidate set with equal legal constraints, common random arrival streams, chronological event invariants for each candidate, paired holdout cohorts, multiple dt bands, bootstrap clustered at site/date level, and leave-one-condition-out stress. Report **incomparable** if confidence/rank stability gates fail. This is study design, not an executed signal-policy experiment here.
