# Source-to-code transfer contract — T2 + RF-CURTAIN (2026-11-21)

## Position: reconstruct old scientific methods BEFORE claiming originality

A paper citation is not itself an implementation. Each transfer must have
**source page/equation/table**, input/output domain, units, observation time,
code entry point, independent test, reproduction status, and field applicability.
Only mark `REPRODUCED_ORIGINAL` if the paper's own described algorithm
and published test/benchmark have actually been replicated. A meaningful
simplification is allowed and often useful, but name it `SIMPLIFIED_ANALOGUE`.

## Source-to-code mapping as currently evidenced

| Paper / native Drive original | Exact transfer target | GitHub location | Current state / essential missing evidence |
|---|---|---|---|
| Wu et al. (2024), 10.1080/21680566.2024.2363273 | `Rl,Rt` state 0 none,1 spillback-no-block,2 active block; 10 types in original Table 1; **independently verify** actual phase/demand/discharge when calling physical blockade | `rf_observation_identifiability.py` models *our five* toy causes only | **NEW ANALYTIC ANALOGUE**, not Wu's LPR classifier. Need inspect Table1 types and reproduce author labels only with actual lane queue/discharge data |
| Qi et al. (2020), 10.1016/j.trc.2020.102824 | Partial CV track→piecewise simplified trajectory likelihood/objective→triggering movement + duration, with true turning labels | No paper-specific exact Qi estimator | **NOT_IMPLEMENTED**; RF occupancy alone lacks the required trajectory |
| Shafik & Rakha (2025), 10.3390/s25030830 | First-stage adaptive Kalman turn fraction/flow; second-stage independent queue and density posterior, with covariance and missing-sensor handling | `research/t2/efficiency_loop/two_stage_queue_estimator.py` (check exact path in Git before importing) | **SIMPLIFIED_ANALOGUE**; paper's complete adaptation, noise models and benchmarks NOT reproduced |
| Long et al. (2026), arXiv 2610.06992v1 | Decision-time causal availability, oracle boundary, action set, paired loss and regret | `research/t2/analysis/20261121/sensor-fusion/PRIOR_METHOD_TRANSFERS.md`, related SF-01 code | **METHOD AUDIT TRANSFER**; not authors' Xuancheng case nor field validation |
| Huang et al. (2025), 10.1080/21680566.2025.2474656 | Physical lane assignment layer vs signal policy layer, constraints | T2 dual-lane & SF-01 structural modes | **CONCEPT TRANSFER**, NOT paper MILP/MIQP replicated |
| Hidas (2005), 10.1016/j.trc.2004.12.003 | Free/forced/cooperative lane change with data-backed following gap | `dual_lane_v11.py` has idealized 1/2/3 eligible-tick count | **NOT_HIDAS_IMPLEMENTATION**; cannot call duration a measured human reaction time |
| Emtenan & Day (2021), 10.1177/03611981211017139 | Throughput loss vs turning share / storage / cycle length; real calibration and fixed demand needed | PHYS01–11 synthetic runs | **QUALITATIVE MODEL COMPARISON**; no original capacity function calibration |
| Guo et al. (2026), 10.3390/su18179194 | Bayesian upstream observation boundary posterior and heldout action-effect test | T2 near-support distance ablation, RF geometry | **NOT_BAYESIAN_BOUNDARY_REPRODUCTION** |
| Tan et al. (2025) / Tan et al. (2026) | Explicit distribution/ambiguity sets and decision regret | T2 OOD heuristic & theoretical audits | **CONCEPT TRANSFER ONLY**, not robust MILP / Wasserstein DRMP |
| WiTraffic (2017) / DeepWiTraffic (2019) | Real CSI acquisition, subcarrier/time features, vehicle truth and layout holdout | RF-CURTAIN `rf_pilot_evaluator.py` | **EVALUATION SOFTWARE ONLY**; no Wi-Fi CSI, no actual original hardware results |
| Zhu et al. (2024) / Guarino et al. (2026) | Multisession/domain-shift reproducibility, chipset/tool metadata, packet capture rate, raw CSI and code licensing | `PILOT_PREREG.md`, `DATA_CONTRACT.md` | **PROTOCOL DESIGN**, not physical measurements or original dataset |

## New first executable mathematical check

`research/t2/exhibition/rf_curtain/rf_observation_identifiability.py`
and `test_rf_observation_identifiability.py`.

Fix exactly FIVE user-defined toy worlds:
`no_demand, free, pocket, downstream, both`.

Observe PERFECT Boolean presence at a pocket barrier (P) and at a
downstream boundary (D). The two worlds `no_demand` and `free`
both have `P=D=False`, so the five labels partition into 4 signatures
with only **3 labels uniquely identifiable**. An additional PERFECT
independently obtained *approach demand* bit (A) splits that alias
and gives 5 unique signatures. One lone P or D bit uniquely labels
none of the five worlds.

This is exactly and only an **instantaneous static occupancy model**.
Real Wi-Fi CSI may carry motion/temporal content and may discriminate
free flow vs absence; this analysis does NOT establish the need for
another hardware sensor, superiority of Wi-Fi, or a spatial RF footprint.
A contradictory reading P=True/A=False gives empty compatible set
and MUST produce `OUTSIDE_DEFINED_MODEL`, not a fabricated label.
`None` means unavailable; it is not coerced to False.
All 9 targeted Python tests passed on the GitHub-blob-identical
source in Python 3.13. Source SHA-1:
`694913f4a00783214379be51464bce2f022775e4`;
test SHA-1: `101a213915b8cbd3dffa13246435ecd2722d3b50`.
Generated uncalibrated JSON SHA-256
`bbdf15578bd46dd13029528ca294469001c5f3cd1d9b111841845d06e13cfd77`.

This is a faithful **mathematical comparison of measurement designs**,
not a reproduction of Wu2024's empirical 10-type classifier.
The user defined a five-class tabletop prototype in RF01; that
label ontology cannot inherit the source paper's field accuracy.

## Next step, deliberately not rushed

- Obtain and read the full WiTraffic, DeepWiTraffic, 2025 ESP32
  CSI traffic, Zhu2024 and Guarino2026 originals and check equations,
  setup, hardware API and published comparison splits.
- Determine whether ordinary stationary metal model cars produce a
  repeatable CSI feature under available school-owned, consented gear.
  If no owned CSI exposure, label the physical experiment BLOCKED.
- Only after independent recorded CSI exists reproduce baseline features
  and run session/placement holdout. No sensor values invented by the
  traffic simulator may be called RF data.
- Keep previous traffic physics simulations and K047 sealed field
  observations as a **separate T track**.

## 2026-11-21 추가 전수 정정 및 원문 수학 구현 감사

- **원문 보유 판정 선행:** RF literature ledger 상단 CURRENT 정정표를 먼저 참조한다. 최초의 구 B절에서 미보유로 분류된 RF 후보 12편 중 9편이 10_PAPERS의 실제 PDF로 보유 확인되었다. 이전의 '원문 확보 전' 판정을 반복하지 않는다.
- **Won, Zhang & Son (2017), WiTraffic, DOI 10.1109/ICCCN.2017.8038380.** 원문 PDF [1hMMeALKst2WyQUGAw0EorCZG6ddSkdK4](https://drive.google.com/file/d/1hMMeALKst2WyQUGAw0EorCZG6ddSkdK4/view). Original: vehicle CSI distributions from each trained lane, EMD-based lane dissimilarity, alongside separate vehicle and speed methods. Code [witraffic_emd_baseline.py](../../../exhibition/rf_curtain/witraffic_emd_baseline.py) implements **only exact normalized 1D discrete histogram transport** via |CDF difference| integrated over ordered bins. **Status SIMPLIFIED_MATH_ANALOGUE**; original CSI preprocessing, multivariate ground metric, training data, actual lane accuracy/speed method and evaluation **NOT REPRODUCED**. Test [test_witraffic_emd_baseline.py](../../../exhibition/rf_curtain/test_witraffic_emd_baseline.py) checks normalization, units, triangle inequality, input boundary and ties; no radio acquisition claimed.
- **Won, Sahu & Park (2019), DeepWiTraffic, DOI 10.1109/MASS.2019.00062.** 원문 PDF [1RSuuT9VlXv_KHIYf1u1HVOBlnmqhPqLC](https://drive.google.com/file/d/1RSuuT9VlXv_KHIYf1u1HVOBlnmqhPqLC/view). Original: CSI amplitude low-pass filtering, 30-subcarrier PCA dimension reduction, phase linear transformation, vehicle segmentation and CNN classification with video truth, month-scale rural road. **Status ORIGINAL_READ_PARTIALLY / NOT_IMPLEMENTED**; RF pilot centroid classifier is not the paper CNN.
- **Shahid et al. (2025), IEEE QPAIN, ESP32-Based Wi-Fi CSI Traffic Monitoring.** Original [1w2zgRKFFuWl3CsPBec7xHQkqi_7eNIcc](https://drive.google.com/file/d/1w2zgRKFFuWl3CsPBec7xHQkqi_7eNIcc/view). Its extracted Table I Leguna-type P=.67, R=.57, F1=.24 conflicts with F1=2PR/(P+R)≈.615968. Code [published_metric_consistency.py](../../../exhibition/rf_curtain/published_metric_consistency.py) performs arithmetic-only audit, **not** correction of original study or performance replication. Before public citation inspect the original Table I page visually and distinguish table, PDF extraction and typographical error.
- **Guarino et al. (2026), Computer Communications, DOI 10.1016/j.comcom.2026.108431.** Original [1_p2Y2BrDnuxoTIeUc9a8OZuCNKA_0Fcj](https://drive.google.com/file/d/1_p2Y2BrDnuxoTIeUc9a8OZuCNKA_0Fcj/view). Reproducible CSI requires device/chip metadata, actual data access, preprocessing details, session/position split and evaluator code. Our [rf_pilot_evaluator.py](../../../exhibition/rf_curtain/rf_pilot_evaluator.py) has **METHOD-LEVEL INSPIRED EVALUATION CONTRACT**, not replication of review's benchmarks.

**Missing original vs missing method distinction:** paper original on Drive is held even if data/weights/raw CSI and complete algorithm are not; a held PDF ≠ independently reproduced method. A public OA DOI ≠ stored Drive original. Preserve publisher/repository licensing; do not copy PDFs into GitHub.

## RF04 — new originals and exact upstream-code difference (2026-11-21)

**00_INTAKE now contains only the SHA-pending WiCross duplicate-hold folder; seven PDF originals moved with original IDs into 10_PAPERS.** Full [seven-source receipt](../../../exhibition/rf_curtain/RF04_INTAKE_00_LITERATURE_RECEIPT_20261121.md).

| Paper/source | Implementation transfer | Status |
|---|---|---|
| Brunello et al. 2025, DOI 10.1016/j.iot.2025.101634, Drive ID 1uR6NjkYfs3EQDrxx9zWk8FOXDgXLs1nX | Require held-out physical collection day and mounting layout because static CSI fingerprints may drift | EVALUATION_DESIGN_TRANSFER, no original experiment replay |
| Khamaisi et al. 2026, OpenCSI arXiv 2607.26665v2, Drive ID 1rqlZxB_wmDxYrpF6o28KeLJwE17qcSyw | Source idea quiet-mean Welford and z=abs(amplitude-mu)/sigma; mathematical tests for gain/noise/contamination/drift | **SIMPLIFIED_MATH_ANALOGUE** in [open_csi_quiet_calibration_analogue.py](../../../exhibition/rf_curtain/open_csi_quiet_calibration_analogue.py), not the full published library or source test/data |
| Euchner & ten Brink 2024, ESPARGOS arXiv 2408.16377v1, Drive ID 1QWrotEVB9RqUASamY-XJfeG7M44dzBAk | Timestamp, position and phase calibration metadata / multi-antenna comparison reference | ORIGINAL_READ_SELECTED_METHODS, hardware/data NOT_IMPLEMENTED |
| Zubow et al. 2024, SensingWall, Drive ID 1Lq0RtZxFSH6p4rph0e1uqQStJyDoclKG | Centralized multi-ESP32 CSI acquisition and visualization | ORIGINAL_READ_SELECTED_METHODS, hardware NOT_IMPLEMENTED |
| Armenta-Garcia et al. 2025, Sensors 25:6220, Drive ID 16y4Zm_yBHdNDg7VDEHjuSax1jjGZAdr_ | CSI acquisition and edge HAR reference; their EMD is *Empirical Mode Decomposition*, not Earth Mover's Distance | NOT_IMPLEMENTED, TASK_NOT_VEHICLE |
| Chen et al. 2026, Electronics 15:585, Drive ID 1CPMGt6oiVAn7blhlI7N1wq3C2WeMy4OF | LiDAR point-cloud preprocessing and complete/partial occlusion correction | NOT_IMPLEMENTED, distinct sensor modality |

**Upstream author implementation checked, not executed:** [sensing-group/OpenCSI](https://github.com/sensing-group/OpenCSI), Apache-2.0 as displayed by upstream README. Exact upstream files [Welford](https://github.com/sensing-group/OpenCSI/blob/main/src/opencsi/core/welford.py) blob `d79ed61294619922d2b74cf7da2c87a7739a7cfb`, [calibrator](https://github.com/sensing-group/OpenCSI/blob/main/src/opencsi/core/calibrator.py) blob `472ccd548a51e993a79869dcd4997197783f6677`, and [baseline](https://github.com/sensing-group/OpenCSI/blob/main/src/opencsi/core/baseline.py) blob `5c70d65a981906658c3408253915e1a6ab37f1e8`. Upstream baseline defines **MIN_SAMPLES_FOR_BASELINE=10**, **MIN_STD_THRESHOLD=0.1** and timestamp-based staleness checks; our **toy** defaults are min_samples=3, sigma_floor=1e-9 solely to exercise tiny preregistered arithmetic fixtures and are not production reproduction. Our scalar returns no physical lane, cause, phase or maturity/quality estimate. Upstream quiet gate, AGC and phase sanitization, frequency/age reliability, multi-link CSI packets and baseline drift handling are entirely missing. Never compare model F1 to paper data or claim source-code parity.

**New mathematical source/test Git blobs checked against locally run Python 3.13.5:** source `7c788086965a38e2c9e0c29be83b5e2356d12fdd`; tests `bca092a81ecb7a8c7efde5b12a01a979d552cbd8`. RF04 10/10 test methods and earlier RF01/RF02 21/21 passed in one local extraction folder, total RF subset 31/31, **not the full T2 integration suite**. Fixed synthetic math JSON SHA-256 `f95a21f80d4cb0a016aaaaaffea6c92e767bfe22dd27c449e0a6529b4250f65a`; [JSON](../../../exhibition/rf_curtain/rf04_open_csi_math_fixture.json). No CSI files or measured RF samples exist.

**Next actual method-replication gate:** separate device-specific CSI packet schema, actual empty-room calibration time, original baseline/min-floor choices, sanitizer settings, hardware/link orientation and baseline expiry; only then attempt author-library implementation with allowed school equipment. Preserve missing/abstaining frames and cross-day holdout as precommitted. Never promote the 5 scalar examples to detector validation.
