# Daypart signal decisions and paired simulation

## Hypotheses

A time band is information available before selecting a plan. It can be useful
when the distribution of approach demand and pedestrian arrivals changes.
Storage and downstream green alignment can change which plan wins within one
band. CityArtery establishes that its workbook reports different nominal
durations by band, but supplies no validated clock join for trajectory replay.

## Registered comparisons

Use three synthetic bands (night, midday, peak), each with two vehicle-arrival
patterns at exactly the same movement counts (dispersed and platooned). Repeat
each under open and constrained downstream receiving. Give all plans the same
arrivals and physical parameters within each world. The terminal penalty is
60 seconds per unfinished entity. Vehicle and pedestrian weights are initially
equal. Report components and unfinished counts so the choice can be revisited
under explicit pedestrian constraints.

Use a finite candidate catalog with an 84-second cycle, three green splits,
two choices of left-turn order and three offsets. Compare the existing fixed
split, pooled minimax cost, pooled minimax regret and band-specific minimax
regret. Freeze all choices on seed 17 and re-evaluate all policies on seed 23.
This is a synthetic evaluation set. DLR held-out footage remains untouched.

The experiment is evidence about these chosen worlds and this catalogue. Each
phase runs with a 3-second clearance and a 1-second startup, using the existing
protected-stage model. The next field admission check requires geometry,
movement mapping, the signal-state clock and provenance for their join.
