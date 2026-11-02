# T2 v5.1 — Movement-aware signal service and held-out policy ranking, 2026-11-02

## Research claim (strictly limited)

The v5.0.1 IDM-on-3-junction prototype was extended with explicit **legal directed connections** and four movement types: main-through, main-exit, side-merge and side-exit. A stage-specific service headway is assigned to each movement type. For a total of 216 paired synthetic runs spanning 3 demand scenarios, 3 movement headway hypotheses, 4 seeds and 6 feasible green-split/offset policies, the balanced-demand average policy ranking switched from `(38, progression)` to `(38, zero)` under an **extreme synthetic** turn-headway assumption. **This reversal did NOT replicate** in a separately fixed, 48-seed stochastic replication: in that replication, progression had a lower mean vehicle-second exposure in both the equal-headway and stress-headway cases. Under stress headways, the 95% approximate confidence interval for the paired difference includes zero.

A more reproducible finding within this simulator is that the heavy-turning stress **attenuates the relative effect of offset progression**: 48 matched seeds give the difference of paired differences (stress-minus-equal) +155.07 vehicle-seconds, approximate 95% t interval [+26.60, +283.54]. This estimate applies only to this synthetic demand and candidate control pair. The hypothetical headways were not measured and the model lacks realistic conflict geometry, so it is neither field evidence nor a transferable control law.

## Model and software changes

- Directed successor connections: M0→M1→M2, S0→M1→M2, S1→M2, and S2 as a terminal side approach. Each prefix may end at an exit sink; there are no teleporting OD paths.
- Reject duplicate IDs, disconnected OD paths and birth times that are negative/non-finite or unaligned to the discrete timestep.
- All three signalized junctions are active and independently offset. The existing two-stage main/side green & all-red controller ensures cross-stage exclusion. A conservative movement-conflict table is recorded, **not a geometrically calibrated conflict matrix** or fully separate protected-turn phases.
- Movement-specific interdeparture headways `main_through_s`, `main_exit_s`, `side_merge_s`, `side_exit_s` parameterize discharge (seconds), not continuous turning trajectory. Each incoming link remains one FIFO lane, without turn bay or weaving.
- Crossing events are recorded per vehicle with t, junction, from/to link, movement type and assigned phase; conservation and within-link minimum gap are checked at each timestep.
- A newly discovered severe bug: if a proposed crossing is rejected when downstream receiving space is exhausted, simply moving the leading vehicle back to the nominal stopline can compress its follower beyond the 6.5 m (4.5 m vehicle + 2.0 m gap) minimum clearance. Specific observed stress failure: S1 link, `main_peak` seed 11, long-turn model, g38 progression, tick 951. Fix: transactional same-link reconciliation using positions **before** this tick, and never roll back any vehicle below its pre-tick position. Waiting counters for forcibly stopped vehicles are corrected. This is a discrete invariant repair, not a proof of collision freedom in the real world.

## Reproducibility and counts

- Existing 26 tests plus 11 new movement/rollback tests: **37/37 passed** locally. All 12 checked v5.0.1 demand×policy cases had identical vehicle-seconds and completed-trip counts under default 2-second movement headways.
- Main sensitivity study: **216** synthetic runs, 3 demand modes × 3 movement headway hypotheses × 4 matched seeds × 6 signal policies. Vehicle-time exposure identity holds (maximum absolute error zero).
- Independent seed replication: **192** runs, 48 different seeds (101–148), 2 movement models × 2 offsets at fixed g38, balanced demand. 96 matched paired comparisons; NOT independent field observations.

### Main discovery four-seed exploratory outcomes (mean vehicle-seconds)

| Demand | equal 2s best | moderate best | stress best |
|---|---|---|---|
| balanced | g38 + progression | g38 + progression | g38 + zero |
| main_peak | g38 + progression | g38 + progression | g38 + progression |
| side_peak | g32 + zero | g32 + zero | g32 + zero |

Balanced, g38, offset progression minus zero under four exploratory seeds: equal headway −200.625 ± SD 194.41 veh-s; moderate −89.125 ± SD 329.96; stress +120.625 ± SD 417.32. The sign inversion is exploratory and sample-sensitive.

### Confirmatory new seeds, n=48 each

| Turn model | Progression − zero, mean veh-s | Paired SD | Approximate 95% t interval | Progression wins |
|---|---:|---:|---|---:|
| Equal 2s | −305.865 | 326.382 | [−400.648, −211.081] | 39/48 |
| Stress | −150.792 | 535.720 | [−306.369, +4.785] | 26/48 |
| Interaction: stress Δ − equal Δ | +155.073 | 442.373 | [+26.605, +283.541] | 30/48 positive |

A two-sided 95% t interval is not a guarantee of predictive validity. Estimators are conditional on the simulator, OD generator, chosen policy set and assumed driver model.

## Source ground and simulation scope

Official SUMO docs describe lane-to-lane signal-controlled **connections**, not merely road lanes, and the distinction between permissive and protected conflict/yield behavior:
- https://eclipse.dev/sumo/docs/Simulation/Traffic_Lights.html
- https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html
- https://sumo.dlr.de/docs/Simulation/Intersections.html

Our synthetic connection taxonomy is aligned conceptually with that representation but **does not reproduce SUMO intersection traversal, geometry, lane-changing or pedestrian conflict rules**.

## Explicitly unfinished

The new movement model does not contain multiple lanes or physical turn pockets, pedestrians, buses, multi-turn collision geometry, yellow/amber clearance, separate protected turn phases, link-specific capacity calibrated from measurements, spatially explicit right-of-way crossing zones, independently verified SUMO simulation, actual traffic signal plans or field-derived Gyeongnam OD. Field observation and model calibration are the next gates, not accomplishments already achieved.

## Next decisive experiments

1. Add real geometry with lane-resolved turning connections; compare with SUMO's `linkIndex` and junction rights-of-way while preserving controlled stage conflict matrices.
2. Measure movement-specific saturation headways, turn proportions and queue length by signal cycle from supervised, non-identifying field observation; calculate realistic parameter intervals rather than arbitrary stress settings.
3. Measure whether those additional observations narrow policy regret, separating *fit of microscopic trajectories*, *accuracy of held-out queues* and *stability of recommended policies*.
4. Pre-register independent stochastic seeds and hold out real days for out-of-sample testing; never promote exploratory four-seed rank reversal to empirical discovery.
