# N research verdict (2026-11-05)

**GO — controlled geometry/software feature:** sampled 3D curvature and torsion (first/second/third derivatives), 2 stencil sizes; synthetic helix analytic reference, source-knot fail closed. A numerical difference between two stencil sizes does NOT provide a certified truncation/roundoff error bound. Source-declared lane center is a conditional cross-section approximation, not an independently surveyed lane geometry.

**GO — actual observed external data contact:** six published 2026 Michigan winter-driving CSVs read via GitHub connector. They have 5,967 synchronized frame rows and 19 consecutive blocks of constant `marwis_friction` with 13 changes. Real MARWIS readings are NOT 5,967 independent friction measurements, NOR 19 independent ground truths. Snow/ice context and geographic/seasonal confounding preclude causal attribution to asphalt/concrete.

**HOLD — original raw-data custody:** SHA1s are upstream Git blob IDs, not local independently calculated byte checksums. Original six CSVs were inspected via connector and remain in the upstream source repository; they are not in the N ZIP. DTU original CSV download and FHWA measurement rows remain unavailable locally. Do not claim field calibration.

**HOLD — policy:** P12 optimization deliberately frozen pending comprehensive road and data validation; no active controllers, field actuation, speed or safety instructions added.

**Next:** Obtain full source CSV with independent hash and named device units; time-cluster at sensor update or trip level; test reproducible independent OpenDRIVE sample, 3D lane-profile discontinuities, and 3D coordinates under varying lateral geometry. Build a site/day holdout before any empirical model claims.
