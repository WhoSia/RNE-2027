# R&E 2027 / T2 P11-Y D23 — Time-dependent access and phased conflict occupancy

2026-11-05. **P12 signal optimization remains FROZEN.** This work contains only a fixed-timetable path query and a synthetic sequential occupancy reference; no signal policy is evaluated or recommended.

## 1. Why this belongs in T2

A physically short route need not minimize arrival time. Generalized link/path cost is not a static distance: accessibility at stop, signal phase, or conflict zone depends on a shared time coordinate and capacity constraints. But a public transit itinerary router is NOT an intersection control optimizer. These are analogies to guide model *representation* and independent validation, not justification to unfreeze P12.

## 2. Source-backed distinctions

- Uber H3 is a hierarchical hexagonal geospatial **index**, not an earliest-arrival route solver. Appropriate later for demand/hotspot aggregation and coarse spatial join; no actual H3 cells computed here. Official https://h3geo.org/docs/
- Timetable earliest arrival and Pareto arrival/transfers are covered by RAPTOR (Delling et al.) https://www.microsoft.com/en-us/research/publication/round-based-public-transit-routing/ . CSA scans chronological connections https://transnetlab.github.io/transit-routing/html/Algorithms/CSA/index.html . OTP does transfer-point optimization as distinct postprocessing https://docs.opentripplanner.org/en/latest/RouteRequest/ . These are PREVIOUS WORK and NOT innovations of the current prototype.
- Official GTFS Schedule reference https://gtfs.org/documentation/schedule/reference/ documents stops.txt, trips.txt, stop_times.txt, calendar, frequencies.txt (exact_times distinction), transfers.txt and pathways.txt. None of the GTFS files or real-time feeds were downloaded or parsed for this stage.
- South Korean precedent: KCI article '환승 저항을 고려한 운행시간표 기반 대중교통 다중 경로 탐색 알고리즘' https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002363455

## 3. Actual synthetic timetable results

Topology O→N→D traverses 3 km; O→F→D traverses 8 km. Near link N→D low frequency departures 28,58,… min; far connector F→D departures 8,14,20,… min. At request time 0, near path arrives 32 min and far path 14 min (18 min sooner despite +5 km). With minimum transfer slack 2 rather than 1 minute, arrival via F becomes 20 min, illustrating exact connection fragility. 61 departure times (0…60) × 3 transfer margins (1,2,4) yielded 183 query results. Of 61 queries at each margin, F wins 57 times and N wins 4 under this DESIGNER-CHOSEN timetable. This is NOT statistical evidence that real transit is superior at distant interchange points. Real-time delays, walking, accessibility, fares and trip service days are omitted.

Algorithm: earliest-arrival label-setting search with state (stop, last trip, transfer count), nonnegative wait and arrival times; brute exhaustive enumeration validated 150 randomized small timetable DAGs. Static shortest-distance Dijkstra is computed separately and intentionally ignores schedules. This is a small research reference, not an optimized RAPTOR/CSA implementation or an H3 router. Clock is integer minutes.

## 4. Sequential physical zone model

The old P11-X locks ALL zones for each entire trip, while actual ordered zone occupation requires a time-expanded resource view. New independent model locks only current zone and uses an atomic handoff once the next zone is free; it holds the old zone while blocked, thereby representing a very basic form of queue blocking. Example: pedestrian occupies zone B [0,3); vehicle in A [0,3) although nominal phase duration is 2, enters B at 3 and exits at 5; following vehicle attempts A at 1, enters at 3 and exits at 4. The *additional A occupancy* is 1 tick. If opposing actors enter A and B and request each other's zone, an unresolvable hold-and-wait cycle is detected as DeadlockError. This is a model diagnostic, NOT permission to ignore deadlocks or proof that traffic gridlock always has that form.

Severe omissions: no actual vehicle position, link length, driving kinematics, within-lane queues, safe gaps, merging priority, stop lines, signal legality, road users' behavior or spillback metrics; time discretization is integer abstract ticks. Multiple simultaneous requests are deterministically ordered by arrival and ID (a scheduling convention rather than a real traffic priority rule).

## 5. Research track separation

- **Development**: phased event semantics, check conservation and transitions; next integrate finite storage and verify original P10 vehicle-event replay, without touching frozen policy code.
- **External reproduction**: secure original GTFS feed with hash/license and test true service dates; inD/NGSIM for positions and SUMO as independent physical-movement baseline. Separate the unit of observation, time zone and physical meaning of each data source.
- **Exhibition**: finite turn-lane storage, queue spillback and crossing occupancy as measurable phenomena. Transit analogy belongs in motivation/diagram or as *future demand-model interface*, not an unsourced claim of field benefit.
- **Journal**: formalize time-dependent event semantics, FIFO arrival property, multi-resource handoff and deadlock counterexamples; compare with strong published routing and discrete-event literature before claiming novelty.
- **Policy P12**: IDEAS ONLY, FROZEN.

## 6. Nonclaims / gates

No H3 package called, no transit API or official timetable used, no real routing ETA, no SUMO or existing P10 original engine executed, no study of policy ranking and no real road-safety claims. Transfer frequencies in simulation are chosen, not optimized. Store both test results and failure cases; keep independent model distinct from integrated T2 engine.
