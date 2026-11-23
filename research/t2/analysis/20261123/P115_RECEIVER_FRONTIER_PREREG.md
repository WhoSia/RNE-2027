# P115 prereg — receiver-capacity frontier after Claude offset falsification

Committed before P115 result inspection. Exact original T2 unchanged. This is a conditional synthetic falsifier, not a SUMO or field calibration.

- Four preselected tapes: seeds 86001 and 86002 × uniform and platoon4 at demand 900vph and left share .75.
- Capacities 2,3,4,5,6,8,12,16,64 **receiver cells**; physical-equivalent nominal lengths are 7m/cell × C but no surveyed roadway implied. Pocket remains 7m = 1 cell, upstream 140m.
- For EACH receiver capacity, create same-tape paired checkpoints at t84 and compare 30s vs 60s with **both starting red**, meaning offsets phi30=15s, phi60=30s, 50% green.
- Strict all-vehicle completion under extended 4800s horizon; do not compare arbitrary residual penalties. Track `receiver_denied_seconds`, network vehicle-seconds, difference.
- Four tapes × 9 capacities ×2 policies =72 arms = 36 matched comparisons.
- Report paradox (denied_30 < denied_60 AND cost_30 > cost_60), 30-worse cost, absolute cost difference and its sign for EACH capacity. Capacity is the treatment across configurations, with a common predecision **within each capacity**, not across capacities.
- Primary falsifier: at C>=16, fewer paradox cases than at C=4 (precommit criterion). If not, don't claim capacity dominates the local observation.
- Secondary: when comparing C=4 and C=8, inspect whether two signal calendars remain identical; note that the first conditional departure can change with storage.
- The Claude 81/96, 96/96, 32/96, 1/96, 0/96 population counts are external assertions and not inherited as new results. This smaller pilot cannot validate all of them.
