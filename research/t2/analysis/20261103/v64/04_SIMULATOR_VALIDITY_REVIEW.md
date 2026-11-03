# T2 v6.4-P0 — Special researcher review, 20261103

## Accepted
- Field capture/validation specification based on FHWA and SUMO, including explicit units and provenance.
- Eight executable tests in standalone Python; source + original synthetic CSV in Drive ZIP with SHA-256 manifest.
- Synthetic noisy-sensor discrimination reanalysis with an explicit decision-value negative control.
- Matched training vs seed-heldout scenario analysis with arbitrary warning-penalty sensitivity.
## Held / Not established
- Actual Korean intersection calibration: no field dataset yet.
- Pedestrian/bicycle/bus geometry and multi-lane parallel occupancy: NOT integrated.
- SUMO independent simulation: NOT run.
- Validity of fixed 1s green-end guard as real safety law: NOT established.
- Missingness, calibrated sensor error, actual optimal observation: NOT established.
- Statistical confidence using 30,000 noise draws as if they were independent field days: DISALLOWED.
## Priority
1. Secure **permitted** real signal/geometry/turning counts and paired queue/travel-time observation with clear provenance and no personal identifying data.
2. Model real lane connectivity and collision-point occupation; do not simply add abstract physics features.
3. Compare simple baseline, T2 and SUMO at matching input granularity with held-out days.
4. On policy-science side preregister observation channels, risk/cost interpretation, and model class before holdout experiments.
Status: methodology accepted, field/operational claim held.
