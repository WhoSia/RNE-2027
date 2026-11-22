# T2 P24 — OpenDRIVE stopline candidates and observed signal head crosswalk

**2026-11-22 KST | physically grounded engineering | decision: PARTIAL ACCEPT, signal→lane crosswalk still HOLD.**

## 1. Evidence and version boundaries

Source A: [DLR-UT v1.3.1 official PDF](https://drive.google.com/file/d/1gUqUJEAGtXw06RjQCLbBoJ0k-pcee5Uq/view), 27 pages, pp. 12–13 Table 3 (signal locations) and p. 14 Table 4 (state codes), verified SHA256 **94fd9ebd32d04a9c35b02be526fbd11a8d5a613933d7961fde800386853b34f3**.

Source B: [DLR source OpenDRIVE map](https://drive.google.com/file/d/1j6xu3ngbh1dO75_eCdrgBWVgytRAzGtg/view), file `bs-inner-ring-road-ut.xodr`, verified SHA256 **256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4**.

The OpenDRIVE header reports **revision 1.4, vendor DLR, date 2015-03-25, map version 1.0.0**; the observed time-series is **2023-09-24**. Therefore do not infer that the 2015 digital map encodes the precise 2023 controller program or lane use without additional checks.

The map consists of **28 road elements, one junction, and seven XML `<signal>` elements**. The seven `<signal>` elements have **`dynamic="no"`, `type="294"` and six distinct IDs**: 300600, 300602, 300604, 300605, 300606, 300607 (ID 300607 reused across two road elements). This is NOT the same namespace as the observed 30 light IDs (1–30). **No active controller or verified observed-light-ID link is embedded in those seven entries.**

External ASAM reference: [OpenDRIVE–CityGML stopline example](https://publications.pages.asam.net/standards/ASAM_OpenDRIVE_with_CityGML/index.html) uses static signal `type="294"` to represent a **stopline marking**, not necessarily a traffic lamp. [ASAM OpenDRIVE signal-reference example](https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.8.1/specification/14_signals/14_04_signal_reference.html) explicitly distinguishes a dynamic lamp, static stopline, and an optional reference/dependency. This interpretation is grounded in the standard example and this file's actual attributes, but the 2015 file supplies no explicit lamp→stopline dependency to audit.

## 2. Coordinate-normalization experiment

The XODR header declares `+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=-104763 +y_0=-5792795 +datum=WGS84 +units=m +no_defs`. The official PDF Table 3 gives 18 measured UTM zone 32U coordinates for nine **vehicle signal IDs**. Using `pyproj` transform `EPSG:32632 → map CRS`, signal 1's first head `(604755.480,5792814.102)` becomes XODR local `(-7.520,19.102)m`, consistent with the offset of this map.

Each static XODR feature was positioned using its actual road `s,t` coordinates, the appropriate OpenDRIVE reference-line geometry (line or constant-curvature arc), and a checked reverse coordinate transformation to EPSG:32632. For each of the 18 official signal-head points, the three nearest *static map features* were ranked as **hypotheses only**, with no movement assignment.

Distance to nearest static marking across 18 heads: **min 4.673m, median 8.057m, max 18.924m**. A 4–19m offset is plausible for different physical roadside features but proximity is NOT proof of which traffic signal controls which crossing. The 18 points are multiple heads for nine observed IDs; they must not be mislabeled as 18 independent phase controllers.

## 3. Source-faithful failure gates

**PASS:** original PDF/map byte SHA, EPSG zone 32→local reversible transform, 28-road/one-junction/7-feature census, nine official vehicle-light IDs with 18 physical coordinate records, geometry solver regression, no ID conflation. **FAIL-CLOSED:** `controlling_lane=None`, `movement=None` for all 18 head candidates. No fabricated signal→stopline or signal→movement linkage.

**NEXT:** interpret XODR laneSection/road links/road direction and the published traffic-volume column naming convention (`East1South0`, etc.); create an independent manual/geometry evidence table specifying lane validity and crossing direction. Validate one candidate using 20Hz observed trajectories and same-window 1Hz movement counting WITHOUT selecting only successful exits. Freeze temporal interpolation rule before testing. Physical queue-tail, pocket spillback and independent SUMO matched-road validation remain open.

## 4. P23 evidence lineage correction

A prior P23 release ZIP contains **old PDF SHA256 3c733b…3849** and tests claiming success. The actually fetched Drive PDF in the present session hashes **94fd9ebd…34f3**. The current `main` P23 reader has already been updated to the latter SHA (Git blob **f2363324a7a3c8aa2017901d9d2da1d9f4f5c1c1**), and the prior test file, rerun locally against the actual present PDF and signal CSV after the exact one-line SHA correction, passed **5/5**. Do not reuse the older release ZIP as a byte-current copy of P23. Preserve the historical artifact as a historical snapshot and distinguish it from the corrected source. No claim that the older source PDF was forged or different without independently obtaining those bytes.

## 5. Internal adversarial assessment

- **Geometer:** UTM conversion and reference-line evaluation PASS; nearest distances are candidates only.
- **Traffic engineer:** `type=294, dynamic=no` means *static stopline features in standard convention*, NOT the observed 1–30 active heads. Assignment HOLD.
- **Empirical auditor:** Published 1-s route counters depend on detected trajectories and changing column presence. Stopline event time is interval-censored, not exact. Independent trajectory cross-check still required.
- **Reproducibility skeptic:** Source files and current-main code must match bytes; an uncorrected P23 historical ZIP would be a false provenance source.
- **Research lead:** R&E physical traffic research retains top priority; RF physical sensor discrimination and predecision policy-value stay separate parallel workstreams.

These are explicitly self-adversarial roles; **not independent people or external LLM calls**. The result is a scientifically useful **negative constraint** on false controller mapping and a reproducible geometry candidate artifact, not a completed model of traffic throughput.

## 6. Verification

[Source-locked P24 geometry and candidate generator](p24_xodr_static_signal_audit.py), blob `abbc47e9b735c24266add10020ab33113f5f2f7f`; [nine actual-input unit tests](test_p24_xodr_static_signal_audit.py), blob `0b0af2215f2c01c2e95a3c7be996032570ba5890`. Both were exported **as exact `main` code**, reconstructed via an auditable Google Docs transport receipt, and verified using `git hash-object`. **9/9 tests passed** against the actual SHA-matched original map and PDF, including negative-input and geometric consistency checks.

Full geometry result JSON SHA256 `dd9edd1b714a3f43d65740cbb54037d30e85a8e56235063911113030e879dea5`; exact-source test log SHA256 `353d2e0d1be2dc77a8fd44c3f37c2348aaf9eb026d69a08600d61af7d34de857`. Original licensed source PDF and XODR map are kept on Drive, not duplicated as GitHub code.
