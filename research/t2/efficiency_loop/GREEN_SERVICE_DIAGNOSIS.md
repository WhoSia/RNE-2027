# Through-service diagnostics under two storage constraints

## Design

At a scheduled protected-through service opportunity, log actual entry,
a through vehicle ready in the stop-line bay, a full through receiving
link, and this separate upstream signature: a left-turn vehicle at the
shared FIFO head, a full left bay and a through vehicle behind the head.
An occupied left bay alone cannot identify obstruction. Log from the
same pre-service frame, so simultaneous downstream discharge does not
silently become space already available to the upstream controller.

Use the paired daypart arrivals for seeds 17 and 83. For each demand
world, cross left-bay capacity 1 or 5 with through-receiving capacity 2
or 12 in both directions. Leave left receiving storage, downstream
signal, transit speeds and other capacities fixed. Compare left-first
and through-first at the same green allocation. Signs and magnitude of
effects need not be the same across demand worlds or plan orders.

## Interpretation

Retain six mutually exclusive labels. Actual entry comes first.
Otherwise, a through vehicle at the stop line plus full receiving link
means downstream blockage, possibly accompanied by a shared-FIFO
signature. With no stop-line through vehicle, report the shared-FIFO
signature separately, including whether downstream space also was
unavailable. Pending upstream demand with neither diagnostic signature
remains a separate case, as does no through demand at all.

The shared-FIFO signature is evidence of upstream queue obstruction
in the model, not a claim that removing the left head would permit
a same-tick stop-line crossing. A joint signature does not identify
which constraint a real vehicle would have reached first. All results
in this sweep are synthetic, and no DLR held-out inputs are used.

For repeated field annotations, timestamp the through phase and record
stop-line presence, actual discharge, fork FIFO order and receiving
entry room independently. Unknown coverage, an uncertain phase
transition, or unverified lane mapping must remain unknown. Do not
substitute counts from a later interval for contemporaneous occupancy.

## Results

The 96 synthetic runs cover 12 demand worlds, two phase orders and
four capacity pairs. Each capacity pair contributes 2,688 scheduled
through opportunities across both directions. All labels are counts of
opportunities, which can repeat for an individual vehicle.

| Left bay / through link | Served | No through demand | Upstream pending | Pocket signature | Downstream blocked | Joint signature |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 / 12 | 1,207 | 725 | 60 | 683 | 4 | 9 |
| 1 / 2 | 666 | 141 | 27 | 174 | 1,237 | 443 |
| 5 / 12 | 1,440 | 996 | 91 | 150 | 0 | 11 |
| 5 / 2 | 714 | 149 | 33 | 0 | 1,774 | 18 |

With left bay 1 and through link 12, left-first is cheaper in all 12
worlds. With left bay 5 and through link 2, through-first is cheaper in
8 of the same 12 worlds. Comparing the two corner cases changes both
storage settings, so this is a rank reversal across conditions, not
a one-factor explanation. In the small through link cells, enlarging
the bay decreases the joint label and increases the downstream-only
label. A change in either label by itself is a poor measure of total
delay or real-world benefit.

Reproduce with
`python green_service_experiment.py ../analysis/20261117/green-service/grid.json`
from this directory. [Paired simulation data](../analysis/20261117/green-service/grid.json)
retains per-cell costs and pre-service examples. Dayparts and storage
conditions in this run are synthetic settings, and the protected-stage
model does not implement a shared downstream lane, calibrated vehicle
dynamics, or a spatial blocking event at the stop line.
