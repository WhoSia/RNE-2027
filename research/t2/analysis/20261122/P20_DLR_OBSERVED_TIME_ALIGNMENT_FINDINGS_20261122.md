# T2 P20 — Real DLR-UT 1.3.1 time-alignment and source integrity check

Date 2026-11-22 KST. **Real observational raw CSV were independently downloaded and read** from the existing R&E dataset lake. This is a *schema/timing gate*, not calibration to the T2 simulator, not an intersection-specific vehicle discharge study.

## Data provenance
The source folder [DLR_UT_v1.3.1](https://drive.google.com/drive/folders/1MgVtPHh8UKMuv0hNhUQLRSmP_oNLN_FX) already contains `raw_data/trajectories`, `traffic_lights`, weather, road condition, air quality, map and metadata. Files sampled (both for **2023-09-24 23:30–23:45 UTC**, same nominal 15-minute interval):

1. [trajectories_230924-233000_230924-234500.csv](https://drive.google.com/file/d/16SyjOzQBy5t9iVIV0tdZaAOlo39jYOri/view), 1,478,064 bytes, SHA-256 `6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50`.
2. [traffic-lights_230924-233000_230924-234500.csv](https://drive.google.com/file/d/1TXma5bvw_M-NSfqO2LhW7JrEFqANxUOy/view), 1,015,948 bytes, SHA-256 `95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c`.

Verified both Drive download bytes and parsed actual CSV. **Do not re-upload an altered original**. The analysis code refuses source SHA mismatches.

## Observation results

| Metric | Trajectories | Signal state |
|---|---:|---:|
| Rows | 8,624 | 26,970 |
| Distinct IDs | 37 tracked objects | 30 signal IDs |
| Timestamp window start UTC | 23:30:07.816482 | 23:30:00.992000 |
| Timestamp window end UTC | 23:44:59.966482 | 23:44:59.988000 |
| Median within-ID sampling interval | 0.05 s | 1.0 s |
| Duplicate (ID,timestamp) pairs | 0 | 0 |
| Empty cells in fields | 0 | 0 |

The signal series contains codes 1,3,4,5,7,9 with respective rows 604,20,924,128,4,680,339,295, totaling 26,970 rows. Across the **30 signal ID series**, there are 869 observed adjacent code changes, not 869 legal traffic signal transitions by color. The meaning of integer codes has not been independently checked in the official DLR codebook.

Rows with `classifications_car > 0.5`: 6,471, with velocity_magnitude median 6.025 in the dataset's stated numeric column. These are repeated samples from moving tracked objects, not 6,471 different cars; the entire trajectory window contains only **37 unique object IDs**.

## Important parsing failure discovered and repaired

Naïve pandas `to_datetime` failed because signal timestamps mix fractional seconds and whole seconds in the same column. The documented parsing code uses `datetime.fromisoformat` (which accepts both) and preserves UTC offsets. This is the first concrete external data integration pitfall for P20.

## Why this is NOT yet a model-to-field comparison

- Vehicle coordinates use easting/northing and signal measurements use signal IDs. We have **not yet validated the map-based link/lane geometry or which signal head controls which trajectory**. Matching file intervals alone does not establish a causal signal–car trajectory pair.
- Sampling clocks differ roughly 20:1, so joining by exact timestamp or discarding unmatched samples would yield severe selection artifacts. A synchronized join must declare lag, interpolation, time-zone conversion, nearest-neighbor tolerance, and held-out windows.
- An all-car speed median cannot be compared to T2's discharge time headway without identifying the actual stopline crossing trajectory and its controlling phase.
- The source is one 15-minute observational window; repeated high-rate rows do not constitute independent observations for statistical uncertainty.
- The DLR sensor classification is an observed *object class probability*, not evidence of Wi-Fi CSI capability or of causal pocket blockade.

## Executed software verification

- [SHA-pinned CSV reader and alignment metadata audit](p20_dlr_observed_window_gate.py).
- [Five independent regression tests](test_p20_dlr_observed_window_gate.py): exact original window counts, hash mismatch rejection, mixed timestamp parsing, empty-source failure, missing-ID failure.
- **5/5 tests PASSED** with actual downloaded files. Remote GitHub `main` source/test exact Git blob files were separately recovered, hashed against remote, and re-executed: implementation `54f7c2ab8d1a76e49ddead3c5ab2d9740018982b`, test `840ee4035de32b0f640b598ae51e2729e474febf`.
- [Frozen machine-readable results](P20_DLR_UT_REAL_OBSERVATION_15MIN_SUMMARY_20261122.json). Codebook, map alignment, and discharge calibration **OPEN**.

## Research direction
1. Use the existing DLR map `bs-inner-ring-road-ut.xodr` and official codebook to assign signal IDs to stop lines/turn lanes.
2. Freeze a single monitored movement, derive stopline crossing times from trajectories independently of the simulator, and calculate headway/queue distributions on that movement.
3. Only then compare model-P19 vs DLR and subsequently a separately executed SUMO with matched geometry, with uncertainty intervals and observed-data selection declared prospectively.
4. The required signal phase ordering/amber/pedestrian rights cannot be inferred from this 15-minute integer-code count alone.

K047 remains sealed; ~5GB CIM ZIP still unlocated and not opened; no live road signal access; no GitHub Actions.
