# PHYS-04 — local transition-logic parity and regression repair (2026-11-21)

## Status: local source-derived execution PASS; exact repository-byte execution PENDING

The ChatGPT Python container could not resolve github.com by DNS, and the
available Vercel environment was not authorized. For execution, the T2
dual-lane state-transition code was copied from a live GitHub connector read
of main into a local Python runtime. Imported spatial_v10 and
receiving_cells_v15 APIs were copied as locally equivalent implementations
rather than byte-for-byte checked-out repository files. **Therefore this is
not an exact-blob canonical checkout or an upstream CI pass.** Do not label
it as one.

The 144 paired conditions were nevertheless executed locally with the
source-derived dual-lane logic. For all 144 conditions at t=84:

- uninterrupted baseline == full-state checkpoint/resume baseline;
- same exogenous arrival tape and unchanged physical configuration held within
  each control-versus-policy pair;
- 13 mapped metrics across all 144 conditions matched the independently
  implemented reference, **1,872/1,872 comparisons, zero discrepancies**;
- model conservation assertions and road occupancy assertions passed.

The 13 fields included control/treatment costs, three terminal penalties'
deltas, remaining vehicles, S/L downstream exit counts and lane changes.
Their agreement is structural model replication, **not field validation**.

Local 144-pair JSON SHA-256:
`0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001`.

## Regression test defect and repair

An old regression test compared a checkpoint directly with
`deepcopy(checkpoint)`. This is a false equality oracle because
`random.Random` objects do not implement content-based equality.
The test failed on an otherwise unchanged checkpoint.

Changed the committed test to compare
`pickle.dumps(checkpoint, protocol=4)` before and after branching or
observation extraction. The local copied engine returned identical serialized
checkpoint bytes after resumption. Eight additional local regression
assertions (including trace/no-trace; cells/FIFO; invalid gaps; no-lookahead
observation; unsafe phases; conservation and historical witness) passed.

**Remaining work before a canonical tag:** copy exact GitHub blobs into a
reproducible checked-out environment; run committed unit tests and 144-pair
canonical command; compare all same fields with the independent reference;
record Python version and exact Git HEAD; compare byte-identical rerun output.
No GitHub Actions were used.

## Research verdict

The earlier reconstructed model's numerical reference is corroborated by a
separately instantiated copy of the current transition rules and explicit
resume-identity assertions, but the source-bitwise and distribution-level
reproducibility gate remains open. Maintain SYNTHETIC_UNCALIBRATED status and
do not treat 1,872 numerical checks as 1,872 independent field observations.
