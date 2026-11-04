# P3 matched three-engine replay

130 unit test executions passed: P1a 56; P1b 61; P3 13 (several historical tests overlap in source). Matched replay 36 simulations: seeds941..943, walk0/8s, storage30/100m, engines P1a/P1b/P3. With walk0 P3 matches P1b exactly on all selected runs.

Storage 30m finite horizon 360s, mean completed / total vehicle-seconds:
WALK0: A 26/4617.083, B 20.333/5819.667, P3 20.333/5819.667.
WALK8: A 20/5638.083, B 17.667/6367.500, P3 17.667/6320.833.
P3 fixed walk8 seed943 triggers 2 failed_stopline warning ticks at 36.75 and 37.0s in storage30 and storage100. The passenger/turn interval-WALK intersection test stays at zero for these scenarios. Physically, preventing entry to WALK is not equivalent to guaranteeing upstream stopline viability.

All 36 matched runs are finite-horizon and many vehicles unfinished, so no complete-trip-time claims.