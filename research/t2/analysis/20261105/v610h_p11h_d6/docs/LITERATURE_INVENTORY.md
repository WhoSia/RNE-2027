# D6 Literature gap audit — 2026-11-05

Sources searched: Google Drive metadata across accessible files (PDFs) using title and author queries. A negative title search is **not** a definitive absence proof for unindexed/renamed PDFs. No missing paper has been downloaded or claimed to be owned. Separate peer-reviewed publications from official standards.

## Confirmed as existing Drive PDFs (DO NOT classify missing)

1. Kesting, Treiber & Helbing (2007), General Lane-Changing Model MOBIL, Drive file `10GL2nJFgmvDfFOTo4IiNxSB6RYOIKu00`.
2. National Academies (2015), Signal Timing Manual 2nd Edition, Drive `1ZoL5zLQthqOqbEjDFulaDcCfGp_RQGoG`.
3. Harth, Langer & Bogenberger (2022), Automated Calibration of Traffic Demand and Traffic Lights in SUMO Using Real-World Observations, Drive `1_kMBvodn3843e1Xr7Wk-y_y7MDKqc8DT`.
4. Treiber & Kesting (2013), Microscopic Calibration and Validation of Car-Following Models, Drive `1wkAtAR0uhfSLWCVjGUqDOYHGk60FbJQt`.
5. Liu & Chang (2011), Lane Blockage and Spillback Arterial Optimization, Drive `1HR0BJCclEIb4eXZTALsbZFgXgaA-Cqcz`.
6. Ali, Zheng & Bliemer (2023), Calibrating Lane-Changing Models, Drive `1Ow2jv3VtvDdsm0BQL27ftEBh7Eeq_409`.

## Drive PDF NOT FOUND by exact title/author query — high priority to obtain

1. **B. Schwab & T. H. Kolbe (2022)**, *Validation of Parametric OpenDRIVE Road Space Models*, ISPRS Annals X-4/W2-2022, 257–264, DOI `10.5194/isprs-annals-X-4-W2-2022-257-2022`; open access article: https://isprs-annals.copernicus.org/articles/X-4-W2-2022/257/2022/ . Key: 99 independent real OpenDRIVE datasets and lane continuity validation; overlap with our continuity gate demands a direct novelty comparison.
2. **M. E. Vázquez-Méndez & G. Casal (2016)**, *The Clothoid Computation: A Simple and Efficient Numerical Algorithm*, Journal of Surveying Engineering 142(3), DOI `10.1061/(ASCE)SU.1943-5428.0000177` https://ascelibrary.com/doi/10.1061/%28ASCE%29SU.1943-5428.0000177 . Key: alternative Taylor/ODE methods for Euler spiral numerical accuracy.
3. **N. Hasan (2014)**, *Spiral Length Design*, Journal of Transportation Engineering 140(5), DOI `10.1061/(ASCE)TE.1943-5436.0000651` https://ascelibrary.org/doi/abs/10.1061/%28ASCE%29TE.1943-5436.0000651 . Key: curve length, superelevation and design comfort; not equivalent to validating our planar reference line.
4. **M. E. Vázquez-Méndez, G. Casal & J. B. Ferreiro (2020)**, *Numerical Computation of Egg and Double-Egg Curves with Clothoids*, Journal of Surveying Engineering 146(1), DOI `10.1061/(ASCE)SU.1943-5428.0000299` https://ascelibrary.com/doi/10.1061/%28ASCE%29SU.1943-5428.0000299 . Key: complex transition-curve construction and initial value methods.
5. **Closed form parametrisation of 3D clothoids by arclength with both linear varying curvature and torsion (2022)**, Applied Mathematics and Computation 421, 126907, DOI `10.1016/j.amc.2021.126907`, https://www.sciencedirect.com/science/article/pii/S0096300321009905 . Key: 3D curvature/torsion; a future extension; not currently used.

## Technical references (standards, NOT academic papers)

- ASAM OpenDRIVE 1.8.1: https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.8.1/specification/09_geometries/09_04_spiral.html
- Lane offset: https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/v1.8.1/specification/11_lanes/11_04_lane_offset.html
- Superelevation: https://simulation.pages.asam.net/opendrive-group/opendrive-antora-gen/ASAM_OpenDRIVE_Specification/v1.8.1/specification/10_roads/10_05_elevation.html

## Acquisition rule

Prefer official open-access PDF of Schwab/Kolbe first; others rights may limit access. Do not create empty placeholder PDFs or infer original-byte custody from a webpage. Place acquired PDFs in canonical Research OS 00_INTAKE -> verify hash/LICENSE -> promote to 10_PAPERS. Existing verified six papers should not be fetched again.
