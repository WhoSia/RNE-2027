# CityArtery (Dongguan) v1

- Dataset DOI: [10.17632/ftzzmh2cmt.1](https://doi.org/10.17632/ftzzmh2cmt.1), Wang (2025), CC BY 4.0.
- [Publisher ZIP preserved on Drive](https://drive.google.com/file/d/1u0wdnqNxA9ryKMXs2eeGeS3s8c6slT3t/view)
- 30,582,559 bytes; SHA-256 `75cc46cf54d88179254788acc9f3b8ed65024db7c3b6c7d26478b9205586d67c`.

## Reproduce the inventory and measurement proxies

From this folder, after installing `openpyxl` for workbook extraction:

```sh
python archive_audit.py /path/to/CityArtery.zip /tmp/cityartery-manifest.json
python trajectory_audit.py /path/to/CityArtery.zip /tmp/cityartery-tracks.json
python signal_plans.py /path/to/CityArtery.zip /tmp/cityartery-plans.json
python stopped_tracks.py /path/to/CityArtery.zip /tmp/cityartery-stops.json
```

All 24 archive members pass the ZIP CRC check. Exact digest groups in the
manifest reveal reused bytes across intersection-folder labels. The processed
tables contain 8,650 recording-scoped track keys, including 533 pedestrians,
and 574,516 sample rows. Each within-track gap rounds to 1.001 s. The two time
columns disagree on 361,302 rows. Both gate fields are absent or blank in all
processed observations. The speed-only audit counts 6,765 episodes (in 5,220
tracks) under a 2 km/h threshold and a 2-second contiguous minimum sampled
span, including 384 pedestrian episodes. These are recording-local observations
with censoring at the track boundary. A queue count requires spatial and
movement criteria in addition to low speed.

## Evidence required for signal-synchronized replay

| Join | Available now | Next evidence |
|---|---|---|
| File to site and recording | File paths, video IDs and byte-equivalence groups | Author/site mapping including duplicate interpretations and disambiguation |
| Samples to spatial movements | Local coordinates and lane codes | Georeferenced stop lines, pedestrian crossing, lane connectivity, and lane-to-movement mapping |
| Workbook to field signal | Three sheets, 18 rows of nominal phase sequences and durations | Actual signal-state events or a visually anchored phase clock, clearance periods, plus uncertainty |
| Trajectories to signal clock | Recording-local times and sample cadence | Multiple distinct observed anchors and residual check on an unused anchor |
| Queue to downstream blockage | Low-speed spans and sample positions | Link occupancy, usable receiving space, and identification of the downstream release |

Keep each join explicit and record its provenance. The ZIP by itself supports
descriptive summaries of trajectories and nominal timings. A paired intervention
replay would additionally require validated site and clock joins and a model of
movement flows. Report geometry or time ambiguity at the affected movement
instead of imputing a mapping from a directory name.
