"""D48 breadth-first sweep: 84 synthetic demand/capacity cases, 60 offsets."""
import csv
from finite_storage_offset_v1 import (Config,platoons,sweep,efficiency_key,fairness_key)

HEADER=[
 "capacity_vehicles_each_way","east_vehicles_per_cycle","west_vehicles_per_cycle",
 "east_arrival_phase_s","west_arrival_phase_s",
 "baseline_offset_s","baseline_mean_delay_s","baseline_unserved",
 "baseline_blocked_green_seconds","best_eff_offset_s","best_eff_mean_delay_s",
 "best_eff_unserved","best_eff_blocked_green_seconds","best_fair_offset_s",
 "best_fair_worst_direction_delay_s","best_fair_unserved",
 "policy_offset_changed_vs_unbounded","unbounded_best_offset_s",
 "finite_at_unbounded_offset_unserved","finite_at_unbounded_offset_mean_delay_s",
 "strict_policy_gain_unserved","strict_policy_gain_delay_s"
]

def scenarios():
    for cap in (4,6,8,10,12,20,1000):
        for east_n,west_n in ((12,12),(18,6),(6,18)):
            for east_phase,west_phase in ((0,0),(0,10),(10,0),(0,30)):
                cfg=Config(east_link_capacity=cap,west_link_capacity=cap)
                east=platoons(6,east_n,phase_s=east_phase)
                west=platoons(6,west_n,phase_s=west_phase)
                values=sweep(east,west,cfg)
                best=min(values,key=efficiency_key)
                fair=min(values,key=fairness_key)
                unlimited=min(sweep(east,west,
                    Config(east_link_capacity=1000,west_link_capacity=1000)),
                    key=efficiency_key)
                base=values[0]
                inherited=values[unlimited.offset_B_s]
                unserved_gain=inherited.total_unserved-best.total_unserved
                delay_gain=(inherited.mean_delay_s-best.mean_delay_s
                            if unserved_gain==0 and inherited.mean_delay_s is not None
                            and best.mean_delay_s is not None else 0.0)
                yield (cap,east_n,west_n,east_phase,west_phase,0,
                       base.mean_delay_s,base.total_unserved,base.blocked_green_seconds,
                       best.offset_B_s,best.mean_delay_s,best.total_unserved,
                       best.blocked_green_seconds,
                       fair.offset_B_s,fair.max_direction_mean_delay_s,fair.total_unserved,
                       int(best.offset_B_s!=unlimited.offset_B_s),unlimited.offset_B_s,
                       inherited.total_unserved,inherited.mean_delay_s,
                       unserved_gain,delay_gain)

if __name__=="__main__":
    rows=list(scenarios())
    with open("finite_storage_sweep_84_cases.csv","w",newline="",encoding="utf-8") as fp:
        writer=csv.writer(fp)
        writer.writerow(HEADER)
        writer.writerows(rows)
    print("84 synthetic cases x 60 offsets:",len(rows)*60)
    print("different best offset:",sum(row[16] for row in rows))
    print("fewer unfinished vehicles:",sum(row[20]>0 for row in rows))
    print("same unfinished count, less mean delay:",sum(row[21]>1e-9 for row in rows))
