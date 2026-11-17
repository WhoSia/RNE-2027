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
