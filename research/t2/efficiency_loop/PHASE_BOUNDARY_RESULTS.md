# Phase-order sensitivity and the value of pocket sensing

**Sign convention.** Delta is leading-left minus lagging-left cost, in approach vehicle-seconds from scheduled departure to observed crossing, capped at the common horizon. Negative favors leading. Each SUMO pair differs only in its phase program. Twelve SUMO pairs and sixty dedicated point-queue settings are in `results/phase_boundary_factorial.json`.

## Same green start times, different service eligibility

At tau 1 s and step 0.25 s, SUMO with yellow gives −99.25; changing the same yellow slots to red gives +7.75. The through contribution stays −131.50 in this pair, while the left contribution changes from +32.25 to +139.25. The first leading left-turn vehicle's crossing bracket changes from 12.00–12.25 s to 59.75–60.00 s. The second bracket crosses the red-to-green boundary, so it does not certify a red crossing. One vehicle's bracket shift explains part of the left total change; other left departures also move.

All six with-yellow SUMO configurations favor leading. Five of six synthetic all-red configurations favor lagging. At tau 0.8 s the red-substitution contrast changes from −38 at step 0.25 s to +10 at step 0.5 s. This is time-discretization sensitivity inside this benchmark. These two steps alone do not establish a converged sign.

At point-model headway 2 s and travel time 10 s, granting 0.25 s of extra service beyond the green boundary moves leading vehicle v01 from 62 s to 12 s and changes delta from +110 to −56. Extending service through all three yellow seconds changes delta to +5 and also changes through movements. The first witness explains the discontinuity at the initial boundary, not the entire factorial. Permitted service in the point queue and replacing the displayed color in SUMO are two distinct interventions.

## Finite storage and the same pre-decision information

Each of the 400 D51 contexts has the same admissible arrival paths and true pocket-count partition across five service calendars. The 5 s intergreen changes the best strict regret-minimizing choice in 12 of 200 contexts at capacities 1–2 and in 4 of 200 at capacities 3–4, relative to the original calendar. When the calendar is itself unknown, the controller faces the union of each pocket-count group's cost bounds. Exact count improves the worst regret in 37/200 and 50/200 contexts respectively. Symmetric one-vehicle error helps in 0/200 and 4/200.

Adding three eligible amber ticks has no effect on the unobserved delta intervals in this short early-arrival grid. The 2 s discharge spacing changes 102 and 84 such intervals, however. For an independent late-arrival witness with a single left arrival at tick 11 and a 5 s intergreen, the fixed-input delta is +31 without amber service and −17 with it. The latter result addresses the coverage of the short grid rather than revising its measured outcome.

## Worst cost and worst regret can recommend opposite orders

The objective pilot evaluates the identical compatible worlds by independent enumeration and checks their cardinalities and delta extrema against D51's dynamic program. Across two capacities, two service calendars and fifty information contexts in each panel, the objectives choose opposite orders in 20/200 settings. At capacity one the two calendars each produce 8/50 disagreements. At capacity three they each produce 2/50.

One capacity-one witness has decision tick 6 and two closed three-tick bins each reporting two through vehicles with no left turns. Future count ceiling is two. The worst absolute costs for lag and lead are 147 and 138, so worst cost chooses lead. The worst regrets are 29 and 102, so regret chooses lag. Both comparisons use the same forecast and initial-state alternatives. This isolates an objective difference before attempting a calibrated comparison to Tan et al.'s controller.

## Next validation

Extend the finite-pocket arrival window to deliberately include arrivals by the first phase boundary. Evaluate the same instances at finer time steps in a microsimulator. For DLR review, record whether each crossing bracket overlaps yellow or the first sample of green; match traffic movement and detector boundary first. Reviewers classify the occupied-path mechanism separately. No held-out DLR cases were opened in this cycle.

```sh
python -m unittest discover
python phase_boundary_experiment.py /tmp/t2-phase-run /tmp/t2-factorial.json
python pocket_calendar_experiment.py /tmp/t2-pockets.json
python objective_comparison_pilot.py /tmp/t2-objective.json
```
