# D42 — Real 15-minute DLR raw triad QA and epistemic gates (2026-11-09)

## Source files actually downloaded and parsed
Dataset: DLR Urban Traffic v1.3.1, CC BY-NC-SA 4.0, AIM Braunschweig.
Observation window: 2023-09-24 12:00–12:15 UTC.

| Role | Drive file ID | bytes | SHA-256 |
|---|---|---:|---|
| 20-Hz trajectories | `14yh6W9MLAW6IvsoZsvHr3SzS_rovYs6S` | 51,209,266 | `5504d37534fd12e95a9e1b019de18f504a2d668dcf564392bb169d42ab42550e` |
| 1-Hz traffic signals | `1f8s3nFhMHeqFBAQ74ItgfpCQByNaHeVM` | 1,013,056 | `444290f5a29c9f3d767e275a2c87d281614d4ab951cc5a5a7ee9fb8c1bf9efcb` |
| 1-Hz stopline crossing count metadata | `1L89cdXpt5qJ1hPS8w00C4pyzg-oxAqUB` | 81,393 | `98e4e0a593702188c2d134cef1346cbc7501067c9ad421ddb9e72a1e6d9d1d15` |

Raw files remain in `01_ACTIVE_T2/02_DATASETS/20_OBSERVED — International/DLR_UT_v1.3.1`, **not** the 20261109 '사유' Google Docs folder.

## Findings (direct Python processing of the three raw files)
- Trajectory: 299,053 records, 636 source tracking IDs, 18,000 distinct 0.05s timestamps, no duplicate ID-timestamp, no NULL/nonfinite numeric fields, no nonpositive within-ID time gap, maximum between-consecutive-points inferred speed ≈20.0864m/s. 2,673 rows marked interpolated (0.8938%). 4,276 rows have classification-probability sums outside [0.95,1.05]. Do not normalize silently or equate 636 IDs to unique real-world persons/vehicles: publisher warns track fragmentation, merges and ID recycling.
- Signals: 30 signal-head IDs; 26,910 samples; 897 distinct timestamps, one value for each head per observed time. Three ~2s gaps: next sample at 12:04:35.995, 12:09:35.986 and 12:12:55.981 UTC. 893 **observed** categorical transitions, of which 9 span ~2s gaps. Numeric codes observed: 1,3,4,5,7,9. Until the publisher code legend is checked, do NOT assert a particular code means red/yellow/green; a transition across a gap has interval-censored time.
- Count metadata: 900 one-second observations × 32 named movement fields; sum across cells = 436 recorded crossing counts, not the 636 tracking IDs. Counts per minute min 21, max 39, peak at minute index 5 (12:05–12:06 UTC). A stopline-count field can represent a crossing, not a distinct vehicle. Separate link geometry and movement assignment are required for independent reconstruction.
- Three missing signal-sample second slots: 12:04:34, 12:09:34, 12:12:54 UTC; recorded count cells in these seconds: 0, 1, 0. Do not claim all vehicle crossings have matched signal states.

## Status
**Passed:** files acquired and hashed, full raw 15-min trajectory schema and quality scan, categorical head and crossing metadata scan, independent QA prototype local tests (10/10). The full reproducibility bundle with two Python audit scripts, original-source checksum manifest, per-track QC, transition graph, per-minute count output and test logs passed ZIP integrity check:
https://drive.google.com/file/d/1IizRbVxb-M7RU3qP7twfY1qF0GnoLynA/view
ZIP SHA-256 `9d61950ec4d9528203345e0f3f20a003dde458f94ba934d2e50ba49f2ede124f`.

**HOLD:** normative decoding of state codes; traffic-signal head-to-movement mapping, OpenDRIVE lane geometry and exact stopline crossing, independent track-derived count agreement, queue calibration, independent SUMO execution, field policy ranking. There is no empirical policy effect claim.

## Specific next independent replication
1. Derive lane centerlines, stopline segments and traffic light head IDs using publisher documentation + OpenDRIVE; record ambiguities as UNKNOWN.
2. Determine possible temporal intervals of center-point stopline crossing from 20Hz trajectory segments. Use observed signal states only if exact head mapping is established and observation interval supports it; otherwise interval-censor.
3. Compare independently reconstructed counts with supplied 32-field metadata **only under identical movement labels**, accounting for fragmented IDs and uncertain assignments.
4. Select unmodified holdout windows, then calibrate T2 vs independent SUMO with identical OD, network and phase timings. Use complete/discarded-trip accounting.

## GitHub gate
`signal_volume_gate.py` and `test_signal_volume_gate.py` provide a small standard-library categorical time/gap gate, with seven synthetic tests **committed, not executed in this session**; the package's separate ten local QA tests were executed and passed. Do not merge these evidence claims.
