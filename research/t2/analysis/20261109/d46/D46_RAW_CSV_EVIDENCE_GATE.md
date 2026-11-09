# D46 — Direct raw DLR 20 Hz / 1 Hz / stopline-count audit, 2026-11-09

## Ground truth and source scope

**One observed 15-minute window:** 2023-09-24 12:00:00–12:15:00 UTC, DLR Urban Traffic v1.3.1, CC BY-NC-SA 4.0. Original published CSV files were fetched byte-for-byte through the connected Google Drive; only **derived aggregates and original analysis code** are committed here.

| Publisher CSV | Bytes | SHA-256 |
|---|---:|---|
| `trajectories_230924-120000_230924-121500.csv` | 51,209,266 | `5504d37534fd12e95a9e1b019de18f504a2d668dcf564392bb169d42ab42550e` |
| `traffic-lights_230924-120000_230924-121500.csv` | 1,013,056 | `444290f5a29c9f3d767e275a2c87d281614d4ab951cc5a5a7ee9fb8c1bf9efcb` |
| `traffic-volume_230924-120000_230924-121500.csv` | 81,393 | `98e4e0a593702188c2d134cef1346cbc7501067c9ad421ddb9e72a1e6d9d1d15` |

Drive publisher source folder: https://drive.google.com/drive/folders/1MgVtPHh8UKMuv0hNhUQLRSmP_oNLN_FX

## Executed original-data results

- Raw tracks: **299,053 rows, 636 observed IDs, 18,000 unique timestamps**; per-ID timestep consistently 0.05s. Duplicate (ID,timestamp)=0; null cells=0; consecutive >0.1s gaps=0.
- Reported `interpolated=True` on 2,673 rows (**0.8938%**). Minimum sum of the six reported object-class probabilities **0.822**; do not assume normalization or unique actual vehicle per ID. Reported speed max 20.051m/s; displacement-implied speed max ~20.0864m/s. Per-ID jumps >5m: 0.
- Previous D42 12:00–12:15 XOSC contained **299,053 vertices**, exactly the raw CSV row count. A row-count identity is not an independent observational validation; the representation is derived.
- Signal: **26,910 rows** = 897 time samples for each of 30 heads. Three ~2sec shared time gaps: 12:04:33.982→12:04:35.995, 12:09:33.986→12:09:35.986, 12:12:53.982→12:12:55.981 UTC. States observed as integers `1,3,4,5,7,9`. **DO NOT infer red/green meaning without official enum.**
- Stopline counts: **900 one-second rows**, 32 movement columns; sum of event-count cells **436**. Publisher README says a road-user *center* crossing a lane stop line defines an event. **436 is NOT established as 436 unique real vehicles.**

## Conservative temporal alignment — experiment only

For signal head #1 solely as an example of source timestamp observability, join the previous measurement at or before each of 18,000 distinct vehicle timestamps. Mark as UNKNOWN when no earlier observation or last sample age exceeds cutoff.

| allowed previous-sample age | UNKNOWN timestamps / 18,000 |
|---|---|
| 0.50s | 9,040 (50.222%) |
| 1.05s | 94 (0.522%) |
| 1.50s | 50 (0.278%) |
| 2.05s | 20 (0.111%) |

**Threshold sensitivity is not sensor failure probability.** There is no verified geometric or causal mapping from head #1 to any particular moving object or stopline event. Do not use this toy join to claim signal-compliance or policy performance.

`signal_alignment.py` and `test_signal_alignment.py` give the conservative UNKNOWN-preserving rule and 12 local-passing tests. `raw_window_audit.py` is the reproducible pandas/numpy source audit.

## Gate and publication constraints

**Done:** exact raw source files read, three SHA-256 seals, descriptive schema/spacing/track interpolation checks, timestamp-uncertainty sensitivity, 12 tests.

**HOLD:** official state code semantics, signal head↔movement and OpenDRIVE lane↔stopline mapping, trajectory fragmentation/boundary censoring, counted center-crossing independent reproduction, SUMO executable comparison, T2 calibrated physics, policy-rank inference.

Durable Drive sealed analysis ZIP:
https://drive.google.com/file/d/1i4lgDLzr0tddD_oIPEKxAIGBgCpYEl0U/view
SHA-256: `bc3f480d3f38aed71bf2f4b204fa0068cadf38acac1dad50f8a620440e048195`.

Research reasoning stays as a Google Doc in 20261109 김우준의 사유:
https://docs.google.com/document/d/1ng25IRQWeOqyULZJHO7zJSKG86W--Wwv31un7bIkuCk/edit

No original third-party data or full data ZIP added to GitHub; no GitHub Actions invoked.
