# T2 v4.6 — Factorial ablation of feasible signals, switch loss and within-tick movement

2026-11-02 local executed code `/mnt/data/t2_v46/ablation.py`, six unittest pass. 48 worlds × (5+5+3+3+9+9+7+7) = **2304 runs**, each 80 time steps. Parametrization storage 2/4/8/16, main arrival 1/2/3 per tick and 3 side origin streams at side rate 0/1/2/3 per tick. 8-step global cycle; cycle lost ticks 0/2; positive-green requirement on/off; snapshot movement on/off. Source SHA256 bf0ce7f1fe1f2b0af540ae05c8a4219fadc3d10c9a95528cb8d569c6541db205. ZIP SHA256 0b8227e9b06cd49b9ad98c53ec9ae6701e284672db3e4078374013f2777ecb7b.

Observation key: baseline global main-green split=3, aggregate network exits only. Compare worlds with same finite storage capacity and main arrival but different side demand, identical observed baseline exit count, and disjoint optimal green-split sets. Across all 8 ablation groups, **36 equal-observation pairs per group, zero disjoint-optimum pairs**.

Ablation conditions (min-green required / lost / snapshot / runs):
- yes,0,no 240; yes,0,yes 240
- yes,2,no 144; yes,2,yes 144
- no,0,no 432; no,0,yes 432
- no,2,no 336; no,2,yes 336.

**Scientific limitation:** this is NOT an isolated causal decomposition of why v4.4 differed from v4.5. v4.4 used a 5-tick period, a zero-green side baseline and different movement ordering, while this sweep uses a new shared 8-tick family and baseline split 3. Factorial comparisons are within v4.6 only. A negative result in the chosen parameter grid does NOT establish policy identifiability. Models remain unrealistic: no actual approach signal phases independently timed, turn conflict, pedestrian calls, origin-destination graph, calibrated micro vehicle dynamics, or Gyeongnam field data. Full implementation + CSV+JSON reproducible in zipped sandbox artifact rather than GitHub executable source (source sync outstanding).

Next hypothesis tests: (a) replicate exact historical v4.4 branch and vary one parameter at a time preserving original semantics, (b) look for distinct near-equal calibration worlds under noisy vector observations rather than exact equal completion, (c) validate under genuinely feasible independent junction phases and OD objectives, (d) field model calibration on independent days and microscopic SUMO comparison.