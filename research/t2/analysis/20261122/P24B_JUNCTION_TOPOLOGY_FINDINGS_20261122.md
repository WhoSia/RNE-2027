# T2 P24b — Stopline marker topology discriminates approach from connector (2026-11-22)

This continues [P24 source-locked XODR/PDF geometry audit](P24_XODR_STOPLINE_AND_SIGNAL_CROSSWALK_FINDINGS_20261122.md). Main scientific priority is traffic engineering at actual intersections, not creating more audit-only tools.

## Evidence

The original DLR UT 2015 OpenDRIVE digital map includes seven `type=294, dynamic=no` static signal XML elements (ASAM convention: stopline marking). Six distinct XML signal IDs are reused in seven physical road contexts. The source file has 28 roads and one junction, and lacks a verified mapping to the live 2023 time-series signal IDs 1–30. An element marked static must not be assumed to be a traffic-light controller.

**Structural rule frozen in code:** a non-junction road with successor junction and feature position within 1m of road end is an *inbound approach-end candidate*; a non-junction road with predecessor junction and feature within 1m of road start is an *outbound junction-start feature*; a road with a junction attribute is an *internal connecting-road feature*. This is a road-topology classification, **not a guarantee of stopline legal applicability or a signal head→movement assignment**.

## Verified 7-marker census

| Structural class | Count | Road IDs |
|---|---:|---|
| Inbound approach-end | **4** | 100000, 179000, 201000, 280000 |
| Outbound junction-start | **1** | 101000 |
| Internal junction connectors | **2** | 300013, 300018 |
| Unclassified | 0 | — |

The marker ID **300607 is reused by two different physical roads**, outbound 101000 and inbound 280000. Any algorithm using `marker_id` alone as a globally unique physical stopline primary key would merge distinct geographic objects. The correct key includes the *road ID plus marker occurrence* and should preserve the 2015 source reference.

This removes an obvious false interpretation: 7 static XML `<signal>` entries are **not** 7 active vehicle signal controllers, and they are not all independent inbound stoplines. In particular, two are inside the junction and one is on an outgoing road.

## Tests and exact executable provenance

[Physical structural classifier](p24b_junction_stopline_roles.py) remote `main` Git blob `bc3468312afb52de27c161b001e3a7deedc6160c`; [seven exact-source tests](test_p24b_junction_stopline_roles.py), blob `001abde2c8472f1f5b8d8a749c0e39fac6421152`. These files were fetched from GitHub `main`, reconstructed exactly via a read-only Google Docs transport receipt, confirmed with `git hash-object`, and **7/7 actual original-source tests passed**. Complete P24b JSON SHA256 `79f1ff78090cce0fe974571d0a5ae7ba666df7c753b06dc1f0738d2a96666f5f`, test log SHA256 `34f369aa8d09a7475ed44581d8996ef349d3fd402fff0003aa7939c031c3fcdd`. [Compact machine ledger](P24B_JUNCTION_APPROACH_STOPLINE_RESULTS_20261122.json).

## Independent skeptical check and next physics experiment

- Geometric auditor: source projection, arc geometry, road successor/predecessor topology pass.
- Skeptic: do **not** infer movement control from nearest Euclidean distance; road coordinate `s` and predecessor/successor are only *candidate gates*.
- Data engineer: 300607 duplicate key is a true counterexample; require `(road_id,marker_index)`, not marker ID alone.
- Traffic engineer: direction/validity may depend on lane sections and legally permitted turns, and no explicit valid `<validity>` lane range was found on these seven features. Need select individual route and verify against the official movement column and video-derived 20Hz trajectory.
- Statistical reviewer: the 2023 Sunday 12:00 window 436 crossing indications is not independently labelled congestion. Selection on successful exits would bias observed headways. Do not use post-treatment arrival information for decision claims.

**Next P25:** for each of the four approach-end candidates, compute reference-line direction and laneSection driving-lane indices at that point; match a vehicle's passage to the source stopline geometry with a frozen signed-crossing rule, then independently compare 1Hz source movement-bin counts. Retain unmatched vehicles, censored cases and negative controls. Yellow/clearance and SUMO external confirmation remain open.

Original publisher source files remain in Drive; K047 sealed and CIM held; no actions on live traffic controllers.
