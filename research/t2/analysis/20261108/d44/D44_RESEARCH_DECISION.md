# D44 — 2026-11-08: physical braking counterexample and evidence scope

## Source inspected
Original D27 micro reference on research/t2-spatial-fig2-v02:
`research/t2/analysis/20261106/p11ab_d26_d30/d27/src/micro_world.py`.
The simulator uses dt=1 s only. Vehicle has `decel_mps2` but the velocity update uses acceleration and then clips speed to free room to leader/end of road. It does not enforce the declared deceleration limit.

## Minimal witness
One 12-m road, one 4.5-m car with acceleration 1.5 m/s^2 and configured maximum deceleration 0.25 m/s^2. Red after initial 1-s green in a 10-s cycle. The extracted update rule yields velocities after successive ticks: 1.5, 3.0, 3.0, 0.0 m/s. Final one-tick deceleration magnitude is 3.0 m/s^2, 12 times the configured 0.25 m/s^2.

At speed 3 m/s and 3 m remaining before the road boundary, constant deceleration needed to stop is at least v^2/(2d)=1.5 m/s^2. This is six times the configured bound, even without reaction time. A physically feasible stop is unavailable given those state assumptions; this is NOT repaired by simply clipping speed to the maximum allowed deceleration because that could induce stopline overshoot or a collision.

## Implemented and verified in this session
- `stopping_feasibility.py` includes a deterministic kinematics oracle; 8 unit tests ran locally (8/8 PASS) in a copy using equivalent formulas.
- `test_braking_bound.py` exercises the actual D27 engine and marks the known inconsistency as `unittest.expectedFailure`. This particular imported-engine test was committed but NOT run in this session.
- Standalone test ZIP SHA256: c91338603a575e661d4aa03fc2f1e8c2edc0ac7adf8d8a36c1fa0808f7ba80d4. Uploaded to the 20261108 shared Drive release folder: https://drive.google.com/file/d/19mKTZqHqfkvo1RjQ8YtoS0FE8bqKSUVQ/view

## Next acceptance tests
1. Execute imported original-engine known-failure test in a clone and record whether it is indeed expectedFailure or unexpectedSuccess.
2. Preserve exact original D27 source and prove per-tick motion/stopline invariants before modifying code.
3. Investigate stopping feasibility *before* entering infeasible states, including signal prediction horizon, comfortable/emergency deceleration, and leader vehicle occupancy.
4. Execute timestep refinements on the actual main engine, not the separate one-car oracle.
5. Match measured stopline/traffic-light phase timeline from a single DLR intersection observation and compare to independently run SUMO.

## Evidence labels
Source code inspected: YES (GitHub connector).
Isolated numerical update rule executed: YES.
Standalone oracle tests: 8/8 local PASS.
Original D27 module imported and executed in this session: NO.
DLR raw ZIP acquired and independently hashed: NO.
SUMO independent run: NO.
Field validation / live signal deployment: NO.

This is an offline model audit only.
