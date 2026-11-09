# D42 — 2026-11-10 stopline candidate negative gate

**Scientific verdict: NOT VALIDATED.** This audit is designed to *fail closed* rather than force agreement with the published 436 movement counts.

## Verified input
- DLR UT v1.3.1 vehicle trajectory CSV, 2023-09-24 12:00–12:15 UTC; 51,209,266 bytes, SHA-256 `5504d37534fd12e95a9e1b019de18f504a2d668dcf564392bb169d42ab42550e`.
- OpenDRIVE map 820,847 bytes, SHA-256 `256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4`.
- Publisher-provided metadata 32-movement volume cells sum to 436; this is NOT the count of 636 tracking IDs.

## Exploratory candidate method
1. Select OpenDRIVE `signals/signal[type=294]` (7 entries, 6 unique sign IDs).
2. Evaluate the line/arc `planView` reference pose at sign `s`.
3. Treat the **infinite reference-plane normal** as a hypothetical gate with ±16 m lateral width and ±6 m longitudinal extent.
4. For consecutive 20 Hz observations of each ID, count signed crossings with time gap ≤75 ms and absolute projected velocity ≥1 m/s.
5. Do not identify physical lane segments, valid signal heads, route movements or traffic-control violations.

Result: 821 candidate forward crossings, 845 candidate reverse crossings. These totals can include opposite-direction flows, overlapping gates and repeated crossings; neither total is a valid independent reproduction of the publisher's 436 center-stopline crossing events. `signal id=300607` appears on two distinct roads; two sign elements are on junction roads, further increasing overlap risk.

## Tests / reproducibility
- Independent local code + eight synthetic tests: 8/8 PASS; no field agreement.
- Source code (GitHub): `research/t2/analysis/20261110/d42/d42_stopline_preliminary.py`, synthetic tests alongside.
- Source-preserving reproducibility ZIP (Drive): https://drive.google.com/file/d/1yZP75wtqjjBR3ndvBmK3jnV8D8xUdk4G/view — SHA-256 `08673bf0f6913adef4ffe082d466025dccd057cf93901064ed7648c270db79a8`.
- Derived candidate CSV (Drive): https://drive.google.com/file/d/1iYvsGu5Cw6n1WwQKxuX8gpLNlh4jqnNN/view.

## Mandatory next gate
Recover actual lane width, direction, and permitted movements from OpenDRIVE topology, **physically finite** stopline segments, tracking ID re-use, signal-head ID 1–30 mapping to 32 movement labels, and preserve ambiguous/unknown cases. Avoid fitting gate geometry using the target count 436 and then claiming independent validation. Evaluate on independent time windows when possible.

No SUMO run or signal policy field-effect claim is made.
