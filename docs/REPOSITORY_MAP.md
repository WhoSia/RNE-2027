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


### RF06 late incoming papers and primary sources (final checked snapshot 2026-11-21)

The canonical intake total grew from **23** to **29** during this live session as six further PDFs appeared. The additional **four peer-reviewed papers/preprints** were P&K-renamed and moved to `10_PAPERS`; the **1988 Abadi/Lamport DEC report and 2024 Lamport author bibliography** are **11_SOURCES**, not journal articles. All six original Drive file IDs, canonical parents and preservation statuses verified. Thus this turn ended with **27 new 10_PAPERS PDFs and 2 new 11_SOURCES PDFs**, a live 00_INTAKE direct child count of zero at its last check. [Six-source intake and methodological harvest receipt](../research/t2/exhibition/rf_curtain/RF06_LATE_SIX_ACCEPTANCE_AND_REFINEMENT_RECEIPT_20261121.md). No 5GB CIM dataset inspection or relocation.

The peer-review literature requires preserving rejected and false-positive AI code-review judgments, explaining where an executable test oracle comes from, and distinguishing merged code/accepted changes from satisfaction of a scientific requirement. This complements the 20/20 RF06 exact-math test receipt; no real CSI or signal policy proof was produced.


## 2026-11-21 follow-on research: T2 P12–P13 and exhibition RF08

The core research remains **T2 traffic physics and model-relative policy falsification**; the low-cost exhibition RF lab is a separate and independently validated track. Do not force every T2 result through RF, and do not treat a vivid RF visualization as a measured camera.

**T2 P12** — An illustrative-only phase contract was designed and coded to detect missing invented transition intervals, green-time conflicts, pedestrian timing contradictions, and adjacent duplicate stages. [P12 preregistration](../research/t2/analysis/20261121/decision-time-gate/T2_P12_ACTION_FEASIBILITY_PREREG_20261121.md), [implementation](../research/t2/analysis/20261121/decision-time-gate/t2_p12_phase_contract.py), [15 authored tests](../research/t2/analysis/20261121/decision-time-gate/test_t2_p12_phase_contract.py), [open verification and bug-repair receipt](../research/t2/analysis/20261121/decision-time-gate/T2_P12_IMPLEMENTATION_EVIDENCE_20261121.md). This is **NOT a Korean legal or safety-certified signal controller**, and the uploaded canonical tests have not been executed in a clean checkout.

**T2 P13** — A strict observational-alias test guards against treating +34/−178 arrival-clock sensitivity under DIFFERENT six-count observations as a strict same-observation cause-identification failure. [P13 pre-fixed criteria](../research/t2/analysis/20261121/decision-time-gate/T2_P13_IDENTIFICATION_AUDIT_PREREG_20261121.md), [implementation](../research/t2/analysis/20261121/decision-time-gate/t2_p13_identification_audit.py), [13 authored tests](../research/t2/analysis/20261121/decision-time-gate/test_t2_p13_identification_audit.py), [open evidence receipt](../research/t2/analysis/20261121/decision-time-gate/T2_P13_IMPLEMENTATION_EVIDENCE_20261121.md). No new PHYS simulation or real-world traffic result has been run in this stage.

**RF08 exhibition** — [official ESP-CSI minimum empirical ladder](../research/t2/exhibition/rf_curtain/RF08_OFFICIAL_CSI_MINIMUM_DEMO_GATE_20261121.md) and [independently accepted T2 simulator vs RF sensor demonstrators](../research/t2/exhibition/rf_curtain/RF08_DUAL_TRACK_EXHIBITION_ACCEPTANCE_20261121.md). CSI still requires appropriate authorized owned devices, supervision and independent truth labels; no measurements or hardware purchase were made.

All changes are targeted to `main`. No GitHub Actions/bot, sealed K047, the separately held large CIM ZIP left untouched.


## 2026-11-21 T2-P14 exact toy clock screen / RF09 source-trace gate

**T2 P14**: A deliberately small and separate four-slot, two-queue cost model exhaustively compared abstract AABB/BBAA service orders across 100 fixed-demand timestamp tapes. [Exact local source](../research/t2/analysis/20261121/decision-time-gate/t2_p14_clock_screen.py), [14 exact-blob-matched local tests](../research/t2/analysis/20261121/decision-time-gate/test_t2_p14_clock_screen.py), [machine-readable 100-world result](../research/t2/analysis/20261121/decision-time-gate/t2_p14_results.json), [findings](../research/t2/analysis/20261121/decision-time-gate/T2_P14_FINITE_QUEUE_CLOCK_FINDINGS_20261121.md), [structural symmetry / post-hoc sensitivity correction](../research/t2/analysis/20261121/decision-time-gate/T2_P14_SYMMETRY_AND_SENSITIVITY_AUDIT_20261121.md).

Result: 39 AABB-favored / 39 BBAA-favored / 22 ties. **This symmetry is mathematically enforced by equal lane treatment and complete swapped-tape enumeration** and must not be cited as an empirical frequency. Fourteen locally executed tests and all three committed artifact Git blobs were hash-compared to the executed files. This is **NOT a PHYS engine run, sensor measurement, or operational signal test**.

**RF09 Harvest**: [first-party CSI acquisition versus viral camera-like display](../research/t2/exhibition/rf_curtain/RF09_CSI_FIRST_PARTY_VS_VIRAL_VISUALIZATION_HARVEST_20261121.md). Official Espressif sender/receiver examples establish a realistic *measurement target*, not verified object localization. Cheap optical/magnetic baselines and independent empty/static/moving truth labels remain essential; no hardware was obtained or used.

Both tracks remain independent until model-real observation evidence exists. No GitHub Actions/bot, no K047 access, no CIM dataset inspection.


## 2026-11-22 — Collaborator review and new daily custody

- Shared R&E Research Log parent: [daily folders](https://drive.google.com/drive/folders/15HIj9OU7e63K2kuVnxGJY00nxGsmNODZ).
- New folder: [20261122 김우준의 사유](https://drive.google.com/drive/folders/1wIlGAxjTuhYW0GNoBrjZV2i4t5yHJ3Xf).
- Dated Google Docs note: [independent review verdict and T2/RF handoff](https://docs.google.com/document/d/1Zo0Z-Q50o3f7oLvOF-73vKOCQcDGLq5fynmGaStm0kA/edit).
- Collaborator original: [20261121 김세호의 사유 — independent Claude critique](https://docs.google.com/document/d/15CFAM0QsRQkYNGUvf3VEyISxG9Pxyz-I_4WX32CAQp8/edit). Retain attribution and historical authorship.

**P15:** [Adversarial review and verified paper-arithmetic receipt](../research/t2/analysis/20261122/P15_COLLABORATOR_CLAUDE_AUDIT_RECEIPT_20261122.md) confirms a specific inconsistent published Table I via source PDF and independently recomputed F1/weighted recall. Reviewer's local `f1e57b0` is NOT pushed; do not count it as a remote project commit or re-author his patch. [Preregistered RF class-to-T2 state/decision sufficiency contract](../research/t2/analysis/20261122/P15_RF_TO_T2_STATE_INTERFACE_PREREG_20261122.md) distinguishes staged toy-zone labels from policy-relevant traffic state; no new physical CSI measurement or strict PHYS action-reversal witness yet.

The older 2026-11-21 folders remain intact. All updates to repository `main`; GitHub Actions and bot commits forbidden; K047 sealed and the ~5GB CIM dataset stays on HOLD.


### 2026-11-22 P15 exact artificial decision-interface implementation and reviewer separation

[Nov22 P15 index](../research/t2/analysis/20261122/README.md), [originally frozen interface prereg](../research/t2/analysis/20261122/P15_RF_TO_T2_STATE_INTERFACE_PREREG_20261122.md), [exact source](../research/t2/analysis/20261122/p15_rf_decision_sufficiency.py), [19 tests](../research/t2/analysis/20261122/test_p15_rf_decision_sufficiency.py), [generated JSON](../research/t2/analysis/20261122/p15_rf_decision_sufficiency_results.json), [exact byte/hash and limitations](../research/t2/analysis/20261122/P15_1_EXACT_DECISION_SUFFICIENCY_FINDINGS_20261122.md), [김세호 independent-review mandate](../research/t2/analysis/20261122/P15_INDEPENDENT_PEER_REVIEW_MANDATE_20261122.md).

This **pure mathematical checker** was implemented and tested locally (19/19 unit tests PASS), then its final code, test and generated-output Git blobs on `main` were read back and matched to the executed local bytes. Three *invented* cost-table cohorts distinguish within-label state aliasing from lack of common optimal action, including a legitimate common-action null. A deliberate correction replaced the potentially ambiguous pocket-only downstream-free-cells=0 fixture with a nonzero downstream capacity; the coarse JSON did not change, so the exact code and fixture hashes are essential.

No new traffic engine simulation was run; no live signal or CSI observation occurred. **Independent reviewer 김세호 may inspect, falsify and provide attributed patches but does not automatically commit to `main`; development and integration are owned by 김우준.**


### 2026-11-22 P16 — Read actual T2 checkpoint schema before labeling any RF cause

[Checkpoint schema and physical transfer audit](../research/t2/analysis/20261122/P16_CHECKPOINT_INTERFACE_FINDINGS_20261122.md), [fail-closed adapter](../research/t2/analysis/20261122/t2_p16_checkpoint_contract.py), and [20 exact-blob-matched local tests](../research/t2/analysis/20261122/test_t2_p16_checkpoint_contract.py).

The adapter is grounded in `dual_lane_v11.checkpoint_observation` and `physical_checkpoint_capacity_screen.py`. It distinguishes pocket presence, receiver fullness and receiver *entry-cell* occupancy. **A full link necessarily occupies cell 0 under the one-car-per-cell assumption; cell-0 occupancy alone does not imply full.** The output expressly leaves the five causal/manual RF labels UNKNOWN, not inferred from one simulator snapshot.

A second function can screen independently provided PHYS-04 result rows for same-six-count opposite-effect candidates but **was not executed on real PHYS-04 results in this unit**. The 20/20 local regression suite used invented schema fixtures. No claim of found same-observation PHYS witness, physical CSI measurement or deployable signal controller is made.


### 2026-11-22 P17 — Historical PHYS-04 archive re-downloaded, 144 authentic model outcomes audited

[Findings](../research/t2/analysis/20261122/P17_HISTORICAL_PHYS04_EXACT_ARCHIVE_FINDINGS_20261122.md), [exact-byte checksum-pinned script](../research/t2/analysis/20261122/p17_zip_audit.py), [9 executed tests](../research/t2/analysis/20261122/test_p17_zip_audit.py), and [compact model-result JSON](../research/t2/analysis/20261122/P17_PHYS04_VERIFIED_ARCHIVE_SUMMARY_20261122.json).

A fresh Google Drive download confirmed exact ZIP SHA256 `7f7eff90b83cfe5e1f071bb02d5880face9c0e047abcd17349cd3fb06392758e` and contained authentic historical PHYS-04 **source-derived, not byte-identical canonical-engine** cost data (144 pairs). Under full geometry and six-count matching, 133 observation groups, 11 collision groups, **one weak pair (−305,+1) at epsilon0, ZERO strict opposite-sign pairs at epsilon5**. With occupied-cell positions also matched: 141 groups, 3 collision groups, zero opposing signs. A deliberately **invalid** comparison omitting B-share manufactures two apparently strong contrasts, including `−305/+1477` in the SAME seed. Do not cite this as a true observation alias or independent arrival-day evidence.

The historical archive is now remote-byte checked; its model implementation is still described by its original source-derived provenance. No new canonical engine run, physical CSI measurements, field estimates, or real controller operations occurred.


### 2026-11-22 P18 — First exact-five-blob canonical PHYS-04 rerun and fresh arrival-clock experiment

**Canonical source code finally run locally**: all five exact `main` Python blobs (dual lane, spatial timing, receiver, objective, PHYS-04 executor) were fetched through GitHub, byte-preserving transferred via [dated manifest](https://docs.google.com/document/d/1NCnqkEJpeUL03d7MAuy2F_DlprxGGOxlpAurA6gwjB0/edit), restored and separately verified by `git hash-object`. Re-executing `physical_checkpoint_capacity_screen.py` reproduced **144/144 historic PHYS-04 `pairs` records exactly**, including model policy costs and decision observations. The *whole JSON files* are not byte-equal because wrappers/summary keys differ.

A prospectively fixed [P18 256-world timing+position+abstract-action experiment](../research/t2/analysis/20261122/P18_PROSPECTIVE_CLOCK_POSITION_ACTION_PREREG_20261122.md) then used fresh seeds104–111. Two clock types retained the same total vehicles and ordered turn-route sequence. In all **128 paired clock comparisons** for each of the 4s and 8s model-native intervention definitions, zero `epsilon=5` strict sign reversals occurred; among full-geometry same-six-count groups, also zero strong sign aliases. **32**, not 256, unique full arrival tapes due to repeated geometries. A six-second *invented model* minimum left-green gate excludes the 4s option and leaves the 8s option eligible on minimum duration alone; **real amber/red/pedestrian and controller feasibility are still unknown**.

[Full P18 analysis, exact hashes, limits](../research/t2/analysis/20261122/P18_CANONICAL_REPLAY_AND_PROSPECTIVE_FINDINGS_20261122.md); [executable runner](../research/t2/analysis/20261122/p18_clock_position_action.py); [15 passed tests](../research/t2/analysis/20261122/test_p18_clock_position_action.py); [summary JSON](../research/t2/analysis/20261122/P18_EXACT_MAIN_SUMMARY_20261122.json); and [five-test posthoc service-event witness](../research/t2/analysis/20261122/p18_exploratory_service_witness.py). The exploratory 8s-versus-4s comparison was 0 better, 10 worse and 246 ties across the 256 geometry-worlds; no generalization is justified. **No GitHub Actions, no K047 unsealing, no held CIM data touched, no actual CSI.**


### 2026-11-22 P19 — Prospective finite receiving storage and downstream offset evidence

[Pre-outcome P19 design](../research/t2/analysis/20261122/P19_RECEIVER_SERVICE_OPPORTUNITY_PREREG_20261122.md), [exact-source mechanism runner](../research/t2/analysis/20261122/p19_receiver_service_opportunity.py), [9 passing tests](../research/t2/analysis/20261122/test_p19_receiver_service_opportunity.py), [complete findings](../research/t2/analysis/20261122/P19_RECEIVER_SERVICE_OPPORTUNITY_FINDINGS_20261122.md), [summary JSON](../research/t2/analysis/20261122/P19_RECEIVER_SERVICE_SUMMARY_20261122.json).

New seeds112–119, two demand regimes, receiver capacities2/4, downstream offsets0/15, pockets14/28m and B allocation0/.5 gave **256 synthetic world/tick84 paired-policy evaluations** from **16 genuinely distinct whole arrival tapes**, re-used across geometries. All results were generated twice, byte-identically (SHA256 `0681f683acd549cb2d32cc8957038ce3e652819f47e8288c5a751b6acd7e2468`). **9/9** tests passed using exact local/git-blob-matched runnable sources.

Within each 64-world stratum, 8s model left intervention favored treatment/baseline/tie: capacity2 offset0: **17/47/0**; capacity2 offset15 **16/0/48**; capacity4 offset0 **16/14/34**; capacity4 offset15 **19/0/45**. Additional early L stopline crossings and later receiver-entry rejection counts were explicitly logged. **No epsilon5 strict opposite policy-sign pairs** among 128 geometry-matched *cross-offset* comparisons. These are **different predecision physical states** across offsets/capacities, not same-state receiver-setting effects. The unchanged intervention still lacks actual amber/red/pedestrian or field calibration. **Do not present these counts as real-world road efficiency or safety conclusions.**

The 2026-11-22 dated Google Docs research log remains the research argument source; GitHub main is the code/provenance authority. No GitHub Actions/bot, sealed K047 preserved, held ~5GB CIM ZIP unopened.


### 2026-11-22 P20 — Internal event audit, first observed-data source gate, and missing large-ZIP custody

[P20 512-path independent receiver event ledger](../research/t2/analysis/20261122/P20_EVENT_LEDGER_AND_EXTERNAL_MODEL_GATE_20261122.md), [P20 code and tests](../research/t2/analysis/20261122/README.md), [event-result manifest](../research/t2/analysis/20261122/P20_EVENT_LEDGER_RESULTS_20261122.json), [independent DLR-UT 15-minute observation time gate](../research/t2/analysis/20261122/P20_DLR_OBSERVED_TIME_ALIGNMENT_FINDINGS_20261122.md), [source-sealed DLR observation summary](../research/t2/analysis/20261122/P20_DLR_UT_REAL_OBSERVATION_15MIN_SUMMARY_20261122.json), [public-dataset inventory and large-ZIP custody](../research/t2/analysis/20261122/P20_DATASET_INVENTORY_AND_CIM_CUSTODY_20261122.md).

The exact five-blob T2 core and P19 branches underwent an independent receiver-cell shadow reconstruction: **256 synthetic worlds × 2 branches = 512 paths, 122,880 ticks; 9/9 exact-main local tests passed, no detected consistency mismatches**. All 256 existing P19 cost/tape records were reproduced, but this does not constitute SUMO or real-world agreement. A pair of original DLR-UT v1.3.1 2023-09-24 23:30–23:45 UTC raw files was SHA-sealed and analyzed: 8,624 trajectories from 37 IDs and 26,970 signal readings from 30 IDs; **5/5 exact-main local parser tests passed**. No matching stopline/signal-head map or empirical time-headway is yet demonstrated.

Existing DLR v1.3.1, CityArtery.zip and SUMO scenarios remain in their proper data-lake folders. Open Utah SPaT/BSM and ESPARGOS static CSI are prioritized *future possible* acquisitions, not completed downloads. About-5GB `CIM dataset.zip` was not located in the connected Drive; **NO MOVE** occurred. Empty quarantine destination folder [CIM UNVERIFIED_HOLD](https://drive.google.com/drive/folders/1BWRCLDTyvRkQZRIUloZo63EHDGIlgjet) is created and verified. Never invent file ID, SHA or a successful move. K047 sealed; no bot commits or physical interventions.


### 2026-11-22 P21 — Observed signal timing, low-speed proxy and INTERACTION inbound staging

[Read-only DLR observation and INTERACTION receipt](../research/t2/analysis/20261122/P21_DLR_OBSERVATION_AND_INTERACTION_INTAKE_FINDINGS_20261122.md), [exact-main tested P21 source](../research/t2/analysis/20261122/p21_dlr_segment_gate.py), [8 exact-source tests](../research/t2/analysis/20261122/test_p21_dlr_segment_gate.py), [machine manifest](../research/t2/analysis/20261122/P21_DLR_SIGNAL_RUNS_AND_INTERACTION_CUSTODY_20261122.json). **Real DLR sampled data:** 37 tracked objects, 30 signal IDs, 869 state-code changes and 899 runs; 4 IDs have pairs of <=0.5m/s speed, but neither real queues nor actual phase colors/stopline headways have been established. Exact `main` code/test 8/8 local tests PASS.

Two user-downloaded INTERACTION TC/DR compressed archives were not present in accessible Google Drive or conversation runtime; therefore **NO actual file move has occurred**. [Immutable originals receiving folder](https://drive.google.com/drive/folders/1k-EEwOyBgUVoQaGwQsModGfmP92w0Gzv) has been created under `02_DATASETS/20_OBSERVED — International`. Once user uploads originals or provides their accessible Drive IDs, preserve their bytes, verify sizes/hashes and parent IDs, and then analyze copied derivatives without altering originals.


### 2026-11-22 P22 — Adversarial independent-unit review and preregistered measured stopline comparison

[BFS/DFS research replay and six-role skeptical review](../research/t2/analysis/20261122/P22_ADVERSARIAL_MULTIROLE_FINDINGS_20261122.md), [preinspection-gated observational protocol](../research/t2/analysis/20261122/P22_ADVERSARIAL_REALITY_GATE_PREREG_20261122.md), [exact-source tested audit code](../research/t2/analysis/20261122/p22_block_and_stopline_audit.py), [7 tests](../research/t2/analysis/20261122/test_p22_block_and_stopline_audit.py), and [structured independent-units and DLR source SHA evidence](../research/t2/analysis/20261122/P22_ADVERSARIAL_STOPLINE_AND_BLOCK_RESULTS_20261122.json).

P19 256 simulated worlds reuse only **16** complete arrival tapes. Aggregate offset0 policy-cost sign reverses when one seed (115 or 118) is removed, while offset15 has 0 harmful effects in **16 tape clusters**, not 128 independent examples. Exact IID conditional upper bound 0/16 is 17.07% (Wolfram numerical cross-check); it is NOT a validated field failure confidence bound.

Three DLR 1s observed movement-count files on Sun 2023-09-24 were audited under precommitted time windows: 12:00 436 crossing indicators/32 movement channels, 18:00 192/27, 23:30 17/12. Source movement channel columns vary; counts do NOT directly identify congestion or signal phases. Seven original-input tests PASS. [P22 proof ZIP stored on shared Drive](https://drive.google.com/file/d/1ZbIMHN_4r7xU_xckynxcnlMLB_MG-d35/view), 9,771 bytes, re-downloaded and SHA256-equal to local source (73badd36c839968018d9e2420195a3431379895ec4d5e5b22d0609f6506543f8). No restricted archive opened, no live controller changed, no GitHub Actions/bot, no independent model reviewer falsely claimed.


### 2026-11-22 P23 — Real DLR publisher codebook resolves signal color without falsely resolving lane control

[Publisher primary PDF page14 state mapping and page12 motor/VRU signal groups](../research/t2/analysis/20261122/P23_OFFICIAL_DLR_CODEBOOK_AND_SIGNAL_PURPOSE_FINDINGS_20261122.md), [source-locked audited code](../research/t2/analysis/20261122/p23_dlr_official_signal_codebook.py), [5 real-source tests](../research/t2/analysis/20261122/test_p23_dlr_official_signal_codebook.py), [compact results](../research/t2/analysis/20261122/P23_OFFICIAL_DLR_SIGNAL_CODEBOOK_RESULTS_20261122.json). Actual DLR original PDF Figure1/Table4 distinguishes green(5), yellow(7), red(3), red+yellow(4), flashing yellow(9), and special motor protected green/yellow codes (6/8), with ID1–9 motor, ID10–29 VRU and ID30 flashing warning; 30 sampling gaps >1.5sec prevent subsecond transition claims. **5/5 source-backed tests PASS.** Exact local/source hashes verified. [P23 Drive ZIP](https://drive.google.com/file/d/1OpitphlBVFnSrcnRWpYwBvk9sQME0nL9/view) was uploaded then re-downloaded, 5,139 bytes, SHA256 bee87e23aca56bf7cff53d79090291c763b68a0823f35183defd19dd628c7e73 equal. Signal-vehicle lane correspondence and independent SUMO still OPEN; no field controller operations.


### 2026-11-22 P23/P24 — Raw DLR 3-source geometry proof and official signal-code resolution

[P23 real geospatial & official stopline findings](../research/t2/analysis/20261122/P23_DLR_GEOMETRY_AND_STOPLINE_FINDINGS_20261122.md) and [P24 official DLR v1.3.1 signal semantics](../research/t2/analysis/20261122/P24_OFFICIAL_SIGNAL_CODEBOOK_AND_GEOMETRY_FINDINGS_20261122.md), with exact-source implementations, 7+7 locally executed tests, machine-readable JSON in [20261122 analysis](../research/t2/analysis/20261122/README.md).

P23 uses 3 original SHA-verified DLR assets: v1.3.1 OpenDRIVE, UTM trajectory CSV, exact-window official 1-second movement crossing CSV. **8,389/8,624 tracked position samples within 10m of projected centerline**; wrong +100m coordinate shift drops to 584/8,624. Official late-night metadata contains 17 positive movement crossing bins across 12 columns and 893 seconds; no identity-matched headways.

P24 exact-version PDF Table 4 identifies code1 off, code3 red, code4 red+yellow, code5 green, code7 yellow and code9 flashing yellow, verified against all 26,970 live samples. Official Table 3 lists **35 physical points from 26 distinct signal IDs; IDs 10–13 have no coordinates**, though all 30 appear in live data. There are 869 sampled code changes, including 171 3→5 and 168 5→3 adjacent-code observations, **not proof of unsafe or omitted yellow/clearance** under 1Hz sampling. Signal pole coordinate≠verified signal-lane assignment. No independent SUMO run or traffic policy recommendation. Main-only commits, K047 sealed, unlocated CIM ZIP HOLD; INTERACTION TC/DR not yet found in accessible Drive despite user PC downloads.


### 2026-11-22 P25–P29 — Further exact-core T2 synthetic intervention tests and score identifiability

**[Full five-stage followup findings](../research/t2/analysis/20261122/P25_P29_PHYSICAL_FOLLOWUP_FINDINGS_20261122.md)**; full code, preregistration, tests and result links at [20261122 research index](../research/t2/analysis/20261122/README.md). These extend P19 original headway/capacity/offset physical simulation **without changing the frozen 256-world P19 result**.

- **P25**: 192 synthetic receiver-headway worlds (1/2/4 sec), four original complete demand tapes; cost effects with 8s abstract left intervention beneficial/harmful/tie per 64 worlds **47/0/17; 18/12/34; 0/0/64**; P19 headway2 rows 64/64 verified.
- **P26**: 64 same-checkpoint model-worlds, 6/8/10s actions **all equal in scalar cost per world**, but receiver-denial attempts increase across all worlds.
- **P27**: 128-world exploratory event-traced longer green stages, 24s beats 6s in 64, ties in 64. The 24s condition was motivated by pilot output and **must not be called a confirmatory discovery**.
- **P28**: 64/64 P26 6s-vs10s pairs share the exact terminal score but have **4 more denial-attempt events**, 128/128 P27 cases likewise; 32/128 also have additional modeled L stopline crossings with equal scalar score. Raw denial-attempt event frequency ≠ unique blocked cars and is opportunity-conditioned.
- **P29**: truly unused **synthetic** seed labels120–123, 128 worlds, 4 unique arrival tapes, protocol committed before experiment. At downstream offset15 all **64/64** 24s vs6s show lower model cost; at offset0 all **64/64** tie. Not independent empirical traffic observation or same-state causality across offsets.
- **26/26 local tests passed** and repeat runs byte-identical. Source exact Git blobs verified. [Full reproduction ZIP](https://drive.google.com/file/d/1U8KErQrF_7YyXGUvH4CM0AawchRkJuDQ/view) uploaded to shared Drive research evidence and independently SHA-readback verified (**93,782 bytes, SHA256 9de9ab34333c4afd8ba3e54d901a503b1a9a76096fa6a4f692b8b5052ce442fd**); [delivery receipt](../research/t2/analysis/20261122/P25_P29_EXACT_DELIVERY_MANIFEST_20261122.json).

This evidence establishes only repeatable **internal synthetic simulator** mechanisms. It does **not** validate real traffic light yellow/all-red/pedestrian clearance, real road operation, independent SUMO physics, or RF sensing. Next research gate: distinct-vehicle receiver blockage, vehicle-level waiting times, different arrival-law families and independent published DLR/SUMO physical comparison. No GitHub Actions/bot, K047 sealed, large CIM ZIP HOLD and INTERACTION archives pending visible Drive upload.


## 2026-11-22 P30–P32: identity measurement, new-clock counterexamples and canonical branch audit

- [P30–P31 full analysis directory](../research/t2/analysis/20261122/README.md): original deterministic simulator preserved, P30/31 per-ID refusal and new-arrival-clock stress, 20/20 final tests. Eight new full arrival tapes in P31; 9/128 new synthetic worlds break the original 6s/10s model cost equality, while P30 found 34/64 worlds with extra distinct receiver-denied vehicle despite unchanged model score.
- [P32 full evidence and paper-axis critique](../research/t2/analysis/20261122/P32_ID_CORRIDOR_EXIT_AUDIT_AND_PAPER_AXIS_20261122.md): 192 replayed synthetic worlds, 12 complete arrival tapes; **47** worlds with equal score, aggregate counts and throughput but different vehicle-ID stopline/receiver exit events. **11/11** tests. All P31 historical rows have mislabeled `baseline_score` (actually `remaining`); P32 fixes interpretation without changing frozen files. Event inference is internal, not external traffic validation.
- [P32 exact reproduction ZIP](https://drive.google.com/file/d/1Y2xY7q6PRGqU3gtBO3iJmsQCDQ2xH1uz/view) in shared evidence shelf, 53,959 bytes, SHA256 `f8cea1babfceb841da6087f5563f9877b4771ad46fc52005d508d01706558b12` and matching re-download. [P32 Notion Harvest L](https://app.notion.com/p/420ef561cf9281688691dd9ffd4a537f) is a short idea record, not source of experiment truth. [Four archived R&E conversation pattern audit](../research/t2/analysis/20261122/P32_CHAT_ARCHIVE_PI_PATTERN_AND_DELIVERABLE_PRIORITY_20261122.md) establishes practical **exhibition model** vs scientific **paper hypothesis** distinct tracks.
- **Branch consolidation:** `research/t2-spatial-fig2-v02` is a strict ancestor of main (0 unique commits, main ahead by 336 at 2026-11-22 audit); no merge necessary. `main` remains the canonical single development branch. **Old branch is NOT remotely deleted yet**: the connector lacks a delete-ref method; delete it in GitHub Branches UI after reviewing [branch audit](../research/t2/analysis/20261122/P32_MAIN_ONLY_BRANCH_CONSOLIDATION_AUDIT_20261122.md). No force push/history rewrite. The lack of deletion does not change main's canonical content.


### 2026-11-22 P24 — Official DLR field-map UTM join and hard stop on invented signal/lane control

[Research analysis](../research/t2/analysis/20261122/P24_DLR_MAP_JOIN_AND_P23_CORRECTION_FINDINGS_20261122.md), [map-space code](../research/t2/analysis/20261122/p24_dlr_map_join_gate.py), [physical road-reference diagnostic](../research/t2/analysis/20261122/p24_geometry_proximity_check.py), [9 local tests](../research/t2/analysis/20261122/test_p24_dlr_map_join_gate.py), [machine-readable result and provenance](../research/t2/analysis/20261122/P24_DLR_MAP_JOIN_GATE_RESULTS_20261122.json). Source DLR map original 28 roads, static sign IDs300600–300607, motor field signal IDs1–9 cannot be matched by shared ID. 18 documented vehicle signal heads/9 unique IDs converted into map CRS; 8,624 measured positions map to georeference with nearest road-reference median3.572m/p95=7.416m; map proximity is NOT control mapping, lane assignment or actual crossing. Three preregistered volume windows contain 32/27/12 movement columns and `West0West1`, cannot equate tokens with OpenDRIVE lane ID. P23 previous locked PDF digest was incorrect for the actual published file; original 4/5 re-run error, corrected 5/5 PASS, Git P23 source and structured manifest amended with failure evidence preserved.

[**P24 shared Drive 9-file ZIP**](https://drive.google.com/file/d/1OX2RpxVZQMF7A6aTZUA1VW8Glsju5Amq/view) downloaded back and SHA256 equal `cb677b5b98dcdb29d669b9fd41a9dd766259eb8c606ada9c1883193916875e9e`. It contains local tested source, full results, logs and per-file checksums; nine regression tests passed locally, but GitHub exact-blob replay of the new P24 source remains pending. Official [TASI](https://github.com/DLR-TS/TASI) CSV parser consumes rather than constructs publisher volume route labels, so it cannot close the controlling-signal mapping gate. Primary school science-fair work remains actual regional traffic-engineering improvements, not validation machinery alone.

### P24 + P24b (2026-11-22): DLR original 2015 map vs 2023 active head crosswalk and stopline geometry

[P24 full geometry evidence and provenance correction](../research/t2/analysis/20261122/P24_XODR_STOPLINE_AND_SIGNAL_CROSSWALK_FINDINGS_20261122.md); [P24b structural role audit](../research/t2/analysis/20261122/P24B_JUNCTION_TOPOLOGY_FINDINGS_20261122.md). Original DLR OpenDRIVE 2015 map has 28 roads, 1 junction, 7 static `type=294` features with six IDs 3006xx; the real DLR 2023 light IDs 1–30 have no embedded match. Table3 PDF has 18 official vehicle-head coordinates. Nearest marker ≠ controlling light. Junction structural role separates **4 inbound candidate**, 1 outbound marker, 2 interior connectors and identifies duplicate geographic ID 300607. Exact-main original-source tests P24 9/9 and P24b 7/7 PASS; verified full reproduction ZIP files [P24](https://drive.google.com/file/d/1D0_iQ-FPHXvpjeH7Oy_5pYRkXqV85RQj/view) and [P24b](https://drive.google.com/file/d/112UeWG-AYdWaEktOW5jYCoxZIDYthvG5/view). Note corrected official PDF current SHA 94fd9ebd…34f3, historical P23 ZIP previously referenced a different SHA. Next physical work is individual lane/direction stopline crossing and 1Hz vs 20Hz validation; no field causal claim.


### 2026-11-22 P34-OBS — Source-locked 20Hz DLR stopline center-crossing reconciliation

[Full report and amendment to P24b XML lane-validity misread](../research/t2/analysis/20261122/P34_OBS_DLR_STOPLINE_RECONCILIATION_FINDINGS_20261122.md), [23 source-backed tests](../research/t2/analysis/20261122/test_p34_dlr_stopline_event_reconciliation.py), [runner](../research/t2/analysis/20261122/p34_dlr_stopline_event_reconciliation.py), [compact evidence](../research/t2/analysis/20261122/P34_OBS_DLR_STOPLINE_RECONCILIATION_SUMMARY_20261122.json). Observed 2023-09-24 23:30–23:45Z: real XODR center-plane crossings 17; producer same-source 1Hz route counts 17; max-cardinality min-time one-to-one matching by approach ±1s **16/17**, median 0.59025s; the unmatched East 23:32:16.505Z crossing and South 23:36:10Z official count (only downstream-first-frame left-censor candidate) remain OPEN. All detected brackets 50ms. Prior P24b searched nonexistent `validity` XML; corrected `laneValidity` appears in **all 7 source static features** and source-lock regression 7/7 passes, BUT its 2015 lane scope retains only 7/17 matched geometry candidates, so it is not an authoritative 2023 route/controller mapping. Actual original-source P34 tests **23/23 PASS** and GitHub main bytes equal tested code. Same raw optical-track genealogy means this is a **dataset internal consistency result**, not independent field validation, verified route destination, field signal optimization, or SUMO cross-calibration. No branch or Actions created.


[P34-OBS delivered exact-source ZIP on shared Drive](https://drive.google.com/file/d/1DPABAywIBwQc7uZZjI37dvJ4-e7wt65F/view), 19,867 bytes, re-downloaded and SHA256 verified `bb8701db35578951e82202845c5fa9b65d5ee55afb31c1afed22292e65a3c679`. The frozen bundle contains 10 entries: 2015 map geometry reader, corrected P24b, P34 observed crossing and tests, full internal 17-event result, log and SHA manifest; no raw publisher data. [20261122 research decisions in Google Docs](https://docs.google.com/document/d/1Zo0Z-Q50o3f7oLvOF-73vKOCQcDGLq5fynmGaStm0kA/edit) appended and read back.
