# D51 phase-order response around late left arrivals

The prior D51 short-grid comparison found no change in its unobserved interval
when three service ticks during amber were added. The single left arrival at
tick 11 showed a sign reversal under the new rule. This follow-up asks how close
to a service boundary an arrival must be for the reversal to persist and how
queue order and discharge spacing modify it.

## Frozen comparison

Use a 60 s cycle, T24/L12 greens, 5 s intergreen, a 240 s horizon and through
capacity 12. Sweep left arrival ticks 8–18 and 26–35, inclusive, across left
capacity 1 or 3 and discharge headway 1 or 2 s. Fix three demand patterns:

- Single left at t.
- Left at t and through at t+1.
- Left at t−1 and t and through at t+1.

For each setting, simulate all four combinations of phase order (lag or lead)
and amber service (0 or 3 ticks). Service follows the D51 pre-tick queue rule.
All vehicles must complete in each arm. The outcome is total simulated vehicle
delay in seconds, with signed contrast lead minus lag. Count strict opposite
signs separately from changes through a tie, same-sign changes, and exact
invariance. Retain raw arm costs and compare by pattern, headway and window.

This is a mechanism stress test on an extension chosen after the previously
published witness. D51's amber mode gives additional service opportunities to
queued vehicles in the abstract point queue. Driver decisions and actual
clearance dynamics are outside this model. Do not use the DLR field holdout.
