# R&E 2027 repository and Drive map

The current T2 code, runnable experiments, and verification tests are on
[research/t2-spatial-fig2-v02](https://github.com/WhoSia/RNE-2027/tree/research/t2-spatial-fig2-v02).
Use this branch for navigation. Link to the tested commit SHA when recording
an experiment, so later branch changes cannot change the cited inputs.

| Looking for | Location |
| --- | --- |
| Project entry point and latest evidence | [START HERE](https://docs.google.com/document/d/1TdenHgyCjQOGHf75tJyR49Jrt2dteutkygHGEeAZSF4/edit) |
| Current claims and methodology | [T2 verification ledger](https://docs.google.com/document/d/10nj0pmvCF4BnJ_9o0wxdHzxLBQ0ZYziRW6KfXP7xwrk/edit) |
| Protected-stage model, policy search, and observation experiments | [Efficiency experiments](../research/t2/efficiency_loop/README.md) |
| Corridor offsets and finite downstream storage | [Offset information protocol](../research/t2/policy/OFFSET_INFORMATION_PROTOCOL.md) |
| Import and validation of observed data | [Jinju receipt](../research/t2/data/20261117_jinju/README.md), [CityArtery receipt](../research/t2/data/20261117_cityartery/README.md), [DLR input contract](../research/t2/efficiency_loop/DATA_ACCESS.md) |
| Original data and derived datasets | [Dataset shelves](https://drive.google.com/drive/folders/1s_n1K4_YzfZqxuBXRITN2l0CjJ4a-IyW), [derived outputs](https://drive.google.com/drive/folders/1pR7cpMnQm0iB7Xzj5u5JYd6XTVQFhmYX) |
| Daily reasoning, decisions, and teammate replies | [Research log](https://drive.google.com/drive/folders/15HIj9OU7e63K2kuVnxGJY00nxGsmNODZ) |
| Published manifests, bundles, and visualizations | [Reproducible evidence](https://drive.google.com/drive/folders/182v-EmB9Z6ylmUrbeOBiPchCg-NyEsmz) |
| Paper originals and project-specific reviews | [Research OS papers](https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP), [T2 reading and field notes](https://drive.google.com/drive/folders/1PszjYiffe8bRxtM6PnYbQHvhC_6gWfky) |
| Superseded records and recovery objects | [Archive](https://drive.google.com/drive/folders/1jpRsGlui6ZISoYnUTA1DEAmBuGZ7xhIH), [branch recovery bundle](https://drive.google.com/file/d/1vF8oDwafQtfhP4Lx29kw0WcMO2A07fNp/view) |

The archived analysis refs ended at
`bd450b87be24bb024fe483e2e2108c6ee82f37a5` and
`ae62d8aa7513c6985bf22343ab0a59f36ae3d406`. Both are reachable from the
current working branch. Cite these commits when discussing the corresponding
historical results. Candidate-topic notes and raw chat transcripts remain in
their existing Drive shelves. See the [Drive contract](DRIVE_LAYOUT_CONTRACT_20261109.md)
for source and output placement.


## 2026-11-21 current T2 source and prior-work transfer

The latest research unit [SF-01 robust sensor-information fusion](../research/t2/analysis/20261121/sensor-fusion/FINDINGS.md) uses Long (2026) decision-time forecast diagnostics, Huang (2025) lane/signal separation, and an explicitly simplified Shafik/Rakha (2025) two-stage queue estimator. [43-test local validation and unresolved 192 physical runs](../research/t2/analysis/20261121/sensor-fusion/VALIDATION_RECEIPT.md). [Executable physics-screen design](../research/t2/physical_transfer_screen.py) is **not** yet a completed physical result. No empty K047 HTML or fabricated field scenes are considered evidence.


## Latest T2 implementation receipt — 2026-11-21

[704 synthetic physical run assessment](../research/t2/analysis/20261121/decision-time-gate/PHYS_192_384_128_FINDINGS.md) consists of original 192-case fixed-geometry screen, 384-case physically time-gated opportunity comparisons, and separately exploratory 128-case geometry sensitivity. Source/test byte fingerprints, 3 original output SHA-256 values and the 21/21 self-contained tested checks are provided in the individual receipts. The paired 48/48/16 cost comparisons are preserved as CSV in Git. **These are not 704 independent field samples or 704 validations of a real controller.** The K047 blank viewer remains retired. Next technical gate: clone the complete traffic microstate at a valid decision time and compare future policies with identical information prefixes, then use prior gap-acceptance and state-estimation work.
