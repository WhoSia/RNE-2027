# T2 P23 — Three-source DLR coordinate alignment and published stopline bins

Date: 2026-11-22 KST. **First measured geospatial-geometry gate PASS. Signal-head assignment, observed per-car stopline crossing, T2-vs-SUMO dynamics and field policy effect remain OPEN.**

## Sources actually read (three existing Drive originals, no new mass download)

- DLR-UT v1.3.1 `map/bs-inner-ring-road-ut.xodr` OpenDRIVE, file ID `1j6xu3ngbh1dO75_eCdrgBWgytRAzGtg`, SHA-256 `256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4`.
- `trajectories_230924-233000_230924-234500.csv`, file ID `16SyjOzQBy5t9iVIV0tdZaAOlo39jYOri`, SHA-256 `6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50`.
- `traffic-volume_230924-233000_230924-234500.csv`, original dataset metadata file previously in Drive, SHA-256 `00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798`. The original README explicitly defines its movement-column events as traffic participants' **center points crossing movement-specific stoplines**.

All three originals were SHA-sealed on disk before calculations. The 2023-09-24 23:30–23:45 UTC interval is a single late-night observational segment; its 37 trajectory IDs and 8,624 repeated samples are not independent traffic days.

## Geographic alignment

The exact OpenDRIVE `header/geoReference` reports `+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=-104763 +y_0=-5792795 +datum=WGS84 +units=m +no_defs`. Raw trajectories supply easting/northing in UTM zone 32N. The script uses **pyproj** to transform `EPSG:32632` into the embedded OpenDRIVE projected CRS; for a sample raw point `(604746.796,5792790.916)`, the transformed map point is `(-16.204,-4.084)`. No manually optimized offset was fit to the trajectories.

The original map contains **28 roads** and **201 planView segments** (194 arcs and 7 straight lines); those curves were independently sampled at ≤1-meter steps, then assembled into a Shapely multiline centerline reference. For **all 8,624 trajectory samples**, not just a curated car subset:

| Nearest projected road centerline metric | Result |
|---|---:|
| Samples at or within 5m | **6,962 / 8,624** (80.7%) |
| Samples at or within 10m | **8,389 / 8,624** (97.3%) |
| Samples at or within 20m | **8,624 / 8,624** (100%) |
| Median / 90th-percentile distance | **3.342m / 6.956m** |
| Maximum sampled centerline distance | **13.153m** |

**Exploratory negative control:** deliberately shift every aligned point **100m east in the map coordinate system**, with no other change. Median distance increases to **29.231m** and only **584 / 8,624** points remain within 10m. This is a constructed corruption check, not a preregistered independent calibration. The spatial concordance strongly supports correct georeferencing but does NOT identify the correct specific lane, direction, turning movement, signal ID, stopline or queuing state. The sample includes vulnerable road users that need not lie on a roadway centerline.

## Official DLR 1-second stopline *bin* source

The same-window `traffic-volume` file contains **893 observed 1-second records** (23:30:07–23:44:59 UTC) and **12 movement columns** with one-second `0/1` crossing indicators. The total of all movement-column positive bins is **17**. The available volume columns all contain ≥1 recorded crossing bin in this file. These movement names include `South2North1` (4 bins), `East2West0` (2), `West1East0` (2), and nine other 1-bin movements (see structured JSON). The 17 is *recorded movement-specific bins*, NOT proof of 17 distinct vehicles after ID de-duplication; multiple simultaneous movement channels can fire and metadata has different tracking rules from raw trajectories. It is a late-night subset and should not be treated as a representative traffic demand estimate.

Importantly, the stopline bin file provides a **direct empirical crossing constraint** before individual stopline coordinates can be inferred from OpenDRIVE. Its 1-second time grid cannot resolve precise continuous inter-vehicle discharge headways and does not explicitly assign one of the dynamic 30 traffic-signal IDs.

## A crucial map-ID mismatch

OpenDRIVE contains **7 static `road/signals/signal` elements with only 6 distinct static IDs**, whereas the real-time traffic signal CSV has **30 signal IDs**. Those IDs are distinct systems and have not been causally mapped. Attempting to join by equal integer IDs or nearest geometric signal location without verifying official DLR signal-head mapping would manufacture a false phase/trajectory association.

## Executed code/tests and reproducibility

- [Implementation](p23_map_volume_alignment.py) performs exact SHA-256 source gate, XML OpenDRIVE arc/line centerline conversion, official UTM-to-OpenDRIVE CRS, exhaustive trajectory map distance, 100m negative-control, and binary 1Hz stopline movement audit.
- [Seven regression tests](test_p23_map_volume_alignment.py): all 8,624 real source positions and 893 volume bins, 100m negative control, static/dynamic signal namespace non-equality, exact coordinate landmark, invalid sampling stride, wrong SHA failure, and forbidden unsupported stopline/headway inference.
- **7/7 tests PASSED locally** on the three exact raw source files. Source Git blob `16c830a93b6dda4860d200f1b7c03c95dcb84105`, test blob `c4e2583b6856d98e768481d6392a0066c2062867`; exact hashes have been read back from GitHub `main`.
- [Full structured result](P23_DLR_SPATIAL_ALIGNMENT_RESULT_20261122.json), locally reproduced SHA-256 `36c1032db31698af3a19c3c01d63822b56a39445461e1b8e1760edf661cc9f35`; 7-test transcript SHA-256 `b71aa5d5589d96188dde5953178ad01223f9382a37310c929007aad4d3bb0477`.
- Dependencies: Python 3.13, pyproj 3.7.2, Shapely as installed; this audit does not require the synthetic T2 engine or SUMO.

```bash
python p23_map_volume_alignment.py /path/to/bs-inner-ring-road-ut.xodr /path/to/trajectories_230924-233000_230924-234500.csv /path/to/traffic-volume_230924-233000_230924-234500.csv p23_alignment_results.json
python -m unittest -v test_p23_map_volume_alignment.py
```

## Research direction and falsification

Next research gate is **not** optimizing signals. Obtain DLR's official signal ID/name/approach mapping and exact stopline lane lines. Independently reconstruct crossing bins from the 20Hz trajectories with declared interpolation and lane geometry, compare those events against the official 1Hz 17-bin movement reference **without retrospective alignment tuning**, and report false/missed crossing bins. Only after that pass should a SUMO intersection with matching geometry and a frozen arrival tape be compared on headways, queuing and finite receiver storage. Traffic-light control legality and potential real-world safety remain independent checks.

INTERACTION TC ZIP and DR RAR were reported downloaded to user PC; as of the last Drive check, neither was accessible in the [prepared immutable originals receiving folder](https://drive.google.com/drive/folders/1k-EEwOyBgUVoQaGwQsModGfmP92w0Gzv). No move, hash, extraction or content validation claimed for those files. User can upload originals unchanged.

K047 sealed; CIM ~5GB raw file HOLD; no real-road intervention or GitHub Actions.
