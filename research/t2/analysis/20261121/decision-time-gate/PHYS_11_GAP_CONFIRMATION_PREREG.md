# PHYS-11 — Contiguous eligible-gap confirmation as a synthetic lane-change sensitivity

2026-11-21 · pre-registration **before** PHYS-11 policy outcome generation

## Motivation and physical interpretation

The current T2 two-lane engine allows A→B lateral movement on a
single eligible tick if the adjacent target lane has the specified
vacant cells. This is a minimal lane-change proxy, not real human
gap acceptance. We will add a backward-compatible `lane_change_gap_confirmation_s`
parameter (default 1) to require **1/2/3 consecutive one-second
ticks** satisfying all current lateral-change candidate and target
clearance predicates before the movement can occur. A vehicle's
confirmation streak resets when the opportunity is not eligible,
the target gap is blocked, the vehicle advances longitudinally or a
configured opportunity window is closed. Streak state is included in
checkpoint snapshots to maintain deterministic branching.

This is an exploratory *gap persistence* condition, **not**
driver reaction time or empirically safe following distance. It does
not add realistic velocity, driver aggressiveness or cooperative
response. Denied-candidate-tick counts must not be interpreted as
the number of individual drivers who refused a gap.

## Experimental lock

- First run the new code with default confirmation=1 and prove the
  prior PHYS-04 output fields match the exact-core baseline (all
  144 conditions), plus trace/checkpoint equality and original
  PHYS-07/08/09/10 numeric output invariance.
- Prospective seed **80–87** only (8 never-used seeds). Fixed demand
  1800 vehicles/hour, left fraction 0.50 and normal uniform arrivals.
- Receiver storage **4 cells**, pocket lengths **14/28/70m**,
  B-lane preassignment **0/.5**, change zone **100m**,
  lateral target clearance **1 cell**.
- Confirmation settings **1/2/3 consecutive ticks**. Each setting
  defines a distinct physical model world and creates 8×3×2=48
  same-state policy pairs; across all settings **144 matched pairs**.
  Across confirmation settings the predecision state is *not*
  identical and must not be interpreted as direct causal treatment.
- Within each condition, branch from complete pre-tick-84 state
  into the baseline future and the same 3s clearance / 4s left
  green treatment, holding arrivals and all physical parameters.
- Objective: integrated outside/upstream/receiver vehicle-seconds
  plus 60×remaining at tick 240.
- Metrics: matched baseline/treatment score and delta, crossing
  counts, remaining, total A→B lane changes, motivated candidate-tick
  target-gap denials and confirmation-wait candidate-ticks.
  Report both average effects and strict changes of policy-sign
  preference across the three physical settings.
- Replay each setting from checkpoint and compare to uninterrupted
  run; conservation and finite-road geometry assertions must pass.
- Two byte-identical output generations and exact GitHub blob checks
  for new engine/runner/test files are required before reporting
  verified local results.
- Preserve original 704-run PHYS evidence and K047 holdout.

## Stop conditions and limitations

If default=1 changes pre-existing outcome fields, checkpoint replay
or branch state, do not publish new sensitivity findings before
isolating the regression. If no gap-confirmed changes occur for
2/3 settings, report that as a model degeneracy instead of inventing
a human driver implication. Never represent the added parameter
as measured reaction time, a real traffic-signal safety guarantee,
or an empirical gap-acceptance model.
