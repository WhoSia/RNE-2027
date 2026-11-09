# D42-R1 — DLR UT v1.3.1 20Hz/1Hz Real-File Alignment Audit (2026-11-09)

## Single immutable observation window
2023-09-24 12:00:00 to 12:15:00 UTC. Original source is [DLR Urban Traffic Dataset v1.3.1](https://zenodo.org/records/20919480), CC BY-NC-SA 4.0. Read original individual Drive files rather than its 463MB ZIP (which exceeded 256MiB connector limit). All four source byte streams were fetched and hashed locally:

| Original | Bytes | SHA-256 |
|---|---:|---|
| trajectories_230924-120000_230924-121500.csv | 51,209,266 | 5504d37534fd12e95a9e1b019de18f504a2d668dcf564392bb169d42ab42550e |
| traffic-lights_230924-120000_230924-121500.csv | 1,013,056 | 444290f5a29c9f3d767e275a2c87d281614d4ab951cc5a5a7ee9fb8c1bf9efcb |
| traffic-volume_230924-120000_230924-121500.csv | 81,393 | 98e4e0a593702188c2d134cef1346cbc7501067c9ad421ddb9e72a1e6d9d1d15 |
| bs-inner-ring-road-ut.xodr | 820,847 | 256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4 |

Original Google Drive IDs respectively: `14yh6W9MLAW6IvsoZsvHr3SzS_rovYs6S`, `1f8s3nFhMHeqFBAQ74ItgfpCQByNaHeVM`, `1L89cdXpt5qJ1hPS8w00C4pyzg-oxAqUB`, `1j6xu3ngbh1dO75_eCdrgBWVgytRAzGtg`.

## Executed acceptance checks
The 51.2 MB raw trajectory CSV contains 299,053 rows × 21 fields, 636 *within-file track IDs*, 18,000 unique 20Hz frame timestamps. 2,673 rows carry `interpolated=True` (0.8938%). No missing values in the 21 parsed columns; no nonmonotone per-ID time steps, nonfinite positions/speeds, >50m successive coordinate leaps or >40 m/s finite-difference leaps under this window's checks. Every within-ID consecutive timestep is 0.05s. These are **limited quality tests**, not a complete verification of physically correct trajectories or identity stability.

Official published PDF Table 4 explicitly defines traffic light state code 3=red, 4=red-yellow, 5=green, 7=yellow, 9=flashing yellow, 1=off. The 30 signal IDs each have 897 recorded samples (26,910 rows). Signal timestamps are jittered around `XX:XX:SS.991`; **truncation to integral UTC seconds creates false missing samples** (about 55). Align to nominal 1Hz sample grid with the expected 0.991-second phase first: only 3 nominal samples are missing, at offsets 274, 574, 774 seconds (12:04:34, 12:09:34, 12:12:54 UTC). Across raw snapshots, gaps are ~2.013, 2.000, 1.999 seconds. No claim about actual hidden light color at missing instants.

The provider's traffic-volume CSV has 900 1-second rows and 32 movement-direction columns. Sum of numeric count cells is 436. The source README describes center-of-object stopline crossings: this **is not** a unique-vehicle count comparable directly to the 636 tracked IDs. Counts must later be checked at identical stoplines, lane definitions and time windows.

## Joint, explicitly limited observational facts
A 900-second aggregate series was computed from the track CSV. Across 18,000 frames, the mean number of simultaneously visible track rows per camera frame is 16.6141, and mean number of motorized-classification-dominant track rows moving <0.5m/s is 5.9218 per frame. These are **whole-camera-footprint state proxies**, not queue length or the causal effect of a policy.

For any trajectory row, if the *previous observed* signal snapshot is more than 1.1s old, freshness is flagged (not imputed). 340 trajectory rows precede the first signal snapshot, 1,058 are >1.1s stale, 297,655 have previous snapshot age <=1.1s. The 1.1s threshold is an analysis diagnostic only; last observation does **not** establish the true color between controller events.

Independent test module: **11/11 PASS** for raw-file observations and diagnostic invariants. Run the included `audit.py`, `joint_timeline.py`, `test_field_gate.py` with original raw sources supplied separately.

## Files and topology
The reproducibility ZIP is **20,034 bytes**, SHA-256 `d636fc0028a23754be969448b2d316cabd2ae43339e67e5785c1e1ebbe305dc7`. It intentionally excludes the 52MB raw sources to avoid duplication and preserve the DLR author's CC BY-NC-SA provenance:
https://drive.google.com/file/d/1x5PEc5j2emGhLQVWUb2odzRm_nH7309g/view

Derived 1s timeline:
https://drive.google.com/file/d/1E4WHxDVbjS1HR72r5YATnbtivCGDil0v/view

Derived head-level observed state summary:
https://drive.google.com/file/d/1tpyeXBc9saqmc9_EcRay_D9rOKsk6o3E/view

Research notes are in the 20261109 Google Docs, source files in 01_ACTIVE_T2/02_DATASETS/20_OBSERVED, derived files in 40_DERIVED and sealed ZIP in 03_REPRODUCIBLE_EVIDENCE. No new date-specific Drive folders created.

## Open gates / prohibitions
1. Establish and audit OpenDRIVE lane geometry, reference projection and *movement-specific* stoplines versus `center_easting/center_northing`. OpenDRIVE's signal entities (IDs ~300600) cannot simply be equated to 1..30 observational signal-head IDs; official PDF has geographic positions but no validated signal-to-movement binding yet.
2. Reconstruct crossing events and confidence intervals from 20Hz samples, distinguish stopline crossing and unique-ID semantics, compare against publisher's 32 movement counters.
3. Explicitly propagate signal sampling uncertainty especially near 3 missing seconds and all transitions.
4. Only then derive lane-specific queues, calibrate micro motion, run independent SUMO parity and policy holdouts. No current field-derived superiority or reversed ranking claim.

This unit is an *offline observation data gate*, not operational traffic light control.
