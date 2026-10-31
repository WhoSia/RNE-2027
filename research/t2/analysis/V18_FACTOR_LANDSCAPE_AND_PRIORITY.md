# T2 factor landscape v1.8 — prioritize physical mechanisms over parameter count

2026-10-31 · research branch only · exploratory R&E study

## Newly identified mechanism groups

| Group | Controllable/observable variables | Physical question | Model validity gate |
|---|---|---|---|
| Short left pocket | actual storage, taper, pocket entrance position, lane-change access | Does queue exceed bay storage and block adjacent straight stream? | Distinguish pocket-full from pocket-empty-but-inaccessible |
| Through-lane blockage | shared-lane route order, trapped left cars, passing opportunities | Does left turn hold up S under S green? | Compare exact vehicle trajectories / phase |
| Signal operation | leading/lagging left, intergreen, yellow/all-red, protected-permissive turns | Which eligible vehicles actually receive service? | Safety/conflict constraints not represented by throughput |
| Arrival stream | exact per-cycle turn inventory, burst timing, bus arrival groups | Does ordering matter at fixed counts? | Match timestamp list AND per-cycle L/S inventory |
| Upstream coordination | offset, platoon dispersion, stochastic travel time | Does a burst arrive during useful green? | Paired traffic arrival measurements |
| Downstream receiving | per-lane receiving supply, occupancy, link length, second signal green/offset | Is upstream green rendered ineffective by spillback? | Must distinguish local stopline crossings from network exit |
| Lane geometry | channelization, dedicated right lane, diverging branches, downstream turn allocation | Do route-specific cars share the same downstream receiver? | Current single shared receiving link is oversimplified |
| Vehicle fleet | class fractions, physical length, occupancy, acceleration and reaction, saturation headway | Does heavy-vehicle mix reduce both physical storage and discharge? | Headway-only surrogate is NOT class-heterogeneous length |
| Bus/curb activity | near-side/far-side stop location, dwell, pullout bay, reentry gap | Does transit dwell create a temporary local obstruction? | Global service outage surrogate is NOT a bus-stop model |
| Pedestrian/cycle | crossing phase, turning conflict, cyclist priority | Does protected/permitted turn capacity change? | No safety conclusion from a flow-only model |
| Background use | parking, driveway ingress/egress, deliveries, lane drop | Are effective lane lengths and access reduced? | Requires location-specific geometric evidence |
| Observation | detector placement, missing periods, counting errors, queue tail visibility | Can parameters be identified from aggregate counts? | Blind/out-of-sample check; do not fit all data |
| Policy objectives | S/L completed, queue vehicle-seconds, costs, land take, pedestrian safety | Which alternatives are Pareto-feasible? | Avoid single throughput maximization |
| Initial boundary | initial queues, warmup, run duration, unserved outside traffic | Is an apparent gain finite-horizon artifact? | Compare stabilized vs transient conditions |

## Priority candidates for the next breadth-first iterations
1. Paired 120-second exact L/S order with leading vs lagging signal — **implemented v1.8**.
2. Explicit right-turn demand / divergent downstream receiving lanes — high-value missing routing mechanism.
3. Initial queues and warmup/horizon — essential diagnostic of capacity vs finite-horizon throughput.
4. Pocket full vs pocket empty but physically inaccessible — two distinct short-bay failure signatures.
5. Bus-stop position with a vehicle-specific lane obstruction, not time-only outage.
6. Heavy-vehicle length and headway as separate factors, with vehicle-length storage occupancy.

## Principles
The v1.8 source does not newly reproduce CTM's triangular fundamental diagram,
MOBIL's acceleration-and-gap test, or bus-stop conflict models.
All completed quantitative numbers remain synthetic and uncalibrated.
No GitHub Actions or main-branch work.
