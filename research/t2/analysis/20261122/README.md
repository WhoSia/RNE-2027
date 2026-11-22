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


## P22 — BFS/DFS archive replay, adversarial independent-unit audit, actual DLR stopline counts

- [P22 preregistration (committed before newly collected DLR windows)](P22_ADVERSARIAL_REALITY_GATE_PREREG_20261122.md)
- [Six-role adversarial findings and negative controls](P22_ADVERSARIAL_MULTIROLE_FINDINGS_20261122.md)
- [Exact-source block/stopline analysis](p22_block_and_stopline_audit.py) and [7 source-backed tests](test_p22_block_and_stopline_audit.py)
- [Post-prereg exploratory terminal-penalty sensitivity rerunner](p22_penalty_sensitivity.py)
- [Machine-readable result, independent units, raw checksums and release](P22_ADVERSARIAL_STOPLINE_AND_BLOCK_RESULTS_20261122.json)

**7/7 tests PASS** using exact-DLR original 1s movement-volume files; all 3 input byte SHA256 matched. DLR Sunday 2023-09-24 UTC 12:00 436 crossing bins/32 movement columns, 18:00 192/27, 23:30 17/12; variable columns and vastly different traffic intensity flag invalid constant-schema and night-as-congestion assumptions. P19 256 world outcomes use only 16 full arrival tapes, not 256 independent traffic days; at offset15 0/128 harm = 0/16 tape blocks. Exact conditional IID 95% one-sided upper probability 0.1707497 confirmed in Wolfram, **not valid field-world confidence without IID**. Offset0 +5108 aggregate reverses to −2248 if seed115 omitted or −2230 if seed118 omitted. Post-prereg model penalty 0/60/120 rerun holds policy sign frequencies, but does not validate physically feasible signal interventions.

Actual [shared Drive P22 8-member reproduction ZIP](https://drive.google.com/file/d/1ZbIMHN_4r7xU_xckynxcnlMLB_MG-d35/view) uploaded to 03_REPRODUCIBLE_EVIDENCE/10_RELEASE_BUNDLES, **re-downloaded and SHA256 verified** (9,771 bytes, 73badd36c839968018d9e2420195a3431379895ec4d5e5b22d0609f6506543f8). Original publisher CSV files remain exclusively in 02_DATASETS and have not been replaced. Core research priorities remain physical traffic, real sensing, decision-value; dataset intake does not override scientific gates.


## P23 — DLR official codebook table decoded; VRU warning separated from motor signals

[Official publisher-source findings](P23_OFFICIAL_DLR_CODEBOOK_AND_SIGNAL_PURPOSE_FINDINGS_20261122.md), [PDF/CSV SHA-locked reader](p23_dlr_official_signal_codebook.py), [five source-backed tests](test_p23_dlr_official_signal_codebook.py), [compact output](P23_OFFICIAL_DLR_SIGNAL_CODEBOOK_RESULTS_20261122.json).

The **original DLR-UT v1.3.1 27-page PDF**, printed page14 Table4, defines state codes: 3 red, 4 red+yellow, 5 green, 7 yellow, 9 flashing yellow, plus protected green 6/yellow 8. The actual Figure1 printed page12 maps ID1–9 motor vehicle lights, ID10–29 VRU lights, ID30 separate flashing VRU warning. In the existing night 26,970-row signal CSV, motor readings red6105/green1645, VRU red14819/green3035; ID30 warning off604/flashing yellow295. Maximum consecutive sample gap 2.004s and 30 gaps over 1.5s: do not infer subsecond phase transition times. Both original source hashes locked. **5/5 tests PASS** with actual publisher PDF and actual CSV, exact code Git blobs matched remote main.

[Exact P23 six-member reproduction ZIP on shared Drive](https://drive.google.com/file/d/1OpitphlBVFnSrcnRWpYwBvk9sQME0nL9/view), **5,139 bytes**; downloaded back and SHA256 `bee87e23aca56bf7cff53d79090291c763b68a0823f35183defd19dd628c7e73` matched local. Raw PDF and CSV still only in original dataset shelf. Signal codebook resolved; lane movement signal attribution, exact vehicle headway, legal safety and independent SUMO remain OPEN.


## P23/P24 — Real DLR observation-to-map alignment, official stopline bins, and version-exact signal definitions

### P23: Actual geospatial source evidence
- [Findings](P23_DLR_GEOMETRY_AND_STOPLINE_FINDINGS_20261122.md), [geospatial source](p23_map_volume_alignment.py), [7 tests](test_p23_map_volume_alignment.py), [machine-readable results](P23_DLR_SPATIAL_ALIGNMENT_RESULT_20261122.json).
- Three exact Drive SHA-sealed originals (DLR-UT map, trajectories, same-window traffic-volume) were independently processed. `EPSG:32632` → OpenDRIVE header's projected CRS was verified on the original UTM coordinates; all **8,624** raw sample points checked, **8,389/8,624 within 10m of nearest centerline**. An exploratory wrong +100m easting shift reduces that to **584/8,624**. This is geometric concordance, not a proven lane/signal assignment.
- Official `traffic-volume` source from [existing dataset lake](https://drive.google.com/file/d/1YHLhvITWSru8vm1RWmZudJMSgezJSaiv/view) contains **893 seconds**, **12 movement columns**, **17 positive one-second crossing bins** in this late-night period; it is not 17 independently matched vehicle IDs or sub-second headway.
- OpenDRIVE has 7 static road-signal elements with 6 unique IDs, which are not the 30 real-time signal IDs. **7/7 local tests PASS**, exact source Git blob `16c830a93b6dda4860d200f1b7c03c95dcb84105` and test blob `c4e2583b6856d98e768481d6392a0066c2062867`; full output SHA256 `36c1032db31698af3a19c3c01d63822b56a39445461e1b8e1760edf661cc9f35`.

### P24: The version-1.3.1 official signal-state and coordinate source
- [Official-codebook findings](P24_OFFICIAL_SIGNAL_CODEBOOK_AND_GEOMETRY_FINDINGS_20261122.md), [PDF codebook/coordinate parser](p24_dlr_official_signal_codebook.py), [7 tests](test_p24_dlr_official_signal_codebook.py), [structured summary](P24_DLR_OFFICIAL_CODEBOOK_SUMMARY_20261122.json).
- Exact DLR v1.3.1 documentation PDF (original Drive ID `1gUqUJEAGtXw06RjQCLbBoJ0k-pcee5Uq`, SHA256 `3c733b677ee63fd2cb282946f415f649d23954ac420d5bc37e0af545f7293849`) **Table 4** identifies observed code 1=off, 3=red, 4=red+yellow, 5=green, 7=yellow, 9=flashing yellow. Code 0/2/6/8 also documented but absent from observed CSV. The full 26,970 signal rows are tallied and 869 observed 1Hz code changes verified.
- Official PDF **Table 3** has **35 position rows for 26 distinct live signal IDs**. IDs **10,11,12,13** appear in data but have no coordinates in the table: not silently imputed. Figure 1 supplies the approach-group diagram but position≠controlled lane or stopline. **7/7 local tests PASS**, exact source Git blob `0e5edb4884b9385eb778f71222270249aaebcf47`, test blob `dfc348476412c691ae051dbe561df14e37bc2da2`; full JSON SHA256 `d48376cf8958764e567b75b97b38307be799934ab7d04446775dafd9d727c3a1`.
- New observed transition matrix includes 171 apparent red→green and 168 green→red adjacent-code changes. At 1Hz, these observations **do not prove missing clearance in a physical controller**; they can reflect sampling or different signal-head type. No live signal operations were performed.

**P25 scientific next gate:** explicit Figure 1 signal-to-approach grouping and stopline-lane directional match, then within the 20Hz tracked vehicle trajectories derive and *independently compare* predicted crossing events with the observed 1Hz official 17-bin movement signals. Report false positives/negatives and ambiguous lane assignments; avoid optimizing geometry after inspecting results.

**INTERACTION TC/DR custody:** [prepared publisher-originals folder](https://drive.google.com/drive/folders/1k-EEwOyBgUVoQaGwQsModGfmP92w0Gzv) remains empty at last check; user PC downloads do not automatically create accessible Drive files. Do not report move/ingestion until bytes are uploaded. No GitHub Actions, K047 sealed, CIM HOLD.


## P25–P29 — Further original-engine synthetic followups (2026-11-22)

**[Consolidated independently rerunnable scientific results](P25_P29_PHYSICAL_FOLLOWUP_FINDINGS_20261122.md)**, pre-commit designs [P25/P26](P25_P26_FOLLOWUP_PREREG_20261122.md) and [P29](P29_FRESH_SEED_HOLDOUT_PREREG_20261122.md), openly outcome-informed exploratory [P27](P27_STAGE_OPPORTUNITY_EXTENSION_PLAN_20261122.md), [P28](P28_EVENT_METRIC_IDENTIFIABILITY_PLAN_20261122.md). Exact `main` Python runners: [P25/26](p25_p26_physical_followups.py), [P27](p27_stage_opportunity_extension.py), [P28](p28_event_metric_identifiability.py), [P29](p29_fresh_seed_holdout.py).

- **P25** 192 synthetic worlds, receiver headways1/2/4 sec, only four unique arrival tapes. For 64 worlds per headway, treated-cost beneficial/harmful/tie **47/0/17; 18/12/34; 0/0/64**. Headway2 effects exactly reproduce 64 frozen P19 rows. Cross-headway *initial states differ*.
- **P26** 64 identical-checkpoint worlds, green durations6/8/10s. **Every world has equal scalar model cost for all 3 durations** despite 6→10s **exactly four more receiver denial attempts per world** and distinct event histories.
- **P27 exploratory** 128 worlds, headway1/2 with 6/10/16/24s treatments. Under 24s, cost improves vs 6s in 64, ties in64, worsens in0. The 24s arm was selected after outcome-informed pilot; do **not** cite as preregistered independent confirmation.
- **P28 posthoc** cross-validate source-sealed P26 vs P27 with **64/64 overlapping worlds**; raw `receiver_denied_attempts` is policy opportunity-conditioned and is **not unique blocked vehicles** or an invariant congestion measurement. Of 128 6→10s comparisons, 32 alter modeled left crossing events even when model cost does not change.
- **P29 fresh seed-label holdout** preregistered *before running* new seeds120–123, 128 new synthetic geometry worlds (four complete arrival tapes). When downstream offset15, 24s is more favorable than 6s in **64/64**; when offset0 all **64/64 tie**. Other geometrical factors and headway1/2 retained. This is **not empirical road generalization**.
- [P25/P26 compact results](P25_P26_HEADWAY_AND_DOSE_RESULTS_20261122.json), [P27 compact results](P27_LONG_STAGE_EXPLORATORY_RESULTS_20261122.json), [P28 source-sealed metric findings](P28_METRIC_INVARIANCE_RESULTS_20261122.json), [P29 holdout results](P29_FRESH_SEED_HOLDOUT_RESULT_20261122.json).
- Regression tests [P25–27, 11](test_p25_p26_p27_physical_followups.py), [P28, 8](test_p28_event_metric_identifiability.py), [P29, 7](test_p29_fresh_seed_holdout.py): **26/26 PASS** with exact-GitHub-main blob code locally, checkpoint immutability, P19 reference, full non-degenerate cohort, and negative controls. All P25/P26/P27/P29 full result reruns yielded byte-identical JSONs.
- [Full 22-member reproducibility delivery manifest](P25_P29_EXACT_DELIVERY_MANIFEST_20261122.json): raw reference P19, original-engine source, all experimental code/tests, full JSON outputs and test transcripts. **Actually uploaded** to the shared Drive `03_REPRODUCIBLE_EVIDENCE/10_RELEASE_BUNDLES`: [T2_P25_P29_20261122_FOLLOWUP_REPRODUCTION.zip](https://drive.google.com/file/d/1U8KErQrF_7YyXGUvH4CM0AawchRkJuDQ/view), 93,782 bytes, SHA-256 `9de9ab34333c4afd8ba3e54d901a503b1a9a76096fa6a4f692b8b5052ce442fd`. Raw-byte readback agrees with local original.

**Next hypothesis:** reconstruct *unique vehicle IDs* denied and per-ID wait time rather than denial-event frequency; vary complete arrival-law families (not only seed/geometry), and obtain an independently run SUMO + empirical DLR stopline baseline. Nominal model phase `-` is not certified yellow/all-red/pedestrian clearance, and 24s stage **must not** be proposed for real intersection control. K047 and large CIM HOLD, no GitHub Actions/bot; user-downloaded INTERACTION sources still require accessible Drive upload.


## P30–P31: Identity-level measurement and arrival-process falsification (2026-11-22)

- [P30 prereg](P30_UNIQUE_VEHICLE_EVENT_AUDIT_PREREG_20261122.md), [source](p30_unique_vehicle_event_audit.py), [9 tests](test_p30_unique_vehicle_event_audit.py), [machine summary](P30_UNIQUE_VEHICLE_EVENT_AUDIT_RESULTS_20261122.json), [scientific findings](P30_UNIQUE_VEHICLE_EVENT_AUDIT_FINDINGS_20261122.md): exact original engine, 64 prior P26 synthetic worlds and four original traffic tapes. Cost equal64/64, +4 denial attempts64/64, but **distinct rejected vehicle identities increase in only 34/64**, equal in30/64. Test key-type fix made after first 6/9 run, then **9/9 PASS**. Full P30 output SHA256 `6fc5d2e02192f8dd4ad97f420bbb8961bb0339d2c7ca01bc3a7ac16c3a43763f`.
- [P31 prereg](P31_TWO_ARRIVAL_FAMILIES_PREREG_20261122.md), [source](p31_two_arrival_families.py), [11 tests](test_p31_two_arrival_families.py), [machine summary](P31_TWO_ARRIVAL_FAMILIES_RESULTS_20261122.json), [scientific findings](P31_TWO_ARRIVAL_FAMILIES_FINDINGS_20261122.md): **128 synthetic worlds, eight new complete arrival tapes (seeds124–127)** over fixed-route-count uniform and four-platoon clock families. **9/128 worlds break the P26 6s=10s objective plateau**, all 10s score−6s score =−189, and **20/128** break exact+4 denial-increment pattern. **11/11 PASS**; output SHA256 `ff0452b4b37174b17bf91228722209de0f26ac60730ef9ef673b08d50c0f4915`.
- One exact-source reproducibility ZIP holds P30/P31 complete JSON (including all per-world records), runner and tests, original unchanged simulator source, test logs, SHA manifests. **20/20 total tests passed**. Both are **synthetic uncalibrated** experiments, not new human road observations, SUMO validation, or legal signal operation. Independent tape units=4 and8 respectively; repeated geometry worlds are not statistically independent arrival days.


## P32: ID-level corridor exit and main-only branch audit (2026-11-22)

- [Prereg for P32](P32_PER_VEHICLE_EXIT_RECONSTRUCTION_PREREG_20261122.md), [exact experiment runner](p32_id_corridor_exit_audit.py), [11 corruption and regression tests](test_p32_id_corridor_exit_audit.py), [machine summary](P32_ID_CORRIDOR_EXIT_AUDIT_RESULTS_20261122.json), [paper-axis, multiple skeptical reviews and findings](P32_ID_CORRIDOR_EXIT_AUDIT_AND_PAPER_AXIS_20261122.md).
- Reran exact P30 (64) and P31 (128), **192 paired synthetic worlds, 12 unique arrival tapes**, 11/11 tests pass. P30 **16** and P31 **31** worlds have equal all frozen aggregate costs/counts but different observed vehicle-ID stopline/receiver-exit events. Full P32 SHA-256 `fa0e1447377e2aa716dd12e348e3a8a2c17dc4a165913da2883b22110e3f636e`. Receiver exits are only inferred from original frames, not independent physical/field measurements. Non-exits are right-censored. Original model unchanged; historical P31 mislabeled baseline_score=remaining is corrected *only in P32*.
- [Main-only branch ancestry audit](P32_MAIN_ONLY_BRANCH_CONSOLIDATION_AUDIT_20261122.md): old `research/t2-spatial-fig2-v02` is strict ancestor of `main`, **0 branch-only commits**. No merge needed; old remote branch deletion **NOT EXECUTED** because GitHub connector has no delete-ref method. User may delete it from GitHub Branches UI.
- [Actual archived-chat prompt pattern review and decision on priorities](P32_CHAT_ARCHIVE_PI_PATTERN_AND_DELIVERABLE_PRIORITY_20261122.md): read four dated R&E chat original MD exports; exhibition/prototype track and paper/novelty track are distinct. No claim of review by external Claude or any other model; internal mechanistic, measurement, novelty and progress reviews are documented.
- [Friend-readable LR-L Harvest in Notion](https://app.notion.com/p/420ef561cf9281688691dd9ffd4a537f), continuing LR-J and LR-K.
- [Complete P32 16-file reproduction archive on Research OS Drive](https://drive.google.com/file/d/1Y2xY7q6PRGqU3gtBO3iJmsQCDQ2xH1uz/view): SHA-256 `f8cea1babfceb841da6087f5563f9877b4771ad46fc52005d508d01706558b12`, exact-source and test logs, full P30/P31/P32 JSON, checksum manifest; raw upload/download verified.


## P24 — Native OpenDRIVE/UTM geometry sanity check; do NOT invent vehicle-signal control mapping

- [P24 exact-source official map joining and failed-map correspondence report](P24_DLR_MAP_JOIN_AND_P23_CORRECTION_FINDINGS_20261122.md)
- [P24 offline source-locked map/vehicle/route auditor](p24_dlr_map_join_gate.py), [nine input-backed regression checks](test_p24_dlr_map_join_gate.py), [road-reference geometric proximity check](p24_geometry_proximity_check.py), [structured results](P24_DLR_MAP_JOIN_GATE_RESULTS_20261122.json)
- [Original-byte P24 reproduction ZIP on Drive](https://drive.google.com/file/d/1OX2RpxVZQMF7A6aTZUA1VW8Glsju5Amq/view): 13,958 bytes, re-downloaded SHA256 `cb677b5b98dcdb29d669b9fd41a9dd766259eb8c606ada9c1883193916875e9e`, and each of eight member checksums verified.

Official DLR publisher PDF's **actually downloaded SHA256** is `94fd9ebd32d04a9c35b02be526fbd11a8d5a613933d7961fde800386853b34f3`, not the original reported P23 value. Replaying original P23 bundle on this exact PDF yielded 4 PASS + 1 source-hash ERROR, corrected source now **5/5 PASS**, Git blob `f2363324a7a3c8aa2017901d9d2da1d9f4f5c1c1`. Main P23 code and JSON amended, historical evidence kept.

Actual DLR source map: 28 road elements, 1 junction; 7 static type-294 sign instances with 6 IDs, no dynamic controller and no mapping to actual light heads ID1–9. Publisher has 18 positions for 9 motor signal IDs. Real 8,624 vehicle trajectory samples transform correctly into map bbox; road-reference line nearest distance median3.572m/p95 7.416m, 97.26345% within 10m (serially correlated samples, NOT valid vehicle-lane attribution). Traffic-volume 12:00/18:00/23:30 labels have 32/27/12 columns and include same-approach route `West0West1`; no direct OpenDRIVE lane IDs inferred.

DLR's public [TASI](https://github.com/DLR-TS/TASI) at commit `5dc52b93cd375e92cd5ae4aa3a7f10e5aeafca11`: `DLRTrafficVolumeDataset` is a pass-through CSV wrapper and `TrafficVolumeDataset.from_csv` only stacks imported columns. **This does not establish any lane-to-signal generation/mapping contract.** TASI data loader is useful for reading published 1s data, not proof of actual signal control. Local P24 source tests 9/9 PASS; exact remote main Git blob was not separately executed in this session. Keep field-phase/map correspondence UNKNOWN until real authoritative lane topology/label evidence.

Physical goal: provide regional (Changwon/Gyeongnam) traffic-flow improvement models calibrated/checked against external datasets. The P24 join gate is a prerequisite, not a replacement science-fair topic. Independent SUMO and true signal/queue/stopline validation remain open.


## P33 — Go DLR field-time fidelity and synchronized observation gap

- [Prospective field-data QC protocol](P33_GO_DLR_TEMPORAL_FIDELITY_PREREG_20261122.md)
- [Go 1.23 stdlib source](dlr_temporal_gate_go/main.go), [Go module](dlr_temporal_gate_go/go.mod), [13 Go unit/integration tests](dlr_temporal_gate_go/main_test.go)
- [Independent Python raw-CSV measurement parity](p33_python_csv_parity.py)
- [Full 30-head/37-track JSON result](P33_GO_DLR_FIELD_FIDELITY_FULL_20261122.json)
- [Scientific interpretation and adversarial findings](P33_GO_DLR_OBSERVATION_GAP_FINDINGS_20261122.md)

Raw input SHA-locked to DLR-UT v1.3.1 real 15-minute window: 26,970 signal observations across 30 heads, 8,624 tracked-object observations across 37 IDs, exactly **899** synchronized signal timestamps, 869 sampled state changes. **One globally synchronized 2.004s observation gap** (23:31:44.010Z–23:31:46.014Z) affects all 30 signal heads; IDs **12,20,21** change observed code across the gap, while one tracked object contributes **40 trajectory samples inside it**. No exact transition instant, controlled-lane mapping, field causation, or signal timing legality is inferred. The Go implementation reproduces the earlier P24/P20 counts exactly and finds the common-mode missing observation. **13/13 tests PASS**, Go vet and race checks PASS, independent Python parity PASS. Go full JSON SHA256 `fc70c9cd0859a73a2d113ecbeea8a531b23151901391959d18ffabf1c1dc7687`.

No extra modules, system install, GitHub Actions or new development branch. Reproduce with Go 1.23+ and the two exact CSVs locally:

```sh
cd research/t2/analysis/20261122/dlr_temporal_gate_go
P33_SOURCE_DIR=/path/to/dir/with/exact/CSVs go test -count=1 -v ./...
go vet ./...
go run . --signals /path/to/traffic-lights_230924-233000_230924-234500.csv --trajectories /path/to/trajectories_230924-233000_230924-234500.csv --out /tmp/p33_new.json
python ../p33_python_csv_parity.py /tmp/p33_new.json /path/to/traffic-lights_230924-233000_230924-234500.csv /path/to/trajectories_230924-233000_230924-234500.csv
```

Go was selected for independent typed streaming and no-dependency output, **not** as a replacement for the source Python physical simulator. Scientific next gate: combine officially grounded signal head→movement geometry with the observation-gap interval mask; only then assess movement-specific stopline crossing observation or independent SUMO calibration.

## P24/P24b — DLR OpenDRIVE map geometry, 2015 static stoplines vs 2023 observed signal heads

**Physical evidence priority.** [P24 official PDF+XODR crosswalk audit](P24_XODR_STOPLINE_AND_SIGNAL_CROSSWALK_FINDINGS_20261122.md), [source-locked geometry code](p24_xodr_static_signal_audit.py), [nine tests](test_p24_xodr_static_signal_audit.py), [compact outcome](P24_XODR_STATIC_MAP_AUDIT_20261122.json). The real map (2015-03-25, v1.0.0) has 28 roads, one junction, seven `type=294,dynamic=no` stopline-style markers using IDs 300600-series; the 2023 observed signal CSV has IDs 1–30, **no direct controller ID crosswalk**. Original PDF lists 18 motor-head coordinates across nine IDs; mapped nearest stopline distance ranges 4.673–18.924m but does not identify a controlling signal. All 9/9 exact-remote-main source-backed tests pass. [P24 reproduction bundle](https://drive.google.com/file/d/1D0_iQ-FPHXvpjeH7Oy_5pYRkXqV85RQj/view), re-downloaded SHA256 63b0cc2fec83befb7863f51394bba9e81dc432e6f8af0857e0f9b0c2c2a12ffa.

[P24b junction roles](P24B_JUNCTION_TOPOLOGY_FINDINGS_20261122.md), [structural role code](p24b_junction_stopline_roles.py), [seven tests](test_p24b_junction_stopline_roles.py), [compact result](P24B_JUNCTION_APPROACH_STOPLINE_RESULTS_20261122.json): 4 approach-end candidate markers (roads 100000/179000/201000/280000), 1 outbound, 2 internal connectors. **Marker ID 300607 is reused on distinct roads**, so source IDs are not unique geographic objects. **7/7 exact-remote-main source-backed tests pass.** [P24b reproduction bundle](https://drive.google.com/file/d/112UeWG-AYdWaEktOW5jYCoxZIDYthvG5/view), re-downloaded SHA256 1655323445bf7cfc8e003ce3a5671ee55573fdc457314e0b347b1bfb397d02a9.

**Provenance correction:** the prior P23 reproduction ZIP refers to old PDF SHA 3c733b…, whereas the currently fetched official Drive PDF hashes **94fd9ebd…34f3**; the current `main` P23 source blob f2363324a7a3c8aa2017901d9d2da1d9f4f5c1c1 has already corrected this, and 5/5 source-backed tests were rerun successfully. The older ZIP is a historical release, not current source bytes. No invented signal→lane attribution or physical queue proof.


## P34-OBS — 20 Hz measured stopline-center crossings vs publisher's derived 1 Hz route counts

[Full paper-style findings and P24b erratum](P34_OBS_DLR_STOPLINE_RECONCILIATION_FINDINGS_20261122.md), [source-locked reader](p34_dlr_stopline_event_reconciliation.py), [23 original-source/adversarial tests](test_p34_dlr_stopline_event_reconciliation.py), [compact machine results](P34_OBS_DLR_STOPLINE_RECONCILIATION_SUMMARY_20261122.json).

Actual DLR 2023-09-24 23:30–23:45Z: 8,624 trajectory rows, 37 IDs; 893 route-counter seconds and 17 total derived counts. Source-locked 2015 XODR four inbound static marker tangent planes yield 17 non-interpolated 20Hz vehicle center crossings with **50ms evidence brackets**. One-to-one approach+timestamp ±1s matching finds **16/17**, with East 4/5, South 5/5, West 7/7. An East crossing at 23:32:16.5046Z lacks a matching official count, and one South volume at 23:36:10Z has only a **possible left-censored first frame**, not a witnessed crossing.

**Important corrected P24b claim:** every static `type294` element includes XML `laneValidity` (prior code searched the wrong tag `validity`). Corrected reader/test on main **7/7 PASS**; 2015 map static laneValidity retains only **7/17** observed crossings, excluding many 2023 source-consistent events, hence must not be treated as validated active controller lane scope. **P34-OBS 23/23 tests PASS**, exact GitHub-main source text verified against locally executed source; original raw bytes preserved on Drive.

This is **same-source consistency**, not an independent field truth: publisher traffic-volume originates from the same trajectory system. **Movement destinations, 2023 light controller→lane, live queue discharge, field causal policy benefits, and independent SUMO comparison remain OPEN.** The `P34-OBS` name avoids collision with existing **synthetic P25–P29 and subsequent P30–P33** research sequence.


**P34-OBS reproducible Drive delivery:** [Exact-source 10-member ZIP](https://drive.google.com/file/d/1DPABAywIBwQc7uZZjI37dvJ4-e7wt65F/view), 19,867 bytes, re-downloaded SHA256 `bb8701db35578951e82202845c5fa9b65d5ee55afb31c1afed22292e65a3c679` identical; includes full 17-event ledger, exact tested source and 30/30 test log. Original licensed raw datasets excluded. [P34 researcher diary](https://docs.google.com/document/d/1Zo0Z-Q50o3f7oLvOF-73vKOCQcDGLq5fynmGaStm0kA/edit) persisted and read back.
