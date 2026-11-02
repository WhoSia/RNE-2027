# T2 v3.0 precursor — Fair policy comparison protocol

## Problem
The first locally greedy queue-pressure controller completed fewer OD trips than the fixed-time policy in every one of 64 simulated inputs. This is not yet an explanatory finding: it could be a controller implementation defect or mismatched switching constraints rather than a failure of local control. No claim of a Max-pressure theorem counterexample is authorized.

## Required changes
1. Log movement opportunities, exact stage transitions, clearance intervals, stage activation, blocked receiving, and phase lost time at each intersection.
2. Compare like-for-like: same minimum green, amber/all-red, actuation/switch limits, downstream entry permissions, initial queues and same exogenous arrivals.
3. Implement true store-and-forward Max-pressure with movement weight q_up - sum(turn_ratio*q_down), feasible simultaneous movement stages and fixed saturation rates; distinguish unlimited-buffer theorem from finite-storage experiments.
4. Include strong fixed-time optimization under the **training** demand, and hold out seeds/demand-shift scenarios. A poorly configured fixed-time controller is not a valid baseline.
5. Pre-register outcome hierarchy: OD trip completion and total unfinished vehicles; censored trip time; total vehicle-time; service-by-movement; side-road fairness; spillback. Optimize no metric on held-out simulations.

## Exact falsification questions
- Does local pressure fail only because of phase switching overhead?
- Does finite storage create blocked-greens that change network stability?
- Is a higher completed-trip count attributable to early terminations or actual clearance under longer horizons?
- Does an adaptive policy starve one approach under asymmetric turning demand?

**State:** protocol only; no new policy implementation or benchmark run in this commit. Code executed offline is preserved separately in the 20261102 Drive ZIP. No GitHub Actions.
