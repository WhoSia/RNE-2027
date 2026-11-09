# D42 — 2026-11-09 DLR UT v1.3.1 real-file access, 45-minute OpenSCENARIO audit

## Source acquisition
Google Drive original ZIP: https://drive.google.com/file/d/1PsoI5qnfTi0ha6YlkJtEL6G28q9OJj36/view
Size 463,386,085 B. Connected Drive raw download returned HTTP 413 with strict 268,435,456 B limit. **Original ZIP has NOT been independently byte-hashed.** The publisher lists MD5 401da7fbc1739c565c366e86fc116473.

An extracted Drive folder already exists with raw_data, meta_data, map:
https://drive.google.com/drive/folders/1kbrvghFqGCUxnu6S-lBRUlKH6PeNMRsb

## Actual XOSC raw-byte analysis
Individual XOSC sources, each < 256 MiB, were downloaded successfully, hashed with SHA-256 and fully XML-parsed.

| UTC window (2023-09-24) | XML bytes | Trajectory nodes | Vertex nodes | SHA-256 |
|---|---:|---:|---:|---|
| 12:00–12:15 | 140160082 | 636 | 299053 | 7e30c842c25a236a8ab120be0f6fff95ad58236f600252f1e0657af096a97753 |
| 12:15–12:30 | 161842192 | 693 | 345788 | 73f5fcd8df4db11317b05a7e3b01b160c01a1c4670973cde7f32ba977093895d |
| 12:30–12:45 | 181500026 | 750 | 388075 | 9879aa830e80fd4a77acecafd10f8c85056096e67d65e7354724b7ac3e069b92 |

Total: 2,079 within-file trajectory nodes, 1,032,916 timestamped vertices. These **are not necessarily 2,079 distinct road users** across windows. Local sequence tests found no nonincreasing adjacent vertex timestamps, nonfinite coordinates, 50m+ consecutive-coordinate jumps, or consecutive-point inferred speeds above 40 m/s, within the stated checks. The tests do not certify the physical truth or completeness of the underlying sensor tracks.

XOSC source records have relative event times 0–899.95 s within each 15-min file. This is a derived OpenSCENARIO representation, not the raw 20-Hz trajectories CSV.

Derived audit CSV deposited in project Drive:
https://drive.google.com/file/d/1wQasWwLe292tOwVioOrQnyffVZmduo10/view

## OpenDRIVE
bs-inner-ring-road-ut.xodr was downloaded and XML-parsed. The document has 28 road elements, one junction element, header OpenDRIVE revMajor 1 revMinor 4, vendor DLR. These are **XML structure counts**, not empirical count of intersecting roads or observed stoplines. Lane-level geometry and traffic-light mapping remain a HOLD.

## Remaining gate
The extracted raw_data/trajectories, raw_data/traffic_lights and meta_data/traffic_volume folder listings were empty at query time; ongoing upload may change the state. Request exact original first 15-min CSVs for 12:00–12:15 UTC once upload is finished, not a modified/recompressed ZIP. These enable lane-aware field queues and actual signal timing. No independent SUMO run, sensor noise estimation or policy field validation has occurred.

References:
https://zenodo.org/records/20919480
https://docs.google.com/document/d/14fh_Szq3f8YSpvXJqAPhoBiX9mSJAsxRYJkSj0Gm4FE/edit
