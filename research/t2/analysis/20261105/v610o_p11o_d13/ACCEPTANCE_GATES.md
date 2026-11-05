# Audit acceptance gates (O)
## Data provenance
- Input: six *derived* MARWIS summaries from N, not raw CSV bytes.
- Cross-check: row totals = 5967, segment totals = 19, change boundaries = 13.
- Asphalt-labeled: 2860 rows/9 segments; concrete-labeled: 3107 rows/10 segments.
- Three weighting estimands checked: frame, constant segment, trip.
- Leave-one-trip-out contrast range checked: [0.01128930, 0.03132484].
- Independent observation count: UNKNOWN; sensor refresh interval: UNKNOWN; original file checksum validated locally: NO.

## Strictly prohibited conclusions
No iid assumption for frames or constant segments; no causal asphalt/concrete inference; no tire-ground-grip calibration; no field validation or safe-speed claims; no signal policy optimization or operational actuation.

## Graduation conditions
G-D13-1: obtain original raw CSV and verify hashes against upstream source.
G-D13-2: inspect per-field timestamp clocks, stale readings, dropout and duplication.
G-D13-3: determine observational unit and collect multiple independent sites/days.
G-P11-O: reproduce specific P10 timestamp-backdating regression at every required dt, compare same-input independent event scheduler.
G-V610-O: evaluate native OpenDRIVE real-source 3D geometry with an independent reference implementation, including knots/near-cusp cases.
G-EXTERNAL: same-conditions SUMO comparison before claims of policy rank stability.
