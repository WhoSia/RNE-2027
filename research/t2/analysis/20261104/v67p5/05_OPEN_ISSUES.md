# T2 P5 — Open issue register, 20261104

| ID | Priority | Open gate | Verified witness | Acceptance condition |
|---|---|---|---|---|
| T2-STOP-01 | P0 | multi-step stop/go viable control | P3 seed943; new candidate still 885 warning ticks across 46/96 independent cases | no hidden braking-limit violation or stopline penetration in isolated + broad held-out trajectories |
| T2-GEOM-02 | P0 | synchronized swept footprint collision | sample prior 193 geometric overlap ticks | time-coherent continuous footprint audit and independent stress |
| T2-NET-03 | P0 | P3 2D state to P4 network link | mesoscopic bridge only | exact ID, rear/front position, class, pose, velocity, time, no duplicates |
| T2-OBS-04 | P0 | actual road and independent SUMO | no measured traffic input | held-out movement flows, discharge headways, queues and travel times |
| T2-CENSOR-05 | P1 | unfinished vehicle censoring | all 120 development + 192 independent runs unfinished | explicit censored estimand and all-drain cases |
| T2-REG-06 | P1 | version-aware test semantics | legacy bit-identity tests invalid after intentional motion change | preserve old 13 passing separately; new 32 pass independently |
| T2-DOC-07 | P1 | Drive/Docs custody and reproducibility | P4 addendum needed; P5 ZIP connector upload blocked | verified ZIP Drive parent+id+hash; native Docs read-back |

Do not close an issue solely because a simulation test passes. Research date 20261104; none of these are field safety certificates. Original code and all negative witnesses preserved.
