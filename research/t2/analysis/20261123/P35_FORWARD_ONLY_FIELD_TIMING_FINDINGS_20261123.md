# T2 P35 — 23 Nov 2026: Forward-only signal observation and 20Hz crossing-time robustness

**Verdict: Measured observational information boundary CONFIRMED; signal-controller/approach correspondence and field intervention effect HOLD.**

## Origin and frozen source ancestry

This is the first T2 study filed under `research/t2/analysis/20261123/` and [new Research Log folder](https://drive.google.com/drive/folders/1HGigW9JfBuIuG-mx6gK3GjTHAA5XhDZC). The 22 Nov P33 synchronized signal-sampling gap and P34-OBS 17 geometrically detected vehicle-center stopline crossings are *not* rewritten or relabeled as new findings. [P35 protocol](P35_OBSERVATION_TIMING_PREREG_20261123.md) was committed to `main` at `94b01a493adf871a8879a161902102336a07c88b` **before** the P35 outcome calculation.

Required exact original inputs:
- P34 independent-code and event archive (itself a **same-source** cross-check): SHA-256 `bb8701db35578951e82202845c5fa9b65d5ee55afb31c1afed22292e65a3c679`. The frozen internal 17-event JSON is `ea0eaae72afd8e82547a5f0b278765e27a871d86cdabeb34a2e4bf4e0a646c72`.
- DLR-UT 2023-09-24 23:30–23:45Z traffic signals, 30 heads / 26,970 rows, exact SHA `95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c`.
- Same-window publisher-derived route counter, 893 rows / 17 events, exact SHA `00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798`.

P34's 2015 OpenDRIVE marker is a tangent-plane approximation, **not** the verified 2023 physical painted stopline; its original 17 detections each have a 50ms interval containing a *linearly estimated* crossing instant. The P34 producer traffic-volume count comes from the **same trajectory producer** and is not independent real-world truth.

## P35 experiments and results

### A. The nearest recorded signal can occur after the crossing

For each P34 crossing interval `[a,b]`, the *causally available* record is the most recent of the 899 synchronized signal timestamps **at or before a**. The retrospective nearest record is whichever 1Hz sample is closest to the interpolated estimated crossing instant; it is not necessarily available at the time of crossing. We do **not** assign the unknown controlling signal ID to any approaching car.

| Measurement | P35 observed |
|---|---:|
| Geometrically detected P34 crossing brackets | **17** |
| Nearest sample is *in the future* of estimated crossing | **11 / 17** |
| Nearest sample is *after the 50ms vehicle interval has already ended* | **10 / 17** |
| A signal sample occurs *within* the vehicle's 50ms crossing bracket | **1 / 17** |
| At least one of all 30 signal heads differs between the bracketing observed sample states | **5 / 17** events |
| Total head×event pairs with different bracketing observed codes | **8 / 510** |
| Actual crossing brackets overlapping the earlier P33 2.004s common signal gap | **0 / 17** |

The **11/17** is a temporal observation hazard under a naive nearest-neighbor join, **not** 11 actual signal phase mistakes or infractions. The one interval straddling a signal sample was **caught as a real implementation boundary defect during the first P35 execution**, then corrected to retain the interval instead of assuming every 50ms bracket lies between consecutive 1Hz samples. Merely adding a limitation without repairing the code would have masked this case.

A different code on either side of a crossing interval for 5 events means we cannot **assume** the state was constant without further evidence, but it does not establish the actual transition time. Without official head→controlled approach/lane mapping, **8 discordant head×crossing observations do not identify 8 conflicting signals for these vehicles**.

### B. Causal freshness at bracket *end*

This conservatively measures the age of the latest signal *available before the candidate crossing interval begins*, measured at the **end** of that vehicle's 50ms bracket.

| Strict past-only recency maximum | Events with record sufficiently fresh | Events without a sufficiently fresh past record |
|---|---:|---:|
| ≤0.25 s | 3 | 14 |
| ≤0.50 s | 6 | 11 |
| ≤1.00 s | 16 | 1 |
| ≤1.50 s | 17 | 0 |
| ≤2.50 s | 17 | 0 |

Observed worst-case staleness: **min 0.126482s, median 0.678482s, max 1.022482s**. The 2.004s global P33 missing-sample interval contained no P34 directly detected stopline crossing, although P33 separately counted **40 observations of one tracked object** there. Do not conflate 40 track samples with 40 distinct crossing events.

### C. Published derived route-count match is highly sensitive to matching tolerance

The P35 tool **reuses the exact source-frozen P34 max-cardinality/minimum-absolute-error dynamic-programming matcher**, changes only a declared threshold, restores the original threshold, and reads the actual official traffic-volume CSV. The independent Node.js program implements its own ordered dynamic programming from the raw CSV and reproduces every total without importing the Python matcher.

| Same-approach timestamp tolerance | Paired P34 crossing candidates to published counters |
|---|---:|
| ±0.25s | **4 / 17** |
| ±0.50s | **7 / 17** |
| ±0.75s | **10 / 17** |
| ±1.00s (P34 original) | **16 / 17** |
| ±1.50s | **16 / 17** |

A 16/17 same-producer match **must always be stated with ±1s tolerance and approach-only matching**; tightening it to ±0.5s cuts it to seven. This is not proof the DLR timestamps are erroneous: the publisher's 1-second counter and geometrically interpolated sub-second trajectory timestamps represent different clock conventions, and a 2015 stopline map is not a trusted 2023 stripe survey.

## Exact execution, multi-role adversarial review and source hashes

- [Primary Python tool](p35_observation_timing.py), production source Git blob `5e2bc07db32d22474f9c5d9096087c2a82145cfb`. Python was retained because reusing the frozen P34 exact matcher removes a provenance risk; no wholesale rewrite.
- [15 Python tests](test_p35_observation_timing.py), final portable Git blob `b452b40de592b5a3379c3f197b597aac5400f36e`, **15/15 PASS**. Includes corrupted original ZIP, signal and volume SHA rejection, counterfactual invalid crossing bracket, forbidden invented signal head, future-information leakage, synthetic straddle, source parity, and deterministic rerun. An early test draft failed only due to comparing tuple vs list and in-memory vs JSON tuples; repaired test expectations; no scientific result was changed.
- [Independent exact-microsecond Node 22 oracle](p35_independent_node_oracle.mjs), Git blob `981601f54c42e36e33752e94ea905b415c0afe71`. Reads the actual three original sources, uses **BigInt microseconds** (no precision loss from JS millisecond Dates), reconstructs signal-clock and independent matching DP, verifies **13 core parity claims**, all PASS.
- [Full per-object event ledger](P35_FORWARD_ONLY_TIMING_FULL_20261123.json), result SHA-256 `2a6dbc99b6643879b88dd3c9a18f756acd31bf6a95a358c5c11a0f9bf659d58f`.
- [Independent oracle receipt](P35_NODE_INDEPENDENT_PARITY_20261123.json), SHA-256 `21c06bbd755dac5f453f39a1fdbce7bf4953bc9f69aeadcfe3802562e9b38625`.
- **Inherited P34 original 23 tests and corrected P24b 7 tests: 30/30 PASS** after fetching the exact proper official PDF version. A separate initially mounted PDF with the same display filename had the wrong hash; this was a **provenance mismatch**, not an excuse to disable the guard. The file was replaced from exact Drive source before inherited tests were re-executed. Preserve the specific original digest and source ID in release manifest; avoid claiming that a different same-name PDF has equivalent authority.
- Source/tree integrity: each GitHub `main` file's fetched Git blob SHA equals the locally executed file's `git hash-object`. No GitHub Actions or additional branches.

**Construct/causal reviewer:** A past sampled code is not guaranteed to equal the continuously displayed phase at the event instant. Nearest-sample hindsight is a *potential design leakage*; a future sample cannot be used by an online algorithm.

**Statistical reviewer:** Each head×event combination reuses the same 17 crossing events and 30 synchronized signal sensors, so 8/510 is descriptive and must not be analyzed as 510 independent vehicles. No p-value is warranted.

**Geometry reviewer:** The P24b old-map laneValidity entries in the 2015 map have not been validated as 2023 active controller lanes. No signal→approach mapping has been verified.

## Resulting actionable design decisions

1. Any future sensor→policy interface must explicitly require **observation timestamp ≤ decision time**, plus declared max age and error/unknown behavior, and must not infer a discrete traffic-light state by linear interpolation.
2. When 50ms vehicle event brackets straddle a 1Hz signal sample, report both the interval and the record ordering; never silently collapse to one predicted instant.
3. Keep publisher-derived counting as *same-source consistency*. Before real-world inference, validate approach/turn destination, official head→lane mapping and a separately measured physical stopline or independent detector.
4. Return to the founding question now: exhibit observable discharge blockage vs demand absence vs sensor non-detection, then independently simulate finite receiver capacity in SUMO. **P35 has not calibrated SUMO or verified operational signal feasibility**.

**RAVEL return:** CORE question = what decision-time signal state is supportable? Current milestone = observation-boundary CORE / field-causality ENABLING; RAVEL attack changed implementation when one event straddled sample. Authority ceiling = field CSV timing. Next = a real controlled-lane mapping or independent simulator rather than further metadata-only work. Debt=1.
