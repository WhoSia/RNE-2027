# Paired phase order under pocket and through-link storage

Use the 12 existing synthetic daypart and arrival-shape worlds from
seeds 17 and 83. For each, replace east through and left arrivals on
ticks 78–89 with one east through and one east left arrival per two-tick
bin. Enumerate the two within-bin orders independently in all six bins
(64 worlds per context). All other arrivals and bin counts are fixed
within that context. Before the decision at tick 84, only the first
three bins are closed. Treat the final three bins' count constraint and
the unchanged background as stipulated bounds in this finite experiment.
Do not treat them as field forecasts or as future measurements.

For each world, compare the existing protected through-first and
left-first schedules, changing only the schedule from tick 84 onward.
Use the same through-first schedule on ticks 0–83. Read east pocket and
east through receiving-link occupancy at the start of tick 84, before
that tick's arrivals or service. Assert that the controller sees the same
state under both orders. Start the common prefix with the existing empty
initial condition. Retain the cost difference in weighted vehicle ticks,
including the model's existing terminal penalty.

Set east and west left pockets to capacity 1 when restricted and east and
west through receiving links to capacity 2 when restricted. An unbound
constraint uses one more than the world's total arrivals. All other
capacities, signals and shared FIFOs remain as in the existing model.
Compare all four storage combinations and count strict phase-rank
reversals along a single storage edge for the same input sequence.
Do not interpret a corner reversal as a one-factor result.

At each storage combination and context compare these pre-decision
observation partitions: no added observation, east pocket full/not full,
east through receiver full/not full, both bits, and both exact counts.
All cases retain the same compatible worlds. For each branch record
extrema of left-first minus through-first cost, the best deterministic
worst-case regret, and whether one order is weakly optimal throughout.
Use the maximum over the nonempty branches for each instrument.
Record one matched pair of sequences with strict opposite choices where
available. A positive change in this grid is a modeled possibility and
a zero change is limited to the tested family.

This is a synthetic within-model comparison. Do not open K047's
18:00–18:30 UTC holdout for this experiment.
