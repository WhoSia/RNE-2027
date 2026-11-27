# RNE-2027

Collaborative R&E 2027 research repository.

## Active research

- **T2 — Spatial Traffic Dynamics:** signalized intersections, short left-turn bays, finite storage, spillback, and lane-specific throughput.
- **RF-CURTAIN — Parallel T2 exhibition sensing research:** camera-free multi-link Wi-Fi CSI as a *hypothesis* for distinguishing pocket-vs-downstream blockage on an authorized indoor model; currently **no real CSI data, no detector or road-signal validation**. [Scientific prior art, apparatus and 21 unit tests](research/t2/exhibition/rf_curtain/README.md) · [2026-11-21 source and missing-paper ledger](research/t2/analysis/20261121/reorientation/T2_RF_LITERATURE_STOCK_AND_MISSING_20261121.md).
- Other candidate projects remain separate until the team agrees to pursue them.

Start with the [repository and Drive map](docs/REPOSITORY_MAP.md) for active T2 code, data receipts, and verification records.


### Exhibition R&D prototype: Adaptive Resolution Lab (2026-11-27)

An [offline executable laboratory prototype](research/t2/exhibition/adaptive_resolution/README.md) connects uncertain observation, causal belief updates, hard pathwise acquisition budgets, exact/limited-depth planning, and model-based optimality certificates. See [acceptance and negative findings](research/t2/exhibition/adaptive_resolution/RND_ACCEPTANCE.md), [R&D priorities](research/t2/exhibition/adaptive_resolution/RND_PRIORITIES.json), and the [Drive release R1](https://drive.google.com/file/d/1SOIABscETeUKg9i0aFg9op9AiPfgeARl/view).

Strong class-informed fixed-policy comparisons show only 0–0.015655% mean cost gains on the conditional synthetic population; large real-world improvement claims remain unsupported. The prior traffic-model and RF tracks are preserved. No field calibration, road actuation, real RF collection, K047 holdout use or student-independent acceptance. The next engineering priorities are measured observation reliability, multiple objective tradeoffs, and independent paired tabletop/model verification.

**R2 (2026-11-27):** [objective-aware engine acceptance](research/t2/exhibition/adaptive_resolution/RND_OBJECTIVE_ACCEPTANCE.md), [teacher/student tabletop protocol](research/t2/exhibition/adaptive_resolution/TABLETOP_PROTOCOL_R2.md), [revised priorities](research/t2/exhibition/adaptive_resolution/RND_R2_PRIORITIES.json), [R2 reproducible package](https://drive.google.com/file/d/196oe4j4jL6vE-fJJjj-HZmeHfWzZJUxe/view). 64 objective contexts; two-step exactness fails in one, and eight lack a depth-two certificate. The stronger fixed-calendar comparator leaves only three positive gains in sixteen tested cap/objective/class/law contexts (maximum 0.626%). No field improvement claim. R1 remains intact.

### Parallel exhibition prototype: RF-CURTAIN (2026-11-21)

A **separate**, teacher-supervised, indoor/tabletop, camera-free RF sensing
research direction is now under [RF-CURTAIN](research/t2/exhibition/rf_curtain/README.md).
The question is whether two **longitudinal** Wi-Fi channel observations can
distinguish turn-bay entrance obstruction from downstream congestion, not
whether a Wi-Fi signal can literally produce traffic camera images.
Wi-Fi CSI vehicle sensing already has prior art. A 2.4GHz/1m first-Fresnel
zone has ~0.177m midpoint radius; naive adjacent-lane resolution is NOT
established. A trial-level evaluation pipeline and 12 local tests exist, but
**no project CSI measurements, field trial, physical apparatus or real
signal actuation has been completed**. See [RF01 proof boundary](research/t2/exhibition/rf_curtain/RF01_FEASIBILITY_RECEIPT_20261121.md).

The existing synthetic T2/PHYS work continues as the **independent modeling
track** and may only ingest RF detector-error data after measured, verified
laboratory trials. No hardware purchase, bystander Wi-Fi tracking or public
traffic-signal changes are authorized by this research plan.

## Collaboration and preservation

- **Canonical working branch: `main`.** Review changes against `main` and commit reviewed, independently meaningful research increments directly to it. Do not create new research branches as routine workflow. Historical branches may remain temporarily for preservation and migration.
- Do not use GitHub Actions for normal experiment execution, and do not attribute research contributions to `github-actions[bot]`.
- Research defaults to continuous discovery → prioritization → execution → verification → reassessment, with no loop numbering. Keep research-unit identifiers for traceability, not as counts of accomplishments. Reassess marginal evidence, alternatives and exhibition readiness before continuing.
- From 2026-11-27, the only active missing-literature register is [Research OS / 00_INTAKE / 00_MISSING_LITERATURE.txt](https://drive.google.com/file/d/1NtFbOpy9Mcv_f-f_iIr6adDuZQTyWoy1/view). Do not create new parallel missing-paper tables; historical ledgers remain historical. Check intake, duplicates and editions, append verified missing works and remove acquired works, keep sequential item numbers, date, UTF-8 BOM and LF, and read back changes.
- Commit frequently, ideally 10–20 substantive commits per multi-cycle research unit when the actual scope supports it; avoid empty changes or artificial commit inflation.
- Record dated reasoning, failures, decision gates, and next steps in the shared R&E 2027 Google Docs. Keep original papers, large inputs and research artifacts in the shared Drive, while GitHub holds code, tests, reproducible configurations and concise verification receipts.
- Keep source-paper reproduction, model assumptions, synthetic results, external-simulator comparisons, and field observations explicitly distinct.
- Never commit credentials, private data, identifiable traffic recordings, or copyrighted source PDFs.

## Current T2 decision gate (2026-11-21)

The earlier three linked PHYS studies (192 + 384 + 128 synthetic runs) found model-dependent interactions among pocket geometry, lane-change opportunity timing and phase order. See [the 704-run synthesis](research/t2/analysis/20261121/decision-time-gate/PHYS_192_384_128_FINDINGS.md).

**PHYS-04/05/05b/06:** state-identical signal interventions, unseen synthetic demand seeds, detector jitter and configurable target-lane clearance. [Earlier evidence ledger](research/t2/analysis/20261121/decision-time-gate/PHYS_04_05_05B_06_EVIDENCE_HANDOFF.md).

**PHYS-07/08/09:** 720 new matched pairs under observation lag / demand shift, 576 pre-registered pairs testing a 12-second geometry fallback, and 576 further pre-registered pairs testing 95th-percentile training-support abstention. The geometry fallback **failed** under low-turn demand; the support-abstention heuristic avoided this synthetic loss but excluded beneficial nominal cases. None is a road-safety claim. [Current evidence ledger](research/t2/analysis/20261121/decision-time-gate/PHYS_07_09_EVIDENCE_HANDOFF.md) · [shared Drive ZIP](https://drive.google.com/file/d/13rCiN3LrVLPVrUMhUtBNpv8Ttl9Bo6Av/view?usp=drivesdk).

**Historical verification note:** the earlier PHYS-07–09 analysis began as a source-derived local runtime. A later audit restored and SHA-verified five GitHub core blobs, and replayed specified outputs exactly. **A full authenticated repository checkout and the entire historical regression suite remain unverified.** K047 remains sealed.

### PHYS-10 / PHYS-11 (2026-11-21): decision support failure and explicit gap physics

- [PHYS-10](research/t2/analysis/20261121/decision-time-gate/PHYS_10_NEAR_SUPPORT_SHIFT_AND_TELEMETRY_FINDINGS.md) used **576 pre-registered matched policy pairs** on unused seeds72–79. Even a zero-distance counts-feature match admitted a harmful synthetic action; correlated detector occlusion made the OOD veto suppress all interventions. In-support feature similarity is not a safety guarantee.
- [PHYS-11](research/t2/analysis/20261121/decision-time-gate/PHYS_11_GAP_CONFIRMATION_FINDINGS.md) introduced optional **1/2/3 consecutive eligible-tick lane-change confirmation**, with default 1 maintaining historical model outcomes. **144** new pairs on seeds80–87 produced **zero strict policy-rank reversals**, an explicit null finding.
- [Reproduction and Drive handoff](research/t2/analysis/20261121/decision-time-gate/PHYS_10_11_EVIDENCE_AND_REPRODUCTION_HANDOFF.md): five GitHub core blobs, runners and tests verified against local source; **34/34** relevant tests pass and PHYS-10/11 JSONs have byte-identical reruns. **Whole-repository authenticated clone and full historical tests remain an OPEN gate.**

The cellular model is an **uncalibrated research prototype**, not a VISSIM reproduction, field causal estimate, or road-control recommendation. The K047 holdout remains sealed.

### Adversarial correction and arrival-clock falsification (2026-11-21)

- [Critical internal review](research/t2/analysis/20261121/decision-time-gate/CRITICAL_INDEPENDENT_REVIEW_AND_CORRECTIONS.md): the PHYS-10 zero-distance +306 witness shows unequal effect magnitude but **does not itself establish strict opposite-optimal actions** (its matched training case ties). The legacy "uniform" traffic generator holds arrival timestamps fixed across integer seeds at the same demand rate.
- [Two pre-registered arrival-clock studies](research/t2/analysis/20261121/decision-time-gate/T2_ARRIVAL_CLOCK_AND_GREEN_ENVELOPE_FINDINGS.md) evaluated **288 synthetic traffic worlds** under three timing generators (seeds88–95) plus **192 worlds** with exact vehicle count and ordered route labels held fixed while only request timestamps change (seeds96–103). The latter produced **1/48 and 9/48 strict effect-sign differences across corresponding timing-world labels**, respectively, in two demand regimes. These are **different predecision states**, not equal-observation identification counterexamples.
- Four green durations (4/8/12/20s) were tested; the engine cannot represent complete real yellow/pedestrian/conflicting-stage/controller requirements. **No proposed plan is certified legal, safe or deployable.** [Drive raw ZIP](https://drive.google.com/file/d/1EFAKMoixNstg9ykW6UGlwGqRq7V-_QMV/view?usp=drivesdk). New standalone runner/test blobs match GitHub `main`, 8/8 clean-extraction tests and full JSON byte-replay pass.

Next scientific priority: calibrate temporally varying arrivals and specify a locally admissible signal-action set **before** claiming real controller consequences. Keep synthetic outcomes, implementation validation and field evidence separate.
