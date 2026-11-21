# PHYS-04 — independent cross-check of matched-state phase intervention (2026-11-21)

**Evidence status: INDEPENDENT REIMPLEMENTATION / PRELIMINARY.** These numbers were obtained by an independently written Python implementation of the inspected `dual_lane_v11.py` cell transition rules. They are **not** results of executing the canonical GitHub engine or its regression suite. Do not merge these counts into the completed 704-run PHYS-01/02/03 results.

## Research question and design

At t=84, copy an entire microscopic state. Keep the subsequent generated arrival tape and the road geometry fixed within each pair. Compare the unmodified signal schedule (straight green at ticks 84–87) to a substitute schedule (clearance ticks 84–86, left green ticks 87–90, no active service 91–119). The two alternatives both have four green ticks in the local comparison window, but differ in the served movement and surrounding red intervals.

For each downstream receiving capacity C in {2,4,8}, use seeds 0–7, pocket lengths 14/28/70m, and preassigned B lane shares 0/0.5: 48 same-state matched policy pairs per capacity, 144 pairs total. Different capacities are different baseline physical worlds, **not** same-state counterfactuals against one another. The observation horizon is 240 ticks (different from the preceding PHYS 720-tick screen), lateral change zone 100m (different from its 70m default), demand 1800 vph, left fraction 0.5. These changes make naive numerical comparison with the 704 earlier runs invalid.

Cost = integrated outside, upstream and downstream vehicle-seconds + terminal penalty times remaining vehicles. Below, \u0394 = intervention cost - baseline cost; negative favors the intervention.

## Independently executed results

| Receiving storage | Penalty | Intervention better | Baseline better | Ties | Mean \u0394 |
|---:|---:|---:|---:|---:|---:|
| 2 cells | 0 | 16 | 32 | 0 | -41.5 |
| 2 cells | 60 | 16 | 32 | 0 | -57.7 |
| 2 cells | 120 | 16 | 32 | 0 | -74.0 |
| 4 cells | 0 | 17 | 3 | 28 | -35.0 |
| 4 cells | 60 | 17 | 3 | 28 | -50.0 |
| 4 cells | 120 | 17 | 3 | 28 | -65.0 |
| 8 cells | 0 | 19 | 0 | 29 | -78.2 |
| 8 cells | 60 | 19 | 0 | 29 | -118.2 |
| 8 cells | 120 | 19 | 0 | 29 | -158.2 |

The p=60 means above are rounded; for C=4 the unrounded mean is -49.95833. At C=4, \u0394 ranged from -358 to +1610; at C=2 from -391 to +1477, and at C=8 from -358 to 0. The results suggest a pronounced **policy \u00d7 downstream storage** interaction in this reconstructed model. They are not statistical evidence for any real intersection.

### Explicit opposite-direction witnesses at C=4, penalty 60

- seed=0, pocket=14m, B share=0: cost 14011 to 13859, \u0394=-152. Straight exits 30 to 26, left exits 15 to 20.
- seed=0, pocket=14m, B share=0.5: cost 13859 to 15469, \u0394=+1610. Remaining vehicles 74 to 84, left exits 19 to 8. This case alone reverses the simplistic 'always reassign to left green' intuition.
- seed=1, pocket=14m, B share=0: cost 14425 to 14067, \u0394=-358. Remaining vehicles 77 to 75; the terminal penalty accounts for -120 of the difference.

Within the 4-cell reconstruction, p=0 vs p=120 yielded **no strict sign reversals**, although penalty changes the effect magnitudes. Do not extrapolate to longer horizons or different demand generators.

## Reproduction receipts and scope

Local reference outputs were independently regenerated twice with byte equality.

- C=2 reference JSON SHA-256: `851f219c0ddf383061143a02b7c05697c0fe2ffa7a1cb323b71cb8fef400f612`
- C=4 reference JSON SHA-256: `90c55f22580738cb7d2da68544281824b971c9682da54de3ebc7b8fc8658ffb3`
- C=8 reference JSON SHA-256: `e46fd3fa966f762b298281688a08a79473c0d4ff4132ec482ef5b9d8313b4d5e`

These local results are **not claimed to have been uploaded to Drive or committed here**. The source and result JSON were generated as downloadable chat artifacts. The new canonical engine study entrypoint is `research/t2/physical_checkpoint_capacity_screen.py`, but has not yet been executed successfully in an environment with an authenticated repository checkout.

## Decision after comparison: expand the simulator in a targeted way

The next simulator capability is **decision-time observation extraction** from frozen state, rather than adding undirected detail. `checkpoint_observation` now provides counts and occupied positions without future arrival tape or RNG state. It deliberately does not equate the simulator's internal observability with real-world detector measurements. Follow this with quantitative observation-ablation tests and event-level trace comparisons. Retain PHYS-04 as preliminary until its canonical direct vs resumed baseline and branch experiments pass.

## Reuse and limitations

Earlier 704-run PHYS work varied both lane-change opportunity timing and phase order across independent runs; this study holds predecision state fixed within each pair, but the independent implementation is a separate codebase and still requires parity checks. The early/late PHYS-02 experiment and the present phase-reallocation experiment are different interventions. K047 holdout remains sealed. No valid inference about observed human lane-change behavior, field delays, legal signal plans, or causal policy effectiveness follows from these synthetic numerical results.
