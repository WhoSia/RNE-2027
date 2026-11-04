# Identical-input model replay

Exact same vehicle list (ID, arrival time, origin, passenger/truck class) fed to two isolated Python processes for the two P1 source trees. Three independent seeds 941-943, WALK restriction 0 or 8s, storage 30 or 100m. 24 simulation executions = 12 code-lineage pairs at 360s.

Mean P1b minus P1a exposure (vehicle-seconds) and completed vehicles:
- WALK0, storage30: +1202.583, -5.667; storage100: +1358.417, -5.667.
- WALK8, storage30: +729.417, -2.333; storage100: +870.417, -2.333.
Under WALK8 the policies differ by time placement and cannot be interpreted as algorithm performance on identical signals.
All 24 still had incomplete vehicles: use finite-horizon occupancy exposure, not all-complete travel times. Across 24: 0 recorded braking, queue, duplicate-membership, sampled polygon or independently audited connector interval/WALK overlap. Absence of observed failures does not prove continuous-time or field safety.
A/B source audit from original ZIPs: A 56 historical tests passed; B 49 historical tests passed; new replay harness 6 passed.