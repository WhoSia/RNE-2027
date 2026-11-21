# PHYS-07 through PHYS-09 — Reproducible evidence handoff

Date 2026-11-21 · T2 in R&E 2027 · `main`

## Shared Drive evidence

[PHYS-07 / PHYS-08 / PHYS-09 evidence ZIP](https://drive.google.com/file/d/13rCiN3LrVLPVrUMhUtBNpv8Ttl9Bo6Av/view?usp=drivesdk)

Drive file ID `13rCiN3LrVLPVrUMhUtBNpv8Ttl9Bo6Av`; folder
`20261121 김우준의 사유`, parent ID
`198h73YvJlPeBC0l3U-rar1q9zLPmsI9j`. Authenticated Drive
metadata readback confirmed MIME `application/zip`, **71,380 bytes**,
and membership of the project shared Drive.

- Locally created ZIP SHA-256:
  **`6ad4757770bc1dde1570fefb36aa81604d7f27ce7c782cbf193dd98839d80e72`**.
- **23 archive members**; ZIP `testzip()` passed. Includes original
  PHYS-04 training and PHYS-05 holdout input cases, PHYS-07/08/09
  analysis source/tests, new raw result JSON, trace witnesses, local
  reconstructed source-derived runtime, `README.md`, and
  per-file-SHA `MANIFEST.json`.
- Upload success and Drive file metadata were confirmed, but the ZIP
  has **not** been downloaded afresh from Drive and its remote bytes
  independently SHA-verified; do not claim an authenticated raw-byte
  seal. Previous PHYS-04–06 bundle remains separately available.

## Provenance and numeric receipts

| Unit | New paired model worlds | Result SHA-256 | Local tests |
|---|---:|---|---:|
| PHYS-07: 432 historic held-out decision cases under five ages, 720 new matched demand-shift pairs | 720 newly simulated | `8af92319b5732f607482de3d2f990879914d27a64fddf7108be9e57c3f312daa` | 7/7 |
| PHYS-08: frozen 12s fallback on seed40–55, two regimes | 576 newly simulated | `8994b32bcd4011d776ac222bd42922136d7acf1b6398a65fa544b1c3a29363f2` | 5/5 |
| PHYS-08 event-level opposite-sign witness | two within-regime paired runs | `47ed567d3d9fdb27d66473d7bcb3a6ed4746646faa24fc7f610ea8aafb94d452` | 3/3 |
| PHYS-09: locked 95th-percentile OOD abstention on seed56–71 | 576 newly simulated | `2902a6090f1d08f6362525e8c51bcf9b566f05b6452bb1b77cea43e33e7974df` | 5/5 |

All four local JSON outputs were regenerated and matched **byte for
byte**, and **20/20** focused regression methods executed successfully.
This is not 1,872 or 720 independent field observations. All values
are simulator-native objective units, not measured vehicle delays.

Exact Git blob digests of the **new analysis/test files** were
verified against the GitHub `main` connector and local files,
including PHYS-07
`0d6831eb651536deaadc0095044f1e08811b612e`,
PHYS-08 `887acba7146b10c68ffcbee51764f668325968b0`,
the trace witness `c1a666f7d0ee89265f8577a978dafe5ea52f8f60`,
and PHYS-09 `0e5811f7c73a7562389b22597379e7e45cc177f5`.

**IMPORTANT OPEN GATE:** the underlying imported dual-lane engine and
helper modules in the local Python execution were independently copied
from source inspections, not obtained from a clean byte-for-byte
checkout of the complete GitHub repository. The analysis scripts'
exact Git blob equality does **not** close this engine provenance
gap. The repo default branch may still be the historical branch,
so pass `main` explicitly to all GitHub write operations.

## Study notes and verdicts

- [PHYS-07 latency and demand-regime findings](PHYS_07_LATENCY_AND_REGIME_FINDINGS.md).
- [PHYS-08 preregistration](PHYS_08_FRESHNESS_FALLBACK_PREREG.md)
  and [prospective negative-result findings](PHYS_08_FRESHNESS_FALLBACK_FINDINGS.md).
- [PHYS-09 preregistration](PHYS_09_OOD_ABSTENTION_PREREG.md)
  and [prospective training-support findings](PHYS_09_TRAINING_SUPPORT_ABSTENTION_FINDINGS.md).

The main research decisions were (i) stale observations can alter
policy selection substantially, (ii) a blanket geometry-based
fallback fails under shifted low-turn demand, and (iii) a
training-support abstention heuristic avoided *one clearly separated*
synthetic low-turn regime at the cost of excluding useful nominal
interventions. None establishes actual field safety or a universal
distribution-shift guarantee. Do not tune the PHYS-09 threshold on
already inspected seeds and re-present those same seeds as holdout.

## Next executable gates

1. Verify the entire source dependency tree by exact Git `main`
   checkout in a trusted Python environment; rerun all test scripts.
2. Download the Drive ZIP and compare its raw SHA if claiming
   cloud-side cryptographic verification.
3. Pre-register intermediate/hidden shifts, delayed and correlated
   missing observations, and new untouched seeds. Require
   false-negative OOD witnesses and coverage-utility analysis.
4. Keep field K047 sealed until its separately controlled release.
   GitHub Actions and `github-actions[bot]` remain prohibited for
   research execution.
