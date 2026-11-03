# T2 v6.4-P0 — Reality/field-data gate | 20261103

**Stage:** experimental specification only. No acquired field traffic observations. Grounding: FHWA Traffic Analysis Toolbox Volume III, original and 2019 calibration update; SUMO official Intersections documentation.

## Required records
1. Junction geometry: measured lane count/width, stop-line geometry, connectors/turn radius, polygon and coordinate reference, provenance and positional uncertainty.
2. Traffic-signal history: direction-specific phases, green/yellow/all-red, offsets, pedestrian and cyclist conflicts, timestamp with timezone.
3. Movement-specific turning counts: inbound lane, outbound road/lane, vehicle class, observation window, coverage/missingness.
4. Anonymous trajectories: time, x/y, speed, heading, uncertainty; do not store personal identities/plate or faces as study observations.
5. Field validation: same-time queues, counts, travel-time, capacity; separate calibration days and holdout days. Unmeasured pedestrian counts must NOT be interpreted as zero.
6. Reproduction: source, permission, transformation and provenance for every input.
## Engineering target
Baseline simple queue model vs T2 single connector vs independent SUMO with matched geometry, OD and phases; report error by movement, demand regime and time, not pooled summary alone.
## Gate
No claimed field predictive performance until a surveyed local intersection is encoded and validated on dates not used for calibration.
Reproducible complete package in shared Drive: T2_v64_P0_field_readiness_policy_value_20261103.zip.
