# RNE-2027

Collaborative R&E 2027 research repository.

## Active research

- **T2 — Spatial Traffic Dynamics:** signalized intersections, short left-turn bays, finite storage, spillback, and lane-specific throughput.
- Other candidate projects remain separate until the team agrees to pursue them.

Start with the [repository and Drive map](docs/REPOSITORY_MAP.md) for active T2 code, data receipts, and verification records.

## Collaboration and preservation

- **Canonical working branch: `main`.** Review changes against `main` and commit reviewed, independently meaningful research increments directly to it. Do not create new research branches as routine workflow. Historical branches may remain temporarily for preservation and migration.
- Do not use GitHub Actions for normal experiment execution, and do not attribute research contributions to `github-actions[bot]`.
- Commit frequently, ideally 10–20 substantive commits per multi-cycle research unit when the actual scope supports it; avoid empty changes or artificial commit inflation.
- Record dated reasoning, failures, decision gates, and next steps in the shared R&E 2027 Google Docs. Keep original papers, large inputs and research artifacts in the shared Drive, while GitHub holds code, tests, reproducible configurations and concise verification receipts.
- Keep source-paper reproduction, model assumptions, synthetic results, external-simulator comparisons, and field observations explicitly distinct.
- Never commit credentials, private data, identifiable traffic recordings, or copyrighted source PDFs.

## Current T2 decision gate (2026-11-21)

The earlier three linked PHYS studies (192 + 384 + 128 synthetic runs) found model-dependent interactions among pocket geometry, lane-change opportunity timing and phase order. See [the 704-run synthesis](research/t2/analysis/20261121/decision-time-gate/PHYS_192_384_128_FINDINGS.md).

**PHYS-04/05/05b/06:** state-identical signal interventions, unseen synthetic demand seeds, detector jitter and configurable target-lane clearance. [Earlier evidence ledger](research/t2/analysis/20261121/decision-time-gate/PHYS_04_05_05B_06_EVIDENCE_HANDOFF.md).

**PHYS-07/08/09:** 720 new matched pairs under observation lag / demand shift, 576 pre-registered pairs testing a 12-second geometry fallback, and 576 further pre-registered pairs testing 95th-percentile training-support abstention. The geometry fallback **failed** under low-turn demand; the support-abstention heuristic avoided this synthetic loss but excluded beneficial nominal cases. None is a road-safety claim. [Current evidence ledger](research/t2/analysis/20261121/decision-time-gate/PHYS_07_09_EVIDENCE_HANDOFF.md) · [shared Drive ZIP](https://drive.google.com/file/d/13rCiN3LrVLPVrUMhUtBNpv8Ttl9Bo6Av/view?usp=drivesdk).

**Verification boundary:** new analysis scripts and local files have matching Git blob digests; the simulator's full imported dependency tree is still **source-derived, not a verified exact-byte GitHub checkout**. The K047 field holdout remains sealed.

### PHYS-10 / PHYS-11 (2026-11-21): decision support failure and explicit gap physics

- [PHYS-10](research/t2/analysis/20261121/decision-time-gate/PHYS_10_NEAR_SUPPORT_SHIFT_AND_TELEMETRY_FINDINGS.md) used **576 pre-registered matched policy pairs** on unused seeds72–79. Even a zero-distance counts-feature match admitted a harmful synthetic action; correlated detector occlusion made the OOD veto suppress all interventions. In-support feature similarity is not a safety guarantee.
- [PHYS-11](research/t2/analysis/20261121/decision-time-gate/PHYS_11_GAP_CONFIRMATION_FINDINGS.md) introduced optional **1/2/3 consecutive eligible-tick lane-change confirmation**, with default 1 maintaining historical model outcomes. **144** new pairs on seeds80–87 produced **zero strict policy-rank reversals**, an explicit null finding.
- [Reproduction and Drive handoff](research/t2/analysis/20261121/decision-time-gate/PHYS_10_11_EVIDENCE_AND_REPRODUCTION_HANDOFF.md): five GitHub core blobs, runners and tests verified against local source; **34/34** relevant tests pass and PHYS-10/11 JSONs have byte-identical reruns. **Whole-repository authenticated clone and full historical tests remain an OPEN gate.**

The cellular model is an **uncalibrated research prototype**, not a VISSIM reproduction, field causal estimate, or road-control recommendation. The K047 holdout remains sealed.
