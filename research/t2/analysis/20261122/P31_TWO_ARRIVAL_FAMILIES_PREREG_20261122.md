# T2 P31 prereg — independent arrival-clock families, 6s/10s event-metric robustness

2026-11-22 KST. **Precommitted before P31 execution**. Exploratory hypothesis following P30; no real-world traffic claim.

Freeze unused seeds `124,125` for 1650vph/left.50 and `126,127` for 1800vph/left.45. From `spatial_v10.arrivals`, preserve each seed's **complete ordered route labels and event count**, but reassign timestamps with two *pre-specified* qualitatively distinct mechanisms:
1. **uniform-clock**: for arrival rank i in N, integer time `floor((i+0.5)*duration_s/N)`, capped at duration−1. Creates regularly spaced ranks, no random arrival-time clustering.
2. **four-platoon-clock**: rank i maps to platoon `i%4`? NO: use `platoon=floor(4*i/N)` to retain ordered traffic sequence. Four fixed 15-second spans anchored at `(20,80,140,200)` seconds; inside a platoon, distribute ranks evenly over that 15-second span using `floor(15*(j+0.5)/size)` with size computed as actual assigned vehicles. Timestamps nondecreasing and 0≤t<240. Four clusters separated by 45-second low-arrival intervals. Clock families hold *routes and total count* fixed but not the same arrival timing, hence cannot be treated as a same-state intervention of the clock at t84.

- Geometry grid per tape: receiver slots2/4 × downstream offset0/15 × pocket14/28m × B-share0/.5, receiver headway2. **4 seeds ×2 clocks×16 geometries = 128 independent model worlds**, only **eight unique complete arrival tapes**. Four pairs of family-matched route labels.
- Within each world, fixed original physical engine and identical tick84 checkpoint; compare no intervention, 6s and10s model-left-stage. Primary: count worlds where model score6 equals score10, and where refusal-attempt delta10−6 differs from 0; secondary: unique rejected ID delta, observed crossing count and terminal remaining differences, tabulated by family.
- P30 signature from reused seed112–117 is **not** presumed universal and is tested as a candidate. A falsification occurs if even one new world shows nonzero 6 vs10 cost difference or the denial increments change; retain all negative results.
- Validate `vehicle_id` in trace events corresponds to each reordered arrival tape, exact conservation and checkpoint immutability. No p-value treating 128 replays as independent timestamps.
- Frozen code must never modify original arrival labels or drop events. Exact engine `main` bytes, no real yellow/red/pedestrian clearance simulation, no field controller use.
