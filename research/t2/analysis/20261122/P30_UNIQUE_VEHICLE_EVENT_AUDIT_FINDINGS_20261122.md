# T2 P30 — Distinct vehicle IDs reveal cost-equivalent but physically different service histories

2026-11-22 KST. [P30 analysis prereg](P30_UNIQUE_VEHICLE_EVENT_AUDIT_PREREG_20261122.md) committed at `5b65010827eba10b0c2dd8460a9b50689d8e0c7b` before evaluation, **though the research question arose after inspecting P28 and therefore is exploratory**.

## Exact-source method
- Original main core: `dual_lane_v11.py` and `receiving_cells_v15.py`, unchanged; [runner](p30_unique_vehicle_event_audit.py) exact Git blob `f4b6adfecab9639616182a35591014befb517362`.
- Frozen P26 full result SHA256 `640ec195830abae2ab99d202d43d92aaf3cbbc5f875a0ddc6765fe82f20c19e4`. All 64 geometries/tapes, original seeds112,113,116,117; **4 unique full arrival tapes**. Same tick84 physical checkpoint, trace-enabled interventions with 6 and10s synthetic L-stage.
- Event identity `vehicle_id` equals full arrival event index. Reject malformed ID, route mismatch, missing denial or repeated stopline-cross; reject any mismatch with engine `receiver_denied_attempts` and `exit_S+exit_L`. ID joins are within each world and intervention, not across traffic datasets.
- Complete P30 full output JSON SHA256 `6fc5d2e02192f8dd4ad97f420bbb8961bb0339d2c7ca01bc3a7ac16c3a43763f` (preserved in reproduction bundle). [Machine summary](P30_UNIQUE_VEHICLE_EVENT_AUDIT_RESULTS_20261122.json).
- [Nine regression/adversarial tests](test_p30_unique_vehicle_event_audit.py): **9/9 PASS**. The first run failed three tests because expectations used JSON string keys while `analyse()` returns in-memory integer-valued dictionary keys; fixed tests only, with a separate Git commit, then reran. Production code, physical engine and results were not altered.

## Results: 6 vs10s stages (10−6), 64 paired synthetic worlds

| Measure | Paired effect distribution |
|---|---|
| Existing `score` at terminal penalty 60 | equal in **64/64** |
| `receiver_denied_attempts` | +4 in **64/64** |
| **Distinct rejected vehicle IDs** | +1 in **34/64**, unchanged **30/64** |
| Extra *repeat* attempts beyond first per ID | +3 in 34/64; +4 in 30/64 |
| Contiguous refusal episodes (one ID, sequential t) | unchanged 30/64; +1 in18/64; +2 in16/64 |
| Number of rejected vehicles subsequently crossing | +1 in34/64; unchanged30/64 |
| Sum of observed first denial-to-crossing interval | +27 seconds in34/64; unchanged30/64 |
| Censored rejected-vehicle count at t240 | unchanged64/64 |
| Total stopline crossings | unchanged64/64 |
| Total L crossings | unchanged64/64 |
| End remaining vehicles | unchanged64/64 |

**Mechanistic moderator (posthoc):** 32/32 offset0 worlds show +1 distinct rejected vehicle, whereas only 2/32 offset15 worlds show +1. Offset differs in predecision state, so this is not a same-checkpoint causal effect of shifting the downstream signal.

**Important:** identical model `score`, stopline crossing counts and remaining vehicles do *not* imply the same vehicles encounter refusal. Adding four service attempts did not translate to four additional blocked vehicles. Counts of refusal episodes also respond to the treatment's service opportunity. The +27s is a **sum** over observed first-denial-to-crossing intervals, not a treatment effect on a fixed set of vehicle waiting times. Per-vehicle transport/welfare comparisons require explicit joint ID-level cohort definitions to avoid changing-composition bias.

## Instrumentation limits and required P31 changes
- The public `service_events` log does not contain per-ID downstream network discharge timestamps; receiver `tick` results are counted in network_out, but not emitted as `service_events`. Therefore cannot claim unique-vehicle full corridor travel times from current trace.
- Some common-exit conflict denials are counted without vehicle-ID events. These are **not** secretly classed as receiver denials.
- `t240` censored waits are not assigned zero or a fabricated crossing time.
- **Proposed P31:** fixed-ID cross-policy trace agreement/discordance and a new *arrival-process family* with independent tapes beyond the four reused random-clock variants. Avoid selecting a longer green simply to produce more wins. New experiments must be appropriately gated as exploratory when based on P30, retain SHA and immutable checkpoints.
- No SUMO or field traffic-calibrated comparison and no real traffic signal legality; K047 sealed, CIM archive HOLD, no GitHub Actions/bot.
