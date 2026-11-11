# T2 D48 — Finite-Storage Corridor Signal Optimization (2026-11-11)

## EXHIBITION-FIRST DECISION

Research priority: solve observable traffic problems using realistic network modeling and feasible signal control. A wholly novel algorithm is not required for the exhibition; prior-art ideas may be used and improved. 2026 exhibition scoring previously checked: creativity/inquiry 45, theoretical validity 25, participation 15, practicality 15. Recheck the 2027 rules.

Geography is not restricted to Changwon. DFS/BFS strategy: explore many real roads and modeling features broadly; intensify high-value branches; preserve tested subproblems and backtrack when depth displaces the overall aim.

## D48 FINITE LINK IMPLEMENTATION

Extend D47 two-way offset exploration with finite vehicle-count link capacity between intersections A and B in each direction.

Model assumptions: two simultaneous straight greens; 60-second signal cycle; 20-second green; travel 16 seconds; upstream service at most one vehicle per second and direction; six synthetic platoons of 12 vehicles per cycle each direction; horizon 600 seconds. Cars occupy finite link slots until exiting downstream; upstream source queues remain unbounded. Upstream admission checks pre-tick occupancy, so a downstream exit cannot free space for admission in that same tick. This is a conservative model convention. No physical queue-tail wave, turn pocket, pedestrian movement, actual metric road width, or calibration is claimed.

Performance objective: minimize incomplete vehicles first, mean delay of completed trips second. Secondary fairness objective: minimize maximum direction mean delay given minimum incomplete vehicles. Avoid comparing mean delays alone when unfinished counts differ.

### Local result (identical bidirectional demand)

| Capacity per directional link (vehicles) | Best offset (s) | Mean delay (s) | Unfinished | Blocked upstream green-seconds |
|---:|---:|---:|---:|---:|
|4|0|132.8955|10|260|
|6|0|80.7222|0|176|
|8|0|41.2361|0|108|
|10|0|26.6667|0|84|
|12|8|22.0000|0|0|
|20|8|22.0000|0|0|
|1000|8|22.0000|0|0|

Synthetic mechanism: receiving capacity can change the selected signal offset. This is not a conclusion about actual road policy performance.

### BFS sensitivity

Seven capacity levels x three directional demand ratios x four arrival-phase pairs = 84 synthetic cases x 60 offsets = 5,040 finite-case evaluations. Each case also computes an unbounded reference policy and re-evaluates that policy in the finite case.

37/84 finite cases show strictly better lexicographic performance when the offset is chosen with finite storage rather than transferred from the unbounded case. In 20 cases unfinished vehicles are fewer; in 17 cases unfinished vehicles are equal but completed-trip mean delay is shorter. These are model-specific counts, not real-world probabilities.

### Local tests and custody

12/12 Python 3.13.5 standard-library tests pass locally: finite occupancy, tick-level conservation, config validation, empty input, censored unfinished trips, no same-tick release reuse, D47 agreement when capacity is nonbinding, and directional fairness.

Local experimental ZIP SHA-256: 0933d75c561e87790d89a0ad5376a5ae5c5e63f9958f534c7a19549b57a53571. GitHub sources were independently transcribed from local sources and remote byte-for-byte correspondence or remote execution is NOT certified. No GitHub Actions or github-actions[bot] were used.

CSV preserved in the reproducibility folder:
https://drive.google.com/file/d/180T1bD72mIg3HzReHyByF25BgBPlHE1C/view

### Data BFS — discovery, not acquisition

Official Seoul T-Data https://t-data.seoul.go.kr/ includes smart-intersection traffic volume (10/15-minute) and signal-related catalog entries. Seoul open data OA-21661 and OA-21662 also describe V2X signal timing/status products. Listing does not prove full-cycle usable phasing for selected adjacent intersections. No actual signal or traffic volume record ingested.

Next: (1) quantify alternative event-tick conventions, (2) implement competing through/turn/pedestrian signal phases, (3) evaluate a real corridor once raw original records and observable queue measurements are available, (4) independent SUMO with matched signals/geometry and real validation. Preserve prior D44/D46 failures; do not allow defect research to swallow the practical exhibition goal.
