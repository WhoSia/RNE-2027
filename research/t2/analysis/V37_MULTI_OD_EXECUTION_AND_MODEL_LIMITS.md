# T2 v3.7 — Executed multi-destination prototype and correction

On 2026-11-02 a separately executable Python model was constructed locally with origin 0 (to destination 1 or 2), side origin 1 (dest 2), side origin 2 (dest 2), link capacity and two operational signal phases at nodes 1/2. Node0 is admission only. Source ZIP local: `T2_v37_multiOD_synthetic_20261102.zip`, SHA256 `6eb82ea61c181417ece971cc35516e02387e95026aaac3cb9fb362cf31c38f57`. Six tests PASS. First implementation FAILed targeted intermediate-exit unit test due to link index mapping; this was repaired BEFORE execution of the 240 experiment runs. Source not yet committed to GitHub, and not a realistic SUMO/CTM traffic model.

240 runs (80 matched contexts × three policies), 5 seeds × 2 link capacities × 2 intermediate-exit fractions × 2 side-demand probabilities × 2 offsets. Arrival generation ends at 450s; measurement ends at 900s. Vehicle conservation and capacity checked each step.

Overall mean completed: fixed 386.425, coordinated 375.9625, heuristic pressure 372.825. Pressure vs fixed: better in 32 of 80 contexts, worse in 48. At upstream intermediate-exit fraction 0: fixed 352.4, pressure 362.75; at exit fraction .5: fixed 420.45, pressure 382.9. These are synthetic descriptive means, not causal field impacts. The routing fraction changes OD demand composition, so cannot interpret as isolated signal-policy effect without scenario-wise matching.

IMPORTANT CAVEATS: two operational signalized nodes (not three), last side origin exits at node2 directly, no realistic intersection conflict or crossing/yield, third link unused, no route assignment, no pedestrian or gradient, `pressure` heuristic NOT Varaiya MP. The prototype is an intentionally limited structural test, not an end-state optimizer.
