# T2 v3.2 — Typed evidence and temporal custody contract inspired by RITHM

## Evidence root and admissible claim
Witness hierarchy: original executed source bytes + SHA and input stream > event trace > independently replayed invariants > aggregate CSV > research narrative. Archive existence does not establish current GitHub source parity. Source acquisition timestamp, model event time, experiment time, Drive receipt, and narrative publication time are DIFFERENT metadata fields; never silently substitute.

## Event schema draft
Each vehicle has immutable id, origin, destination, arrival_time, scenario_id. Transitions contain {tick,vehicle_id,from_location,to_location,event_type,controller_policy,phase,receipt_source_sha}; event_type enum {GENERATED,ADMITTED,CROSSING,DENIED_STORAGE,WAIT_SIGNAL,EXITED}. Negative events need eligibility predicate; zero DENIED_STORAGE means no logged eligible storage refusal under that run's event semantics, not no real congestion.

## Scientific hold/failed claim discipline
- PASS model conservation does not establish field validity.
- A policy winning in 450s and losing in 1800s is not a mechanism explanation without matched cohort and complete traces.
- Current pressure heuristic is NOT formal max-pressure; no theorem contradiction.
- Zero recorded action failures does not establish a road has no hidden queues.
- A calibration set cannot double as a field holdout.

## Independent replay gates
1. Same origin+destination demand stream and IDs across policies.
2. Every vehicle moves at most once per tick and respects link occupancy.
3. All generated vehicles accounted for at each tick, not only end-of-run.
4. Every service denial tied to eligible movement and actual receiving-link full state.
5. Completed trips must show an unbroken legal path in events.
6. Contract distinguishes event timestamp from repository record timestamp.

Scope limit: RITHM evidence control is a research methodology transfer, not evidence that RITHM's human route choice results apply to T2.
