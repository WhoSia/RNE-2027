"""Holdout seed court for paired pocket x downstream offset contrasts.

Seeds 100-119 are deliberately disjoint from exploratory 0-5.
2 link sizes * 2 pocket lengths * 4 downstream offsets * 20 seeds
= 320 synthetic tests, with common arrivals within each seed.
"""
from dataclasses import replace
from itertools import product
from statistics import mean
from pathlib import Path
import json
from spatial_v10 import Config,arrivals
from dual_lane_v11 import DualConfig,run

def evaluate():
    rows=[]
    for seed in range(100,120):
        base=Config(duration_s=720,demand_vph=1500,seed=seed,left_fraction=.3)
        stream=arrivals(base)
        for length,pocket,offset in product((2,8),(14.,70.),(0,15,30,45)):
            c=DualConfig(base=replace(base,pocket_length_m=pocket),
                through_B_share=.5,receiver_mode="cells",receiver_slots=length,
                downstream_green_s=30,downstream_offset_s=offset)
            r=run(c,stream)
            rows.append({"seed":seed,"cells":length,"pocket":pocket,"offset":offset,
                "network_S":r["network_out_S"],"network_L":r["network_out_L"],
                "total":r["network_out_S"]+r["network_out_L"]})
    return rows

def summarize(rows):
    data={(r["seed"],r["cells"],r["pocket"],r["offset"]):r for r in rows}
    out=[]
    for cells,offset in product((2,8),(0,15,30,45)):
        differences=[data[(seed,cells,70.,offset)]["total"]-
             data[(seed,cells,14.,offset)]["total"] for seed in range(100,120)]
        out.append({"cells":cells,"offset":offset,"n":len(differences),
           "paired_total_gain_mean":mean(differences),"min":min(differences),
           "max":max(differences),"nonnegative":sum(d>=0 for d in differences)})
    return out

if __name__=="__main__":
    output=Path(__file__).resolve().parent/"results"
    output.mkdir(exist_ok=True)
    rows=evaluate()
    (output/"holdout_link_v15.json").write_text(json.dumps({
        "seed_source":"UNUSED_100_119","runs":rows,"summary":summarize(rows)
    },indent=2)+"\n")
    print("holdout simulations",len(rows))
