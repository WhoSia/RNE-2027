# PHYS-11 — Consecutive eligible-gap confirmation: prospective sensitivity

2026-11-21 · T2 · **SYNTHETIC_UNCALIBRATED**

## Protocol, model and backward compatibility

The configurable `lane_change_gap_confirmation_s` takes positive
integer 1–10. At each one-second tick, a straight vehicle stopped behind
an A-lane obstruction may move laterally to B only after the complete
existing lateral-change predicate (zone, same-tick nonmovement,
front obstruction, and empty B target cells) has held for the required
number of *consecutive eligible ticks*.

- Confirmation **1** exactly preserves the previous lane-change
  transition rule. History is empty under this default.
- Confirmation **2/3** makes the model remember a counter for each
  vehicle while the identical predicate holds on consecutive ticks.
  Streaks reset on ineligibility, movement, gap blockage and closed
  opportunity windows. The dict is part of the full checkpoint state,
  copied immutably for future policy branches.
- A new counter `lane_change_gap_confirmation_wait_s` counts
  eligible candidate-ticks withheld pending confirmation. It **does
  not** count individual drivers or measured reaction delays.
- Changes to confirmation threshold after a checkpoint are rejected.
  Invalid or Boolean/fractional thresholds are rejected explicitly.

The earlier PHYS-04 144 cases were recomputed under default=1
using the revised exact-Git-blob engine. They retained **all 144
checkpoint identities, all 1,872 independently compared fields and
the identical output JSON SHA-256**
`0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001`.
The original seed0 / bay14m / Bshare0 / 4-cell baseline remained
score 14,011, 34 lane changes, 30 straight downstream exits and
15 left exits. The new physics-specific regression tests passed 5/5.

## Pre-registered prospective experiment (seeds 80–87)

Under [the locked PHYS-11 protocol](PHYS_11_GAP_CONFIRMATION_PREREG.md),
8 new seeds × 3 bay lengths (14/28/70m) × 2 B-share
allocations (0/.5) = 48 baseline-and-intervention matched pairs for
each confirmation threshold. Receiver capacity 4 cells, gap
clearance 1 cell, lateral opportunity zone 100m, fixed demand
1800 vehicles/hour and left share 0.5, 240-second horizon and
terminal penalty 60. Across confirmation thresholds the
pre-tick-84 physical states generally differ; **the confirmation
threshold is not a same-state causal intervention**. Within each
world, both future signal plans share exactly one full state.

| Confirmation ticks | Baseline A→B changes (48 runs) | Candidate-tick confirmation waiting | Intervention lower cost | Baseline lower cost | Ties | Mean (intervention minus baseline) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 704 | 0 | 15 | 0 | 33 | −93.125 |
| 2 | 593 | 1,705 | 14 | 0 | 34 | −85.667 |
| 3 | 578 | 2,795 | 21 | 0 | 27 | −104.979 |

**Negative result:** across the 48 shared *configuration labels*,
there were **zero strict reversals** between an intervention-favored
and baseline-favored policy sign. The mean intervention effect
changed, and 10/48 configurations had at least one nonidentical
numerical delta, but their signs never crossed through positive.

A clear example of a non-strict change is seed80, bay14m,
B-share0: delta [0,0,−358] at confirmations [1,2,3].
Seed86, bay14m, B-share0: [−358,0,−178]. The movement
condition changes effects nonlinearly, but these examples do not
constitute strict sign reversals.

The recorded changes decrease 704→593→578 as eligibility must
persist longer. Individual vehicles and queues may reorganize,
so neither per-case cost nor all detailed trajectories are guaranteed
to be monotonic. All three group means in this cohort favor the
signal intervention, but this synthetic cohort cannot establish
general policy superiority or road safety.

## Verification receipt

- Engine exact GitHub `main` blob equals local Python source:
  `6c18490c42f63e65dc830ad60839c19008b8d647`.
- Study runner exact GitHub blob and local:
  `2ef0bd3996e06c47152ee410b086bb67b3de2659`.
- Physics regression test blob:
  `b0facd25654a5396500ad32dd4db29e64cc15f91`;
  prospective result regression:
  `e9df217a0e0ac2fa7fff59a29dc3ccc33e87c486`.
- 5/5 targeted model tests and 4/4 prospective summary tests ran
  locally, in addition to previously passing 25 PHYS-07/08/09/10
  tests. The 8 earlier local source-contract checks also passed.
- Full 144-pair output generated twice with byte equality and
  SHA-256 `d27a58af091952458032ddcd4f25cc36e3ab4cb1d0dbcf4c159f0d0ee958c84c`.
- Five core GitHub blob identities established in
  [exact-core receipt](PHYS_04_09_EXACT_BLOB_CORE_REPLAY_RECEIPT.md).
  The modified engine is again byte-checked. A *whole-repository
  authenticated git clone* and every historical integration test
  remain outside the verified closure.
- No GitHub Actions, K047 holdout, real detector calibration,
  observed driver gap acceptance or legally certified signal plan.

## Decision

Keep this feature as an optional sensitivity assumption. It is
valuable because an implicit one-tick gap requirement is now an
explicit, auditable model parameter, while its default preserves
the earlier evidence. **Reject** claims of measured human reaction
time or newly demonstrated strict phase-rank reversals.

Next physical extension should be justified by a concrete known
model failure (e.g. vehicle-speed heterogeneity or stochastic
gap acceptance). Before another physical parameter is introduced,
falsify the current policy using error-aware observation, future
arrival-regime uncertainty and a larger sample of independent
synthetic seeds. Mere model complexity is not evidence of realism.
