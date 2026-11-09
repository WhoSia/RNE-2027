# D42 (2026-11-10) — Lane-strip stopline reconstruction HOLD

Direct field inputs: trajectory CSV SHA256 `5504d37534fd12e95a9e1b019de18f504a2d668dcf564392bb169d42ab42550e`, OpenDRIVE SHA256 `256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4`, interval 2023-09-24 12:00–12:15 UTC.

## Step A: open reference-normal planes (unvalidated)
OpenDRIVE type-294 static road signals: 7 XML records / 6 unique sign IDs. With finite ±16m lateral clipping but without lane strips: 821 forward and 845 reverse reference-plane crossings. These are **not** independent traffic volume or road traffic violations. Two sign records lie on junction roads; sign ID 300607 occurs twice. Eight synthetic geometry tests PASS.

## Step B: nominal driving-lane finite strips (also unvalidated)
Evaluate OpenDRIVE laneSection and piecewise cubic widths for each driving lane, extract road-relative negative/positive lateral offsets, interpolate each candidate 20Hz track's crossing point and classify only uniquely assignable strip. Explicitly reject ambiguous shared boundaries, gaps >75ms and projected speed <=1m/s. This is a reference-normal centerplane crossing, **not** independently confirmed publisher lane-specific stopline geometry.

Observed candidate events: 684, 454 distinct track IDs, 230 IDs have crossings at >1 candidate gate. By road: 100000 116; 101000 128; 179000 133; 201000 121; 280000 76; junction 300013 42; junction 300018 68. These are not distinct physical vehicles or guaranteed independent crossings.

Publisher's 32-movement traffic-volume cell sum: **436**. Neither 684 nor 454 is a valid direct comparator because physical stopline segment, topology and route-to-movement mapping are incomplete. No attempts to optimize free parameters toward 436 are authorized before independent geometry definition. Synthetic combined tests 16/16 PASS; **empirical reconstruction remains HOLD**.

## Evidence and provenance
- Zip A (baseline negative): https://drive.google.com/file/d/1yZP75wtqjjBR3ndvBmK3jnV8D8xUdk4G/view SHA256 `08673bf0f6913adef4ffe082d466025dccd057cf93901064ed7648c270db79a8`.
- Derived A: https://drive.google.com/file/d/1iYvsGu5Cw6n1WwQKxuX8gpLNlh4jqnNN/view.
- Zip B (lane-strip): https://drive.google.com/file/d/1OIo9uWTPYgnUxbJB23f9d1cS8ccS7hpJ/view SHA256 `5551ee4b1ab6cd6b339bc90e9383c0dab3708745ac456d24f9011ad16944dad8`.
- Derived B: https://drive.google.com/file/d/1R9P7J2NKP0-MuZv0WLIz-RkxRpNFW__f/view.
- Native reasoning doc (only Google Docs in date folder): https://docs.google.com/document/d/1fkzetvDIyGTho0wyccceYvFhUvB5ZPtPAMhjmJK9DH8/edit
- GitHub code and tests are the executable text source. ZIP B carries the locally executed matching program, tests, result tables and manifest. The deposited ZIP omits large DLR original files; inputs are located separately under immutable Drive dataset archive.

## NEXT GATE
Independently fix complete finite stopline segments and lane permissions using published roadway geometry and road-to-junction connection topology. Match each track across a single approach, junction turn and exit; assign publisher movement labels without using published 436 count as a fitting target. Independently map 30 observed signal heads; preserve UNKNOWN on sensor gaps and ambiguous classifications. Cross-validate on a different unused interval. No independent SUMO or real-world policy gain has yet been established.
