# T2 D42-L2 — 2026-11-10 literature correction and aggregation gate

**Status: VERIFIED ARITHMETIC / EMPIRICAL STOPLINE HOLD.** This revision does not change DLR raw files or publisher counts.

## Frozen-data numerical check

Source: 2023-09-24 12:00–12:45 UTC (DLR UT v1.3.1), frozen D42 per-approach per-bin L1 discrepancy table; 12 approach-window keys × 8 bin widths = 96 rows.

1s=300, 2s=162, 5s=124, 10s=78, 30s=60, 60s=54, 300s=40, 900s=40. Signed total excess is 40 counts, not 40 independently validated extra vehicles.

**Conditional theorem.** With a *nested, aligned* partition, the coarsened L1 discrepancy cannot exceed the finer L1, by applying the triangle inequality `|sum_i d_i| <= sum_i |d_i|` within every aggregated cell. The statement is **false for arbitrarily chosen, nonnested bins**: in the 12:30 window, East approach, the real frozen table shows 2-second L1=7 but 5-second L1=9. This is **not** a contradiction: 2s does not divide 5s, so their partitions are not refinements.

The 1-second 300 decomposes into signed excess 40 and a 260-count balanced bin discrepancy; `(300-40)/2=130` is a *net count-pair equivalent*, **not** 130 identified vehicles with misplaced timestamps.

Execution: 7/7 tests verified, including frozen-schema assertions, nested inequality, unequal-bin counterexample and negative parity/missing input tests. Reproducible Python code, input, results and manifest preserved in Drive ZIP:
https://drive.google.com/file/d/1fF-FmLsAZcdA22mJnCSq6rcCzOBmRJkh/view
ZIP SHA256: `77c1086c4be00fa7d92a7691b1415fa719e54271b75dfebdcd65fb0b0dac6b30`.

## Literature corpus correction

Four papers previously called missing were actually present in Research OS `00_INTAKE`. Each full text was opened and identified before metadata-only rename/move to `10_PAPERS — Canonical Literature Commons`, preserving each existing Drive ID:

- Schicktanz et al. (2025) DLR-UT dataset: `1UX4FNGPA2GAqcOqwwlJMrQTQabkSYCs4`.
- Aboudolas, Papageorgiou & Kosmatopoulos (2009), store-and-forward network control: `1NIkm1DlEE6Gxoc6KBMUyudkDo2hSq5iS`.
- Aboudolas et al. (2010), rolling horizon queue-balancing QP: `1f-CnZE4jfp-5UeJAmMRZkrVi-VVbQZRE`.
- Lo (2001), cell-based dynamic traffic-signal timing: `1sPW8Ip4atLw34iDucXOQLWpme2GDqqFM`.

**Implication for novelty:** finite storage, spillback-aware network control and dynamic timing are prior art. Our distinctive question must test the credibility of measured stopline/queue events and the propagation of uncertainty to model comparisons and policy selection. Current D42 1399/1409 ±1s heuristic matches are NOT independent ground truth.

Full title-search **missing-candidate** inventory (14 verified-bibliography candidates, not globally proven absent), legal publication links and reading priorities are in the 2026-11-10 Google Doc:
https://docs.google.com/document/d/1hACtEeWhYBIpqTFCAZQmXmd2JkkJTDgktNjXnrI0-TA/edit

Next: publisher bin-phase verification, physical lane centerlines + finite stoplines, D42 60 unmatched record adjudication, D44 viable deceleration + SUMO independent comparison.
