# T2 P19 — Finite-receiver service-opportunity transport and action-feasibility falsification

Date 2026-11-22 KST. **Next prospective protocol; NO P19 numerical results generated at registration time.** This is the successor to P18's 144/144 canonical source replay and 256-world clock study.

## Physical research ambition
Test the mechanistic claim that adding a brief protected-turn service window may advance a subset of vehicles across an intersection but also change downstream receiving-link occupancy and subsequent opportunities. A naive 'more green implies better throughput' argument fails in 10 posthoc P18 cases, but a single illustrative event trace does not identify a causal mediator. P19 must distinguish three effects:
1. Actual turn-lane stopline crossings during the extra ticks.
2. Downstream receiving entry and blocked attempts in the next cycle.
3. Final vehicle-seconds, residual vehicles and S/L network exits.

## Freeze the experiment before execution
- Exact main source baseline: `dual_lane_v11.py` blob `a7c9aa6954402e12894d1d5b722e8a474b0bd58f`, `spatial_v10.py` blob `ffbf3fc3f8b9a64a819d4f73ce70b264b877e84e`, and `receiving_cells_v15.py` blob `b078cf215c74b76ace6dffcbcbacab6ae22c3673`. Refetch and verify at the session's pinned main HEAD before P19 execution.
- New never-used model-seed labels **112–119**; two demand regimes 1650vph/left50%, 1800vph/left45%.
- Receiver storage 2/4 cells, downstream signal offset 0/15 seconds, pocket 14/28m, B-lane assignment 0/.5, lane changes enabled, update mode fixed to canonical.
- **One** independent time-redistributed route-matched arrival tape per seed/regime using the **predeclared** timestamp RNG stream `Random(seed+1_000_003)` from P18. Do not tune clock seed or generated routes from outcomes. Repeat the same tape across geometries; identify independent blocks by the **actual tape SHA**. Total world grid: 2 regimes × 8 seeds × 2 receiver storages × 2 offsets × 2 pocket lengths × 2 B shares = **256 worlds**, but only 16 independent seed-regime arrival tapes.
- Baseline and the **8s synthetic left intervention** `((84,87,'-'),(87,95,'L'),(95,120,'-'))` must be resumed from *byte-equal* tick84 checkpoints and the same future tape. Hard fail on any checkpoint mutation, event mismatches, vehicle-count nonconservation or phase transition exception.
- The 8s intervention is merely **eligible under an invented min-green6** check; no claim about yellow/red/pedestrian or Korean site-specific approval. Do NOT add new 4s options to the primary analysis.

## Primary outputs
For each world: generated vehicles, actual unique tape SHA, same-tick baseline and intervention state fingerprint, terminal-penalty-60 integrated model cost difference, terminal remaining, S/L exits, and in the tick84–129 window:
- successful L/S stopline crossings,
- `receiver_entry_cell_busy` and `receiver_capacity_full` blocked attempts,
- lost service opportunities during active green,
- upstream/pocket entry denial events (when trace contract provides them).

Primary descriptive outcome: number of 8s treatment improvements/harm/ties and exact model-cost changes grouped by receiver capacity and offset, while respecting the 16 independent arrival-tape blocks. Secondary: frequency of greater *early* L discharge alongside worse *total* model cost. Do not report geometry-repeated outcomes as independent days or compute naive 256-sample confidence intervals.

## Causal hierarchy and falsifiers
**Within-world:** treatment-vs-baseline difference is a same-frozen-checkpoint simulated intervention effect under this specific engine and tape. **Across receiver storages/offsets:** these are *different baseline worlds and different predecision states*, so differences in the simulated effect are moderation/sensitivity, NOT 'changing receiver capacity after the decision' counterfactual effects. A source of congestion may not be identifiable from a single-count snapshot.

Valid null: zero sign differences by receiver offset, or extra turn crossings not accompanied by worsening cost. Do not retune horizon, epsilon, offsets or group filters to force a positive finding. Preserve full trace, exact core hashes, seed/block identifiers, bounded claims, and failures.

## Dedicated negative controls
- Verify entire checkpoint pickle stays byte-identical under each branch.
- Verify no future arrival time or route label enters a decision-time observation feature.
- Confirm that reversing the grouping error (dropping B-share or pool distinct downstream settings) artificially changes alias statistics; never promote such results.
- No P12 model-only gate is real legal approval. A passing `'-'` transition is not yellow, clearance or pedestrian timing.
- Preserve RF-CURTAIN as separate physical-sensing study; none of these source traces constitute real CSI, physical obstacle localization or field results.

## Delivery
Develop on GitHub `main` in `research/t2/analysis/20261122`. Record actual code/test/output hashes, two byte-identical runs or documented nondeterminism, full scenario manifest and every negative result. Log into the Nov22 Google Docs research note and invite 김세호 only as independent falsification/reproduction evaluator. GitHub Actions/bot prohibited, K047 sealed, 5GB CIM ZIP HOLD.
