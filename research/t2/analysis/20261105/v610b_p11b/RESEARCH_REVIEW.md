# v6.10-B + P11-B research verdict

**GO for an independent multi-hop prototype. NO-GO for a physically calibrated or production ready simulator.**

New functionality: linked-junction routing, link traversal delay, downstream link storage blocking, conservation ledger, signal conflict constraints, and 96 policy evaluations across fixed paired traffic patterns. Numeric conclusion restricted to eight J1 offsets per scenario.

Tests: 12 new multi-hop + 25 baseline new-kernel = 37/37 PASS. Historical P2 suite = 28/28 PASS. This does not establish that the new kernel fixes the historical P2 v6.9 failure in P10 because they implement different dynamics.

Research caution: The queue storage is reserved at connector admission even when the vehicle is still physically in connector. This is a conservative allocation convention, not a solved continuous spatial occupancy model. Exogenous source queues are unbounded, preventing the model from identifying upstream network queues/gridlock. These are known limits and should not be hidden.

Two-track next: capability extension to externally driven routes and lane-level source blocking; independent SUMO evidence and real-data forecasting. Separate immutable original inputs from derived outputs in shared Drive. Manual user-authored GitHub commits only.
