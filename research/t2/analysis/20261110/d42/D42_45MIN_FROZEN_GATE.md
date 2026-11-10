# D42 / 2026-11-10 — Frozen Gate, 45-minute Reproduction

**Verdict: HOLD (internal consistency, not field truth).** The unmodified OpenDRIVE lane-strip candidate detector and the pre-specified ±1s monotone match were replayed on two successive *new* 15-minute blocks, without tuning thresholds to the publisher count.

## Original source by 15-minute window (UTC 2023-09-24)
| Time | Original trajectory SHA-256 | Signal SHA-256 | Volume SHA-256 | Movement columns |
|---|---|---|---|---:|
|12:00–12:15|5504d37534fd12e95a9e1b019de18f504a2d668dcf564392bb169d42ab42550e|444290f5a29c9f3d767e275a2c87d281614d4ab951cc5a5a7ee9fb8c1bf9efcb|98e4e0a593702188c2d134cef1346cbc7501067c9ad421ddb9e72a1e6d9d1d15|32|
|12:15–12:30|7944c785a77f4198abb09672f79ab97a1a0cc867d8df4a0fdd664b5d3ee9bdc7|9a9bbb2d71b26e535f6dd3d4e3423cbb0a199084233bda7c8ca2bc8e473a9d93|ec4469245af40e5ac938f60d54face45448cde6644ddcd35f67e819b5d2cd426|27|
|12:30–12:45|c1fab0dc4569747049461c7aabc7681d0b90ddfd16c0eb4b3f5bb82e23b6a112|4bf6a223b275fd124a83b079c49e8e22ca1626f54450c6609bde8937c22957a8|4a30e5767f33288d1fe3026ca796ea7c9e1a6447d84117f3eaa510ad6516e1c7|26|

Original files are retained in Drive 01_ACTIVE_T2 / 02_DATASETS / 20_OBSERVED — International / DLR_UT_v1.3.1, **not duplicated in the code/release archive**. All three volume files contain 900 one-second records. DLR documentation section 5.1 explicitly allows varying numbers of movement columns: only routes with detected participants are reported. The old D42 topology parser incorrectly insisted on exactly 32, and failed on new windows. New `d42_multibatch.py` fixes schema assumption while refusing unexpected source labels, negative counts, duplicate columns, and wrong time length.

## Replay results, unchanged geometric gate
| Interval | Publisher count cells | Candidate approach crossings | One-to-one chronological matches within ±1 second | Extra candidate | Publisher unmatched |
|---|---:|---:|---:|---:|---:|
|12:00–12:15|436|446|432|14|4|
|12:15–12:30|475|487|471|16|4|
|12:30–12:45|498|516|496|20|2|
|TOTAL|1409|1449|1399|50|10|

The three temporal windows are all from **one calendar day**. The source and publisher-derived traffic volume share measurement lineage. The matching is only by **inferred origin direction and approximate second**, not verified individual identity, physical stopline geometry, permitted movement, or publisher's 32/27/26 movement-specific classifications. Counts cannot be advertised as a true precision/recall score or an independent external validation.

## Diagnostic failure triage (candidate extra events)
- 12:00–12:15: 14, largest per-track category car 13 / motorbike 1.
- 12:15–12:30: 16, car 10 / motorbike 4 / truck 2.
- 12:30–12:45: 20, car 19 / van 1.
- Of 50 extra candidate events, **zero had a nearest observed source frame marked interpolated**. This does not exclude tracking gaps, mixed classifications, wrong geometry, identity reuse or publisher selection conventions.
- Source tracks with the event within 1 second of track start/end: 2+1+4=7; this diagnostic alone is not a cause attribution.

## Traffic-light data freshness
Observed signal timestamps in successive blocks: 897, 899, 895; nominal missing seconds 3, 1, 5 = 9 across 45 minutes. Do not silently forward-fill across them into an asserted true signal color. Traffic head-to-movement mapping remains unverified.

## Tests and release
- Prior 36 geometric, topology and temporal-contract tests + 7 changing-schema negative tests = **43/43 locally executed PASS**.
- Local sealed replay ZIP `RNE_T2_D42_20261110_45MIN_FROZEN_GATE.zip`, 69,346 bytes, SHA-256 `d0b0f6a7fee18eed16ff2b37fa1cb61f2943f0840583d6d59f6489d704173aa8`, containing the exact executed code, reports, profiles, all derived candidate event tables, raw input SHA manifest. Original multi-MB DLR sources are *not* embedded.
- Note: the local ZIP is a user-visible conversation artifact at present, **not yet verified uploaded to Drive**. Github `d42_multibatch.py` and `test_d42_multibatch.py` committed separately. Research source notes: 20261110 Google Doc.

## Next scientific gate
Determine finite physical lane stopline and downstream route using laneLink connection topology. Associate 30 traffic-head IDs to publisher movement designations, separately confirm publisher event accounting and evaluate adjacent trajectory windows. Until then, no claim of queue length, independent SUMO validation, sensor noise distribution, policy superiority, or prize-level field effectiveness.
