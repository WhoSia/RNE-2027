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

**New PHYS-04/05/05b/06:** source-derived local execution compared 144 same-state signal interventions against independent references, tested a 432-case unseen synthetic seed set, assessed observation noise, and exposed target-lane clearance assumptions. The exact GitHub blob checkout and committed test-suite certification are **still pending**. See the [evidence handoff and verification gate](research/t2/analysis/20261121/decision-time-gate/PHYS_04_05_05B_06_EVIDENCE_HANDOFF.md) and [shared Drive ZIP](https://drive.google.com/file/d/1nIHmzoz0Yk3YUqaaxvbBWH7ztgR2ddo-/view?usp=drivesdk).

The cellular model is an **uncalibrated research prototype**, not a VISSIM reproduction, field causal estimate, or road-control recommendation. The K047 holdout remains sealed.
