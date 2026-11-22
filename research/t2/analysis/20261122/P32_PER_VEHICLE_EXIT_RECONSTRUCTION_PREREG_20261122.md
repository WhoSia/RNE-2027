# T2 P32 prereg — corridor-ID conservation and aggregate-equivalence falsification

Date 2026-11-22; main-only new work. This is **exploratory** after P30 and P31. Reuse the unchanged exact GitHub-main `dual_lane_v11`, `receiving_cells_v15`, `p25_p26` and `p31` routines. No live traffic controller and no purported legal clearance.

## Two linked analyses
P32-A: 64 P30 geometry/tape worlds, 6s versus 10s synthetic left stage, same tick84 checkpoint. P32-B: 128 P31 fresh arrival-family geometry worlds, 6s versus 10s, same within-world tick84 checkpoint. In total 192 **synthetic worlds**, **12 unique complete full-timestamp arrival tapes** (4 older, 8 fresh), not 192 independent experimental realizations.

Reconstruct downstream **per-vehicle network exits** as a new third-party *observation-side event ledger*, without modifying core:
- `frames[t].receiver` ID set: compare consecutive snapshots. Previous receiver IDs missing from the next snapshot indicate candidate exits. Validate each candidate had exactly one earlier `stopline_cross` and does not reappear; all crossing IDs accepted into receiver post-crossing (cells mode); no departure may precede admission.
- Reconstructed route-by-route exit totals must match `network_out_S/L`, and final snapshot receiver occupancy must match `receiver_final`. Vehicle IDs never leave receiver except through its tick event under original deterministic model; the reconstruction is a **trace audit**, not independent physics.
- Run all 6s/10s policy pairs from exact same tick84 checkpoint. Verify original core returns same outputs with and without trace. Abort on empty/malformed receiver frames, repeated IDs, event route mismatch or conservation failure.
- Pair *common vehicle IDs* across policies: (a) cross/no-cross sets and timestamp deltas; (b) corridor exit/no-exit sets and timing deltas; (c) new policy IDs crossing; (d) per-ID arrival→network exit intervals only where both complete. Track unmatched IDs and right censoring rather than imputing zeros.
- Primary result: number of **score-equal** worlds with changed individual crossing event or per-ID network-exit time, and score-different worlds with events unchanged. Maintain branch/generation structure and record all 192 paired rows.

## Independent hostile audit gates
- Inject forged receiver frame exit (premature disappearance) and exact network-out mismatch; should abort.
- Duplicate stopline crossing, impossible admission, ID reappearance, mutation of original checkpoint, insufficient sampling horizon: fail closed.
- Cross-check `result.score = physical_transfer_screen.score` and every stored output's prior P30/P31 cost/demand counts. Critical known data-quality issue: archived P31 result field `baseline_score` is incorrectly written as `baseline["remaining"]`. Retain archived bytes, document field as INVALID_LABEL; compute a correctly labeled baseline score separately.
- Avoid treating agent-side reconstruction as SUMO or independent real-world field calibration.
- If no event changes occur in score-equivalent worlds, report that null result directly and shift effort to real DLR/SUMO validation.

## Practical next gate
The paper question is partial identification of policy ordering under coarsened detector inputs and finite downstream storage, distinct from reinventing pocket spillback. Showcase concrete paired counterexamples and a simple baseline before proposing an information-value policy.
