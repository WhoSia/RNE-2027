# T2 D49 — 2026-11-12 — Protected Left / Pedestrian Phase Competition

## Science exhibition priority

The purpose of T2 is realistic traffic-engineering modeling, signal coordination and practical improvements to observable road problems. A wholly novel signal-control algorithm is **not** required for an exhibition project. The 2026 Korean national exhibition student scoring reference is creativity/inquiry 45, theoretical validity 25, direct student participation 15, practicality 15. Check 2027 requirements separately.

**Research geography is open.** Seoul and Gyeongnam are examples, not fixed sites. The DFS/BFS route maintains broad site/data/model exploration and deep implementation only where likely to help the practical research goal.

## Technical artifact

Exact ZIP of locally executed and tested D49 source (6 entries including 3 Python files, test, CSV, README, SHA manifest):
https://drive.google.com/file/d/1xcZ1rsmAxc3bz08tUi07XVOrnEdKXppP/view

ZIP SHA-256: `52c08562aadf2e8c9c2108110012762988c204071218cebee2f5e4112396e130`.

Analysis CSV, original 192 rows:
https://drive.google.com/file/d/1c9A4uY4SCnyuH4dBHQ5q0hTrIUpgmFZZ/view

Native dated reasoning document:
https://docs.google.com/document/d/1E4AhwZObyIgTeexoUdOfKqD4IYGfbPA3-u-EhN4rXls/edit

**The authoritative D49 executable Python source currently lives in the archived ZIP, not in individually verified GitHub Python paths.** This source custody distinction is intentional and must not be concealed. GitHub Actions and github-actions[bot] were not used.

## Experiment

Two consecutive junctions, directional finite vehicle-count link storage, FIFO point queues for east/west through vehicles, separate protected left-turn queues at each junction, and exclusive pedestrian crossing queues. Through, left, pedestrian, clearance phases share a fixed 60-second cycle. At most one waiting road user per second is served for each corresponding lane or crossing. Fixed 16-second between-junction travel time, 1-second time steps, six synthetic arrival cycles, 600-second horizon. A downstream discharge cannot free a link slot for an upstream entry in the same numerical tick.

This is **not** a road safety model and does not validate actual crossing minima or traffic-light intergreen clearance. There is no measured real queue length, actual road geometry, SUMO run, real signal timing, or car-following. D44/D46 physics gates remain outstanding for integrated field claims.

### Small scenario

At directional link capacity K=12, each direction has 12 through vehicles per cycle, each junction 8 protected turns per cycle, and 8 pedestrians per cycle; six cycles.

| Through / left / pedestrian green s | Selected offset s | Mean vehicle wait s | Mean left wait s | Mean pedestrian wait s |
|---|---:|---:|---:|---:|
|18/12/12|10|22.4|23|35|
|24/12/10|0|16.8|24|36|
|30/8/8|58|11.6|29|37|
|20/16/12|44|21.2|12|28|

Lexicographic selection within each split: vehicle unfinished, pedestrian unfinished, completed-vehicle mean wait, then deterministic tie breakers. All arrivals finish in this example. The 30-second through window minimizes average vehicle delay among these four candidate splits, but pedestrian and left-turn waiting are longer than under other splits. No universal recommendation is implied.

### Broad search

4 link capacities (4/8/12/20 vehicles per direction) × 4 sets of demand (through/left/ped per cycle: 12/8/8, 18/8/8, 12/12/10, 8/6/12) × 3 west-direction arrival phases (0/10/20 s) = 48 distinct synthetic cases.

Each case tests 4 candidate phase splits × 60 inter-junction offsets, hence 11,520 distinct evaluations. The CSV contains 192 best-by-split rows. The lexicographic winner split frequencies across 48 cases: 30/8/8 = 22, 24/12/10 = 16, 20/16/12 = 10, 18/12/12 = 0. These are artificially selected scenario counts, not occurrence probabilities or empirical road-policy superiority.

For K=4 some plans leave vehicles unserved at the horizon; treat mean delays as censored. At K=12 and K=20 all vehicle arrivals finish across the tested grid.

### Verification

On 2026-11-12 the original D48 ZIP was re-extracted and its 12 stdlib unittest methods passed. Locally implemented D49 passes 15 stdlib unittest methods, checking phase time budget, strictly integral configuration, disjoint phase clock, arrival validation, road-user conservation each tick, link capacity, intentional blocking, horizon censoring, pedestrian phase and left phase service. ZIP CRC and six-member inventory verified; SHA-256 above. This does not constitute independent field validation.

### Next DFS/BFS research

DFS: pedestrian crossing minimum green and intergreen feasibility constraints, separate conflicting real junction phases, per-movement turn demand and turn-pocket storage/physical blocking, calibrated delay and fairness distributions.

BFS: find a contiguous corridor with synchronized intersection IDs, actual phase plans, turn volumes, geometric lane lengths, pedestrian signals and timestamp-aligned observations. Explore Korea and overseas without deciding the city in advance.

Independent SUMO supports fixed, left-turn and pedestrian phases, priority relationships and actuated control, so these components are prior art (https://sumo.dlr.de/daily/userdoc/Simulation/Traffic_Lights.html). Use SUMO as independent executable comparator once a matched network and signal program are built.
