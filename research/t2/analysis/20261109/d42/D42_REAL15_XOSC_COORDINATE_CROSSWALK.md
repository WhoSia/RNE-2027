# D42 — CSV ↔ OpenSCENARIO 20 Hz full-vertex crosswalk (2026-11-09)

**Finding:** the 2023-09-24 12:00–12:15 UTC original DLR UT v1.3.1 trajectory CSV and the publisher-supplied OpenSCENARIO example are internally consistent at the individual ID, vertex count, timestamp and 2-D coordinate levels.

## Sources and seals

- Raw CSV: [51,209,266-byte original](https://drive.google.com/file/d/14yh6W9MLAW6IvsoZsvHr3SzS_rovYs6S/view), SHA256 `5504d37534fd12e95a9e1b019de18f504a2d668dcf564392bb169d42ab42550e`.
- Publisher XOSC: [140,160,082-byte XML](https://drive.google.com/file/d/1RfAe9dQx8unqbpmYrWRfM8ULrJcYHMxT/view), SHA256 `7e30c842c25a236a8ab120be0f6fff95ad58236f600252f1e0657af096a97753`.
- [Runnable crosswalk validator + 5 synthetic fixtures + JSON result](https://drive.google.com/file/d/1dVjyga_duq7iDu_O4lTqtT9qig75ouhy/view), SHA256 `219ac67c242a3c3eb5f34058ccb1037f37a798c7f873846704941f220845a0c1`.

## Exact correspondence

- `636 / 636` track IDs matched; `299,053 / 299,053` vertices matched and the vertex count for **every individual ID** agreed.
- Coordinate transform: `x_XOSC = center_easting_UTM - 604763.0 m` and `y_XOSC = center_northing_UTM - 5792795.0 m`.
- Max coordinate discrepancy across all 299,053 vertices: East 0.000501073m, North 0.000623894m; RMS East 0.000288521m, North 0.000314242m (plausibly consistent with rounding).
- `t_XOSC = timestamp_CSV - 2023-09-24T12:00:00.016482+00:00`, exact at stored precision (max difference 0 s).
- Five synthetic bridge tests all passed: exact match, coordinate perturbation rejected, timestamp perturbation rejected, missing ID rejected, missing vertex rejected. Together with D42 raw triad's ten contract tests **15/15 pass**.
- During negative test construction, an empty denominator issue in the crosswalk auditor was discovered and fixed; the sealed bridge archive contains the corrected implementation.

**Scope limitation:** these are two representations of the **same underlying sensor measurements**, not independent validation of trajectory accuracy. No heading equivalence, physical signal-head↔movement mapping, lane stopline geometry, queue measurement or field-based policy reversal is established by this check. The claimed coordinate origin is a transformation between data representations; it does not on its own supply lane topology or exact stopline locations.

## Next gate

Derive stopline and lane movement geometry from the publisher OpenDRIVE map and description, then reconstruct center-point crossings with interval-censored timing. Audit the publisher's 32 movement columns and 436 crossing counter cells rather than assuming 436 unique vehicles. Link the 30 traffic signal heads only after physical/semantic association is verified. Preserve the three observed signal sampling gaps.

Previous raw triad audit: [D42_REAL15_RAW_TRIAD_AUDIT](D42_REAL15_RAW_TRIAD_AUDIT.md).
