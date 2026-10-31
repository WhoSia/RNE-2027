# T2 v1.5 — Spatial Receiving Link and Offset Holdout

Date: 2026-10-31. Branch: research/t2-spatial-fig2-v02.
**Repository policy:** no GitHub Actions, no .github/workflows files,
no main merge and no scheduled/background remote execution.

## Question
Can the signal and storage state of a downstream intersection alter
the apparent benefit of extending an upstream left-turn pocket?

## Engineering change
Added receiving_cells_v15.py: an explicitly spatial, one-cell-wide
receiving road segment with N finite cells, one car per cell, one
cell per step, downstream periodic signal offset and minimum exit
headway. Cell 0 is the upstream stopline receiving cell. No car is
admitted if cell 0 is occupied. An already-present receiving vehicle
is moved/discharged before the upstream stopline entry attempt.
Integrated into dual_lane_v11.py through opt-in
receiver_mode="cells"; default receiver_mode="fifo" retains previous
scenario semantics.

**Model scope:** 7m cell and 1s update; fixed speed limit of 1 cell/s,
no stochastic acceleration, merge geometry or pedestrians. The
receiving-link cell coordinates are virtual and don't yet represent
a geometrically surveyed downstream road. This is NOT SUMO/CTM
validation or a calibrated Korean road model.

## Checks and planned experimental design
Legacy v1.4 63 tests + new receiving-link engine 5 + integrated link 5
+ downstream site/provenance 3 = **76 local unit tests PASS**.
Trace audits verify one vehicle per physical receiving cell, mass
conservation including downstream vehicles, red-signal backpressure,
invalid input rejection and FIFO default compatibility.

Exploratory factorial: 4 pocket lengths (14,28,42,70m) × 3 receiving
link lengths (2,4,8 cells) × 4 downstream offsets (0,15,30,45s) ×
2 green durations (15,30s) × 6 seeds (0–5) = **576 simulations**.
All cells reuse the same per-seed upstream generated demand.

With 4 receiving cells, green 30s per 60s, 720s horizon,
left-turn demand share 30%, 1500 veh/h and B lane split 50%:
| Downstream phase offset | Total network out, 14m pocket | 70m pocket | paired gain |
|---|---:|---:|---:|
| 0s | 122.667 | 155.833 | 33.167 |
| 15s | 134.000 | 143.500 | 9.500 |
| 30s | 100.167 | 108.500 | 8.333 |
| 45s | 96.000 | 119.500 | 23.500 |

Independent **input-seed holdout**: 20 previously unused seeds 100–119,
2 link lengths (2,8), 2 pocket lengths (14,70m), 4 offsets =
**320 additional synthetic simulations**.
For 2-cell receiving link, mean paired gains at offsets
0/15/30/45s = +32.75/+10.15/+4.25/+24.05 network exits,
with all 20 seeds nonnegative in each condition. This validates
stochastic-input robustness *inside this same model* but does NOT
measure real-world uncertainty or establish external validity.

A FIFO vs cells experiment must hold the downstream signal schedule
fixed before attributing differences to the spatial discretization.
Earlier raw FIFO vs cells outputs under unmatched signal schedules
are NOT a causal mechanism comparison.

## Provenance interface
site_link_v15.py extends the earlier site_v11 schema with five
integer-valued, provenance-annotated receiving-link inputs and a
"cells" mode selector. A labelled field observation does not confer
calibration. Synthetic example:
fixtures/synthetic_two_signals_v15.json.

## Tested code vs remote repo bytes
Source files and local 76-test receipt were executed in a local copy
of the prior T2 bundle, with new v1.5 amendments. Commits on GitHub
were made through the authenticated connector, not a Git checkout in
the execution environment. No verified byte-equality certificate
between the remote GitHub source and the executed local source exists.
Do not upgrade 76 local PASS to GitHub-HEAD CI status.

## Remaining decisions
1. Independently inspect exact remote branch source and rerun 76 tests
   from a developer machine without GitHub Actions.
2. Replace the receiving single-lane abstraction with real downstream
   lane inventory and lane-to-lane turn routing if field evidence calls
   for it.
3. Use safe aggregate observations of actual signal phase, queue and
   turning counts, held-out periods and explicitly measured road
   lengths for model calibration/validation.
4. Compare interventions by through, left, total network completions
   and queue-integrated vehicle-seconds, not a single favorable metric.
