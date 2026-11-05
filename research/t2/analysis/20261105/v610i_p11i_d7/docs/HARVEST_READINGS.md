# D7 Literature Harvest — 2026-11-05

## Provenance and custody
- `00_INTAKE — Literature Radar` folder ID `1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16` contained eight newly added source PDFs.
- All eight were individually inspected using their actual Google Drive PDF text (title/author, abstract, selected technical/conclusion sections). All eight were renamed **metadata-only** and moved into `10_PAPERS — Canonical Literature Commons` folder `1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP` with the **same Drive file IDs**. We did not regenerate or alter their raw PDFs. Do not equate file-ID stability with post-move byte-level SHA256 proof: raw byte hashes were not obtained in this run.
- Other files in `00_INTAKE` not part of this eight-paper cohort were deliberately left unchanged; some have unresolved bibliographic/duplicate provenance.

## Newly promoted papers, read directly from PDF text
| Official author/year/title | ID | Reading-derived findings | Research use/limitation |
|---|---|---|---|
| Schwab & Kolbe (2022), *Validation of Parametric OpenDRIVE Road Space Models* | `14Nw95goj4fzuuLcAKQVkMC3Ci_Sv308Y` | Derives explicit lane geometries for continuity, topology and semantic validation; assesses 99 OpenDRIVE datasets, identifies substantial lane gaps in about 20%; employs CityGML inspection. | Our new interval-width + link-gap tests overlap known framework. Novelty needs quantified delta, e.g., rigorous bounded polynomial extrema, unknown/legal distinction, counterexample detection, independent source comparisons. |
| Vázquez-Méndez & Casal (2016), *Clothoid Computation: A Simple and Efficient Numerical Algorithm* | `122n7GV-E7o5skZm3qlIfLP_gTLOhalr_` | Compares classical sine/cosine Taylor-based formulas with initial-value-problem numerical computation; discusses Runge–Kutta and three horizontal road alignment cases. | Benchmark against a reference IVP/series implementation rather than only SciPy `quad`; do not conflate 2D mathematical precision with geometry validity. |
| Vázquez-Méndez, Casal & Ferreiro (2020), *Numerical Computation of Egg and Double-Egg Curves with Clothoids* | `1g3ebS6HmVArfUOh1u8PaP76oyRTicLoi` | Models clothoid as constant curvature-change rate with nonzero initial curvature, connects oriented circular boundaries and discusses egg/double-egg road interchange shapes. | Add signed initial curvature, boundary orientation and multi-segment continuity counterexamples; route generation not yet implemented. |
| Hasan (2014), *Spiral Length Design* | `1VknKRfmfzkzOKA04n_n7A6dcJc68ISaS` | Critiques usual independent spiral length formulas and relates jerk, unbalanced and actual superelevation runoff, cant gradient and twist to vehicle comfort. | Our coordinate roll is NOT an engineering safety/comfort criterion. Future audits must accept speed, jerk and actual cross-slope boundary conditions. |
| Frego (2022), *Closed Form Parametrisation of 3D Clothoids by Arclength with Both Linear Varying Curvature and Torsion* | `17Uls-jKN1oNxgshFIPn117vfEkZAD55L` | Studies affine curvature and torsion using linear time-varying frame systems, closed Fresnel cases and 4th-order Magnus/commutator-free geometric integrators. | Our 2D spiral + road elevation + roll is not a 3D clothoid, which requires an actual 3D unit-speed curve and torsion model. |
| Lucas & Ortega-Yagües (2026), *A Geometric Property Characterizing the 3D-Generalized Clothoids* | `1hU8v4dGpsdBZkJCY7CWbJx5RX1qqJEf9` | Characterizes 3D generalized clothoids via ratio torsion/curvature and geometric Darboux line condition; links 3D and spherical clothoids. | Theoretical source for longer-term 3D trajectory research, not a direct OpenDRIVE parser acceptance rule. |
| Ionut (2026), *Explicit Cartesian Coordinates for Three-Dimensional Clothoids*, preprint arXiv:2608.28636v1 | `1YPrsgfAbwS0p_WmggWUvk4CrrLwJMx1E` | Proposes explicit Cartesian arc-length coordinates for nonhelical 3D clothoids through spherical reconstruction and Kampé de Fériet functions. | Preprint, not independent experimental evidence. Potential analytical comparator only after verifying formulas and conditions. |
| Meek & Walton (1992), *Clothoid Spline Transition Spirals* | `1WQMtORyBHo7-_ECRKX2UkmTb18OwXZME` | Discusses G2 planar curves joining two points with assigned tangents/curvatures, gives existence/uniqueness conditions and algorithms for transition spirals. | Strong constraint-aware reference for connected road segments: position, heading, curvature continuity must be distinguished. |

## Distinction between sources, code, and inference
- **PDF-derived:** the methods and claims in the middle column.
- **This study's implementation:** a new source-declared width polynomial interval audit and a limited explicit `laneLink` geometric-gap check, tested on synthetic XML.
- **Hypotheses, not proven:** the new audit will be measurably stronger than Schwab & Kolbe; current study has not reproduced their 99-dataset experiment or quantified comparative detection rates.

## D7 outstanding acquisition
- No source-PDF acquisition required for the eight above: present in canonical `10_PAPERS`.
- Pending: original byte-faithful, appropriately licensed external XODR datasets; independent OpenDRIVE parser and signal/road regulation data. External `.xodr` original run NOT done.
- Paper storage must not be duplicated into T2 daily folders; link to canonical IDs instead.
