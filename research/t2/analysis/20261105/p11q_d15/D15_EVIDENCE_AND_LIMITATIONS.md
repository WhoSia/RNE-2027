# T2 P11-Q / D15 — 2026-11-05
## Synthetic causality result
A requests-to-enter resource at 47.1500s; occupied resource is released at 47.1625s. Correct earliest entry is 47.1625s. An intentionally flawed tick-end release used at tick-start grants 47.1500s at dt=0.5,0.25,0.125,0.05,0.025; no error at dt=0.01 for this witness. Six local tests including 10,000 random combinations PASS. This is NOT the legacy P10 engine replay. Initial floating-point boundary indexing also exposed an independent numerical precision issue and was changed to Decimal.

## Live observed source-data text
GitHub connector independently re-read source text for six Michigan winter-driving MARWIS CSVs at https://github.com/AD-Assurance-Lab/dataset--winter-driving--main. Counts 933,968,959,1114,958,1035; 5,967 total, 40 columns/file; all timestamp differences >0. Median frame intervals [0.0206933,0.0206912,0.0206912,0.0206976,0.0207009,0.0206878] seconds. Friction values are in 19 consecutive constant blocks, NOT necessarily 19 independent sensor updates. Minimal reported vehicle_speed_mps across trips ranges from -0.1466 to -0.1140; no unilateral sign correction. File upstream Git blob SHA1 IDs agree with archived N audit. Source CSV original bytes have NOT been locally verified against SHA256. No source license re-distribution decision.

## Jinju
Official https://www.data.go.kr/data/15152135/fileData.do describes public sample 10 days, 10,000 rows and 2023-25 scope; per-lane traffic-type fields are textual, up to 6 lanes with intentional blanks, download not obtained in this execution. NO observed row-level statistics, independent dataset hash, or site-specific signal timing claimed.

## Research gates
(1) Independently acquire Jinju original CSV, SHA256, encoding, timestamps, units, lane-quantity text tokens, duplicate observation and date-split.
(2) Run original P10 vehicle 1/8 counterexample on untouched engine with verified code state.
(3) Matched SUMO and inD map+tracks external validation.
(4) Policy optimizer P12 frozen until physical/time gates passed.
