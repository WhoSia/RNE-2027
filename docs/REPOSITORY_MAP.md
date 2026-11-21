# R&E 2027 repository and Drive map

The canonical T2 code, runnable experiments and verification tests are on
[main](https://github.com/WhoSia/RNE-2027/tree/main).
Use only main for current collaboration, and pin the tested commit SHA when
recording an experiment. Other historical refs exist for preservation only.

| Looking for | Location |
| --- | --- |
| Project entry point and latest evidence | [START HERE](https://docs.google.com/document/d/1TdenHgyCjQOGHf75tJyR49Jrt2dteutkygHGEeAZSF4/edit) |
| Current claims and methodology | [T2 verification ledger](https://docs.google.com/document/d/10nj0pmvCF4BnJ_9o0wxdHzxLBQ0ZYziRW6KfXP7xwrk/edit) |
| Protected-stage model, policy search, and observation experiments | [Efficiency experiments](../research/t2/efficiency_loop/README.md) |
| Corridor offsets and finite downstream storage | [Offset information protocol](../research/t2/policy/OFFSET_INFORMATION_PROTOCOL.md) |
| Import and validation of observed data | [Jinju receipt](../research/t2/data/20261117_jinju/README.md), [CityArtery receipt](../research/t2/data/20261117_cityartery/README.md), [DLR input contract](../research/t2/efficiency_loop/DATA_ACCESS.md) |
| Original data and derived datasets | [Dataset shelves](https://drive.google.com/drive/folders/1s_n1K4_YzfZqxuBXRITN2l0CjJ4a-IyW), [derived outputs](https://drive.google.com/drive/folders/1pR7cpMnQm0iB7Xzj5u5JYd6XTVQFhmYX) |
| Daily reasoning, decisions, and teammate replies | [Research log](https://drive.google.com/drive/folders/15HIj9OU7e63K2kuVnxGJY00nxGsmNODZ) |
| Published manifests, bundles, and visualizations | [Reproducible evidence](https://drive.google.com/drive/folders/182v-EmB9Z6ylmUrbeOBiPchCg-NyEsmz) |
| Paper originals and project-specific reviews | [Research OS papers](https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP), [T2 reading and field notes](https://drive.google.com/drive/folders/1PszjYiffe8bRxtM6PnYbQHvhC_6gWfky) |
| Superseded records and recovery objects | [Archive](https://drive.google.com/drive/folders/1jpRsGlui6ZISoYnUTA1DEAmBuGZ7xhIH), [branch recovery bundle](https://drive.google.com/file/d/1vF8oDwafQtfhP4Lx29kw0WcMO2A07fNp/view) |

The archived analysis refs ended at
`bd450b87be24bb024fe483e2e2108c6ee82f37a5` and
`ae62d8aa7513c6985bf22343ab0a59f36ae3d406`. Both are reachable from the
current working branch. Cite these commits when discussing the corresponding
historical results. Candidate-topic notes and raw chat transcripts remain in
their existing Drive shelves. See the [Drive contract](DRIVE_LAYOUT_CONTRACT_20261109.md)
for source and output placement.


## Exhibition innovation lane — RF-CURTAIN (2026-11-21, design stage only)

- [Concept, staged gate and source boundary](../research/t2/exhibition/rf_curtain/README.md).
- [Precedents / five candidate technologies](../research/t2/exhibition/rf_curtain/PRIOR_ART_AND_ALTERNATIVES.md) and [candidate decision](../research/t2/exhibition/rf_curtain/CANDIDATE_DECISION_GATE.md): 2017/2019 Wi-Fi CSI traffic research, 2025 ESP32 CSI traffic work, 2026 Wi-Fi crossing work already exist; **no first-of-kind Wi-Fi-vehicle-detection claim**.
- [Physical first-Fresnel-zone falsification](../research/t2/exhibition/rf_curtain/GEOMETRY_GATE.md): naive 1:20 tabletop *adjacent-lane* Wi-Fi link discrimination is not supported even by a midpoint overlap plausibility check. The two measured zones should be longitudinally separated, not presented as RF camera pixels.
- [Lab pilot prespecification](../research/t2/exhibition/rf_curtain/PILOT_PREREG.md), [privacy-safe data contract](../research/t2/exhibition/rf_curtain/DATA_CONTRACT.md), [apparatus and controls](../research/t2/exhibition/rf_curtain/APPARATUS_AND_LABELS.md).
- [Parallel modeling interface](../research/t2/exhibition/rf_curtain/PARALLEL_RESEARCH_INTERFACE.md): no synthetic CSI used as empirical detection probability; only measured, verified sensor errors may later enter the traffic-state uncertainty model.
- [Software/geometry verification receipt](../research/t2/exhibition/rf_curtain/RF01_FEASIBILITY_RECEIPT_20261121.md): 12 local tests passed across four Git-blob-verified source files; **zero CSI measurements, no hardware apparatus, no field trials**.
- [Drive: RF01 source/analysis ZIP](https://drive.google.com/file/d/17zaQUPxzMo8VyYEqE5mEMLGzeswcLd3s/view?usp=drivesdk): 10,361 bytes, eight members, Drive folder `03_REPRODUCIBLE_EVIDENCE`; remote download+SHA verification remains undone.

This **E** apparatus track runs in parallel with, not as a replacement for, the prior T2 `PHYS` synthetic traffic investigation. New technology buzzwords do not imply an original research contribution or a successful physical measurement.

## 2026-11-21 current T2 source and prior-work transfer

The earlier [SF-01 robust sensor-information fusion](../research/t2/analysis/20261121/sensor-fusion/FINDINGS.md) used Long (2026) decision-time diagnostics, Huang (2025) lane/signal separation and a deliberately simplified Shafik/Rakha (2025) queue estimator. Its [43-test validation receipt](../research/t2/analysis/20261121/sensor-fusion/VALIDATION_RECEIPT.md) records an **earlier** state in which the 192-case physical screen was not yet executed. The later 704-run PHYS-01/02/03 physical study is reported separately below; do not treat the older pending statement as current. No empty K047 HTML or fabricated field scenes are considered evidence.


## Latest T2 implementation receipt — 2026-11-21

[704 synthetic physical run assessment](../research/t2/analysis/20261121/decision-time-gate/PHYS_192_384_128_FINDINGS.md) consists of original 192-case fixed-geometry screen, 384-case physically time-gated opportunity comparisons, and separately exploratory 128-case geometry sensitivity. Source/test byte fingerprints, 3 original output SHA-256 values and the 21/21 self-contained tested checks are provided in the individual receipts. The paired 48/48/16 cost comparisons are preserved as CSV in Git. **These are not 704 independent field samples or 704 validations of a real controller.** The K047 blank viewer remains retired.

### PHYS-04 through PHYS-06 — local source-derived execution, canonical exact-checkout gate open

- [PHYS-04 local checkpoint parity](../research/t2/analysis/20261121/decision-time-gate/PHYS_04_LOCAL_PARITY_AND_CHECKPOINT_TESTS.md): 144 uninterrupted/restarted baseline agreements and 1,872/1,872 matched independent-reference fields in a local source-derived Python copy; exact GitHub blob checkout is NOT yet verified. A copied `random.Random` equality-test defect was corrected.
- [PHYS-05 observation value and new seeds](../research/t2/analysis/20261121/decision-time-gate/PHYS_05_OBSERVATION_ABLATION_AND_NEW_SEED_HOLDOUT.md): 144 exploratory leave-one-seed-out cases followed by 432 genuinely unseen synthetic-seed policy pairs, with fixed k=5 policy and seed-block uncertainty.
- [PHYS-05b detector-corruption stress](../research/t2/analysis/20261121/decision-time-gate/PHYS_05B_DETECTOR_ERROR_FALSIFICATION.md): count jitter ±1/±2 and independent occupied-cell omission under the frozen policy, 8 noise replicates per nonzero setting.
- [PHYS-06 target-lane gap sensitivity](../research/t2/analysis/20261121/decision-time-gate/PHYS_06_TARGET_LANE_CLEARANCE_SENSITIVITY.md): backwards-compatible clearance parameter 1/2/3 cells, 144 paired policy comparisons with 2 strict preference reversals.
- [Research evidence manifest](../research/t2/analysis/20261121/decision-time-gate/PHYS_04_05_05B_06_EVIDENCE_HANDOFF.md), [Drive ZIP archive](https://drive.google.com/file/d/1nIHmzoz0Yk3YUqaaxvbBWH7ztgR2ddo-/view?usp=drivesdk), and [dated Google Docs reasoning](https://docs.google.com/document/d/16C7XE2dr24vfqRiz0KQMrYkOq7fARwXNm5y5l9MaTTE/edit).

**Technical gate:** obtain an exact-byte GitHub main checkout in an authenticated Python environment, run the committed tests, and compare all 144 PHYS-04 pairs against the independent references before calling the entire stage canonically reproduced. All post-PHYS-03 results remain **synthetic, uncalibrated and not field causal estimates**.


## PHYS-07–09 decision-information falsification (2026-11-21)

These are **subsequent** source-derived local studies, not extensions of the
704-run PHYS-01–03 historical study's denominator:

- [PHYS-07 — delayed observation, changed demand and arrival regimes](../research/t2/analysis/20261121/decision-time-gate/PHYS_07_LATENCY_AND_REGIME_FINDINGS.md):
  432 earlier policy outcomes rescored with stale tick observations, plus
  720 newly generated same-state control/treatment pairs from seed32–39.
- [PHYS-08 pre-registration](../research/t2/analysis/20261121/decision-time-gate/PHYS_08_FRESHNESS_FALLBACK_PREREG.md)
  and [negative result](../research/t2/analysis/20261121/decision-time-gate/PHYS_08_FRESHNESS_FALLBACK_FINDINGS.md):
  **576** prospective same-state pairs from seeds40–55 showed a
  12-second geometry fallback improved one synthetic demand regime but
  made the low-turn regime substantially worse. [Event witness script](../research/t2/physical_checkpoint_trace_witness.py)
  preserves opposite-sign contrasts under different baseline worlds.
- [PHYS-09 pre-registration](../research/t2/analysis/20261121/decision-time-gate/PHYS_09_OOD_ABSTENTION_PREREG.md)
  and [prospective findings](../research/t2/analysis/20261121/decision-time-gate/PHYS_09_TRAINING_SUPPORT_ABSTENTION_FINDINGS.md):
  **576** further same-state pairs from seeds56–71; a label-free 95th
  percentile training-support abstention avoided actions in a clearly
  out-of-support low-turn synthetic regime, at the cost of false
  exclusions under nominal traffic. This is **not** a universal or
  safety-certified OOD detector.
- [Current raw evidence handoff](../research/t2/analysis/20261121/decision-time-gate/PHYS_07_09_EVIDENCE_HANDOFF.md)
  · [Shared Drive ZIP](https://drive.google.com/file/d/13rCiN3LrVLPVrUMhUtBNpv8Ttl9Bo6Av/view?usp=drivesdk)
  · [2026-11-21 dated reasoning](https://docs.google.com/document/d/16C7XE2dr24vfqRiz0KQMrYkOq7fARwXNm5y5l9MaTTE/edit).

The PHYS-07–09 analysis runner and test blobs were individually matched
to the remote GitHub blobs. The subsequent [five-core exact-blob replay
receipt](../research/t2/analysis/20261121/decision-time-gate/PHYS_04_09_EXACT_BLOB_CORE_REPLAY_RECEIPT.md)
then established byte identity of the dual-lane engine, arrival/signal model,
receiving link, objective and decision-feature code. PHYS-04, PHYS-07,
PHYS-08 and PHYS-09 outputs were replayed against these exact core files
with byte-identical data. **A full authenticated repository clone and the
entire historical integration suite are still unverified.**


## PHYS-10–11 completed research units (2026-11-21)

- [PHYS-10 preregistration](../research/t2/analysis/20261121/decision-time-gate/PHYS_10_NEAR_SUPPORT_SHIFT_AND_TELEMETRY_PREREG.md) and [full findings](../research/t2/analysis/20261121/decision-time-gate/PHYS_10_NEAR_SUPPORT_SHIFT_AND_TELEMETRY_FINDINGS.md): **576 new same-state policy pairs**, seeds72–79, four moderate demand/turn-share shifts. Harmful signal actions remained **inside** the nominal OOD support region; under a contiguous detector blackout the veto rejected every intervention. A zero-distance counts-feature alias gave a +306 cost counterexample.
- [PHYS-11 preregistration](../research/t2/analysis/20261121/decision-time-gate/PHYS_11_GAP_CONFIRMATION_PREREG.md) and [full findings](../research/t2/analysis/20261121/decision-time-gate/PHYS_11_GAP_CONFIRMATION_FINDINGS.md): configurable 1/2/3 consecutive eligible one-second target-gap confirmation, built into `dual_lane_v11.py` and its checkpoint. **144 prospective pairs**, seeds80–87. Default1 retains historical results; **zero strict phase-policy preference reversals** were observed across confirmation choices.
- [PHYS-10/11 evidence handoff](../research/t2/analysis/20261121/decision-time-gate/PHYS_10_11_EVIDENCE_AND_REPRODUCTION_HANDOFF.md) and [Drive evidence ZIP](https://drive.google.com/file/d/1mcnPyQRoSSji5bulvK0E4tXUFOXcgTTh/view?usp=drivesdk). Exact core Git blobs + exact PHYS-10/11 runner/test blobs were locally verified. PHYS-10 and PHYS-11 JSON files were regenerated byte-identically; **34/34** targeted tests plus **8/8** separate local core-contract tests pass.

Every numerical statement is conditional on a synthetic, uncalibrated model.
Neither a field-causal effect nor a safety-certified controller is established.
No GitHub Actions or `github-actions[bot]` contributions were used; K047 stays sealed.


## T2 latest correction and clock-timing falsification — 2026-11-21

- [Critical audit](../research/t2/analysis/20261121/decision-time-gate/CRITICAL_INDEPENDENT_REVIEW_AND_CORRECTIONS.md): PHYS-10 `+306` aggregate alias was **not** a strict opposite-optimal-policy witness; canonical `uniform` request timestamps were identical across random seeds at fixed demand. The t0 checkpoint resume bug was corrected and tested.
- [Arrival-clock study preregistration A](../research/t2/analysis/20261121/decision-time-gate/T2_GREEN_ENVELOPE_AND_ARRIVAL_CLOCK_PREREG.md), [preregistration B](../research/t2/analysis/20261121/decision-time-gate/T2_ROUTE_MATCHED_CLOCK_PREREG.md), [full findings](../research/t2/analysis/20261121/decision-time-gate/T2_ARRIVAL_CLOCK_AND_GREEN_ENVELOPE_FINDINGS.md): **288 new simulated worlds** on seeds88–95 using legacy/fixed-count randomized/Poisson arrival clocks, plus **192 new worlds** on seeds96–103 holding total vehicles and ordered movement labels fixed while varying only timestamps. Two changed-timestamp cohorts produced **1/48 and 9/48 strict action-value sign differences across matching seed/geometry labels**, clustered in 1 and 3 seed blocks. Across clock worlds, t84 states and six-count observations are different; no same-observation identification claim is made.
- [Drive full evidence ZIP](https://drive.google.com/file/d/1EFAKMoixNstg9ykW6UGlwGqRq7V-_QMV/view?usp=drivesdk): 15 entries, 44,335 bytes, local SHA-256 `846d85912bf92249bc9f4ba40e198b6bbdba0587958b45ecaf336e905663fb16`. New Python source matches GitHub blob identities. Clean extracted-folder **8/8** tests and exact JSON byte-replays passed. Remote metadata was checked; remote ZIP bytes were not independently rehashed.

**Feasibility gap:** `'-'` is only a synthetic no-service state; yellow, pedestrians, cross-street conflicts and site-specific controller phase constraints remain unimplemented. The four 4/8/12/20s left-green envelopes are **not** certified legal or deployable. K047 remains sealed; no GitHub Actions used.

## 2026-11-21 post-RF01 literature reboot and collaborator audit

The R&E T2 project deliberately runs two **parallel** evidence tracks.
**E** = indoor, authorized, empirical observation/sensing prototype;
**T** = existing synthetic intersection, queue, phase and policy
identification research. No sensor measurement is simulated into
existence by the traffic model. CSI radio measurements in E: **ZERO**.

- [Complete T2 study genealogy and earlier negative-results boundary](../research/t2/analysis/20261121/reorientation/T2_RESEARCH_GENEALOGY_AND_DUAL_TRACK_GATE.md).
- [Original held 15-paper and new missing-candidate 12-paper evidence ledger](../research/t2/analysis/20261121/reorientation/T2_RF_LITERATURE_STOCK_AND_MISSING_20261121.md). 'Missing candidate' means title/DOI search did not find an original Drive PDF; not a complete-library absence proof.
- [Paper-to-executable-code transfer levels and nine-test ideal-occupancy audit](../research/t2/analysis/20261121/reorientation/SOURCE_TO_CODE_METHOD_TRANSFER_CONTRACT.md).
- [RF-CURTAIN ideal observation experiment receipt](../research/t2/exhibition/rf_curtain/RF02_IDEAL_OBSERVABILITY_AND_LITERATURE_RECEIPT_20261121.md) and [Python generator](../research/t2/exhibition/rf_curtain/rf_observation_identifiability.py): static pocket and downstream bits give 4 signatures among 5 toy classes, leaving demand-absent versus free-flow unresolved; no measured CSI.
- [2026-11-21 research reading notebook (Google Docs)](https://docs.google.com/document/d/1EBtlEcZJ5FCDgdqsmXOCLIJD-cVj8NVoTXZSB0zBxzw/edit), physically placed in the dated Kim-Woojun Drive research-log folder; [main dated reasoning](https://docs.google.com/document/d/16C7XE2dr24vfqRiz0KQMrYkOq7fARwXNm5y5l9MaTTE/edit).
- [Kim Seho's previous independent audit (2026-11-17)](https://docs.google.com/document/d/1vtBLTnL6S9m7VJPOmWnwQRVGCuwIUHewZ8SPGVFX2Bc/edit), [his 2026-11-21 dated research folder](https://drive.google.com/drive/folders/1BxbNV7-e87G9phXzWJ_TBORJ4S71KBZM), and [Claude adversarial handoff prompt](../research/t2/analysis/20261121/reorientation/CLAUDE_KIM_SEHO_CRITICAL_REVIEW_PROMPT_20261121.md). His next Google Doc must be authored by him, not fabricated by the other researcher.

Preserve the K047 protected holdout, do not use GitHub Actions/bot
contributors, and do not claim externally calibrated traffic or legal
real-road signal operation from indoor RF trials or synthetic physics.


## 2026-11-21 RF04: Research OS 00_INTAKE, original-method and calibration gate

Seven original papers from [00_INTAKE](https://drive.google.com/drive/folders/1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16) were title/author/year normalized and moved to canonical [10_PAPERS](https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP) with original IDs, metadata and destination parent independently checked. An existing-text-identical, same-size WiCross candidate was quarantined in [SHA_PENDING duplicate hold](https://drive.google.com/drive/folders/1xcWYLqJjeK6hSy48WW5sQmA5QFLxnTI6), not deleted or declared byte identical. [Seven-source intake receipt](../research/t2/exhibition/rf_curtain/RF04_INTAKE_00_LITERATURE_RECEIPT_20261121.md) and [updated missing-paper ledger](../research/t2/analysis/20261121/reorientation/T2_RF_LITERATURE_STOCK_AND_MISSING_20261121.md) supersede older candidate-missing statuses.

OpenCSI-style **scalar math-only** [pre-registration](../research/t2/exhibition/rf_curtain/RF04_OPENCSI_MATH_STRESS_PREREG_20261121.md), [runner](../research/t2/exhibition/rf_curtain/open_csi_quiet_calibration_analogue.py), [synthetic-only JSON](../research/t2/exhibition/rf_curtain/rf04_open_csi_math_fixture.json), and [31/31 RF-specific local checks](../research/t2/exhibition/rf_curtain/RF04_INTAKE_AND_CALIBRATION_VALIDATION_RECEIPT_20261121.md) are complete. This math unit shows how wrong calibration and quiet drift can defeat raw signal thresholding, **not real RF vehicle detection or the authors' OpenCSI full source replication**. The next science task is independent cross-day × cross-position *actual* CSI physical trials after approved owned equipment and a locked trial design; then separate RF information value from traffic-signal feasibility. K047 sealed; GitHub Actions disallowed.


## RF05 — cross-disciplinary idea radar + crossed RF evaluation contract (2026-11-21)

- [Diverse research-idea missing-paper register](../research/t2/exhibition/rf_curtain/RF05_DIVERSE_IDEA_FARMING_MISSING_LEDGER_20261121.md): **17 newly screened** titles and five prior missing exact originals, official literature links, proposed science-fair mechanisms and decisive failure cases. Missing means exact PDF not identified in targeted accessible Drive searches, NOT proof no paper exists or author data is public. The RF04 seven moved originals remain HELD.
- [Session × placement preregistration](../research/t2/exhibition/rf_curtain/RF05_CROSSED_HOLDOUT_PREREG_20261121.md) and [evaluator](../research/t2/exhibition/rf_curtain/rf_crossed_holdout_evaluator.py): same training data, separate P2/S2 placement, P1/S3 time, P2/S3 joint holdouts. The former single joint test was confounded.
- [Exact RF05 software receipt](../research/t2/exhibition/rf_curtain/RF05_CROSSED_HOLDOUT_VALIDATION_RECEIPT_20261121.md): **40/40 local RF-specific unit tests**, source/test/data Git blobs matching fetched GitHub main; four [artificial test cases](../research/t2/exhibition/rf_curtain/rf05_crossed_synthetic_suite_summary.json) with all gates **NOT_APPLICABLE_SYNTHETIC_FIXTURE**. No captured Wi-Fi CSI and no real lane/traffic controller result.
- Suggested independent sensor lines: low-cost magnetic/acoustic for lab negative controls; event camera static-queue failure; expensive institutional fiber DAS; info-theoretic sparse sensor placement. Do not infer that any detects why real road discharge stopped.


## RF06 — late 2026-11-21 two parallel harvest/execution streams

**23 verified P&K PDF admissions:** 20 newly uploaded traffic sensor / dynamic observability papers plus 3 late-uploaded score-validity / test-oracle / requirements papers. All moved from [00_INTAKE](https://drive.google.com/drive/folders/1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16) to [10_PAPERS](https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP) under original Drive IDs; independently checked 23/23 canonical parent and P&K filename, then confirmed the 00_INTAKE direct listing empty. Scope of reading: source abstract + selected methods, not complete full-text/reproduction. [20-source receipt](../research/t2/exhibition/rf_curtain/RF06_20_PNK_INTAKE_HARVEST_RECEIPT_20261121.md) and [three meta-method source receipt](../research/t2/exhibition/rf_curtain/RF06_META_METHOD_THREE_PAPERS_RECEIPT_20261121.md). No 5GB `CIM dataset.zip` inspection, metadata query, migration, download or unpacking; the user's live download remains on explicit HOLD elsewhere in shared Drive.

**Intellectual and experimental dual track:** [seven unconventional source-grounded exhibition idea experiments and falsifiers](../research/t2/exhibition/rf_curtain/RF06_EXHIBITION_IDEA_HARVEST_AND_RIVAL_MATRIX_20261121.md) and [nine new 2026 candidate paper links](../research/t2/exhibition/rf_curtain/RF06_NEXT_LITERATURE_NINE_NEW_20261121.md). The old RF05 missing 17 candidates have been superseded as HELD; five old exact PDF records and nine new only are currently tracked as unlocated (not a global exhaustive proof of absence).

**Executable physics-independent toy:** [preregistered ideal sensing information-vs-task risk](../research/t2/exhibition/rf_curtain/RF06_CAUSE_OBSERVABILITY_PREREG_20261121.md), [exact rational source](../research/t2/exhibition/rf_curtain/rf_cause_observability.py), [unit tests](../research/t2/exhibition/rf_curtain/test_rf_cause_observability.py), [synthetic-only JSON](../research/t2/exhibition/rf_curtain/rf06_exact_observability_results.json), [11/11 tested source/hash receipt](../research/t2/exhibition/rf_curtain/RF06_CAUSE_OBSERVABILITY_FINDINGS_AND_EVIDENCE_20261121.md). In the equiprobable P/D toy, sensor P+D has 1.5 bits but 1/4 Bayes error for pocket bit; ideal P probe 1 bit and zero such error. 2-time measurement matrix det=b-a means mathematically unidentifiable for equal dynamics. **Neither original road model reproduction nor measured physical sensor / field traffic policy**. Historical T2 PHYS work is preserved separately; exact same-state policy rank reversal remains unproved across distinct arrival-clock initial states.


### RF06-D addendum — pure Bayes action information (2026-11-21)

[Pre-registered abstract policy cost](../research/t2/exhibition/rf_curtain/RF06_POLICY_INFORMATION_VALUE_PREREG_20261121.md), [exact conditional policy source](../research/t2/exhibition/rf_curtain/rf_policy_information_value_toy.py), [9 tests](../research/t2/exhibition/rf_curtain/test_rf_policy_information_value_toy.py), [synthetic-only JSON](../research/t2/exhibition/rf_curtain/rf06_policy_value_results.json), [20/20 combined RF06 toy test receipt](../research/t2/exhibition/rf_curtain/RF06_POLICY_INFORMATION_VALUE_FINDINGS_20261121.md). Arbitrary dimensionless action deltas +3/-2: perfect pocket observation has smaller conditional oracle regret than higher-entropy overall queue measurement. This is an **elementary Bayes decision toy**, not a signal-controller or PHYS traffic experiment. No missing data imported; 5GB `CIM dataset.zip` remains uninspected HOLD.
