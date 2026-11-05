# T2 v6.10-I / P11-I / D7 — 2026-11-05 Decision

**GO** for a narrow mathematical audit of OpenDRIVE lane-width polynomial intervals and a conservative source-declared geometric junction audit. **NO-GO** for complete OpenDRIVE conformance, road legality, vehicle collision-free motion, field validation, or superiority over Schwab & Kolbe (2022).

All eight newly added intake PDFs were confirmed via their text, renamed and moved to `10_PAPERS` with unchanged Drive file IDs. Neither original PDF byte SHA256 nor independent copies were needed or produced. Existing H source ZIP unchanged.

**Technical result:** A width profile `w(s)=(s-5)^2-1` appears positive at both endpoints of `[0,10]` but negative at s=5; a station-only/endpoints-only validator misses it. New code analytically evaluates derivative roots on each piece. It also detects a jump at a width knot and a declared road transition with disjoint XY endpoints. Geometrically matching lane centers return `UNKNOWN` until actual driving orientation, restrictions and 3D clearance are independently established.

**Limitations:** The polynomial extrema have floating-point numerical rounding; no interval-arithmetic rigorous error bound. The geometry gap compares endpoints/centers but not full lane polygons, driving direction or crossing priority; 2D gap may hide 3D vertical separation. The existing H road model cannot decode full OpenDRIVE 1.9, paramPoly3, lane height, shape, complete signal logic. Policy P12 remains frozen except nonexecuting vocabulary from H.

**Next:** perform independent original OpenDRIVE raw-byte parse; add lane polygons and bounded-precision tests; parameterize 3D gaps and orientation; run matched reference-pipeline study against Schwab & Kolbe before novelty claims.
