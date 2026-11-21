# T2 P19 — Finite receiver, downstream signal offset and changing left-stage opportunity

Date 2026-11-22 KST. **Prospectively fixed experiment** in the exact five-blob T2 physical engine, following [P19 preregistration](P19_RECEIVER_SERVICE_OPPORTUNITY_PREREG_20261122.md).

## Verdict: ACCEPT conditional synthetic moderation; HOLD physical causal mechanism identification

The model does not support the claim that a longer/intervening protected-left stage universally improves simulated delay. Downstream offset and finite storage substantially change the distribution of intervention costs. **However, comparing different downstream settings or receiver capacities compares different predecision states**, so this is a cross-world moderation screen, not a same-checkpoint counterfactual in which an operator changes downstream offset at t84.

## Design and exact evidence

- Fresh seed labels 112–119 and two regimes (1650 vph, left .50; 1800 vph, left .45).
- One fixed-count randomly timestamped arrival tape per regime/seed, route labels taken unchanged from original canonical `spatial_v10.arrivals`, with `Random(seed+1_000_003)`; **16 unique entire tape SHA256 fingerprints**.
- Receiver storage 2/4 cells, downstream timing offset 0/15 seconds, pocket length 14/28m, B preassignment 0/.5. Total **256** model worlds; 128 geometry-matched comparisons across offset0 vs offset15.
- Within every world, `baseline` and the **8s abstract left-stage intervention** at ticks87–95 follow from a byte-equal tick84 checkpoint and the same future request tape. The simulator's own phase validator enforces its 3-second **no-service** transition, which is not a yellow/red/pedestrian program. The invented green≥6 criterion rules out the earlier 4s action but *does not authorize 8s in real life*.
- Source and test files in GitHub `main`: [runner](p19_receiver_service_opportunity.py) with Git blob `760fd8ce81f1e56d02b1707e5e2fef8d4720f4d1`, [nine tests](test_p19_receiver_service_opportunity.py) blob `350fc2b4def767bbd88e78397e5883f50e489b38`. Both were read back from the connected GitHub repository and matched local `git hash-object` checks. Executed Python 3.13.5 tests **9/9 passed**.
- Full new 256-world result JSON SHA256 `0681f683acd549cb2d32cc8957038ce3e652819f47e8288c5a751b6acd7e2468`, from **two byte-identical independent invocations**. The full JSON and exact runnable sources are preserved in a standalone conversation download, not claimed to be shared Drive bytes. [Summary JSON in main](P19_RECEIVER_SERVICE_SUMMARY_20261122.json).

## Model cost distribution (within each 64-world geometry stratum)

Cost = `outside_vehicle_seconds + upstream_vehicle_seconds + receiver_vehicle_seconds + 60×remaining` (artificial uncalibrated model units); negative delta means 8s intervention lower cost.

| Receiver cells | Downstream offset | Δ negative | Δ positive | Δ zero | Sum Δ | Extra early left crossings | Extra blocked receiver attempts t120–129 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0 | 17 | 47 | 0 | +1,656 | +192 | 0 |
| 2 | 15 | 16 | 0 | 48 | −3,926 | +21 | 0 |
| 4 | 0 | 16 | 14 | 34 | +3,452 | +256 | +124 |
| 4 | 15 | 19 | 0 | 45 | −8,174 | +42 | 0 |

Note: event counts are **sums over repeated model geometries**. They are NOT independent episodes in the statistical sense. For each stratum, exactly 16 full request tapes underlie 64 worlds.

### Mechanistic evidence and its limits

The count of additional successful early left-turn stopline crossings under the 8s intervention differs sharply by receiver offset. With capacity4/offset0, the intervention generated 256 more early L crossings (aggregated across 64 scenarios) but also **124 additional later receiver-entry denials** at t120–129. For offset15, early crossing gains were much smaller (+21 at cap2, +42 at cap4) and no excess later denial appeared. This joint observation is a *plausible model mechanism* linking early service to later receiving bottlenecks, but not proof that the denials alone mediate the cost difference: lane assignment, initial queues, future arrivals and simulator rules also matter.

For all **128** receiver- and geometry-matched offset0-versus-offset15 pairs, there were **zero strict negative-versus-positive effect-sign reversals at epsilon5**. Cases where offset0 was harmful often became a tie rather than a strongly beneficial treatment at offset15. The prevalence of positive vs nonpositive deltas is not a statistical significance test and cannot be generalized to real roads.

## Falsification and negative results

- New seeds and timing do not guarantee 256 independent traffic trajectories: only **16 distinct tapes** were used.
- No demonstrably site-legal signal program was generated; the `'-'` phase is a synthetic no-service phase, not an actual yellow/red clearance.
- The intervention's timing changes model receiver occupancy and queue cost, but there is no identification of an isolated receiver-mediated causal component.
- No RF-CURTAIN radio measurements exist and no traffic state-to-RF causal label mapping has been validated.
- No full traffic-controller integration, actual pedestrian phases, regulatory minimum greens, or field/observational calibration was performed.
- K047 remains sealed; held `CIM dataset.zip` never opened; GitHub Actions and bot contributors not used.

## Next model-science decision

**P20 should target physical model validity rather than generating more synthetic seed-based effects.** Two decisive alternatives:

1. **Receiver event conservation:** independently reconstruct every stopline crossing, receiver admission, link occupancy and downstream network exit from event traces and require tick-level conservation and causal ordering, including cases with blocked entry. The same engine's internal counters alone are insufficient as an independent oracle; this may reveal a modeling defect and must not be tuned to fit an expected sign.
2. **External reference and calibration:** compare delay and discharge headway against an independent SUMO or established car-following/finite-storage model, with held-out geometry and traffic regimes. Report model discrepancy even when it contradicts our own preference reversal claims.

Continue the separate RF exhibit track with a controlled, authorized physical sensor versus cheap optical/magnetic baseline; never treat simulated occupancy labels as measured CSI.
