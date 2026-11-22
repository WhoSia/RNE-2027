# P37 — Nighttime route and prior sampled signal evidence

All five east-approach candidates were carried forward from P34. The original map, nighttime trajectory and signal files passed their P34/P35 SHA-256 checks. The analysis reused the daytime map raster and direct-sample reader, with competing route cells excluded. The holdout was outside the input window.

| P36 candidate group | Candidates | Expected ordered route only | Alternative ordered route | Neither |
| --- | ---: | ---: | ---: | ---: |
| 3, straight to west | 4 | 3 | 0 | 1 |
| 4, left toward south | 1 | 1 | 0 | 0 |

The counts are unchanged at 10, 20 and 40 seconds. All four straight candidates had ordered hits through the 40–52 m connector band. Three reached both the last connector band and west entry. A receiver-only check also found three, so relaxing the connector sequence does not recover the missing detection.

In the follow-up signal analysis, the latest eligible sample for each candidate group was code 5 (green), including the incomplete straight track. Eligible timestamps are at or before the start of the crossing bracket and at most 1 s old at its end. The codes are sampled support for the transferred group assignment. They do not establish the continuously displayed phase, cause of the incomplete track, or an estimate of green-time blockage. Both route masks and detector depend on the same map and trajectory sources.

The missing west observation survives the widened window and receiver-only sensitivity checks. To test a blockage explanation, the next observation must include queued upstream demand and downstream occupancy at the same time, including green intervals with no departure. The P34 cohort conditions on a crossing and cannot supply that denominator.

## Reproduction

Download the [map](https://drive.google.com/file/d/1j6xu3ngbh1dO75_eCdrgBWVgytRAzGtg/view), [trajectory CSV](https://drive.google.com/file/d/16SyjOzQBy5t9iVIV0tdZaAOlo39jYOri/view) and [signal CSV](https://drive.google.com/file/d/1TXma5bvw_M-NSfqO2LhW7JrEFqANxUOy/view). Supply the original P34-OBS ZIP. From this directory:

```sh
PYTHONPATH=../../efficiency_loop python p37_night_routes.py P34_OBS.zip map.xodr trajectories.csv signals.csv
PYTHONPATH=../../efficiency_loop python -m unittest test_p37_night_routes test_p36_crosswalk_transfer test_dlr_route_evidence
```
