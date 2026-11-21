# T2-P20 — Independent event-ledger physical audit and model-comparison gate

Date: 2026-11-22 KST. **Result: PASS for internal event consistency in an uncalibrated synthetic engine; external SUMO or real-road physical agreement NOT VERIFIED.**

## Question and provenance
After P18 exact-main PHYS-04 replication and P19 downstream-offset moderation, can we reconstruct each vehicle's receiver entry, cell motion, departure and network conservation from independently written transition logic, rather than trusting only engine end totals?

The canonical input code is pinned to `WhoSia/RNE-2027` `main`:
- `dual_lane_v11.py`, Git blob `a7c9aa6954402e12894d1d5b722e8a474b0bd58f`
- `receiving_cells_v15.py`, blob `b078cf215c74b76ace6dffcbcbacab6ae22c3673`
- P19 original `p19_receiver_service_opportunity.py`, blob `760fd8ce81f1e56d02b1707e5e2fef8d4720f4d1`

P20 implementation: [independent event-ledger auditor](p20_independent_receiver_ledger.py), exact remote blob `9aff64b943407692c1d8364994c7c840ee9bb223`; [9 regression tests](test_p20_independent_receiver_ledger.py), blob `526d250789f7914aa429f264ced35b425b1369a4`; [256-world rerunner](p20_full_256_audit.py), blob `e84fbca3a02ab3c6de7e4dd9032c85ac9c71d61d`.

### What is checked each second

1. Independently step a *separate* cellular receiver automaton: release an occupied last cell when the downstream green and headway allow; move the remaining vehicles forward by at most one cell under synchronous snapshot occupancy; admit actual upstream `stopline_cross` events at receiver cell zero, rejecting double occupation.
2. Compare independently predicted receiver cell→(vehicle ID, movement) mapping against the original engine's frame at every tick.
3. Check vehicle conservation independently from the original arrival tape and reconstructed receiver departures. At each tick, `generated_through_t = outside + approach_A + approach_B + pocket + receiver + cumulative_network_exits`.
4. Check no simultaneous road/receiver vehicle ID, no disallowed longitudinal jumps, no impossible road-to-pocket lane transfers, and recorded pocket-entry/lane-change events against end-of-tick positions.
5. Count rejected receiver admissions and ensure these event counts agree with the engine's recorded aggregate; reject tampered counts and event logs.

These checks cover **observed trace transitions**. They are not a fully independent generator of upstream traffic behavior: stopline-crossing events and frame snapshots originate from the simulator under audit. Matching the same cellular update assumptions tests implementation conformance, not external physical realism.

### Actual execution results

First, a 16-path smoke cohort used two seeds (112, 113), capacities 2/4, downstream offsets 0/15, baseline/intervention. Python 3.13.5 `python -m unittest -v test_p20_independent_receiver_ledger.py` passed **9/9 tests**, including seven distinct corruptions deliberately injected into known-good traces.

Next, rerun the entire P19 256-world experiment, baseline + abstract 8-second intervention = **512 trace paths, 122,880 second-by-second audits**. Independently audited event aggregates across paths:
- Receiver admissions (stopline crossings): **21,898**
- Network exits after the receiving link: **21,546**
- Receiver-entry **denial attempts**: **40,910**
- Distinct complete arrival tape hashes: **16**

The huge denial-attempt total is an event-frequency count. The same vehicle can be denied repeatedly at successive ticks; it is **NOT 40,910 unique obstructed vehicles**.

The event audit completed all paths without a trace mismatch or conservation failure. All **256/256 P19 policy cost differences and tape hashes** matched the previously frozen P19 JSON. The complete P20 output was generated twice byte-for-byte identically: SHA-256 `b8d88c6ed7a771e7b489ae761070d78d88d9970957a7458d7304a33f37a6318b`. The P20 source/test exact Git blobs were recovered from remote `main` through a text-only transfer manifest and tested locally: 9/9 PASS. Full source path local `git hash-object` matched remote code.

## External model readiness — not conflated with PASS
SUMO is not installed in the execution container used for these tests. An independent cellular shadow agreeing with a cellular model cannot establish microscopic physical validity. A valid *next* SUMO comparison must freeze:
- Identical intersection geometry, lane lengths, pocket 14/28m, downstream storage 2/4 cells at 7m per cell, signals, and exact timestamped (L/S) demand tape.
- A vehicle route/connection representation, actual yellow/all-red and legal pedestrian/phasing requirements. Existing `L/S/-` phase overrides cannot be transplanted as deployable controller phases.
- SUMO output: per-vehicle FCD trajectories, lanechange events, tripinfo, optional detector/queue indicators, and declared queue definition.
- Compare headway distributions, discharge delay, queue length over time, receiver-entry admission refusals and temporal spillback—not only total vehicles or weighted terminal cost.
- Note model-class differences (T2 1 cell/second ≈7m/s longitudinal motion, fixed 2s nominal headway, synchronous receiver movement versus SUMO's vehicle-following dynamics). These should be tested as **different physical models**, not automatically tuned into numerical agreement.

Official SUMO documentation:
- https://sumo.dlr.de/docs/Simulation/Output/index.html
- https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html
- https://eclipse.dev/sumo/docs/Simulation/Output/TripInfo.html

**Limitations:** synthetic 240s runs; no empirical calibration, no verified real controller feasibility, no actual SUMO run, no physical RF measurement, no causal proof of spillback from occupancy alone. Zero trace mismatches cannot rule out a *shared* physical modeling assumption error.

Next priority: calibrate a frozen small scenario using the **already-owned** DLR-UT raw trajectories + traffic light observations, and then run an independently specified SUMO version with matched geometry and vehicle input; preserve any disagreement as substantive evidence. Original DLR and CityArtery datasets already reside in the Drive dataset lake; do not duplicate download.

K047 sealed, the large CIM ZIP remains metadata-only HOLD pending actual Drive file ID; no GitHub Actions or bot.
