# D30 — Experimental P12 policy track reopens ONLY in offline sandbox

The student authorized studying signal optimization after the engineering track. We therefore resume **research questions and a clearly limited synthetic comparison**, not a validated field controller or a global optimum claim.

`src/od_and_policy.py` considers 3 prechosen fixed plans for two competing inbound approaches A and C merging onto one finite downstream link S: signal cycle 24 s, green A=6/10/14 s, green C=20-greenA s, 2 s all-red in each transition. Same synthetic OD process, bus mixture and fixed physical model across plans; 4 development seeds (101,103,107,109), 2 untouched holdout seeds (211,223), horizon 260 s, 28 requests each scenario. Do not tune plans using holdout.

Results from this code, **synthetic only**:

| A green | Train mean trip [s] | Holdout mean trip [s] | Train mean A/C gap [s] | Holdout A/C gap [s] |
| --- | ---: | ---: | ---: | ---: |
| 6 s | 45.902 | 47.125 | 45.184 | 43.674 |
| 10 s | 39.920 | 43.125 | 13.243 | 10.820 |
| 14 s | 48.509 | 52.911 | 44.684 | 50.677 |

All 6 cohorts per plan finished in the chosen horizon. **This is not a comparative field experiment**; it is a unit test of controlled counterfactual policy selection. No vehicle safety audit, pedestrian injury model, real detector verification, time-grid convergence or SUMO parity. The use of 10s for the synthetic scene must NEVER be translated into real signal timing advice.

Research next: preregister scenario distributions, multiple independent arrival processes, pedestrian fairness, maximum queue blocking and person-weighted delay, robust Pareto comparisons, independent holdout evaluation, dt stability and SUMO/field transport check. No live actuator or infrastructure interfaces exist.
