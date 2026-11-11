# T2 D46-C — 2026-11-11: finite-buffer causal-order and time-step bias

**Experimental gate: SYNTHETIC CONTRACT PASS; FIELD/SUMO/POLICY HOLD.**

## Mechanism
A minimal two-link fluid corridor with downstream finite storage K=6, and deliberately unbounded upstream queue:
- transfer at t = min(opening upstream inventory, upstream transfer capacity, downstream free space at opening);
- sink exit at t = min(opening downstream inventory, sink discharge capacity);
- outside arrivals, transfer and sink exit update inventories at END of step.

Opening-stock update prevents same-step multiple-link teleportation, but a conservative synchronization delay may artificially reduce throughput. This is a model convention and does not establish the physical optimum.

## Frozen A/B experiment
40 steps, 3 cars/step arriving for first 25 steps (75 total); upstream transfer cap 4 cars/step.
- Open sink cap 4 throughout: exits 75, residual 0, maximum upstream queue 3, blocking steps 0.
- Restricted sink cap 0 for steps 0–9, 1 for 10–29, 4 for 30–39: exits 50, residual 25, maximum upstream queue 55, blocking steps 32, first blocked step index 3.

Physical interpretation: a synthetic downstream discharge restriction can block upstream transfer under finite receiving capacity. This **does not** demonstrate a spatial queue-tail velocity or an observed DLR spillback event. A sum of "blocked transfer capacity" across time is *not* a count of unique unserved vehicles.

## Grid-refinement result with IDENTICAL PHYSICAL RATE SCHEDULE
|h|exit over [0,40]|residual|peak upstream|first blocked time|
|---:|---:|---:|---:|---:|
|1|50|25|55|3|
|0.5|60|15|54.5|2.5|
|0.25|60|15|54.25|2.25|
|0.125|60|15|54.125|2.125|
|0.0625|60|15|54.0625|2.0625|

Each step uses h-scaled arrival/transfer/exit rates; physical schedule and K unchanged. All cases maintain exact vehicle conservation but the coarse h=1 produces **10 fewer exits** than h<=0.5. This directly shows that **conservation success is insufficient to validate throughput**, especially when event timing and storage reopening are modeled by discrete synchronous updates.

Smaller-grid plateau is only evidence at these trial values; it is not proof of the exact physical solution.

## Evidence / code
- 32 legacy D46 regression tests PASS, 15 new corridor contract tests PASS, 4 dt tests PASS = **51/51 executed**.
- Independently verified ZIP MANIFEST SHA256 entries (20 files) and package SHA256 `f288cec1f7139346447ad5a67833162dec5996d0264990d3ab0d5e25670163b0`.
- Reproducibility archive: https://drive.google.com/file/d/163YfvCqtN4O26ZzWIjlSWx8lOAOwT5K7/view
- Native research record: https://docs.google.com/document/d/1ZZPfPZXyHazuLiSqOowHQfSRecseZtzSY1gn1EEOhqc/edit
- Source and tests: `research/t2/analysis/20261111/d46/d46c/` on `research/t2-spatial-fig2-v02`. No GitHub Actions[bot] contribution.
- DLR 45min observed movement counts (1409) are not demand, receiving supply, or validation values for this experiment.

## Next scientific gates
1. Finite *upstream* storage and explicit externally queued/rejected arrivals; geometric queue-tail detection, with actual spatial displacement.
2. Event-time refined reference that enforces causal ordering without artificial one-step delays; investigate h=1 model bias.
3. D44 physically feasible braking successor and independent pinned SUMO execution under identical inputs.
4. D42 exact finite stopline and movement mapping with UNKNOWN/censored observations; only then inject empirically grounded capacity uncertainty.
