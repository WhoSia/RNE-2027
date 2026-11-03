# T2 v6.3-P0 — 20261103 cross-lab research receipt

Canonical collaboration surface: **Shared Drive / 02_RESEARCH_LOG / 20261103 김우준의 사유**, not a private root folder. Docs ledger ID: 1oxsUpQ6W_A71FqC_9D7_YKQCj7XHQejbLI6mfcMW-9U.

## Reproducible source and data
[Full experiment ZIP, 29 files](https://drive.google.com/file/d/16bdDAcN0JnMDm-Hp4QNCDOSUQjMnatSC/view)

SHA-256 of final ZIP: `5b4a1ea194cf025b49dc930b30791a852b3c7260b8fecacd343a7ebbe1e3a6d9`

Contents: exact unchanged single-junction v6.2 baseline code; idealized viability module; deterministic tests; original v6.2 factorial CSV; paired cluster-bootstrap analysis; 288-run brake×turn-acceleration×demand heterogeneous experiment; 160-run prespecified fresh-seed response audit; 30-run observation-channel comparison; raw CSV/JSON; reviewer report; per-file SHA-256 manifest. **14 new tests passed, 478 new synthetic simulator executions, 144 historical simulations analyzed from saved output**.

## GitHub work and limitations
Subdirectory `research/t2/analysis/20261103/v63/` contains separately committed theory, experimental design, reviewer gate, heterogeneity, aggregate alias, new-seed holdout, and measurement resolution audits. `research/t2/theory/v63/viability_envelope.py` is a standalone theoretical kernel. **The full experimental Python scripts/data are in the Drive ZIP and are not yet all committed individually to GitHub**; do not assert full source sync.

No empirical driver calibration, SUMO confirmation, collision-free physical operating guarantee, structural identifiability theorem, or policy-ranking reversal was established.

Next scientific gate: quantify observation channel resolution/noise/cost and target regret, and design braking-state reachability for actual IDM upstream integration.
