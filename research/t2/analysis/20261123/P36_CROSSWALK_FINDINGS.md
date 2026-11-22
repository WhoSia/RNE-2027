# P36 — Nighttime east-approach transfer

The frozen P34 geometry and P35 timing outputs join one to one across 17 candidates. Four nighttime east candidates use mapped lanes −3/−4 (group 3 hypothesis), and one uses lane −2 (group 4 hypothesis). The remaining 12 candidates lack a documented mapping in this analysis.

All five east candidates have a prior observation at most 1 s old at the bracket end. Two have discordant samples for some signal group, but zero have discordant samples for the hypothesized controlling group. This distinction matters when screening for observation ambiguity. Identical endpoint codes alone cannot certify the intervening phase.

This run transfers the movement/geometry correspondence in the earlier daytime audit. The nighttime trajectories have not been independently traced into the expected connectors, and the geometric gate is not a 2023 physical stripe survey. The audit does not establish field blockage, a continuously displayed phase, or actual movement-specific signal control. Next physical check is tracing the five nighttime candidates to the west and south receivers, keeping missing or fragmented tracks in the denominator.

Run with the hash-locked P34-OBS reproduction ZIP:
```sh
python p36_crosswalk_transfer.py /path/to/P34_OBS_20261122_REAL_DLR_STOPLINE_REPRO.zip P35_FORWARD_ONLY_TIMING_FULL_20261123.json
python -m unittest -v test_p36_crosswalk_transfer
```
