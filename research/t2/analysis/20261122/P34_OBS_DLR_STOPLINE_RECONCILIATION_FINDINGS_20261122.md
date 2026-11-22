# P34-OBS — Official DLR route counts versus actual 20 Hz center-point stopline crossings

2026-11-22 | R&E 2027 T2 | physical evidence priority 1 | **PARTIAL PASS / safety and causal gates HOLD**

## Research question and preexisting evidence

Can the **same measured 15-minute DLR-UT window** generate independently *detected* stopline center crossings and the publisher's **1Hz route-count** metadata in temporal agreement, without inferring signal-to-lane control? This is an **internal data-pipeline consistency check**, not independent field validation: DLR explicitly defines published traffic-volume data as derived from the same trajectory records, using a center-point stopline criterion (official documentation p.20 §5.1). The published 20Hz trajectory measurement has tracking and object fragmentation limitations (official documentation pp.24–25).

Use the older source-locked 2015 OpenDRIVE map `bs-inner-ring-road-ut.xodr` from [Drive publisher original](https://drive.google.com/file/d/1j6xu3ngbh1dO75_eCdrgBWVgytRAzGtg/view), with 2023-09-24 23:30–23:45 UTC [trajectory](https://drive.google.com/drive/folders/1MgVtPHh8UKMuv0hNhUQLRSmP_oNLN_FX) and [traffic-volume](https://drive.google.com/drive/folders/1MgVtPHh8UKMuv0hNhUQLRSmP_oNLN_FX) originals from one 15-minute batch. HASH LOCK: map `256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4`, trajectory `6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50`, 1Hz volume `00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798`. Original data bytes stay in Drive, not republished in Git.

### Preregistered analytical intent / source and route constraints

Prior P24 established candidate static stopline-style `type=294,dynamic=no` map features. P24b classified 4 inbound approach ends (100000, 179000, 201000, 280000), 1 outbound and 2 inside connectors. **P34-OBS is observational**, distinct from the existing **P25–P33 synthetic model / Go synchronization sequence** in main. The method is recorded here as executed exploratory analysis; it was **not independently preregistered before its first local examination**, so do not claim preregistered external replication.

Detector is independent of official volume events: use each object's successive direct (non-interpolated) sampled centers, map UTM32 to XODR, find whether the signed projection along the road reference tangent goes from negative to nonnegative (`s^-<0<=s^+`) at the static marker's tangent plane, enforce a driving lane in 2015 map, lateral coordinate within 20.5m and adjacent 20Hz sample time ≤0.20s. Only after detecting do we read publisher volume events and pair by the geometrically inferred **origin arm** and **timestamp within ±1s**. The matching is one-to-one maximum-cardinality / minimum absolute time error using ordered dynamic programming; route **destination and lane index are not inferred** by this matching.

> Geometric plane crossing is an approximation to the physical painted stopline width and optical location; linear interpolation between 20Hz positions gives a point estimate within the 50ms measurement bracket, not a directly observed instant.

## Results (one 15-minute nighttime sample)

Inputs: **8,624 trajectory rows / 37 tracked IDs**, 893 traffic-volume seconds, 12 nonzero-present route columns, 4 inbound map candidates.

| Inferred origin | Detected direct crossings | Publisher derived counts | One-to-one approach/time matched |
|---|---:|---:|---:|
| East (road 100000) | 5 | 4 | 4 |
| South (179000) | 5 | 6 | 5 |
| West (201000) | 7 | 7 | 7 |
| North (280000) | 0 | 0 | 0 |
| **Total** | **17** | **17** | **16** |

All 17 detected events have **50ms** adjacent direct-observation time brackets and no accepted event relies on a flagged interpolated sample. The **16/17** temporal/origin matches have median absolute timestamp difference **0.59025s** and largest difference **0.9163s**. These values are relative to the published *integer second timestamp*, not a validated precision or accuracy of vehicle stopline crossing timestamps.

### Two unmatched events are scientific data

1. **Trajectory only:** East road `100000`, car ID `1695598300234044` crosses the geometric plane at approximately **23:32:16.504583Z**. No official same-arm route count within ±1s. The reason is **unknown**: field of view, count publication rules, movement definition, map vintage or track processing are possible hypotheses, not conclusions.
2. **Official volume only:** `South1West1` count at **23:36:10Z** has no directly observed negative→positive crossing bracket. A potential left-censor candidate is tracked ID `1695598569934245`, which **first appears 23:36:10.516482Z, 0.436m downstream** of the projected South marker line. An event likely preceding the first frame is **plausible**, but cannot be promoted to a measured crossing. It remains an observation-boundary uncertainty.

The equal totals of 17 do **not** justify silently cancelling one unmatched crossing against one missing event.

## P24b correction — important source/schema issue

The original P24b source searched for `<validity>`, yet the actual DLR XODR source uses `<laneValidity fromLane="…" toLane="…"/>`; **all 7 static markers have this element**. It is incorrect to state that the source recorded no explicit marker lane validity. The original P24b code and its regression tests have been corrected in main. All four incoming markers have a declared scope: road100000 `-1..-5`, road179000 `-1`, road201000 `-1`, road280000 `-1`.

However, applying the **2015 static marker scope** as a mandatory 2023 trajectory-flow filter retains only **7/17 detected crossings**, including **6 of the 16 official-aligned crossings**. It rejects 10 internally aligned crossing events. Therefore the source has explicit geometric lane-validity metadata, **but that static metadata has not been validated as the 2023 vehicle-counting or active-signal lane scope**. Declared map membership is not an authority to erase source-consistent 2023 counts, nor proof the XODR map itself is wrong: the signal element's limited lane scope may serve a different semantic purpose from the producer's route counters.

## Adversarial multi-role review (one model, not independent peers)

- **Geometry critic:** A tangent crossing plane is not a finite-width painted stopline polygon; 2015 maps can differ from 2023 physical road markings. Require independent figure/visual check and georeference robustness.
- **Traffic data critic:** Same-source cross-check cannot validate reality independently; publisher volume counts originate from published trajectory pipeline.
- **Statistical critic:** Overall count 17/17 hides 1+1 unmatched records. 16/17 is an approach+time match, not proof of 16 correct destination routes.
- **Algorithm critic:** Greedy nearest-time one-to-one pairing can fail max-cardinality. A synthetic counterexample forces the new dynamic-programming matcher to return 2 pairs rather than 1.
- **Censoring critic:** A first frame already downstream is not evidence of an observed crossing; preserve event as unknown instead of back-extrapolating.
- **Causal/field critic:** **Do not infer controller group, red-light running, signal optimization effects, queue discharge headways, or physical congestion relief.**

Scientific claim allowed: **a SHA-locked 15-minute DLR observation window admits 16/17 internal, approach-and-second-aligned stopline crossing reconciliations, with explicit unresolved edge cases and a map lane-validity mismatch**. Any external-world or intervention effect claim is **HOLD**.

## Exact work products and reproduction

- [Actual-source audit runner](p34_dlr_stopline_event_reconciliation.py) remote Git blob `e2813ef8e42e86fec9066fcb1870fbcc7816144c`.
- [23 source-backed and adversarial unit tests](test_p34_dlr_stopline_event_reconciliation.py) remote Git blob `9004a078887f261c7840ff245b3025e390c81108`.
- [P24b corrected role reader](p24b_junction_stopline_roles.py), blob `1a4de55710f15ed51a7cf1e2e772c2acecd188c8` and [7 corrected tests](test_p24b_junction_stopline_roles.py), blob `da8509314768567c480027c13b055db126d33fb1`.
- [Machine-readable compact result and unresolved object IDs](P34_OBS_DLR_STOPLINE_RECONCILIATION_SUMMARY_20261122.json). Full 17-event candidate table is included in the external reproducibility bundle (original source originals excluded).
- **P34-OBS 23/23 and corrected P24b 7/7 local Python tests PASS**; remote `main` source content was independently fetched and matched exactly to the tested local source. No GitHub Actions or extra branches.

Run locally with `python -m unittest -v test_p34_dlr_stopline_event_reconciliation.py` and `python p34_dlr_stopline_event_reconciliation.py --map /path/to/bs-inner-ring-road-ut.xodr.xml --trajectories /path/to/trajectories_230924-233000_230924-234500.csv --volume /path/to/traffic-volume_230924-233000_230924-234500.csv --out p34_result.json` (requires `pyproj` and importable P24 geometry source in the same directory). File SHA mismatch is a hard error.

**Next:** an independent annotation of four physical approach stoplines, review movement-specific destination from track endpoints and actual lane semantics, inspect the two unmatched events with a human-labeled visual sample if available, and compare an independent road micro-simulator under frozen scenario inputs. Keep RF sensor signal quality and predecision policy-value studies on separate research tracks; school exhibition output still targets a physically observed city-road congestion phenomenon and credible improvement proposal.
