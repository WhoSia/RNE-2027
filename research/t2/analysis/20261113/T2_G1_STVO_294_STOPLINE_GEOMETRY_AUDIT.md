# DLR K047 G1: StVO 294 stop-line geometry gate (2026-11-13)

## What was actually discovered

The original OpenDRIVE source `bs-inner-ring-road-ut.xodr` in Research OS Drive has seven `<signal type="294" dynamic="no">` XML elements. Germany's official Straßenverkehrs-Ordnung (StVO), Anlage 2, defines traffic marking **Zeichen 294 = Haltlinie (stop line)**, rather than a traffic-light head. Authority: https://www.gesetze-im-internet.de/stvo_2013/anlage_2.html .

The seven map objects have only **six distinct IDs**: ID 300607 occurs on both roads 101000 and 280000, and must not be treated as a unique dynamic traffic signal. The DLR raw `traffic-lights` CSV instead provides states for **30 head IDs (1..30)**. **No head-to-road-movement equivalence has been established.**

## Classified physical stop-line candidates

| OpenDRIVE road | object ID | s (m) | distance to road end (m) | role |
|--|--|--:|--:|--|
| 100000 | 300606 | 155.566906 | 0.576461 | incoming road, endpoint candidate |
| 179000 | 300605 | 68.286569 | 0.529276 | incoming road, endpoint candidate |
| 201000 | 300600 | 67.071898 | 0.102093 | incoming road, endpoint candidate |
| 280000 | 300607 | 173.537797 | 0.243997 | incoming road, endpoint candidate |
| 300013 | 300604 | 1.068287 | 40.458809 | internal junction connector candidate |
| 300018 | 300602 | 0.329977 | 61.354296 | internal junction connector candidate |
| 101000 | 300607 | 0 | 66.622609 | road-start marking, not an incoming-road endpoint |

All four incoming-road markings are near the road's **reference-line** end, not necessarily a single shared vehicle crossing line. The 101000 object has orientation `-` and `laneValidity +1..+1`; the source's active lane +1 at s=0 is `shoulder` rather than `driving`, hence this is explicitly **not accepted** as an independently validated vehicle stop line. Map road signal objects may be cross-section road markings, not traffic heads.

The map has one major junction (`300000`), 16 connections, 28 road elements, 123 lane sections; these numbers do not imply 16 signal phases or 7 dynamic lights.

## Independent numerical extraction gate

A stdlib `xml.etree.ElementTree` tool evaluated OpenDRIVE `planView` line/arc reference geometry with:
- line: `x=x0+ds cos(h); y=y0+ds sin(h)`;
- arc: `x=x0 + 2 sin(k ds/2)/k cos(h+k ds/2)`, `y=y0+2 sin(k ds/2)/k sin(h+k ds/2)`.

Road `s` and local reference-line `x,y` are expressed in meters. **The map-local coordinates must not be compared directly to DLR trajectory UTM32 Easting/Northing without an independently verified coordinate conversion.** Unsupported spiral geometries throw errors rather than silently returning approximations. Six local tests passed, including synthetic quarter-circle/line, geometry rejection, actual seven objects/six IDs, incoming-road filter and duplicate-ID check.

The exact executed Python source, CSV, tests, plot and SHA manifest were packaged locally as `RNE_T2_20261113_G1_STOPLINE_294_V1.zip`, SHA-256 **a44acb8123db2aab53aa42ea77e9f1f5d24731fbd1afe5352cce560bb77ef746**. The CSV in this repository is a compact hand-verified subset; use the ZIP as the tested source of truth. ZIP is **not automatically a Drive-uploaded artifact** unless its Drive ID is independently confirmed.

## Scientific meaning and gate status

**G1 = PARTIALLY RESOLVED, STILL OPEN.** The StVO 294 map-object semantics and four incoming stop-line candidates are supported by raw source + legal marking definition, but per-lane stop-line position, lane/turn permission, UTM-to-local projection, actual 20Hz trajectory crossings, head-to-movement mapping and independent queue annotations are **UNRESOLVED**.

Next: validate the source `geoReference` transform, map reference lines to lane centers using laneOffset/laneWidth, then demonstrate crossing of one documented approach stop-line by actual trajectories. Independently assign each of 30 traffic heads to controlled movement using publisher documentation or documented geometrical/temporal evidence; UNKNOWN otherwise.

**Do not** infer a field-policy delay improvement, fabricate a head mapping, or open the prospectively reserved 18:00–18:30 UTC holdout before model rules are frozen.

## Sources
- German government StVO Anlage 2: https://www.gesetze-im-internet.de/stvo_2013/anlage_2.html
- DLR original dataset v1.3.1: https://zenodo.org/records/20919480
- Research OS originally stored map in DLR-UT extracted original files. No map bytes were modified.

## Later 2026-11-13 extension: verified map projection and real trajectory proximity

The map's exact `geoReference` uses the same Transverse Mercator definition as trajectory EPSG:32632, except false easting and northing. `pyproj 3.7.2` verified for **this map only**: `x_local = UTM_E - 604763 m`; `y_local = UTM_N - 5792795 m`. Raw trajectory coordinate pairs (604746.796,5792790.916) and (604810.383,5792808.425) map to (-16.204,-4.084) and (47.383,13.425) m, respectively.

One explored 23:30–23:45 UTC original CSV contains 8,624 20Hz poses from 37 track IDs. Distinct IDs within radius 5m of four inbound stop-line *reference points*: roads 100000/179000/201000/280000 have 4/2/6/2. These **14 object/road proximity pairs are not validated car counts or stop-line crossing events**. The publisher's classification probabilities include non-cars, and actual lane centerline/line crossing are not yet established. Derived id, timestamp and distances are committed to `research/t2/data/20261113/dlr_2330_track_stopline_reference_proximity.csv`.

Local eight geometry+CRS tests passed. MCP-Hub independently confirmed seven source-derived CSV rows had uniform 17-column structure; this is not traffic validation. Exact locally run source, tests, figure, CSV and SHA manifest are preserved in [Drive G1 V2](https://drive.google.com/file/d/1AK20rUWmzBqJx0zdz_1DvtrvJUabQ1d3/view) (134153 bytes, local SHA256 `6299dfac7bace24e62900a8bee4a8a8fde6f2541ba899b4d5f61573c688cff97`). Drive file metadata size verified but remote full-byte hash not re-read. GitHub lightweight extractor is independently authored, **not byte-identical** to this executed ZIP.

G1 remains **PARTIALLY RESOLVED**: lane-specific stop-line segments, per-track orientation/vehicle classification, 30 signal-head/movement mapping and independent observation GT remain open. Preserved prospective holdout 18:00–18:30 UTC remains unopened.
