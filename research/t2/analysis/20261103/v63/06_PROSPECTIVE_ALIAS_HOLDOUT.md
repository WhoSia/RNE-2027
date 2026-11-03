# T2 v6.3-P0 — Prespecified parameter-pair new-seed confirmation

Preselected from a different prior synthetic 288-run grid: balanced arrivals 10/min main and 6/min side, duration 130s, horizon 180s, lateral-acceleration cap 2.4m/s², braking cap theta_A=2 vs theta_B=3 m/s². Interventions: green-end guard 0s vs 1s. New independent seed labels 500..539. **160 new synthetic engine executions** (40 seeds × 2 physical assumptions × 2 guards).

15/40 seeds produced the exact same baseline aggregate (generated,completed,cumulative vehicle seconds) in both parameter models. In **3 of these 15** equal-aggregate seeds the guard intervention had different cumulative-exposure effects. Across all 40 new seeds, guard-effect values differed in 8. The selected old example at seed406 was not part of this holdout.

This extends the finite-time *counterexample* beyond a single cherry-picked seed, but does NOT establish general structural non-identifiability, distributional equivalence, or policy ranking reversal. Same three aggregate measures means only those three observables. The difference could disappear when trajectories, phase-specific events, or noisy sensor outputs are included. Research direction: determine discriminatory observation channels and measurement precision while preserving within-scenario held-out tests.
