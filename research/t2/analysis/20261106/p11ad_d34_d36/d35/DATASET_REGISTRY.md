# D35 — external evidence registry, 2026-11-06

| Source | What was actually verified | Acquisition status | Valid target |
|---|---|---|---|
| AD-Assurance-Lab [winter-driving mcity asphalt 1](https://github.com/AD-Assurance-Lab/dataset--winter-driving--main/blob/main/metadata/mcity_wspi/jan28-highway-asphalt1_sync.csv) | GitHub source CSV 933 rows, 40 columns; git blob SHA-1 e7bae3751fae6aedfabd3328ef720ce6a4ca7390; duration 19.53 s | Original source read with connected GitHub; local preservation only of derived summary, raw redistribution/licence not verified | Speed and sensor data quality audits, NOT queue/signal calibration |
| ETH Zürich [UTD19](https://doi.org/10.3929/ethz-b-000437802) | Official DOI, 40 cities, ~23.5k detectors; source documentation and data license CC BY-NC-SA 4.0 | Dataset download not obtained; official metadata reviewed | Urban flow, occupancy, speed distribution; NOT vehicle-level trajectories or exact queues |
| [SUMO official downloads](https://eclipse.dev/sumo/docs/Downloads.html) | Official `eclipse-sumo` wheel install route | `sumo`,`netconvert` missing; pip install returned no matching distribution in this container | Independent physical simulator comparison after real binary execution |
| [GTFS official example](https://gtfs.org/getting-started/example-feed/) | Canonical illustrative schema | No new real operator feed; educational sample only | Validate GTFS parser interface; not empirical trip reliability |

Do not confuse the above sensor run with real traffic policy outcomes. Raw file hashes beyond the GitHub blob ID have NOT been verified locally. Underlying vehicle-following model remains uncalibrated.
