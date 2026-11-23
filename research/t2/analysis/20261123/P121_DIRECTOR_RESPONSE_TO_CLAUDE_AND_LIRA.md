# P121 — research-director response to Claude independent review (2026-11-23)

**Status:** adversarial adjudication with *new completed* P114, P115, P118 and P120 simulations. External reviewer original was supplied by the user and archived unchanged in the dated T2 Google Drive folder. **No SUMO / real-road validation was performed.** This is a scientific scope correction, not a cosmetic endorsement of an outside review.

## 1. What the reviewer got right — decisive evidence and reproducibility

The review argues that P87's "30 vs 60" claims mix period, relative phase and first 15s vs 30s red, that 4 receiver cells are a selected geometry, that the allegedly independent P100 seed tapes are deterministic in arrival times and differ in movement labels, and that P97's `2/576` should actually be `2/1152` at adjacent policy-arm comparisons. These objections were treated as falsifiable hypotheses.

**P114 prereg** `7acc7d15`, 4 tapes (seeds 86001,86002 × uniform/platoon4, share .75). Exact original P87 engine, all 30 offsets for 30s period and 60 for 60s period, each 50% green, t84 matched pre-split checkpoint, extended horizon 4800, **360 arms all complete**:
- GREEN onset: shorter 30s period improves network vehicle-second cost in **4/4 tapes**.
- RED onset: shorter period worsens cost in **4/4**.
- Equal-weight phase **mean**: 30s improves cost in **4/4**.
- Independent optimized phase **minima**: 60s improves cost in **4/4**.
- Both comparative cost directions are available for **4/4** tapes over the crossed offsets.
- For 86001/uniform: min(30)=6755 at phi=10; min(60)=5149 at phi=42; phase-mean delta=-2119.1167 vehicle-s; selected red-start delta=+845. These two quantities answer different policy estimands. **There is no globally phase-invariant standalone cycle-duration effect.**

**P115 prereg** `0c5b9e93`, 4 tapes × capacities `2,3,4,5,6,8,12,16,64` receiver cells × both period policies, red-start phi30=15/phi60=30. **36 pairs, 72 arms all complete**:
| Receiver cells | paradox n/4 | sum(cost30−cost60) vehicle-s |
|--:|--:|--:|
|2|4/4|+9428|
|3|4/4|+7299|
|4|4/4|+4106|
|5|4/4|+3072|
|6|4/4|+741|
|8|0/4|−1321|
|12|0/4|−1718|
|16|0/4|−2005|
|64|0/4|−6|

**P118 prereg** `23454170`: fix previous deterministic arrival-time problem by drawing sorted random second-arrival times with replacement within [0,239] for uniform family and random arrival seconds within each of four 15s platoon windows. Route labels inherited from 86001/86002, time RNG independently keyed by timing seeds 88001..88008; **32 distinct time vectors verified, 64 matched comparisons, 128 fully cleared T2 arms**:
- C4 denied-down/cost-up **32/32** (cost difference sum +33,009 vehicle-s).
- C8 denied-down/cost-up **1/32** (cost difference sum −8,325 vehicle-s).
- Both preregistered gates pass. This shows the conditional C4→C8 boundary is robust to **new within-240s timestamp patterns in this engine**, not to unrelated road links or different supply/demand regimes.

**P116 exploratory**, no extra simulation, reuse P114 360 scenario arms. Fixed left-phase green-overlap duration in [84,400), predictor sign(cost30−cost60)=sign(overlap60−overlap30): strict correct 6276/7024=**89.35%** (176/7200 abstentions), all-comparisons correct 6276/7200=87.17%. Always-30-better baseline 3854/7200=53.53%. These **7200** crossed offset pairs share only **360 arms across four label tapes**. Do not treat as independent n.

**P120 prereg** `d3e3bd6e`: apply UNCHANGED P116 overlap-sign rule to 4 **previously unseen stochastic timestamp vectors**, timing seeds 88101,88102 × two arrival families, fixed route labels seed 86001. 360 full T2 arms, **7200 crossed offset pairs**, out-of-time-tape holdout performance:
- Accuracy on non-abstention pairs **89.1515%**, coverage **97.5556%**; always-shorter-better baseline over ALL crossed pairs **54.7778%**, so these are different-coverage denominators (no directly precise lift claim).
- Per-tape non-abstention accuracy 0.8878/0.8935/0.8884/0.8964. No parameter fitted to P120. Predeclared gate (>75% strict accuracy and >15 percentage points above all-pair baseline) passes.
- This validates **a predictive calendar signal in T2 under unseen temporal arrival patterns**, NOT a mechanistic sufficiency theorem or an independent computational engine. Error cases remain ~11% and can involve storage, queue order, turn priority and vehicle identity; fit a queue-aware correction only on a new preregistered cohort.

**P97 documented error independently confirmed:** P97_RESULT.json has 192 matched cohort records ×2 policy periods ×3 adjacent loss increments = **1,152** adjacent absolute-cost contrasts, only **2** cost-decreasing adjacent contrasts. The legacy `2/576` denominator is invalid for this unit of analysis. A 576 denominator could refer to some differently aggregated construct; do not silently substitute units.

## 2. Limits, and where we challenge the reviewer

1. Reviewer's full sweep numbers (45.7% 30s worse; 26.7% paradox; 96/96 phase-averaged; 32/32 phase-optimized; 50,623/56,185 left-cost sign predictions, 2/4/8/16/64 with 81/96 to 0/96) were **NOT** independently reproduced at full denominator here. P114/P115 directly reproduce their *qualitative implications on a smaller predeclared cohort*. Avoid citing those large numbers as independently verified.
2. Neither mere cycle period nor overlap seconds alone is universally the "true cause" in a finite, queued, priority-rule system. Offset changes are causal **interventions within the simulator**, but marginalizing over offsets and selecting optimized offsets defines *different estimands*. The review's statement "cycle length is not a cause" is too absolute. Our defensible formulation is **period and offset are joint treatment dimensions, whose effect is conditional on receiver capacity and demand timing**.
3. P100 newly randomized **labels** across seeds and P118 newly randomized **timestamps**. Do not rebrand 64/64 as 64 independent physically sampled arrivals, nor use 7200 crossing pairs as independent statistics.
4. The reviewer read historical GitHub P103 at `2e83ec8`, before later P109 corrections. P103 is retained as an unmodified historical decision record, and the dated README/P109 expressly supersede its incorrect "7-cell pocket" language. The original engine uses 7 **meters = one cell**, four receiver cells. Correct every new summary, keep old exact provenance.
5. P110 block "no SUMO runtime" describes the **research container**, not global impossibility. Installing `eclipse-sumo` in the reviewer's environment may be a valid alternative execution route, but does **not** certify model/route equivalence. P111/P112/P113 provide baseline ID, phase and predecision state exports, but not SUMO output or physical arrival/exit parity.
6. Existing DLR night field data cannot establish this model's downstream end-to-end delay without terminal exits and official head→lane mapping; the present **calculational paper scope** should not spend the primary research budget on repeatedly checking the known incomplete DLR source.

## 3. LIRA: claim-specific retention recommendations (NOT truth probabilities)

| Scoped claim | LIRA | Decision | What would reverse it |
|---|---:|---|---|
| P87 selected-onset comparison identifies cycle period effect independent of relative offset | **0.06** | REJECT | matched offset-conditional causal identification with proper definitions |
| Period×offset joint policy produces strong sign reversals in the original T2 model | **0.98** | KEEP | independent replay breaks P114 full clearing or cost arithmetic |
| Receiver storage 4→8 cells changes red-start paradox frequency in high-left T2 | **0.97** | KEEP | new fully cleared time-randomized T2 contradicts P118, or a source bug |
| Original 64/64 P100 is evidence of diverse stochastic arrival timestamp processes | **0.02** | REJECT | actual per-seed arrival timestamp hash differences (P31 time vectors fixed) |
| P118 tests fresh timestamp perturbations without changing the T2 engine | **0.97** | KEEP | rerun reveals timestamp SHA duplicates or mismatch |
| Calendar left-green overlap is a useful predictive correlate under these two timestamp families in T2 | **0.91** | KEEP | further genuine heldout process shows <75% strict accuracy |
| Calendar left-green overlap alone is a proven sufficient analytic causal mechanism | **0.31** | REJECT | derive theorem with residual queue effect bounds, falsification checks |
| Local receiver/pocket denial metric ranks network vehicle-second policy objective globally | **0.07** | REJECT | must impose and prove missing queue/flow monotonicity hypotheses |
| Original P97 nonmonotonicity result has exactly 576 adjacent policy-arm contrasts | **0.01** | REJECT | change the target comparison unit and recompute the registered dataset |
| Independent geometry-matched SUMO confirms the P120 overlap pattern | **0.00** | REJECT | independently run, pass geometry ID and terminal-event gates |
| Computational/analytic-only T2 manuscript is warranted as a research direction | **0.86** | KEEP (prospective) | prior literature proves no novelty; review after full-text comparisons |

These are editorial ratings of **scoped evidence utility**, not calibrated probabilities, and do not replace the actual comparison counts.

## 4. Research decisions: fewer documents, more falsification

**CHANGE SCIENTIFIC THESIS** to: "In a finite-storage corridor with two movement streams competing for a shared downstream receiver, phase alignment, cycle duration and receiving capacity jointly determine whether reduced local entry denial ranks policies consistently with completed vehicle residence time."

**Next P0:** move beyond an overlap heuristic to a **minimal analytic queue model** with piecewise service windows, queue-stock carryover and finite storage; preregister a falsification set of equal-overlap / opposite-cost scenarios before fitting. A ≥90% predictor learned on same engine, by itself, is insufficient novelty.

**Next P1:** physically separate left/right receiving links in an isolated T2 test branch of the simulation *without expanding Git branches*: legacy regression test must remain byte-equivalent; if paradox collapses, thesis restricts to shared-receiver merges. Observe source semantics carefully, because distinct downstream links with both outputs may alter geometric path identity.

**Next P1:** use existing P111–P113 manifests and P112 event contract to implement genuine SUMO and compare complete per-ID downstream exits. Require matched signal meaning, physics and time origin; engine package installation does not imply equivalence.

**Next P1 literature:** read original full texts on spillback/short links and offset optimization, not just abstracts; report comparative novel element and theorem-level distinction. Avoid citing unsupported references until verified.

**STOP:** adding labels-only seeds, repeating identity verifications as scientific successes, reporting 0.0005 subjective priority differences, treating real-road effect as established, or inflating pairwise offset counts.

## 5. Reproducibility ledger
- P114 prereg `P114_CLAUDE_OFFSET_ADJUDICATION_PREREG.md`; source `p114_offset_adjudication.py`; result `P114_RESULT.json`.
- P115 prereg `P115_RECEIVER_FRONTIER_PREREG.md`; source `p115_receiver_capacity_frontier.py`; result `P115_RESULT.json`.
- P116 exploratory code `p116_phase_overlap_diagnostic.py`; result `P116_RESULT.json`.
- P118 prereg `P118_RANDOM_TIME_HOLDOUT_PREREG.md`; source `p118_temporal_arrival_holdout.py`; result `P118_RESULT.json`.
- P120 prereg `P120_OVERLAP_HOLDOUT_PREREG.md`; source `p120_overlap_temporal_holdout.py`; result `P120_RESULT.json`.
- All work committed to `WhoSia/RNE-2027` **main** as WhoSia with no github-actions[bot]. The external review PDF/MD itself is archived unchanged in the dated Drive folder.
