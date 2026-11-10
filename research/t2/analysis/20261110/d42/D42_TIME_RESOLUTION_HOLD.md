# D42 2026-11-10 — Exact-second vs ±1s temporal association

The previously frozen three DLR UT v1.3.1 windows (2023-09-24 12:00–12:45 UTC) have publisher movement count-cell total **1409** and 1449 approximate approach reference-plane crossing candidates. These are **not verified lane-specific stopline crossings**. Comparing approximate candidate times to publisher's 1-second movement-count timestamps produces:

| Interval | Publisher counts | Candidates | Within-approach chronological ±1s matches | Same integer-second count-bin overlap |
|---|---:|---:|---:|---:|
|12:00–12:15|436|446|432|395|
|12:15–12:30|475|487|471|426|
|12:30–12:45|498|516|496|458|
|TOTAL|1409|1449|1399|1279|

Same-second overlap is `sum_{approach,integer-second} min(candidate_count, publisher_count)`; candidate second is **hypothetically** `floor(interpolated crossing timestamp)`. Publisher counting bin phase and geometry are not independently established; therefore 1279 is *not* a new error-rate truth, just a stricter diagnostic. ±1s chronological matching can pair different physical objects, and its 1399 count cannot be called validated agreement. Original ±0.5s chronological matching: 283,304,315 = **902** across the same three windows. Timing gate width materially changes the apparent match statistic.

The earlier field-data structural incompatibility is also confirmed: active movement columns differ by window **32, 27, 26**. The publisher documentation allows absent route columns in no-detection windows. New `d42_multibatch.py` accepts variable movement columns and rejects unrecognized headings/negative counts. The original 32-column assertion remains in the sealed older baseline code; do not silently rewrite original history.

Signal-head observations comprise **897, 899, 895** nominal seconds within three 900-second windows, meaning **9 missing nominal signal observations** in aggregate. Unknown actual state in a missing second is preserved.

Across the three windows, **50 candidate excess and 10 publisher excess** entries remain unmatched within ±1s. For these 50 extra candidate events, the nearest source trajectory frame had `interpolated=True` in **zero** instances; seven events were within 1 second of a track endpoint. Neither statistic establishes a causal explanation.

New exact-bin tests 7/7, existing tests 43/43: **50/50 locally executed PASS**.

Latest reassembled release: `RNE_T2_D42_20261110_45MIN_FROZEN_GATE_V2.zip`, 72,159 bytes; SHA-256 `b5118116ec8c5c8915f149bbdd22da1ae29e89ea5ad27939ba690c0d6d9199c0`. Exact executed source, inputs manifest, source hashes, derived event CSV and tests are in the release ZIP; raw source DLR files remain in the Drive immutable data lake. **ZIP currently exists as a verified sandbox conversation artifact, not a confirmed Drive upload**.

The central GATE remains HOLD: certify real finite lane-specific stoplines and 30 signal-head-to-movement links, rebuild publisher center-crossing events without fitting to counts, then independent simulator and external days. No signal-policy field improvement is claimed.
