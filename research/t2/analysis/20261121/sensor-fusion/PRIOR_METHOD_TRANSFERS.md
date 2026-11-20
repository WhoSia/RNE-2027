# 2026-11-21 | Prior methods to REUSE, not discard
Status: METHOD TRANSFER (not a reproduction of the authors' source code)

## Long, Li, Lei & Wang (2026) — forecast-to-decision value
[Authenticated preprint, arXiv:2610.06992v1](https://drive.google.com/file/d/1xfbbwXdee0_wGBWxpEb-3uM_BdZB5FvL/view).
**Take:** audit chronological availability, action support, objective mismatch, and the difference between oracle gain and forecast-conditioned gain. We operationalize the **value-of-decision** objective with a fixed action set and a nonnegative regret loss. We do not borrow their model outputs or claim to reproduce their 29-day Xuancheng experiments.

## Huang, Huang, Zhou & Cheng (2025) — coupled lane and signal optimization
[Authenticated article, DOI:10.1080/21680566.2025.2474656](https://drive.google.com/file/d/1vq5kKhQmejR1KgwDiH-wdjtdhLxXUYot/view).
**Take:** treat lane allocation/admissibility as a distinct decision layer from signal timing. Our existing two simulator bypass modes are merely frozen synthetic **structural scenarios**. We use the separation as an analysis tool; we do NOT reproduce Huang et al.'s upper-layer MILP, lower-layer MIQP, iterative solver or dynamic lane switching controller. Their 19.08% result is not a T2 improvement claim.

## Shafik & Rakha (2025) — turning and queue state fusion
[Authenticated Sensors 25(3),830 article, DOI:10.3390/s25030830](https://drive.google.com/file/d/1LJpiI0hENPuBmWadMgIbUP9Fp_rqZAum/view).
**Take:** separate observables from their uncertainty and combine sources that measure different traffic states. The paper's first-stage turning-flow estimator and second-stage density/queue estimator are concrete paths to future model inputs. Our current binary mode report and categorical arrival report are **NOT** their two-stage adaptive Kalman filter, are not calibrated to probe penetration, and have no measured reliability.

## Mechanical and information bridges
[Zhang & Tong (2008)](https://doi.org/10.3141/2071-09) and [Hidas (2005)](https://doi.org/10.1016/j.trc.2004.12.003) provide older pocket blockage / lane-change mechanism comparators. Use their definitions to evaluate physical admissibility before interpreting any information value.
**Synthesis:** geometry/allowed movement (Huang) → state estimation and uncertainty (Shafik/Rakha) → action/forecast interface and realized loss (Long). This is a plan to incorporate and test **established** science, not a novelty rejection list.

## Transfer status at the end of SF-01 (2026-11-21)
- Long audit is implemented as the precommitment/provenance/late-report gate and same-world action regret comparator in `sensor_cost_policy.py`.
- Huang's **separation** is implemented as frozen structural scenario classes vs two phase-order actions. Dynamic lane-assignment MILP and switching penalties are not yet implemented.
- Shafik/Rakha's **two-stage structure** is now adapted in `two_stage_queue_estimator.py`: scalar probe-based turn-fraction Kalman update feeds a count-based queue predictor, which is optionally corrected by an independent noisy queue reading. This is neither their full adaptive Kalman system nor a calibrated sensor, and it is intentionally kept separate from the 16-world information model until capture-time and uncertainty contracts can be linked.
- Hidas (2005): verified DOI **10.1016/j.trc.2004.12.003**. Its observed merging/weaving and forced/cooperative changes can inform the next physically constrained simulator, but are **not** encoded into the present 7-m discrete cell model.
