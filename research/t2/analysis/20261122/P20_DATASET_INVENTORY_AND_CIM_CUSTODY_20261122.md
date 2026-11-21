# P20 Harvest — external datasets, existing Drive inventory, and CIM ZIP custody

Date: 2026-11-22 KST. This is a **metadata-only inventory and acquisition triage**, not a claim of new raw-data downloads or physical sensor validation.

## Shared Drive audit (direct provider reads)

Dataset lake [02_DATASETS](https://drive.google.com/drive/folders/1s_n1K4_YzfZqxuBXRITN2l0CjJ4a-IyW) is organized into `00_CATALOG_AND_LICENSE`, `10_OBSERVED — KR`, `20_OBSERVED — International`, `30_SIMULATION_SCENARIOS — SUMO`, `40_DERIVED`, `90_QUARANTINE_AND_UNVERIFIED`. Source bytes must remain unmodified and distinct from derived simulation results.

| Asset | Verified existing state | Scientific next action |
|---|---|---|
| [DLR Urban Traffic v1.3.1](https://drive.google.com/drive/folders/1MgVtPHh8UKMuv0hNhUQLRSmP_oNLN_FX) | **ALREADY OWNED**: extracted `raw_data/trajectories`, `traffic_lights`, `weather`, `road_condition`, `air_quality`, `meta_data`, `map`; documentation PDF | PRIORITY 1: select matched trajectory/signal-time windows, validate clock alignment and lane mapping. Do not download another giant DLR archive without a missing-file audit |
| [CityArtery](https://drive.google.com/drive/folders/1SV1ocEpo9_x8K3u4WMRsKgffpy1kEHIg) | **ALREADY OWNED**: `CityArtery.zip` ~30.58MB | PRIORITY 2: license/manifest and trajectory schema check before importing, without mutating the source ZIP |
| [USDOT Utah SPaT](https://drive.google.com/drive/folders/1eEVqcnE3GIJ_v55wQA0W83ZZDrIR9O7t) | Folder exists but **EMPTY** | PRIORITY 1 new acquisition: timestamped signal phases/clearance, eventually join to BSM traces; verify time zones, coverage, license before downloading |
| [USDOT Utah BSM](https://drive.google.com/drive/folders/1SgysviNOpJOrA0_qH2boF2tzIR8qS6i6) | Folder exists and was directly listed: **EMPTY** | New acquisition only after SPaT matched date/segment is chosen; trajectory latency and privacy filters |
| [USDOT NGSIM](https://drive.google.com/drive/folders/1NRWD3LwUcFLrxeWR0y2Nm3WGjPNbVnca) | Folder exists but **EMPTY** | PRIORITY 3, mainly vehicle-following headway calibration; less directly suitable for signal phase and turn pocket behavior |
| [SUMO scenarios](https://drive.google.com/drive/folders/1G0-2ZrV8TYyDo2wHzApIDlCn3eypo4xI) | LuST, MoST, DLR scenario folders **ALREADY OWNED** | Before fetching a new city scenario, audit route/edge and version compatibility and the actual SUMO executable availability |

## Newly vetted public candidate sources (not yet downloaded)

1. **USDOT Utah SPaT + BSM** — highest incremental value for P20 because it observes real signal phase/clearance times next to connected-vehicle movements. Official public catalog: https://catalog.data.gov/dataset/traffic-signal-change-and-clearance-interval-pooled-fund-study-utah-spat-data and https://catalog.data.gov/dataset/traffic-signal-change-and-clearance-interval-pooled-fund-study-utah-bsm-trajectories-sampl . We have an empty SPaT folder already, so create metadata and choose a tiny time-aligned subset first.
2. **INTERACTION trajectory dataset** — official maintained dataset location moved to https://huggingface.co/datasets/INTERACTION-dataset/INTERACTION-dataset . Signalized intersection, merging, and lane change trajectories with maps can act as an independent behavior/geometry comparator. It **does not automatically provide aligned signal phase history**, so it is not a substitute for SPaT. License/terms must be checked per release before ingestion.
3. **TUMTraf Intersection / CrossVision** — https://github.com/tum-traffic-dataset/tum-traffic-dataset-dev-kit . Anonymized timestamped multimodal road/intersection observations useful for trajectory/occlusion sensor baseline. Some versions and modalities require registration and larger download. The Drive currently owns only the TUMTraf *paper* under the general paper shelf; owning a PDF is not possession of raw annotated video.
4. **ESPARGOS `espargos-0001`** — https://darus.uni-stuttgart.de/dataset.xhtml?persistentId=doi%3A10.18419%2FDARUS-4352 , CC BY 4.0 dataset of indoor Wi-Fi CSI plus externally recorded reference positions/timestamps. Includes a `static_middle.tfrecords` file (~59.6 MB) and a separate `static_middle_with_person_walking_nearby` condition. Useful for proving a raw CSI decoding/evaluation pipeline can work with a stationary target, but **NOT a real-road or tabletop vehicle traffic model**. Check split by recording session and antenna array to avoid leakage; select only lawful provided public data, no third-party Wi-Fi collection.
5. **Official DLR-UT 1.3.1** — https://zenodo.org/records/20919480 , already owned in extracted form. Official paper https://elib.dlr.de/212925/ documents signal-state and trajectory capabilities; no new mass acquisition justified before aligned-window verification.

## Specific acquisition verdict

**Do not download gigabytes simply to expand a dataset count.** First use the already-downloaded DLR-UT v1.3.1 for P20's *model vs observed* headway and queue-state comparison, and pick an official small Utah SPaT/BSM date window if actual signal change timing cannot be derived from DLR. In the RF track, use the controlled ESPARGOS *static* public file as a pipeline-baseline candidate, but do not present it as actual traffic sensing.

## Large CIM dataset ZIP — move status and provenance

The user explicitly requested moving a giant shared-drive ZIP to an appropriate shelf, superseding the prior blanket 'do not move' HOLD **for file organization only**. The prior archive records named `CIM dataset.zip`, about 5 GB, possibly still being downloaded separately. **No actual file ID, parent folder, size metadata or direct accessible file was found** after searching Drive for exact and partial names, generic ZIP, and checking R&E's DATASETS and evidence parents. The source ZIP was NOT opened, downloaded, enumerated or moved. Do not claim otherwise.

**Prepared receiving folder:** [CIM_dataset_zip — UNVERIFIED_HOLD (metadata only)](https://drive.google.com/drive/folders/1BWRCLDTyvRkQZRIUloZo63EHDGIlgjet), directly below [02_DATASETS/90_QUARANTINE_AND_UNVERIFIED](https://drive.google.com/drive/folders/1VrkYRMoJSXf8QpYYW7Fy0J196Y6qzORD). Verified new folder ID `1BWRCLDTyvRkQZRIUloZo63EHDGIlgjet`; it is currently empty. Once the actual existing ZIP ID is visible, move **metadata only** by adding this folder and removing the verified old parent, preserving the exact file ID, raw bytes, original name, external permissions and any separate ownership. Before promoting from quarantine, require title, provider-confirmed size, uploader provenance, license, SHA256 when available and actual study relevance.

**NOT DONE**: cannot move an invisible/unlocated file, and no license/content validation attempted. The empty quarantine folder is a valid completed preparation, not the move.

## T2 / RF data collection safety and limits
This research uses public published datasets and school-approved future tabletop equipment; no unauthorized Wi-Fi capture, live road controller access, traffic infrastructure modifications, or private data harvesting. K047 field archive remains separately sealed, CIM content unopened, GitHub Actions/bot never used.

Sources: official SUMO output docs https://sumo.dlr.de/docs/Simulation/Output/index.html ; DLR https://zenodo.org/records/20919480 ; US DOT and other links above.
