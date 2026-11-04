# P10 experimental capacity-time gate and limits
Independent copy of corridor.py: at each tick store each outgoing link occupancy at tick start; when judging new connector entrance require enough link storage against max(start_occupancy,current_occupancy). This blocks use of link storage that is only freed at tick end. The production/original P2 is unchanged.

Original vs adjusted: dt=0.5 vehicle8 entrance 47.0s -> 88.0s; dt=0.125 47.125s -> 87.375s; dt=0.05 47.0s -> 47.15s. No selected retroactive capacity use in eight-grid modified witness. All reported runs have completed=63 and issues=0. But modified dt=0.04 still yields entry87.28s while dt=0.025/.02/.0125/.01 yield entries 47.125/47.12/47.075/47.08s. **Time-grid sensitivity persists**, so this is not a complete numerical repair or proof of convergence.

P9b earlier one-tick connector release gate and P10 capacity release gate repair different temporal relations. Neither proves globally causal event scheduling.
