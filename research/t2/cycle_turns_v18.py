"""Reassign left/through labels within each complete signal cycle, preserving exact vehicle counts.
Same timestamps and per-cycle route multisets; synthetic counterfactual ONLY.
"""
from collections import defaultdict
from dataclasses import replace
from itertools import product
from statistics import mean
from pathlib import Path
import csv,json,random
from spatial_v10 import Config
from dual_lane_v11 import DualConfig,run
from arrival_design_v14 import ArrivalProfile,make_arrivals

PROFILES=("random","L_first","L_last","L_even")

def arrange_cycle(events,profile,seed,cycle=120):
    if profile not in PROFILES or not isinstance(cycle,int) or cycle<=0:
        raise ValueError("invalid ordering/period")
    groups=defaultdict(list)
    for i,(t,route) in enumerate(events):
        groups[t//cycle].append((i,t,route))
    out=list(events)
    for period,items in groups.items():
        n=len(items);left=sum(m=="L" for _,_,m in items)
        positions=list(range(n))
        if profile=="random":random.Random(seed*271+period).shuffle(positions)
        elif profile=="L_last":positions.reverse()
        elif profile=="L_even":
            selected=set()
            if left:
                selected={min(range(n),key=lambda i:(abs((i+.5)/n-(j+.5)/left),i))
                          for j in range(left)}
                if len(selected)!=left:raise AssertionError("nonunique distributed positions")
            for j,(idx,t,_) in enumerate(items):
                out[idx]=(t,"L" if j in selected else "S")
            continue
        selected=set(positions[:left])
        for j,(idx,t,_) in enumerate(items):
            out[idx]=(t,"L" if j in selected else "S")
    return tuple(out)

def evaluate():
    rows=[]
    for seed in range(8):
        original=make_arrivals(ArrivalProfile(seed=seed,duration_s=720,
                                     rates_vph=(1500,),left_shares=(.3,)))
        for pattern,order,offset,bay in product(PROFILES,("leading","lagging"),
                                                (0,30),(14.,28.,70.)):
            stream=arrange_cycle(original,pattern,seed)
            c=DualConfig(base=Config(seed=seed,duration_s=720,phase_order=order,
                         pocket_length_m=bay),receiver_mode="cells",receiver_slots=4,
                         through_B_share=.5,downstream_green_s=30,
                         downstream_offset_s=offset)
            y=run(c,stream)
            if y["generated"]!=y["remaining"]+y["network_out_S"]+y["network_out_L"]:
                raise AssertionError("vehicle conservation")
            rows.append(dict(seed=seed,profile=pattern,phase=order,
                downstream_offset_s=offset,pocket_m=bay,
                network_S=y["network_out_S"],network_L=y["network_out_L"],
                total=y["network_out_S"]+y["network_out_L"],
                pocket_block_s=y["pocket_block_seconds"]))
    return rows

def summarize(rows):
    groups=defaultdict(list)
    for r in rows:
        groups[(r["profile"],r["phase"],r["downstream_offset_s"],r["pocket_m"])].append(r)
    result=[]
    for key,group in sorted(groups.items()):
        if len(group)!=8:raise ValueError("missing paired seeds")
        result.append(dict(zip(("profile","phase","downstream_offset_s","pocket_m"),key),
            mean_total=mean(r["total"] for r in group),
            mean_S=mean(r["network_S"] for r in group),
            mean_L=mean(r["network_L"] for r in group),
            mean_pocket_block_s=mean(r["pocket_block_s"] for r in group)))
    return result

if __name__=="__main__":
    root=Path(__file__).resolve().parent/"results"
    root.mkdir(exist_ok=True)
    rows=evaluate()
    with (root/"cycle_turns_384_v18.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (root/"cycle_turns_summary_v18.json").write_text(json.dumps(summarize(rows),indent=2)+"\n")
    print("synthetic cases",len(rows))
