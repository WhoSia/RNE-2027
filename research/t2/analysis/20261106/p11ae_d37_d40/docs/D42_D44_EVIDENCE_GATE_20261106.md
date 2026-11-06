# D42 and D44 — Evidence audit (2026-11-06)

## Official DLR UT v1.3.1 evidence
Record: https://zenodo.org/records/20919480
README: https://zenodo.org/records/20919480/files/README.md?download=1
One-day observation from 2023-09-24 00:00 UTC to 2023-09-25 00:00 UTC, 15-minute CSV batches, 20-Hz trajectory positions, 1-Hz signal states, 30 signal heads and OpenDRIVE map. Stopline traffic volume is defined by object-center crossing. License CC BY-NC-SA 4.0. Original ZIP ~463.4 MB; uncompressed ~3.13 GB.
The README warns about trajectory fragmentation, merged objects and possible recycled track IDs. Do not assign an observed exact event-time signal based only on the last 1-Hz state sample.
Evidence status: metadata/README read; DLR ZIP raw bytes NOT ACQUIRED, SHA256 NOT COMPUTED; actual lane queues and signal-head mapping NOT VALIDATED.

## Local prototype actually executed
Source-agnostic trajectory and signal audit module written and ten synthetic fixture unit tests passed locally (10/10). Handles tracking gaps, nonfinite records, position jumps, stale/unknown signal data, and interval-censored stopline crossings. These tests did NOT process raw DLR records; do not call them field validation.

## D44 code review
At research/t2/analysis/20261106/p11ab_d26_d30/d27/src/micro_world.py: dt_s != 1 is hard rejected. The speed step enforces acceleration but truncates speed to leader/road clearance without explicitly enforcing the per-vehicle decel_mps2 limit. Therefore the separate D34 time-step refinement is not evidence of this engine's convergence; actual stopping feasibility must be tested.
Next: execute the P10 original vehicle-1/vehicle-8 backdating witness on unchanged archived code, establish fractional time-step event causality, and test identical vehicle demand for dt=1,0.5,0.25,0.125.

## Acceptance gates
1. Download and hash original DLR ZIP.
2. Inspect original CSV and XODR, align head IDs to permitted movements and calibrate lane stoplines.
3. Reconstruct observed lane-specific crossing intervals, queue counts and quality flags. Unknown must remain unknown.
4. Independently execute version-pinned SUMO against matched geometry/demand/signal; preserve raw tripinfo, FCD, missing and incomplete vehicle accounting.
5. Fix policy definitions before evaluating an untouched holdout interval.

Offline research only; do not operate actual street signals.