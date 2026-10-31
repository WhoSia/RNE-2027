"""Matched two-intersection cellular receiving-link experiment.

4 pocket lengths * 3 downstream lengths * 4 downstream phase offsets
* 2 downstream green durations * 6 paired demand seeds = 576 runs.
All conditions reuse identical per-seed time-stamped demand.
Outputs are synthetic and NOT calibrated to a real intersection.
"""
from dataclasses import replace
from itertools import product
from statistics import mean
from collections import defaultdict
from pathlib import Path
import hashlib,csv,json
from spatial_v10 import Config,arrivals
from dual_lane_v11 import DualConfig,run

LENGTHS=(14.,28.,42.,70.)
LINKS=(2,4,8)
OFFSETS=(0,15,30,45)
GREENS=(15,30)
SEEDS=range(6)

def evaluate():
    rows=[]
    for seed in SEEDS:
        base=Config(duration_s=720,seed=seed,left_fraction=.3,demand_vph=1500)
        stream=arrivals(base)
        fingerprint=hashlib.sha256(repr(stream).encode()).hexdigest()
        for pocket,link,offset,green in product(LENGTHS,LINKS,OFFSETS,GREENS):
            c=DualConfig(base=replace(base,pocket_length_m=pocket),
                through_B_share=.5,receiver_mode="cells",
                receiver_slots=link,receiver_headway_s=2,
                downstream_green_s=green,downstream_offset_s=offset)
            result=run(c,stream)
            if result["generated"]!=result["network_out_S"]+result["network_out_L"]+result["remaining"]:
                raise AssertionError("network mass conservation")
            rows.append({"seed":seed,"pocket_m":pocket,"downstream_cells":link,
                "downstream_offset_s":offset,"downstream_green_s":green,
                "arrival_sha":fingerprint,"generated":result["generated"],
                "stopline_S":result["exit_S"],"stopline_L":result["exit_L"],
                "network_S":result["network_out_S"],"network_L":result["network_out_L"],
                "network_total":result["network_out_S"]+result["network_out_L"],
                "remaining":result["remaining"],
                "receiver_full_denied_s":result["receiver_full_denied_s"],
                "outside_vehicle_seconds":result["outside_vehicle_seconds"]})
    return rows

def summarize(rows):
    groups=defaultdict(list)
    for r in rows:
        key=(r["pocket_m"],r["downstream_cells"],r["downstream_offset_s"],r["downstream_green_s"])
        groups[key].append(r)
    output=[]
    for key,group in sorted(groups.items()):
        if len(group)!=len(SEEDS):raise AssertionError("missing paired seed")
        output.append({"pocket_m":key[0],"downstream_cells":key[1],
            "downstream_offset_s":key[2],"downstream_green_s":key[3],
            "mean_network_S":mean(x["network_S"] for x in group),
            "mean_network_L":mean(x["network_L"] for x in group),
            "mean_total":mean(x["network_total"] for x in group),
            "mean_blocked_s":mean(x["receiver_full_denied_s"] for x in group),
            "mean_outside_vehicle_seconds":mean(x["outside_vehicle_seconds"] for x in group)})
    return output

if __name__=="__main__":
    root=Path(__file__).resolve().parent/"results"
    root.mkdir(exist_ok=True)
    rows=evaluate()
    with (root/"linked_576_v15.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    (root/"linked_summary_v15.json").write_text(json.dumps(summarize(rows),indent=2)+"\n")
    print("runs",len(rows),"condition_means",len(summarize(rows)))
