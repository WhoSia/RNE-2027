# P11-H / D6 verdict — GO for limited 3D geometry; NO-GO for full OpenDRIVE or policy

**Date** 2026-11-05. Earlier P2~P11-G original files are immutable. This artifact is an independent derived snapshot.

**Implemented**: OpenDRIVE `<spiral curvStart curvEnd>` heading and XY Simpson quadrature with independent adaptive quadrature and Fresnel tests; `laneOffset`, `superelevation`, and conditional lane-center coordinates. Existing G tests were adapted in exactly 2 places that previously asserted spiral unsupported. Additional H tests include numerical integration stress across 80 explicit parameter combinations. The representation does not support lane height, lane level=true, arbitrary road shapes, paramPoly3 or Road CRG; no real-world position guarantee.

**Policy idea only**: `policy_idea/variable_contract.py` defines future variable names and information-dependence metadata. It does not implement optimization, a deployable controller or a phase schedule; previous P12-A/B frozen.

**Evidence**: controlled synthetic XML, 88 local tests, independent SciPy quadrature; the Esmini original `.xodr` is NOT present locally, so external real `.xodr` parse remains NO-GO. Need literal original bytes for byte identity and separate license validation.

**Critical scientific overlap**: Schwab & Kolbe (2022) already validates parametric OpenDRIVE topology across 99 datasets, so continuity testing alone is NOT novel. Any research claim must compare error detection, edge cases, solver accuracy, safety boundaries and empirical failures to that work. Missing PDF list is only Drive metadata-negative, not certifiably absent.

**Next tests**: polygonal lane footprint and width extrema over intervals (not just sample points); nonzero slope road frame with roll; sample limits under high curvature; `paramPoly3` and exact `pRange`; external independent parser; real world regression; multi-level `laneLink` direction; OSM via-way relation.
