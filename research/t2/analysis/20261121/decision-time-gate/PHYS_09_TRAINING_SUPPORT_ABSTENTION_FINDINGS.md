# PHYS-09 — Label-free training-support abstention: prospective result

2026-11-21 · R&E 2027 / T2 · **SYNTHETIC_UNCALIBRATED**

## Provenance and frozen test

The study's scope, learner, training-support rule, distance quantile,
demand regimes and never-used seed range were locked **before**
inspecting this round's outcomes in
[PHYS-09 pre-registration](PHYS_09_OOD_ABSTENTION_PREREG.md).

The five-neighbor policy was trained solely from 144 conditions in
seeds 0–7. For the *counts* and *positions* feature sets separately,
the 95th-percentile nearest-other-seed training distance became the
admissible range. An unseen observation outside the radius causes
**no phase intervention** (a form of abstention), regardless of the
learned action. Nothing in the rule knows the true demand rate,
left-turn fraction, held-out outcome or future arrival stream.

Actual squared-distance radii computed from training only:

- Counts: **0.022777777777777765**.
- Positions: **0.11499999999999999**.

The new prospective cohort used **seeds 56–71**, disjoint from earlier
0–55 studies. Two regimes × 16 seeds × 3 downstream capacities ×
3 pocket lengths × 2 B-shares = **576 same-state paired policies**.
The full pre-tick-84 state and future arrival tape were fixed within
each policy comparison, and direct baseline versus checkpoint resumed
baseline plus conservation were tested for each case.

## Results on new seeds

Savings relative to keeping the baseline signal; negative means
increased model cost. Hindsight oracle is a retrospective, unavailable
upper bound.

| Policy | Base demand 1800 vph, 50% left (288 pairs) | Low demand 1350 vph, 30% left (288 pairs) |
|---|---:|---:|
| Always existing baseline | 0 | 0 |
| Always signal intervention | 32,586 | −96,752 |
| Frozen counts predictor | **33,597** | −18,341 |
| Frozen positions predictor | 33,590 | −20,947 |
| Counts + 95th-percentile support abstention | 31,474 | **0** |
| Positions + 95th-percentile support abstention | 31,442 | **0** |
| Retrospective oracle | 34,406 | 5,720 |

The support monitor flagged **8/288** baseline-regime cases as outside
the counts training range and **7/288** for positions. This modest
number of false exclusions still reduced savings by **2,123**
and **2,148**, respectively, relative to their unconditional predictors.

In the low-turn regime **all 288/288 cases were flagged** by either
feature map, causing total abstention (zero intervention actions). The
monitor blocked 71 harmful and 23 beneficial interventions that the
frozen counts policy would otherwise choose. For the positions policy
it blocked 87 harmful and 27 beneficial interventions. These are
descriptive *retrospective* tallies, not information the selector had.

## Seed heterogeneity and uncertainty

Resampling **16 seed blocks**, each containing 18 repeated geometric
configurations, in 10,000 deterministic-bootstrap draws gave the
following 95% percentile bounds for the support-abstaining policy's
**per-case savings advantage** relative to the corresponding
unconditional predictor:

| Regime | Counts advantage | Positions advantage |
|---|---|---|
| Original demand | −7.37; **[−18.47, +0.007]** | −7.46; **[−22.38, 0]** |
| Low-turn demand | +63.68; **[+24.81, +100.60]** | +72.73; **[+20.42, +124.47]** |

The low-turn improvement was positive in **13/16 seed blocks** for both
feature maps. Three seed blocks lost possible benefit from abstention.
This block bootstrap only captures simulated seed variation, not
uncertainty about the physical law, detector errors or the real
distribution of demand.

## Verification receipt

- The exact full PHYS-09 Python analysis file executed locally and
  fetched from GitHub `main` had the same Git blob
  **`0e5811f7c73a7562389b22597379e7e45cc177f5`**.
- Full output was regenerated twice with identical JSON SHA-256
  **`2902a6090f1d08f6362525e8c51bcf9b566f05b6452bb1b77cea43e33e7974df`**.
- Tests **5/5** passed locally for train-seed-only radii, false
  outcome-label independence, distance symmetry and new seed splits.
- As before, the imported traffic engine and supporting modules were
  reconstructed from source, rather than obtained as a byte-for-byte
  exact GitHub checkout in the Python runtime. This is a **source-derived
  local result, not an exact-blobs canonical model certification**.
- The original K047 holdout remains sealed. No GitHub Actions run
  or `github-actions[bot]` attribution was involved.

## Interpretation and research decision

The result shows a *conditional opportunity* for confidence-aware
abstention: a low-turn regime outside this training support caused
large loss for the frozen policy, and a simple training-feature monitor
blocked every action while losing some model gains in the original
regime. This is **not universal OOD detection**, much less a fail-safe
signal controller: it was evaluated only on two clearly separated
synthetic traffic regimes and perfect simulator observations.
A changed driver model, a milder shift, correlated sensor dropout or
stale telemetry may be *in support* despite a wrong treatment.

**Do not promote the 95th-percentile threshold to deployment.** Next
falsification should include intermediate and opposite demand shifts,
stale/noisy observation, and fresh untouched seeds, with parameter
choices fixed before results. A physical clearance or driver-response
extension must still pass default-physics backward compatibility and
the open exact-checkout gate.
