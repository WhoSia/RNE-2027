# DLR 15-minute file completeness is NOT guaranteed

2026-11-13 source data audit found that DLR source filenames and time-window completeness are different concepts.

At UTC 2023-09-24 **23:30–23:45**, the three source CSVs were read directly from the existing user's Research OS Drive original dataset:
- trajectories: **8,624 rows**, **37 unique track IDs**, **21 columns** (timestamp, UTM position, velocity, acceleration, dimension, class probability, interpolated).
- traffic_lights: **899 distinct sampling instants**, **30 signal heads** and **26,970 head records**.
- traffic_volume: **893 one-second records**, **12 movement columns**, **17 total publisher-derived movement counts**. First volume timestamp 23:30:07 UTC, last 23:44:59 UTC, so first seven nominal seconds are not recorded in this source table.

The earlier audit script wrongly required exactly 900 volume rows per 15-minute file. That overstrong contract was corrected: reject empty, >900, malformed, duplicate or out-of-order observations, but **accept partial intervals and flag** `partial_window`, `coverage_ratio`. Neither interpolate nor set missing counts to zero unless independently justified.

The previous 96×3 complete matching 15-minute **filename** census is still accurate, but it cannot prove full data availability in every 15-minute interval. This is an identified data-quality failure mode, not a corrupted-file claim. The 18:00–18:30 UTC evaluation holdout remains reserved and its contents unopened.

Independent cross-date evaluation is still unavailable from this one-day DLR-UT record; future source search and site selection should account for it.

Dataset source https://zenodo.org/records/20919480. Full operational artifact is sealed in Drive reproducibility evidence; output examples and tests are available in this repo.
