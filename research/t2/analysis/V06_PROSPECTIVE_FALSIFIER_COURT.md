# T2 v0.6 — Prospective Falsifier Court (RITHM methodological transfer)
Date: 2026-10-31. Branch: `research/t2-spatial-fig2-v02`.
Status: **COURT IMPLEMENTED; PURE 4-TEST SUITE EXECUTED; v0.5 HOLDOUT RUN NOT YET EXECUTED**.
This document is an a priori test plan, not an outcome report. Main remains unchanged.
No GitHub Actions, bots, or automatic merges.

## Scientific motivation and prior art boundary
The traffic domain already has models and simulations for turn-pocket blockage/spillback:
- Zhang & Tong (2008), https://doi.org/10.3141/2071-09
- Reynolds, Rouphail & Zhou (2011), *Turn Pocket Blockage and Spillback Models*,
  https://doi.org/10.3141/2259-10 — macroscopic variable-size cells, lane
  utilization, signal overlap, phase sequence, time-varying demand.
- Wei et al. (2021), https://doi.org/10.1177/03611981211006433
- *Characterizing the dynamics and uncertainty of queues at signalized
  intersections with left-turn bay* (2022),
  https://www.sciencedirect.com/science/article/abs/pii/S0378437122003223
- *Quasi-real time estimation of turning movement spillover events*
  (SUMO as synthetic benchmark),
  https://www.sciencedirect.com/science/article/abs/pii/S0968090X20307294
- *Left-turn queue spillback identification based on single-section license
  plate recognition data* (2024), DOI 10.1080/21680566.2024.2363273.

Novelty NOT established for simulating a short left-turn pocket, producing
a capacity curve, distinguishing leading from lagging phase, detecting
spillback, or applying SUMO. The tentative question is **mechanism and
claim stability under admissible alternative models, input histories,
and negative controls**, subject to further prior-art review.

## RITHM transfer: exact scope
RITHM M05.121–M05.126 distinguishes history MASS from history SHAPE.
T2 analog: M = numbers of L/S arrivals, Q = ordered route sequence.
RITHM M05.132 insists on common-scale negative controls and group-level
interference. T2 analog: vehicles within one simulation are mutually
coupled; individual vehicles are not independent replications. One
random seed is a simulator environment, not a field-level intervention
unit. Replicated random seeds with one frozen codebase provide numerical
robustness, NOT independent real-world validation.

## Frozen prospective challenge
Discovery seeds: 0..9, already inspected in v0.5.
Holdout seeds: 100..119. Never tune to them in the same court.
Grid: f in {-21,-13}, K in {2,4}, protected order in {leading,lagging},
update in {sequential,parallel}; clearance=3s; duration=4200s;
same timestamp/route/lane arrival stream per seed across f/K contrasts.
20 new seeds x 2 signals x 2 updates x 4 cells = **320** runs.
For each seed compute the interaction:
I=[Q(-13,4)-Q(-13,2)]-[Q(-21,4)-Q(-21,2)].

**Strict predeclared falsifier**: v0.5 exploratory 10/10 negative sign
on each signal/update; if ANY held-out I >= 0, mark that context's
universal-within-holdout sign claim REFUTED. If all 20 are negative,
mark PASS_TOY_ONLY, not empirical validation. As a descriptive secondary
metric report mean and individual contrasts, including zeros.
Selection of this sign criterion is exploratory relative to the whole
project because it was informed by the v0.5 discovery set.

**Exact negative control**: `left_fraction=0`, same seeded arrivals
and geometry. Varying only virtual bay cap K cannot change state:
the cap check occurs only for route L. Therefore
Q(f,K=2)=Q(f,K=4) identically at each fixed fork f, conditional on
the simulator's deterministic update logic. If violated, FAIL the
implementation/admission invariant. This is an exact code-level
negative control, not evidence that real road geometry is inert.
Run a 600s version separately for each signal and update policy.

## How to run; sealed outcomes
```bash
python -m unittest discover -s research/t2 -p 'test_prospective_court_v06.py' -v
python research/t2/run_prospective_v06.py --output research/t2/results/prospective_v06.json
```
The 4 pure court unit tests passed on Python 3.13 locally and include
negative-control failure injection and a nonnegative-holdout falsifier.
The full 320+ placebo simulator runs are **NOT YET EXECUTED**;
the outcome file does not exist as a committed fixture. Once executed,
record Python version, exact repository HEAD, generated JSON SHA256,
all 80 per-condition seed-level interactions, and any FAIL/REFUTED
without post-hoc exclusions.

## External competitors and non-substitution gates
SUMO is not automatically a ground truth: LC2013 strategic/cooperative
lane choice, actual insertion delays, junction connections, phase
definitions, and physical car length can each alter the causal surface.
Official documentation:
https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
https://eclipse.dev/sumo/docs/Simulation/VehicleInsertion.html
https://sumo.dlr.de/docs/Simulation/Output/Lanechange.html

A SUMO comparison needs matched geometry, signal timings, emitted/
departed/arrived vehicle counts, route choice, queue profiles, and
lane-changing event reasons. Its validation should compare mechanism
signatures, not just overall Q. See FHWA 2019 microsimulation
calibration guidance: https://ops.fhwa.dot.gov/publications/fhwahop18036/chapter5.htm

**Not licensed**: same result under 20 more seeds => independence from
simulator; SUMO agreement => field causality; equal vehicle counts =>
same history process; 2x2 virtual cap K => roadway length intervention;
a difference in finite-horizon departures => stable saturation flow.

## Research programme after this court
1. Execute the frozen v0.6 320-run challenge without inspecting/tuning
   after each partial result. Report all outcomes including failures.
2. Negative-control challenge by independently generating all-S streams,
   and a second control in which no green is available.
3. Match phase-clearance semantics; re-run with periodic cycle queue
   measurements and warm-up/cool-down separation.
4. Only then design a SUMO synthetic network; start with alternate
   insertion policies and strategic-lane-change parameterization to
   test mechanism sensitivity rather than confirming an attractive plot.
5. Independent field-contact: multiple observation days, blinded
   incident/queue audit, and no vehicle-identifying data.
