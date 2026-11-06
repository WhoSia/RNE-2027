# Executable acceptance gates

| Gate | Need to see | Current evidence | State |
| --- | --- | --- | --- |
| D37 Original source | CSV rows decoded with source path and file blob hash, visible data dictionary | 16 original public CSVs read through GitHub app; locally persisted source-level derived metadata | **PARTIAL** |
| D38 Actual single intersection | One georeferenced junction, signal plan/phase by time, individual vehicles in same window and lane queue observations | DLR metadata only; no original ZIP or signal mapping | **HOLD** |
| D39 Independent SUMO | Executed pinned SUMO and raw tripinfo/FCD; same geometry/demand/signals; compare with T2 and field | `sumo`/`netconvert` not found | **HOLD** |
| D40 Policy causal evaluation | Sensor error data measured, policy fixed before held-out observations, all vehicles accounted, measured queue tail | Four-seed synthetic proof-of-possibility only | **HOLD** |

Safety/validity: never direct the actual operation of a public signal controller; all signal policies remain in an offline virtual model. Public external source access does not imply permission to redistribute underlying raw data.
