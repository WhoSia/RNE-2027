# T2 v6.10-J / P11-J — research verdict (2026-11-05)

## Question and outcome

Can an OpenDRIVE lane centerline and reference-road join be geometrically plausible while the corresponding **source-declared lane boundaries** fail to match in 3D?

**Yes, for controlled synthetic fixtures.** We constructed 5 source-declared, two-road, one-lane junction scenarios. A nominally matched XY/XYZ connection remains `UNKNOWN`, not `ALLOW`; independent mismatches were identified for a 2 m elevation change, 0.4 rad reference-tangent kink, 1 m lane width discrepancy, and 2 m XY separation. New 3D left/right boundaries are sampled from an existing, restricted OpenDRIVE geometry and cross-section representation.

## Gates and reproducibility

- Code: `src/lane_boundary.py`; experiment: `src/run_boundary_audit.py`; tests: `tests/test_lane_boundary.py`.
- Local tests: 113/113 passed (previous I 99 plus 14 new tests). Separate, unchanged original v6.9-P2 ZIP tests: 28/28 passed.
- All examples are synthetic XML created for this research. Neither imported original real-world `.xodr` nor independent SUMO vehicle simulation were executed. Policy P12 remains frozen.
- Input scope: inherited subset supports planView line/arc/spiral, cubic road elevation, laneOffset, superelevation, width polynomials and declared junction laneLinks. Sampling a single section is not exact road surface triangulation; physical lane heights and `level=true` are unsupported.
- `FAIL` applies to an **explicit geometric assumption** under the recorded candidate seam, not real-world lawful movement or vehicle collision. Travel orientation remains unverified; our fallback chooses one candidate endpoint according to center gap; intersections with nonzero reference-to-reference connecting roads or unusual topology may require different seam evidence.
- Numeric tolerances (edge 0.15 m, width 0.15 m, height 0.12 m, heading 0.08 rad) are **research-only discriminators**, not calibrated roadway safety standards or formal numerical error bounds. Floating point arithmetic and sampled strips do not certify entire continuously varying surfaces.

## Scholarly comparison

Schwab & Kolbe (2022), *Validation of Parametric OpenDRIVE Road Space Models* (canonical Research OS ID `14Nw95goj4fzuuLcAKQVkMC3Ci_Sv308Y`), already extracts explicit lane representations, finds lane geometry gaps and evaluates 99 real OpenDRIVE datasets. Our 3D synthetic seam failures do **not** establish novelty or higher detection performance. A matched dataset and consistent, blinded annotation criteria for false positives/false negatives is necessary before any relative claim. Read alongside Meek & Walton (1992) regarding tangent/curvature constraints and Hasan (2014) regarding why geometry does not certify operating comfort or safety.

## Next gate

1. Original OpenDRIVE scenario file raw-byte custody and real parser execution, with source version/license verified.
2. Derive lane-boundary polygon mesh with continuous arclength and per-lane elevation/shape; test self-intersection and multi-section stitching.
3. Determine road-link and lane-link source endpoint orientations from full predecessor/successor semantics; avoid heuristic candidate endpoint misclassification.
4. Explicit source limit handling and interval-directed numerical bounding; compare Schwab & Kolbe data and external SUMO/OpenDRIVE validators.
5. Keep policy frozen until broader road physics and independent evidence are ready.

## Matched I-versus-J synthetic diagnostic

The identical five fixtures were submitted to the **frozen I predicate** `road_integrity.full_audit` and the new J `audit_boundary_seams` without changing source XML: continuous geometry, 2m XY displacement, 2m vertical displacement, 0.4rad tangent kink, and 1m lane-width mismatch. I reported at least one FAIL in **1/5** (XY displacement); J reported FAIL in **4/5** (all four intentionally defective cases), while both kept the continuous case non-approved/UNKNOWN. This is a purpose-designed counterexample set, **not measured real-world sensitivity/specificity**, and the changed failure criteria make it an ablation diagnostic rather than a validated performance benchmark. The full side-by-side machine-readable results are in `results/boundary_audit.json`.
