# T2 independent arrival-clock isolation — confirmatory protocol
2026-11-21 · **PRESPECIFIED BEFORE RUNNING SEEDS 96–103**

## Motivation, corrected attribution

The earlier [T2 green-envelope & arrival-clock protocol](T2_GREEN_ENVELOPE_AND_ARRIVAL_CLOCK_PREREG.md)
compared a legacy fixed timestamp generator to a fixed-N uniformly
randomized timestamp generator and a Poisson process. It found
substantial response differences across arrival families. But the
fixed-N random family also used an **independently redrawn turn-label
sequence**. Consequently, the earlier contrast was a joint change in
arrival timing and vehicle movement mix, not a clean isolated test of
arrival timestamps.

## Frozen experiment

- Never-used synthetic seeds **96–103**, two regimes
  (1800 vph, left 0.45) and (1650 vph, left 0.50).
- For each seed/regime, generate once the **legacy canonical tape**
  through `spatial_v10.arrivals`, retaining the exact vehicle
  count and sorted per-vehicle route-label sequence.
- Construct a second tape by drawing one uniformly random second
  per original vehicle in 0..239 with **separate deterministically
  seeded timestamp RNG** and sorting those timestamps. Assign the
  original vehicle's i-th route label to the i-th new timestamp.
  Thus both tapes have **identical vehicle count and ordered
  movement labels**; only request timestamps change.
  Note: vehicle/route type is matched in ordinal order, not a
  real-world matched vehicle identity or identical pre-t84 state.
- Hold geometry and signal configuration: receiver 4 cells,
  pocket 14/28/70m, B-share 0/.5, one-second microscopic tick,
  240s horizon, same `DualConfig` and receiver physics.
- Two timing worlds × two demand regimes × eight seeds × three bays
  × two B-shares = **192 synthetic worlds**. Within each world,
  one baseline and four phase policies (t84–87 no service, L
  4/8/12/20 seconds from t87, no service until t120) share
  exactly the same pre-t84 checkpoint and complete future tape.
  Across different timing tapes, the predecision microstates
  generally differ — contrast across tapes is NOT same-state
  causal clock intervention on signal effects.
- Objective and metrics identical to the prior registration:
  integrated outside+upstream+receiver vehicle-seconds plus
  60×end remaining. Signed ΔJ=J_treat−J_baseline.
- Before reading any outcomes: primary comparison is for the 4s
  plan, by regime and tape: count ΔJ<0/ΔJ>0/ΔJ=0, sum/mean,
  and per-identical-route-sequence label classifications.
  Report number of label pairs where a *strict negative* ΔJ
  under one clock becomes *strict positive* under the other,
  excluding ties; also tally one-sided zero-to-nonzero changes.
- Secondary: check whether longer L green reverses signs within
  fixed timing-world; do not tune lengths or choose seeds.
- Required validations: N and full route-label array exactly
  match between clocks; timestamp arrays differ across the eight
  new seeds; no use of outcome labels in generator; check every
  uninterrupted-vs-checkpoint baseline and vehicle conservation,
  plus fixed checkpoint before treatment. Run full output twice,
  compare bytes, SHA-256 and commit file hashes.
- Neither timing generator is calibrated to real traffic, and
  these phase windows are **not** legally implementable controller
  schedules without additional yellow, pedestrian, cross-street
  and local timing constraints. Do not claim field efficacy,
  empirically identified driving behavior or road safety.
- K047 field holdout stays sealed. No GitHub Actions or bot
  contributions. Negative outcomes must be reported.

## Decision

If independently redrawing the timestamps, while preserving
the number and ordered route labels of all vehicles, changes
the sign of ΔJ on matched seed+geometry labels, then the earlier
fixed-timestamp generalization claim is not robust to an
alternative arrival clock. This is **synthetic demand-clock
sensitivity** only. It cannot identify an empirical magnitude
without measurement calibration and a genuine operational action set.
