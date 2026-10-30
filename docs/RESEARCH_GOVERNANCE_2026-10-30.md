# R&E 2027 — Research governance (2026-10-30)

## Authoritative locations
- GitHub: source code, test suites, machine-readable configs, small reproducible fixtures, experiment manifests. Treat each result as bound to a commit SHA.
- Shared Drive: Korean research notes, paper review, experiment interpretation, field protocols, submitted reports, and sealed historical artifacts.
- Raw large CSV/PNG: regenerate from tracked code and seeds. Archive on Drive only for irreplaceable observations, publication/submission artifacts, or a deliberately sealed benchmark.
- Archive ZIP on Drive dated 2026-10-28 is **historical only**; it is not the working source checkout.
- Every Docs result must link to repository branch+commit, exact experiment config, result digest if applicable, and a status: PROPOSED / RUN / VERIFIED / REFUTED / RETIRED.
- Do not enable GitHub Actions or bot-authored commits; manual human-authored commits and local test runs only.

## T2 validation gates
1. Verify split topology before/after left-turn pocket entrance; straight vehicles downstream cannot block pocket admission merely through stale FIFO.
2. Prove numerical vehicle conservation, collision exclusion, and deterministic replay for the tested input stream.
3. Coupled same-arrival streams for L=100/200/400/500 ft, across specified fixed seeds; archive per-seed records and confidence intervals instead of relying only on means.
4. Separate monotonicity **inside a specified simulator** from any theorem for physical roads. Search counterexamples by varying demand, lane rules, signal timing, spillback, and merge behavior.
5. Cross-check with an independent simulator such as SUMO before making external validity claims; observational field data are needed for geographic claims.

## Research log cross-references
- Shared Drive root: https://drive.google.com/drive/folders/0AJNkgue2w3zMUk9PVA
- 2026-10-30 notes: https://drive.google.com/drive/folders/1ixaDbDav25T4u0hcqV15P7goZqFAklWt
- 2026-10-28 historical package: https://drive.google.com/file/d/1a2Q-KamhQoWS_GEVRJgMtXgGsUBmSRpf/view
- Earlier research prototype: research/t2-spatial-fig2-v02; PR #1 remains draft until validation.

## What is NOT established
- Real intersection effect sizes, measured flow in Changwon, proof of monotonicity for all admissible road layouts, replication of the source paper's trajectories.
