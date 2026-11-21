# RF01 — Honest feasibility receipt: Wi-Fi sensing as a traffic-blockage diagnosis

Date: 2026-11-21 · R&E 2027, exhibition research track.
**Evidence grade: analytic radio geometry + tested data-evaluation SOFTWARE.
No actual Wi-Fi CSI, vehicle RF trials or built detector.**

## Decisions completed

1. Established that Wi-Fi CSI vehicle sensing and signal-related
   traffic sensing are prior art (WiTraffic 2017/DeepWiTraffic 2019;
   2025 ESP32-CSI congestion; WiCrossing 2026). Rejected a
   'first camera-free Wi-Fi traffic light' claim.
2. Selected a narrowly falsifiable novelty hypothesis: distinguish
   toy **turn-pocket entrance** from **downstream receiving** blockage
   using two longitudinal fixed links and out-of-placement/session
   generalization, not generic vehicle counting.
3. Ran exact 2.4 GHz first-Fresnel geometry: 1m link radius
   ~0.176716m. At 1:20 scaled 3.5m lanes, 0.175m center
   separation is less than the sum of link midpoint first-zone
   radii ~0.353432m. **Naive adjacent-lane spatial separation
   fails the midpoint overlap plausibility gate.**
4. A 0.70m longitudinal section separation has no midpoint-disc
   overlap for the same illustrative pair. **This is geometry,
   not proof of CSI response selectivity.**
5. Pre-registered five labels, negative controls, separate
   training/test placement/day, RSSI-vs-CSI baselines, abstentions,
   trial-unit counting and empirical stop criteria **before
   any new RF measurements**.
6. Built a trial-level classifier assessment with train-only
   feature standardization, label-independent prediction,
   fixed P1/S1–S2 training and P2/S3 held-out testing.
   Test missingness is counted in the denominator; synthetic
   fixture results CANNOT pass the empirical gate.
7. Inspected zero new purchases or live road signal interfaces.
   This study never ran a radio data collection process.

## Code and deterministic checks

Python 3.13.5, local `unittest`:
**12/12 pass** (five RF geometry and seven held-out evaluation checks).

| File | Git blob SHA-1, independently matched local `git hash-object` |
|---|---|
| `rf_link_geometry.py` | `7009f1801b1fce72d599fbe53367db4f143a3d28` |
| `test_rf_link_geometry.py` | `aaaed552f726b7f3714b7ed6318629a5ed6dfcc9` |
| `rf_pilot_evaluator.py` | `3ed96b70c8b8569424480c0ba12940d07ee8266f` |
| `test_rf_pilot_evaluator.py` | `d8cfc34afb0651b2351c250815c05bcf84239d51` |

One initial test caught an origin-mismatch validation issue
(test mixed-synthetic-vs-real input triggered ground-truth failure
first). The test constructed a valid manual ground-truth value
before asserting mixed-origin rejection; rerun 12/12 passed.
A second semantic safety improvement forbids synthetic fixture
`pilot_gate=PASS`; it now returns
`NOT_APPLICABLE_SYNTHETIC_FIXTURE`.

Output fingerprints:
- `geometric_feasibility.json` SHA-256
  `262cd1e4c01ef7ce84427f4a17ee545443a889a23e87b4b39db0d12e8181e7ea`.
- `synthetic_evaluator_contract.json` SHA-256
  `8cffdd30f6a46f49f268d6597c7fc3f95c5dac9473181f82853ae61c84e56841`.

The toy test fixture deliberately encodes each class in two
CSI-named numerical columns, causing perfect **synthetic** CSI
macro-F1=1.0 and RSSI-only macro-F1≈0.067. This is evidence
only that the evaluation code computes metrics as intended.
It says **NOTHING** about actual Wi-Fi hardware performance
and should not appear as a detector result in an exhibition.

## Byte preservation

Verified local ZIP: **10,361 bytes**, eight members, CRC
`testzip() is None`, SHA-256
`634a331348645c16b191df8c8956b52a465c4a6824a6770301bb52450e3c4158`.

Uploaded and confirmed on Google Drive, `03_REPRODUCIBLE_EVIDENCE`:
https://drive.google.com/file/d/17zaQUPxzMo8VyYEqE5mEMLGzeswcLd3s/view?usp=drivesdk

Drive metadata readback confirmed filename, folder ID
`182v-EmB9Z6ylmUrbeOBiPchCg-NyEsmz`, MIME `application/zip`
and exact 10,361-byte reported size. The remote ZIP was
**not re-downloaded and independently hashed**. Therefore
remote-byte cryptographic equality remains unsealed.

## Status and hard next gates

- **SUPPORTED:** geometry arithmetic, code reproducibility,
  fair baseline/provenance metric implementation, bounded
  prior-art audit, a falsifiable classroom experimental protocol.
- **UNTESTED:** CSI signal acquisition on available school
  hardware, stationary metal presence detection, physical
  separation of the two RF sites, cross-placement robustness.
- **NOT CLAIMED:** 'camera-like Wi-Fi image reconstruction',
  person or pedestrian pose detection, any field vehicle
  counts, certified safety, executable road signal control
  or actual green-delay improvement.
- **CONTINUE in parallel:** existing T2 simulator and
  information-value theory; do not silently import synthetic
  RF fixture performance as measured observation noise.

No GitHub Actions or `github-actions[bot]` contributions were
made. K047 real-world holdout is sealed. No procurement or
student roadside testing has been authorized.
