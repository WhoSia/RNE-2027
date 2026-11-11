# D46-I — 2026-11-11 multi-vehicle gap dynamics: local diagnostic gate

**Verdict: 29/29 unit tests PASS; 12/12 scenarios executed; 4/4 deliberately infeasible variants flagged. Safety-certified follower, finite-storage integration, real traffic verification: HOLD.**

This project resumes the lineage of D46-G (metric vehicle lengths, link reservation, eligibility time) and D46-H (single-car bounded acceleration and stopline feasibility), but **D46-I is a separate prototype**. It has not yet coupled its continuous position/velocity states to D46-G's event-calendar admissions/exits or changed the original D27 engine. Its starting states are two or more already-on-link cars in one lane, ordered front to rear.

## Method
For a vehicle with front coordinate x, velocity v, length ell, maximum deceleration b and a leader with front coordinate x_L, length ell_L, speed v_L, conservative leader stopping envelope:
`x_leader_stop = x_L + v_L²/(2b)`, `d_follow = x_leader_stop - ell_L - min_gap - x`.
A red stopline adds `d_red = x_stop-x`. The active bound is the smaller distance, and the independent command chooses constant deceleration to stop at that boundary if feasible, else full bounded braking and a **negative feasibility flag**. Acceleration is capped and exact distance is integrated through speed-limit and full-stop events. This heuristic is **not a proof of collision avoidance or anticipatory driving**, and does not model reaction times or any real controller actuation.

New crucial improvement: do not only compare net bumper gap after the integration step. Within a step, the two vehicles' velocities are piecewise linear, so relative gap is piecewise quadratic. Split at the speed-cap/full-stop event times and evaluate gap at all subinterval endpoints and internal roots where relative velocity is zero. Report `min_net_gap_during_step_m` and `collision=True` if the minimum is below configured `min_gap_m`. Do not clamp impossible overlap or rewrite history. Replay stops at first flagged violation rather than feeding overlapping states to the next tick.

## Actual tests and executed cases
- **29/29** local unit tests pass. This includes 19 basic kinematic and invalid-input cases plus 10 tests of exact intra-step minimum-gap and failure handling.
- 300 deterministic random combinations of speed, acceleration and step length compared exact algebraic minimum against 1001-step sampled trajectories; sample vs analytic discrepancy < 0.003m in this limited check. This is code validation, not proof for all real trajectories.
- **12** synthetic runs: 3 two-car initial situations x dt=0.05/0.1/0.25/1 seconds over 2 seconds. Both nonpathological situations did not flag collision; the intentionally infeasible near-following example flagged collision **4/4** and the diagnostic run terminated.
- First exploratory replay failed because it attempted to carry an overlapping state into a subsequent step and triggered an initial-overlap exception. The model was then updated to stop and report the first violating step, preserving that failure as an engineering counterexample.
- These checks neither certify actual collision prevention nor show DLR queue wave, signal safety, or policy gains.

## Reproducibility
The complete exact locally run code (`multicar.py`, two test modules, 12-run synthetic experiment, CSV/JSON, logs, research note and SHA-256 manifest) is in:
https://drive.google.com/file/d/11_50OUEH-GZ1l6nWVoBIqNUvqSI8uf3i/view
ZIP SHA256 `00739e3bdb0ce13192ce149ace6605dc0f4da7c8214899fba4dcac09f006992c`.
The GitHub Markdown is the scientific decision record, **not a claim the complete source is separately synchronized to GitHub**.

## Open acceptance gates
1. Use a proven viability/following constraint or detect earlier and reject non-viable start states, not just report collisions after they occur.
2. Couple D46-I longitudinal car states with D46-G finite link occupancy/admission calendars while preserving vehicle IDs and actual geometric clearance; add lane exits and discrete stopline crossing timestamps.
3. Compare against D42 empirical 20Hz lane coordinates with censorship and camera boundary uncertainty; D27 physical correction remains unpatched.
4. Pin/run independent SUMO before any policy ranking result.
