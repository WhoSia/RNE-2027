# T2 v6.4-P1: Temporal demand sensitivity (20261103)
Source v6.2-P2 single-junction synthetic testbed. 108 new vehicle simulations: 3 demand regimes x 6 seeds x 3 arrival profiles x 2 guard policies. The same vehicle IDs, OD labels and counts, but different birth times: uniform Bernoulli, later-concentrated t_new=T*sqrt(t_old/T), or 12-second platoon compression. NOT actual measured peak or platoon arrival.

At H=155s, the extra 1-second guard increased mean accumulated exposure vs no guard by +3.889 / +6.611 / +2.903 vehicle-seconds for uniform / late / platoon respectively, each 18 demand-seed blocks. Sampled braking-warning ticks zero for these particular cases, not proof of safety.

Observation horizon and incomplete trajectories confound comparisons across arrival time distributions. Preserving OD counts alone does not match inflow timing.
All executable source and original CSV: https://drive.google.com/file/d/1jiZf9L9IpcWMQJ-lsnSsCYYuO2oewhZt/view
