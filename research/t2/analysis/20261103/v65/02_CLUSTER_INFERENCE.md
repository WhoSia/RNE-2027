# v6.5 — Cluster inference and research limitations

The v6.4 cohort table has 54 rows (3 profiles × 3 demands × 6 seeds) but 18 paired demand×seed blocks for each nonbaseline profile. Since each seed is reused across all 3 demand strata, the relevant seed-level re-sampling units are only 6 clusters, not 54 independent observations.

A seeded 20,000-resample percentile cluster bootstrap (resample the six seed indices, keeping all three demand cases together) yields:

late_concentrated minus uniform:
* 155s mean -263.25 vehicle·s; 95% percentile interval [-364.75, -148.18]
* 1000s mean +340.58; interval [+51.28, +637.14]
* differential unobserved tail +603.83; interval [+365.40, +811.61]

platoon_12s minus uniform:
* 155s mean +73.08; interval [+37.75, +98.90]
* 1000s mean -20.92; interval [-155.85, +89.79]
* differential unobserved tail -94; interval [-194.92, -9.11]

Intervals are exploratory sensitivity estimates for this deliberately constructed synthetic 6-seed scenario set. They do not establish coverage for observed road traffic. In particular platoon long-horizon change includes zero.

At 155s the total unfinished-vehicle counts (sum over 18 scenario runs) are baseline 376, late 420, platoon 368. At 1000s all are zero.

Reviewer gate: report horizon, generated/completed counts, arrival profiles and incomplete-vehicle exposure before presenting any traffic performance comparison. Distinguish accumulated vehicle·seconds from completed-vehicle mean travel time.