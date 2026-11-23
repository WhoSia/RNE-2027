# P118 — Temporal-arrival stochastic holdout preregistration

Committed BEFORE P118 outcomes. Challenge from external Claude report: original 48 seed blocks alter L/S route labels and lane assignment but the 900vph P31 clock timestamps are exactly the same uniform and platoon4 vectors for every seed. Thus P100 64/64 is route-label stability, NOT variation in temporal arrival conditions.

## Locked intervention / population
- Routing/movement label seeds `86001,86002` (baseline high-left .75, volume 900vph, 60 labels), independently randomized **timing seeds `88001..88008`** and two timing families. Exactly 2×8×2=32 new tapes, 16 route-label groups; time vectors independently drawn per (label seed,time seed,family) using a separate deterministic seed; expected 32 distinct timing sequences.
- `stochastic_uniform`: for 60 vehicles sample 60 independent integer arrival times uniformly in 0..239 inclusive **with replacement**, then sort, attach old route labels by original ID order. This induces bunching, variable headways and potentially simultaneous arrivals; unlike P31 fixed 4s spacing, not constrained to exact interval occupancy.
- `stochastic_platoon4`: 15 vehicles in each of four 15s windows starting 20,80,140,200; sample independent integer offset 0..14 with replacement, sort within each window. Labels remain in ID order; the previously deterministic platoon structure is made internally random.
- Treatments: 4 and 8 receiver slots; original pocket 7m=1 cell, 140m approach, 2s headway, upstream 6s left-first, t84 common checkpoint within each configuration; red-onset periods 30s vs 60s (phi30=15, phi60=30).
- 32 unique temporal/label tapes ×2 capacities ×2 downstream cycles =128 runs =64 matched policy pairs. Execute each over 4800s, **all IDs must clear** and initial-arrival ID count 60 preserved. No SUMO or physical-validation claim.
- Primary falsifier: `C4 paradox count >=24/32` AND `C8 paradox count <=16/32`; if either fails, the report's 4→8 frontier requires conditioning on temporal demand and P115 should not be transported.
- Secondary: mean signed cost diff per capacity and frequency 30s cost > 60s, total receiver denial delta.
- Separately count 32 unique time vectors by SHA; failure (less than 32) invalidates diversity claim.
- `P114` calibration and `P115` results are known, so this is an **independent timing-randomization stress of the same model**, not an independent computational engine. Randomization across simulations is independent conditional on frozen routing-label sequences; no broad real-world inference.
