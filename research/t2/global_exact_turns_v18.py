"""Global exact-inventory temporal order stress, synthetic and uncalibrated.
12 seeds x 2 arrival offsets x 4 route orderings x 3 pocket lengths
x 3 downstream offsets = 864 traffic simulator runs.
"""
from itertools import product
from dataclasses import replace
from collections import defaultdict
from statistics import mean
from pathlib import Path
import csv,json,random
from spatial_v10 import Config
from dual_lane_v11 import DualConfig,run
from arrival_design_v14 import ArrivalProfile,make_arrivals

PATTERNS=("random","L_early","L_late","L_distributed")
def reorder(events,pattern,seed):
    if pattern not in PATTERNS:raise ValueError("invalid temporal pattern")
    n=len(events);nleft=sum(r=="L" for _,r in events)
    if pattern=="L_distributed":
        chosen={min(range(n),key=lambda i:(abs((i+.5)/n-(j+.5)/nleft),i))
                for j in range(nleft)} if nleft else set()
        if len(chosen)!=nleft:raise AssertionError("duplicate vehicle slots")
    else:
        indices=list(range(n))
        if pattern=="random":random.Random(seed+103).shuffle(indices)
        elif pattern=="L_late":indices.reverse()
        chosen=set(indices[:nleft])
    return tuple((t,"L" if i in chosen else "S") for i,(t,_) in enumerate(events))

def evaluate():
    rows=[]
    for seed,aoff in product(range(12),(0,30)):
        original=make_arrivals(ArrivalProfile(seed=seed,duration_s=720,
           arrival_offset_s=aoff,rates_vph=(1500,),left_shares=(.3,)))
        for pattern,bay,offset in product(PATTERNS,(14.,28.,70.),(0,20,40)):
            events=reorder(original,pattern,seed)
            c=DualConfig(base=Config(seed=seed,duration_s=720,pocket_length_m=bay),
              receiver_mode="cells",receiver_slots=4,downstream_green_s=30,
              through_B_share=.5,downstream_offset_s=offset)
            r=run(c,events)
            if r["generated"]!=r["remaining"]+r["network_out_S"]+r["network_out_L"]:
                raise AssertionError("vehicle conservation")
            rows.append({"seed":seed,"arrival_offset":aoff,"pattern":pattern,
              "pocket_m":bay,"downstream_offset_s":offset,"generated":r["generated"],
              "generated_L":sum(x=="L" for _,x in events),
              "network_S":r["network_out_S"],"network_L":r["network_out_L"],
              "total":r["network_out_S"]+r["network_out_L"]})
    return rows

if __name__=="__main__":
    root=Path(__file__).resolve().parent/"results";root.mkdir(exist_ok=True)
    rows=evaluate()
    with (root/"global_exact_turns_864_v18.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print("runs",len(rows),"synthetic only")
