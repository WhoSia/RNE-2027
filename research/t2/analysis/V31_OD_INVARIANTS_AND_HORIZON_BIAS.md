# T2 v3.1 precursor — OD identity, finite-horizon bias and conservation

## Executed minimal-network invariant
At each time t, for every generated vehicle ID exactly one of (outside origin queue, a finite-capacity link, completed exit set) contains the ID. The cardinality and set checks are both executed. Final generated=completed+pending; all finite links contain no more than their configured storage.

## Additional invariants before expansion
- Per-vehicle valid origin, destination and route itinerary. Terminal node may only be marked complete when vehicle reaches its own destination; next version should support multiple destination nodes and turn-specific movement queues.
- No same-second traverse of more than one junction; no vehicle transfer to a full receiving link.
- Conservation across merges/diverges, not merely node/link aggregate counts.
- Distinguish stopline crossings from OD completions. A path with more links can increase crossings without completing more trips.
- Demand and initial queues must be identical between interventions, or causal comparability is compromised.

## Boundary bias
Completed-only mean travel time is conditionally estimated given completion before T and may reward policies that strand slow vehicles. Report completion rates, vehicle-time, queue age distributions, and horizon/clearance sensitivity. A 900 s truncation cannot establish asymptotic network capacity or stable queues.

## External validity gate
Toy queue approximation is not a geometric micro-simulation. Real turning behavior, car following, acceleration, pedestrian protection, public transport, network map-matching and independent holdout must be explicitly modeled/observed before any field recommendation.

**State:** tests passed only in archived local minimal engine; remote GitHub source parity for old T2 engine is still unresolved. No GitHub Actions.
