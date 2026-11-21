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

The three linked PHYS studies (192 + 384 + 128 synthetic runs) found model-dependent interactions among pocket geometry, permissible lane-change opportunity timing, and signal-phase order. Next, preserve an identical predecision microscopic state at tick 84, then branch only the postdecision intervention and compare paired outcomes. See [the synthesis](research/t2/analysis/20261121/decision-time-gate/PHYS_192_384_128_FINDINGS.md).

The cellular model is an **uncalibrated research prototype**, not a VISSIM reproduction, field causal estimate, or road-control recommendation. The K047 holdout remains sealed.
