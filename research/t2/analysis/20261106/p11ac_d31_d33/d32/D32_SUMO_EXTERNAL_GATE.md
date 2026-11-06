# D32 — Independent SUMO reproduction gate

Date: 2026-11-06. Status: **HOLD — no actual SUMO run.**

The current runtime was checked for `sumo` and `netconvert`; both are missing. `src/sumo_gate.py` generates synthetic two-input/one-output junction nodes, edges and route XML. XML creation and deterministic SHA receipts are tested, but the *network cannot be called a SUMO result* until `netconvert` compiles it and `sumo` returns successful tripinfo. `run_if_available` records `NOT_EXECUTED`, avoids synthetic stand-ins and never writes fake tripinfo.

**Important:** the 100m SUMO lanes in this preparatory scenario are NOT physically equivalent to D30's A/C links of 24m and downstream S of 25m. Therefore, even a future SUMO run of these files alone would be a pipeline smoke test, not an independent comparison. Equivalence must be engineered through lane length, speed, departure time, vehicle length, gap, acceleration, traffic lights, bus dwell, insert delays and routing before claiming model parity.

Official definitions: https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html and https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html . `depart`, `departDelay`, `arrival`, `duration`, waitingTime and timeLoss are distinct. D29 existing validation rejects mismatched IDs, malformed tripinfo and silently omitted agents; incomplete trips are not to be treated as zero delay.

This work provides an independently executable *scenario recipe*, NOT a verified external benchmark. We still need actual SUMO binary and raw output bytes SHA-256, platform/version, configuration, and observed traffic measurements.
