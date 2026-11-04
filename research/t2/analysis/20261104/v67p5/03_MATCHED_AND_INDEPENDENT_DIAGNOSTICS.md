# P5 Matched diagnosis

Development: 15 seed IDs (941-943 and 960-971) x WALK0/8 x storage30/100 -> 60 matched pairs = 120 simulated runs. Baseline prior P3: 8 braking/stopline diagnostic ticks across 4 runs. Turn-only candidate: 0 across 0. Both zero queue, sampled geometry and WALK connector interval overlaps. All 120 unfinished; mean 360s exposure change candidate-prior = -2.9 vehicle seconds per paired scenario. **Not complete travel time.**

Independent challenge: 8 new seeds 1001-1008 x radius 9/12/18m x WALK 0/8s x dt 0.25/0.5s -> 96 pairs = 192 runs. Prior: 6545 braking diagnostic ticks in 22 runs and 193 sampled geometry-overlap ticks; candidate: 885 braking ticks in **46 runs**, 0 sampled geometry overlap ticks. Warning ticks decreased but affected runs INCREASED, so not uniformly improved. All 192 runs still unfinished at 210s. Synthetic/no field evidence, highly correlated cells; no independent collision interpretation.

Tests: 13 original P3 replay+contract tests passed in the unmodified directory. 32 candidate-focused tests (including corridor and standalone viability) passed. Old tests insisting on bit-identity and preserving the historic failure are intentionally incompatible with changed dynamics: never count them as passing on candidate.

Promotion: HOLD. Accept transparent negative result and a separate one-step bounded-acceleration feasibility component for integration design, NOT the candidate as safe vehicle controller.