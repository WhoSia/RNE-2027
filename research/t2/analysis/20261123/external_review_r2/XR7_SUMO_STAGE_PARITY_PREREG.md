# XR7 — SUMO–T2 ID-wise timing divergence decomposition (pre-registered before XR7 execution)
Date: 2026-11-23. XR3_SUMO 1.28.0 E0e fails on both red-onset arms; E0b was judged by **median** absolute approach admission error despite **max** 66.75s and 42.75s. Original XR3 result remains frozen, and SUMO policy-sign comparisons are forbidden until all identity and time-parity gates pass.

## Frozen inputs
Same XR3 fixed world: label seed 86001, time seed 88501, stochastic_uniform share L=.75, C4, 60 T2 vehicle IDs, baseline 900vph, downstream policies (30,phi15) and (60,phi30), upstream phase override at t84 and original demand tape. Do not modify SUMO geometry, vehicle parameters, phase windows, nor T2 lane/pocket logic while measuring XR7. One exact baseline run per arm; future intervention deliberately separate.

## Decomposition for each vehicle i
Define T2 arrival A_i, first admitted upstream tick U_i, upstream stopline crossing S_i, full network exit E_i; SUMO equivalents U'_i, S'_i, E'_i, preserving vehicle ID i.
\[
E'_i-E_i = (U'_i-U_i)
 + [(S'_i-U'_i)-(S_i-U_i)]
 + [(E'_i-S'_i)-(E_i-S_i)].
\]
The three terms are approach insertion alignment, upstream approach/pocket dynamics, and downstream receiver/travel differences. Record by ID and L/S movement, original admission time, stopline time, exit time, all signed and absolute errors. Distinguish **true SUMO departure** from externally scheduled tape arrival. Verify this exact decomposition numerically for all vehicles; keep missing IDs explicit and treat as failure, never drop them from the denominator.

## Decision gate
- D1: all 60 IDs have 3 timestamps in each engine; do not use median filtered only nonmissing IDs.
- D2: compare time-of-first-deviation by stage, report median, p90, max of ABS errors by movement, and count errors>3s; do not infer which mechanism causes a discrepancy from these statistics alone.
- D3: in addition to XR3 E0b median criterion, require p90(|U'-U|) <= 1s. This stricter admission alignment criterion is **new** and is not retroactively applied as the original XR3 prereg gate.
- D4: report p90(|S'-S|) <= 3s and p90(|E'-E|) <= 10s separately. If any fail, all policy-sign comparison MUST remain blocked.
- D5: verify native T2 score equals sum of reconstructed exact exit-minus-arrival vehicle seconds before using those exits as reference.

The existing XR3 result has already failed E0e. XR7 is an explanatory diagnostics design, **not a retroactive success or proof of SUMO equivalence**. In this execution environment SUMO is not installed; actual XR7 runs must report NOT_EXECUTED and must not fabricate CSV rows.

## Scientific interpretation
High insertion tails may be caused by upstream congestion, SUMO lane change/pocket routing, entry blocking, or mismatch in vehicle representations; this test isolates *where timing errors accumulate*, not necessarily their causal origin. Next receiver-only microbenchmark is a separately predeclared experiment that injects T2 stopline-cross attempts and checks actual SUMO receiver admission; never coerce SUMO departure timestamps to equal T2 while counting unadmitted vehicles as admitted.
