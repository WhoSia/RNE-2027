# T2 P21 — Signal-code runs, low-speed observations, and INTERACTION original custody

Date: 2026-11-22 KST. **Real DLR-UT observational data timing analysis completed; INTERACTION originals not yet accessible for an actual file move.**

## 1. INTERACTION archives: inbound custody
The user reports downloading both `INTERACTION-Dataset-TC-v1_0.zip` and `INTERACTION-Dataset-DR-v1_1.rar` onto a local device. A Google Drive filename search for both exact names and the `INTERACTION` substring, plus a current conversation mounted-file inspection, did **not** locate either archive. Downloading to a private desktop cannot automatically expose files to a cloud connector.

Created destination folder, under the established immutable observations lake:
[02_DATASETS/20_OBSERVED — International/INTERACTION_v1 — publisher originals (TC_DR)](https://drive.google.com/drive/folders/1k-EEwOyBgUVoQaGwQsModGfmP92w0Gzv), ID `1k-EEwOyBgUVoQaGwQsModGfmP92w0Gzv`, parent `1jPPgcsrlStDzDn907gO1BVAUJh-0a2Du`. This **does not mean either original was uploaded, moved, hashed or inspected**.

Inbound gate: user uploads the original archive files **without extracting or renaming** into that folder, or otherwise supplies an accessible provider file ID. Preserve raw bytes and upstream names; then independently verify Drive parents, sizes, provider-owned file IDs, SHA256 and archive listings (after license gate). Distinguish raw input from derived CSV and never copy original ZIP/RAR into the GitHub source repository.

Hugging Face upstream [INTERACTION dataset repository](https://huggingface.co/datasets/INTERACTION-dataset/INTERACTION-dataset), metadata identifies Creative Commons Attribution 4.0; verify the actual downloaded file release and included LICENSE before publication. The TC camera intersection data and DR drone trajectory data are distinct acquisitions, not JSON/XML/CSV format duplicates.

## 2. Development: DLR signal-code run and low-speed audit
[Implementation](p21_dlr_segment_gate.py), [regression tests](test_p21_dlr_segment_gate.py), [machine-readable manifest](P21_DLR_SIGNAL_RUNS_AND_INTERACTION_CUSTODY_20261122.json).

The two already-held DLR-UT v1.3.1 source CSVs were re-read from Google Drive, their exact SHA256 matched, and the algorithm segmented time-sorted readings of 30 signal IDs by unchanged **integer state code**. Boundary runs are explicitly censored; observed within-run span is a sample-based *lower bound* and **not an exact green duration**. A different analysis checks consecutive tracked-object readings with both speeds <=0.5 m/s, only across time gaps <=0.2s; it is **not** a stopline, traffic queue, phase-response or intervention-effect estimator.

Measured from the 2023-09-24 23:30–23:45 UTC observation window:
- Trajectory objects: **37**, modal object classifications: car22, truck6, van3, bicycle4, motorbike1, pedestrian1.
- Signal IDs: **30**; code changes across IDs: **869**; uninterrupted code runs: **899**. The 899 follows from 30 initial runs plus 869 changes.
- Among 37 objects, **4 IDs** have at least one pair of adjacent recorded speeds <=0.5 m/s; **1,901 adjacent low-speed intervals** totaling **95.05 sampled seconds**. This is not 1,901 separate stopping vehicles nor the summed durations of distinct queuing episodes.
- No trajectory gaps >0.2s within tracked IDs in this 15-minute window.
- Numeric state codes remain unknown. Neither mapping to green/yellow/red nor a controlling signal-head/stopline correspondence has been established. Do not infer signal timing safety or claim headway calibration.

The `main` implementation blob `ab7b17dfc0ee9d4a690a550353de99b13fb216a0` and test blob `5b264851fc9c5bbed261f9c0ec5d775667ffdc19` were recovered as **exact bytes** through a read-only transfer and confirmed with local `git hash-object` before running. **8/8 regression tests passed**, including actual Drive CSV checksum/row census, mixed ISO timestamps, missing timezone rejection, right-censored runs, duplicate samples, gap discontinuities, and no false stopline claims.

Complete 899-run output JSON SHA256 `640915f04d97d8e60c689efbec98631e6f7121452e89dc9921b83d3374f76465`; verbose test-log SHA256 `d9a6605fe35e78b32079b999429dca76287c3a29cb1271d164bb842235bfbffb`. These files are in the current session's container and should be preserved in a local reproduction bundle, not falsely presented as already uploaded to Google Drive.

## 3. Scientific gates and research direction
Immediate priority remains obtaining the **official DLR-UT signal codebook and map/geometry**, validating which signal ID governs a candidate stopline, and extracting per-vehicle crossings with a frozen interpolation/time-tolerance contract. Without those steps, a plot of 899 code runs cannot validate T2/P19 simulated signal discharge or SUMO. Once INTERACTION originals are actually present, inspect TC/DR contents independently for trajectory time/coordinate systems and intersection map representations. INTERACTION lacks an independently confirmed aligned real SPaT time tape in this session; do not infer it from trajectory filenames.

**Custody:** GitHub `main` only; no GitHub Actions/bot; original source dataset bytes intact; CIM ~5GB HOLD untouched; K047 sealed; no live road controller or unauthorized RF collection.
