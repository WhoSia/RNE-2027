# T2-PHYS-02 — 384 actual simulator runs, measured **within the synthetic engine**

**Date 2026-11-21. Status RUN, not field-validated.** The experiment fixed 8 original demand seeds, pocket sizes 14/28/70m, B shares 0/.5, two protected phase orders and the same downstream receiving cells. Four mutually predeclared opportunity regimes were evaluated: never, early 20–35 per cycle, late 70–85 per cycle, and always. Both early and late offer exactly 15 ticks/cycle ×6 cycles = 90 ticks, though a gap being nominally open does NOT imply that a vehicle is positioned and able to change lanes.

## Actual execution and verification
- `384` original-engine executions, `192` corresponding phase-order pairs and `48` early/late same-stream and geometry pairs. No sample exclusions.
- `192/192` never/always control rows agree **exactly** with the original PHYS-01 runs under the corresponding lane-change permission, including terminal outcomes and all motion counters.
- Complete 384-run raw JSON was executed twice from the same source and compared byte-for-byte. SHA-256: `e53db5374467d542a67772a3c161177ba12b12a26e7a25795e765ed3d7828c71`. Raw data retained in the conversation's local downloadable artifact (not represented as deposited in GitHub); all 48 paired numeric comparisons are published in `physical_384_window_contrasts.csv`.
- Both original v2.2 source-level motion-invariant tests and six new time-window tests passed, along with six separate 384-run baseline/contrast tests: **17/17** in the present local run. Original core code SHA matches remote; new `dual_lane_v11.py` instrumented exact Git blob SHA `407f29d75b12d88752e4e212b3512e05bfe7a1c2`.
- PHYS-02 extension script `research/t2/timed_physical_screen.py` was byte-verified to GitHub blob `e0dd9ac66a82caec669b6f480d610ca58c22d9ef`.

## Main result and controls
| Terminal vehicle penalty | Early/late opposite phase preferences /48 | Ties in primary p60 |
|---:|---:|---:|
| 0 | 25 | – |
| 60 (predeclared primary) | 25 | 0 |
| 120 | 24 | – |

Of 48 comparisons, `20` have the same successful total A→B moves summed across the two phase orders for early and late. **Three** of these 20 comparisons also reverse which phase order is optimal, and have >0 actual changes in both schedules. This proves aggregate successful lane-change count is insufficient to reproduce the ranking in this synthetic model. **It does not prove matching individual vehicle motions** (within one pair the two phase orders can allocate changes very differently).

Successful A→B moves counted across all early/late phase-order cases: early **1017**, late **1214**. By pocket: 14m early581/late660, 28m early436/late554, 70m early0/late0. Every 70m scenario has a known geometric degeneracy because the permitted lateral zone stops at 70m exactly at the pocket entrance.

## Important confounding and action semantics
The early and late windows coincide with different parts of the two alternative phase calendars; the resulting ranking reversals encode **opportunity timing × protected phase interaction**, not a standalone delay advantage of earlier/later windows. The artificial windows are exogenous eligibility gates and do not model real speed-dependent safe gap acceptance. Both schedules begin empty at t=0, but policies from t0 diverge, so they do not constitute a t=84 same-prefix microscopic counterfactual.

These results extend the simulator mechanism without confirming empirical causes. The next separate sensitivity tests how 70m pockets behave if a 100m eligible change zone is available, which changes spatial geometry assumptions and must remain labeled exploratory. Real street camera evidence and K047 playback are not involved.
