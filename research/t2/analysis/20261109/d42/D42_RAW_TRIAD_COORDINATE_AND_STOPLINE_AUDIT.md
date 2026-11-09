# D42 — Real 20Hz vehicle / 1Hz light / reported crossing-count audit (2026-11-09)

## Provenance / bytes directly read
DLR Urban Traffic v1.3.1, 2023-09-24 12:00–12:15 UTC.
- Trajectories CSV: 51,209,266 bytes, SHA256 `5504d37534fd12e95a9e1b019de18f504a2d668dcf564392bb169d42ab42550e`, Drive `14yh6W9MLAW6IvsoZsvHr3SzS_rovYs6S`.
- Traffic lights CSV: 1,013,056 bytes, SHA256 `444290f5a29c9f3d767e275a2c87d281614d4ab951cc5a5a7ee9fb8c1bf9efcb`, Drive `1f8s3nFhMHeqFBAQ74ItgfpCQByNaHeVM`.
- Traffic volume CSV: 81,393 bytes, SHA256 `98e4e0a593702188c2d134cef1346cbc7501067c9ad421ddb9e72a1e6d9d1d15`, Drive `1L89cdXpt5qJ1hPS8w00C4pyzg-oxAqUB`.
- DLR OpenDRIVE XML: 820,847 bytes, SHA256 `256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4`, Drive `1j6xu3ngbh1dO75_eCdrgBWVgytRAzGtg`.

## Empirical results
- Trajectories: 299,053 raw rows, 636 unique track IDs (NOT independently identified physical persons/vehicles), exactly 18,000 time frames and 0.05s within-track increments; 2,673 interpolated rows (0.894%); no missing table cells. Coordinate-difference inferred maximum step speed = 20.0864232775849 m/s; no >40 m/s intervals. Reported velocity norm differs from easting/northing vector norm by at most 0.001177 m/s. Classification probabilities should not be equated to definitive ground-truth vehicle types.
- Traffic lights: 26,910 rows, 30 IDs at each observed timestamp, 897 unique timestamps; three sampling gaps just over or at 2s. State values `1,3,4,5,7,9` **not interpreted** before establishing official enum meanings.
- Temporal bridge via backward as-of match from 18,000 trajectory timestamps to sampled lights: 20 frames before first light observation, 30 frames where latest signal observation >1.5s old; remaining 17,950 frames matched to a sample with <=1.5s age, but still **not a guarantee of state between samples**. Staleness threshold is an audit parameter, not known signal physiology.
- 32 reported movement columns, 900 one-second rows, total reported cell counts = 436. This is a count of specified stopline-center crossing events in provided metadata and **cannot** be equated to 436 distinct tracked objects. Independent geometric recount has not been attempted.
- Mixed timestamp string precision (some exact integer seconds, others microseconds) requires `pd.to_datetime(..., format='mixed', utc=True)`; naïve single inferred datetime format fails.

## Spatial bridge / STOPLINE CANDIDATES (not yet field confirmed)
Assumed raw input CRS EPSG:32632 (UTM zone 32N) transformed with the embedded OpenDRIVE geoReference string; e.g. UTM (604755.977,5792823.363) -> XODR (-7.023,28.363) m. Source CRS documentation and lane-level validation are still required. Map XML has 28 road elements, 1 junction element, 7 `signal` elements with `dynamic=no` and `type=294`, 6 unique IDs (ID 300607 appears on 2 roads). German StVO Zeichen 294 is a stop line (Haltlinie), see https://www.gesetze-im-internet.de/stvo_2013/anlage_2.html. **Only a candidate stopline interpretation**; OpenDRIVE signals type context and actual lane offsets need independent validation. These seven static map elements are not the 30 live signal head IDs.

Arc-centerline reference coordinates for the seven candidates were derived from OpenDRIVE planView geometry; no 30-ID signal mapping or valid crossing adjudication claimed.

## Reproducibility and release
Local scripts `audit.py`, `test_audit.py`, `map_bridge.py`, `stopline_candidates.py` plus derived JSON/CSV included in versioned ZIP. Six synthetic audit unit tests PASS, two separate arc geometry assertions PASS.
Drive source-preserving release: https://drive.google.com/file/d/1aokvtHnTVuddPm5EVf_jua3trCCqXh-1/view
ZIP SHA-256 `ee2b85f8969fdc63a8795dfaa70a6a99a231ffaf5651ab5d07788a015badd8b1`, 10,192 bytes. ZIP deliberately omits raw 51MB/1MB/81KB/820KB sources; they stay in immutable Drive dataset lake, indexed by the SHA256 above.

Derived CSVs:
- movement counts: https://drive.google.com/file/d/1w_h2C3wyUUAPEm6RfNyR8U0CLSqQTrRl/view
- signal sample gaps: https://drive.google.com/file/d/10xqz6wUEjxzyoW6089ErQ5HcxRkrIL0w/view
- unknown/stale frame times: https://drive.google.com/file/d/10ak5btvFl_j296voAiKV-Wa0iWg-99i7/view
- stopline candidates: https://drive.google.com/file/d/1PQGhHfAFQoPwiL1AsGS2jBRVwY-Jsojx/view

## Must-pass next gate
1. Confirm CRS and type=294 semantics from primary dataset documentation; determine actual lane offset/width and heading/orientation.
2. Map signal CSV ID 1..30 to particular movements and stoplines using published metadata; retain UNKNOWN wherever unavailable.
3. Construct lane-aware center crossing event intervals between 20Hz position samples, censor partial tracks and interpolated segments. Independently reconcile by movement against 436 reported crossing counts; do not optimize mapping on the same target used to assess generalization.
4. Run matched-demand SUMO only after geometry, signal mapping and phase semantics are validated.
5. Preserve recorded partial observations; no claims about real policy improvements until independent field and numerical gates pass.
