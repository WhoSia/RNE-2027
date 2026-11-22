# P24 — DLR-UT map-source join: coordinate success is not a traffic-control assignment

**2026-11-22, main-only research; passive observations.** The immediate research goal is to enable external calibration of an actual traffic-efficiency simulator, not to replace the original Changwon/Gyeongnam traffic-improvement aim with an endless audit of audit machinery.

## Grounded sources

- Original publisher DLR Urban Traffic v1.3.1, *documentation.pdf*, pp. 12–14, Table 3 (signal positions), Figure 1 (visual identification), Table 4 (colors), p.20 (route count conditions). **Observed SHA256 `94fd9ebd32d04a9c35b02be526fbd11a8d5a613933d7961fde800386853b34f3`.** This corrects the previous P23 recorded digest `3c733...` which fails on the present exact downloaded primary file. Tested corrected P23 now 5/5, prior P23 code against this exact PDF 4/5 due to locked digest mismatch. Earlier claim of byte-sealed acceptance is amended; underlying document state-code interpretation remains separately supported by actual Table 4.
- Original `.xodr` publisher map SHA256 `256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4`.
- Night `23:30–23:45` trajectory CSV SHA256 `6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50`.
- Three original `traffic-volume` CSVs SHA256 locked under P22, 12:00,18:00,23:30 UTC. No retrospective switch of which time windows are tested.

## Result A — coordinate registration

OpenDRIVE root records 28 roads, 1 junction and geoReference `+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=-104763 +y_0=-5792795 +datum=WGS84 +units=m +no_defs`. EPSG:32632 coordinates in the publisher PDF become the map's planar coordinates with east/north translation `(-604763,-5792795)` to a high precision in these source examples: physical vehicle signal ID 1 UTM (604755.480, 5792814.102) => local (-7.520, +19.102).

Official document Table 3 has 18 physical head locations for 9 vehicle traffic-light IDs 1–9. All 18 transform into the `.xodr` map's declared extent; all 8,624 sampled trajectory centers also lie within that wide map bounding box. **But a bounding box is weak: an entire city district can fit inside it.** A separate 1-m stepped exact line/arc reference-geometry sample yields median distance 3.572 m, p95 7.416 m and p99 12.459 m over 8,624 trajectory observations; 97.26345% are within 10m of the nearest *road reference* line, not a lane center. Repeated observations from 37 tracked objects are not independent experiments. The reference-curve distance is a coordinate plausibility diagnostic only; road width/lane offset and the identity of actual vehicle approach are not inferred.

## Result B — no automatic signal/movement join

The `.xodr` map has seven `<signal>` instances with 6 unique ID strings `300600,300602,300604,300605,300606,300607`, each with `dynamic="no"` and type `294`. There are no `<controller>` or `<signalReference>` elements. The real traffic-light observation channels are ID 1–30; the nine motor channels 1–9 are all disjoint from the `.xodr` signal IDs. The map signal references are not the physically measured signal states. **A nearest-sign heuristic would be a new unsupported assignment**, not a successful join.

The publisher's `traffic_volume` movement names for the predeclared DLR observation windows give 32,27,12 distinct route columns. For example `West0West1` appears in the 12:00 source; rejecting a same-direction route by a hardcoded `from != to` condition would be an analysis bug. The route label's approach/lane token *does not correspond automatically to an OpenDRIVE lane index*. The official PDF explicitly says columns appear only for routes with a detected participant in that interval: an omitted column should not be imputed into a uniformly zeroed permanent route catalog without an independently validated global schema.

## Result C — source-sealed, fail-closed offline analysis

`p24_dlr_map_join_gate.py` and its 9 regression tests were run locally on six actual original files. Nine tests passed, including PDF exact digest, 18 signal head coordinates, 8,624/8,624 bbox points, unmatched signal IDs, all three movement schemas, valid same-approach route label, and deliberately wrong source digest errors. New source/test copies also written to GitHub `main`, but **the remote GitHub source is not claimed to have been re-run in this session as an exact blob**, unlike corrected P23. Exact local P24 source, actual computed outputs, checksums and test logs are preserved in the bundle.

## Independent-role challenge

- BUILDER: UTM registration and neighborhood-level spatial sanity established; **PASS**.
- EMPIRICAL: a visible signal head location and car position are *not* a correct signal-to-lane assignment; **HOLD**.
- STATISTICIAN: 8,624 points are serially correlated within 37 trajectories, do not use them as 8,624 independent confirmation trials; **PASS correction**.
- FAILURE REVIEWER: previous P23 code's official-PDF digest was wrong; a previously claimed green P23 unit run fails against the exact present input, now **corrected with reproduced 5/5**; preserve both original failed and corrected evidence.
- TRAFFIC ENGINEERING: traffic-volume route labels are not independently validated OpenDRIVE lanes, and road reference lines differ from lane center/stopline; **HOLD**.
- RESEARCH DIRECTOR: do not redefine the school science-fair project into a map-converter or verification-only topic. Restore primary Gyeongnam/Changwon traffic-flow study, with DLR international data as an external calibration yardstick, SUMO as independent simulator and physical sensing/decision-value secondary conditional work; **GO with narrow next gate**.

## Next P25 — concrete physical-gate task, no specious output

1. Extract actual OpenDRIVE `laneSection` geometry and predecessor/successor topology, not only road reference centerlines; establish route token → candidate approach polygon with evidence and a human-review UNKNOWN option.
2. Use the publisher Table 3 traffic light coordinates plus Figure 1 road orientation to make a candidate correspondence table, not an automatically accepted control map. Require an independent stopline-crossing comparison and publish both mistaken/ambiguous cases.
3. Once route labels align with signal IDs, use the *predeclared midday* DLR observations and actual trajectories to establish a finite-resolution discharge benchmark. Sampling 1Hz cannot produce arbitrarily precise controller transition times.
4. Independently replay matched demands in SUMO. **Do not** infer yellow/all-red, pedestrian clearance or legal field phases from the incomplete observed controller tape; no live intervention.
5. Translate the validated geometry, baseline congestion and operational constraints into Changwon/Gyeongnam candidate scenarios. A usable school science-fair result is a tested local traffic-flow improvement, not just an ever-growing validation harness.

No K047 opened, no CIM ZIP opened, no GitHub Actions/bot, no new working branch, no fictitious independent external LLM peer review.
