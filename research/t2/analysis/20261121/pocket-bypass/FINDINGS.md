# Pocket bypass changes what must be observed

Tested 18,432 runs: 768 complete arrival streams, four storage settings,
three bounded bypass rules and two phase orders. Used the [frozen
protocol](PROTOCOL.md) and the same demand and terminal penalty (60) as
the previous forecast experiment.

| Bypass reach | Ambiguous groups if rule is known (all storage settings) | Strict phase reversals vs FIFO (pocket-only, of 768) |
| --- | ---: | ---: |
| 0 | 2 / 384 | 0 |
| 1 | 0 / 384 | 158 |
| 3 | 0 / 384 | 222 |

The two original ambiguous groups were found only in the FIFO model.
In the eight-world exhibit group, cost difference (left-first minus
through-first) ranged from −27 to +346 at depth 0, from −932 to −720 at
depth 1, and from −484 to −408 at depth 3. Immediate bypass is an upper
availability sensitivity with no gap check, not a calibrated traffic model.

## Access uncertainty with exact arrivals

If the permitted bypass depth is unknown, 222/768 streams in the
pocket-only setting admit opposite signs **at the same complete arrivals
and observed east occupancies**. This count is zero for each of the
other three storage settings. The count measures matched synthetic
streams, not probability. In a representative exhibit stream whose
future orders are [0, 1, 1] (0 through first, 1 left first), the difference
is +176 under FIFO and −830 under depth 1. Thus even the entire arrival
sequence cannot decide the better order if the model's bypass access
is unknown.

## Exhibition decision

Keep the original FIFO example as a selectable baseline. After revealing
all three orders, switch the allowed bypass depth without resetting the
case. The reversal then motivates a direct field observation:

1. Can the first straight vehicle reach the open lane beside the blocked
   left-turn queue before the back of the pocket?
2. Is a gap available in that lane at that moment, and do markings or
   lane geometry allow the maneuver?
3. Did the driver take it, remain stopped despite an opportunity, or is
   the relevant area outside view?

Two observers can mark these separately in the same camera window.
Availability and uptake are distinct. Future refinement may compare
intermittent safe openings; avoid treating geometry alone as proof a
vehicle could pass at every tick. K047 holdout remains sealed.

From `research/t2/efficiency_loop` run
`python pocket_bypass.py /tmp/pocket-bypass.json`.
Compare to [the full result](results.json).
