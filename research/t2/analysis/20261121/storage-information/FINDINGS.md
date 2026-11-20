# When storage changes a phase choice and when a snapshot can resolve it

The [registered protocol](PROTOCOL.md) paired 768 fixed streams
(12 contexts × 64 sequences), four storage settings and two orders:
6,144 simulation runs. The time-84 switch follows a common through-first
prefix. In the two plans the queues, scheduled splits, startup, clearance,
downstream calendar and future arrivals agree at the start of the
comparison. The only schedule intervention is the order of the two
protected stages from the switch onward.

## Direct effects of a change in storage

Each row compares strictly opposite signs of the cost difference in
768 matched streams. The model uses one unit of cost per person or
vehicle still in the system for each tick and 60 additional ticks per
unfinished person or vehicle at the horizon. The terminal columns
rescore those same outcomes without rerunning the traffic.

| Newly restricted storage | Terminal 0 | Terminal 60, primary | Terminal 120 |
| --- | ---: | ---: | ---: |
| Pocket with through receiver unbound | 460 | 414 | 416 |
| Through receiver with pocket unbound | 352 | 352 | 352 |
| Through receiver with pocket restricted | 132 | 190 | 192 |
| Pocket with through receiver restricted | 0 | 0 | 0 |

The pocket-only and receiver-only restrictions can independently reverse
the order. Effects depend on the other constraint. The zero in the
last row counts sign changes only, and does not show absence of a cost
effect. Sensitivities establish persistence of examples, not identity of
all reversed sequences across penalty choices. The capacities are changed
for corresponding east and west movements together. “Unbound” removes
only these two chosen capacity constraints. The shared-approach FIFO,
protected service, and all other bays and receiving links remain.

## What a snapshot can tell the controller

Of 48 context-and-storage combinations, two admit both choices as
strictly optimal in different compatible worlds. Full/not-full for
either or both east sensors improves the baseline worst-case regret
in none of the 48. Exact counts resolve one combination: in the seed
83 midday dispersed context with both targeted constraints unbound,
east pocket count 3 selects through-first (difference +222), and
count 4 selects left-first (−54). This is information about current
queue state even without a binding pocket capacity. Worst-case regret
falls from 54 to zero in that context. Receiving-link count is zero
in both branches.

The other conflict is seed 83, night, platooned, with only the pocket
restricted. The east pocket contains one vehicle and the east through
link contains zero under either continuation. The entire arrival
history before tick 84 is identical. The first conflicting pair of
minimum Hamming distance differs only in the future bin [86,88):

| East arrivals in that bin | Left-first minus through-first cost |
| --- | ---: |
| Left at 86, through at 87 | −27 |
| Through at 86, left at 87 | +109 |

Every two-tick east movement total agrees. The complete observed prefix
and both exact counts leave worst-case regret 27 in this context.
A policy could compare forecasts distinguishing that future bin, or
consider changing its decision time only after accounting for the
service forgone by waiting. These hypotheses are a new experiment;
the exact future arrival is not an available sensor.

## Research decision

Measure both physical storage mechanisms for the field explanation.
Test observation value separately in the phase-selection model. The grid
does not estimate how often a field controller would see an ambiguous
state: only two contexts are ambiguous, and the family shares a fixed
background and stipulated future count constraints. The next experiment
should vary decision time, forecast bounds and demand without selecting
new cases by the observed sign. The two current conflicts remain
examples to recheck, not a basis for a universal sensor prescription.

From `research/t2/efficiency_loop`:

```sh
python storage_information.py /tmp/storage-information.json
cmp /tmp/storage-information.json ../analysis/20261121/storage-information/results.json
```

[Results, extrema and same-prefix counterexample](results.json).
