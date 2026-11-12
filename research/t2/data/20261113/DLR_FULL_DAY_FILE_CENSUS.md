# DLR-UT 1.3.1 — 2026-11-13 Full-Day Drive File Census

**Status:** Actual Research OS Drive **file metadata** and four volume/signal 15-minute source windows read, with source XML map parsed locally. File census is NOT equivalent to full-day row-level verification.

| File group | 15-minute windows | Total bytes | Window range |
|---|---:|---:|---|
| raw_data/trajectories | 96 | 2,621,708,178 | 2023-09-24T00:00 through 2023-09-25T00:00 UTC |
| raw_data/traffic_lights | 96 | 97,168,311 | same |
| meta_data/traffic_volume | 96 | 6,005,890 | same |
| **Three-group total** | **288 files** | **2,724,882,379** | 24 hours |

All 96 normalized 15-minute filename windows were present in **all three groups**; no missing file-window pair was observed. The three groups are **not** the entire source archive: weather, road condition, air quality, map, OpenSCENARIO and documentation are stored separately.

Actual source files were read for 2023-09-24 UTC 12:00–13:00: 4 volume and 4 traffic-signal CSVs. Their derived metrics are in `dlr_utc_1200_1300_observed.csv`. Movement metadata has **32/27/26/28 columns**, which are not identical! A missing movement field should not be silently set to zero. All four volume blocks have 900 seconds; signals contain 897/899/895/898 *measurement instants*, each with 30 heads.

The 12:00–12:45 publisher-derived counts sum to 1,409 (436+475+498), reproducing prior D42 scope. Additional 12:45–13:00 count is 450; this interval was examined and is NOT a blind test holdout.

**Prospectively reserved validation window:** 2023-09-24 **18:00–18:30 UTC**. The source filenames, sizes and existence have been observed, but contents were NOT read in this 2026-11-13 pass. Do not tune on this window before the model and mapping rules are frozen. It remains a *same-day* holdout, not cross-date independent validation.

The provided map (OpenDRIVE v1.0.0 XML) has 28 roads, 1 junction, 16 connections, 123 laneSections, 1005 lane elements and 7 signal elements. It is not yet verified that map signal objects correspond to the 30 traffic-light CSV signal-head IDs. Road reference lines are not guaranteed actual lane centrelines. All counts here derived from XML structure, not visual topology inspection.

Public dataset source: https://zenodo.org/records/20919480 .
Research OS Drive raw bytes preserved in existing dataset tree; no raw files moved or replaced.
