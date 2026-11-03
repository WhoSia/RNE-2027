# T2 v6.7-P1 — Special researcher reviewer conclusion

Decision: **APPROVE experimental integration; HOLD real-world physical validity and signal-policy superiority.**

47 historical v6.6 regression tests and 9 new P1 tests pass in one invocation = 56. These tests span heterogeneous vehicle length/dynamics, class assignment reproducibility, receiving-meter proxy, signal-exclusive WALK, conservation and sampled geometry. 48 synthetic factor runs at 360s, none all-complete. The outcome is an exploratory interaction among vehicle mix, storage and signal service, not a claim of traffic science novelty.

The project already has a separate v6.7-P0 mesoscopic study in the 20261104 Docs that reports 256 simulations and 12 tests. **Do not sum those figures as if they came from the same integrated 2D simulator**. P1 is a distinct subsequent integration experiment with its own source and bytes.

Missing: exact 2D footprint occupancy during fractional time intervals, arbitrary opposing concurrent compatible movements, empirical discharge headways, real crosswalk occupancy, downstream physical queue spillback, independent SUMO replication. Additional randomized rare-boundary tests should target green-phase changes and full storage to avoid false universal compliance claims.

Dated byte identity: T2_v67_P1_mixed_fleet_storage_pedestrians_20261104.zip (17 files); archive SHA-256 4b27cffaac09ea37888c1af1aedbb6af4d147c04ed5605e1e85f253b02bfde53. GitHub research notes do not replace full source ZIP; GitHub Actions[bot] is not a contributor.
