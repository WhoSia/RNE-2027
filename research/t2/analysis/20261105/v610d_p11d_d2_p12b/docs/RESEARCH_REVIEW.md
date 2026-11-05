# T2 2026-11-05 v6.10-D/P11-D/D2/P12-B — evidence and limits

## Main engineering decision

Design for potentially global road-network coverage through **separate source-format adapters and an explicit, loss-aware lane graph**. It is not feasible or scientifically defensible to claim every road geometry, signal logic, and traffic mode has already been captured. Missing lane turns, conflicts, signal state programs or other safety-relevant road rules are **unresolved facts**, not inferred green permissions.

## Track F — topology and features

* Added `src/road_ir.py`: exact directed lane connections, lane lengths/speeds, signal `linkIndex` references, route reachability.
* Readers: CityFlow roadnet JSON, SUMO `.net.xml` subset, OSMnx/NetworkX `MultiDiGraph` *segment skeleton* (does not synthesize legal turning connections).
* Upstream references: [SUMO netconvert](https://sumo.dlr.de/docs/netconvert.html), [SUMO OSM caveats](https://sumo.dlr.de/docs/Networks/Import/OpenStreetMap.html), [CityFlow roadnet](https://github.com/cityflow-project/CityFlow/blob/master/docs/source/roadnet.rst), [OSMnx](https://networkx.org/documentation/stable/auto_examples/geospatial/plot_osmnx.html), [MATSim](https://www.matsim.org/).
* Current importer omissions: turn restrictions, internal junction geometry, roundabouts and junction conflict auto-derivation, pedestrian cycles, protected/permissive nuance, reversible lanes, bus lanes, elevation/3D intersections, lane closure, time-of-day restrictions, speed changes, multimodal transit and rail. SUMO's turn `dir` and `linkIndex` are retained as fields but full TLS state is NOT reconstructed from them.

## Track V — causal and validation contracts

* Legacy v6.9-P2 is left unchanged and independently replayed: **28/28 regression tests**.
* Existing v6.10-C test suite + 14 newly added tests (10 road IR, 2 OSMnx, 2 sparse controller, 10 basic controller, 4 SPaT intervals) = **62/62 code tests**. The new code tests check stated contracts and synthetic fixtures, not real traffic collision or field prediction.
* A controller that only checks maximum green at the next sensor event can exceed the maximum interval under irregular sampling. Corrected to progress mandatory fixed/max green, yellow and all-red transitions at their **scheduled** timestamps. It remains a discrete synthetic policy prototype and cannot control physical hardware.

## Track D2 — independent observed public data

* USDOT Utah SPaT API `https://data.transportation.gov/resource/j7k2-8r24.json?$where=intersection_id%3D%275502%27&$order=tmstp_utc%20ASC&$limit=1000` HTTP 200. Parsed 1,000 observations, UTC March 1 2025 00:00:00.052–00:01:39.986; 18 observed group2/group4 changes; transition intervals 0.004–0.942 s. These are **brackets**, not exact observed phase-change times. Source time window covers ~100s only and cannot support daily cycle distributions or vehicle delay estimates. Derived summary in GitHub `research/t2/analysis/20261105/data/utah_spat_5502_1000_transition_intervals_derived.json`.
* Previous 500-row processed subset is in Drive `40_DERIVED`; official source bytes are **not** sealed. BSM matching was not achieved; intersection-location mapping to individual vehicles is an open gate. Jinju raw CSV remains unacquired.
* New strict `src/spat_intervals.py` treats absent groups as unknown and preserves adjacent timestamp interval censoring.

## Track P12-B — policy controls

* `src/controllers.py`: simulation-only fixed-duration, queue-demand (gap proxy) and queue-pressure controller policies with observed signal-group sample inputs and explicit `PhaseGuard` enforcing min/max green, yellow, all-red, non-backdating.
* A synthetic 121-observation / 120-second trace was replayed separately through the three controllers; fixed 10 yellow transitions, actuated 11, pressure 11. **This is not vehicle throughput, travel-time improvement, or proof that one policy is superior.** The controllers are **not yet coupled** to the v6.10-C multi-hop vehicle state kernel.
* Next fair policy comparison must drive each controller from independent simulated detector signals, with *the same* input arrival/vehicle kinematics, simulation cost and holdout. A closed-loop vehicle simulation and real SPaT verification are still needed.

## Immediate next gates

1. Define `TurnRestriction`, `LanePermission`, exact junction geometry and importer uncertainty contracts. Build OSMnx real-world graph acquisition with source-byte receipts; never turn inferred crossing into an allowed movement without validation.
2. Integrate guarded controllers into multi-hop event simulation, with causal detector observations, all-red transition and conflict-free phase switching; then compute travel-time/queue effects.
3. Obtain complete small SUMO network and run real SUMO with exact source config/versions. Equal input and output contract; measure discrepancy, not blindly equate simulators.
4. Extend SPaT 5502 on train/held-out dates, verify timestamps and signalgroup->turn mapping, combine location/UTC-matched BSM observations only if grounded.
5. Standardize policy comparisons on same feasible phase schedules and compute budget; establish real fixed/actuated/max-pressure/MPC baselines. No real-world controller deployment.

All source ZIP and prior-day dated folders immutable. No bot commits (`github-actions[bot]` prohibited). GitHub code + Drive dated journal + Drive derived experiments.
