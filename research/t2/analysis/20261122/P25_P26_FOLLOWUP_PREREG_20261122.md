# T2-P25/P26 preregistration — receiver discharge and intervention-dose stress

2026-11-22 KST. Written before evaluating either new cohort. This is an **uncalibrated, synthetic 1D 7-meter-cell vehicle simulator**, never a deployable traffic signal schedule. GitHub source `dual_lane_v11.py`, `spatial_v10.py`, `receiving_cells_v15.py` and P19 original are SHA-sealed from `main`. No live controller, yellow, all-red, pedestrian clearances, sensor RF data, or actual SUMO numerical validation.

## P25: receiver discharge rate as effect modifier (new physical cohort)
Freeze P19's synthetic demand scenarios and arrival generator, but take seed subset `(112,113,116,117)` spanning both 1650/1800 vph regimes. Independent arrival-tape units **4**, reused across geometry. Factorial: 4 regime/seed pairs × 2 receiver cells (2,4) × 2 downstream offsets (0,15 seconds) × 2 pocket lengths (14,28 meters) × 2 B lane assignments (0,.5) × **3 receiver exit headways (1,2,4 seconds)** = **192 worlds**. Every world is replayed baseline and the same abstract 8s left-stage `((84,87,'-'),(87,95,'L'),(95,120,'-'))`, from one identical tick84 checkpoint. Because changing receiver headway changes histories **before tick84**, cross-headway contrasts are effect modification, **not a same-state causal effect of changing headway at tick84**. Mandatory reference gate: all headway=2 rows must match frozen P19 model deltas and tape hashes exactly (64 worlds). Primary outcome model cost delta at terminal penalty 60. Secondary: receiver admissions/exits, denials, remaining cars; report per-headway sign distribution and geometry-matched headway1↔4 sign reversals with strict epsilon 5 and ≥2 independent tape hashes where available. Do not report pseudo-replication as 192 independent independent runs.

## P26: matched-state treatment dose (same checkpoint, meaningful within-world comparison)
Freeze another **64 worlds**: 4 regime/seed pairs × 2 receiving capacities × 2 offsets × 2 pocket lengths × 2 B shares, with `receiver_headway_s=2`. For each exact t84 checkpoint, calculate control baseline and exactly **three model-native abstract interventions** with 3s no-service before and cutoff120:
- 6s: `((84,87,'-'),(87,93,'L'),(93,120,'-'))`
- 8s: `((84,87,'-'),(87,95,'L'),(95,120,'-'))`
- 10s: `((84,87,'-'),(87,97,'L'),(97,120,'-'))`
All three meet an **illustrative** minimum green >=6 s, which is neither necessary nor sufficient for real signal legality. Each baseline vs treatment shares **the identical physical world, exact checkpoint bytes and future arrivals**, so comparisons of candidate policy effects within the world are paired synthetic counterfactuals. Validate 8s deltas against frozen P19 (64/64). Primary: cost deltas for 6/8/10 at penalty60 and within-world winning candidate, including ties. Secondary: non-monotone dose-response, worse-then-better/better-then-worse patterns, and number of cases where *all* three harms vs no intervention. Any post-hoc subgroup interpretation must be labeled exploratory. A stationary zero-difference world is not an efficacy witness.

## Non-negotiable gates
- Source is exact original main repository physical engine; no reconstructed historical archive code substituted.
- File/integrity: full prior P19 result SHA, exact engine Git blob, code test SHA documented; preserve frozen inputs, deterministic JSON and rerun equality.
- `score()` vehicle conservation, same timestamped demand, no changes to checkpoint object, and baseline direct/resume check in first case.
- 4 independent full arrival tapes per arm at most. Report full-world frequencies as descriptive finite scenario counts, no p-values or CI pretending those rows independent.
- If any model's built-in clearance validator fails for an action, **record the failure; do not relax the validator or produce a claimed controller plan**.
- New commits to `main` only; no GitHub Actions / bot; K047 sealed; large CIM data HOLD; user-downloaded INTERACTION awaiting accessible Drive upload.
