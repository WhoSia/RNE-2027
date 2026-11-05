# T2 P11-Z / D24 — 2026-11-06 research decision

## Executive decision

- **Development GO, narrow scope:** A single deterministic integer-clock reference now combines X's overlapping spatial resource sets and Y's ordered resource occupancy. Each zone is finite-slot-capacity, transitions reserve the next set atomically and release prior zones on transfer. When blocked, the movement retains its prior zones. Circular wait is diagnosed, **not silently resolved**. The engine is a synthetic discrete-event model, not a full microtraffic simulator.
- **Real-data evidence HOLD:** Actual official agency GTFS ZIP acquisition was attempted and failed due to DNS/network limitations. No agency raw file bytes, SHA-256 or row-level empirical analysis were obtained. The loader passed tests using an **explicit synthetic fixture**. Official live-source URLs are documented separately; no fabricated operational schedule appears in this package.
- **Policy P12 FROZEN:** All vehicle/demand/transfer input conditions here are fixed, not optimized or tuned to yield a preferred signal policy.

## Origins and independent checks

- X legacy source from `research/t2/analysis/20261105/p11x_d22/src/lane_fifo.py`, archived byte-identically as `baselines/x_lane_fifo.py`, SHA256 `6427b9a9903301b1ae58717ac695f2a6ac36a10037b92acade9d88b810c90486`.
- Y source from `research/t2/analysis/20261105/p11y_d23/src/zone_phases.py`, archived as `baselines/y_zone_phases.py`, SHA256 `6b8899e40fa33b78792c900170818f985db2b2e55740b26ec66771237b27947b`.
- New 18 unittest cases pass, including 100 random source-X equivalent scenarios, original-Y hold-and-wait entry/exit reproduction, 100 × 40 randomized requests for bounded occupancy/conservation, and six synthetic GTFS parsing cases.
- Prior Y archived tests pass separately: 17/17 (not integrated into new run).
- Baseline comparison applies only to models' **common supported subdomain**. It does not verify their complete semantics or the original P10 vehicle 1/8 trace.

## Synthetic cross-stage proof-of-concept

At t=0, pedestrian occupies B for 3 ticks; vehicle occupies A for 2 ticks nominally and then requests B for 2 ticks; follower requests A at t=1. With `capacity(A)=1`, B remains occupied until t=3, the vehicle holds A until t=3, and follower begins t=3. With `capacity(A)=2`, B remains at capacity 1 and follower starts t=1. This is a finite-slot thought experiment, not measured lane delay or driver behavior. A symmetric A→B/B→A example produces a circular wait witness `east → west → east` and explicitly raises `DeadlockError`.

The strong distinction: finite *abstract slot capacity* is not physical vehicle storage capacity. No length/spacing/vehicle class calibration, free speed, acceleration, road lanes, signal legality, midlink interaction, spatial collision geometry, actual GTFS routes, independent SUMO comparison or site-specific queues have been verified.

## Research value: two separate tracks

**Science fair:** Study observable local turn-pocket and crosswalk occupancy, queue formation/back-propagation/recovery, matched observed spatial lengths/time series, and an independently reproducible small demonstration. Strictly do not claim that generic synthetic occupancy or fixed-timetable route inversion measures real conditions. Publication/entry eligibility and overlapping preprints require organizer review.

**Journal:** Propose a mathematical test framework for time-causal multi-zone event semantics and finite-storage conservation. Actual novelty is unproven: compare rigorous discrete-event simulation semantics, resource-constrained movement scheduling, deadlock graphs, CTM/LTM and established traffic simulators. Need formal definitions, counterexamples, exact reference oracles, strong baselines, convergence analysis and empirical validation.

**Policy:** Prior ideas on dynamic signal control/OD/transfer remain unimplemented and FROZEN until substantial physical/observational gates pass. Timetable earliest arrival is not a control optimization.

## Next scientific gates

1. Audit original P10 sealed engine and replay the specific vehicle 1/8 failure in untouched and patched implementations.
2. Compare same multi-zone trace with real map-to-zone assignment and SUMO event logs; validate time units and stop-line occupancy, not just counts.
3. Obtain agency original GTFS ZIP, content hash and license. Confirm requested service day is active and that feeds' declared timezone, frequencies, minimum transfers, interstop pathways and post-24h times are handled. Missing GTFS-Realtime means no observed delays.
4. Add physical vehicle length/gaps and link dimensions to derive plausible capacity bounds; validate with video/trajectory occupancy where available.
5. Test gridlock interpretation: circular wait in a resource graph does not itself prove observed road gridlock.

## Sources

- Official GTFS Schedule: https://gtfs.org/documentation/schedule/reference/
- SMTD official current feed: https://www.smtd.org/about-smtd/gtfs/ ; downloadable advertised https://ride.smtd.org/gtfs/smtd_gtfs_feed.zip
- Malaysia official GTFS feed APIs and stated CC BY 4.0 license: https://developer.data.gov.my/realtime-api/gtfs-static.en
- MBTA official feed schema and download location: https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs.md
- Uber H3 index: https://h3geo.org/docs/ . Spatial index only, no timetable router.
