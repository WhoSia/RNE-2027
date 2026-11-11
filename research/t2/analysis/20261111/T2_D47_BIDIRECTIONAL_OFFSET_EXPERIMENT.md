# D47 — Two-Way Corridor Offset Research, 2026-11-11

## Exhibition-first decision

The project studies **realistic road-network modeling and traffic-signal improvement**, with verification as an engineering prerequisite, not as the goal itself. Site selection remains open (Korean and international datasets). Maintain breadth-first exploration alongside selected depth-first experiments.

For the **2026** Korean National Science Exhibition, the student scoring rubric previously checked is: creativity/inquiry 45, theory 25, student participation 15, practicality 15. Confirm **2027** separately before citing the current rubric. Do not infer award probability.

## New model

- Source: `research/t2/policy/bidirectional_offset_v1.py`
- Tests: `research/t2/policy/test_bidirectional_offset_v1.py`
- 24-case generator: `research/t2/policy/sensitivity_bidirectional_v1.py`
- 2 serial intersections (A and B), 2 opposing straight streams; both streams green concurrently, no turn or pedestrian conflict.
- Deterministic 1-second service events; max 1 vehicle per second per direction per stopline; cycle 60s, green 20s, travel time 16s, horizon 600s.
- Six platoons per direction, 0..59s second-intersection offset; infinite point queues, no finite storage/spillback.
- Two separate objective functions: (1) minimize total unserved then volume-weighted average delay; (2) minimize total unserved then maximum direction-specific average delay. Both methods use fixed synthetic demand and do not infer field improvement.

## Local execution evidence

Python 3.13.5 standard-library unit tests: 10 test methods PASS in local artifact. They cover invalid configuration/arrivals, no demand, all-green equivalence, separate conservation, censoring, candidate ranking, and opposite-direction comparisons. Separate remote runner not executed. Code files were manually committed to the research branch; remote byte-for-byte parity with local ZIP is not yet certified.

| East/west arrivals per cycle | Base mean delay (offset 0) | Optimal average-delay offset | Optimal average delay | Minimax delay offset |
| --- | ---: | ---: | ---: | ---: |
| 12/0 | 26.667s | 8s | 0.000s | 8s |
| 0/12 | 26.667s | 0s | 26.667s | 0s |
| 12/12 | 26.667s | 8s | 22.000s | 0s |
| 18/6 | 26.667s | 14s | 11.000s | 43s |
| 6/18 | 26.667s | 0s | 26.667s | 0s |
| 16/16 | 30.000s | 12s | 22.000s | 44s |

### Key falsifiable result: efficiency versus directional fairness

At East=West=12, phase (0,0), 6 cycles: offset 8 minimizes vehicle-weighted network mean delay (22s), **but worst-direction mean delay rises to 44s**. Offset 0 minimizes worst-direction mean delay (26.667s). Thus different mathematically stated objectives select different synthetic plans. This is a model-dependent example of a known optimization tradeoff, not proof of a novel road phenomenon.

### BFS sensitivity study

8 arrival phase pairs × 3 directional demand ratios = 24 synthetic scenarios, 60 candidate offsets each. Example phase (0,40), demand (12,12): average-delay minimizing offset 32 yields 10s mean delay and 16s worst direction; minimax offset 30 yields 14s worst direction. Relative result depends on arrival patterns.

## Next research decisions

- DFS: phase competition, opposite-direction coordination, heterogeneous green windows and finite receiving/storage constraints; reproduce old D44/D46 defects when integrating physical state.
- BFS: seek accessible true signal plans, directional demands, road geometry and intersection/corridor cases across Korea and other countries; no chosen city yet.
- Keep independent SUMO execution and held-out field evidence on the publication/exhibition acceptance path.
- No GitHub Actions use, no github-actions[bot] contributor, no edits to archived data.
