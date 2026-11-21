# RF05 — Crossed session/placement holdout evaluator: executed validation receipt

2026-11-21 · **SYNTHETIC_EVALUATOR_CONTRACT / NOT EMPIRICAL RF PERFORMANCE**.

## Research motivation and precommit
Earlier [RF pilot](PILOT_PREREG.md) tested only P2/S3, which changes both acquisition session and antenna placement. That design cannot attribute a failure separately to temporal drift versus mounting geometry. [RF05 pre-registration](RF05_CROSSED_HOLDOUT_PREREG_20261121.md) was committed first (`9f55cf18694a734d973d23f5953d6a441ef1da84`). A 3-session ×2-placement ×5-class ×10-reset artificial collection design fixes 100 P1/S1-S2 training trials; three nonoverlapping 50-trial diagnostic/primary groups P2/S2 (placement), P1/S3 (session), P2/S3 (joint); P2/S1 held unused (50). Class-proportionality and six-cell completeness are checked and missing RF samples remain abstentions.

Source [rf_crossed_holdout_evaluator.py](rf_crossed_holdout_evaluator.py) and [test_rf_crossed_holdout_evaluator.py](test_rf_crossed_holdout_evaluator.py) reuse the prior RF evaluator's fixed class label set, numeric features, fit, per-class confusion and metrics. No learning occurs on diagnostic/test groups. No new classifier, CSI generator, synthetic RF traces or signal control added.

## Locked artificial falsification output

**All numeric values below belong to mathematically constructed test fixtures with class labels encoded in artificial CSI feature columns. They are not measured Wi-Fi observations.** F1=1.0 in baseline is deliberately easy because we manufactured separable features.

| Artificial perturbation | placement-only test CSI macro-F1 | session-only test CSI macro-F1 | joint test CSI macro-F1 |
|---|---:|---:|---:|
| None, deliberately separable class-encoded features | 1.0000 | 1.0000 | 1.0000 |
| P2-placement feature offset +2000, no S3 shift | 0.0667 | 1.0000 | 0.0667 |
| S3-session feature offset +2000, no P2 shift | 1.0000 | 0.0667 | 0.0667 |
| P2 and S3 feature offsets both +2000 | 0.0667 | 0.0667 | 0.0667 |

All scenarios have **`primary_gate=NOT_APPLICABLE_SYNTHETIC_FIXTURE`**, regardless of displayed F1. The RSSI two-link artificial baseline F1 is about 0.0667 in each group (both RSSIs constants), intentionally not evidence of a real modality advantage.

An additional test removes one CSI value from joint S3/P2 `both`: the model abstains on exactly 1/50, class `both` recall falls to 0.9 and the class remains in the denominator. Discarding an entire session/cell/label, adding an S4 cell, mixing artificial with declared real provenance, or feature-leaking session/label identifiers are explicitly challenged.

Machine-readable [four-scenario JSON](rf05_crossed_synthetic_suite_summary.json):
- local SHA-256 `6d8239bb28b6807f84a4ec2d4b6973b31303b040bde41a4fa5d7e51c97ed2759` (3,059 bytes);
- locally computed git blob `12658aa2736e95c3d044578e6c903879dc3b7c8b` **equal to GitHub main fetch**.

## Executed code contracts

- Python **3.13.5**, local independently invoked full **RF-only** test discovery: **40/40 passed**; 9 new RF05 tests + 31 previously registered RF01–RF04 tests.
- The executed RF05 source local git blob `961ef22561eb72dbb381d1d0dea3019827efa292`, test local git blob `674ad74bd6c05ab5a5a0faafdbfe4030ee631bed`: **both identical to GitHub main fetched blob SHAs**. Dependency `rf_pilot_evaluator.py` executed blob `3ed96b70c8b8569424480c0ba12940d07ee8266f`, also identical to GitHub main.
- Synthetic case JSON twice reproducible through deterministic fixture construction; no raw RF signals were read, no network traffic intercepted, no real signal controller accessed.
- The entire historical T2 checkout test suite, a hardware integration test, and the original OpenCSI upstream author-code execution are **NOT claimed** here. K047 sealed, no Github Actions/bot commits.

## Critical methodology limitations

- Calling S2/P2 *placement-only* is conditional on **P1 S2 having been included in training**; this is not a randomized physical causal intervention.
- S1/P2 is held in unused reserve, and only 3 collection sessions would exist under the minimum design. No well-powered general population CI or multi-lab transfer inference can follow from 3 sessions.
- The test's `measured_authorized_lab` marker is a declared string, not cryptographically verified data provenance. The evaluator can only emit `PASS_PROVISIONAL_REQUIRES_SOURCE_AUDIT` for apparent real data until independently inspecting raw measurement bytes and truth labels; test fixtures merely relabeled as measured must never be submitted as RF measurements.
- The original RF pilot P2/S3 threshold still determines the primary outcome. The diagnostic cells cannot be used for hyperparameter selection if the final heldout inference is to stay credible.
- A physical 'pocket' vs 'downstream' toy object label is NOT proof of real transportation blocking or of a worthwhile traffic signal action. Sensor vs traffic-policy validation remain separate.

## Expanding idea farming while retaining current research

New [17-item cross-modal exact-PDF-not-located radar](RF05_DIVERSE_IDEA_FARMING_MISSING_LEDGER_20261121.md) across fiber DAS, magnetometers, beamforming, mmWave, event cameras, thermal, information-theoretic observability and traffic shockwaves. Combined with five previously missing specific originals, this is **22 exact-PDF-not-located candidate records**, not 22 globally absent publications. Existing OpenCSI/ESPARGOS/SensingWall/Brunello/Chen originals were already admitted in RF04 and must not be mislabeled as missing.

**Decision**: ACCEPT software split contracts and paper candidate register. HOLD claims about actual CSI generalization, physical queue cause discrimination and safe signal intervention. Next real gate is obtaining approved real CSI hardware and independent cross-day × cross-placement trials; no purchase or roadside installation assumed.
