# T2 v6.10-L / P11-L / D10 — Field-contact research gate

**Policy:** P12 optimization remains frozen. New modules are measurement contracts, planar geometry and signal time audits, not physical traction calibration.

## Reproducible results
- New L code + inherited K.R1: 173/173 tests pass (150 inherited + 23 additional).
- Canonical ZIP with 51 files, CRC verified, SHA256 `aba254b26c23260f2e72269813761e9a8dfc3036cef57a18772c9cfd84209315`. https://drive.google.com/file/d/1kQV6RpMRcytvzJUpKpdHE2jRwdLKxHpm/view
- Unmodified K.R1 parent SHA256 `2b785769dded97c92957480336ed3389576c701b39ea29692c5b80ffe4d80536`.
- Planar normal-offset lane curve: k_lane=k_ref/(1-t*k_ref) under constant offset/no cusp and no bank/grade; example 0.02 / (1 + 0.04) = 0.0192307692308 inv m. If unsupported terms appear, return UNKNOWN.
- Utah intersection 5502: 500 previously derived real-source SPaT observations revisited through connected source; 7 state transitions within 49.913s and temporal brackets recorded; these are NOT friction, traffic delay, or vehicle trajectories.
- FHWA InfoPave MON_FRICTION and FHWA InfoMaterials CPFM catalog and access routes verified, but **zero original field friction records downloaded**. A reported Skid Number, a CPFM device result, a texture depth, and tire effective friction are different constructs. No unverified conversions.
- esmini/OpenDRIVE published example 500m line and lane widths examined through external GitHub; local raw byte source not obtained, example is not surveyed real road.

## Reproduction and caveats
Drive journal: https://docs.google.com/document/d/1STwyyvd8LqEjI73qmNV7xVitLm_NGAILQ0dNpTt9vPM/edit
Full code, inherited K.R1 source and all test code are in the canonical ZIP. The historical GitHub K.R1 road_physics_bridge.py source had an unresolved upload blocker, hence **this GitHub branch alone is not an independently executable complete L snapshot**. Do not claim a matched independent real-road OpenDRIVE parse. Original K.R1 preserved; no bot author.
