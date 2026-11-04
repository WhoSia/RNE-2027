# P5 Stopline microstate forensics

Immutable prior P3 source: `network_v67_p3_prior.py`. At seed943, walk exclusive 8s, storage30/100m, truck id1 at t=36.50s had front x≈118.9554m (line 120m), v≈3.3465m/s, class braking limit 2.2m/s². Diagnostic `failed_stopline` time ticks 147/148 (t=36.75/37.00s) had x≈120.3536m and 120.9449m on the same truck, NOT two independent vehicles/crashes.

Existing controller uses an anticipatory turn-speed limit `v>limit-1.5` to force max brake even when speed is still below the instantaneous turn-speed envelope. A first rejected candidate removed margin for BOTH straight/turn and eliminated this failure but created `unreachable_turn_speed` ticks in straight movements.

Second candidate keeps original straight behavior and changes ONLY side-turn threshold to `v>limit+epsilon`. This resolves the witness within its tested setting, but is heuristic, not a reachable-set/controller proof. Retain prior P3 as canonical. Do not claim safe stopping.