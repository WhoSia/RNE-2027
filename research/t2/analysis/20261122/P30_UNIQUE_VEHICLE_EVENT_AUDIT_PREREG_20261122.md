# T2 P30 — Paired unique-vehicle denial and waiting-time audit (preregistered 2026-11-22)

## Motivation and scientific boundary
P26/P28 showed **64/64** cost-equivalent synthetic worlds where 10s vs6s intervention added exactly four **receiver denied attempts**. This is an internal instrumentation concern. The exact main physical engine records `service_events` with `(t, vehicle_id, movement, reason)` and `frames` with lane/receiver occupancies. Receiver exits are also stored in the checkpoint link object, but the public `run` result does not expose their vehicle IDs. **Do not invent downstream per-vehicle times from absent output.** Treat an unobserved release as censored unless reconstructing unambiguously from frame-to-frame identity.

## Frozen P30 evaluation
- Cohort: all **64** P26 geometry/tape classes, seeds (112,113,116,117), receiver headway2, the exact original full timestamp arrival tapes. **Four unique arrival tapes**, not 64 independent observations.
- From the exact tick84 checkpoint, replay **baseline, 6s, 10s** phase variants, trace=True. Do not modify `dual_lane_v11.py`, `receiving_cells_v15.py`, `score`, original frozen P19 result or original P25–29 results.
- Primary paired outcomes over the **entire 240-second trace**: number of events `receiver_capacity_full/receiver_entry_cell_busy`; number of **distinct** rejected `vehicle_id`; sum and maximum per-ID refusal attempts; number of unique time-contiguous refusal episodes (interruptions allowed only if `t` differs by more than 1); first-denial-to-first-post-denial-crossing time if observed, otherwise right-censor at end tick240. Identity is assigned as the index in the same full arrival tape.
- Secondary: number of actual `stopline_cross` events by movement, receiver cell occupancy in frames, end remaining and model score. Audit count of trace denial attempts equals model field `receiver_denied_attempts` and stopline count equals `exit_L+exit_S` on each run. Check all event IDs in range, no ID crosses twice, no denial after crossing, and no premature crossing before arrival. Match frozen P26 score and denied attempts for exact 6s/10s action independently.
- No inferred event ID for `common_exit_denied_s` because current trace doesn't emit those as vehicle-specific events: coverage disclosure.
- Distinguish per-ID time to crossing from total end-to-end travel time. If nobody crosses before t240, censored, not zero wait. Compare within-world differences, report full 64 records and grouped cross-tabs. No p-values based on geometry reusing four tapes.

## Anti-overclaim gate
This is **posthoc selected after observing P28**, hence explicitly exploratory in interpretation even though the exact P30 analysis plan is committed before evaluation. A model-only stage schedule with `-` is NOT real yellow/red/pedestrian clearance; do not use for a field controller. P30 has no independent SUMO/traffic calibration.
