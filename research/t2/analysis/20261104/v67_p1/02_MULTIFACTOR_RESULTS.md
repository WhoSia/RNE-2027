# T2 v6.7-P1 — 48-run matched factorial, 20261104

2 truck shares (0%,40%) × downstream capacity (25m,140m) × exclusive-P duration (0s,8s) × 6 common seeds (40..45). Constant main/side traffic intensities 12+12 vehicles/min, arrivals until 160s, horizon 360s, simulation step 0.25s. 48 finite synthetic executions, **0 all-complete executions**. Means are finite-horizon vehicle-second exposures, NOT final travel times.

| Truck | Downstream | Walk | Mean completed | Mean vehicle-seconds |
|---|---|---|---|---|
| 0% | 25m | 0s | 38.667 | 11851.417 |
| 0% | 140m | 0s | 38.667 | 11851.417 |
| 0% | 25m | 8s | 33.667 | 12844.875 |
| 0% | 140m | 8s | 33.667 | 12844.875 |
| 40% | 25m | 0s | 24.667 | 14169.375 |
| 40% | 140m | 0s | 34.167 | 12746.125 |
| 40% | 25m | 8s | 21.167 | 14899.875 |
| 40% | 140m | 8s | 28.333 | 13747.250 |

Non-additive interaction: increasing capacity from 25m to 140m changed completed count 0 in all-car cases, but +9.500 for 40% truck/no exclusive-P and +7.167 for 40% truck/8s exclusive-P. These are **synthetic model effects only**. Drivers, signals, road geometry, crosswalk and headways were not calibrated to a real site. Six matched seed clusters, not 48 independent population samples. Total monitored braking, gap, membership, sampled-pose collision, exclusive-P connector warnings across this experiment = 0; this does not guarantee safe physical operation.

Full source/tests/CSV/manifest stored in shared Drive dated ZIP: https://drive.google.com/file/d/1tHw8BxV1BKnZOElQlKT5JEo1mab7wQru/view
