# P11: Event-Time Causality and Policy-Selection Reliability

**Priority A (model correctness):** Define an explicit timestamped event-order model, where receipt/release at t+dt never authorizes admission at t. Preserve exact original P2, modify an experimental fork, unit-test the minimum P10 vehicle1/vehicle8 witness (last side green entry t=47.1625s) before scaling. Distinguish vehicle conservation, physical storage, signal phase, downstream transfer, and stopline safety.

**Priority B (numerical validation):** Sweep dt in a preregistered decreasing sequence; measure earliest diverging events, completed trip times, pairwise policy rank, argmin stability and score gap (selection margin) with same arrivals and holdout seeds. No guaranteed convergence inferred from a finite sweep.

**Priority C (independent validation):** Build the smallest equivalent two-intersection SUMO comparator before complex Bologna network; ensure exact signal-state, turn connection, arrival demand, vehicle dimensions and completion accounting. Keep upstream SUMO files unchanged. Gather Jinju CSV raw bytes and metadata, distinguish detector discharge counts from actual upstream demand. Calibrate/train and holdout on distinct dates.

**Decision certificate (conditional mathematics):** Let objective estimate Jhat(p), truth J*(p). If an actually proven uniform error bound sup_p |Jhat(p)-J*(p)| ≤ epsilon exists, and estimated first-vs-second gap >2epsilon, argmin Jhat is also argmin J*. Current experiments supply NO such epsilon. Empirical dt-spread or bootstrap confidence interval is not a deterministic error bound. Until otherwise proven, label outcomes as model-conditional relative preferences.

Next gates: G1 event-time invariants and safety; G2 credible dt/rank uncertainty; G3 equivalent external SUMO; G4 independent observed-data forecast; G5 novelty comparison against published robustness/signal coordination work.

Sources: FHWA Traffic Signal Timing Manual Ch. 3 and Ch. 7; SUMO traffic lights, SUMO detector-data comparison; 2026 multi-agent signal coordination survey; 2026 T-REX robustness benchmark. Research artifacts on shared Drive Research OS in '20261105 김우준의 사유'. All commits must be manual user-author, no github-actions[bot].
