# T2-SF-01 | Exact action-loss constraints, numerical optimizer
With world Δ=C_left−C_through and left-choice probability p, regret is max(−Δ,0)+Δp. For each report r, optimize p_r∈[0,1] with worst-case epigraph t≥0.

Given world w, emission law P(r|w, qm,qa), require
t ≥ max(−Δ_w,0) + Δ_w Σ_r P(r|w,qm,qa)p_r
for every 16 worlds and every (qm,qa)∈{0,εm}×{0,εa}.

Because the two channels are conditionally independent, P is **bilinear** in qm and qa; an affine or bilinear function on a rectangle takes a maximum at a corner. Thus these endpoint constraints cover all error pairs in their specified ranges. The code solves the resulting finite LP using SciPy HiGHS and explicitly reevaluates each constraint after optimization.

Information labels:
- none: 1 report
- structural mode: 2 reports
- future arrival pattern: 8 reports
- both: 16 reports

Value is computed without observational costs first. Adding a fixed known source cost c to every world adds c to worst regret, but cannot improve the optimal policy for that fixed source set. Costs are therefore compared at the **source selection** step.

The LP is exact as a *finite linear program*. The implemented SciPy solver uses floating point; baseline and endpoint cases are independently checked against existing rational arithmetic in finite_sensor_information.py, and tolerances remain explicit. This is not a field-calibrated uncertainty set.
