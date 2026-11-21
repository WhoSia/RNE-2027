# PHYS-10 — In-support harmful actions and over-abstention under correlated sensor loss

2026-11-21 · **SYNTHETIC_UNCALIBRATED** · exact-blob core replay

## Registered design and execution

The four moderate single-variable demand shifts, unseen seeds 72–79,
12-second historical observation, contiguous 10-cell A-lane occlusion,
95th-percentile training-support radii and fixed k=5 predictor were
prespecified in
[PHYS-10 pre-registration](PHYS_10_NEAR_SUPPORT_SHIFT_AND_TELEMETRY_PREREG.md).
No parameters were adjusted after inspecting outcomes.

For each regime: 8 seeds × 3 receiver capacities (2/4/8) × 3 pocket
lengths (14/28/70 m) × 2 B-lane preassignments = 144 matched
t84 policy branches. Four regimes comprise **576 distinct matched
policy pairs**. In each pair, the two futures share a checkpoint,
traffic tape and physical configuration. Across regimes, predecision
states and tapes differ. Outcome: integrated vehicle-seconds plus
60×remaining at 240s, hence not field delay performance.

## Clean decision-time observations: OOD test fails to certify policy sign

The support radii are fixed from seeds0–7: counts squared distance
0.022777777777777765 and positions 0.11499999999999999.

| Test regime | Out of support, counts | Harmful treatment actions *inside* support, counts | Counts 5-NN savings | Counts+OOD savings | Hindsight oracle |
|---|---:|---:|---:|---:|---:|
| 1800 vph, left 45% | 10/144 | **14** | 8019 | 4739 | 9035 |
| 1800 vph, left 55% | 9/144 | **7** | 33396 | 30174 | 34509 |
| 1650 vph, left 50% | 20/144 | **7** | 21826 | 17778 | 22161 |
| 1950 vph, left 50% | 15/144 | **11** | 18021 | 12967 | 18423 |

For the position-based classifier the clean-observation harmful
in-support action counts were 17, 7, 10, 14 respectively. Harmful
means that intervention increased *synthetic* objective against the
same-state baseline, not that road users were physically harmed.

The OOD veto mostly rejected *beneficial* candidate interventions
under these moderate shifts: counts-policy blocked beneficial actions
9, 9, 14, 14 and blocked harmful candidates 0, 0, 2, 0.
No unconditional safety claim is warranted.

### Concrete feature-aliasing witness (not merely out-of-support)

- **Evaluation:** seed 76, 1800 vph and 45% left, receiver 4 cells,
  pocket 14m, B share 0. At t84, counts-only nearest-training distance
  is **exactly 0**. The 5-NN predicts intervention delta **−30.2**,
  selects intervention and passes the training-support gate. The
  actual matched-state delta is **+306** (baseline 13,584,
  intervention 13,890).
- **Training cohort:** seed 3, 1800 vph and 50% left with the same
  receiver capacity, bay and B share has precisely the same six
  aggregate t84 counts but a different arrangement of A/B vehicles.
  Its cost delta is **0**. Equal aggregated counts do not imply
  equal action value or equal future demand distribution.
- The position-feature model sees the difference (nonzero squared
  nearest distance 0.04) and predicts **+31**, so it chooses baseline
  in this one witness. This does not prove positions always fix the
  problem.

Seed76's cost decomposition for intervention minus baseline:

| Field | Difference |
|---|---:|
| Outside vehicle-seconds | −90 |
| Upstream vehicle-seconds | +290 |
| Receiver vehicle-seconds | −14 |
| End remaining vehicles | +2 vehicles × 60 = +120 |
| **Total** | **+306** |

At stopline between ticks 84–119, baseline served two straight
crossings (t84, t86) while intervention served two left turns
(t87, t89). The changed later queue dynamics caused two fewer
network exits for straight vehicles, no additional left network
exits and two extra remaining vehicles at the endpoint.
The compared training condition is a different *world*; only the
within-evaluation-policy branches are identical-state causal contrasts.

## Stale telemetry and correlated occlusion

All four regimes were also evaluated at t72 observation (12s stale)
and under a spatially contiguous missing A-lane detector section
covering cells -20 through -11. For each occluded snapshot the
reported A count is reduced by the number of omitted occupied
cells, maintaining consistency between count and occupancy list.
The true traffic tape, microstate and outcome remain unchanged.

**All 576 occluded states were declared outside support** by both
the counts and positions support monitors; the veto prevented all
interventions in every regime. This is not a calibrated detector
failure distribution, and a fail-closed baseline is not a
field-certified safe action. It nevertheless shows severe
*false abstention*: among proposed counts-model interventions,
the number of beneficial candidates blocked was 20, 97, 67, 52
for left45, left55, demand1650 and demand1950 respectively.

| Regime | t72 counts: in support | t72 counts harmful admitted | t72 counts+OOD savings | Clean counts+OOD savings |
|---|---:|---:|---:|---:|
| Left 45% | 131/144 | 5 | 5479 | 4739 |
| Left 55% | 134/144 | 1 | 19625 | 30174 |
| Demand 1650 | 139/144 | 3 | 10376 | 17778 |
| Demand 1950 | 128/144 | 3 | 11593 | 12967 |

The metric can occasionally be better under stale data because
the learned decision boundary is imperfect. Do not interpret this
as a physical benefit from delaying telemetry.

The 8-seed-block bootstrap was computed for each regime/scenario/
feature policy pair; the complete 24 sets of intervals are stored
in the original result JSON. Their resampling unit was seed, not
the 18 correlated geometry combinations within a seed.

## Verification and limits

- PHYS-10 local script Git blob `459e11987b0fc423f26f96e1aff0adf42c0f7cd6`
  exactly matches GitHub `main`; the test blob is
  `1d06d7e2fd6aaabc35818ec7df8b76e619f86a15`.
- Simulator core, receiver, arrival, objective and observation learner
  are the five cryptographically matched GitHub blobs documented in
  [exact-core replay receipt](PHYS_04_09_EXACT_BLOB_CORE_REPLAY_RECEIPT.md).
- Full 576-pair result JSON generated *twice* with byte-identical
  SHA-256
  `ebd182b7c18d684cde6072557298943dc1480cdc15d6e8508ce032411f22cb8b`.
- PHYS-07/08/09/10 local contract tests **25/25 passed**.
- A full clean `git clone` of every repository file and historical
  test suite remains unverified; Python 3.13.5 local runtime.
- K047 remained sealed, GitHub Actions not invoked.
- Model-internal position and arrival assumptions are uncalibrated
  and cannot justify actual signal-controller safety.

## Verdict

**REJECT** the claim that being inside a 95th-percentile feature-support
ball certifies nonharmful signal intervention. Even exact count-feature
matches can exhibit different action value because observed aggregate
state is not sufficient to determine future traffic or internal
vehicle arrangement. Also reject using a correlated detector blackout
as *proof of changed traffic distribution*: hardware malfunction
and demand shift require distinct observability channels.

Next research:
1. Explicitly separate **detector health/missingness** from
   **traffic distribution support** in the decision observation.
2. Improve uncertainty estimates for conditional action value,
   not only nearest-feature distance.
3. Re-run with a different physical driver response/target-gap
   assumption after a backward-compatible physics extension, then
   determine whether the failure mechanism persists.
