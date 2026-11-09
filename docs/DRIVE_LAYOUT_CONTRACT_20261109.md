# R&E 2027 — Drive Layout Contract (2026-11-09)

## Provenance

Restores 2026-10-30 chat decision ("code and research notes mixed", no spider-like directory tree) and the Drive [START HERE](https://docs.google.com/document/d/1TdenHgyCjQOGHf75tJyR49Jrt2dteutkygHGEeAZSF4/edit). A full migration receipt was recorded in the [2026-11-09 research log](https://docs.google.com/document/d/1f0VRscBOmX9-CzpyFH_bPumCmAZu5jHeDOKS2E80_S4/edit).

## Mandatory single sources of truth

- **Executable code and tests:** GitHub `WhoSia/RNE-2027` research branch; GitHub Actions[bot] contributions forbidden.
- **Human reasoning:** [02_RESEARCH_LOG](https://drive.google.com/drive/folders/15HIj9OU7e63K2kuVnxGJY00nxGsmNODZ). Each day folder contains Google Docs only; *never* create per-D-number source-code or ZIP directories there.
- **Immutable observed records:** [01_ACTIVE_T2/02_DATASETS](https://drive.google.com/drive/folders/1s_n1K4_YzfZqxuBXRITN2l0CjJ4a-IyW); organize by source/provenance and RAW/DERIVED, not by day of upload.
- **Derived measurements:** [02_DATASETS/40_DERIVED](https://drive.google.com/drive/folders/1pR7cpMnQm0iB7Xzj5u5JYd6XTVQFhmYX). Never overwrite original; cross-reference source IDs, transformations and code SHAs.
- **Reproducibility evidence:** [03_REPRODUCIBLE_EVIDENCE](https://drive.google.com/drive/folders/182v-EmB9Z6ylmUrbeOBiPchCg-NyEsmz); `10_RELEASE_BUNDLES` for ZIP, `20_VISUAL_ARTIFACTS` for HTML/PDF. Preserve sealed SHA and source receipt.
- **Original publications:** Research OS `10_PAPERS`; do not duplicate PDFs inside R&E. Keep citations and reading decisions in Drive.
- **Legacy original test folders:** [90_ARCHIVE/T2_LEGACY_UNIT_FOLDERS](https://drive.google.com/drive/folders/1n-wq8VSNTZ1J1ONztAGzpZPahQXrD762), grouped by archival date. Moving an old code folder there does not imply scientific invalidation, only removal from active browsing.

## DLR UT 1.3.1 original

Raw and publisher files at immutable [DLR UT 1.3.1](https://drive.google.com/drive/folders/1MgVtPHh8UKMuv0hNhUQLRSmP_oNLN_FX), inside `02_DATASETS/20_OBSERVED — International`. Upload structure is native DLR dataset tree; 96 CSVs each in `trajectories`, `traffic_lights`, `traffic_volume`, `weather`, `road_condition`, `air_quality`; 4 XOSC files; 1 OpenDRIVE map. Folder traversal showed 3,359,579,569 total listed bytes. This is **not** a cryptographic attestation of all source files.

The original ZIP (~463.4MB) cannot pass Drive MCP fetch's 268,435,456-byte limit; individual files can. The three audited XOSC XMLs have separate SHA256 records in D42, but raw CSV file-by-file hashing and signal/vehicle time alignment remain outstanding.

## Migration / verification

- 20261105: 23 Google Docs returned to day root, 28 unit directories archived.
- 20261106: 27 Google Docs returned to day root (11 direct, 16 nested), 7 unit directories archived.
- 20261108: 1 Doc at day root, 6 unit directories archived, 1 ZIP moved to evidence.
- 20261109: 3 Docs at day root, 5 unit directories archived, 2 ZIP moved to evidence; DLR originals moved to immutable data lake.
- 20261030–31: legacy empty / output folder trees archived.
- 20261101–04: 45 loose ZIP/HTML/PDF moved to evidence and 9 loose CSVs moved to derived. 3 existing ZIPs from `40_DERIVED` moved to evidence.
- Cross-project RITHM markdown was moved to `NON_T2_MISFILED_HOLD` for review, not deleted. Prevent repeat ingress by fixing the source uploader's folder routing; do not periodically create more R&E subfolders.
- No file bytes modified; Google Drive moves/renames preserve file IDs and current sharing links.
- At verification, date-folder direct children were only native Google Docs. Empty dated folders are left intact rather than inventing retrospective notes.

## Forward workflow

1. Research question and decision → Google Doc in today's existing `02_RESEARCH_LOG/YYYYMMDD … 사유` folder.
2. Source acquisition → appropriate immutable dataset source folder, byte receipt/catalog entry.
3. Analysis → GitHub commit + in-memory/local test; persist needed derived outputs in `40_DERIVED`.
4. Auditable milestone → versioned ZIP or visual artifact to `03_REPRODUCIBLE_EVIDENCE` with manifest and checksum.
5. Update START HERE and a single current research ledger with all stable Drive file IDs and exact evidence gates.
6. Before creating a folder, look for an existing location by **asset role**; never create a parallel date-based tree for the same kind of data.
