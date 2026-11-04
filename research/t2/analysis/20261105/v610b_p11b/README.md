# T2 v6.10-B / P11-B — Multi-hop traffic and causal audit (2026-11-05)

## Evidence and scope

Independent derivative research code. Historical T2 v6.9-P2 and v6.10-A/P11-A ZIP files are unmodified.

- `src/multihop.py`: multi-intersection route-based vehicle progression; downstream link capacity reserved at connector admission; link travel event at connector exit plus travel time; upstream link storage remains allocated until a legal downstream admission. Event queue with monotonically increasing timestamps, per-movement connector exclusion and conflict constraints from the network contract.
- `src/multihop_demo.py`: 2-junction linked corridor (J0 cycle 6 seconds, J1 cycle 8 seconds), each route is either J0→J1 or a side arrival at J1. J1 offset 0..7s. Link travel times {1,3,5}s; capacities {6.5,13}m; 2 demand patterns. Total **96 synthetic runs**; all 20 source vehicles complete per run in the 150-second horizon.
- `tests/test_multihop.py`: 12 new tests. Historical v6.10-A 25 tests also pass: **37/37**. Standalone v6.9-P2 regression tests **28/28** pass in an untouched extracted copy. No changes applied to previous source.
- `results/multihop_offset_experiment.csv`: 96 rows; `results/multihop_summary.json`: best candidate for each of 12 cells.

## Example evidence

Balanced demand, link travel=5s: downstream link storage 6.5m -> best J1 offset 2s (749 vehicle-seconds system time). Storage 13m -> best offset 6s (537 vehicle-seconds). The matched traffic input is held constant; the storage sizes alter queue spillback and policy choice. The link's storage is a simple footprint capacity, not geometric queue modeling.

Main-peak demand, link travel=3s: storage 6.5m -> best offset 4s (495.4 veh-s); storage 13m -> best offset 4s (492.4 veh-s). There is NOT always a different preferred offset.

The new objective is sum over all vehicles of completion time minus source arrival time, including time on links and queueing. The legacy v6.10-A optimizer used arrival-to-first-admission waiting and v6.9-P2 used different vehicle-exposure measures; do not directly compare those scores.

## Limitations / issues to investigate

- Only an illustrative route sequence, deterministic length-based storage footprint, equal-speed travel-time proxies, one connector occupant per movement. No real acceleration, stopping-distance, car-following, gap acceptance, per-lane queue geometry, pedestrians or buses.
- Source arrivals are held in virtual upstream queues; first-entry/source-lane storage is not modeled. This is not full-network gridlock physics. Link occupancy is a reservation at connector entrance, a conservative capacity approximation (not exact geometric occupancy). No spillback-wave propagation or traffic shockwave model.
- Signal clearance semantics use movements' declared clearance_s and phase duration, not actual yellow/all-red transition behavior.
- Offsets are 8 enumerated choices with tiny synthetic cycles; exhaustive best is only within those candidates.
- Absolute numerical objective cannot be compared with old T2 engines without matching state/output contracts.
- No SUMO execution and no observed traffic-series calibration. Therefore no on-road signal proposal or prediction accuracy claim.

## Reproduce

```sh
python -m unittest discover -s tests -q
python src/multihop_demo.py
```

For previous P2 regression independently extract original `T2_v69_P2_signal_optimization_robustness_20261104.zip` and run the four original test modules. No retroactive modification.

## Next

1. Build a small SUMO network matching two intersections and route paths exactly, and independently compare vehicle completion/time/queue.
2. Add source-lane capacity/backpressure and realistic lane-level occupancy/wave travel, including arrivals blocked at the boundary.
3. Add explicit yellow/all-red and protected/permissive movement rules.
4. Integrate optimization algorithms in a common policy-space with fair computational budgets, external validation and observational holdout.
