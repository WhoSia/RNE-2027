# T2 v2.0 — Protected/Permissive Gap Supply and Finite-Horizon Court
Date: 2026-10-31. Branch: research/t2-spatial-fig2-v02.

## Research intent
Prior v1.9 had movement-specific receiving inventories, but no opposing
through-traffic gap conditions for permissive left turns. v2.0 introduces a
small, separate *conceptual queue simulator* to evaluate the sensitivity to
turning phase mode and opposing flow; this does NOT modify the physical
dual_lane_v11.py upstream pocket simulator.

## 1,728 synthetic runs (local execution)
**1,296 factor cases:** 12 common seeds × 3 policies (protected,
permissive, protected_permissive) × opposing demand 0/400/1000 veh/h ×
left bay storage 2/4/8 vehicles × independent/shared receiving buffer ×
downstream signal offset 0/30s. 720s horizon, nominal 1500 veh/h
total arrivals, 30% left.

**432 horizon/initial-queue cases:** 8 seeds × 360/720/1440s × 0/15/30
initial left vehicles × bay 2/4/8 × independent/shared receiving.
Paired demand streams constructed from same random seed.

**9/9 new local unit tests PASS:** movement-level conservation every
second, deterministic replay, permissive no-gap extreme, protected-flow
negative control, receiver-storage ablation, validation and zero arrivals.

Permissive-gap opportunity at second t is an independent Bernoulli
draw with p = exp(-q_opposing * tau / 3600), where tau=5s and opposing
flow q is veh/h. It is a simplified Poisson gap *availability proxy*,
not observed behavior or an engineering safety threshold.

Selected 1,296-case averages (pooling pockets, receiving offsets,
12 seeds), shared receiver:
| Phase mode | Opposing q | Left network exits | Straight network exits |
|---|---:|---:|---:|
| Protected | 0 | 61.29 | 17.33 |
| Protected | 1000 | 61.29 | 17.33 |
| Permissive | 0 | 19.54 | 17.46 |
| Permissive | 1000 | 10.33 | 26.67 |
| Protected+Permissive | 0 | 63.88 | 14.33 |
| Protected+Permissive | 1000 | 63.21 | 15.21 |

Protected-phase invariance to *opposing q only* is a code design
negative control, not evidence protected phases are inherently
superior. Shared storage and finite green differ between the three
models; no common objective/safety/cycle optimization performed.

**Important horizon artifact:** shared receiver, 4-slot bay, in the
432-run scenario: with a 360s run, initial L=0 -> 46.6 exits,
103.4 remaining; initial L=30 -> 59.0 exits,121.0 remaining.
With a 1440s run the analogous results are 225.0/375.0
and 237.8/392.2. Extra initial vehicles are counted as part of
generated population. Therefore completed vehicles alone is not a
valid claim of higher capacity.

## Literature and source inventory
Tageldin, Sayed & Ismail (2018), AAP, DOI 10.1016/j.aap.2018.07.029:
3 treated and 3 matched control approaches; reported surrogate traffic
conflict count improvement adjusted for control changes, NOT crash
count reduction. Exact PDF was downloaded by the user, identified
and moved from 00_INTAKE to canonical 10_PAPERS.
Furth & Tabatabaei (2026), TRR 2680(11):689–705,
DOI 10.1177/03611981261424234: short right-turn/auxiliary-through
lane functional storage can be understood as per-cycle bonus discharge
or negative lost time; their paper explicitly does not cover
different-phase left-turn pocket dynamics. Exact PDF similarly moved
and renamed.
Yang et al. (2018) and Leng et al. (2012) are already held and
inform conceptual permitted left service model. Wang et al. (2022),
DOI 10.1061/JTEPBS.0000764, remains unheld; no full-text claim.

## Development gates / next steps
- Check physically accessible pocket entrance vs pocket storage full
  and blocked receiving link, in **one unified spatial model**.
- Separate receiving departure signal by movement lane group with
  collision-conflict constraints.
- Examine opposing headway data and calibrated, correlated gap
  acceptance instead of iid Bernoulli draws.
- Add generated/served/remaining and directional vehicle-seconds to
  finite-horizon evaluation. Outside-queue initialization is not
  neutral.
- Derive field-observable blocked-entry-cycle and queue-tail crossing
  metrics from Tageldin et al. before calibration.

The complete **executed local** v2.0 Python source, two raw CSVs
(1296+432 rows), JSON summaries, nine local test results, plot,
readme and SHA256 manifest are archived separately in
`T2_v20_phase_gap_repro.zip` with SHA256
`400f9b1292d386ec34a4c8ba013cea7279778a57821a797c05aa77c883524647`.
The v2.0 source has **NOT been uploaded to GitHub** and no GitHub
source parity/remote test claim is made. ZIP local path is recorded
in the associated conversation artifact. GitHub Actions/workflows
and main not changed.
