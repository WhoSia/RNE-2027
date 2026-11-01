# T2 v2.3 — Source parity and event counting audit (2026-11-01)

Status: **remote/archived source parity FAILED; archived executable internal counting PASSED**.

## Provenance
Archived Drive ZIP: T2_v22_world_contact_physics_repro.zip. Remote branch: research/t2-spatial-fig2-v02. Read remote via GitHub connector. Local archive manifest SHA256: 10/10 PASS.

## Source disparity
Remote vs archive fixed character counts:
- dual_lane_v11.py: 11760 vs 12477
- spatial_v10.py: 8085 vs 9800
- receiving_cells_v15.py: 3574 vs 2106
- test_physical_invariants_v22.py: 1897 vs 1987

All four also differ by noncryptographic FNV-1a fingerprints. This proves source mismatch, not necessarily which is correct. Do not label remote as independently validated v2.2.

## Independent local execution gate
Archive extracted and imported with PYTHONPATH=fixed. Five archived invariant tests: 5/5 PASS. Independent audit invoked the fixed simulator for 8 seeds × 3 bay lengths × 2 lane-change modes = 48 runs. Zero discrepancies against archived fixed_v22 CSV rows for exits, per-movement exits, lane change count, motion violations and event counts. Total motion violations: zero.
- Receiver denial attempts = count of denied service events: 48/48
- Receiver denial seconds = cardinality of unique denial timestamps: 48/48
- Pocket block seconds = count of exact denied pocket-entry events: 48/48
- Blocker ID key present in every denied pocket-entry event: 48/48
- 10/10 manifest SHA256 file checks pass.

Limitations: This validates archive implementation consistency; it does not show remote parity, independently reproduce the baseline 48 runs, verify video/roadside truth, or establish the physical validity of the 1-cell-per-step model.

## Next gate
1. Reconcile source files across repository and executed archive without silently overwriting later development.
2. Add external reference event reconstruction, explicit event ordering tests and exact blocker identity assertions.
3. Re-run full suite from an exact GitHub checkout locally (no GitHub Actions).
4. Keep results synthetic until field measurements and holdouts.

Governance: no GitHub Actions, no bot-authored commits, no main merge before provenance repair.
