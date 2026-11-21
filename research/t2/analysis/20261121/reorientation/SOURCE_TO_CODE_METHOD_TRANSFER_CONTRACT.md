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
