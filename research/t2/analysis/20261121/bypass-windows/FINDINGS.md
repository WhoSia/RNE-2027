# Bypass timing matters when opportunities are scarce

## Cycle 1: fixed number of opportunities

Across 18,432 runs with six eligible ticks, early, late and alternating
windows produced no strict phase-rank reversals and no ambiguity
in the pooled 384 groups. Magnitudes still changed: in pocket-only
storage, early versus late changed the paired cost difference in
240 of 768 streams. The eligibility mask is exogenous and shared
by both approaches. A tick counts even if no vehicle can use it.

## Cycle 2: fewer opportunities

The separately registered pocket-only follow-up added 15,360 runs.
Each row compares 768 complete arrival streams. All had the same
pre-decision history for the paired early and late intervention.

| Eligible ticks | Strict reversals | Changed cost difference | Ambiguous groups of 96 with schedule unknown |
| --- | ---: | ---: | ---: |
| 1 | 4 | 144 | 2 |
| 2 | 8 | 272 | 2 |
| 3 | 0 | 240 | 0 |
| 4 | 0 | 368 | 0 |
| 6 | 0 | 240 | 0 |

In the low-count follow-up, a snapshot of eligibility at tick 84
identifies the early/late schedule by construction. Knowing that
schedule still leaves two arrival-based ambiguities per count.
Knowing the complete future arrivals alone leaves one ambiguous group
at count one and two at count two. Knowing both eliminates ambiguity
in the enumerated cases. The exactly known full schedule and arrivals
are diagnostic upper bounds on available information.

For seed 17, midday dispersed, order bits all zero, a single eligible
tick at 84 gives −3 and one at 95 gives +35 left-first minus through-first.
Two consecutive eligible ticks at the early and late ends give −3 and +139.
The component check for one tick is +57 versus +95 in within-horizon
queue/occupancy area, and −1 in terminal unfinished count for both.
Thus the phase reversal at penalty 60 is absent when the terminal
penalty is zero in this witness. Three eligible early ticks admit an
eastbound straight vehicle at 86 under through-first, which is not
available under the one-/two-tick early mask. The effect is conditional
on the modeled FIFO relaxation, fixed 336-tick horizon and objective.

## Cycle 3: field and exhibit decision

The demonstration now has a second fixed scenario, separate from the
previous eight-world case. The presenter changes the number of eligible
ticks and compares early and late placement using the same arrivals.
Present the no-reversal six-tick control next to the sparse case. Field
data should record when gaps can be seen, where the waiting vehicle
is, and when a driver actually takes a gap. See the [field worksheet](FIELD.md).
This is evidence for what to measure, without an estimated field effect
or opening the K047 holdout.

From `research/t2/efficiency_loop`:
`python bypass_windows.py /tmp/bypass-windows.json` and
`python scarce_bypass.py /tmp/scarce-bypass.json`.
Compare against [six-tick results](results.json) and [scarce results](scarce.json).
