# R&E 2027 T2 — D51 Phase Order × Turn-Pocket Capacity (2026-11-12)

## Exhibition-first principle

The priority is a measurable traffic-engineering problem with student-led discovery, modeling, validation and an actionable improvement. Novelty of the isolated phase-order or short turn-bay mechanism is not claimed; older traffic engineering literature already studies such policies. The 2026 exhibition rubric was 45 creativity/inquiry, 25 theory, 15 participation and 15 practicality; independently reconfirm 2027. Preserve DFS/BFS scope and avoid freezing on simulation defects.

## Engineering implementation and reproducible evidence

Source-of-truth Python ZIP in Drive: https://drive.google.com/file/d/1oreoAeDmCPsSK9B0T3_0SiJlA7V3uDSp/view
CSV 288 matched cases: https://drive.google.com/file/d/10-NfE7XlyadnCtuKVB0vNP9rOhfNoYsw/view
ZIP SHA256: dbda1631b24a9c277056d2bc76d958767497c5f5ae6fd2b25a395f0a596801e4

D51 code extends D50 single-approach shared FIFO queue with through/left finite vehicle-count bays and a policy switch left_first. Both policies use the same input vehicle arrival IDs, same 60s cycle, 24s through green, 12s protected-left green, 24s nominal all-red remainder, same receiving capacities, and max 1 upstream admission per second. The sole intervention is phase sequence: leading L-then-T versus lagging T-then-L. The model does NOT implement a real safety-valid timing plan, yellow/intergreens, opposing turns, pedestrians, physical motion, merging, or lane changing. Downstream discharge precedes admissions within a tick but entry checks pre-tick occupancy, forbidding same-tick freed-space reuse.

Baseline fixed arrival trace: 6 cycles; each cycle 18 vehicles, 12 through and 6 left, arriving once per second from cycle phase 0. Every third vehicle turns left. Through bay capacity 12. Pocket K = 1,2,3,4,6,8,12,20. All 108 vehicles complete within 600s for the representative K=4 and K=6 policy comparison.

| Pocket K | Lagging mean delay s | Leading mean delay s | Preferred |
| ---: | ---: | ---: | --- |
|1|71.9259|44.6481|Leading|
|2|31.1296|11.2963|Leading|
|3|24.0556|11.1574|Leading|
|4|17.3889|11.1574|Leading|
|6|7.0000|11.1574|Lagging|
|8|7.0000|11.1574|Lagging|
|12|7.0000|11.1574|Lagging|

This is a model-specific *policy ranking reversal* under controlled capacity variation. It does not imply an empirical switch at six cars, establish novel prior art, or give an on-road policy prescription.

BFS: 8 capacity values × 3 per-cycle arrival counts (12,18,24) × 3 turn placement patterns (each 2nd, 3rd, 4th arrival left) × 4 arrival phases (0,10,20,30s) = 288 matched pairs / 576 simulations. Each policy is ranked first by total unfinished trips at 600s, then mean completed-trip delay. Leading chosen in 148, lagging in 140; for 273 cases where BOTH policies complete every car, leading chosen in 139 and lagging 134. This artificial-grid selection frequency is not a real-world probability.

Local stdlib regression: 12 D51 tests plus 13 unchanged D50 tests passed (25/25). D51 tests cover input/parameter contracts, cycle phase wrap, leading/lagging order, conservation, capacity, censoring, no same-tick space reuse, D50 lagging parity and identical demand. No independent SUMO execution/holdout field calibration. The original D50 implementation is included unchanged in ZIP and original Drive archive remains preserved.

## Krauß (1998) literature connection

Original German/English dissertation metadata validated and archived under Research OS 11_SOURCES (PhD thesis, Universität zu Köln, DLR Forschungsbericht 98-08). It warns that coarse spatial discretization and rounding can alter safety constraints; its car-following model with bounded acceleration/deceleration and stochastic perturbation is NOT D51 point-queue physics. Reference dissertation: https://drive.google.com/file/d/1PHBnwzpVYsOGvh9LmuP1bcw5h4Np5KGW/view. Do not claim D51 is validated by Krauss or SUMO.

## Gates to reach real traffic signal engineering

1. Replicate using a second independent event-scheduling implementation and reverse pre-tick capacity reuse convention; test whether policy rank changes.
2. Add valid yellow/intergreen and pedestrian/opposing turn conflict times, equalized cycle/split across policies; retain frozen arrivals.
3. Convert vehicles to measured bay length in meters with vehicle lengths and spacing; document upstream boundary and physical queue occupancy.
4. Calibrate with intersection approach counts, turning fractions, lane geometry and signal controller phases; split time periods into calibration and held-out testing.
5. Evaluate field-realistic multi-criteria: delay distribution per movement, throughput, unserved, pedestrian wait, and storage/blocking events.
6. Continue BFS search for empirical data in Korea and internationally; select location based on evidence, not familiarity.

Research log: Google Docs / 20261112 김우준의 사유. No GitHub Actions or github-actions[bot]. Code ZIP on Drive is exact executable artifact; this GitHub file is research documentation.
