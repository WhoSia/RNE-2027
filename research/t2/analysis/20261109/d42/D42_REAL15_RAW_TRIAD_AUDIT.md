# D42 — DLR UT v1.3.1 raw 15-minute field audit (2026-11-09)

## Raw inputs: actual bytes acquired, not sample mocks

| Source 2023-09-24 12:00–12:15 UTC | Bytes | SHA-256 | Drive |
|---|---:|---|---|
| Trajectories (20 Hz) | 51,209,266 | `5504d37534fd12e95a9e1b019de18f504a2d668dcf564392bb169d42ab42550e` | [original](https://drive.google.com/file/d/14yh6W9MLAW6IvsoZsvHr3SzS_rovYs6S/view) |
| Signal heads (~1 Hz) | 1,013,056 | `444290f5a29c9f3d767e275a2c87d281614d4ab951cc5a5a7ee9fb8c1bf9efcb` | [original](https://drive.google.com/file/d/1f8s3nFhMHeqFBAQ74ItgfpCQByNaHeVM/view) |
| Publisher movement counters (1 Hz) | 81,393 | `98e4e0a593702188c2d134cef1346cbc7501067c9ad421ddb9e72a1e6d9d1d15` | [original](https://drive.google.com/file/d/1L89cdXpt5qJ1hPS8w00C4pyzg-oxAqUB/view) |

## Actual audit results

- Trajectories: 299,053 rows, 21 fields, exactly 18,000 global sample times, 636 unique track IDs. No null/nonfinite or duplicate ID–time fields; exactly 0.05 s spacing within each one-file track. `interpolated=True` for 2,673 rows (0.8938%). Median reported speed 3.75 m/s; p95 13.082; max 20.051.
- Track mean classification argmax: car 531, motorbike 13, van 11, truck 12, bicycle 52, pedestrian 17. Track ID != unique physical traffic participant because DLR documentation notes fragmentation and possible ID reuse/merging.
- Whole-camera field of view row-level motor class and velocity <0.5 m/s: 106,593 out of 280,983 motor-class rows (37.94%). Counting qualifying observations per one-second bin gives median 120, p95 233.15, max 293. **These are not lane-specific queue lengths** or unique stopped vehicles.
- Signal: 30 heads x 897 observations = 26,910 rows. Three ~2-second sampling gaps (largest 2.013 s). Across heads 893 recorded state changes, of which 9 changes occur across >1.5 s intervals. This is not 893 independent signal cycles. Codes follow publisher v1.3.1 Table 4: `1=off, 3=red, 4=red+yellow, 5=green, 7=yellow, 9=flashing yellow`. Observed row counts respectively 613, 21,114, 133, 4,408, 358, 284.
- Publisher-derived traffic volume: 900 second rows, 32 observed movement columns, sum=436 stopline crossing counter cells. Per publisher §5.1, an object center crossing a lane stopline triggers a count. No independent cross-check against lane geometry yet. `436` is not a proven distinct-ID vehicle count.

## Reproducibility / code

[Actual validated Python source, 10 synthetic contract tests, audit.json, execution log and research note ZIP](https://drive.google.com/file/d/1K0Dz4aoobl7NsPwVSxNeBLSTCrR812UO/view)

ZIP SHA-256 `6cbfd20d0e23f55af7bc0082451f45618715eb25f4529be24af4c26457b1a839`.
Local actual file audit succeeded; **10/10 synthetic contract unit tests PASS**. Raw publisher CSVs are not duplicated inside ZIP: re-fetch originals and verify hashes.
Research note: https://docs.google.com/document/d/14fh_Szq3f8YSpvXJqAPhoBiX9mSJAsxRYJkSj0Gm4FE/edit

## Critical unresolved acceptance gates

1. OpenDRIVE `road/lane/s` geometry and real physical stopline delineation, **not merely signal head coordinates**.
2. Link 32 movement labels to lane-level center crossing and validate timing against publisher 436 counter records, with explicit trajectory censoring and interpolation.
3. Identify signal head ↔ controlled movement from publisher map/geometry; hold `UNKNOWN` otherwise. For each 1 Hz signal change, transition is interval-censored (not known at a precise 20 Hz sample).
4. Independently replay identical demand, geography and signal phase with SUMO executable; compare to T2 with complete arrivals/departures/missing completions.
5. **No real-data-supported detector-error policy-ranking reversal yet**. Do not infer causal performance from this descriptive audit.

Sources: Official DLR documentation v1.3.1 §4.2 Table 4 and §5.1; README and three original CSV files are recorded above.
