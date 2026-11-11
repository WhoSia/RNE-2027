# D46-G (2026-11-11) — dimensioned event-storage acceptance gate

**Status: SYNTHETIC DIMENSIONAL CONTRACT PASS / D44 PHYSICAL BRAKING AND D42 FIELD SPATIAL WAVE HOLD.**

## New actually executed implementation

Independent `d46g_spatial.py` extends archived D46-F exact-rational calendar. Each vehicle has a unique ID and a physical length `ell_m`. Each link has metric length `L_m`, configured cruise `v_mps`, and standstill gap `g_m`. Scalar storage footprint = `ell_m + g_m` meters and maximum link occupancy is `L_m`. Earliest event eligibility after link entry is `L_m / v_mps` seconds. Tie order remains sink exit → inter-link transfer → external admission. The vehicle's full footprint is reserved until link exit.

**Not** a microscopic car-following trajectory: scalar occupied length does not identify vehicle coordinates, geometry-based queue tail, collision or wave speed. The speed is constant prescribed minimum-travel timing, not acceleration. A scalar conservative footprint includes a trailing gap even for a boundary vehicle.

## Executed 108-case controlled grid

Vehicle length 4.5 / 6.0 / 7.5 m × standstill gap 1 / 1.5 / 2 m × upstream link length 12 / 18 / 24 / 36 m × upstream cruise 9 / 18 / 36 m/s = 108 synthetic cases. Downstream length=36 m, downstream cruise=36 m/s. Demand stream 3 veh/s during [0,25] (75 total), 4 veh/s potential gate+transfer, sink 0 veh/s [0,10], 1 veh/s [10,30], 4 veh/s [30,40]. The sink rate integral cap is 60 vehicles.

Executed outlet counts span **18 to 60**. At upstream 18m, 18m/s, standstill gap 1.5m and downstream 36m/36m/s:
- 4.5m vehicle → 6m footprint → upstream storage 3 vehicles → **53 sink exits**, outside waiting 16.
- 6.0m vehicle → 7.5m footprint → storage 2 → **42 sink exits**, outside waiting 29.
- 7.5m vehicle → 9m footprint → storage 2 → **42 sink exits**, outside waiting 29.

This discontinuity is induced by **discrete link-packing and fixed service calendars**; NOT evidence for a measured road response or a traffic policy's merit.

Four homogeneous cases with lengths divisible by footprint and `tau=L/v` were checked against the sealed original D46-F vehicle-capacity engine: exact final (sink exits, external backlog, upstream stock, downstream stock) tuples **4/4 agree**. Shared assumptions mean this is an internal regression, not independent empirical truth.

## D44 auxiliary physics: diagnosis, not repair

Separate necessary check for constant deceleration and zero reaction delay: stopping distance `d_stop = v^2/(2 b_max)`. At 10 m/s and 3 m/s² a stop needs 16.67m, impossible within 6m. This is a separate diagnostic only: **braking is not integrated into event engine and original D27/D44 flaw is not repaired.**

Tests: new **25/25 PASS** and sealed original D46-F **24/24 PASS**, combined **49/49**; 108 grid executions; four exact model-consistency examples; source/CSV/JSON/manifest verified in ZIP.

Reproducibility ZIP: https://drive.google.com/file/d/1M5xDnOkNVFluvSdYE3aaSkBNHAO6_4tk/view

SHA-256: `a40196a439f5bee2779b71942f520a5ab5d1ff9237bcf9e66878780b42dd6562`.

Daily research Docs: https://docs.google.com/document/d/1ZZPfPZXyHazuLiSqOowHQfSRecseZtzSY1gn1EEOhqc/edit

**Remaining gates:** real lane positions and finite stoplines (D42), full viability-aware micro-motion (D44), independent SUMO and policy ranking under uncertainty. The exact executed scripts are inside the sealed Drive ZIP; this note does not claim individual new Python files were synced to GitHub. GitHub-actions[bot] contribution is not used.