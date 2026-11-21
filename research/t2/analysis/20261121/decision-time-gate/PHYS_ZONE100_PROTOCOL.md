# T2-PHYS-03 — exploratory 100m lane-change-zone repair for 70m pocket

**Design entered before execution (2026-11-21).** This is exploratory sensitivity prompted by an observed geometric degeneracy in the earlier preregistered 70m pocket grid. Do not replace the original zero-change observation in the earlier tables.

Fix the original 70m pocket (10 cells), 7m approach cells, 720-s demand, 8 seeds 0..7, 1800 veh/h and 50% left turns, receiving link 4 cells, lane B preassignment share 0/.5, two phase orders and four exactly defined regimes (never, early 20–35/cycle, late 70–85/cycle, always). Change **only** the upper limit of upstream A→B lane-change zone from 70m to **100m** (floor(100/7)=14 cells). The spatial origins x∈[-14,-11] now contain **four** eligible cells rather than none.

8 seeds × 2 B shares × 4 regimes × 2 phase orders = **128 runs**, with 16 early/late timing comparisons. Compare against all original zone70 pocket70 rows; the `never` regime must remain byte-for-byte identical in motion and objective. Check all 128 conservation constraints, actual trace and no horizontal-plus-lateral move in one tick.

Report actual A→B moves, 16 timing comparisons' strict phase-sign reversals and ties at p=0/60/120, and numbers for the empty/allowed baseline. **Do not** search many change-zone lengths post-hoc to maximize reversals. A longer upstream zone in this 7m-cell model is *not* a field road layout or a guaranteed safe lane-change region.

Source-method inspiration: Hidas (2005) highlights gap acceptance beyond an arbitrary static rule; Huang et al. (2025) shows lane allocation and signal timing can interact. This exploratory repaired geometry tests sensitivity to those established concerns without reproducing their models. K047 remains limited to DLR track evidence; no HTML is used.
