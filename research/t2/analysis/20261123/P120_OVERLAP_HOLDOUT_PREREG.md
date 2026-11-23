# P120 — pre-registered temporal holdout for calendar overlap sign heuristic

Written before running P120. Use **never previously inspected** independent timing seeds 88101 and 88102, one frozen route label seed 86001, two timestamp families `stochastic_uniform` and `stochastic_platoon4` from P118's generator. Exactly 4 different temporal arrival vectors.

For each vector, keep T2 original high-left .75 route labels, receiver 4 cells, one-slot turn pocket, original signal and t84 checkpoint. Period30 offsets 0..29; period60 offsets 0..59; 360 full-arm runs across 4 tapes, horizon 4800 and full network exit required.

Frozen heuristic, no fitting: calculate `O(period, offset)=count of integer ticks t in [84,400) with upstream left phase active AND downstream green displayed`, using exact model `spatial_v10.phase` and P69 phase override. For each of the 30×60=1800 offset-pair comparisons per tape, predict the sign of 30s-minus-60s **TOTAL vehicle-seconds** as `sign(O60-O30)`. Any zero overlap difference is a prediction abstention, NOT counted as correct. True cost tie is a separate category.

Primary gate: strict-prediction sign accuracy >0.75 over all non-abstentions and at least 0.15 absolute improvement over the frozen always-30s-better sign classifier. This is a descriptive coverage-weighted gate; 7200 pairs share just 360 arms and FOUR temporal scenarios. Do NOT report a 7200-sample confidence interval or infer population success.

If gate fails, downgrade analytic sufficiency and prioritize queue-state features. If it passes, calendar overlap remains predictive *within T2*, but not proven sufficient for causal mechanism or transferable to SUMO.
