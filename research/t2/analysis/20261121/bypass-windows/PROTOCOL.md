# Does the timing of a bypass opportunity change the preferred phase?

Retain the previous 768 arrival streams, four storage conditions, decision
tick 84, horizon 336 and terminal cost 60. Compare three masks with exactly
six eligible ticks, all in [84,96): first six, last six, and alternating
even ticks. A mask is imposed in both approaches, before service, and
applied to both candidate orders. Only the first waiting straight vehicle,
when immediately behind a blocked left-turn head with pre-service room,
can use it. Outside the mask strict FIFO applies. Mask counts are eligible
ticks, not realized overtakes, available vehicle gaps, or field rates.

Compare rank changes between every pair of equal-count schedules at matched
arrivals. Then pool the three schedules while holding pre-decision arrival
prefix and occupancies fixed. Compare no extra information, exact schedule,
exact future arrivals, and both, using worst-case regret over compatible
cases in each information group. Treat these exact revelations as model
diagnostics. Neither future input is available at the decision in this study.
Report if the calendar comparison leaves an unresolved ambiguity even with
all future arrivals known. Do not use field holdouts.

## Follow-up after the six-tick comparison

No strict reversals were observed across the three six-tick schedules.
Compare earliest versus latest contiguous windows with 1, 2, 3, 4,
and 6 eligible ticks within [84,96). Restrict this follow-up to the
pocket-only storage condition, where the always-on versus FIFO result
previously reversed. Retain all 768 fixed streams. For each count report
tie transitions, cost differences, strict reversals, and the observation
partitions. Label this follow-up separately from the first comparison.
