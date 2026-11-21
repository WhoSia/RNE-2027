# T2 — Arrival clocks and phase-window validity: two registered falsification screens
2026-11-21 · **SYNTHETIC_UNCALIBRATED**, not a legal road-signal feasibility study

## Executive decision

The original 'uniform' generator fixes every request timestamp for a
given demand rate. New seeded clocks exposed materially different
policy rankings. In the second, more carefully controlled cohort,
**strict opposite policy-value signs appear even after exact matching
of the total vehicles and ordered turn-route labels**. Thus the
original seed-only generalization claims **DO NOT transfer directly
to varied arrival timestamps**.

However, the opposite signs occur under **different pre-t84 microscopic
states and generally different six-count observations**. The result
is **NOT** a same-observation strict-identification impossibility theorem.
Within each world, baseline and intervention still share the full
pre-t84 checkpoint. The proposed four green durations remain
*abstract, uncalibrated actions* because no real yellow indications,
pedestrians, conflicting cross-street movements or controller
commitments are represented.

### Engineering caveat from official technical references

FHWA Traffic Signal Timing Manual Ch.5 differentiates minimum green,
yellow change and optional red clearance, and notes minimum-green
settings depend on driver expectation, detection and pedestrians.
It discusses illustrative left-turn minima of 2–5s for some facility
contexts, not a universal rule that 4s green is always illegal.
The current engine's `'-'` means no served vehicle, NOT an explicitly
modeled amber signal:
https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter5.htm

SUMO's official documentation explains exponential/Poisson arrivals
and equidistributed randomized departures as alternative temporal
flow models. Our standalone two random generators follow analogous
mathematical ideas, **but this is NOT a SUMO experiment or a calibrated
replication**:
https://eclipse.dev/sumo/docs/Simulation/Randomness.html

## Cohort A — seed88–95, three arrival-clock generators

Pre-registered [before results](T2_GREEN_ENVELOPE_AND_ARRIVAL_CLOCK_PREREG.md).
288 unique traffic worlds = two regimes × three arrival clocks ×
eight seeds × three pockets (14/28/70m) × two B assignments (0/.5).
Receiver capacity4, 240s horizon, decision tick84.
Within each world, all four proposed signal windows are paired to
one baseline through the same checkpoint and tape.

Arrival families:

1. `legacy_deterministic`: exact canonical `spatial_v10.arrivals`.
2. `fixed_count_uniform`: exact N=floor(240*demand/3600)
   arrival requests, random timestamp allocation, independent
   seeded route RNG.
3. `poisson_exponential`: independent exponential interarrivals,
   randomized total number and separately seeded route RNG.

**Confounding admission:** (2) and (3) alter both temporal arrival
profiles and route-label draws relative to the legacy generator;
they are distribution-stress tests, not isolated clock effects.
Cohort B below removes this confound.

| Regime | Clock | Distinct time tapes, 8 seeds | Mean input requests | 4s plan ΔJ<0 / ΔJ>0 / tie (48) | Total ΔJ |
|---|---|---:|---:|---|---:|
| 1800 vph, left45% | legacy | 1 | 120 | 1 / 3 / 44 | +812 |
| 1800 vph, left45% | fixed-N random | 8 | 120 | 21 / 8 / 19 | −4725 |
| 1800 vph, left45% | exponential | 8 | 117.625 | 9 / 2 / 37 | −730 |
| 1650 vph, left50% | legacy | 1 | 110 | 21 / 0 / 27 | −6612 |
| 1650 vph, left50% | fixed-N random | 8 | 110 | 25 / 6 / 17 | −9315 |
| 1650 vph, left50% | exponential | 8 | 107 | 21 / 2 / 25 | −4659 |

At 1800 vph the exponential-family total requests ranged 93–131
across the eight seeds; at 1650 vph a different finite-sample range
is in the JSON. No eight-seed estimate should be treated as a
field-calibrated stochastic distribution.

**Changing left-green width 4→8/12/20:** only **6 of 288**
worlds exhibited a nonidentical ΔJ across widths, and **zero strict
negative-to-positive reversals across the four widths** occurred
within fixed microstate/tape worlds. In a few cases extending
left-green created extra model cost (e.g. seed93, left45,
Poisson clock, pocket14m, B-share0: ΔJ 0→+780).
Do not call 'longer green is intrinsically safer'.

Known-seed exploratory check, separate from preregistered novel
cohort: the original PHYS-10 seed76 +306 case remained +306
at all tested widths 4,5,7,10,15,20,25,29s. Lengthening green
alone did not fix this model counterexample, but still cannot
certify a real controller plan.

**Full JSON SHA-256 (two byte-identical runs):**
`d5a11da4cd71cec3d1aa305ddf85e3b45fba0a3d89824b1ccf6e49bb9a9da6f2`.

## Cohort B — new seed96–103, isolate clock only

Pre-registered the new cohort [before inspection](T2_ROUTE_MATCHED_CLOCK_PREREG.md).
Exactly **192 worlds** = two regimes × eight new seeds ×
three pockets × two B shares × two arrival clocks.
Same receiver4 and green-width plans.

For each seed/regime:
- Generate the exact original deterministic arrival tape once.
- Draw a second sorted uniform timestamp for every original request.
- Reassign the original **i-th movement label to the i-th new
  request timestamp**. Check total request count and full ordered
  route-label array match exactly, not just marginal left fraction.
- The two clock worlds differ in pre-t84 input queues and traffic
  microstate, so their action-effect contrast is NOT an identical
  predecision-state causal effect. Within each clock, the signal
  branches still share one frozen pre-t84 state.

| Regime | Clock | ΔJ<0 / ΔJ>0 / tie (48) | Mean ΔJ |
|---|---|---|---:|
| 1800 vph, left45% | legacy | 8 / 2 / 38 | −47 |
| 1800 vph, left45% | random time only | 18 / 12 / 18 | −87.0625 |
| 1650 vph, left50% | legacy | 27 / 6 / 15 | −150.125 |
| 1650 vph, left50% | random time only | 21 / 13 / 14 | −103.0417 |

The four-second intervention showed **strict policy-sign opposition**
between the two clocks for **1/48** corresponding labels in
left45 and **9/48** in demand1650. The nine contrasts in
demand1650 cluster in **three independent seed groups
(96,97,100)**, not nine independent traffic days. One additional
seed101 provided the left45 sign opposition.

One clean example, seed96, demand1650, pocket14m, B-share.5:
- Legacy arrival clock: ΔJ **+34**, signal intervention worse.
- Same total 110 vehicles, same route-label sequence, timestamp-only
  randomized clock: ΔJ **−178**, signal intervention better.
- The first 84 seconds receive 38 versus 34 arrivals and the
  observed occupancy vector differs. **This is NOT a
  same-aggregate-observation alias**.

We inspected **all ten** strict opposite-sign contrasts: **none**
had identical full six-count decision-time observation across
the two clocks. The original PHYS-10 observation-insufficiency
claim is not proven by this new timing experiment.

Exploratory penalty sensitivity selected after seeing the ten
reversals: all ten maintain strict opposite signs at terminal
penalty **0, 30, 60, 120**. Example seed96:
legacy +34 at all four penalties; timestamp-randomized
−118, −148, −178, −238 respectively. This is posthoc
robustness within the fixed synthetic response model, NOT a
new confirmatory sample.

**Full JSON SHA-256 (two byte-identical runs):**
`7aedc8e7d85808bf4be36dbcd4d9023bd5dcd9468e84ac8660fd281b60e9e8ed`.

## Reproducibility and validation receipts

- Core engine file: GitHub `main` and executed local Git blob
  `a7c9aa6954402e12894d1d5b722e8a474b0bd58f`.
- Exact core imported modules:
  `spatial_v10.py` `ffbf3fc3f8b9a64a819d4f73ce70b264b877e84e`;
  `receiving_cells_v15.py` `b078cf215c74b76ace6dffcbcbacab6ae22c3673`;
  `physical_transfer_screen.py` `8d75745053ff720db6c8af0001aaaf13ba1f295e`;
  `physical_checkpoint_observation_ablation.py`
  `db9ceb2774ee1b7e70728a340b50d41f4c884c18`.
- New experiment and test Python files were uploaded to `main`
  and **fetched back with exact Git blob SHA identity** to the
  local executed copies. A first test revision incorrectly
  referred to a local untracked JSON; it was **fixed** to regenerate
  the complete cohort directly. Clean-run local new tests **8/8**.
- Core baseline equals direct run in all **480** new traffic worlds,
  every branch respects the simulator conservation identity, and
  all 1920 within-world phase-plan contrasts use the same frozen
  decision checkpoint and arrival tape. The exact same-state
  condition is NOT claimed for different arrival-clock worlds.
- Full outputs were regenerated in two independent Python
  invocations and byte-compared, not merely compared by rounded
  aggregate results. Execution used Python 3.13.5, not GitHub
  Actions; no whole-repository historical test-suite claim.
- K047 field holdout remains sealed; no real traffic calibration
  or external model execution occurred.

## Decision and next gates

**REJECT** the notion that new integer seed IDs under a deterministic
arrival clock demonstrate day-to-day arrival-time robustness.
**ACCEPT** the narrower simulated finding that timing redistribution
with the total and ordered route labels fixed can flip a policy-effect
sign across physically different predecision states.

**HOLD** any legal signal-plan recommendation, actual traffic effect,
or general impossibility of identification from equal observations.

The next high-value experiment is not another feature knob:
formalize an **operational action-feasibility gate** using real
yellow/red/pedestrian/conflicting-stage constraints and a
separate empirical arrival-clock calibration. Re-test a candidate
strict reversal under those independently justified constraints.
A valid negative result is preferable to proliferating uncalibrated
control heuristics.
