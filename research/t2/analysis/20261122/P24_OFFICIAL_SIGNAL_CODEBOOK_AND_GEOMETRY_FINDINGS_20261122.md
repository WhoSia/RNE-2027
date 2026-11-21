# T2 P24 — Official DLR-UT v1.3.1 signal semantics and geographically referenced signal IDs

**Date:** 2026-11-22 KST. **Verdict: ACCEPT the actual codebook-to-30-live-ID mapping; PARTIAL signal location coverage (26/30 IDs); HOLD controlled-lane and policy interpretation.**

## Official version-matched source

The original **DLR-Urban-Traffic-dataset_v1-3-1_documentation.pdf** was downloaded from the existing Drive DLR-UT v1.3.1 inventory, file ID `1gUqUJEAGtXw06RjQCLbBoJ0k-pcee5Uq`; exact PDF SHA-256 `3c733b677ee63fd2cb282946f415f649d23954ac420d5bc37e0af545f7293849`. The real traffic signal CSV for **2023-09-24 23:30–23:45 UTC** was read and verified against SHA-256 `95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c`. The official v1.3.1 PDF's Figure 1 and Tables 3–4 were inspected; the v1.2.0 legacy PDF is useful as corroboration but is **not substituted** for the exact owned v1.3.1 version.

**Research genealogy correction:** The existing P23 official DLR signal-codebook study had already decoded all ten states and separated vehicle/pedestrian-warning signal purposes using this source. P24 independently cross-checks that prior result and **adds 35 physical coordinate rows / 26 located IDs, four explicitly missing IDs, and a traceable 869-transition matrix**. Do not count the official state decoding again as an entirely new discovery.

## Exact official code semantics

| Original state code | DLR v1.3.1 Table 4 meaning | Observations in 15min |
|---|---|---:|
| 1 | off | 604 |
| 3 | red | 20,924 |
| 4 | red + yellow | 128 |
| 5 | green | 4,680 |
| 7 | yellow | 339 |
| 9 | flashing yellow | 295 |
| **Total** | | **26,970** |

Table 4 also formally describes code 0 as status unavailable, 2 as a stop-required state, 6 as green with protected movement allowed and 8 as yellow with protected movement allowed. Those codes were **not observed** in this 15-minute sample. Code numbers are factual sensor observations; they do not automatically identify which road lane has legal right of way.

The 30 signal-ID time series yielded **869 observed changes**. The observed state-transition matrix (when adjacent 1Hz readings differ) is:
- 3→5: 171; 5→3: 168
- 3→4: 128; 4→5: 127
- 5→7: 127; 7→3: 127
- 9→1: 11; 1→9: 10

A direct 3→5 or 5→3 transition in sampled data **does NOT demonstrate a physical signal skipped red/yellow clearance or had an unsafe controller schedule**. The 1Hz series can miss intermediate state changes, and different signal-head types may have different operational sequences. No real signal safety statement is inferred.

## Critical physical-coordinate result: Table 3

The official v1.3.1 **Table 3**, pp. 12–13, includes **35 physical coordinate rows for 26 distinct signal IDs**. Some signal ID labels appear at more than one pole position. Figure 1 on p.12 shows approaches and includes all 30 IDs, but **Table 3 has no coordinate entries for IDs 10, 11, 12 or 13**, even though all four are present in the raw signal readings. Thus:
- **26 / 30** live signal IDs have at least one official Easting/Northing position.
- **4 / 30** live signal IDs are currently unpositioned by the source coordinate table and must not be silently imputed.
- Coordinate points are in **UTM zone 32** consistent with the real trajectories used by P23. A signal's position near a road or track is **not proof** of its controlled lane or stopline; Figure 1's approach/vehicle-vs-VRU labels and any manufacturer signal-head mapping must be independently combined.

This partially resolves the P23 geospatial-alignment blocker: the unrelated 7 `road/signals/signal` OpenDRIVE static elements and 30 real-time CSV IDs cannot be joined by numeric equality, but the official supplementary PDF supplies a **separate, authoritative physical coordinate table for 26 of the 30 real-time IDs**. The remaining four remain unresolved.

## Distinct signal-purpose groups (cross-checked with earlier P23)

The publisher Figure 1 and already committed P23 split **IDs 1–9 as motorized traffic heads; 10–29 as bicycle/pedestrian signals; ID 30 as a special warning device**. All 9 vehicle-facing signal IDs have official coordinate records (18 physical position rows); 16/20 VRU signal IDs have records (16 rows), while IDs 10–13 are missing, and warning ID30 has one point. The spatial source therefore has **9/9 motor, 16/20 VRU, 1/1 warning heads positioned** at the ID level. The color and signal-purpose classification from prior P23 is not novel to P24; the coordinate completeness and missingness are. The source still does not tell us which exact lane or crossing movement each signal controls.

## Code/execution and verifiability

- [Source](p24_dlr_official_signal_codebook.py): SHA-fail-closed reader calls `pdftotext -layout` on the exact v1.3.1 PDF, extracts Table 3 official 35 Easting/Northing point records and Table 4 all 10 code definitions; then checks the exact owned CSV for all 30 IDs, unknown states, duplicate per-ID timestamps, counts and transitions. No invented map matches or real road control.
- [Seven tests](test_p24_dlr_official_signal_codebook.py) all **PASS** with the real original PDF and CSV: PDF state semantics, 35-coordinate/26-ID census, exact 30-ID code histogram and 869 changes, four missing physical IDs, SHA mismatch veto, wrong-version veto, truncated-PDF veto, and no incorrect lane-meaning claims. Local standard-library Python 3.13.5; external `pdftotext` command.
- [Compact machine-readable receipt](P24_DLR_OFFICIAL_CODEBOOK_SUMMARY_20261122.json), exact production source Git blob `0e5edb4884b9385eb778f71222270249aaebcf47`, test Git blob `5dfe96f6e74fec4919fe8975628ce957d1c12cb6`. Both checked against GitHub `main`.
- Full version-locked result JSON with **all 35 coordinate rows** is separately packaged in the conversation artifact; its SHA-256 is `d48376cf8958764e567b75b97b38307be799934ab7d04446775dafd9d727c3a1`. Unit test log SHA-256 `39f597d8bcd2b3b6b8e16f4b570edc795298960ecc97631930a296727158bb6e`.

## Research direction

Next **P25** should freeze a small set of traffic movement paths (from the existing official 1-second crossing bins) **before** connecting measured signal-head coordinates to movement groups. Compare the official Figure 1 mapping with OpenDRIVE lane geometry; report ambiguity explicitly, particularly for IDs 10–13 and repeated pole locations. The independent metric should be observed stopline-crossing timing and per-vehicle trajectories, not simply proportions of green samples. Only then construct separately specified SUMO geometry and compare empirical vs simulated discharge/queue dynamics.

The GitHub `main` source registry and 20261122 research log record this finding. No SUMO execution or observed real-road policy intervention has occurred. K047 remains sealed; large CIM archive remains unlocated; INTERACTION TC/DR files were downloaded to the user's computer but not found in the accessible Google Drive custody folder at the previous check; no GitHub Actions/bot.
