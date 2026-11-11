# T2 D46-C — 2026-11-11 synchronous finite-storage and time-grid gate

## Actual executed experiment
Two-link fluid/vehicle-count model (synthetic; no actual DLR input used for its arrival schedule). At each step:
- Beginning-of-step upstream stock `U` and downstream stock `N`.
- Transfer `T = min(U, C, K-N)`.
- Downstream exit `O = min(N, E)`.
- Next upstream `U' = U + A - T`; next downstream `N' = N + T - O`.
- Invariant `A_cumulative - O_cumulative = U + N`.
- Arrivals and the room freed by departures **do not** become immediately available for transfer in the same tick. This is a conservative numerical event-order convention, **not a verified continuous-time flow law**.

Experiment: 40 physical time units, 3 veh/unit arrivals during first 25, transfer cap 4 veh/unit, downstream storage K=6 veh; downstream exit profile either a constant 4 veh/unit, or 0 for [0,10), 1 for [10,30), 4 for [30,40).

At h=1 the unobstructed exit yields 75 vehicles exited and 0 remaining; the blocked exit yields 50 exited and 25 remaining, maximum upstream inventory 55 and 32 blocked steps. These comparisons hold the arrival schedule and upstream potential capacity equal. They **do not** measure a real queue tail distance or make a field policy claim.

## Discretization counterexample
Holding identical *physical rates* and 40 time-unit horizon fixed:
|Step h|arrivals|exits|remaining|max upstream|first blocked time|
|---:|---:|---:|---:|---:|---:|
|1|75|50|25|55|3|
|0.5|75|60|15|54.5|2.5|
|0.25|75|60|15|54.25|2.25|
|0.125|75|60|15|54.125|2.125|
|0.0625|75|60|15|54.0625|2.0625|

The **10-vehicle discrepancy** at h=1 demonstrates numerical time-grid sensitivity. A plateau at 60 for these finer steps is *not* sufficient to prove continuous-time convergence or simulator validity. The defined 40-unit sink capacity for the congested profile integrates to 60 vehicles in the continuous-time rate schedule; its realization depends on queue availability and event processing.

## Tests, source provenance and artifacts
- Re-executed the V4 ZIP's original 32 D46 tests plus 19 D46-C tests: **51/51 PASS**.
- The original 32 include synthetic node feasibility, demand/supply constraints, and the field-volume parsing contract (the test fixture is synthetic); the 19 cover dynamic conservation, timing, invalid input, and time-grid sensitivity.
- GitHub executable modules: `d46c/corridor.py`, `d46c/experiment.py`, `d46c/dt_sensitivity.py`, `d46c/test_corridor.py`, `d46c/test_dt_sensitivity.py`; the full locally run code/test provenance and outputs are sealed in V4 ZIP.
- V4 Drive ZIP: https://drive.google.com/file/d/163YfvCqtN4O26ZzWIjlSWx8lOAOwT5K7/view
- V4 SHA-256: `f288cec1f7139346447ad5a67833162dec5996d0264990d3ab0d5e25670163b0`.
- 11/11 Google Docs reasoning record: https://docs.google.com/document/d/1ZZPfPZXyHazuLiSqOowHQfSRecseZtzSY1gn1EEOhqc/edit

## HOLD
The model has **unlimited upstream storage** and a lumped downstream vehicle buffer. It has no lane-specific spatial queue tail, traffic wave propagation speed, signal conflict matrix, realistic micro-braking, DLR identified arrival demand or observed downstream receiving capacity. Consequently, no DLR spillback reproduction, actual SUMO independent run, or policy-rank claim follows.

Next experiments: (1) add upstream finite storage and cumulative unadmitted arrivals; (2) compare against event-time and finer-grid reference without same-tick causality errors; (3) finish D42 field lane/entry/exit geometry and D44 physical stopping viability, then independent SUMO.
