# P15 independent peer-review mandate — 김세호 / Claude

Date 2026-11-22 KST. **Role: independent falsifier / reproducibility auditor, NOT implementation owner.** Developer and `main` integrator: 김우준 with ChatGPT assistance. Reviewers must be able to say REJECT and must not optimize for agreement with prior assistant claims.

## Mandatory source set (read original content, not summaries alone)

1. [P15 protocol](P15_RF_TO_T2_STATE_INTERFACE_PREREG_20261122.md)
2. [P15 exact math source](p15_rf_decision_sufficiency.py), [19-test suite](test_p15_rf_decision_sufficiency.py), [frozen example JSON](p15_rf_decision_sufficiency_results.json)
3. [P15 findings + exact SHA receipts](P15_1_EXACT_DECISION_SUFFICIENCY_FINDINGS_20261122.md)
4. [Original collaborator's Nov21 independent review](https://docs.google.com/document/d/15CFAM0QsRQkYNGUvf3VEyISxG9Pxyz-I_4WX32CAQp8/edit)
5. [RF apparatus and labels](../../exhibition/rf_curtain/APPARATUS_AND_LABELS.md), [frozen pilot](../../exhibition/rf_curtain/PILOT_PREREG.md)
6. [P13 exact six-count audit](../20261121/decision-time-gate/t2_p13_identification_audit.py)
7. [Nov22 research log](https://docs.google.com/document/d/1Zo0Z-Q50o3f7oLvOF-73vKOCQcDGLq5fynmGaStm0kA/edit) and [GitHub research map](../../../../docs/REPOSITORY_MAP.md).

Use GitHub `main` with a **pinned current HEAD SHA**, not repository's historically different default branch. No GitHub Actions; no bot contributions.

## Top eight adversarial questions

1. Is `intersection argmin` mathematically equivalent to zero finite-set minimax regret? Prove or produce counterexample with ties, >2 actions and varied action availability. Beware silent grouping across different action sets.
2. Does the implemented `cohort` grouping allow manually partitioning contradictory worlds so the result looks sufficient? What must be fixed **before** reading policy costs to avoid cherry-picking?
3. Are `arrival_group` strings evidence of independent arrival histories? They are NOT. Propose a falsifiable seed/tape-fingerprint or provenance test; distinguish a witness *pair* from independent traffic-day replication.
4. Is the named `contract` actually checked against P12 or just a string? Demonstrate how an impossible signal policy could otherwise yield artificial apparent value.
5. Does the `pocket` label in the six toy worlds have physically defensible semantics under `APPARATUS_AND_LABELS.md`? Can an identical label map to opposite policies under a **real T2 PHYS** state rather than assigned toy costs? If not, report the gap, not a proof.
6. Are `epsilon=5`, regret 8 and delta -8/+9 in invented units a meaningful result, or built into the fixture? Is strong sign reversal tested in *an independent prospective* PHYS cohort?
7. Can changes in antenna mounting, metal mass and stationary duration cause `P(CSI features | label, state)` to drift even when labels match? Specify cheap matched optical/magnetic and repeated-session null controls, without collecting real data now.
8. Does the report JSON omit the exact physical proxy state and thereby conceal changed fixtures? Check code, test, output hashes and demand a manifest binding them; identify any other undocumented change.

## Execution / reporting standard

- Clone or otherwise obtain exact `main` bytes; pin HEAD. Run `python -m unittest -v test_p15_rf_decision_sufficiency.py` locally from the 20261122 directory. Report actual pass/fail/error output. Hash relevant files.
- Independently recalculate both regret values (8 vs 9 for the OPPOSITION costs) and a counterexample with a common optimal action despite state aliasing.
- Create at least **three adversarial tests** in an isolated scratch environment, with input and expected answer. Do NOT make unrequested GitHub commits, pushes or merges. You may propose a patch/diff, preserving author attribution.
- Never call your own test run external validity. Separate VERIFIED CODE, PROPOSED PHYS, UNMEASURED CSI, and UNVALIDATED REAL ROAD.
- Document any true error with minimal reproducer, severity, anticipated research-claim impact and the proposed smallest repair. Distinguish design limitations from implementation defects.
- Do not modify sealed K047, open/inspect/move the ~5GB CIM dataset, monitor unrelated RF traffic, use public road equipment or alter live signals.
- If the currently accessible source differs from the stated SHA, STOP, inspect the discrepancy, and report it instead of silently changing the comparison.

## Required deliverable (reviewer-owned)

Add a **new dated appendix** to your own `20261121 김세호의 사유` or a new 20261122 reviewer note, preserving earlier independent notes. Include:
- Verdict: ACCEPT / CONDITIONAL / REJECT for (i) mathematical P15 checker, (ii) PHYS connection, (iii) RF exhibit measurement readiness.
- A claim-by-claim matrix with exact source paths, tested revision, test commands, PASS/FAIL/OPEN.
- Top three high-severity criticisms and at least one legitimate negative/null finding.
- A concrete next decisive experiment, specified inputs, frozen exclusion/holdout, and cheapest competing baseline.
- Four-line handoff: Completed / Next / Blocked / Developer action.

**Role separation:** Reviewer issues adversarial findings and reproduction artifacts; developer decides and carries out `main` changes. No obligation for reviewer to produce lots of commits. This is a collaboration protocol, not permission to alter primary data.
