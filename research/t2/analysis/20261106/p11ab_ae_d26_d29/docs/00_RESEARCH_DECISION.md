# R&E 2027 — T2 P11-AB/AC/AD/AE · D26–D29
**2026-11-06 | Research Decision · source-to-evidence gate**

## One-paragraph decision
We have **built and run a new research-only, finite-link microscopic reference** that connects several previously isolated mechanisms, and **replayed the byte-verified original P10** from its historical P9/P10 source archives. This is **NOT** a full production simulator, an independent SUMO validation, an inD/NGSIM field fit, or a demonstrated signal-policy improvement. The new reference is intentionally small and modular; its large finite-dt sensitivity is an adverse result, not a convergence certificate.

## Four substantive research units

1. **D26 — Event chronology and micro-motion foundation.** Start-of-tick receiving-space decisions, per-vehicle position/speed/acceleration input, vehicle length, longitudinal gap, fixed-time signals, stopline control, original P10 replay with SHA source attestation. Original P2 baseline 28/28 and original P10 8/8 tests passed. Eight original grid outcomes agree byte-for-byte at the model-data level with preserved `boundary_mechanism.json`.
2. **D27 — Spatial network and conflict graph.** Directed link connections, deterministic merge arbitration, optional experimental lateral lane changes, finite queue storage, pedestrian crossing occupancy, bus stop dwell, route validation, geometric grade/radius speed caps. These are **simplified functional primitives**, not complete IDM/MOBIL, interaction-safe crossing geometry, 2D road design, or OpenDRIVE integration.
3. **D28 — Demand and observed-data interface.** Reproducible Poisson OD input, fixed network route selection, raw input SHA manifest, date-disjoint holdout, standardized unit-specific MAE/RMSE metrics and strict observation time monotonicity. Actual GTFS/inD/NGSIM/Jinju matched observation cohorts were **NOT** acquired in this run. H3 is neither essential to nor executed by this model.
4. **D29 — Coupled counterfactual, numerical negative result, independent-engine adapter.** Same 22 synthetic vehicles through two finite links; downstream closure at 0/15/25 seconds with fixed signals, readouts for external queue, completion, receiving blockage. Time-grid refinement .5/.25/.125/1.0 seconds was run. Exported netconvert/SUMO **input XML**; independent SUMO binary missing, and no SUMO results were generated.

## Result values — controlled synthetic, NOT field findings

| Closure on U before | Generated/completed | Max outside queue | Last completed | Receiving/closure evidence |
|---:|---:|---:|---:|---|
| 0s | 22/22 | 15 vehicles | 72.0s | receiving-space denials present |
| 15s | 22/22 | 18 vehicles | 82.0s | 20 closure-blocked ticks |
| 25s | 22/22 | 18 vehicles | 92.0s | 40 closure-blocked ticks |

At fixed 20s U closure, last completed at 109.0, 87.0, 81.5, 78.625 seconds respectively for `dt=1,0.5,0.25,0.125s`. This **does not establish convergence**; large differences are a high-priority HOLD against policy scores.

## Verification contract and explicit remaining failures
- P10 source archive SHA256 `9fa06146b781bcbbd1f5e19dc25b277e1e98c695b13e61fc0b291b58cd53b59c` verified, byte-identical P2 `corridor.py` SHA256 `12987786fb36409a272a50233c12c006d0a23d5f75a5487be68d51392c4614cc`. Historical 8-grid trace matches archived results, 8/8 original tests passed. This is a **verified historical replay**, not a claim that original defect was generally repaired.
- New reference uses synchronous finite time steps. Lateral lane changes check the instantaneous 1D gap, not the complete maneuver; longitudinal follower updates are simplified; grade and curvature speed bounds are heuristic, not calibrated. Vehicle stops can violate intended deceleration limits because a stop-line clamp is algebraic; test that failure explicitly in future. No safe operation claim.
- The experimental receiving link uses start-of-tick occupancy, preventing the selected backward-capacity decision, but discrete stopline transfers introduce additional delay and distinct artificial artifacts. Hence **finite-dt time convergence is unproven**.
- No external SIMSUMO binary (`sumo`, `netconvert`) is available here; only source input XML validated. No real trajectories, actual signals, calibrated pedestrian observations, or cross-city field validation. Date-disjoint scoring functions exist but have not scored a measured cohort.

## Research output separation
- **Science exhibition:** observed finite turn-pocket storage, crossing occupancy and queue spillback vs independently measured video/trajectory and SUMO. Synthetic diagrams are prototype explanation only.
- **Journal:** event-time semantics, order-preservation, finite storage, causal counterexample and time-step numerical pathology, with explicit prior-art comparisons. Do not claim novel FIFO or known CTM principles.
- **Policy axis:** user has **authorized resumption from the NEXT research step**. We may run offline, fixed-conditions and matched-input **exploratory** signal-policy baselines next, but must not promote rankings, use real-world controllers, or make field recommendations until causal/simulation/data holdout gates pass. Keep old P12 frozen as a historical artifact, implement new research in separately versioned sandbox.

## Priority D30
1. Bound/decompose micro-model numerical error in positions, exits, stopline service and acceleration; test `dt` convergence on multiple traffic cohorts.
2. Actually execute SUMO matched network and confirm artifact schema/vehicle transfers.
3. Acquire actual official GTFS original bytes and NGSIM/inD/Jinju matched observation units, license, source SHA, separate date/site holdouts.
4. Integrate 2D road geometry and signal legal movement conflict graph; align realistic bus/pedestrian behavior.
5. Then add *sandbox-only* signal-policy evaluation with causal error bands and cross-demand robust tests.
