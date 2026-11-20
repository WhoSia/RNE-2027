# A single arrival-order forecast does not resolve the full counterexample

With penalty 60, 2 of 384 pre-decision information groups admit opposite
optimal orders. Each has eight compatible continuations and no-forecast
deterministic worst-case regret 27. Their cost differences range from
−27 to +346. The earlier matched pair isolated a possible decision flip
but did not establish sufficiency of the order in the bin beginning at 86.

| Exact orders known, by bin start | Worst-case regret in each group |
| --- | ---: |
| None or any single bin | 27 |
| 86 and 88 | 9 |
| 84 and 86, or 84 and 88 | 27 |
| 84, 86 and 88 | 0 |

In the post-protocol joint-message check the error bound applies to the
entire transmitted tuple. On an error the adversary may select any wrong
tuple; no independence is required. Both the two-bin and three-bin
forecast strictly improve on the deterministic baseline only below
27/346 (7.80% conditional error). Against a forecast-free randomized
policy with worst-case expected regret 9342/373, the corresponding
threshold is 27/373 (7.24%). Forecast-conditioned rules here are
deterministic. The randomized comparison is a reference, not an
optimization over randomized forecast-conditioned policies.

Objective sensitivity remains substantial. Without terminal penalty
there are seven ambiguous groups. In three, a perfect 86-bin forecast
alone resolves the order; its tolerable conditional error versus the
deterministic baseline ranges from 9/55 to 13/49. With terminal penalty
120, none of the groups is ambiguous. These are synthetic numerical
bounds, not observed traffic forecast accuracy or field policy effects.

From `research/t2/efficiency_loop` run
`python forecast_information.py /tmp/forecast-information.json`.
Compare to [the full result](results.json). [Protocol](PROTOCOL.md).
