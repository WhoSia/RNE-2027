# R&E 2027 T2 — 2026-11-13 G1 V4 Front-vs-Center Geometric Gate

## Objective
Week 1 of four-week exhibition plan: field data custody and measured definitions before signal-policy claims. Use original DLR-UT 23:30–23:45 UTC tracks and official OpenDRIVE, maintaining 18:00–18:30 UTC locked same-day holdout.

## Source-derived empirical result
Input: 8,624 raw tracked-object rows / 37 unique IDs. StVO Zeichen 294 static marking candidates, four approaching roads. Adjacent observations <=0.25 s, car+van+truck probability >=0.5, broad lateral +/-20 m. Vehicle front is *inferred* at center + 0.5 * reported length * [cos yaw, sin yaw], not independently annotated.

| point convention | broad reference-line crossing candidates | within particular marking's lane-validity |
| center | 17 | 7 |
| inferred front bumper | 22 | 7 |

All seven marking-valid vehicle/road pairs are shared. In those 7, front crossing is earlier by 0.126–0.867 s; median 0.243 s. The broad difference (extra five front intersections) does NOT demonstrate five extra traffic movements. Four additional broad crossings on road 201000 and one on 280000 are outside the marking validity lane interval. These events may involve valid neighboring movements or modeling uncertainty. Classification and positional error unassessed.

## Limits / failure modes
- No map from static road markings to dynamic signal head IDs 1..30 established; do not report crossing-on-red, safety compliance, green-start delay or observed control improvement.
- Bumper is an assumed geometric transformation; yaw conventions checked against velocity direction but not instrument independently validated.
- Track ID may span intersections. Same tracked object is allowed to be a candidate on multiple road reference lines (not unique cars crossing the intersection).
- No held-out validation, no separate day validation, no SUMO comparison.
- Source day 2023-09-24; this one sample is low nighttime volume and not a peak-hour traffic model calibration.

## Week 1 BFS status
DLR source bytes already present on Drive, primary field method validator. Seoul five-minute turning counts official catalog and CityArtery UAV multi-intersection dataset official record verified; raw joined Seoul rows and CityArtery bytes not yet ingested. The 4-week strategy continues: 45% data/field, 25% physical validation, 20% policies only after validation, 10% literature and audit.

## Reproduction
`python -m unittest discover -v` in package directory; 18 tests pass on this local environment. `python front_bumper_gate.py --xodr <xodr> --trajectories <original 23:30 csv> --output observed_2330_center_vs_front_events.csv`. The raw CSV and map are **not repackaged**; same originally stored source Drive IDs remain evidence-of-origin, and output CSV is accompanied by SHA manifest. Dataset citation: DLR-UT v1.3.1 Zenodo https://zenodo.org/records/20919480.
