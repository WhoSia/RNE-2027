# T2-PHYS-01 — objective sensitivity, full screened factorial

The cost is accumulated outside + upstream + receiving vehicle-seconds, plus `p × remaining_at_720s`. Each original run's state and physical movement rules are unchanged when recomputing alternative values p∈{0,30,60,120}; these are secondary cost interpretations, not reruns or retuned generators.

| Terminal remaining penalty p | Strict preference reversals / 48 lane-rule pairs | Zero sign differences |
|---:|---:|---:|
| 0 | 15 | 0 |
| 30 | 15 | 0 |
| 60 (predeclared primary) | 16 | 0 |
| 120 | 15 | 0 |

**14/48** strict reversals persist in all four objectives; they are the stable core. The specific p=60 extra keys are (seed 0,pocket14m,Bshare0), which is absent at p=0/30, and (seed 4,pocket28m,Bshare0), which is absent at p=120. This makes the terminal-cost dependence visible rather than hiding it.

For this 7-m cell model, changing lane-change permission on a known fixed geometry is causal **within the simulation**, but changes the whole 720-second trajectory from its first tick. It does not isolate a specific decision at tick 84 under strictly equal full microstate, and does not imply a field controller's achievable benefit.

All source SHA-1 and complete-output SHA-256 are in [run receipt](PHYS_192_RUN_RECEIPT.md). The full 48 matched contrasts under three penalties are in [paired CSV](physical_192_paired_costs.csv); p=30 can be recomputed from raw occupancy and terminal counts. All 192 original runs, including the least favorable ones, were included.
