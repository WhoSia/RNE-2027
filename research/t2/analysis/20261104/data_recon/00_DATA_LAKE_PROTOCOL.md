# T2 Dataset OS — 2026-11-04

Canonical shared Drive: `R&E 2027 / 01_ACTIVE_T2 — 교통신호·차로 모델링 / 02_DATASETS — immutable source originals`.

Research data may be international. Keep Korean/Gyeongnam traffic as a later transfer/generalization target for a regional science fair, not a prerequisite for physical calibration.

Separate `10_OBSERVED — KR`, `20_OBSERVED — International`, `30_SIMULATION_SCENARIOS — SUMO`, `40_DERIVED`, and `90_QUARANTINE_AND_UNVERIFIED`; preserve raw provider bytes with SHA256, source URL, version, collection period, unit, license and receipt. Do not overwrite original files. Never call SUMO scenario inputs real-road observations or join NGSIM and Utah SPaT as co-located observations. Utah SPaT and related Utah BSM may be joinable after checking actual station IDs/time windows.

Data intake status: provider catalog verified, but real Jinju/NGSIM/Utah raw observations and full SUMO networks **not yet downloaded**. Exact LuST `scenario/dua.static.sumocfg` source file (1397 bytes) was acquired and upstream Git blob SHA-1 verified; it alone is NOT the complete LuST scenario. Public source details and receipt are in Drive catalog README.

Prioritize offline vehicle-trajectory calibration, observed signal phase transitions, and independent traffic-count validation. Only then compare signal-policy ranking against held-out real observations. Retain existing T2 v6.9 optimization ZIPs unchanged. `github-actions[bot]` must not contribute.
