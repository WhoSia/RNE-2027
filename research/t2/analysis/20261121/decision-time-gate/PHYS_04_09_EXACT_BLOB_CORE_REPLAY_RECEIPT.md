# PHYS-04–09 exact-blob core replay receipt — 2026-11-21

**Result: PASS for the 5-module exact-blob core and PHYS-04/07/08/09 numeric replay. Full git checkout/integration suite: still OPEN.**

## Why this is stronger than previous source-derived execution

The first T2 experiment runtime used a small reconstructed version of the
`spatial_v10` and `receiving_cells_v15` APIs and a shortened local
`dual_lane_v11` file. This receipt replaces that ambiguity. We read
the current **`main` blobs** through the GitHub connector, restored
the exact UTF-8 files in a local Python 3.13.5 runtime and independently
computed their Git blob SHA-1 using `git hash-object`.

| Repo path under `research/t2/` | GitHub blob SHA-1 = local git hash-object |
|---|---|
| `dual_lane_v11.py` | `eb78b4de62629fa205ec66749a7faa00869d0bb1` |
| `spatial_v10.py` | `ffbf3fc3f8b9a64a819d4f73ce70b264b877e84e` |
| `receiving_cells_v15.py` | `b078cf215c74b76ace6dffcbcbacab6ae22c3673` |
| `physical_transfer_screen.py` | `8d75745053ff720db6c8af0001aaaf13ba1f295e` |
| `physical_checkpoint_observation_ablation.py` | `db9ceb2774ee1b7e70728a340b50d41f4c884c18` |

The PHYS-07/08/09 experiment scripts and tests also matched their
individual published GitHub blobs, as recorded in
[the prior evidence handoff](PHYS_07_09_EVIDENCE_HANDOFF.md).
This is a **file-specific cryptographic identity check**, not a claim
that a `git clone` from GitHub or every repository module/test was used.

## Replayed numerical claims

After swapping in these exact five module blobs and setting
`PYTHONPATH` to the verified core, we executed:

1. PHYS-04: all **144** direct-vs-checkpoint baselines were equal;
   independently written reference across **13 mapped outcome fields
   per case (1,872 comparisons) had 0 discrepancies**.
2. PHYS-07: all 432 lagged-observation cases and 720 shifted-regime
   paired controls generated output identical to the sealed previous
   `phys07_result_v2.json`.
3. PHYS-08: all 576 prospective matched policy cases generated output
   identical to the sealed previous `phys08_result_v2.json`.
4. PHYS-08 event witness: the exact same crossed stopline records and
   opposite-sign cost results were regenerated.
5. PHYS-09: all 576 prospective pairs generated output identical to
   the sealed previous `phys09_result_replay.json`.
6. **20/20** PHYS-07/08/09 Python test methods passed when imported
   against the five exact-blob core modules (Python 3.13.5).

Every output comparison in items 2–5 used **full file byte comparison**
(`cmp`), not merely rounded group summaries.

| Output | Byte-identical SHA-256 |
|---|---|
| PHYS-04 144 pairs | `0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001` |
| PHYS-07 lag and 5 demand regimes | `8af92319b5732f607482de3d2f990879914d27a64fddf7108be9e57c3f312daa` |
| PHYS-08 12s fallback | `8994b32bcd4011d776ac222bd42922136d7acf1b6398a65fa544b1c3a29363f2` |
| PHYS-08 trace | `47ed567d3d9fdb27d66473d7bcb3a6ed4746646faa24fc7f610ea8aafb94d452` |
| PHYS-09 support abstention | `2902a6090f1d08f6362525e8c51bcf9b566f05b6452bb1b77cea43e33e7974df` |

**Nuance:** the PHYS-04 runner `canonical/run_comparison.py` itself
is a local audit program rather than an exact repository copy; its output
provenance text retains the older identifier
`LOCAL_RECONSTRUCTED_FROM_MAIN_SOURCE_NOT_BYTE_VERIFIED`, but this
receipt supplies independent evidence that its actual imported
transitions, generator, receiver, score and feature-map files now
match the exact GitHub blobs. The PHYS-07/08/09 runner files were
individually Git-blob checked in the prior stage.

## Open gates

- No authenticated full `git clone` was possible from the isolated
  execution environment (GitHub DNS unavailable). A complete repository
  tree SHA and all other T2 tests have therefore **not** been certified.
- `physical_checkpoint_capacity_screen.py`, original
  `test_physical_checkpoint*.py` suites, and all earlier 704-run
  integration/legacy tests have not been executed *as exact repo files*
  in this receipt.
- No calibrated field observations, detectors, signal-controller
  constraints, legal minimum green, driver behavior or K047 holdout
  were included.

This closes the **core transition-logic identity ambiguity** for the
named PHYS experiments, but not the whole-project gate. No GitHub
Actions were invoked, and all experiments remain synthetic.
