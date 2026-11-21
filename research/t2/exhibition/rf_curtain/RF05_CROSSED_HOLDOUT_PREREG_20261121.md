# RF05 — Crossed session × placement RF pilot diagnostic (preregistered before code)

2026-11-21. **DESIGN/FROZEN TEST SPEC; NO WIFI CSI SAMPLES COLLECTED.**

Motivation: existing `rf_pilot_evaluator.py` trains on P1,S1/S2 and checks only P2,S3. That conflates a **new session** with a **new antenna placement**; the source papers Brunello et al. (2025, temporal CSI generalization) and Guarino et al. (2026, RF reproducibility), both HELD in Research OS 10_PAPERS, motivate a crossed design. This is about evaluation attribution, not improving apparent accuracy.

### Prescribed 3 × 2 × 5 × 10 independently reset trial grid (300 trials)
The five class labels are `no_demand,free,pocket,downstream,both`; each cell must have >=10 independently reset trials for each class. Keep `trial_origin`, manually assigned independent truth labels, missing records and all six distinct session-by-placement cells. Do not split CSI *packets* from the same reset between train and test.

| Partition | Session | Placement | Relative shift versus fitted observations | Use |
|---|---|---|---|---|
| Training | S1 | P1 | Original baseline | 50 labeled trials |
| Training | S2 | P1 | Additional training-day variability in *same* placement | 50 labeled trials |
| Diagnostic TEST | S2 | P2 | **placement-only conditional on S2 represented in training** | 50, locked |
| Diagnostic TEST | S3 | P1 | **new-session-only relative to P1 training** | 50, locked |
| PRIMARY TEST | S3 | P2 | **joint new-session × new-placement** | 50, locked |
| Unused frozen reserve | S1 | P2 | Not consumed by current locked evaluator | 50, preserve |

Importantly "placement-only" is conditional on training seeing S2 P1 samples; this is **not an individual physical causal intervention effect** or a replicated between-day comparison. With just 3 sessions, the measured F1 uncertainty may be very large and no strong population generalization conclusion follows.

### Locked evaluation criteria
- Reuse exact `MODELS`, `LABELS`, `validate`, `fit_predict` and `summarize` from the original RF pilot evaluator; **fit standardization/class centroids ONLY on P1,S1 and P1,S2**.
- All three test groups must each contain every class with >=10 independently reset records; never use P2,S2 for threshold/model tuning even though S2 P1 is in training.
- Report for each group: 5x(5+abstain) confusion, macro-F1, balanced accuracy, class recall, missing/abstention rate and all model predictors. Preserve missing in denominator.
- Do not average over conditions until separate placement-only, session-only and joint failures are shown.
- Existing Stage-C threshold (CSI macro-F1 >=.70; minimum recall >=.50; CSI F1 improvement >=.10 over best RSSI, >=80% per-test-cell valid rate) is applied to the **joint S3,P2 primary** only, separately report other two as diagnostics. The old global min-session >=80% remains a guard. These thresholds are provisional, not formal p-value proof.
- `synthetic_test_fixture` MUST always return `NOT_APPLICABLE_SYNTHETIC_FIXTURE`, even with artificially perfect F1. Mixed provenances rejected; any real measurement must be independently source audited.
- Missing or nonfinite telemetry should never silently become a high-confidence class label.
- If all three group performances are exactly equal, report equality; not evidence of hardware independence.
- No part of this design warrants mounting hardware on a road or changing real signal control.

### Frozen test fixture plan (not empirical evidence)
- 300 artificial rows: exact 3 sessions ×2 placements×5 labels×10 resets, class-encoded CSI in two dimensions, RSSI noninformative.
- One missing CSI test in the joint cell should raise the CSI abstention denominator to 1/50, without reassigning its class.
- Remove all examples of a single label from one diagnostic cell: fail early, do not redefine the split.
- Alter the held-out placement P2 CSI by a large additive value: expect a diagnostic performance drop **without retraining**; do not assume any particular real physical phenomenon.
- Remove unused P2,S1 rows: fail if contract requires complete grid.
- Check train source groups and exclusive split membership and status flag.

### Gates and interpretation
Primary scientific outcome now is a **sound analysis plan and tested leakage control**, not a measured RF result. Do not generate fake CSI packets or infer road effectiveness. Keep K047 sealed and do not use GitHub Actions.
