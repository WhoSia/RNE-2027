# T2 v6.7-P1 — Model contract, 20261104

Research OS: shared-drive 02_RESEARCH_LOG / 20261104 김우준의 사유. This is a **P1 experimental extension** of the v6.6 2D single-connector harness, not a replacement for the separate v6.7-P0 mesoscopic prototype already logged in today's Docs.

New state: each vehicle has a car/truck class with class-specific length, width, minimum gap, acceleration cap, braking cap. Sensitivity parameters (NOT field-calibrated): car 4.5m×1.8m, min gap 2m; truck 10m×2.5m, min gap 3m, acceleration 0.65x and braking 0.75x reference car. A separate random number stream assigns vehicle type while preserving same arrival time/source/ID across fleet-share conditions.

Downstream storage is approximated as sum of (vehicle length+minimum gap) for vehicles in link D, bounded by 25m or 140m. This is a meter-based **queue occupancy proxy**, not exact spatial link geometry or calibrated receiving supply. Alternative count-based admission is preserved for regression.

An exclusive pedestrian signal phase P uses 0s or 8s carved from side movement green; no pedestrian agents or crossing-time observations exist. An anticipatory gate includes minimal connector clearance before P. Zero sampled conflicts does not prove pedestrian safety.

Core invariant: generated = pending+approach+connector+downstream+completed; no simultaneous duplicate memberships. Every monitored violation is logged rather than silently labeled a success. Single-vehicle exclusive connector means parallel compatible movements are not validated here.
