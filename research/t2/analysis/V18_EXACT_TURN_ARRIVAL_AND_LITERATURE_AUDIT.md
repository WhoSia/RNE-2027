# T2 v1.8 — Fixed arrival demand inventories, timing interactions and literature audit

**Date**: 2026-10-31  
**Branch**: `research/t2-spatial-fig2-v02`  
**Run status**: LOCAL synthetic execution; NO field data; NO GitHub Actions.

## Research question

At a fixed total demand, does left-turn/through *arrival order* alter pocket benefit,
and can the conclusion survive the stronger test where every signal cycle also
contains exactly the same numbers of left and straight vehicles?

This distinction repairs an explicit v1.7 confound: changing a stochastic
left-turn share profile can slightly alter realized total left-turn vehicles,
so it is not a pure timing-only intervention.

## v1.8A global inventory court — 864 synthetic runs

12 seeds × 2 upstream platoon offsets × 4 route-label time patterns ×
3 physical pocket lengths × 3 downstream signal offsets = **864** simulations.

The generated arrival timestamps and complete-horizon left/straight
vehicle inventories are preserved exactly for a given seed/arrival offset.
The ordering of left/straight labels is manipulated, including deliberately
extreme early/late concentration conditions used as negative controls.

Under a 720s horizon, left-leading protected phase, upstream arrival offset
0s, downstream signal offset 0s, 14m→70m total-network completion gains:
- randomized routes: 158.833 − 127.750 = **+31.083** vehicles;
- all left vehicles at the start of the horizon: **+0**;
- all left vehicles at the end of the horizon: **+0**;
- evenly distributed left turns: 161.000 − 125.083 = **+35.917**.

The two zero cases are intentionally unrealistic route blocks. In the
late-L case, the model discharged no left-turn vehicles over the observation
horizon, so the zero does NOT establish that bay length is unimportant.

## v1.8B exact *within-cycle* inventory court — 384 synthetic runs

8 seeds × 4 within-cycle route-order patterns (random/left-first/left-last/
evenly dispersed) × 2 left-signal sequences (leading/lagging) ×
2 receiving-signal offsets (0s/30s) × 3 physical pockets (14/28/70m)
= **384** new runs.

**Both the vehicle timestamp list and every 120-second signal cycle's
L/S vehicle counts are identical across all four timing patterns.**
This is the stronger counterfactual test; the only modified variable
within a matched scenario is route-label order.

Downstream offset 0s, 720s, 8 paired seeds:
| Within-cycle L order | Leading: benefit 70−14m | Lagging: benefit 70−14m |
|---|---:|---:|
| Random | +28.500 | +37.250 |
| Left first | +19.625 | +21.250 |
| Left last | +13.875 | +19.625 |
| Evenly dispersed | +33.000 | +39.375 |

For the left-leading/random case the marginal benefits are +16.875
(14→28m) and +11.625 (28→70m). By comparison, left-leading/L-last
has +4.375 (14→28m) and +9.500 (28→70m).

The model's lane preassignment and lack of explicit physical overtaking
strongly affect these patterns; this study reveals model sensitivity,
**not** observed traffic optimization. The simulation has one receiving
lane and omits downstream route-specific receiving groups.

## Tests / artifacts / parity

Four new exact-inventory regression tests and three new cycle-inventory
tests passed. Counting selected inherited suites, **44/44 selected
local tests PASS**. This is NOT a full re-run of all historic v1.0–v1.7 tests.

The local archive `T2_v18_exact_turns_repro.zip` has 18 files:
two executed scripts, analysis, unit tests, supporting v1.7 source,
1,248 raw case rows, scenario means, paired contrasts, plot, test log,
manifest. ZIP CRC PASS. SHA256
`bc2962c775d0960ccecf748fcc42559224ee28873ded034e461edd2895ea626f`.

GitHub source was written through authenticated connector, while simulations
ran in the local reconstructed source tree. **Exact GitHub HEAD byte
parity and full exact-source execution remain UNVERIFIED.**
No GitHub Actions, workflow edits, or main merge.

## Literature and inventory correction

Held in Google Drive by exact document title:
- Daganzo (1994), *The Cell Transmission Model: Network Traffic*
  (working paper, not single-link journal article).
- Yang et al. (2022), *Characterizing the dynamics and uncertainty of
  queues at signalized intersections with left-turn bay*.
- Zhang & Tong (2008), Liu et al. (2019), Wei et al. (2021),
  Li & Elefteriadou (2013), Reynolds et al. (2011), Qi et al. (2020),
  and Wu et al. (2024), among other existing holdings.

Not located in targeted connected Google Drive title/author searches
(NOT proof of absence from every local Research OS shelf):
1. Liu & Chang (2011), *An arterial signal optimization model for
   intersections experiencing queue spillback and lane blockage*,
   DOI 10.1016/j.trc.2010.04.005.
2. Yin, Zhang & Wang (2011), *Modeling Delay during Heavy Traffic for
   Signalized Intersections with Short Left-Turn Bays*,
   DOI 10.3141/2257-12.
3. Pang, Ye & Pei (2016), *Influence of bus stop with left-turn lines
   between two adjacent signalized intersections*,
   DOI 10.1088/1674-1056/25/8/088901.
4. Daganzo (1994), *The cell transmission model: A dynamic representation
   of highway traffic consistent with the hydrodynamic theory*,
   DOI 10.1016/0191-2615(94)90002-7 (different from the HELD network report).
5. Wang et al. (2022), *Traffic Queue Length Estimation at Permissive
   Left-Turn Signalized Intersections with Probabilistic Priority*,
   DOI 10.1061/JTEPBS.0000764.

**Research scope**: the papers above were confirmed on publisher, academic,
or author publication pages; their *titles and abstracts* were used where
available. Do not assert that unheld full papers were fully read.
