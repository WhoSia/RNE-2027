# T2-PHYS-04 — Identical-predecision-state branching protocol (design gate)

Date: 2026-11-21. Status: **PROTOCOL ONLY — not executed**.

## Why the next experiment must change

PHYS-01/02/03 successfully screened 704 synthetic runs, but the lane-change regime was varied from the beginning. Even when demand seeds were shared, the states at the decision instant could differ. Those studies support model sensitivity, not an isolated postdecision causal effect.

## Unit of comparison

Let `S_84` denote the **entire** saved microscopic state immediately before the decision at tick 84: vehicle IDs, lanes, cell positions, speeds/eligibility states if modeled, receiver occupancy, waiting counters, signal and clearance timers, queued arrivals and random-generator state. Saving only pocket occupancy is insufficient.

Define cost difference for an intervention pair as `Δ(S_84,D,F)=J(leading|S_84,D,F)-J(lagging|S_84,D,F)`, where `D` is the identical future external demand stream and `F` the unchanged physical geometry and lane-changing feasibility rule. Compare interventions on **clones** of the same `S_84`; do not independently generate the predecision histories.

## Pre-registered implementation gates

1. **State inventory.** Map every mutable field used by `dual_lane_v11.run`, `spatial_v10`, and `receiving_cells_v15`. In particular, identify hidden local counters and PRNG calls. No claim of full snapshot coverage before this inventory passes.
2. **Checkpoint/restart identity.** Run an uninterrupted baseline and a checkpoint-at-84/resume baseline. Compare complete event streams, end state and objective byte-for-byte under the same environment. If this fails, stop: no treatment-effect calculation.
3. **Paired intervention.** Fork two deep-copied states, change only the designated *post-84* signal plan, and keep the future arrival tape identical. Verify a trace hash and state hash at the fork point.
4. **Feasibility perturbations.** In a separate factorial experiment, toggle future lane-changing opportunity windows only after tick 84, with geometry fixed. Changes that affect movement before tick 84 are disallowed in the matched-state claim.
5. **Robustness and failure reporting.** Repeat under at least two objective horizons, compare a small set of pocket/receiving capacities, record ties and failures, and publish per-pair results rather than only counts of sign reversals.

## Explicit falsification conditions

- A checkpoint run differs from the uninterrupted reference in the no-intervention control.
- Vehicle conservation or collision/occupancy invariants fail.
- Unintended predecision or future-demand differences appear in paired traces.
- Apparent policy reversals disappear after fixing objective horizon or the model geometry.

Any of these failures blocks causal language. Counterfactuals within the same simulator are **model-conditional**, not field-confirmed causal impacts.

## Time-boxed exhibition integration

Keep a separate demonstration track aimed at a usable offline exhibit by 2026-12-18: coherent question, one transparent paired experiment with reproducible data, a judge-operable interactive comparison, and a concise account of model/field gaps. The K047 18:00–18:30 UTC holdout is not part of the development data. Do not recreate the retired `K047-review.html`.

## Source and reuse boundaries

- PHYS-01/02/03 synthesis: `PHYS_192_384_128_FINDINGS.md` in this directory.
- Hidas (2005): qualitative constraints around vehicle interactions; gap acceptance remains unimplemented.
- Huang et al. (2025): lane assignment × signal-timing framing; no claim to implement its published full optimizer.
- Shafik & Rakha (2025): queue-estimation inspiration; not used as a validated input to the present PHYS simulations.
- Long et al. (2026): separate oracle future availability from actual decision-time information.

## Proof standard for closing PHYS-04

Code + independently rerunnable tests + exact pair manifest + hash receipts + a dated Docs research decision. A protocol commit alone is not an experiment.
