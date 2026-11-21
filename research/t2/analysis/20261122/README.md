# T2 Research — 2026-11-22

**Ownership:** development, tests, research log and `main` integration by 김우준 (ChatGPT-assisted). Independent adversarial peer review by 김세호/Claude. Peer review findings do not automatically authorize or replace code changes.

## P15 — coarse RF labels vs T2 policy-relevant state

- [Prior formal interface contract](P15_RF_TO_T2_STATE_INTERFACE_PREREG_20261122.md)
- [Independent critique receipt](P15_COLLABORATOR_CLAUDE_AUDIT_RECEIPT_20261122.md)
- [Exact synthetic decision-sufficiency auditor](p15_rf_decision_sufficiency.py)
- [19 local tests](test_p15_rf_decision_sufficiency.py)
- [Deterministic machine-readable result](p15_rf_decision_sufficiency_results.json)
- [Results and exact SHA/blobs](P15_1_EXACT_DECISION_SUFFICIENCY_FINDINGS_20261122.md)
- [Independent reviewer mandate](P15_INDEPENDENT_PEER_REVIEW_MANDATE_20261122.md)
- [Daily Google Doc](https://docs.google.com/document/d/1Zo0Z-Q50o3f7oLvOF-73vKOCQcDGLq5fynmGaStm0kA/edit)

To reproduce locally without any repository automation:

```sh
cd research/t2/analysis/20261122
python -m unittest -v test_p15_rf_decision_sufficiency.py
python p15_rf_decision_sufficiency.py > /tmp/p15_result.json
```

The locally executed final source and tests match the GitHub `main` Git blob IDs in [findings](P15_1_EXACT_DECISION_SUFFICIENCY_FINDINGS_20261122.md); 19/19 pass. Three toy cohorts demonstrate (i) an **invented** strict opposite-policy pair under identical staged label, (ii) a common optimal action despite non-injective label, and (iii) an exact tie/common action. The artificial cost matrix was chosen by the developer to exercise the logic: **no new PHYS model, radio signal, policy deployment or empirical traffic observation**.

Review priorities: maliciously chosen cohort boundaries; unverified independent arrival groups; action contracts represented by strings instead of validated P12 feasibility; physically staged occupancy labels not guaranteed to map to real T2 state; within-class RF emission drift; complete compatibility-set sampling. Do not promote artificial fixtures to field results.

Working branch `main`; no GitHub Actions, K047 seal preserved, ~5GB CIM dataset remains untouched.


## P16 — Genuine PHYS checkpoint schema, NOT a five-class RF diagnosis

- [Source-derived checkpoint-to-proxy adapter](t2_p16_checkpoint_contract.py)
- [20 targeted schema/alias regression tests](test_t2_p16_checkpoint_contract.py)
- [What was read from the canonical core and what remains UNIDENTIFIABLE](P16_CHECKPOINT_INTERFACE_FINDINGS_20261122.md)

```sh
cd research/t2/analysis/20261122
python -m unittest -v test_t2_p16_checkpoint_contract.py
```

**20/20 local tests passed** with exact-byte GitHub blob-matched code/test source after final line-break reconciliation. The adapter uses the exact fields of `dual_lane_v11.checkpoint_observation` and the PHYS-04 row schema, but no complete PHYS-04 empirical/synthetic result JSON was run or audited during this unit. `rf_five_class_label=None` is intentional: neither a static obstruction nor a causal queue diagnosis is identifiable from a single time-slice count alone. A fake opposite-delta test is only a regression test, not a discovered PHYS witness.


## P17 — Authentic historical PHYS-04 archive, re-downloaded and audited

- [P17 archived 144-policy-pair findings](P17_HISTORICAL_PHYS04_EXACT_ARCHIVE_FINDINGS_20261122.md)
- [ZIP-SHA-pinned read-only auditor](p17_zip_audit.py)
- [9 focused tests including exact historic ZIP](test_p17_zip_audit.py)
- [Compact structured result](P17_PHYS04_VERIFIED_ARCHIVE_SUMMARY_20261122.json)
- Original [Nov21 PHYS04/05/05b/06 Drive ZIP](https://drive.google.com/file/d/1nIHmzoz0Yk3YUqaaxvbBWH7ztgR2ddo-/view) — now actually downloaded and SHA-256 verified; this **does not** repair its internal reconstructed-engine provenance.

**New P17 decision:** 144 stored pair rows, 133 strict matching groups, 11 count-collision groups, just one weak opposite-sign witness (−305 versus +1), **zero robust opposite-sign witness at epsilon=5**, and zero opposite signs after matching full occupied-cell positions. Deliberately dropping B-share from the key produces 2 **invalid** large opposite-sign artifacts; both compare different lane allocations at the same seed.

Run with a local copy of the *specific* existing 52,090-byte Drive ZIP:

```sh
python p17_zip_audit.py /path/to/T2_PHYS04_05_05b_06_20261121_Research_Bundle.zip p17_full_audit.json
P17_HISTORICAL_ZIP=/path/to/T2_PHYS04_05_05b_06_20261121_Research_Bundle.zip python -m unittest -v test_p17_zip_audit.py
```

**9/9 local tests passed**, the actual historical results were opened in this run, source/test Git blobs match committed `main`, and full audit output has a recorded SHA. This is a genuine analysis of earlier model-output bytes, *not* a fresh execution of the T2 physical engine or field observation. The 5GB held CIM dataset was untouched.


## P18 — Exact canonical PHYS-04 parity + 256 prospective timing worlds

- [P18 pre-outcome registered clock, position and action contract](P18_PROSPECTIVE_CLOCK_POSITION_ACTION_PREREG_20261122.md)
- [Exact canonical-code and prospective results analysis](P18_CANONICAL_REPLAY_AND_PROSPECTIVE_FINDINGS_20261122.md)
- [Executed main-compatible experiment runner](p18_clock_position_action.py)
- [15 targeted tests](test_p18_clock_position_action.py)
- [Compact machine-readable summary](P18_EXACT_MAIN_SUMMARY_20261122.json)
- [Posthoc downstream-service event witness](p18_exploratory_service_witness.py), [its five tests](test_p18_exploratory_service_witness.py)
- [Exact five-source GitHub transfer manifest](https://docs.google.com/document/d/1NCnqkEJpeUL03d7MAuy2F_DlprxGGOxlpAurA6gwjB0/edit), already in Nov22 dated Drive folder.

The precise five GitHub `main` Python blob hashes matched the local runner. Fresh canonical execution regenerated **all 144 PHYS-04 paired result rows identical** to the historical P17 ZIP's original numeric rows (top-level JSON wrappers differ). The prospectively frozen P18 **256 synthetic worlds**, **32 unique arrival tapes**, **128 same-geometry clock pairs** and **768 baseline/treatment future trajectories** yielded no strict opposite-sign alias at epsilon=5 under six-count or position-complete observation. Strong real-world claims are not established. Under an *invented* minimum 6s left green, 4s is excluded; 8s meets only that single synthetic parameter and does not certify actual clearance or pedestrian constraints.

Exact executable run from the `research/t2` directory, with the P18 runner and tests discoverable on `PYTHONPATH`:

```sh
PYTHONPATH=research/t2:research/t2/analysis/20261122 python -m unittest -v test_p18_clock_position_action test_p18_exploratory_service_witness
PYTHONPATH=research/t2:research/t2/analysis/20261122 python research/t2/analysis/20261122/p18_clock_position_action.py p18_result.json
```

The 15 preregistered runner regressions and five posthoc event regressions passed locally (20/20 combined). Two complete new-cohort JSON generations were byte-identical. A 17-entry standalone local ZIP reproducer and its SHA256 `be3e10629398958500fba71151bff09e7f8312232eae4f07fee85faa3f0cd620` are available as a conversation download, **not yet shared-drive uploaded**. K047 sealed, CIM ZIP held, no GitHub Actions.


## P19 — Prospective receiver storage × downstream signal offset mechanism screen

- [Pre-execution frozen P19 protocol](P19_RECEIVER_SERVICE_OPPORTUNITY_PREREG_20261122.md)
- [Executed exact-core 256-world receiver/offset runner](p19_receiver_service_opportunity.py)
- [9 exact-byte tests](test_p19_receiver_service_opportunity.py)
- [Full findings, event-count caveats and causal-boundary verdict](P19_RECEIVER_SERVICE_OPPORTUNITY_FINDINGS_20261122.md)
- [Compact 4-stratum machine-readable summary](P19_RECEIVER_SERVICE_SUMMARY_20261122.json)

P19 holds every world’s baseline and synthetic 8s left intervention to the same frozen checkpoint and arrival tape. Cross-world comparisons vary downstream capacity 2/4 and offset 0/15 and are **NOT same-state interventions on the receiver**. 256 worlds reuse **16** unique route-matched arrival tapes. All **9/9** tests passed and two full-result runs matched SHA256 `0681f683acd549cb2d32cc8957038ce3e652819f47e8288c5a751b6acd7e2468`.

Receiver cell capacity2/offset0: 17 favorable /47 harmful /0 ties; cap2/offset15: 16/0/48; cap4/offset0: 16/14/34; cap4/offset15: 19/0/45. **Zero** strict opposite sign pairs across matched offset changes at epsilon5. Early extra turning crossings and later receiver-entry denial events are logged separately; **do not equate their correlation with mediation causality**. All units artificial/synthetic, no real signals or RF sensing.

To reproduce, place the exact five verified engine sources plus P18 runner on the Python path and run:

```sh
PYTHONPATH=research/t2:research/t2/analysis/20261122 python -m unittest -v test_p19_receiver_service_opportunity
PYTHONPATH=research/t2:research/t2/analysis/20261122 python research/t2/analysis/20261122/p19_receiver_service_opportunity.py p19_result.json
```

The local 12-entry reproducer `P19_20261122_RECEIVER_MECHANISM_BUNDLE.zip` has SHA256 `bd23ae325f84880dd8f6eacc25bad385c559e6e749af46a7e43651bdf6a65b42` (39,580 bytes). This is a chat attachment, not a claim of shared Drive upload. K047 and the held 5GB CIM ZIP were untouched; GitHub Actions unused.


## P20 — Exact-core event ledger, empirical DLR time gate and dataset custody (2026-11-22)

**Internal event consistency:** [P20 findings](P20_EVENT_LEDGER_AND_EXTERNAL_MODEL_GATE_20261122.md), [independent cellular shadow auditor](p20_independent_receiver_ledger.py), [9 adversarial tests](test_p20_independent_receiver_ledger.py), [full 256-world P19 trace runner](p20_full_256_audit.py), and [machine-readable seal/limitations](P20_EVENT_LEDGER_RESULTS_20261122.json). A second implementation audits receiver discharge, cell shifts, stopline admission, position continuity and cumulative conservation. The exact `main` source/test files were read back and executed locally: 9/9 PASS. Full 256 synthetic worlds × 2 branches = 512 trajectories, 122,880 time ticks, zero internal disagreements, P19 costs/tape hashes 256/256 matched. Two generated full result JSON files were byte-identical (SHA256 b8d88c6ed7a771e7b489ae761070d78d88d9970957a7458d7304a33f37a6318b). **This is NOT SUMO validation or physical calibration.**

**Real independent published data:** [DLR 15-minute findings](P20_DLR_OBSERVED_TIME_ALIGNMENT_FINDINGS_20261122.md), [SHA-locked original CSV parser](p20_dlr_observed_window_gate.py), [5 tests](test_p20_dlr_observed_window_gate.py), [structured results](P20_DLR_UT_REAL_OBSERVATION_15MIN_SUMMARY_20261122.json). The existing Drive DLR-UT v1.3.1 `2023-09-24 23:30–23:45 UTC` aligned CSV file pair had 8,624 trajectory rows from 37 tracked object IDs and 26,970 signal-code rows from 30 signal IDs; sample interval medians 0.05s and 1.0s. Five exact-remote-blob local tests passed. No map/signal-head mapping or empirical stopline discharge has been validated, so no direct vehicle-headway calibration is claimed.

**Data acquisitions and large ZIP:** [P20 dataset inventory, priorities, and honest CIM custody status](P20_DATASET_INVENTORY_AND_CIM_CUSTODY_20261122.md). Existing DLR, CityArtery and SUMO scenarios should be exploited before further mass downloads. Utah SPaT and BSM currently have empty dataset-lake folders; official open datasets can be staged after license and matched-time selection. ~5GB `CIM dataset.zip` was **NOT FOUND in accessible Drive** and has NOT been moved, inspected or downloaded; a new empty receiving folder has been verified at [02_DATASETS/90_QUARANTINE_AND_UNVERIFIED/CIM_dataset_zip — UNVERIFIED_HOLD](https://drive.google.com/drive/folders/1BWRCLDTyvRkQZRIUloZo63EHDGIlgjet).

Reproduce (download original DLR files from source links above; use the correct SHA-locked file names):
```sh
python -m unittest -v test_p20_independent_receiver_ledger.py
python p20_full_256_audit.py /tmp/p20_full_256_results.json
P20_DLR_TRAJECTORIES=/path/to/trajectories_230924-233000_230924-234500.csv P20_DLR_SIGNALS=/path/to/traffic-lights_230924-233000_230924-234500.csv python -m unittest -v test_p20_dlr_observed_window_gate.py
```

Next: use an explicitly mapped real signal ID/stopline and independently execute SUMO with matched geometry and selected arrival tape. Preserve discrepancies and avoid controller-safety claims. GitHub Actions/bot banned, K047 sealed.


## P21 — DLR measured signal-code runs and pending INTERACTION TC/DR originals

- [P21 DLR source-derived findings and INTERACTION custody](P21_DLR_OBSERVATION_AND_INTERACTION_INTAKE_FINDINGS_20261122.md)
- [Verified source-sealed DLR run/low-speed code](p21_dlr_segment_gate.py) and [8 tests](test_p21_dlr_segment_gate.py)
- [Machine-readable P21 manifest](P21_DLR_SIGNAL_RUNS_AND_INTERACTION_CUSTODY_20261122.json)

**8/8 local tests, exact `main` blob-match**. DLR real 2023-09-24 15-minute sample: 37 tracked IDs, 30 signal IDs, 869 code changes, 899 code runs, 4 object IDs with low-speed pairs. Numeric signal codes are **NOT yet mapped to colors or stoplines**. The user reported both INTERACTION archives downloaded to PC; neither was found in accessible Drive/attachments. [Prepared original archive folder](https://drive.google.com/drive/folders/1k-EEwOyBgUVoQaGwQsModGfmP92w0Gzv) is empty until explicit upload. No false move or archive inspection claim.
