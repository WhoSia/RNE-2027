# 2026-11-22 — T2 branch consolidation evidence and safe deletion gate

## Audited repository and exact refs
Repository: WhoSia/RNE-2027.
GitHub `compare_commits(base=main,head=research/t2-spatial-fig2-v02)`:
- status `behind`; ahead_by **0**; behind_by **336**; file differences **0**.
- merge base and T2 branch head `0c6bc9e2052e2cd8f699c84ee8d388a03cb5bf37`.
- Audited `main` SHA at comparison `3b4552b3d03ce2cba68c0d5f0663704a1415af46`.
Reverse comparison: `research/t2-spatial-fig2-v02...main` status `ahead`, ahead_by **336**, behind_by **0**, **223** file diffs. This is a **strict ancestor** relationship; the old branch has **zero unique commits**, so there is no integration work to cherry-pick, merge or squash.

## Decision
Keep `main` as sole canonical development branch; retire `research/t2-spatial-fig2-v02`. Do **not** rewrite `main`, force-push, or rebase. The GitHub connector available in this session has no `delete_branch`/`delete_ref` operation; do **not** substitute `update_ref` (moving a branch is not deletion). Actual remote deletion remains **NOT EXECUTED** until deletion via GitHub Branches UI or trusted CLI, followed by remote recheck.

### One-step human deletion
Open `https://github.com/WhoSia/RNE-2027/branches`, find `research/t2-spatial-fig2-v02`, delete that branch, retaining main. Do not delete main. Confirm branch list shows only main; if the branch has an open PR/protection, inspect it before removal. GitHub commits remain in main's history.

## Research development and provenance constraints
- Keep all P19–P31 immutable evidence and SHA source history in main and Drive; commit small logical research units directly to main, without Github-Actions[bot] writes or workflows.
- Do not claim branch deleted just because ancestry check passed.
- Every new claim: causal predecision equality (or explicit not), unique arrival-tape count, event-ID validity, external transfer limits, severity and exact source hashes.
- Avoid commingling field observations with simulated outcomes. T2 has **no live traffic controller** and the synthetic stage `-` is not physically cleared yellow/red/pedestrian phases.
