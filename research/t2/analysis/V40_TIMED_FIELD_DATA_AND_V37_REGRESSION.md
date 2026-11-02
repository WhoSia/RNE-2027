# T2 v4.0 — Timed field-data verification and v3.7 regression (2026-11-02)

Executed on archived local sources rather than using only written prior summaries.

## Runtime outcomes
- Existing v3.7 multi-OD model: six original unit tests pass. Executed example seed 2, 80s, demand end 40s: 52 generated, 30 completed, 22 unfinished, with generated=completed+unfinished and finite links maintained. Not a field replication.
- New independent `field_v40.py`: nine unit tests pass. Handles integer window start/end, duplicate and overlapping observations, adjacent-window queue boundary mismatch as a diagnostic, movement queue conservation residual, disjoint-day holdout MAE and WAPE. This is input QA + evaluation; no observed traffic data has been provided.
- Local release artifact `T2_v40_timed_field_validation_20261102.zip`, SHA256 d5019b8b6230ed7d79945cdbc37ff787ddc9560a8b88ec34bf85bbf52e5027c4. This ZIP is local unless separately uploaded; do not claim Drive custody without upload confirmation.

## Limits
- v3.7: only two operational signals, allows origin2=destination2 and unused third link, no genuine movement/route matrix and no pedestrian/bus modelling. Code expansion should repair these before adding further complexity.
- Conservation residual assumes a closed exclusive movement group. Real-world lane changes, turning changes and mid-window unmeasured arrivals invalidate the simple equality without an augmented boundary model.
- Green/headway reference from v3.9 is not a capacity theorem. v4.0 deliberately decouples interval accounting from a spurious physical bound.
- Do not treat nine test passes as evidence of traffic-prediction accuracy.

## Next gates
1. Full three *active* signal junctions and a proper multi-destination network graph with legal OD paths, independent source/sink, movement conflict matrix.
2. Movement-level event log and source/receiver queue invariants at each tick.
3. Coupled SUMO comparator with shared geometry and arrivals.
4. Field-day observation CSV for Changwon/Gyeongnam and one genuinely held-out date. Only then fit and assess signal policies.

GitHub Actions/bot contributor disallowed.