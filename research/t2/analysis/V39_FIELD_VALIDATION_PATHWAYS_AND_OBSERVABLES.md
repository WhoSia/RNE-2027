# T2 v3.9 — Independent field validation pathways (2026-11-02)

Implemented and locally tested separate empirical observation reader and date-holdout checker (6/6 tests passed). GitHub code: `research/t2/validation/field_validation.py`, tests: `research/t2/validation/test_field_validation.py`. The implementation does **not** validate any actual road case yet.

## Distinct observational endpoints

1. Geometry: lane counts, pocket length, upstream/downstream distances, grades and authorized turns.
2. Signal: real stage sequence, cycle, green split, intergreen, offset, TOD variability and pedestrian constraints.
3. Demand: 5–15 minute movement-specific approach counts across multiple days and peaks, measured rather than inferred from population alone.
4. Queue: per-cycle maximum and residual, both measured using defined physical boundaries.
5. Trip performance: matched corridor travel times and incomplete trips. Prefer distributions rather than only mean completed-trip time.
6. Generalization: site A calibration day vs independent day, then distinct site B, then Korea-wide contexts after Gyeongnam evidence.

## Measurement model

For one closed movement-group observation boundary:
`queue_start + arrivals - departures - queue_end = residual`.

Nonzero residual is *not* necessarily a simulator bug: lane changes, turning diversion, multiple queues, observer count error and crossing the window boundary can violate the closed-unit assumption. The naive reference `green_seconds/mean_headway_s` is not an exact engineering capacity bound.

## Real-data availability and caution

Public ITS design manuals describe phase timing, lane/movement flows and queue-relevant inputs. Existing Korean intersection signal optimization literature in Wonju used direction-turning counts with time-of-day segmentation and simulation-based control-delay comparisons (Park et al., ITS Korea 2024, https://kits.or.kr/file/2024/ITS_2024_04.pdf). The study's data are NOT T2 data. Open Korean traffic API listings provide travel-time/speed and incidents but not necessarily real phase or turning counts in the target district.

## Actionable acquisition matrix

A. Existing agency intersection timing plans: ask owner authority if public/releasable; independently verify recorded timing.
B. Short non-identifying hand counts from safe public vantage with adult/school supervision: temporal turning counts and queue snapshots, no private tracking.
C. Public urban speed link indicators (KTDB/View-T) for coarse corridor consistency only, not a substitute for per-movement counts.
D. Bus timetable and stops to test predicted queue perturbation; timetable alone is not bus dwell event data.
E. Terrain/road map and independent geometry verification to parameterize slope and lane storage.
F. SUMO synthetic matched-network reproduction as mechanism check, not proof of real fidelity.

Do not operate real traffic signals, trespass, or collect identifying plates/pedestrian data.

## New priority gate

Before optimizing any local signal, reproduce its **existing fixed-time operation** against at least one held-out observation day on: turning counts, max and residual queue, travel-time distribution, stage timing. If failed, revise model, do not optimize over incorrect simulator.

Code and experiments remain on research branch; no GitHub Actions or bot author.
