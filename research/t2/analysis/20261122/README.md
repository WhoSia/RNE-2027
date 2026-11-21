# T2 Research — 2026-11-22

**Ownership:** development, tests, research log and `main` integration by 김우준 (ChatGPT-assisted). Independent adversarial peer review by 김세호/Claude. Peer review findings do not automatically authorize or replace code changes.

## P15 — coarse RF labels vs T2 policy-relevant state

- [Prior formal interface contract](P15_RF_TO_T2_STATE_INTERFACE_PREREG_20261122.md)
- [Independent critique receipt](P15_COLLABORATOR_CLAUDE_AUDIT_RECEIPT_20261122.md)
- [Exact synthetic decision-sufficiency auditor](p15_rf_decision_sufficiency.py)
- [19 local tests](test_p15_rf_decision_sufficiency.py)
- [Deterministic machine-readable result](p15_rf_decision_sufficiency_results.json)
- [Results and exact SHA/blobs](P15_1_EXACT_DECISION_SUFFICIENCY_FINDINGS_20261122.md)
- [Independent reviewer mandate](P15_INDEPENDENT_PEER_REVIEW_MANDATE_20261122.md)
- [Daily Google Doc](https://docs.google.com/document/d/1Zo0Z-Q50o3f7oLvOF-73vKOCQcDGLq5fynmGaStm0kA/edit)

To reproduce locally without any repository automation:

```sh
cd research/t2/analysis/20261122
python -m unittest -v test_p15_rf_decision_sufficiency.py
python p15_rf_decision_sufficiency.py > /tmp/p15_result.json
```

The locally executed final source and tests match the GitHub `main` Git blob IDs in [findings](P15_1_EXACT_DECISION_SUFFICIENCY_FINDINGS_20261122.md); 19/19 pass. Three toy cohorts demonstrate (i) an **invented** strict opposite-policy pair under identical staged label, (ii) a common optimal action despite non-injective label, and (iii) an exact tie/common action. The artificial cost matrix was chosen by the developer to exercise the logic: **no new PHYS model, radio signal, policy deployment or empirical traffic observation**.

Review priorities: maliciously chosen cohort boundaries; unverified independent arrival groups; action contracts represented by strings instead of validated P12 feasibility; physically staged occupancy labels not guaranteed to map to real T2 state; within-class RF emission drift; complete compatibility-set sampling. Do not promote artificial fixtures to field results.

Working branch `main`; no GitHub Actions, K047 seal preserved, ~5GB CIM dataset remains untouched.


## P16 — Genuine PHYS checkpoint schema, NOT a five-class RF diagnosis

- [Source-derived checkpoint-to-proxy adapter](t2_p16_checkpoint_contract.py)
- [20 targeted schema/alias regression tests](test_t2_p16_checkpoint_contract.py)
- [What was read from the canonical core and what remains UNIDENTIFIABLE](P16_CHECKPOINT_INTERFACE_FINDINGS_20261122.md)

```sh
cd research/t2/analysis/20261122
python -m unittest -v test_t2_p16_checkpoint_contract.py
```

**20/20 local tests passed** with exact-byte GitHub blob-matched code/test source after final line-break reconciliation. The adapter uses the exact fields of `dual_lane_v11.checkpoint_observation` and the PHYS-04 row schema, but no complete PHYS-04 empirical/synthetic result JSON was run or audited during this unit. `rf_five_class_label=None` is intentional: neither a static obstruction nor a causal queue diagnosis is identifiable from a single time-slice count alone. A fake opposite-delta test is only a regression test, not a discovered PHYS witness.


## P17 — Authentic historical PHYS-04 archive, re-downloaded and audited

- [P17 archived 144-policy-pair findings](P17_HISTORICAL_PHYS04_EXACT_ARCHIVE_FINDINGS_20261122.md)
- [ZIP-SHA-pinned read-only auditor](p17_zip_audit.py)
- [9 focused tests including exact historic ZIP](test_p17_zip_audit.py)
- [Compact structured result](P17_PHYS04_VERIFIED_ARCHIVE_SUMMARY_20261122.json)
- Original [Nov21 PHYS04/05/05b/06 Drive ZIP](https://drive.google.com/file/d/1nIHmzoz0Yk3YUqaaxvbBWH7ztgR2ddo-/view) — now actually downloaded and SHA-256 verified; this **does not** repair its internal reconstructed-engine provenance.

**New P17 decision:** 144 stored pair rows, 133 strict matching groups, 11 count-collision groups, just one weak opposite-sign witness (−305 versus +1), **zero robust opposite-sign witness at epsilon=5**, and zero opposite signs after matching full occupied-cell positions. Deliberately dropping B-share from the key produces 2 **invalid** large opposite-sign artifacts; both compare different lane allocations at the same seed.

Run with a local copy of the *specific* existing 52,090-byte Drive ZIP:

```sh
python p17_zip_audit.py /path/to/T2_PHYS04_05_05b_06_20261121_Research_Bundle.zip p17_full_audit.json
P17_HISTORICAL_ZIP=/path/to/T2_PHYS04_05_05b_06_20261121_Research_Bundle.zip python -m unittest -v test_p17_zip_audit.py
```

**9/9 local tests passed**, the actual historical results were opened in this run, source/test Git blobs match committed `main`, and full audit output has a recorded SHA. This is a genuine analysis of earlier model-output bytes, *not* a fresh execution of the T2 physical engine or field observation. The 5GB held CIM dataset was untouched.
