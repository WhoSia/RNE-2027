# DLR-UT K047 — 2026-11-13 G1 Lane-Validity Crossing Gate

## Finding with empirical source-derived evidence

Opened **actual** source CSV `trajectories_230924-233000_230924-234500.csv` in the existing Research OS DLR-UT v1.3.1 Drive repository. It has **8,624 rows / 37 object identifiers**. The OpenDRIVE map is an independently stored corresponding source; four approaching roads have static `type=294` stop-line marking candidates (StVO Zeichen 294). The map objects do **not** establish a direct map to 30 signal-state IDs.

Tracked objects were sorted by timestamp and a linear interpolation was made for **forward center position crossing** of the road-reference-line normal at the source marking's road s-coordinate. Max adjacent sample separation was 0.25 s (recorded positive events used 0.05 s), max broad lateral gate 20 m, car+van+truck classifier probability >= 0.5. All counts are *candidate events*, not independent manual crossing truth.

| Incoming road | Broad ±20 m center crossings | Within OpenDRIVE marking laneValidity | Excluded as outside marking-valid lanes |
|---|---:|---:|---:|
| 100000 | 5 | 5 | 0 |
| 179000 | 5 | 0 | 5 |
| 201000 | 7 | 2 | 5 |
| 280000 | 0 | 0 | 0 |
| **Total** | **17** | **7** | **10** |

Lane boundaries were calculated from the road-s-specific laneSection and piecewise width polynomials, not a single arbitrary 3 m lane. On these four roads no `laneOffset` XML element was present. At the marker the source marking validity covers lateral interval approximately road 100000 [-14.787,0]m (lanes -5..-1), road 179000 [-3.006,0]m (lane -1), road 201000 [-2.800,0]m (lane -1), road 280000 [-2.508,0]m (lane -1). Negative lateral is right of reference in road travel direction.

**Interpretation:** The 10 rejected reference-line crossings are *not* disproven traffic movements. Their observed center positions are outside the lanes covered by those **particular map marking objects**. A signal-head mapping, center/front bumper correction, independent human stopline annotation, vehicle-trajectory-to-road matching and signal-lane conflict validation are needed before claiming 7 observed field stopline crossings. Do **not** equate counts to publisher per-movement counts or signal violations.

## Reproducibility

Local sealed source package and derived events CSV, Python runner, 12 passing local unittest tests: https://drive.google.com/file/d/1h_lmPQeiB0qdZR7HoOomYNBsONsfyN79/view

ZIP SHA256 `b82907a4fe492597005adb1be1087cdec5b1eb358fb7488d16f830a309a922ec`. Raw 20-Hz source bytes are **not** duplicated into ZIP; the runner requires the exact Drive original file mounted locally. GitHub Python `crossing_lane_validity_v1.py` is a separately authored, standalone functional mirror and is **not byte-identical to sealed ZIP source**; GitHub remote runtime tests not asserted. Existing D42/D44 fail records remain preserved. No GitHub Actions used.

## Week 1 BFS status (source metadata vs raw evidence)

- **DLR K047**: empirical raw-access gate partially passes; one full-day 96×3 file-window census; chosen 23:30 exploratory track window read; earlier 12:00–13:00 published volume/signal CSV contents read; G1 head-to-movement and human ground-truth gate still HOLD.
- **Seoul TOPIS smart intersection**: 5-minute turn counts official catalog fields `CROSS_ID,DIR_CD,STND_DT,STND_TM,LTURN_VOL,STURN_VOL,RTURN_VOL,UTURN_VOL`. Historical C-ITS signal file: `https://t-data.seoul.go.kr/dataprovide/trafficdataviewfile.do?data_id=10382`. Both dataset catalogs confirmed, but actual joined row pairs `CROSS_ID↔itstId` not observed. Legacy APIs sunset **2026-11-15**, replacement historic file route preferred.
- **CityArtery**: official Mendeley DOI `10.17632/ftzzmh2cmt.1` (2025) states 14,490 UAV trajectories, three cameras, 1 km 2–3 signalized intersections, map, simulation calibration and signal timing records; raw file bytes unacquired. Treat as catalog, not validation.
- Held-out DLR **18:00–18:30 UTC same day 2023-09-24 remains unopened**, no claims of blind/new-date field validation.

## Next DFS/BFS gate

DFS: build lane-centerline-aware actual marking segment + valid vehicle orientation; manually inspect fixed predeclared short set of ambiguous events; map time-stamped signal head to movement without publisher-count circularity. BFS: use provider file history and semantics to find same Seoul cross-id/time signal records; check CityArtery raw file listing/download; switch primary field location only if evidence quality improves. **No new synthetic traffic signal features** until observational gate is closed.
