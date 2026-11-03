# T2 v5.8 — Physical path-time proxy and geometry provenance audit
Date: 2026-11-03. SYNTHETIC RESEARCH ONLY. NOT A TRAFFIC SAFETY CERTIFICATE.

## Problem discovered
The historical v5.5–v5.7 polyline approximation for right turns went via the remote (±30m,±30m) boundary corner. All four right-turn paths N>W, W>S, S>E, E>N had zero line length within the square [-8m,8m]^2. These were not realistic junction turn paths and prevented a meaningful local path-distance occupancy estimate. v5.8 repairs the right-turn polyline via local waypoints near (±8m,±2m). Repaired local path length is ≈8.485m each. At a required centreline clearance of 2.5m, old and new models happen to retain all 42 incompatible movement pairs and 11 maximal stage combinations; this does not prove geometric validity for any other clearance or road geometry.

## Implementation
`path_occupancy.py` computes path centreline length clipped to [-a,a]^2 using Liang–Barsky segment clipping. Occupancy time proxy is `dt * ceil(((L_inside + 4.5m)/clip(v_entry, v_floor,v_cap) + buffer)/dt)` with dt=0.5s; defaults a=8m, floor=4m/s, cap=12m/s, buffer=0s. Speeds are sampled before movement at approach-front vehicle state; fixed `occupancy_s` remains available, but simultaneous fixed and path-time arguments are rejected. The interval gate inherited from v5.7 blocks conflicting movement admissions until the predicted time has elapsed. A pre-crossing reservation is canceled (not entered into occupancy log) if downstream supply rejects the crossing. Independent interval auditor checks zero cross-movement conflicts for accepted events.

This is NOT true integrated intersection motion: it assumes constant clipped entry speed across a polyline, adds the entire vehicle length, does not enforce curvature-dependent turn speed or vehicle width swept polygon, excludes pedestrian conflict, and still applies a whole-junction reservation instead of conflict-zone segments. The speed floor in particular can understate occupancy of slow vehicles. Real values require road survey/empirical trajectories and a separately calibrated SUMO internal-lane comparison.

## Actual executed tests and data
- 20 unittest checks PASS (10 previous v5.7 + 10 new v5.8).
- New regression confirms old-vs-new right-turn path defect, invariant 2.5m clearance graph, zero-duration exact historical outputs for three traffic cohorts, path-speed physical quantities, and vehicle accounting.
- 288 synthetic simulations: exploration 3 demand cohorts × 16 seeds × 4 occupancy modes = 192; independent 3 × 8 seeds × 4 modes = 96. All matched OD inputs within each seed; no real field measurement or SUMO executable.
- Holdout mean difference in cumulative vehicle-seconds versus no temporal occupancy: balanced fixed3 +359.6, path v_floor4 +535.3, path v_floor6 +353.9; main_peak +344.4, +536.6, +328.8; side_peak +207.6,+768.9,+212.8. All differences were positive in all eight holdout seeds per cohort/mode. This sensitivity cannot establish which occupancy model predicts reality.
- With the 2.5m conflict graph unchanged, differences among occupancy choices are meaningful internal model sensitivity. **Not** a formal causal decomposition of v5.7→v5.8 across all possible geometry parameters.

## Independent verification and literature
SUMO's official intersection documentation explains internal lanes/internal junctions, waiting within intersections and turning-radius-dependent speed limitations. This is a suitable independent implementation comparator, but SUMO has not been executed in this work environment. FHWA microsimulation calibration guidance stresses measuring queues, speeds/travel time and varying demand conditions with observed representative days; no field calibration is yet done.

## Two publication narratives
**Exhibition:** construction and validation of physically dimensioned centreline movement paths, road-capacity constraints, multi-junction longitudinal vehicle motion and signal gating; repeatable geometry error detection and unit consistency. Next target: lane geometry survey, true turn curvature, independent model prediction against observed lane queue length and departure count.

**Paper:** uncertainty in geometry, entry speed and unobserved turning clearance may yield different signal policy recommendations. Current v5.8 confirms predicted exposure sensitivity only and **does not establish an observed policy reversal or novelty result**. Next targeted study should match empirical observation vectors across plausible parameter sets and compare policy regret on an out-of-sample physically validated network.

## Gate to v5.9
1. Use real per-movement internal junction path from surveyed geometry / OpenStreetMap verified geometry, with lane connections and turn-radius-dependent speed.
2. Explicit vehicle kinematics over internal lanes and conflict locations, not merely instant transfer + aggregate time reservation.
3. Independent SUMO same OD/signal scenario, record vehicle trajectories and conflict-zone traversal-time residuals.
4. Select an actual Korean road junction and obtain observational signals and traffic counts; no manipulation of public signal infrastructure.
