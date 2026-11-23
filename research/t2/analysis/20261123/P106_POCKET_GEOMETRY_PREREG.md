# P106 pre-registered falsifier — 7 m is ONE pocket cell, not seven

Date 2026-11-23. This plan is committed **before** reading P106 pocket-length outcomes.

## P0 correction to prior prose
Actual source: `spatial_v10.Config.pocket_length_m` (meters), `cell_m=7.0`; `validate` computes `k=floor(pocket_length_m/cell_m+1e-9)`. The P87/P100/P101 `build_config(seed,900,share,7,4,.5)` therefore means **7 meters, 1 pocket cell**, downstream `receiver_slots=4` means 4 receiver cells (28m if equivalent cell unit is assumed), and approach `approach_length_m=140` means 20 approach cells. Previous phrases “7-cell pocket” in P100/P101/P103 are incorrect. Source-derived signed costs remain untouched, but interpretations and geometry-parity requirements must be amended. Do NOT turn an uncalibrated 7m cell into an officially surveyed lane geometry.

## Predeclared experiment P106
- NEW seed blocks `87001..87008` inclusive, two arrival families `uniform`, `platoon4`. Share 0.75 only; red onset only, same original fixed six-second left-first upstream phase.
- Treatments: pocket physical lengths **7/14/28/56 meters = 1/2/4/8 cellular slots**, fixed 7m cell. Receiver fixed 4 cells, through_B_share 0.5, no closures, upstream approach 140m, demand 900 veh/h, exact t=84 checkpoint.
- Each `seed × family × pocket length` gets 30s and 60s downstream cycles (same 50% green, red at decision), same tape and physical configuration within its pair; 8×2×4=64 pairs, 128 arms. Alter pocket only before checkpoint, not after it.
- Primary descriptive falsifier: **compare per-length counts of denied<0 and cost>0**, report all counts (denominator 16 each). Existing 1-cell pocket in prior heldout cohort had 64/64. Precommit target for “robust to this geometry variation”: minimum **14/16** paradox cases at EACH of 2,4,8-cell lengths. This target is an arbitrary strict robustness gate, not a population probability.
- Secondary: by length, red-onset `delta.cost` sum and mean, count 30s cost>60s; and 95th percentile of per-tape positive cost deltas after source replay if available.
- Validate every 128-arm run: `remaining==0`, generated==tape length, post84 receiver conflict not violated; record actual `pocket_slots` returned by engine and direct `validate(cfg.base)` equal 1/2/4/8.
- Regenerate both clocks from their same predecision checkpoint per geometry. DO NOT claim P101 directly refuted if this new finite synthetic geometry differs; report conditional fragility.
- If any of 2/4/8 lengths falls under 14/16, **demote universality of P101 mechanism** and promote transport geometry to #1. If all pass, continue to independent SUMO/field, not another same-engine seed sweep.
- Stop and mark `PENDING_EXECUTION` if full engine or source identity cannot be loaded; do not report made-up outputs.

## Required follow-up
A P0 correction note to dated diary/README/P103; preserve immutable original prereg text but add superseding erratum. LIRA retain the corrected physical geometry claim at >=0.8 only after runtime check, and downgrade real-geometry extrapolation until official lane survey.
