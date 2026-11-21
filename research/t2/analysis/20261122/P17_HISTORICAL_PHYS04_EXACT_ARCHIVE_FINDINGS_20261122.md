# T2 P17 — Historic PHYS-04 real-archive observation/geometry audit

**Date:** 2026-11-22 KST  
**Verdict:** **NO_STRONG_WITNESS** for a strict opposite-policy-sign alias at pre-fixed epsilon=5 among 144 historical source-derived PHYS-04 cases, when capacity, pocket length, B-lane assignment and the exact six count-observations are held fixed. One **weak opposite-sign candidate** exists only at epsilon=0. Adding occupied-cell positions eliminates that candidate. This is a bounded negative result, **not proof of universal sufficiency**.

## Authentic source, not fabricated fixtures

Source: [PHYS-04/05/05b/06 Drive evidence archive](https://drive.google.com/file/d/1nIHmzoz0Yk3YUqaaxvbBWH7ztgR2ddo-/view), uploaded 2026-11-21 and downloaded freshly through the connected Drive provider on 2026-11-22.

- Downloaded ZIP: 52,090 bytes, exact SHA-256 `7f7eff90b83cfe5e1f071bb02d5880face9c0e047abcd17349cd3fb06392758e`. This **now establishes matching remote ZIP bytes**, upgrading the original metadata-only check without rewriting its earlier historical receipt.
- The **ZIP integrity test** found no damaged members.
- `canonical_local_capacity144.json` SHA-256: `0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001`, exactly the prior PHYS-04 reported digest.
- Original JSON provenance is explicitly `LOCAL_RECONSTRUCTED_FROM_MAIN_SOURCE_NOT_BYTE_VERIFIED`. It comes from a **historical locally reconstructed model**, not a 2026-11-22 rerun of exact canonical GitHub engine. Its original 144 checkpoint identity cases, 0 reference mismatches and 13 fields per case are internally confirmed; those 1,872 recorded comparisons were not independently regenerated in this session.
- Our new independent read-only audit validated **all 144 row schemas**, six integer counts, occupied-cell cardinalities and bounds, vehicle conservation proxy constraints for receiver fullness, and the recorded treatment-minus-baseline costs at penalties p=0/60/120. No P15 synthetic cost fixture entered this result.

## Exact screening definition

Each matched group holds fixed:
`(capacity, pocket_m, b_share, outside_A, outside_B, approach_A, approach_B, pocket_vehicles, receiver_vehicles)`.

For a chosen terminal penalty p, `delta_p = cost_treatment_p - cost_baseline_p`. A strict opposite-sign pair at epsilon=5 must contain a delta < -5 and a delta > +5 **within one matched group**. A record's two policy futures already share its own checkpoint; distinct records need not share full microscopic states or future arrival histories.

| Grouping | Unique groups (144 rows) | Groups with >1 row | Opposing signs ε=0 | Strong opposition ε=5 |
|---|---:|---:|---:|---:|
| Full geometry + six counts | 133 | 11 (22 rows) | **1** | **0** |
| Full geometry + six counts + occupied-cell positions | 141 | 3 (6 rows) | **0** | **0** |
| **INVALID**: drop B-lane assignment `b_share` | 123 | 19 (40 rows) | 2 | **2 (spurious)** |

The same qualitative results hold at terminal penalties 0,60,120 and with epsilon20 (no strong matched pairs). See the frozen machine-readable [summary](P17_PHYS04_VERIFIED_ARCHIVE_SUMMARY_20261122.json).

### The only weak six-count candidate

- Receiver capacity 2, pocket 14m, B preassignment share 0.
- Six counts at the decision time: `(outside_A=0, outside_B=0, approach_A=16, approach_B=8, pocket=2, receiver=2)`.
- Seed0 model Δp60 = **−305** vs seed3 Δp60 = **+1**.
- Full B-lane occupied positions differ: seed0 `[-11,-7,-6,-5,-4,-3,-2,-1]`; seed3 `[-11,-9,-6,-5,-4,-3,-2,-1]`. Thus there is no identical *position-level* observation in this contrast.
- Both original worlds have 2 pocket vehicles and 2 receiver vehicles, but there is no independent proof that their future arrival request streams are drawn from genuinely independent clock histories. As found in the earlier arrival-clock audit, nominal `uniform` request timestamps can be identical across seeds at fixed demand.

This is an **ordinary weak model-sign opposite**, not evidence of a robust policy harm under same observation.

### The dangerous negative control: erase B-share from the match

If we remove `b_share` from the grouping key, two apparently strong oppositions appear:

- Capacity2, pocket14, **same seed0**, B share 0 versus .5: `−305` against `+1477`.
- Capacity4, pocket14, **same seed0**, B share 0 versus .5: `−152` against `+1610`.

These are different baseline lane allocations and predecision microscopic worlds. Treating them as 'same observed state' would manufacture a strong causal or informational conclusion. The nonvalid grouping is retained only as a **reproducible falsification test for data leakage and mismatched scenario contracts**, not as research evidence that sensors fail.

## Reproduce exact historical input

Source code committed on `main`:
- [p17_zip_audit.py](p17_zip_audit.py)
- [test_p17_zip_audit.py](test_p17_zip_audit.py)
- [Compact result summary](P17_PHYS04_VERIFIED_ARCHIVE_SUMMARY_20261122.json)

Save the above Drive ZIP locally without modification, then:

```sh
cd research/t2/analysis/20261122
python p17_zip_audit.py /path/to/T2_PHYS04_05_05b_06_20261121_Research_Bundle.zip p17_full_audit.json
P17_HISTORICAL_ZIP=/path/to/T2_PHYS04_05_05b_06_20261121_Research_Bundle.zip python -m unittest -v test_p17_zip_audit.py
```

Python's standard library only. **9 / 9 local tests PASSED** on the downloaded historical ZIP, including full 144-row results. The tool refuses mismatched archive and result hashes rather than proceeding on an unverified copy. With no ZIP in the test directory, the file-dependent test is explicitly skipped instead of falsely passing.

Exact executed/fetched canonical `main` source blob: `48520ec26fb215f30cdebf39803524e9c2bd3cc4` (SHA256 `6e8c3746ca786c151c8d88c322bff98bf41e09112314c0bc4e2aadf14cd6a2a5`). Exact test blob `5d3cc0cc51deb0ef0d68ce7f0ce93b376067c416` (SHA256 `62af0276223bb3b58ec488a775eb90b0e1d10010e0edaf3f9cd57fc64ea11474`). Complete locally regenerated 27-condition audit JSON SHA256 `833b7eecfef1d3f2ab1b7903c2b8190db661ff813f39c25525bb03a2f55f9913`. Local 9-test verbose log SHA256 `a155b46e990d1d47e68180a7439e70d424ea8889a7506839167f31aa87c10e59`. GitHub Actions/bot not used.

## What we still CANNOT claim

1. That six counts suffice for every T2 physical state. Only 144 preselected historic cases were checked; 11 collision groups are sparse.
2. That 144 worlds equal 144 independent experimental traffic days, or that different seeds imply different request timestamps.
3. That the existing P12 abstract timing validator is integrated with PHYS-04 phase controls. The historic intervention remains a **virtual** left-service intervention with incomplete operational constraints.
4. That RF CSI detects any of these six counts or diagnostic labels. No RF radio hardware, fresh sensor trial or real street was involved.
5. That positions themselves causally explain the −305/+1 difference: only a position mismatch was identified, with future timing and model state still potentially confounded.
6. That the earlier source-derived execution is now a full clean canonical re-run. The remote **archive** bytes were independently sealed; its internal historical **model provenance** remains unchanged.

## Next falsification gate

First reproduce the 144 PHYS-04 cases using exact canonical engine code and compare the resulting JSON with this archive. Then construct a prospectively frozen cohort that respects action feasibility and distinct timestamp tapes. Test equal six-count and full-position groups without dropping geometry, report both strict sign and practical regret, and explicitly report NO_WITNESS when appropriate. Keep the independent RF exhibit track separated until real CSI trials show any measurement validity.

K047 sealed; `CIM dataset.zip` on HOLD; no public-road intervention.
