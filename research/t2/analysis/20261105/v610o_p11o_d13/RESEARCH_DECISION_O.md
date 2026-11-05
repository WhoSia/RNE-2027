# T2 v6.10-O / P11-O / D13 — observation-unit sensitivity audit
2026-11-05. Exploratory computations on previously derived Michigan MARWIS run-length data, NOT raw CSV. P12 policy frozen.

## Observed aggregate
Six source trajectories: 5,967 synchronized frame rows; 19 constant-value segments; 13 value-change boundaries. Six trips are not sufficient to identify independent sensor-update events.

| Aggregation | Asphalt-labeled | Concrete-labeled | Difference |
|---|---:|---:|---:|
| Frame weighted | 0.26043217 | 0.24038361 | 0.02004856 |
| Constant-segment equally weighted | 0.25475666 | 0.24258523 | 0.01217143 |
| Equal trip weighting of frame means | 0.26033558 | 0.24000006 | 0.02033552 |

Leave-one-trip-out row-weighted contrasts range from 0.01128930 to 0.03132484. These are purely DESCRIPTIVE and NOT material causal effects; filenames, snow/ice and trip/site/time confound the comparison. Both frame rows and constant runs cannot be automatically treated as IID. No p-values, confidence intervals or road-grip/safety claims.

## Next gates
Original raw-byte custody and hash verification; device update clock and missingness audit; independent site/day samples; external OpenDRIVE geometry comparison; P11 event-causality and SUMO same-conditions replay before any optimizer.

An independently executed local Python script reconstructs these statistics from recorded friction-block starting rows and values, with hard row/block/count assertions. Source 6-file derived audit: research/t2/analysis/20261105/v610n_p11n_d12/data/michigan_marwis_six_trajectories_derived_audit.json.
