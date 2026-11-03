# v6.5 — Finite-horizon exposure identity (20261103)

Source data: v6.4-P1 54 synthetic single-junction runs at 1000s, with corresponding 155s runs. All vehicles in the compared cohorts arrived before 105s. All 54 cohorts completed by 1000s. No measured traffic or independent SUMO validation.

For arrival a_i and departure c_i, cohort exposure at H after all arrivals is E_H = sum_i[min(c_i,H)-a_i]. If all departures occur by T, E_T-E_H = sum_i max(c_i-H,0). Hence, for matched temporal arrival profiles A and B,
Delta(E_T) = Delta(E_H) + Delta(unobserved-tail exposure).

Existing 18 demand×seed paired blocks per alternative timing profile (3 demands × 6 seeds) yield:
* late_concentrated minus uniform: 155s -263.25 vehicle·s, differential tail +603.8333, 1000s +340.5833. Strict within-block sign reversals 11/18.
* platoon_12s minus uniform: 155s +73.0833, differential tail -94, 1000s -20.9167. Strict within-block sign reversals only 1/18.

Never claim that all blocks reverse or that platoon has established long-run superiority. The long horizon happens to finish all cohorts *in this finite synthetic sample*. The differences also reflect artificial shifts in arrival timestamps, not an isolated causal effect of signal control.

Canonical source files and Python verifier: downloadable T2_v65_censoring_decomposition_20261103.zip (8 entries, SHA-256 54a75f7d17758d2199ccfc6dbbded46184aaf0b1cbd2ea253b6702f5882b2abe).