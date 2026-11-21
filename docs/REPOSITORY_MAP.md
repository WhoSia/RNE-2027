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
