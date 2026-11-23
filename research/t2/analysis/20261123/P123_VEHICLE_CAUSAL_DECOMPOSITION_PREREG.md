# P123 prereg — exact per-ID departure and stopline/receiver-delay decomposition

Committed before run. Following P122's identical aggregate left-green-overlap counterexamples, the next falsifier will test whether total cost differences can be **exactly** allocated to each vehicle and to delay accumulated before/after the upstream stopline. This is an identity audit with mechanistic descriptive value, not an independent physical engine or new statistical generalization.

Frozen original T2 inputs: 900vph, left share .75, one-cell 7m pocket, 4-cell shared receiver, label seeds 86001/86002, P31 uniform/platoon4 60 identities; common t=84 checkpoint; 4800s horizon; all vehicles must clear. P114 original source unchanged.

Specific comparisons, selected before trace replay using P122:
1. 86001 uniform period30 phi0 versus period60 phi28 (equal green-overlap=66, delta network cost +577 vehicle-s).
2. 86001 uniform period30 phi10 versus period60 phi22 (equal overlap=48, delta network cost -2042 vehicle-s).
3. 86002 platoon4 period30 phi10 versus period60 phi57 (equal overlap=48, delta network cost -2537 vehicle-s).
4. **Within-period control** 86001 uniform period30 phi0 vs period30 phi1 (both overlap=66; delta cost -732 vehicle-s), strongest exclusion of period confounding.

For each policy trace, reconstruct each ID's upstream stopline-crossing time (service_events.reason==stopline_cross) and **final downstream exit tick** (difference of consecutive receiver ID snapshots, starting frozen checkpoint). Require identical IDs, movements and arrival times; every ID crosses once and exits once. Compute paired sum of exit-time differences, left/right sums and absolute spread; verify equals `score(short,0)-score(other,0)`. Also decompose for every vehicle into upstream delay difference + downstream (exit minus crossing) delay difference and assert exact closure. Show biggest individual winners/losers, movement net split, and first-100-s trajectory crossing differences. Do not treat vehicle entries as independent statistical samples because shared queues couple their delays.

In comparing **same period phi0 vs phi1**, total left-overlap duration is exactly identical and period is identical; only timing placement differs, so if delta remains unequal it is stronger evidence aggregated overlap is insufficient.

STOP if any trace/score/arrival ID mismatches; record the failure rather than overriding it. Do not infer optimal field control.
