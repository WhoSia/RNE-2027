# 2026-11-13 — T2 Exhibition Site Data Gate

Exhibition-first: no novelty requirement for already-known traffic engineering phenomena; direct observation, reproducible student inquiry and a feasible traffic signal improvement matter.

## Real-source verification (not field-policy effectiveness)

Existing **DLR-UT v1.3.1** original Drive folders were examined for traffic-volume, traffic-light and vehicle-trajectory CSV blocks, 4 XOSC files, and an OpenDRIVE map. CSV **content** of 2023-09-24 UTC 12:00–13:00 four volume and four traffic-light blocks was read and summarized. K047 Braunschweig original OpenDRIVE was parsed locally. From 12:00–12:45 publisher-derived movement counts = 436 + 475 + 498 = 1,409, matching prior D42 report. Additional 12:45–13:00 has 450; this is a **same-day temporal holdout**, not a different-date independent replicate.

Each of the four 12:00–13:00 volume blocks has 900 one-second records, but those **sampled midday blocks** have different movement-column schemas (32/27/26/28) and thus requires **schema union, not blind omission-to-zero**. Signal blocks: 30 heads at 897/899/895/898 sampling instants, respectively. Flooring timestamps causes artificial duplicate second bins (51/52/57/60). Rounding to nearest second removes these collisions in first three blocks, but there remains 1 nearest-second collision in the fourth block. No signal color interpretations or traffic movement mappings certified.

OpenDRIVE XML: 28 road elements, 1 junction, 16 connections, 123 lane sections, 1,005 lane nodes, 7 road signal elements. The seven map objects are not a validated mapping to the **30 signal-head IDs**. Source road map version attribute 1.0.0 differs from DLR archive dataset package version 1.3.1; do not conflate.

## Candidate ranking

A. DLR K047 — immediate observation-validation; raw local copies in Drive, needs stopline/head-movement alignment and independent queue annotation.
B. Seoul smart intersections — domestic applicability and 5-minute movement data officially cataloged; actual raw traffic CSV, signal join and physical geometry not yet ingested. Official T-Data notice says old C-ITS signal APIs cease **2026-11-15**; use official replacement history/API, not sunset client code.
C. CityArtery, Dongguan — official dataset describes 14,490 trajectories along a ~1km corridor with 2–3 signalized intersections plus signal timing records; raw bytes unverified this pass.
D. INTERACTION — tracks + HD maps exist, but timed traffic signals not confirmed.

## Reproduction

Runnable standard-library audit source and 6 passing tests preserved in project ZIP/Drive evidence. The audit requires original DLR 15-minute CSV files on local disk; this GitHub folder holds **derived evidence and source pointers only**, not proprietary copies or invented field observations. Source links:
- https://zenodo.org/records/20919480
- https://t-data.seoul.go.kr/
- https://www.data.go.kr/data/15166094/fileData.do
- https://data.mendeley.com/datasets/ftzzmh2cmt/1

**Do not** claim SUMO execution, standalone validation, field-calibrated traffic control or improved real-world timing. Hold policy improvement until observed and modeled queue/flow match on unseen observations.

## 2026-11-13 source correction and release

See `DLR_PARTIAL_WINDOW_GATE.md`: an additional **23:30–23:45 UTC** DLR volume CSV has only **893 contiguous observed one-second rows** (starts 23:30:07), compared with 899 signal instants and 8,624 trajectory rows. The audit code was amended to flag partial observed windows rather than incorrectly reject them or zero-impute. **9 local unit tests** passed, including duplicate signal heads and unordered timestamps.

File-existence inventory across 96 matched 15-minute windows per type: 2,621,708,178 trajectory bytes, 97,168,311 signal bytes, 6,005,890 volume bytes. Existence does **not** imply full 900-record completeness in every window.

Final V3 source/test/derived-evidence ZIP (Drive): https://drive.google.com/file/d/1w2m7XFVTUmHIMn3IIWbv5u6v0ufn6TGA/view
V3 SHA-256: `5ca9d84b3945614a1d9150808dc7f91cbabf4040909b48bb62944c3d14c1ab89`.
The 18:00–18:30 UTC raw contents remain prospectively reserved; do not inspect them until rules are frozen.

Active acquisition and validation gates: [DLR G1](https://github.com/WhoSia/RNE-2027/issues/2), [Seoul G2](https://github.com/WhoSia/RNE-2027/issues/3), [CityArtery G3](https://github.com/WhoSia/RNE-2027/issues/4).
