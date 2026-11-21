# T2 P12 — Abstract action feasibility gate: pre-implementation contract (2026-11-21)

## Core motivation
Existing T2 PHYS-04–11 used a short isolated virtual left-green intervention, with no complete yellow indications, pedestrian clearance or conflicting cross-street movements. Earlier results cannot be promoted as operationally legal signal plans. Our next task is **not** a live controller implementation; it is to prevent unrealistic abstract policy proposals from silently entering a scientific comparison.

## Research questions
- Q1: Does a formal, configurable, and *illustrative-only* stage-timing contract reject the existing 4-tick virtual intervention when its stipulated minimum green exceeds four ticks?
- Q2: Does it detect omitted stage changes, incomplete clearance, and incompatible pedestrian clearance without treating a time label '-' as yellow?
- Q3: Can we separate 'contract-valid for a chosen artificial parameter tuple' from 'approved by a traffic authority'? The former never implies the latter.

## Freezing the scope before implementation
Use a self-contained Python module taking a sequence of (movement, green, yellow, all_red) stages and invented phase timing constraints. Reject booleans, negatives, noninteger values, duplicates and incompatible stage sets. Compute a *conservative illustrative* sequential stage duration. It is not the engine's native execution schedule and cannot silently modify it. No code path for live devices.

Acceptance examples:
1. With invented minimum left-green 6 ticks, a four-tick left stage fails.
2. With invented minimum left-green 4 ticks, the same stage passes this single check, but can fail clearance checks independently.
3. Missing yellow/red when the spec demands nonzero intervals fails.
4. Pedestrian clearance longer than chosen compatible green+yellow interval fails.
5. A clean, independent local Python unittest run passes the full contract tests.
6. The test parameters are deliberately invented and are not Korean regulatory minima.

## Scientific boundary
The cited FHWA Traffic Signal Timing Manual Ch5 describes minimum green, yellow and red clearance as separate concepts; the applicable Korean jurisdiction and actual intersection controller have NOT been established. Hence P12 only supplies formal model hygiene. No K047 holdout, no live signal changes, no safety certification.

## Links / continuity
- Previous critical audit: CRITICAL_INDEPENDENT_REVIEW_AND_CORRECTIONS.md
- Previous arrival clock study: T2_ARRIVAL_CLOCK_AND_GREEN_ENVELOPE_FINDINGS.md
- FHWA manual: https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter5.htm
- SUMO random departures: https://sumo.dlr.de/docs/Simulation/Randomness.html
