# P11-G — Verdict 2026-11-05

**GO** for a limited OpenDRIVE source-auditing component; **NO-GO** for a simulation-ready road network or globally validated OpenDRIVE reader.

### Evidence

- Executable 2-road synthetic OpenDRIVE example: `A` line (s 0–20m) with `z(s)=3+0.02s` and 3.5m width; `B` arc (s 0–10m, curvature 0.05 1/m) with constant z=3.4m. One explicit `A:-1 -> B:-1` laneLink accepted but *traffic orientation NOT certified*. The computed endpoint of B is approximately (29.58851, 2.44835, 3.4)m. Synthetic test passes.
- 16 new OpenDRIVE tests and 60 v6.10-F existing tests pass (76 total). Source P2 SHA checked; 28 regression tests pass on a temporary extraction without mutation.
- Explicit null elevation, unsupported geometry and invalid geometry continuity recognized; the importer never synthesizes legal turn permissions or signal programs from topology alone.
- External metadata inspection `esmini/esmini/resources/xodr/straight_500m.xodr`: SHA1 `87d852dafad73809ec0724260bbe9235c7cca8e5`, 7080 bytes, one `<road>`, one `<line>` and one `<laneSection>`, with elevation metadata. Raw original file not locally acquired or tested by our parser. License review pending.

### Known faults / absent capabilities

- No full XODR 1.9.0 conformance; subset based on portions of v1.8.1. Clothoid/spiral, parametric curves, lateral offsets and superelevation missing. Cubic lane-widths are parsed, but values becoming negative beyond the start are reported as unknown rather than subjected to a global positivity proof.
- Junction `contactPoint` and `laneLink` reference identity is checked; legal driving direction, link predecessor/successor semantics, conflict polygon, lane type permissions, signal state and clearance remain unvalidated.
- No physical collision geometry, field-scale vehicle movement, policy optimizer run, external SUMO run, observed data prediction.

### Next (P11-H/D6)

1. Add `spiral` with numerical reference verification and `paramPoly3` with explicit `pRange` conventions; test exact end-pose continuity and road lengths against independent esmini/ASAM implementation.
2. Add `laneOffset`, `superelevation`, `lane-level elevation/height`, lane section borders, pedestrian and bike lanes. Do not treat numeric centerline elevation as physical clearance proof.
3. Acquire/release-license-audit an immutable upstream XODR example; execute parser on original bytes, compare reference curves with esmini or another independent parser.
4. Continue source-grounded OSM via-way restrictions / actual junction mapping and USA SPaT/BSM provenance. **P12 policy work remains frozen**.
