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
