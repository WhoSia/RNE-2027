# T2 v5.2 — turn-pocket integration: tested results & limits

**Execution date:** 2026-11-02. Local authoritative artifact is `T2_v52_turn_bay_research_20261102.zip` (SHA256 `beec6b99f74ef3dee46c184fc0f4ce61e6efddb70585b3889f078b6c1c6bceda`), 21 files, including Python source, tests, CSVs, SHA256 manifest and both audience-specific narratives.

## Corrected OD semantics
Initial model wrongly treated the final downstream M2 completion as a turn exit, forcing every through vehicle into terminal pocket P2 and exaggerating geometry effects. That run was discarded. The corrected network distinguishes intermediate main_exit from terminal main_outflow and prohibits any P2 pocket. Physical bay geometry `PocketGeometry((L0,L1,0))` is simulated only at J0 and J1.

## Core implementation
A vehicle changes from common main lane into a separate turn pocket only if it has an exit destination, is at or beyond the pocket entrance, pocket occupancy is below floor(length/6.5m), and pocket tail gap allows entry. A full pocket leaves the exit car in through lane and impedes following cars. Instant lateral change and a shared main signal stage remain simplifications. A shared junction release clock prevents multiple conflicting crossings in one 0.5s tick. Vehicle, gap, conservation, travel-time exposure and feasible-stage invariants are tested.

## Executed verification
46/46 tests pass: 37 v4.9–v5.1 regression checks adapted to the corrected model plus 9 new pocket-specific tests. Zero-bay counterfactual exactly matches v5.1 on selected counts, vehicle-seconds, blocked transfers and release events.

## Exploratory: 288 paired synthetic runs
L = 15,30,60,90m × demand = balanced/main_peak/side_peak × policy = fixed_32/coordinated_32/main_priority_38 × seeds = 11,29,41,73,101,137,151,179. Demand manifest fixed within seed. Horizon 440s; arrival window 260s; dt 0.5s. All exposure reconstruction errors 0.0.

## Replication: 144 runs with 8 new seeds
L in 15,90; seeds 211,233,257,269,307,331,353,389. For all nine demand-policy combinations, average 90m−15m vehicle-seconds is negative. Fixed32: balanced −341.6 [−559.0,−124.1], main_peak −345.7 [−429.5,−261.9], side_peak −416.4 [−550.3,−282.6] approximate 95% t CIs based on 8 matched synthetic seed differences. These are NOT field confidence intervals. For 90m side_peak, coordinated_32 mean vehicle-seconds 19679.375 vs fixed_32 19738.0; paired difference −58.625 with approximate CI [−534.0,416.8]. Thus no stable evidence of a different best policy.

## Unresolved fidelity gates
Real turn geometry vs abstract branch; explicit protected turning stage and conflict graph; realistic lateral maneuver + taper and mixed vehicle lengths; calibrated demand; SUMO independent check and field holdout. No countrywide improvement, field forecasting or traffic safety claim is warranted.
