# New-seed evaluation changes the six-opportunity conclusion

The [registered protocol](PROTOCOL.md) compares four unused synthetic
seed inputs (24 contexts; 1,536 streams at each count) with the original
two seeds (12 contexts; 768 at each count). Across both panels and three
counts, the 27,648 simulations cover two schedules and two phase orders.
Using the recorded area and terminal components to rescore a penalty adds
no new traffic simulation.

| Eligible ticks | Original at 60 | New at 0 | New at 60 | New at 120 | New with same strict reversal throughout [30,90] |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 4 / 768 | 32 | 44 | 36 | 20 |
| 2 | 8 / 768 | 20 | 56 | 32 | 24 |
| 6 | 0 / 768 | 4 | 32 | 24 | 8 |

New-panel columns have denominator 1,536 each. At penalty 60,
affected contexts are 3, 2 and 2 of 24 respectively, all midday dispersed.
Streams share background generators and bin constraints and are not
independent observations. The previous six-opportunity observation remains
correct for the original panel at penalty 60. It is not a stable threshold:
even the original panel shows 8 six-tick reversals at penalty 120.

In the new seed-337 midday dispersed witness with one eligible tick,
early and late left-first-minus-through-first differences are
`−53−p` and `91−p` for terminal penalty `p`. Thus early is −113
and late +31 at p=60, and both signs persist throughout [30,90].
This example reverses even at p=0. The original witness at count one
has `57−p` and `95−p`; it requires 57 < p < 95. Preserve both
examples in the exhibit and do not present the positive cases as
typical. The independent panel only varies seed inputs within the same
generator; a recorded lane-use timeline or independent simulation is
still needed to relate this result to roads.

From `research/t2/efficiency_loop` run
`python timing_generalization.py /tmp/timing-generalization.json` and
compare against [the complete table](results.json).
