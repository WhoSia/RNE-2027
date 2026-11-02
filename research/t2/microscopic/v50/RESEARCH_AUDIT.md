# T2 v5.0 — Microscopic-driver uncertainty, separable green/offset effects, exposure-ledger correction

**Date:** 2026-11-02. **Status:** executed synthetic experiments; no Korean field calibration, no SUMO verification. **Visuals:** intentionally not generated.

## 1. Source and correction of v4.9 accounting

`T2_v49_network.py` in the historical package counts `vehicle_seconds+=(generated-len(completed))*DT` **after** crossing completions at the end of each step. A vehicle completing during `[t,t+DT)` should contribute `DT` vehicle-seconds for that step. The post-completion placement omits exactly `DT` per completed vehicle. For v4.9, `DT=0.5s` and the bias is `0.5 × completed vehicles` vehicle-seconds (per scenario, assuming discrete aligned births and completions). The corrected v5.0 engine accounts exposure **before** completing movements. Independent trajectory reconstruction passes the identity:

`system_exposure = Σ(finished_i - born_i for completed i) + Σ(H - born_i for right-censored i)`.

Every step retains the conservation invariant: generated = completed + inside + source_pending. All 216 new runs checked this identity. Three directly repeated original cases also verify the difference equals exactly `0.5 × completed`.

Using the original 60-row historical v4.9 CSV and analytically correcting per run, main-priority (green+offset combined) versus fixed improved exposure in balanced demand by **18.7845%** (earlier 18.8883%), main-peak by **15.1081%** (earlier 15.1620%), and worsened side-peak by **4.1999%** (earlier 4.2127%). The ranking does not reverse due to this correction. Individual rows are in `v49_exposure_correction.csv`; original v4.9 history is preserved, not silently overwritten.

## 2. Factorial experiment

3 demand classes × **4** paired exogenous arrival seeds `(11,29,41,73)` × **3** driver micro-parameter assumptions × 3 main green times `(25,32,38)s` × 2 offset patterns `(0,0,0)` or `(0,14,28)s` = **216 completed, independent simulation calls**. Fixed 60s cycle, 2s lost per stage, 15s min green, Δt=0.5s, 580s horizon, new demands stop at 320s. Driver configurations:

- `v13_T1`: free desired speed 13 m/s, IDM headway 1.0s;
- `v13_T1.3`: free speed 13 m/s, IDM headway 1.3s (v4.9 reference);
- `v10_T1.8`: free speed 10 m/s, IDM headway 1.8s.

**Caution:** These are arbitrary sensitivity configurations, not a calibrated uncertainty/confidence set for Gyeongnam. Parameters other than these are held as in v4.9, and no multi-driver heterogeneity inside one run is implemented. The matched-seed cohort enables within-model comparisons, not external causal estimates.

### Selected comparison at reference driver v13_T1.3

All values mean cumulative vehicle-hours over four paired seeds (smaller better), including unresolved vehicles through the horizon.

| Demand | G32 zero offset | G32 progression | G38 zero offset | G38 progression | G38 progression vs G32 zero |
|---|---:|---:|---:|---:|---:|
| balanced | 3.182 | 3.074 | 2.654 | 2.599 | 18.34% reduction |
| main_peak | 8.018 | 7.887 | 6.933 | 6.788 | 15.33% reduction |
| side_peak | 7.023 | 7.194 | 7.173 | 7.411 | 5.52% increase |

This **separates** green effects from offsets. Example for balanced demand at green32: progression reduces mean exposure by ~389.625 vehicle-seconds relative to zero offset. Under side_peak, identical green32 progression **increases** mean exposure by ~612.5 vehicle-seconds. The actual sign is not constant across four paired seed draws in all contexts, so no population-level inference is justified.

### Micro-parameter sensitivity and robust recommendation

Among **six candidate policies only**, after averaging over four seeds in each scenario × driver configuration, all three tested drivers selected the same candidate per demand:

- balanced: `G38_progression`;
- main_peak: `G38_progression`;
- side_peak: `G32_zero`.

The maximum relative model-regret within this finite three-parameter model set is zero for each corresponding best candidate, **because the same candidate is optimal in every one of those three assumed models**. This is a limited *negative finding* for policy rank reversals and provides neither a globally optimal signal timing nor field-valid decision confidence. Note that main-peak `G38_zero` finishes *more* vehicles than `G38_progression` in the observation horizon even while the latter has lower cumulative vehicle-seconds; metrics have distinct trade-offs.

## 3. Verification

- 13 inherited v4.9 tests pass against v5.0 code;
- 12 new tests pass: driver parameter validation, independent green vs offset, non-negative states, matching input scenarios, corrected exposure accounting, right-censoring, and more;
- independent cohort sum reproduces corrected cumulative exposure to numerical tolerance on **every** run;
- 216 actual output rows in `matched_runs.csv`, 54 cell means, 63 paired contrast rows and 18 robustness rows; files present in the package.

An initial oversized 648-run configuration exceeded the current execution window; it was **not** completed and is not included in any results. The reduced, prespecified 216-run factorial completed without failure. Four seeds are too few for a precise confidence interval.

## 4. Theoretical boundary and prior art (verified 2026-11-02)

**Do not claim to invent robust max-pressure control under uncertain observations.** Tan, Hu & Wang, *Regret-Based Max-Pressure Traffic Signal Control under Uncertain Traffic States*, posted October 23, 2026, https://arxiv.org/abs/2610.32290, already treats pressure regret from imperfect measured state and derives performance bounds and SUMO evidence. Huang et al. 2026, DOI https://doi.org/10.1109/TITS.2026.3709347, develops more systematic microsimulation calibration for control. FHWA Traffic Signal Timing Manual chapters 3, 5, 6, 7 document service lost time, minimum green, timing offsets and field queue validation. Our potential contribution must instead focus on **measurable uncertainty introduced by different micro-mechanisms/measurement sets in a realistic, independently tested corridor**, ideally with a falsifiable new result.

## 5. Next gates

1. Identify what field observations *actually* distinguish the 3 micro assumptions: departure headway, queue dissipation profile, speeds, and queue length; compare sensor cost and accuracy on independent days.
2. Make a proper merge/movement-conflict graph and left-turn movement queues, add bus stops and pedestrian calls; test signal safety constraints. Current 6-link one-lane prototype still lacks all of these.
3. Compare exactly matched OD, geometry, speed models and phases against SUMO; report divergences instead of assuming equivalence.
4. Obtain Gyeongnam intersection phase plans, movement counts and independent queue observations. Do not recommend changing live signals without authorization.
5. Increase seeds and perturb actual parameter uncertainty only once independent calibration evidence is available.
