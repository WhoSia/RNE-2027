# RF04 — 2026-11-21 Research OS 00_INTAKE admission and method audit

**Evidence status:** ORIGINAL PDF EXTRACTED TEXT REVIEWED; DRIVE MOVES VERIFIED; NO PHYSICAL RADIO MEASUREMENTS.

Source [00_INTAKE](https://drive.google.com/drive/folders/1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16), destination [10_PAPERS](https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP). Seven original file IDs were preserved, renamed author/year/title and moved; resulting parents individually verified. Source PDF bytes were not edited or deleted. Not a complete visual examination of every figure/equation.

| Newly held original (author year edition) | Original Drive ID | What transfers / cannot transfer |
|---|---|---|
| Chen et al. (2026), Roadside LiDAR Multilane Queue, Electronics 15:585, DOI 10.3390/electronics15030585 | [1CPMGt6oiVAn7blhlI7N1wq3C2WeMy4OF](https://drive.google.com/file/d/1CPMGt6oiVAn7blhlI7N1wq3C2WeMy4OF/view) | Actual intersection point clouds, full/partial occlusion and lane queue; LiDAR comparator, not Wi-Fi RF |
| Armenta-Garcia et al. (2025), Embedded Wi-Fi Sensing, Sensors 25:6220, DOI 10.3390/s25196220 | [16y4Zm_yBHdNDg7VDEHjuSax1jjGZAdr_](https://drive.google.com/file/d/16y4Zm_yBHdNDg7VDEHjuSax1jjGZAdr_/view) | CSI collection/ESP32-S3 human activity, **not vehicle queues**; EMD here = Empirical Mode Decomposition, NOT WiTraffic Earth Mover's Distance |
| Other cross-domain Wi-Fi materials-sensing research paper (2018; out of current traffic sensing scope) | Original Drive ID preserved in 10_PAPERS; no direct external source link in this traffic-specific research note | Method domain does not establish traffic queues, stopped vehicle blockage, or feasible signal actions; excluded from RF-CURTAIN core baselines |
| Brunello et al. (2025), Time Matters: Temporal Generalization, Internet of Things 32:101634, DOI 10.1016/j.iot.2025.101634 | [1uR6NjkYfs3EQDrxx9zWk8FOXDgXLs1nX](https://drive.google.com/file/d/1uR6NjkYfs3EQDrxx9zWk8FOXDgXLs1nX/view) | CSI static-fingerprint drift; independent day/session and placement holdout necessary, not a vehicle study |
| Khamaisi, Sigg & Rodrigues (2026), OpenCSI, arXiv 2607.26665v2 | [1rqlZxB_wmDxYrpF6o28KeLJwE17qcSyw](https://drive.google.com/file/d/1rqlZxB_wmDxYrpF6o28KeLJwE17qcSyw/view) | Empty-room Welford mean/std and dimensionless per-link z=abs(Abar-mu)/sigma, maturity; original claims binary presence, NOT cause attribution |
| Euchner & ten Brink (2024), ESPARGOS, arXiv 2408.16377v1 | [1QWrotEVB9RqUASamY-XJfeG7M44dzBAk](https://drive.google.com/file/d/1QWrotEVB9RqUASamY-XJfeG7M44dzBAk/view) | Phase-synchronous calibrated many-antenna CSI datasets, not interchangeable with cheap uncalibrated ESP32 pair |
| Zubow et al. (2024), SensingWall, short demo paper | [1Lq0RtZxFSH6p4rph0e1uqQStJyDoclKG](https://drive.google.com/file/d/1Lq0RtZxFSH6p4rph0e1uqQStJyDoclKG/view) | ESP32 CSI acquisition and time-series visualization; no evidence for vehicle-queue mechanism discrimination |

**Duplicate candidate, not deleted:** inbound Shi et al. WiCross [1_3_C5I7PgvHx1AhD38DPgojPatJqvq0_](https://drive.google.com/file/d/1_3_C5I7PgvHx1AhD38DPgojPatJqvq0_/view) has exact equal extracted text and the same 1,045,538-byte Google file size as canonical [1MzvUQrq-1GZ2o_e2CoApQyEwOzjwm3xl](https://drive.google.com/file/d/1MzvUQrq-1GZ2o_e2CoApQyEwOzjwm3xl/view). Byte SHA not verified. The inbound copy is preserved in [00_DUPLICATE_CANDIDATES__SHA_PENDING_DO_NOT_DELETE](https://drive.google.com/drive/folders/1xcWYLqJjeK6hSy48WW5sQmA5QFLxnTI6); existing 10_PAPERS canonical stays untouched. 00 root now contains only this candidate-hold folder.

## Research direction gate

- Prefer source-derived CSI acquisition/calibration and independently observed object ground truth; do not substitute perfect binary synthetic occupancy labels for RF readings.
- Report cross-day and changed-antenna-placement generalization, including missing samples and uncertainty; no random packet-wise train/test leakage.
- Report comparison accuracy from LiDAR/ESP32 HAR/OpenCSI ONLY as prior authors' task-specific claims, never our accuracy.
- Source **EMD** collision: WiTraffic (2017) Earth Mover's Distance vs embedded HAR (2025) Empirical Mode Decomposition. Never use a shared EMD algorithm name or implementation.
- Next isolated method study: test quiet-period Welford z-score under positive affine receiver scaling, additive noise, drift, and occupied-calibration failure. Mark the unit SIMPLIFIED_MATH_ANALOGUE, not original OpenCSI author-code replication.
- No hardware acquired; no live road work; K047 holdout sealed; no GitHub Actions or bot contributions.
