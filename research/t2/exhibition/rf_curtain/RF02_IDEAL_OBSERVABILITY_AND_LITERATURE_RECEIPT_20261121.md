# RF02 — Ideal observation identifiability, source-integration receipt
2026-11-21 · R&E 2027 T2 · RF-CURTAIN exhibition parallel research
**CLASSIFICATION: ANALYTIC_IDEAL_OCCUPANCY_ONLY_NOT_MEASURED_RF**

## What was implemented

The five **user-defined toy** physical conditions in RF01 are represented
by exact three-bit symbolic states, not radio signals:

| Toy label | Pocket occupancy P | Downstream occupancy D | Approach demand A |
|---|---:|---:|---:|
| no_demand | 0 | 0 | 0 |
| free | 0 | 0 | 1 |
| pocket | 1 | 0 | 1 |
| downstream | 0 | 1 | 1 |
| both | 1 | 1 | 1 |

For a chosen ideal sensor subset, the program enumerates all five
possible worlds, builds signatures, counts states that can be
identified without guessing, and treats a missing bit (`None`) as
uninformative and a contradictory observation as outside this small
declared model.

**Exact computed enumeration:**

| Ideal sensors | Signatures | Individually uniquely identifiable labels / 5 |
|---|---:|---:|
| none | 1 | 0 |
| P | 2 | 0 |
| D | 2 | 0 |
| A | 2 | 1 |
| P,D | 4 | 3 |
| P,A | 3 | 1 |
| D,A | 3 | 1 |
| P,D,A | 5 | 5 |

For P,D alone, `no_demand` and `free` are indistinguishable,
both having (0,0). Under these *ideal instantaneous static occupancy*
assumptions, a separate demand bit separates the classes.

**NOT inferred:** a real extra sensor is required. Real CSI may
contain movement information over a time window and change the
observation function; first-Fresnel zones and measured multipath
also invalidate the 'perfect binary sensor' assumption. Moreover
mere pocket/downstream occupancy is not equivalent to physically
*causing* traffic discharge blockage. Wu et al. (2024) categorize
10 different turning/through spillback cases and distinguish
spillback vs blocking; this five-label model is NOT their algorithm.

## Why this is relevant to source papers

- Wu, Yao, Cao & Tang (2024), Table 1, DOI
  10.1080/21680566.2024.2363273; Drive full original
  https://drive.google.com/file/d/155MVLQ8tpc1AhK5mo03Rz2w5MHBQUJ_r/view
- Qi, Dai, Tang & Hu (2020), DOI 10.1016/j.trc.2020.102824;
  true spillover triggering movement requires trajectory/direction,
  not just two occupancy bits:
  https://drive.google.com/file/d/110GFwIyMMN1cJc_iyeTMVeZCVFRYTVmP/view
- WiTraffic/DeepWiTraffic prior CSI classification:
  https://doi.org/10.1109/ICCCN.2017.8038380 and
  https://doi.org/10.1109/MASS.2019.00062
- This module's claim is a modest formal analysis of **our**
  chosen label/observation ontology and is explicitly not new
  empirically confirmed Wi-Fi sensing or a replication of Wu/Qi.

## Local real execution and blob identity

- Python 3.13, `python -m unittest -v test_rf_observation_identifiability`
- Exactly 9 test methods all PASSED, including all five worlds
  across all sensor subsets, incomplete/contradictory reports,
  monotonic refinement, and never treating 1 as Boolean True.
- Main source `rf_observation_identifiability.py`
  local `git hash-object` and GitHub main blob both
  `694913f4a00783214379be51464bce2f022775e4`.
- Test `test_rf_observation_identifiability.py`
  local `git hash-object` and GitHub main blob both
  `101a213915b8cbd3dffa13246435ecd2722d3b50`.
- Output exact JSON from the local source
  SHA-256 `bbdf15578bd46dd13029528ca294469001c5f3cd1d9b111841845d06e13cfd77`.
- No full repo integration suite was run in this unit; no actual
  RF recordings or real-world traffic observations were used.

## Gate before any prototype physical claim

1. Read full CSI prior-method originals, not only abstracts;
   check exact hardware/packet interfaces and licensing.
2. Measure static + moving class separation under school-authorized
   indoor conditions, with independent camera/manual truth;
   use no unrelated Wi-Fi traffic or person tracking.
3. Distinguish stable occupancy, demand, motion crossing and
   true blockage from mere signal disturbance and RF link failure.
4. Keep cross-placement and session holdout frozen before inspecting.
5. Only with measured error rates can information value be evaluated
   in the separate T2 traffic action/regret framework.

**No hardware purchased, no public-road installation, no signal
controller touched, no GitHub Actions or bot contributor, K047 sealed.**
