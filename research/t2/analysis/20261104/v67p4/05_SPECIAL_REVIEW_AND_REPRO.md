# Special researcher verdict: PARTIAL ACCEPT / INTEGRATION HOLD

P4's 12 bridge/viability tests and P3's 13 contract/replay regression tests passed; 156 additional controlled synthetic runs generated. The two test sets assess different physical abstraction levels; do not sum their evidence as a validation of a unified microsimulator.

Accept: explicit multiple-junction state model, length-based finite receiving links, stage-wise conservation audit, storage blockage reporting, signal phase offsets and synthetic stop-go diagnostic.

Hold: true P3 2D/IDM multi-intersection integration, upstream/downstream feedback with continuous geometry, multi-vehicle compatible conflict graph, P3 seed-943 stopline repair, independent SUMO and field calibration. The bridge's single connector makes intersection capacity deliberately conservative.

Repro archive T2_v67_P4_network_bridge_viability_20261104.zip, 14 files with per-file SHA256 manifest, in dated Research OS 20261104 folder once upload is verified. Code must remain accessible via immutable ZIP unless GitHub executable code sync is separately verified. No GitHub Actions bot credited.