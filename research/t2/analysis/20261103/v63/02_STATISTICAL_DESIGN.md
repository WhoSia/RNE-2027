# T2 v6.3-P0: Experimental design and pseudoreplication audit

Date 20261103. The historical v6.2 2×2 mechanism experiment has **144 executions but only 36 paired demand×seed blocks**, using 12 distinct random seeds reused across 3 demand labels. Do not treat 144 output rows as independent observations. The main-effect contrasts are computed within each 4-cell block. Resample entire **seed clusters** across all three demands for uncertainty summaries.

Verified from original v6.2 CSV: mean effect of +1s green guard = +48.0486 vehicle·seconds; preserving connector overshoot = -12.7222 vehicle·seconds; interaction = -2.7222 vehicle·seconds. Seed-cluster bootstrap (10,000 resamples; fixed pseudo-random seed) illustrative percentile intervals: guard [+2.90,+95.63], overshoot [-28.46,-3.41], interaction [-8.28,+0.14] vehicle·seconds. These intervals quantify sensitivity to selected synthetic seeds, NOT confidence about real traffic. For guard effect 12/36 blocks positive, 24/36 zero, none negative; overshoot effect negative all 36 blocks. One baseline block recorded braking violations (288 warning ticks), cleared by guard.

Further experiment: 3 demand rates × 3 brake bounds × 2 lateral acceleration bounds × 8 seeds × 2 guards = 288 simulations / 144 matched pairs; do not count warning time ticks as independent events. Distinguish policy service-time cost from safety. Separate synthetic model output, theoretical necessary conditions, independent SUMO validation, and empirical road evidence.

Decision criteria: no unconditional physical safety claim, no traffic policy improvement claim without matched field or external simulation baseline. Report per-scenario failures, not merely pooled means.
