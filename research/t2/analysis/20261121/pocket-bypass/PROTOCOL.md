# Is the signal-order counterexample an artifact of strict FIFO?

Hold the 12 existing synthetic demand contexts, 64 within-bin permutations,
four pocket/receiver capacity settings, time-84 decision, objective
(horizon 336, terminal penalty 60), and both signal calendars fixed.
Repeat the comparison with FIFO and with the first waiting straight
vehicle allowed to pass a blocked left-turn head if it is among the
next 1 or 3 positions and the straight bay has space before service.
Apply this to both shared approaches for the entire run, including the
common prefix. One admission at most per approach and tick. Earlier
turns stay queued. This is a bounded overtaking assumption, without
vehicle gaps, acceleration or calibrated lane-changing behavior.

Measure whether an identical observation still admits both strictly
optimal orders. Group by complete varied prefix and pre-decision east
pocket and receiving occupancy within each model. Compare signs across
models with each complete arrival stream matched. Separately track the
two known penalty-60 ambiguity groups from the previous experiment.
Decide whether the exhibition's main example survives a relaxed FIFO rule.
Do not access the K047 holdout.
