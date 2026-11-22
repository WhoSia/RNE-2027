# T2 P34 — Real publisher stopline-volume bins versus naive tracked-object presence

**2026-11-23 KST. Exploratory field-side negative control, not an independently held-out detection model.** This continues P33's 30-head common signal-sampling gap using the third authentic original DLR-UT v1.3.1 traffic-volume metadata CSV.

## Scientific question and baseline

The [before-full-execution P34 protocol](P34_OFFICIAL_VOLUME_TEMPORAL_BASELINE_PROTOCOL_20261123.md) explicitly documents that preliminary data inspection had already revealed a low co-occurrence precision. No posthoc discovery is relabeled prospective.

The official DLR Zenodo release [v1.3.1](https://zenodo.org/records/20919480) says traffic-volume metadata are **extracted from raw trajectory data**. Thus these two exports are **not independent detector modalities or externally independent ground truth**. The publisher's 1s movement-positive bins are a useful *reference label* only for internal consistency, subject to shared-processing and route/stopline definitions. They are not validated same-vehicle identity matches.

Input SHA256 (existing exact publisher originals, 2023-09-24 23:30–23:45 UTC):
- `traffic-volume_230924-233000_230924-234500.csv` — `00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798`, 893 records ×12 movement labels.
- `trajectories_230924-233000_230924-234500.csv` — `6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50`, 8,624 object observations, 37 tracked IDs.
- `traffic-lights_230924-233000_230924-234500.csv` — `95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c`, 26,970 signal observations, 30 distinct heads.

## Experiment executed

For each official volume timestamp t, define `reference_positive(t)` iff *any* of the twelve publisher movement columns is 1. Define the deliberately weak baseline `predict_positive(t)` iff any tracked-object raw timestamp falls into the 1-second half-open interval **[t,t+1s)**, UTC. This test intentionally ignores lane, movement, class, velocity and stopline. The same registered 893 bins are tested irrespective of whether object tracking exists.

| Binary 1-second event measure | Actual result |
|---|---:|
| Published positive movement-channel bins | **17** |
| Unique positive 1-second bins | **17** |
| Published negative 1-second bins | **876** |
| Tracked-object presence positive | **322** |
| True positives against published bin labels | **17** |
| False-positive *bin labels relative to publisher export* | **305** |
| False negatives | **0** |
| True negatives | **571** |
| Precision | **17/322 = 5.2795%** |
| Recall | **17/17 = 100%** |
| Specificity | **571/876 = 65.1826%** |

**Interpretation:** All 17 publisher-positive seconds have some tracked traffic participant present, but an active track is neither a direction-specific crossing nor a verified exact-identity match. In **11/17** positive seconds there are multiple possible tracked IDs; the positive-bin candidate-count distribution is **6 bins with 1 candidate, 7 with 2, 1 with 3, 2 with 5, 1 with 6**. Even the six singleton bins do **not** establish actual crossing-vehicle identity without publisher per-movement line geometry.

A naive proxy has **305 false alerts against the published volume-derived labels**. Because the publisher's labels derive from trajectories, this is not evidence that a sensor independently detected 305 errors, nor proof of 305 physically absent crossings. It shows **temporal co-occurrence alone cannot serve as the crossing-event detector**.

## Time-offset sensitivity, including null controls

Without optimizing the shift, assign every track timestamp to a 1-second bin after an artificial shift of −2, −1, 0, +1 or +2 seconds. Compare against the same 893 published bins:

| Shift of track timestamp | TP | FP | FN | TN | Precision |
|---|---:|---:|---:|---:|---:|
| −2s | 17 | 303 | 0 | 573 | 5.3125% |
| −1s | 17 | 304 | 0 | 572 | 5.2960% |
| 0s | 17 | 305 | 0 | 571 | 5.2795% |
| +1s | 16 | 305 | 1 | 571 | 4.9844% |
| +2s | 16 | 304 | 1 | 572 | 5.0000% |

The precision problem persists under these small diagnostic shifts. This is a **timing robustness descriptive check**, not a randomized negative control or evidence of identification under all offsets.

## Joint P33 common sampling-gap audit

The exact P33 synchronized observation gap is **23:31:44.010Z–23:31:46.014Z**, a 2.004s interval seen by all 30 heads; signal IDs **12,20,21** change sampled code between endpoints. **40 tracked-object samples from one object ID** occur strictly within the gap, while *three official 1-second bin intervals* (beginning at seconds 44,45,46) overlap the gap and have **zero** publisher-positive volume indicators. This does **not** prove no actual crossing occurred, and the tracking samples cannot reconstruct a missing signal-state sample. Head↔movement correspondence remains unverified.

## Geometry blocker confirmed by inspecting original OpenDRIVE

Exact original `bs-inner-ring-road-ut.xodr` SHA256 `256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4`: OpenDRIVE XML contains road/lane plan geometry, **7 static `signal` elements**, but **zero explicit `object` stopline elements, zero elements whose tag contains 'stop', and zero `signalReference` elements**. This tag census does **not** prove stopline information is unavailable in the original dataset or figure; it proves that a stopline detector **cannot be certified from an explicit stopline primitive in this inspected OpenDRIVE XML alone**. Do not invent a directional crossing line by optimizing toward the 17 positive bins.

**Construct-validity dispute:** Do not infer a driver's legal green phase or a queue cause from the existence of a track. The official CSV crossing label is aggregated to one-second movement bins, whereas trajectories have 50ms samples; neither provides vehicle↔movement direct identity or exact continuous stopline contact in current checked sources.

## Execution, tests and custody

- [SHA-fail-closed Python stdlib runner](p34_official_volume_overlap.py) — no new dependency or runtime; Research OS Polyglot rule is to use the smallest coherent implementation.
- [14 integration/adversarial tests](test_p34_official_volume_overlap.py): **14/14 PASS** on original three publisher CSVs and malformed/fake fixtures, including source SHA drift, missing zone, duplicate 1s bin, duplicate signal head, invalid binary movement indicator, asymmetric time shifts, common gap and exact 17/322 confusion.
- [Full reproducible 893-bin aggregate JSON](P34_OFFICIAL_VOLUME_OVERLAP_RESULTS_20261123.json), original output SHA256 `77efa960815049b0a3c89602eef5d4cdf930674bf36ea8cac8cf8ca463e1f968`. Exact 1-second movement columns are aggregated without rewriting source files.
- Test transcript SHA256 `d32639112c361d01fd4131a43060efd8fa2ba3d0b6f2dc826f8082d6f9a87182`.

```sh
python p34_official_volume_overlap.py /data/traffic-volume_230924-233000_230924-234500.csv /data/trajectories_230924-233000_230924-234500.csv /data/traffic-lights_230924-233000_230924-234500.csv p34_results.json
python -m unittest -v test_p34_official_volume_overlap
```

## Reviewer decisions and return edge

- **Origin judge:** This is one concrete real-data benchmark floor, not a new T2 policy mechanism result.
- **Source-dependence auditor:** Publisher explicitly says volume derived from raw trajectory data. Correct claim from “independent validation” to “shared-source export consistency benchmark.”
- **Causal skeptic:** Co-occurrence is not correspondence. Keep no movement-control attribution, no field signal planning.
- **Adversarial benchmark auditor:** all 17 publisher-positive seconds have a track, but 305 proxy alerts relative to publisher labels; timing shifts do not rescue discrimination.
- **Cost-information auditor:** **STOP** adding time-metadata checkers. Next work must recover a trustworthy *stopline/movement geometric definition* from publisher sources or construct explicitly estimated, held-out, source-dependent detector geometry without claiming official ground truth. If unavailable, shift to independent SUMO/real-scene comparison instead of further proxy tuning.

EXPLANANDUM: Identify source-justified stopline crossing event evidence from measured tracked traffic.
AUTHORITY CEILING: Publisher-export temporal co-occurrence, **not** independent stopline detection and **not** causal signal control.
CORE/ENABLING/FORK: ENABLING with real three-source contact, not a core intervention demonstration.
RETURN EDGE: map verified stoplines/movement paths, then report 1Hz crossing event precision/recall and independent movement-level comparison.
DEBT: 1, cannot spend another stage on empty metadata.
