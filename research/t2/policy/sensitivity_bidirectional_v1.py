"""Regenerate 24-case synthetic directional offset sensitivity table."""
import csv
from bidirectional_offset_v1 import Parameters, platoons, sweep, efficiency_key, fairness_key

def rows():
    p=Parameters()
    for east_phase, west_phase in [(0,0),(0,10),(0,20),(0,40),(10,0),(10,30),(0,30),(10,10)]:
        for east_n, west_n in [(12,12),(18,6),(6,18)]:
            values=sweep(platoons(6,east_n,phase_s=east_phase),
                         platoons(6,west_n,phase_s=west_phase),p)
            base=values[0]
            eff=min(values,key=efficiency_key)
            fair=min(values,key=fairness_key)
            yield [east_phase,west_phase,east_n,west_n,
                   round(base.network_mean_delay_s,6),
                   eff.offset_B_s,round(eff.network_mean_delay_s,6),
                   round(eff.worst_direction_mean_delay_s,6),
                   fair.offset_B_s,round(fair.network_mean_delay_s,6),
                   round(fair.worst_direction_mean_delay_s,6),
                   eff.total_unserved,fair.total_unserved]

HEADER=["east_phase_s","west_phase_s","east_per_cycle","west_per_cycle",
        "baseline_mean_delay_s","eff_offset_s","eff_mean_delay_s",
        "eff_worst_dir_mean_delay_s","fair_offset_s","fair_mean_delay_s",
        "fair_worst_dir_mean_delay_s","unserved_eff","unserved_fair"]

if __name__=="__main__":
    with open("sensitivity_24_cases.csv","w",newline="",encoding="utf-8") as fp:
        writer=csv.writer(fp)
        writer.writerow(HEADER)
        writer.writerows(rows())
    print("Wrote sensitivity_24_cases.csv: 24 scenarios x 60 offsets")
