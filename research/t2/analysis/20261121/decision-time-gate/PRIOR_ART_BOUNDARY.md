# T2 novelty boundary: source-by-source research direction (2026-11-21)

## Strong overlapping prior work — acknowledge it

1. **Long, Li, Lei & Wang (2026), *When Better Traffic Forecasts Fail to Improve Signal Control*** (arXiv:2610.06992, https://arxiv.org/abs/2610.06992). This work explicitly studies forecast-to-control value, a decision-time leakage correction, feasible action counts, an event oracle and mismatched optimization objectives. **Therefore T2 cannot claim that observing such a forecast/control disconnect or enforcing chronological forecast inputs is new.** Their test uses traffic demand reconstructed from 29 Xuancheng days and a nine-intersection network. T2 differs in microscopic pocket/queue configuration and the question of when a blocked follower can reach an adjacent lane. Their information gate is a method to cite, not a research gap to re-invent. **Original arXiv v1 PDF located in 00_INTAKE on 2026-11-21, read and moved to the canonical 10_PAPERS shelf:** https://drive.google.com/file/d/1xfbbwXdee0_wGBWxpEb-3uM_BdZB5FvL/view.
2. **Guo, Krylatov & Wang (2026), *Optimal Sensing Boundary Identification for Adaptive Signal Timing via Bayesian Online Learning*** (Sustainability 18(17), 9194, https://doi.org/10.3390/su18179194). Optimizing how far upstream one needs to observe for signal timing has already been studied. A [PDF is present in Drive](https://drive.google.com/file/d/1Vy9IvvLKawOMAzYRCe0LO3cC1XIjZej4/view). We should not say “optimal sensor placement” alone is a novel contribution.
3. **Shafik & Rakha (2025), *Real-Time Turning Movement, Queue Length, and Traffic Density Estimation and Prediction Using Vehicle Trajectory and Stationary Sensor Data*** (Sensors 25(3):830, https://doi.org/10.3390/s25030830). A two-stage Kalman approach already combines probe trajectories and upstream detector data to estimate turning movement and queue states. We should not claim the mere combination of those sensors is new. **Publisher PDF located in 00_INTAKE on 2026-11-21 and moved to 10_PAPERS:** https://drive.google.com/file/d/1LJpiI0hENPuBmWadMgIbUP9Fp_rqZAum/view.
4. **Liu et al. (2024), *Integrated Optimization of Traffic Signal Timings and Vehicle Trajectories Considering Mandatory Lane-Changing at Isolated Intersections*** (TRC 163:104614, https://doi.org/10.1016/j.trc.2024.104614). Mandatory lane change and signal timing have been optimized together. Our admissibility/movement restrictions must be compared to theirs before claiming a new lane-change model. No exact matching title was found in shared Drive during this pass.
5. **Wan, Ma, Lo & Yu (2024), *Signal Optimization at an Isolated Intersection under Cyclic Vehicle Arrivals Using Spatially Sparse Trajectory Data*** (TRC 163:104643, https://doi.org/10.1016/j.trc.2024.104643). Sparse trajectories have been used to estimate cyclic arrivals for signal optimization; distinguish realized and forecast arrival information. No exact matching title was found in shared Drive during this pass.

## What remains a candidate contribution, not yet an established novelty

**H1 — pocket-specific observational equivalence.** Construct physically interpretable paired worlds that share every admissible decision-time measurement (arrival aggregates, initial and current queue, signal history) but differ only in the subsequent *feasible* lane-change windows. Under the same safety-feasible phase pair they reverse the preferred action. A two-world binary witness is a demonstration; its representativeness and survival under realistic lane-changing rules are open.

**H2 — latency- and cost-dependent decision sufficiency.** For a fixed regret objective, establish when available observation and forecast quality actually improve the feasible action, rather than testing forecast MAE alone. The first threshold (−113/+31 with p=60) is **only** an exact restricted two-world deterministic policy bound: forecast-following helps against the fixed order if 113 ε + c < 31. Do not call its 72.6% required conditional accuracy an empirically calibrated sensor threshold.

**H3 — observational bridge.** Label windows at a site where the leader, follower, adjacent lane, signal and downstream receiving space are simultaneously in view. Distinguish *visible spatial opening*, *feasible lane change*, *actual lane change*, and *cannot tell*. The first eight consecutive cycles are a labeling pilot, not a prevalence or predictor evaluation.

The traffic engineering contribution will only be supported after these three pieces can be linked under a consistent geometry and safety rule. We may still publish an honest negative result if the strict FIFO reversal disappears under plausible bypass.

## Claim hygiene and next gates

- **Exhibition first**: label the existing future-reveal demo an *oracle thought experiment*, and show a second panel where a forecast can be wrong, costly or too late. Never represent the policy as operating a real signal.
- **Next experiment**: hold the actions, synthetic arrivals, horizon and terminal penalty fixed; vary only pre-decision observation quality and reporting latency; compare fixed, conditionally observed and oracle actions.
- **Minimum physical check**: K047 HTML review and its unusable template are retired; no synthetic scene or blank interface is treated as a student field measurement. If independently sourced raw observations later become usable, evaluate them at the raw data level. For now, prioritize a new documented observation site and never intervene in real traffic signals.
- **December 18 deliverable**: one causal timeline, one paired-world reversal robust to at least one alternate objective setting, one negative or ambiguous real observation, one measured or acknowledged data gap, and a clear limitations panel.

## Missing source status at this check

**Confirmed in 10_PAPERS on 2026-11-21**: Long et al. 2026 and Shafik & Rakha 2025. **Still without verified PDFs**: Liu et al. 2024; Wan et al. 2024. Guo et al. 2026 and Hidas 2005 are held. Do not spend the four-week exhibition window comparing preprint/publication versions unless a material result depends on it.


## 2026-11-21 revised decision-theoretic gate

The previous ε < 31/113 threshold pertains **only to the deterministic policy that always obeys a binary forecast**. A fully optimized two-world randomized minimax policy can do better even at ε=30%: regret bound 10509/556≈18.90 versus 3503/144≈24.33 for the optimal forecast-free randomization and 31 for the best forecast-free deterministic order. This follows from choosing action probabilities conditional on each report; it is not a demonstrated field improvement or an original general decision-theory theorem. [Verified calculation](RANDOMIZED_POLICY_AUDIT.md).

New authenticated material: [six-paper intake ledger](../INTAKE_6_PAPERS_20261121.md). The standard bibliographic names and stable original Drive IDs are preserved there. Outdated K047 HTML claims are invalidated by retirement commit 0055abb.


## 2026-11-21 16-world structure vs arrival-order stress test

Reused eight fixed synthetic arrival orders in the exhibit under two different simulator bypass rules. With unknown rule and order, the best randomized action has regret 161236/639≈252.33. Perfectly knowing all future arrival bits **without** knowing the rule does not reduce this worst case; knowing the physical rule reduces the bound to 9342/373≈25.05. Even a hypothetical mode classifier with 30% conditional label error gives 483708/2609≈185.40. **This is not a real-world sensing result**: the unobserved variable is a whole simulator-mode switch, the mode affects large-scale costs, and full predecision microscopic equivalence has not been verified. We will not generalize these figures to traffic performance. The next physics-focused experiment must replace this artificial switch with actual timed gaps under a fixed, known geometry. [Exact rational report](FINITE_SENSOR_FINDINGS.md).
