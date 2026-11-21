# P15 — 김세호/Claude independent critical review: source and handoff receipt

Date: 2026-11-22 KST. Source of external review: [20261121 김세호의 사유](https://docs.google.com/document/d/15CFAM0QsRQkYNGUvf3VEyISxG9Pxyz-I_4WX32CAQp8/edit). Independent reviewer is credited; this receipt is not his code and does not count his unpublished local changes as remote commits.

## Reviewer-reported, not personally replayed
- An authenticated `main` clone and 83 RF-CURTAIN `test_*.py` methods passed for the reviewed source tree. These were mathematical/algorithmic tests, **not real CSI sensing**.
- Reviewer locally authored `literature_arithmetic_audit.py` and `test_literature_arithmetic_audit.py`; 4 tests reportedly passed and local commit `f1e57b0` was created, **NOT pushed to remote main**. Original patch remains in the reviewer's own environment (`/mnt/user-data/outputs` on his instance). Do not appropriate or fabricate its authorship. Obtain the patch through an accessible shared artifact or an authorized teammate push, then check exact bytes and run its tests.
- His follow-up read `APPARATUS_AND_LABELS.md` and `PILOT_PREREG.md` at main `08351ce`; this latest addition supersedes the earlier NOT_DONE item in his note.
- Eight other recently admitted PDFs have not been individually rechecked by the reviewer. His earlier 9-held/3-missing result refers **only to an older 12-item subset**; RF06's *different* latest missing-exact-PDF register tracked 14 candidates. Re-audit before any new global total.
- Stored SUMO output checking is not equivalent to rerunning the SUMO binary. `EFFICIENCY_LOOP.md` documents an initial blocked run and a subsequent performed run; this chronological text alone does not establish independent binary reproduction.

## Independent source checks in this review
**Shahid et al. (2025)** [canonical PDF](https://drive.google.com/file/d/1w2zgRKFFuWl3CsPBec7xHQkqi_7eNIcc/view): original PDF extracted Table I lists 'Leguna' precision .67, recall .57, F1 .24, support 325, and six-class weighted recall .78 with accuracy .79. Elementary independent computation yields `2*.67*.57/(.67+.57) = .6159677419354839`. Under standard nearest-hundredth rounding of P/R, F1 would lie approximately within [0.611,0.621], so the printed .24 cannot be explained by ordinary 2-digit rounding. From six printed supports and recalls, weighted recall = `0.8234402889927751`, not .78. Source inconsistency **verified at extracted-table/arithmetical level**, original computation pipeline and error cause **UNKNOWN**. Do not accuse intent or present 0.616 as an author's corrected measured F1.

**Won et al. (2017), WiTraffic** [canonical PDF](https://drive.google.com/file/d/1hMMeALKst2WyQUGAw0EorCZG6ddSkdK4/view): paper discusses transitory passing-vehicle CSI and 0.05/0.1/0.2/0.3-s test windows. The transition from transient crossing to long stationary occupancy needs an independently designed same-object empty/static/moving experiment, not literature score transfer.

**Main source contracts**: [apparatus labels](../../exhibition/rf_curtain/APPARATUS_AND_LABELS.md) and [pilot preregistration](../../exhibition/rf_curtain/PILOT_PREREG.md) confirm only physical model placement/motion classes, not identified spillback cause, queue length or practical signal benefit.

## Decision gates and authorship
1. ACCEPT collaborator review as an adversarial research input and preserve all negative findings.
2. VERIFY arithmetic ourselves as above; do not extrapolate to real road or assert the author's original metric is .616.
3. HOLD any source-level attribution to unpushed commit `f1e57b0`; original reviewer patch is not in remote `main`.
4. PRIORITIZE decision sufficiency of the five RF classes (P15 interface contract below), static-background/placement controls, and independent RF empirical calibration.
5. Keep PHYS results from uncalibrated simulator, P14 four-tick toy, and actual CSI measurements in separate evidence columns.
6. Avoid GitHub Actions and bot contributions; K047 sealed; ~5GB `CIM dataset.zip` remains untouched.

## Google Docs authority
New Nov22 daily log: [20261122 김우준의 사유](https://docs.google.com/document/d/1Zo0Z-Q50o3f7oLvOF-73vKOCQcDGLq5fynmGaStm0kA/edit); Drive [date folder](https://drive.google.com/drive/folders/1wIlGAxjTuhYW0GNoBrjZV2i4t5yHJ3Xf). Old Nov21 review log preserved unchanged.
