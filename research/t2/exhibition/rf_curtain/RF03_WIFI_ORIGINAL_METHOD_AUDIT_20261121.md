# RF03 — Original Wi-Fi traffic papers inspected and first numerical method transfer

2026-11-21. Status: **HELD_PDF_READ / PARTIAL_MATHEMATICAL_ANALOGUE / NO_RADIO_DATA**.

## Exact held original files

- Won, Zhang & Son (2017), *WiTraffic*. Drive PDF [1hMMeALKst2WyQUGAw0EorCZG6ddSkdK4](https://drive.google.com/file/d/1hMMeALKst2WyQUGAw0EorCZG6ddSkdK4/view). Full extracted original includes CSI histogram comparison with Earth Mover's Distance for lane classification, plus vehicle classification and speed estimation. Paper reports field experimental numbers, which belong to the original authors; we have NOT reproduced them.
- Won, Sahu & Park (2019), *DeepWiTraffic*. Drive PDF [1RSuuT9VlXv_KHIYf1u1HVOBlnmqhPqLC](https://drive.google.com/file/d/1RSuuT9VlXv_KHIYf1u1HVOBlnmqhPqLC/view). The methods include low-pass filtering, PCA on 30 subcarriers and transformed phase data, with a CNN for five vehicle types and labeled video. **NOT_IMPLEMENTED**. A static simulated toy car and a moving car on a rural road are not equivalent.
- Shahid et al. (2025), ESP32-based Wi-Fi CSI traffic monitoring. Drive PDF [1w2zgRKFFuWl3CsPBec7xHQkqi_7eNIcc](https://drive.google.com/file/d/1w2zgRKFFuWl3CsPBec7xHQkqi_7eNIcc/view). Bi-LSTM Table I extracted row `Leguna-type precision=.67 recall=.57 F1=.24` has F1 arithmetic inconsistency. Harmonic F1 implied by precision/recall is **0.6159677419354839**, discrepancy **0.3759677419354839**. This may be a reporting/formatting/printing issue; do NOT alter the original, infer which entry is wrong or call the paper invalid without visual comparison against the original PDF table and full training protocol.
- Zhu et al. (2024) [1L7fKfFvdlikH_BHE-FwHls3gPWRkp0t4](https://drive.google.com/file/d/1L7fKfFvdlikH_BHE-FwHls3gPWRkp0t4/view) and Guarino et al. (2026) [1_p2Y2BrDnuxoTIeUc9a8OZuCNKA_0Fcj](https://drive.google.com/file/d/1_p2Y2BrDnuxoTIeUc9a8OZuCNKA_0Fcj/view) describe device/software, cross-environment testing and reproducibility; these are prior-art **evaluation** guides, not hardware validation.

## Delivered code (not a CSI signal generator)

`witraffic_emd_baseline.py`: normalizes ordered **one-dimensional** histogram mass and computes exact 1-Wasserstein distance through cumulative mass imbalances, with supplied bin-center units. This is an auditable mathematical analogue of the EMD distribution-comparison idea in WiTraffic. Original multidimensional CSI feature extraction, distance ground cost, tuning, data, numeric detection and lane benchmarks are NOT reproduced.

`test_witraffic_emd_baseline.py`: committed deterministic tests for identity/scale, symmetry, triangle inequality, invalid inputs and tie behavior. These tests are **COMMITTED / execution verification not asserted in this receipt**. A separate mathematical sanity check found normalized input histograms [2,1,1] and [0,1,3] produce EMD=1.0, not 1.25; an initially mistaken expected value was repaired in a distinct GitHub commit.

`published_metric_consistency.py` and its test: arithmetic-only F1 validation with finite/probability bounds; **NOT training, not a CSI replication**.

## Updated inventory

The original 2026-11-21 *missing RF papers* list had been overtaken by actual paper intake. Full Drive metadata confirmed that **all nine corrected-held PDFs reside in Research OS 10_PAPERS**, and their extracted text was checked. The current status is 9 HELD (two edition-limited), 3 MISSING_EXACT_PDF among the earlier 12, plus eight newly shortlisted MISSING_EXACT_PDF works. See [superseding top-of-file register](../../analysis/20261121/reorientation/T2_RF_LITERATURE_STOCK_AND_MISSING_20261121.md).

## Scientific gates

1. Original CSI crossing events and static blockage detection are **different** data-generating mechanisms.
2. 1D histogram EMD nearest-profile is a baseline, not a calibrated source attribution probability.
3. No RF measurement is available; CSI detector accuracy and robustness are open.
4. Avoid contamination of the unseen placement/session test by feature tuning; missing trials count as abstentions.
5. No road equipment or controller operation, no third-party network capture, K047 sealed and no GitHub Actions/bot use.

Next: verify exact diagrams/table pages in original PDFs, inspect held hardware and obtain consented lab CSI before changing program stage from ANALYTICAL_ONLY.
