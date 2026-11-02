# T2 v5.4 — Abstract conflict audit (2026-11-02)

Independent movement-conflict audit against the unchanged v5.3 network engine: 48 synthetic runs (3 demand cohorts × 8 matched seeds × 2 signal plans), 7,444 individual junction crossing events, zero illegal-phase or simultaneous incompatible crossings. Nine new local tests pass. Reproduced v5.3 protected-minus-two-stage mean exposure increases: balanced +895.81, main_peak +863.69, side_peak +2202.25 vehicle-seconds.

**Important:** A conservative graph treats any two distinct movement types as conflicting. Existing code discharges at most one vehicle at each junction per tick. Therefore absence of conflicting recorded crossings is largely an architectural invariant, NOT a geometry-based collision-safety verification. Simultaneous nonconflicting movements, opposing approaches, pedestrian calls, real turning paths and signal phase legality under actual road geometry remain outside this model.

Exhibition position: a reproducible incremental engineering artifact, not real intersection signal safety validation. Paper position: uncertainty in an inferred movement-conflict graph may change feasible control policies, an untested hypothesis.

Local 7-file reproducible ZIP: T2_v54_conflict_audit_20261102.zip; SHA256 0395129c40494a76c215f42110165061ee3612346ce0a96c5ab90343843d90de. GitHub conflict auditor is a simplified functional equivalent of the fuller local module; for complete tests, manifests and event-level CSV use the ZIP.

Next mandatory gate: infer actual conflict pairs from surveyed lane-to-lane paths (including crossings, merges and pedestrian movements), allow nonconflicting concurrent service, and recheck time-interval conflicts with finer movement timing. Run independent SUMO and real Korean observation comparison. Do not operate public signals experimentally.