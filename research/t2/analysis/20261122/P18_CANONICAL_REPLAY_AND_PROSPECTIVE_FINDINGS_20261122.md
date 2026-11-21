# T2-P18 — Canonical-PHYS exact replay and prospective timestamp × position × abstract-phase study

2026-11-22 KST · R&E 2027 · Canonical GitHub `main`. Status **SYNTHETIC_UNCALIBRATED**.

## Executive decision

**ACCEPT** that the precise five current T2 simulation source files reproduce the *entire record content* of the 144 historical PHYS-04 synthetic policy comparisons. **ACCEPT** the narrower prospective negative result that, in the 256 fixed-grid cases and two fixed abstract interventions, no sufficiently large opposite policy-sign pair (`epsilon=5`) was found at equal six-count observations or in route-matched timestamp-pair worlds. **REJECT** treating either statement as real signal safety/legality, physical RF detection, universal policy sign identifiability, or 256 independent traffic days.

## 1. Exact current source acquisition and 144-case historical replay

The five canonical Python files were retrieved from GitHub via connected service with explicit `ref=main`, serialized into [the byte-preserving temporary transfer manifest](https://docs.google.com/document/d/1NCnqkEJpeUL03d7MAuy2F_DlprxGGOxlpAurA6gwjB0/edit), then restored locally by reversing UTF-8 percent encoding. Each local file passed direct `git hash-object` equality:

| File | Exact Git blob |
|---|---|
| `dual_lane_v11.py` | `a7c9aa6954402e12894d1d5b722e8a474b0bd58f` |
| `spatial_v10.py` | `ffbf3fc3f8b9a64a819d4f73ce70b264b877e84e` |
| `receiving_cells_v15.py` | `b078cf215c74b76ace6dffcbcbacab6ae22c3673` |
| `physical_transfer_screen.py` | `8d75745053ff720db6c8af0001aaaf13ba1f295e` |
| `physical_checkpoint_capacity_screen.py` | `220aeafb492fa41c8a9908f215e393f15fdfb22b` |

Ran `python physical_checkpoint_capacity_screen.py p18_phys04_exact_main.json` under Python 3.13.5. It regenerated **144/144** historical `pairs` without *any Python-level differences* from the SHA-verified prior `canonical_local_capacity144.json` loaded from [the original Drive archive](https://drive.google.com/file/d/1nIHmzoz0Yk3YUqaaxvbBWH7ztgR2ddo-/view). Note: the new JSON's whole-file SHA256 `71d452fe755965985585a6e13ef6cf282be3dc7e28889c0ee30ba512e68fcb52` differs from the old JSON hash `0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001`, because the old archival wrapper uses different top-level summary labels/provenance fields. This is **record-wise numerical and schema-level parity**, not full-file byte equality.

This substantially upgrades P17's internal model provenance: the historical results were checked against the **five exact GitHub source blobs**. It is not a full repository checkout, full historical integration suite, or independent empirical calibration.

## 2. Prospective 256-world protocol

[Pre-outcome preregistration](P18_PROSPECTIVE_CLOCK_POSITION_ACTION_PREREG_20261122.md). New seeds 104–111 inclusive; regimes 1800 vph/left .45 and 1650 vph/left .50; pockets 14/28m; receiver capacities 2/4 cells; B allocations 0/.5; two clocks. 2 × 8 × 2 × 2 × 2 × 2 = **256 worlds**. Each world was evaluated at a frozen tick84 checkpoint using the unchanged baseline and two different abstract left-service modifications; **768 simulated future trajectories**.

The random-time tape preserves (i) EXACT total vehicle requests, (ii) EXACT **ordered route labels** from the canonical deterministic request tape, and (iii) nondecreasing new request timestamps. The sole exogenous change within a paired clock pair is request timing; it changes the tick84 state, so clock comparisons are **NOT same-state causal contrasts**. Within any one world, baseline and treatment futures share the same complete pickle-verified checkpoint and future arrival tape. Sources/tests available on `main`: [experiment](p18_clock_position_action.py), [15 regressions](test_p18_clock_position_action.py).

Unique full request-tape SHA256 values: **32**, not 256. Exactly 16 regime × seed blocks, each contributing one deterministic and one randomized timestamp tape, reused across eight geometry/assignment conditions. There are **128 matched cross-clock geometry comparisons**, but the effective source variation is 16 regime/seed blocks; do not treat all 128 comparisons as statistically independent temporal draws.

## 3. Intervention effects, vehicle-seconds + 60×terminal vehicles

Define `delta = treatment - baseline`; a negative delta indicates an improvement *inside this synthetic objective*.

| Action (synthetic only) | Δ<0 worlds | Δ>0 worlds | Δ=0 worlds | Mean Δ (256 geometry worlds) |
|---|---:|---:|---:|---:|
| 4s left stage | 81 | 110 | 65 | −29.3671875 |
| 8s left stage | 81 | 114 | 61 | −20.3046875 |

A mean across the eight repeated geometry conditions is descriptive **only**. These are not 256 independent road trials; the numerical mean is not a traffic safety effect.

### Illustrative phase-feasibility gate

The actual simulator ran both phase overrides successfully and validated its **own** three-second no-service transition `'-'`. It does **not** distinguish amber, red clearance, pedestrian intervals, or real permitted stage rings. Under the preregistered **invented minimum left green of 6 seconds**, the 4s proposal is marked **INELIGIBLE** and cannot be promoted to the declared model-feasible candidate set. The 8s proposal is **ELIGIBLE ON THE SINGLE MINIMUM-GREEN CRITERION**, not certified for a real intersection. These markers are deliberately explicit and are not equivalent to executing P12's full contract checker.

For the *min-green-eligible* 8s option alone, 81 / 114 / 61 worlds favor treatment / baseline / neither. There is no universal 8s advantage.

## 4. Observation equivalence and location details

Full matching fixed regime, pocket length, receiver capacity, B-lane assignment and the **same six decision-time counts**:

- **233 groups**, 22 collision groups containing 45 worlds, **zero strict opposing-sign groups** for both actions at epsilon=5.
- Adding all four sets of occupied cell positions: **251 groups**, 4 collision groups containing 9 worlds, **zero strict opposing-sign groups**.
- Across **128** exactly route-matched clock pairs per action: **zero strict sign reversals**, **one pair with identical six counts**, **zero with identical occupied-cell positions**, **zero with identical fully pickled checkpoints**.

This confirms that the prospective cohort is mostly non-overlapping at the observation level. A zero witness count is therefore **not** evidence that the six-count observation is sufficient in the full physical state space. No conditional sign impossibility theorem is justified.

## 5. Exploratory, after-results: extra left green changes later service

On the same 256 records, the 8s intervention's cost versus the 4s intervention was equal in **246**, worse in **10**, and better in **0**. This comparison is explicitly **post hoc** and is not a traffic generalization. In the after-results [event-level trace](p18_exploratory_service_witness.py) for seed105/demand1650/pocket14/receiver4/B share.5/legacy clock, all three futures start from the *same frozen checkpoint*:

| Model path | Cost | Terminal remaining | S total exits | L total exits |
|---|---:|---:|---:|---:|
| Baseline | 11,998 | 64 | 27 | 19 |
| 4s synthetic service | 11,998 | 64 | 25 | 21 |
| 8s synthetic service | 12,304 | 66 | 29 | 15 |

The 4s service had left stopline crossings at ticks87,89. The 8s service had crossings at ticks87,89,91,93 but later `receiver_entry_cell_busy` denials at ticks120,121. Longer near-term green changes downstream use and subsequent opportunities; **no isolated mediation estimate** was made. Five dedicated exploratory event tests passed with exact source bytes. Full event JSON SHA256 `18e6c322c78fb8540ad07222e7d8fcff451a497a2b3766642971ea572b9237d9`.

## 6. Reproducibility ledger

- P18 experiment source Git blob `2e50899e07d9a353716258b47eaf8196c307390d`, locally executed SHA256 `45ef50cfbc3269320b140c421d92de51974b1f7dcb3049d9d95920efb2c4e5a5`.
- P18 tests Git blob `f591cc00073617ebe7dbf359ad5029c1fa33f0df`, locally executed SHA256 `dc5e340d2f028719db3a0f5a283efc5821da9f46af5ecdedf8738183f0031c2e`.
- Both files were re-fetched from `main` and their Git blob hashes match the actual executed local bytes. All **15/15** preregistered runner tests passed.
- Whole P18 result JSON SHA256 `a210bc7a1af4a1550e1f8a461ea585c1ed88a41c4c3245f68199b8a52ec9b8a7`. **Two independent Python invocations** produced byte-identical full JSON output.
- Exploratory trace source blob `0c4e0fbc9e26bed2b8610d9152b19142a608e556`; five tests blob `7075c0d50860484a35aa795edb24f03bec723cde`; **5/5** local PASS.
- [Compact summary JSON](P18_EXACT_MAIN_SUMMARY_20261122.json) is in GitHub `main`. A separately created local `P18_20261122_CANONICAL_EXPERIMENT_BUNDLE.zip` contains **all five exact engine sources**, runner, tests, full 256-world JSON, 144-world replay JSON, summary, test logs and SHA manifest, verified to be internally consistent. Local ZIP SHA256 `114ebb96e51d19feb34a58b6b1fcddcb59f6048c43817fece968107f7773e0a8` (47,515 bytes, 14 members). This ZIP is a conversation artifact; not falsely claimed as present in Google Drive.

No GitHub Actions/bot, no use of sealed K047, and no access to the ~5GB CIM dataset.

## 7. Next research direction (P19)

The honest high-value question is no longer 'can we get a significant effect by adding seeds?', but **why arrival-time sensitivity and stage choice interact through finite receiver occupancy**, and what is truly decision-time observable. Next: test policy comparisons under a physical driver/receiver sensitivity change and a stronger *explicit* phase contract. For the RF track, do not assert that `pocket/downstream/both` labels equal a PHYS cause without independently labeled, school-authorized measurements. A robust NO_WITNESS is a good outcome; do not search post-hoc until a desired sign appears.
