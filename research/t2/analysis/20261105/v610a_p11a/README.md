# T2 v6.10-A / P11-A — two-track development, 2026-11-05

This is an **independent prototype**, not a promoted replacement for sealed v6.9-P2/P10 or an approved real-world signal controller.

## Track A — function expansion

- `src/network.py` — typed lane, turning movement, reciprocal conflict, general per-junction variable-length phase programs, offsets, independent cycles.
- `src/policy_search.py` — safe fixed-cycle green splits + offset enumeration on a user-defined small movement network.
- `src/demo.py` — three synthetic demand cases, 18 signal plans each; 54 policy runs. Baseline toy includes one junction, two movements, single downstream storage; no explicit lane changing, passenger interactions, multihop OD, microscopic car following, sensor API or pedestrian agent.

## Track B — numerical/causal validation

- `src/events.py` — event-queue with float seconds, monotone timestamps, explicitly ordered release/arrival/admission events, finite receiving capacity and green clearance. This avoids P9/P10's class of *tick-end storage release backdated to tick-start* **in this new toy**. It does not repair the sealed P2 model.
- `tests/` — contract, conflict, clearance, capacity and output validation. Manual isolated baseline regression: 28 historical P2 tests passed; new 25 tests passed.
- `provenance/original_p2_sha256.txt` — original archive checksum; extracted original source under `provenance` is an unchanged copy for replay only; code in `src` does not modify or import it. Do not put historical zip copies into the daily data lake's `40_DERIVED` as new raw data: existing original is already elsewhere in Drive.

## Example outputs (synthetic, not field estimates)

| demand | candidates | chosen main green | offset | total queue waiting | completion |
|---|---:|---:|---:|---:|---:|
| main peak | 18 | 7s | 1s | 67.1 vehicle-s | 21/21 |
| side peak | 18 | 3s | 2s | 69.9 vehicle-s | 21/21 |
| balanced | 18 | 4s | 0s | 78.6 vehicle-s | 20/20 |

The objective is **arrival-to-admission queue waiting**, unlike earlier P2 total generated-minus-completed vehicle exposure. Those figures **must not** be directly compared across engines or called realistic delays. No real-world data, SUMO trips or physical stopline collision validation has been performed.

## Replay

`cd src && python demo.py`

`python -m unittest discover -s tests -v` (from this directory)

`cd provenance/T2_v69_P2 && python -m unittest -q test_corridor.py test_optimizer.py test_coordinate.py test_robust.py`

## Known limitations and next development

1. Add explicit route topology and movement-to-movement flow across successive intersections, not merely two independently callable junctions.
2. Add time-stamped link traversal and state transitions, separate queue/receiving-link occupancy, conflict-region exclusion across the entire physical clearance interval, time-stepped and event-driven paired tests.
3. Add signal phase constraints for actual pedestrian clearance, yellow/all-red and protected/permissive turns; no generic safety warranty now.
4. Add event-causal parameter uncertainty/selection margin and alternative optimizers (coordinate descent, constrained search, pressure/MPC baselines).
5. Build equivalent SUMO two-intersection network and import real Jinju traffic bytes, audit source semantics, train/holdout.

## Research gate

Do not announce full feature coverage or external validity based on 25 unit tests and 54 synthetic scores. They support only the contracts specified above.
