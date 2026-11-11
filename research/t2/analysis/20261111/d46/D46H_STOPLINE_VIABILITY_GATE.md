# D46-H — Physical stopline feasibility oracle (2026-11-11)

## Decision
**LOCAL KINEMATIC CONTRACT PASS (25/25); ORIGINAL D27 DECELERATION DEFECT REPRODUCED (24/30); MULTIVEHICLE / FIELD / SUMO HOLD.**

## What was actually implemented
Independent `viability_motion.py`, NOT an in-place fix of the historical D27 `src/micro_world.py`. It holds a single vehicle's time `t_s`, **front coordinate** `front_m` (not the D27 rear), and speed `speed_mps`. Its parameters are finite stopline position, speed limit, maximum acceleration and maximum braking. It handles deterministic red/green commands with exact constant-acceleration integration, speed-cap and stop-time splitting, and **signal transition splits**.

At red with remaining front-to-line distance `d` and initial speed `v`, stop feasibility under constant max braking `b`, zero reaction time and flat road is `d >= v²/(2b)`. If feasible it brakes with `a=-v²/(2d)` so that the vehicle can stop at the line without exceeding `b`; if infeasible it applies `a=-b`, returns `feasible_red_stop_initial=False`, and records actual red crossing if one occurs. **It does not teleport speed to zero to fake signal obedience**. Crossing time is computed inside the integration interval rather than retroactively to its start.

## Executed evidence
- New local unit suite **25/25 PASS**: acceleration/braking limits, red stopping, genuine unavoidable red cross, signal switch, speed limit, event timestamp, positive timestep input errors and refinement checks for constant-signal intervals.
- Unmodified D27 extracted from `T2_D26_D30_20261106_RELEASE.zip` under byte SHA256 `83c3f3fc5fe8bf6b8418fe7a48ebc6e3f3c09fbe725d94802d7b5120ca58fdde`. Old engine grid, road length (8,10,12,14,16,20)m × max brake (.25,.5,1,2,3)m/s²: **24 of 30** declared braking ceiling violated; original collision violation count always 0.
- Standalone local oracle on 30 explicitly initialized initial conditions (speed 3m/s, initial front-to-stopline distance road_length−4.5m): **0/30 brake ceiling violations**, **10/30 mathematically infeasible red stops** under stated assumptions. **These initial states are not identical to D27's full trajectories.** This is *not* a paired estimate of improvement and cannot justify a policy result.
- Source, original sealed copy, Python tests, CSV, summary JSON, test log, research note and SHA manifest preserved in Drive ZIP: https://drive.google.com/file/d/1QhoMkj0TOy7CbE0Xtg0DZMMkJfCs6Sl3/view.
- ZIP SHA256: `a45178f1507d2eba25a098b311e432e7b2d59f8d724b8375dd2b56292f0b5ae8`.
- Daily Google Doc: https://docs.google.com/document/d/1ZZPfPZXyHazuLiSqOowHQfSRecseZtzSY1gn1EEOhqc/edit

## Precise scientific limitations
This is **single vehicle only**. It does not model car-following, collision checking, lane geometry, vehicle length variation, reaction time, physical friction, full network node priority, sensor errors or the real DLR movement-signal mapping. The D46-G scalar length-reservation simulator is not yet integrated. The old D27 physical defect remains in its original engine, though it is reproduced and tested independently.

**Next acceptance:** build D46-I discrete longitudinal positions + bounded braking with the same vehicle queue and finite link storage; enforce headway and safe-stopline event order before any throughput/policy comparisons. Independently pin SUMO and compare after real DLR stopline/turn map recovery. Do not call the current code a real-world traffic safety controller or validated traffic-policy optimizer.