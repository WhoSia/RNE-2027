"""T2 v1.7: eight short scoping studies. Synthetic, not field-calibrated.

Per family: three levels, two physical pocket lengths, eight paired seeds.
Changes in arrival schedules are deliberate manipulations of demand timing.
"""
from dataclasses import replace
from itertools import product
from pathlib import Path
from collections import defaultdict
from statistics import mean
import csv,json,hashlib
from spatial_v10 import Config
from dual_lane_v11 import DualConfig,run
from arrival_design_v14 import ArrivalProfile,make_arrivals

FACTORS={
 "rate_timing":("steady","alternating","frontloaded"),
 "turn_timing":("steady","alternating","frontloaded"),
 "through_B_share":(.2,.5,.8),
 "effective_stopline_headway_s":(2,3,4),
 "green_split":("left25","baseline","left45"),
 "downstream_storage_cells":(2,4,8),
 "downstream_phase_offset_s":(0,20,40),
 "downstream_closure":("none","two_15s","two_30s")
}
CLOSURES={"none":(),"two_15s":((180,195),(420,435)),
          "two_30s":((180,210),(420,450))}

def stream(seed,factor,level):
    r={"steady":(1500,),"alternating":(900,2100),
       "frontloaded":(2100,)*6+(900,)*6}
    l={"steady":(.3,),"alternating":(.05,.55),
       "frontloaded":(.55,)*6+(.05,)*6}
    return make_arrivals(ArrivalProfile(duration_s=720,period_s=60,active_s=20,seed=seed,
        rates_vph=r[level] if factor=="rate_timing" else r["steady"],
        left_shares=l[level] if factor=="turn_timing" else l["steady"]))

def case(seed,factor,level,pocket):
    base=Config(duration_s=720,seed=seed,demand_vph=1500,left_fraction=.3,
                pocket_length_m=pocket,left_green_s=35,through_green_s=50)
    c=DualConfig(base=base,through_B_share=.5,receiver_mode="cells",
        receiver_slots=4,receiver_headway_s=2,downstream_green_s=30,downstream_cycle_s=60)
    if factor=="through_B_share":c=replace(c,through_B_share=level)
    elif factor=="effective_stopline_headway_s":
        base=replace(base,departure_headway_s=level)
    elif factor=="green_split":
        left,straight={"left25":(25,60),"baseline":(35,50),
                       "left45":(45,40)}[level]
        base=replace(base,left_green_s=left,through_green_s=straight)
    elif factor=="downstream_storage_cells":c=replace(c,receiver_slots=level)
    elif factor=="downstream_phase_offset_s":c=replace(c,downstream_offset_s=level)
    elif factor=="downstream_closure":c=replace(c,receiver_closures=CLOSURES[level])
    return replace(c,base=base)

def evaluate():
    rows=[]
    for factor,levels in FACTORS.items():
        for level,seed,pocket in product(levels,range(8),(14.,70.)):
            arrivals=stream(seed,factor,level)
            x=run(case(seed,factor,level,pocket),arrivals)
            if x["generated"]!=x["network_out_S"]+x["network_out_L"]+x["remaining"]:
                raise AssertionError("vehicle conservation")
            rows.append({"factor":factor,"level":str(level),"seed":seed,"pocket_m":pocket,
                "arrival_sha":hashlib.sha256(repr(arrivals).encode()).hexdigest(),
                "generated":x["generated"],
                "generated_L":sum(route=="L" for _,route in arrivals),
                "through":x["network_out_S"],
                "left":x["network_out_L"],
                "total":x["network_out_S"]+x["network_out_L"],
                "remaining":x["remaining"],
                "outside_vehicle_seconds":x["outside_vehicle_seconds"],
                "receiver_denials":x["receiver_full_denied_s"]})
    return rows

def summary(rows):
    mapping={(x["factor"],x["level"],x["seed"],x["pocket_m"]):x for x in rows}
    if len(mapping)!=len(rows):raise ValueError("duplicate factorial condition")
    out=[]
    for factor,levels in FACTORS.items():
        for level in levels:
            paired=[(mapping[factor,str(level),i,14.],mapping[factor,str(level),i,70.])
                    for i in range(8)]
            out.append({"factor":factor,"level":str(level),"n_seeds":8,
                "mean_total_14":mean(a["total"] for a,b in paired),
                "mean_total_70":mean(b["total"] for a,b in paired),
                "mean_gain_total":mean(b["total"]-a["total"] for a,b in paired),
                "mean_gain_through":mean(b["through"]-a["through"] for a,b in paired),
                "mean_gain_left":mean(b["left"]-a["left"] for a,b in paired)})
    return out

if __name__=="__main__":
    root=Path(__file__).resolve().parent/"results";root.mkdir(exist_ok=True)
    raw=evaluate()
    with (root/"scoping_384_v17.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(raw[0]))
        writer.writeheader();writer.writerows(raw)
    (root/"scoping_summary_v17.json").write_text(json.dumps(summary(raw),indent=2)+"\n")
    print("synthetic experiments:",len(raw))
