# T2 v4.7 — Historical reconstruction and correction (2026-11-02)

Original ZIP sources inspected: v4.4 network.py and experiment.py; v4.6 ablation.py. Reproduced the v4.4 5-step cycle, horizon 50, paired 12 capacity/main-rate combinations and side rate 0 versus 2. Observing exits under the original all-main green baseline (split=5) gives 12 pairs with identical observed totals and disjoint optimizing split sets. The original v4.4 optimum searches splits 0–4, whereas observations use 5.

**Key result:** Holding the historical network and policy candidate rules constant, but observing under split=3 instead of 5, the same paired witness search gives **zero** cases. Snapshot-only still gives 12; restricting optimized splits to minimum green=1 still gives 12; adding a lost tick still gives 12; changing only cycle 5→8 with all-main baseline still gives 12; cycle8 with baseline split3 gives zero. These are finite-grid findings, not general identification proofs. Ten local unit tests PASS.

**Correction to v4.5/v4.6:** disappearance of this constructed witness in the checked scenarios is driven by switching the *baseline observation policy*, not uniquely by signal feasibility or switch-loss or snapshot. Some minimum-green action-set ablations still observe a physically infeasible zero-side-green baseline. The model remains synthetic, with neither true traffic phases nor micro driver behavior.

This suggests investigating observation as a policy-conditioned measurement: baseline green allocation can hide or expose demand heterogeneity. Field data collection must not require unauthorized manipulation of public signals. Next: fully feasible independent signal stages, movement conflicts, realistic OD/IDM/SUMO, day-separated Gyeongnam validation.

Reproducible local package (10 tests, 11 scenarios, CSV and JSON): https://drive.google.com/file/d/1VslSFpJrte6oll7EmFxHsr1RKxB8yKfJ/view ; SHA256 30df1e7fcd76269a585a71d84708611ff6856ffc0909c949dfca9e260c9444d7.
