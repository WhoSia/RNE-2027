# D42 — 2026-11-10 uncertainty propagation gate (45 min)

## Scientific status: HOLD — descriptive internal consistency, not external truth

Data: DLR UT v1.3.1, 2023-09-24 12:00–12:45 UTC. Frozen candidate approach crossings from already committed D42 lane-strip program; publisher movement volume from same sensor lineage. No new geometry or matching threshold was calibrated against publisher counts.

### New independent recomputation of error budget
- 1,449 frozen approach crossing **candidates** vs 1,409 publisher volume-cell sum; signed candidate excess **40**.
- 50 candidate and 10 publisher event timestamps unmatched with predeclared ±1-second within-approach greedy one-to-one comparison.
- Six approach road/lane IDs have >1 allowed outgoing road by the actual OpenDRIVE 44 laneLinks; **346 / 1,449 (23.88%)** candidate crossings occupy such topologically ambiguous lane IDs. This is not an error rate: their exit direction needs observed trajectory routing to decide.
- The remaining 1,103 candidate events occupy lanes with a single outgoing *road* according to the map, but are not yet proven publisher-labeled movements.
- Candidate-unmatched incidence: ambiguous lanes 15/346 = 4.34%; other lanes 35/1103 = 3.17%. Descriptive only, with traffic/exposure differences and selection confounding.

### Sum of absolute count differences by approach × fixed time bin
|Bin width (seconds)|L1 discrepancy (count-cell units)|
|---|---:|
|1|300|
|2|162|
|5|124|
|10|78|
|30|60|
|60|54|
|300|40|
|900|40|

For any common bin partition, `L1 >= abs(total candidates - total published) = 40`. The 1-second value decomposes arithmetically as 40 signed excess plus 260 balanced bin deviations, equivalent to 130 *net count transfers across bins*, **not 130 identified common vehicles**. At 5 minutes, temporal allocation differences cancel and only the 40 count excess remains. No physical cause is yet identified.

### Timestamp phase sensitivity — non-identifying diagnostic
Holding the publisher's recorded integer-second bin labels fixed, shifting candidate timestamps by −0.25s, 0, +0.25s gave 1-second L1 values 476, **300**, 862 respectively (summing four approaches × three windows). The phase 0s was the previously frozen choice, not a fitted global clock offset; this experiment shows why time-bin conventions must be certified from publisher documentation.

### Execution / provenance
- Local frozen regression suite 50/50 PASS, new synthetic/data auditing assertions 8/8 PASS; **58/58 executed**.
- Exact executed new analysis code `d42_uncertainty_accounting.py` and `test_d42_uncertainty_accounting.py`, source dependencies, original-derived tables, phase sensitivity CSV and manifest in zip:
  https://drive.google.com/file/d/1Z846HRjNbG93u4SF2PXgN6TEo0GgY5Un/view
- ZIP SHA256 `897dc5bb153b7b0022a9fe2036d9c7812cc47fbd04eb1545e30530716291bed1`; original 9 DLR CSVs remain in the dataset lake and are not duplicated in the ZIP.
- Research Docs: https://docs.google.com/document/d/1fkzetvDIyGTho0wyccceYvFhUvB5ZPtPAMhjmJK9DH8/edit

### Gates before claims
1. Publisher time bin origin and precise stopline convention.
2. Observed track→turn→exit mapping at lane and laneLink granularity (346 candidates currently route-ambiguous).
3. Independently adjudicate 60 unmatched event entries (they are not necessarily 60 different physical vehicles).
4. Measure real lane queues with censorship and then cross-check T2 vs independent SUMO; no traffic-signal improvement or policy reversal has been externally validated.

The exact locally executed source is bundled in the Drive ZIP; this Markdown is a provenance/decision record, **not** a claim the source has been separately mirrored to GitHub.