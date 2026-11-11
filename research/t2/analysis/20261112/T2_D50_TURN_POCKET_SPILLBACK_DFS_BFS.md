# T2 D50 — Short Left-Turn Pocket and Through-Queue Interference (2026-11-12)

## Core goal: exhibition first
The project must solve/measure real traffic engineering problems with original student inquiry, not demand a globally novel control algorithm. The four 2026 National Science Exhibition student criteria used in our research decisions were creativity/inquiry 45, theoretical validity 25, direct participation 15, and practicality 15; verify 2027 criteria before final submission. No city is preselected: Changwon is one option among Korean and international sites. DFS/BFS: examine multiple problem branches, intensify promising ones, and return to broader exploration if a subproblem swallows the agenda.

## D49 -> D50 development
D49 models through/left/pedestrian phases but separate source queues. D50 local Python model implements **one mixed FIFO source feeder** with a finite left-turn storage bay and a separate finite through bay. A leading left-turner blocked by full turning pocket traps later through cars in that *shared feeder*. The alternate topology has **two separate feeder lanes**: this comparison is structurally confounded and is not a controlled estimate of only pocket capacity's effect.

Timing: integer 1s ticks; 60s cycle; through green 24s; protected-left green 12s; source arrivals 6 cycles × 18 vehicles, every third vehicle left; 600s horizon. Admission uses pre-tick bay occupancy, not space freed by downstream service in the same tick. Storage units are vehicles, not meters. Source queues unbounded. No physical braking, vehicle footprint, crossing conflict, downstream coordination, pedestrian model, independently executed SUMO, or field calibration.

### Local deterministic result
Left pocket capacity K and mean through-vehicle time from upstream arrival to stopline crossing, **shared feeder**:
- K=1: 78.7778s
- K=2: 36.1944s
- K=3: 26.2500s
- K=4: 16.5833s
- K>=6 (tested 6/8/12/20): 1.0000s
The two-independent-feeder topology gives 1.0000s in this example for each K, but two feeders may admit one each in the same tick; source topology differs. Both variants fully completed all 108 arrivals (72 through + 36 left) in the example. Baseline 1s is an artificial tick admission delay, not measured traffic delay.

### Breadth-first sensitivity
3 platoon sizes (12,18,24) × 3 left fractions (every 2nd, 3rd, 4th vehicle) × 4 arrival phases (0,10,20,30s) × 8 bay capacities (1,2,3,4,6,8,12,20) = **288 synthetic scenarios**.
- Both configurations completely served their own demand before the horizon in 273 scenarios.
- Among these, 91 shared-feeder scenarios had strictly greater through average delay than the independent-feeder version.
- An explicit queue event with through cars trapped behind an overflowed left head occurred in 115/288 scenarios. This counter is time with a trapped T in source FIFO, not directly 'lost through green'.
- **Controlled within-shared-lane comparison:** across the 36 independent demand/phase combinations, 26 were fully served for both K=1 and K=12; in 22 of those 26, K=12 strictly reduced through mean delay relative to K=1. This is a better topology-controlled comparison, but is still synthetic.

### Local tests and custody
Python stdlib unittest: **13/13 tests pass**, verifying source sorting/ID validity, conservation, storage bounds, trapping, phase effects and comparisons. Reproducible code, tests, sensitivity CSV, README and per-file SHA manifest are packed in ZIP.
ZIP SHA-256: `5516c9e018fd2ce93c817f5a21013b27556017179d7a6bbd9e5d9ebe125ff65d`
Drive ZIP: https://drive.google.com/file/d/1TgD3ZWaSO3KmjvXdNulquYfD1tmZr_7i/view
Drive CSV: https://drive.google.com/file/d/1x1fGNCN5iOQdNJ-_0I1G1bYeqpXLER8B/view
Reasoning document: https://docs.google.com/document/d/1y6iGChW-FwddaLICIYOPzRlnThWsrJbWfsMm7vKnezA/edit

**Important:** the executable D50 source is archived in the Drive ZIP; unless separately committed, this GitHub file is the research ledger, not a claim that the Python module is on the remote branch. No GitHub Actions or github-actions[bot] contributions.

### Prior research establishes this is known mechanics
FHWA Traffic Signal Timing Manual ch. 6: https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter6.htm
Zhang & Tong 2008, https://doi.org/10.3141/2071-09
Yin, Zhang & Wang 2011, https://doi.org/10.3141/2257-12
Wei et al. 2021, https://doi.org/10.1177/03611981211006433
NCHRP 812 ch. 12 distinguishes storage bay spillback from storage bay blocking. Do not claim global first-invention of either phenomenon.

## Backtracking/next research
DFS: introduce actual diverge point and vehicle lengths/road geometry, test leading vs lagging protected-left phasing. BFS: find reliable raw signal phase plans + turning movement counts + road geometry + queue measurements for candidate corridors. Retain independent SUMO and holdout field evidence as acceptance gates. Do not select a city only because data catalog exists.
