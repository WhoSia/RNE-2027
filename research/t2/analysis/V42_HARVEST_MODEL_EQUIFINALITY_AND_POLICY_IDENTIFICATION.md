# T2 V42 — Research novelty from five directly read papers (2026-11-02)

Five new PDF originals reviewed including title, abstracts, discussion and conclusions, and moved from 00_INTAKE to 10_PAPERS under author-year-title canonical names:
- Ishaque & Noland (2009), DOI 10.1061/(ASCE)0733-947X(2009)135:6(338): joint pedestrian and vehicle validation and travel-time distribution, VISSIM.
- Treiber & Kesting (2013), DOI 10.1016/j.sbspro.2013.05.050: global gap calibration vs local/speed approaches, orthogonality/robustness/completeness, 1 Hz and ~300s under their study conditions.
- Shahdah et al. (2026), DOI 10.3390/su18147025: SUMO heterogeneous Egypt two-way, GA calibrated IDM W99 Krauss, MAPE 8.79/8.94/10.56%, first two difference below estimate of stochastic optimization noise; coefficients may not uniquely identify behavior.
- Erdmann & Wagner (2025), DOI 10.52825/scp.v6i.2638: practical SUMO Krauß implementation differs from idealized theory, collision prevention not a validated safety-outcome model.
- Punzo, Ciuffo & Montanino (2012), DOI 10.3141/2315-02: calibration reliability varies by optimization algorithm, fit objective, performance metric; synthetic known truth and multi-start inspection.

## Core scientific redirection
Problem is not 'more elaborate SUMO gives better numbers' but **whether signal policy can be identified from limited data**. Falsifiable proposed T2 conjecture: two models with near-equal training error for movement counts can prescribe substantively different green split/offset policies; collecting downstream queue or corridor travel-time data may shrink this policy ambiguity. No demonstration yet; distinguish the hypothesis from cited paper results.

## Next controlled research procedure
Create independently computed fluid/movement queue and IDM/SUMO comparator, same OD arrivals and permitted signal action set. Calibrate on day A counts only; retain >=2 indistinguishable fit sets, maximize discrepancy in policy advice. On day B examine predicted vs measured queue envelope and percentile travel times, evaluate whether observable information added actually narrows the intervention range. Include simpler baseline and stop if all fit-equivalent policies agree. This is stronger than optimizer leaderboard.

## Notion Harvest nodes
H01 https://app.notion.com/p/40cef561cf928107b173eb95cad3b698
H02 https://app.notion.com/p/40cef561cf928148a650e52e51f6820a
H03 https://app.notion.com/p/40cef561cf928163ac3ec09d06a4af87
Google Docs https://docs.google.com/document/d/1zaUc5dScw47gwm49UjxGF94dbtxWFa9h7igd6fvlzXU/edit
No claim of novel empirical discovery.