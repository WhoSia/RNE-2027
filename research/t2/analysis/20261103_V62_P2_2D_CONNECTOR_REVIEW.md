# T2 v6.2-P2 — 2D connector states & stopline boundary review (20261103)

Status: **PROTOTYPE / PHYSICAL SAFETY CERTIFICATION ON HOLD**.

## Implemented and run
- New `geometry_v62.py` projects synthetic straight and quarter-circle connector progress onto an explicit 2D front-bumper pose `(x,y,heading)`.
- Vehicles are oriented 4.5 m × 1.8 m rectangles. The separated-axis test audits footprint overlap with the exclusive connector.
- Connector to downstream transfer preserves residual distance traveled past the clearance threshold, rather than resetting front x to exactly vehicle length.
- Main-heavy seed 203 in v6.1 had 288 warning ticks from delayed braking at the end of side green. A 1s green-end admission margin in the new candidate resolved this finite historical case.
- 38/38 regression and new tests passed. 36 historical matching pairs plus 144 extra stress runs; a separate 180-condition old-vs-new historical comparison (360 simulations), and 72 adversarial synthetic tests — 648 executions total (individual experiments are not independent field observations).
- Historical 180-condition review: v6.1 one invalid condition, v6.2 zero conditions with monitored violations. Extra 72-run stress: zero monitored braking, vehicle membership, queue, footprint-overlap, or connector pose jump events.
- **Efficiency tradeoff:** v6.2 +44.6403 vehicle-seconds per historical configuration on average, and 3150 versus 3193 completions aggregated across those 180 matched configurations. Admission guard and overshoot preservation were altered together; effects are not separately identified.

## Critical reviewer limits
- The 1 second guard is a heuristic, *not* mathematically guaranteed safe stopping for arbitrary acceleration, signal timing, or traffic.
- Connector admits one car only; collision-free simultaneous service has not been established.
- Swept-vehicle volumes between 0.25s snapshots not evaluated. 2D coordinates are a projection of scalar progress, not coupled continuous steering dynamics.
- Synthetic lanes, no pedestrian or real opposing movements; no SUMO independent test, no measured intersection calibration, no integration into original three-junction corridor.
- An earlier 900-run high-load stress design timed out; reduced to 72 prioritised adversarial conditions. No claims for the unfinished design.

**Reproducible entire source, raw CSV and SHA-256 manifest:** [Drive ZIP](https://drive.google.com/file/d/1Zv_LQPyg1FA-eX8AjKzDX46H0PP0G-r-/view), SHA256 `0843c767b18d14a1ed4cb62af13b478357e3f80f586a43cd086cc80cbc6ffae0`.

Next release gate: swept-rectangle collision and viability-set stopping, paired factorial ablations of overshoot vs phase margin, real three-junction integration and independent field/SUMO validation. Do not operate actual public signals from this prototype.
