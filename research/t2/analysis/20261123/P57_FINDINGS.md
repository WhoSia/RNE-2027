# P57 — Evaluation horizon and individual through vehicles

All four cutoffs (90, 120, 150, 180 s) retain the same 16 scheduled through vehicles. A crossing not observed by cutoff contributes time through the cutoff; the experiment truncates existing trajectories, without extending or rerunning the physical horizon at each cutoff.

| Downstream offset | SUMO lead − lag at 90/120/150/180 s | T2 lead − lag at the same cutoffs |
| --- | --- | --- |
| 0 s | +46.5 / +46.875 / +20.875 / −11.125 | +113 / +204 / +330 / +330 |
| 50 s | +28.25 / +27 / +36.5 / +66.5 | −17 / −172 / −248 / −248 |

Units are vehicle-seconds. At 0 s, the disagreement appears only at the last tested cutoff (1/4). At 50 s it survives all four (4/4); the first three early scheduled vehicles in the largest-gap group are v02/v03/v05. At 180 s the four largest absolute individual gaps have signed sums 255.5 of 341.125 at offset 0, and −249.375 of −314.5 at offset 50. These describe concentration, with opposing contributions permitted.

Selection: start the vehicle-path audit at offset 50, examining insertion, first eligible discharge, and downstream storage for v02/v03/v05. Priority .926 (relevance .98, discrimination .97, readiness .88, feasibility .77). Keep offset 0 as a window-sensitivity control and field annotation at .872. All rows share a single arrival tape and different upstream geometries. No external accuracy claim.

Run: `PYTHONPATH=../..:../../efficiency_loop python p57_offset_horizon.py`.
