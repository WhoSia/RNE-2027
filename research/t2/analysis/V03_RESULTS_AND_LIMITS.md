# T2 v0.3 — Result manifest and next causal design

Status: LOCALLY EXECUTED / REGRESSION COMMITTED / NOT PHYSICALLY VALIDATED
Date: 2026-10-30

## Reproduction
Run from repository root:
```bash
python research/t2/spatial_v03.py
python -m unittest discover -s research/t2 -p "test_spatial_v03.py" -v
```
Python standard library only. Fixed seeds 0..9, 4200 seconds per run,
storage_ft=100/200/400/500, other defaults in Config.

| seed | 100ft | 200ft | 400ft | 500ft |
|---:|---:|---:|---:|---:|
|0|1960|2021|2066|2071|
|1|1944|2007|2054|2054|
|2|1979|2027|2071|2083|
|3|1964|2017|2034|2035|
|4|1980|2027|2062|2063|
|5|1937|1979|1994|2013|
|6|1958|2021|2048|2049|
|7|1937|1976|1993|1993|
|8|1952|2020|2035|2036|
|9|1968|2019|2056|2059|
|mean|1957.9|2011.4|2041.3|2045.6|

Paired 500ft minus 100ft: [111,110,104,71,83,76,91,56,84,91].
Mean = 87.7 vehicles; sample SD approx 17.59 vehicles.
These ten seeds are numerical sensitivity cases, not independent field measurements.

## Confounding identified
Currently fork = -(storage_ft/25)-1; changing storage changes fork coordinate.
Thus the observed result is a COMPOUND geometric contrast and cannot
identify the causal effect of storage capacity alone.
The upstream/downstream interface may still contain discretization artifacts.
There is no proof of universal monotonicity, no field calibration, and no
source-paper Figure 2 trajectory replication.

## Next scientific gate
1. Declare two interventions separately: (A) fixed fork coordinate with
   a storage-capacity cap; (B) physical bay-length change that necessarily
   relocates the fork. Explain that (A) is an abstract capacity experiment.
2. Confirm every vehicle moves only forward in global coordinate, has
   unique lane ownership, and preserves the minimum headway at transfers.
3. Use matched arrival streams and signal schedules for each intervention.
4. Record branch/case IDs and lost-green time; trace the first distinct
   event between counterfactual runs.
5. Compare with an independent simulation implementation (SUMO later).
6. Claim only the propositions supported by a specified model and experiment.

Drive research ledger:
https://docs.google.com/document/d/10nj0pmvCF4BnJ_9o0wxdHzxLBQ0ZYziRW6KfXP7xwrk/edit
