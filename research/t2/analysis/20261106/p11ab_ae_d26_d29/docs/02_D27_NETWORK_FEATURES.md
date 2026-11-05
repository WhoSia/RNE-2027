# D27 — implemented network feature audit (10 development factors)

| Priority | Experimental function actually executed | Main missing validity |
|---:|---|---|
| 1 | longitudinal position, nonnegative velocity, acceleration-limited free movement | continuous car-following, reaction delay, guaranteed deceleration bounds, actual x/y trajectories |
| 2 | heterogeneous lengths, minimum gap and no-overlap assertions | complete packing order and realistic standstill/wave behavior |
| 3 | fixed signal green intervals and exact end-of-tick event gating | original P10 production code integration, legal turn priority, clearance and all-event causality |
| 4 | network link transfer, deterministic merge and optional lateral adjacency maneuver | MOBIL/incentive rules, full lateral trajectory, discretionary route choice |
| 5 | finite junction resource, one release per tick and time-window pedestrian occupancy | geometric polygon collision, simultaneous nonconflicting movement scheduling |
| 6 | downstream blocked receiving link, propagated external queuing with no future release reuse | CTM-consistent shockwave travel/receiving, field queue length |
| 7 | fixed pedestrian crossing occupancy schedule | pedestrian route choice, pedestrian speed, bidirectional person-person interactions |
| 8 | bus length/speed, synthetic bus stop dwell and route itinerary | actual GTFS/AVL schedule sync, crowding dwell dependence |
| 9 | seeded temporal Poisson OD and shortest-distance topology | observed OD identification, dynamically calibrated departure processes |
| 10 | directed multi-link graph, grade+curve caps, optional lane connections | OpenDRIVE map ingestion, physical 3D splines, roundabout priority, road-weather traction |

**Meaning of implemented:** executable research prototypes with unit tests and at least one integrated fixed-scenario trial. Not a claim of validated field simulation. All driving parameters are illustrations, not safe operating recommendations.
