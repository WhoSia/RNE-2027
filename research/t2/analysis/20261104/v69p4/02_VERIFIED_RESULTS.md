# P4 heldout results — 2026-11-04

Run with original P2 code plus P4 addon, tests 37/37 passed (28 historical + 5 ingestion + 4 P4).

In 64 paired synthetic evaluation blocks (8 scenarios×storage conditions and 8 heldout seed IDs):
- exhaustive minus local-independent mean fixed-horizon exposure: **-140.1328125 vehicle-seconds**.
- exhaustive better 35, worse 13, tied 16.
- seed-cluster bootstrap 4000 replicates 95% percentile range: **[-253.21875,-24.0625]** vehicle-seconds, NOT real-world coverage.
- exhaustive minus same-information coordinate descent: **-58.015625** vehicle-seconds.
- coordinate descent failed global training optimum in **1/8** cells, agreed in 7/8.
- all relevant policies fully completed in **57/64** evaluation blocks; 7 blocks have finite horizon censoring.

Other limitations: 8 seed clusters only, four predeclared synthetic demand types, repeated seed IDs across cells, P4 mesoscopic connector excludes concurrent movements; stopline P3/P5 safety failure unresolved. Comparison does not establish field policy uplift or the pure value of network information.

Reproduction: `python -m unittest -q test_corridor.py test_optimizer.py test_coordinate.py test_robust.py test_jinju_ingest.py test_p4_validation.py` ; `python p4_validation.py`. Original archive remains unchanged. Local ZIP SHA256 d76bdfba6a45634e80f752693a3dbfb65c0b39244110e70522f43cb81a0e7819; Drive upload not verified (safety gate blocked).
