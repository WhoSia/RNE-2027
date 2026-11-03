# v6.5 special-researcher review — 20261103

Decision: admit analytical censoring-bias correction, do NOT upgrade T2 to field-validated or operationally safe simulator. 10/10 new Python unit tests (source CSV consistency, paired identity, duplicated cohorts, bootstrap determinism) passed in local execution.

Exhibition branch:
1. Measure a real single intersection: stop-line coordinates, lane count/width/turn routing, actual phase transitions and lost time, per-movement arrival and discharge, observed queue/travel times, vehicle class and the actual observation window.
2. Assign distinct calibration vs held-out field dates, compare T2 to deliberately simpler queue baseline and SUMO with the *same* demand and signal plan.
3. Require physical continuity, complete-cohort accounting, negative controls for demand rephasing, and event failure logs before operational performance claims.

Research paper branch:
1. Explicit model set Theta(O) under matched observable aggregates and sensor quantization/noise.
2. Evaluate both model classification and regret of candidate signal policies on independently held-out scenarios; never equate classification accuracy with decision value.
3. Vary time-of-day demand, OD, heavy-vehicle fraction, pedestrian signals and measurement precision. Keep synthetic seeds clustered by input cohort in inference.

Still unresolved: real geometry, multi-lane changes, observed vehicle trajectories, phase legality, pedestrians/cycles, SUMO independent runs. No autonomous real traffic control permitted. Keep Drive as source-byte custody, GitHub for code/reviewer versioning, dated Research OS shared-drive log as semantic chronology.