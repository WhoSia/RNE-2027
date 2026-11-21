# PHYS-05 — decision-time observation ablation and unseen-seed stress test

**2026-11-21 · SYNTHETIC_UNCALIBRATED · source-derived local Python execution.**

## Question

Can traffic geometry and a snapshot observation at the decision boundary
select the beneficial future phase allocation, without future demand leakage?
How much decision value is added by counts and then by occupied cell positions?

## Frozen policy and evaluation

The two actions are the PHYS-04 control and the t=84 locally
clearance-safe left-green reallocation. Each pair's cost difference is
`delta = intervention_cost - control_cost` with a residual-vehicle
terminal penalty of 60 and 240-tick horizon.

Three nested feature maps are evaluated:

1. **Geometry:** downstream receiving capacity / 8, pocket length / 70
   and B-lane preassignment fraction. These are configuration assumptions,
   not inferred sensors.
2. **Counts:** geometry plus outside A/B counts, approach A/B counts, turn
   pocket count and receiving-link count at the decision boundary. These
   values are not all guaranteed observable by real field detectors.
3. **Positions:** counts plus binary occupancy of upstream A/B, pocket and
   downstream receiving cells. Future arrivals and random-generator state
   are never included.

Fixed estimator: nearest five training cases by squared scaled Euclidean
distance; choose the intervention iff mean training delta < 0. No
hyperparameter optimization was performed. This is a demonstrator, not a
production predictor. Hindsight oracle is a retrospective upper bound
that **may not be deployed**.

## Exploratory leave-one-demand-seed-out: 8 seeds, 144 pairs

Each fold holds out 18 conditions of one seed, training on 126 conditions
from the other seven seeds.

| Policy | Total savings vs always-control | Total hindsight regret |
|---|---:|---:|
| Always control | 0 | 15194 |
| Always intervene | 10844 | 4350 |
| Geometry only | 8861 | 6333 |
| Geometry + counts | 13761 | 1433 |
| Geometry + counts + positions | 13751 | 1443 |
| Hindsight best per case | 15194 | 0 |

Positions did not improve this **small exploratory cohort** relative to
counts under the chosen fixed distance scaling.

Sensitivity of total savings to k on the same eight-seed fold study:

| k | Geometry | Counts | Positions |
|---:|---:|---:|---:|
| 1 | -1221 | 11642 | 11591 |
| 3 | 8861 | 13765 | 13764 |
| 5 | 8861 | 13761 | 13751 |
| 9 | 9258 | 13001 | 12996 |

This is a robustness diagnostic; none of these values is an independent
external test and **k=5 was not reselected** for the additional seeds.

## External-to-training seed stress test: seeds 8–31, 432 new policy pairs

Trained all five-neighbor policies only on seeds 0–7; tested 24 new PRNG
seeds across the same 18 physical configurations per seed. These are
unused synthetic seeds from the SAME generator, not real-world or
distribution-shift validation.

| Policy | Total savings on new seeds | Regret vs hindsight |
|---|---:|---:|
| Always intervene | 41454 | 9026 |
| Geometry only | 42468 | 8012 |
| Geometry + counts | 48449 | 2031 |
| Geometry + counts + positions | 49586 | 894 |
| Hindsight best | 50480 | 0 |

Under this fixed policy, positions outperform counts by 1137 cost units
across 432 cases, equivalent to 2.63 units per case. The relative improvement
was **not** present in the exploratory 144 pairs. Thus the observation
hierarchy's ranking depends on seed sample and learning rule.

Twenty thousand seed-block bootstrap draws (24 whole-seed groups, seed fixed)
gave the following *exploratory* 95% percentile intervals for per-pair savings:
counts versus always-intervene [-4.52, +46.35]; positions versus
always-intervene [-1.88, +48.71]; positions versus counts [+0.56, +5.19].
Bootstrap resampling only captures variation among this generator's seeds;
it does not cover model misspecification, real traffic correlations, or
observation noise. Intervals are not adjusted for multiple inspection and
cannot support field-performance claims.

Capacity-specific regrets in this unseen-seed cohort:

| Receiver | Always intervene | Counts | Positions |
|---:|---:|---:|---:|
| 2 cells | 2638 | 1170 | 358 |
| 4 cells | 4804 | 861 | 536 |
| 8 cells | 1584 | 0 | 0 |

## Source and reproducibility status

Local source-derived validation produced 144 checkpoint/restart identity
controls and 1,872/1,872 equal independent-reference fields. The 432 new
pairs each also passed an uninterrupted vs checkpoint-restarted control check.
A second local rerun produced byte-identical JSON for holdout and subsequent
gap sensitivity. **This is not a clean checkout of exact GitHub file blobs.**

- 144 local copied-engine PHYS-04 JSON SHA-256:
  `0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001`
- 144 out-of-fold observation JSON SHA-256:
  `a381cdbbb4a136e36b5d59f148dbf54c37e88ba69b50a1e12871ae2233ca11fe`
- 432 holdout JSON SHA-256:
  `843bda4a78980dcae0dda168e67cf1bd318dd5c3dc2c856e676a55a52c921572`

## Research decision

Advance **explicit observation corruption/missingness** as the next
decision-layer falsification, with a new seed/demand regime test. Do not
interpret position benefit as proof that high-resolution field sensing is
required; the simulated position vectors are privileged and may be
unavailable from real detectors. K047 real holdout remains sealed.

Do not conflate traffic model accuracy with policy-selection validity:
a better position predictor may still make wrong decisions under the
wrong objective, measurement delays or unmodeled vehicle responses.
