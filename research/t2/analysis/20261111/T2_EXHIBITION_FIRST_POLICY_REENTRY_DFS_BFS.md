# T2 — Exhibition-First Policy Re-entry (2026-11-11)

## Research priority / ownership

**The primary goal is realistic traffic modeling and improved signal/network operation, not the discovery of simulator defects as an end in itself.**

The student science-exhibition strategy values a clearly observed practical problem, creative and direct student investigation, theoretical soundness and usefulness. Prior-art methods are allowed as tools; do not imply originality for existing algorithms. The 2026 competition scoring reference is 45/25/15/15 (creativity/inquiry, theory, direct participation, practicality); reconfirm the 2027 rules. Preserve the exhibition's originality and publication-eligibility constraints.

Research geography is deliberately **not restricted to Changwon**. Investigate Korea (including Seoul and Gyeongnam), plus international datasets when they provide a stronger reference or validation case. The target location is selected after evidence is assessed.

## DFS/BFS research routing

- **BFS:** road geometry, vehicle behavior, arrival demand, signal phases and offsets, network coordination, local candidate sites, observational datasets.
- **DFS:** choose high-value findings and test them deeply with specific hypotheses, implementations, counterexamples, baselines, and reproduction.
- **Backtrack:** if one diagnostic becomes disproportionately expensive or drifts from realistic traffic improvement, preserve the evidence, place it on HOLD, and resume other branches.
- Critical physics failures remain acceptance gates; they must not be hidden or proclaimed fixed.

## First concrete result: synthetic two-signal offset probe

Sources: [offset_probe_v1.py](../../policy/offset_probe_v1.py) and [test_offset_probe_v1.py](../../policy/test_offset_probe_v1.py).

Deterministic 1-second point-queue model; two serial intersections, 60s cycles, 20s green, 16s travel, 72 vehicles in six 12-vehicle platoons; green flow capacity 1 vehicle/s; fixed upstream offset 0; downstream offset swept over 0..59s; 600s horizon. Infinite queue storage, no turns, conflict, bus priority, pedestrians or finite downstream storage.

| Input | Offset | Completed | Mean trip time |
| --- | ---: | ---: | ---: |
| Synthetic baseline | 0s | 72/72 | 42.6667s |
| Synthetic best | 8s | 72/72 | 16.0000s |

Difference: 26.6667s (62.5%) **in this particular synthetic input only**. No real-world travel time was measured or improved. Eight local stdlib unittests passed, including conservation and a no-demand condition. The test script was committed; no GitHub Actions were used. A separate 12-case local sensitivity sweep (travel times 8/16/24/32s × platoon widths 6/12/18s) found offset 0 already optimum for travel 8s and widths 6/12s, countering any universal improvement claim.

**Important:** minimizing unserved vehicles is prioritized before mean completed-trip time. Queue storage is infinite, so this probe **cannot** test the physical spillback mechanism found in earlier T2 development. Its job is to reconnect policy experiments to concrete modeling.

## Next branches (parallel, not sequential blockade)

1. Develop bidirectional corridor demand and competing eastbound/westbound offsets, evaluating delay distribution and asymmetric demand.
2. Reintroduce finite link storage, physical blocking and accepted vehicle events from D46 work only through explicitly compatible interfaces.
3. Map suitable real observed signal/traffic data and independently compare with a pinned SUMO executable; do not label a synthetic optimum as an operational recommendation.
4. Use verified practical evidence to select an exhibition-specific road and question. Publication originality remains a secondary decision.

## Research governance

Retain historical D44/D46 counterexamples; they are crucial test gates but not the primary research question. WhoSia-only human-authored commits, GitHub Actions minimized and never use github-actions[bot] as contributor. GitHub stores code/tests; Drive stores raw datasets and reproducibility archives; native Google Docs stores reasoning and decisions.
