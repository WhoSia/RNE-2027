# RF04 — 00_INTAKE verified, OpenCSI-inspired math gate executed

2026-11-21. **VALIDATION CLASS: SOURCE-LINKED SCALAR MATH + LOCAL UNIT TESTS, NOT CSI SENSING**.

## 1. Literature intake receipt and handoff

- Eight PDF files found in canonical [Research OS 00_INTAKE](https://drive.google.com/drive/folders/1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16).
- Seven distinct additional originals read at first-page/selected-method/conclusion text level, bibliographically normalized and moved to [10_PAPERS](https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP) without replacement. Post-move individual metadata verifies seven unchanged IDs and destination parents. See [source-by-source citation and limits](RF04_INTAKE_00_LITERATURE_RECEIPT_20261121.md).
- The remaining incoming Shi WiCross copy exactly matched canonical extracted full text and file size, but byte SHA is **unverified**; retained in a named SHA-pending duplicate hold. No deletion.
- Existing missing-paper ledger amended: of eight newly proposed candidates, six now verified held; two not located. Earlier three missing candidates remain. No change to their publication existence status.
- Among new PDFs, the critical RF methods are Brunello2025 (temporal generalization), Khamaisi2026/OpenCSI (calibration), ESPARGOS2024 (phase synchrony), SensingWall2024 (ESP32 acquisition), Chen2026 (LiDAR multi-lane queue reference) and Embedded Sensing2025 (hardware/edge HAR). The embedded paper calls **EMD Empirical Mode Decomposition**, unlike WiTraffic2017's Earth Mover's Distance.

## 2. Preregistered experiment and true execution

[Locked prerequisites and six hypotheses](RF04_OPENCSI_MATH_STRESS_PREREG_20261121.md) committed **before** new runner and tests. Test source [open_csi_quiet_calibration_analogue.py](open_csi_quiet_calibration_analogue.py), tests [test_open_csi_quiet_calibration_analogue.py](test_open_csi_quiet_calibration_analogue.py). The single-scalar method computes the sample-variance Welford estimate on **known-quiet synthetic inputs**, then an absolute z-score and a threshold. A missing/unreliable channel abstains; neither 1-link nor 2-link scalar score claims pocket-vs-downstream blockage attribution.

| Locked world | Raw baseline/events | Synthetic z | Outcome at threshold3 |
|---|---|---:|---|
| clean quiet vs event | [9,10,11,10,10] vs13 | 4.242640687119285 | deviation flagged |
| affine gain a=2,b=7 | all above values jointly transformed | 4.242640687119285 | exact numeric agreement |
| doubled quiet spread | [8,10,12,10,10] vs13 | 2.1213203435596424 | deviation not flagged |
| **wrongly known-empty** | [12,13,14,13,13] vs13 | 0 | occupied-bootstrap failure |
| quiet environment drift | original quiet vs14 | 5.65685424949238 | false-event-like deviation |
| constant quiet, zero variance | [10,10,10,10,10] vs13 | undefined | **ABSTAIN** |

All are **mathematically arranged numerical inputs**, not observed CSI time series and not estimates of false-alarm rates. The affine invariance result holds only under the explicitly assumed common positive-gain linear transform on *both* baseline and measured event. The toy bootstrap-contamination result proves an assumption failure within this scalar design, not a measured failure of the authors' full OpenCSI library.

## 3. Checkable receipts

- Execution runtime: local Python **3.13.5**.
- Fresh RF04 tests: **10/10** pass; existing RF01/RF02 tests: **21/21** pass; combined local RF-subset run: **31/31** pass. Whole T2 historical test suite NOT run in this unit.
- Local exact source blob SHA: `7c788086965a38e2c9e0c29be83b5e2356d12fdd`; GitHub fetched main blob **same**.
- Local exact test blob SHA: `bca092a81ecb7a8c7efde5b12a01a979d552cbd8`; GitHub fetched main blob **same**.
- Deterministic JSON [rf04_open_csi_math_fixture.json](rf04_open_csi_math_fixture.json), local SHA256 `f95a21f80d4cb0a016aaaaaffea6c92e767bfe22dd27c449e0a6529b4250f65a`; local Git blob `4a5e7d5c86d7c77df2b9b3abc2d7805cfa5efd72` exactly matches GitHub blob.
- Original publicly released author code examined READ-ONLY: [sensing-group/OpenCSI](https://github.com/sensing-group/OpenCSI); Welford blob `d79ed61294619922d2b74cf7da2c87a7739a7cfb`, author baseline blob `5c70d65a981906658c3408253915e1a6ab37f1e8`. Upstream baseline minimum samples10 and sigma floor0.1 differ from this tiny synthetic toy min3/sigma floor1e-9, so **NOT A SOURCE REPLICATION**. Source data, real CSI measurements and hardware-integration code were not obtained or run.
- No GitHub Actions, no `github-actions[bot]`, no actual traffic signals, no K047 unsealing.

## 4. Research-direction review

**ACCEPT:** source intake quality, algebraic stability under common affine gain, known failure under baseline contamination/drift and conservative software abstention. These are strong *design controls*, not detector performance.

**REJECT:** any inference of source-of-queue blockage from merely two scalar z scores; any transfer of LiDAR 99.3%, ESP32 HAR or OpenCSI binary occupancy metrics to a five-class traffic model; any claim of traffic-light safety or useful action from synthetic CSI.

**HIGH-PRIORITY NEXT:** physical acquisition contract and independent held-out lab CSI data under consented and school-approved equipment. Distinguish cross-day-only from cross-position-only and joint shifts: the existing RF pilot evaluator has a *joint* P2/S3 holdout, which cannot attribute failures separately to time vs physical placement. Before next physical collection, **preregister a crossed holdout matrix** and confirm that each trial is independently reset. Link the real measured sensor-error matrix to T2 decision-value comparisons only after this gate.

**STATUS:** RF04_MATH_COMPLETE / RF04_RADIO_NOT_EXECUTED / FULL_REPO_INTEGRATION_OPEN.
