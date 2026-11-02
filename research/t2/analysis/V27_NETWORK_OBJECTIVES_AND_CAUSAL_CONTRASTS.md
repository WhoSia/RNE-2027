# T2 — Network objectives and causal contrasts

## Research question
Under what network topology, storage, turning restrictions, lane configuration, and demand distributions does a locally preferred junction policy cause inferior network-level trip completion or travel time?

## Measurement contract
Use fixed exogenous origin-destination arrivals and vehicle IDs across scenarios. Collect intersection stopline crossings, network exits, completed OD trips, vehicle distance traveled, realized mean and percentile travel time, completed-trip fraction, total queuing time, spillback time, receiver denial attempts and distinct denial seconds, vehicle/pedestrian delay. Do not confuse throughput (crossings per time), capacity and finite-horizon completed trips.

## Factor grid
Road configuration {one lane, two lanes}, control {permitted-left signal TW, left-prohibited signal TWL, roundabout RB}, topology {isolated, 3-junction arterial, 3×3 grid}, network link storage {short, long}, arrival variation {uniform, platooned}, OD turning mix {low, high}, control {fixed, coordinated}. Control physical geometry and route lengths separately. Some combinations require distinct route assignment semantics (TWL reroutes left-turn trips).

## Scientific inference
Compare matched arrival events and same analysis horizon; use warmup and clearance sensitivity; report paired effect sizes and uncertainty; pre-register primary end point (completed OD trips per demand) and secondary criteria. Avoid claiming safety or fuel changes without independently justified models. Validate with SUMO and independent field holdout before operational recommendations.
