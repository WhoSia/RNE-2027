# D46-F — positive link travel-time event reference (2026-11-11)

**Verdict:** exact-rational discrete-vehicle synthetic reference PASS / independent model-equivalence, field DLR and policy validation HOLD.

## Implemented contract
D46-E modeled continuous fluid with zero internal travel time. D46-F models integer vehicles, finite integer-capacity upstream and downstream links, a **positive minimum residence time** before a vehicle becomes eligible for its next boundary, and exact Fraction timestamp events rather than an Euler/fixed-dt integration step.

At equal timestamp: first register new outside demand, then process sink exit, interlink transfer, then entry, checking FIFO and free space. Vehicle conservation: cumulative outside arrivals − sink departures = outside waiting + upstream occupancy + downstream occupancy. The first time outside >0 is not evidence of spillback because a car may simply wait for its next entry slot.

Fixed example: 75 vehicle arrival timestamps k/3 during (0,25], admission and transfer completion slots k/4, sink completion slots every 1 unit on (10,30] and every .25 on (30,40], downstream capacity 6, upstream capacities Ku={1,2,3,6,8,12}; dwell time tau on *each* link in {0,.25,.5,1,2}. Available sink slots =60.

|Ku|tau=0|tau=.25|tau=.5|tau=1|tau=2|
|---:|---:|---:|---:|---:|---:|
|1|60|60|45|35|18|
|2|60|60|60|44|34|
|3|60|60|60|53|38|
|6|60|60|60|60|50|
|8|60|60|60|60|50|
|12|60|60|60|60|50|

Actual execution: **30 scenarios** (six Ku × five tau), 24/24 new regression/negative tests, fail-closed capacity and conservation invariants. Python standard library only.

## Interpretation and limitations
Even when no fixed numerical step exists, strictly positive link dwell plus limited storage and finite service slots can reduce outflow *in this exact discrete-vehicle model*. Therefore, D46-D vs D46-E differences are not identifiable as exclusively numerical time-step bias: D46-E also changes the physical modeling assumptions. This does **not** demonstrate a field spillback propagation velocity or real signal-controller improvement.

This code has no actual road segment length, acceleration/braking, collision prevention, signal phase constraints, vehicle length variations, spatial queue tails, or empirically inferred arrival/receiving capacities. DLR 1,409 observed movement crossing count units cannot be used as simultaneous true entry demand and receiving supply.

## Provenance
- Exact Python implementation committed to GitHub as `d46f/event_vehicle.py`, Git blob SHA `d81395c32c4c9be33cd787e2efc06a16cde8d383`, byte-matched to the local executed source.
- A 10-file SHA-sealed ZIP with exact runnable code, 24 tests, scenario CSV and JSON, test log, environment, source/research note and manifest was generated locally:
  `RNE_T2_20261111_D46F_POSITIVE_TRAVEL_EVENTS_V1.zip`
  SHA256 `59e536743e1127154b8cc9ee677bb8c16bc820b8311dd2cb36e84fc7291175ee`.
- **Google Drive ZIP upload not verified** at this point; do not claim remote byte preservation of this V1.
- Research log §XI: https://docs.google.com/document/d/1ZZPfPZXyHazuLiSqOowHQfSRecseZtzSY1gn1EEOhqc/edit

Next gates: independently implement matched positive-delay reference (common arrival and service event calendars); integrate physically meaningful distance/speed; D42 real lane-based entry, exit and censored queue tails; D44 feasible braking and actual independent SUMO before policy-rank statements.
