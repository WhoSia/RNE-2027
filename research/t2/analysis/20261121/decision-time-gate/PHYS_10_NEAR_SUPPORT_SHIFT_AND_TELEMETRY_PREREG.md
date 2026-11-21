# PHYS-10 — Near-support shift × stale/missing telemetry: prespecified falsification

**2026-11-21 · protocol frozen BEFORE running seeds 72–79**

## Motivation

PHYS-09's train-support abstention correctly withheld all interventions in
one very different low-turn synthetic regime but was never shown to detect
*milder* domain shift. More subtle shifts may resemble training observations,
produce harmful interventions and defeat the OOD gate. Simulated detector
feed age and contiguous missed-cells might also distort the support test.

## Registered design

- **Training:** the original 144 PHYS-04 t84 pairs, 8 seeds 0–7, uniform
  demand 1800 vehicles/hour, left share 0.50. Fit neither the 5-NN rule nor
  the OOD radius on any future data.
- **Evaluation seeds:** 72–79 (8 never-used seeds), excluding every
  previous study's seeds 0–71.
- **4 isolated moderate shifts**, changing only one distribution
  parameter per regime: `(1800,.45)`, `(1800,.55)`,
  `(1650,.50)`, `(1950,.50)`, all uniform arrivals.
  The parenthesized values are (vehicles/hour, left-turn fraction).
  These are four new physical worlds, NOT paired same-state variations.
- For each regime, 8 seeds × 3 receiving capacities (2/4/8 cells) ×
  3 pocket lengths (14/28/70m) × 2 B-lane preassignments (0/.5) =
  **144 same-state policy pairs**, **576 total**. On each pair branch
  the same t84 checkpoint and tape into baseline and the existing
  clearance-safe future left-green plan. Objective: sum of vehicle
  seconds + 60 × end remaining.
- **Fixed predictors:** unweighted 5-NN delta estimate (counts and
  occupancy positions separately), choose treat iff estimated delta<0.
  OOD support distance uses only the original training outcomes' **input
  features**, with the original 95th percentile leave-other-seed
  squared-distance radius. The radius must be recomputed from seeds
  0–7 using previously specified nearest rank, not adjusted on test
  results. If out of support, treat is vetoed.
- **Three observation scenarios per held-out policy pair**:
  A. exact t84 observation;
  B. stale t72 observation (12-second delay, with real earlier snapshot,
     not synthetic imputation);
  C. contiguous-occlusion observation: at t84, emulate the same
     detector section failing on each case. All approach-A cells
     with positions from -20 through -11 are omitted from the observed
     occupancy list, and `approach_A` count is reduced by the number of
     omitted occupancy cells. Preserve true traffic state, causal
     outcome, other fields and training features. This is not
     calibrated, but spatially correlated and internally count-consistent.
- **Policy families** per scenario and feature level: always baseline;
  always treat; 5-NN; 5-NN plus OOD veto.
- **Required reports:** policy treatment coverage, cases out of support,
  harmful actions among those allowed (delta>0), blocked beneficial
  treatment candidates, blocked harmful treatment candidates, total
  saving and regret vs nondeliverable hindsight oracle. Disaggregate by
  regime and capacity; do not promote average gains alone.
- **Uncertainty:** resample 8 whole seed blocks per regime (18 geometry
  settings correlated within block) with fixed 10,000 seed bootstrap
  replicates, and report paired per-pair gain of OOD-veto over the 5-NN.
- **Verification:** 576 exact direct vs restarted baselines, common
  arrival tape, vehicle conservation, leakage isolation, exact core
  module hashes, no target-label dependency in policy. Two byte-identical
  output generations and SHA-256 comparison.
- **Decision gate:** reject unconditional model trust if ANY harmful
  treatments remain in the admitted in-support cohort; report all
  false-safe cases and false exclusions. The absence of observed
  failures is not proof of road safety.

K047 holdout remains sealed. The experiment uses model-internal,
not real-detector, information and a non-certified synthetic signal
intervention. No deployment or legal clearance claim is permitted.
