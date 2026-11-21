# T2-P27 — Exploratory longer left-stage opportunity test (2026-11-22)

Declared after reading P25/P26 results, **not preregistered independently of all prior evidence**. A diagnostic 13-world pilot already probed the action lengths 6,8,10,16,24s (at receiver discharge headway1–4) and found some meaningful changes only when allowing 24s. Any later 24s efficacy count is therefore **exploratory / hypothesis generating**, not a fresh confirmatory threshold discovery.

The earlier P26 6/8/10s flat response is retained, not silently modified to yield a positive effect. This new experiment explicitly tests whether 24s of abstract model-left-stage can access a later service opportunity in a **different** synthetic world. The model 3s `-` transition is not actual yellow/all-red/pedestrian clearance and the 24s action has **no operational authorization**.

## Cohort, interventions, outcome
- Same 4 P25 frozen demand tapes and 64 geometry classes (2 receiver capacities × 2 offsets × 2 pocket lengths × 2 B-share values).
- Two baseline receiver headways, **1s and 2s**: 128 worlds. Each has a frozen t84 checkpoint and same future tape.
- Within each world compare no intervention, abstract left-stage **6,10,16,24 seconds**, at time87 through `87+length`; clear `84–87` and `87+length–120`. This checks exactly 3s model no-service entering the stage and a later no-service, but **not real signal constraints**.
- Primary: score delta at terminal penalty60. Secondary: policy occupancy and per-run physical crossing events in the model at t87–120; distinguish **true new stopline crossing** from changes in aggregate denial attempt counts. Require frozen P19 delta for 8s action as an independent *holdout sentinel* on the headway2 worlds, even though 8s is not part of the P27 treatment sweep.
- Report per-headway dose curves, strict monotonic/nonmonotonic comparisons, earliest dose with changed effect relative to 6s (among *tested discrete lengths only*), and 24s vs6s ranking changes.
- No population inference: four unique full arrival tapes re-used in 128 worlds; no p-values or independent sample claim.

## Falsification conditions
One fixed-checkpoint hash per world, immutable on each resume; all action variants pass built-in phase validator unchanged; demand and vehicle conservation consistent. If all doses tie, publish no added value. If 24s changes policy outcome, **do not assert that extra green caused more discharges without comparing actual traced `stopline_cross` events**. Opposite preference signs across different headways are not same-state causal; within-world action comparison is model-only paired.

Scope: synthetic offline experiment; no SUMO physical matching, real signal actuator, K047, RF CSI or unauthorized road alterations. No GitHub Actions/bot.
