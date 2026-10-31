"""Paired finite receiving-link experiment: 1152 synthetic runs.

2 turn ratios * 8 seeds * 4 pocket lengths * 3 receiver capacities
* 3 discharge headways * 2 B lane allocations. Model-only, no calibration.
"""
from dataclasses import replace
from itertools import product
from pathlib import Path
from statistics import mean
import hashlib,csv,json
from dual_lane_v11 import DualConfig,run
from spatial_v10 import Config,arrivals

POCKETS=(0.,14.,28.,70.)
RECEIVER_SLOTS=(1,2,4)
HEADWAYS=(2,4,8)
LEFT_SHARES=(.3,.5)
LANE_B_SHARES=(.5,1.)
SEEDS=range(8)

def evaluate():
    rows=[]
    for share,seed in product(LEFT_SHARES,SEEDS):
        base=Config(duration_s=720,demand_vph=1500,left_fraction=share,seed=seed)
        stream=arrivals(base)
        sha=hashlib.sha256(repr(stream).encode()).hexdigest()
        for pocket,slots,head,split in product(POCKETS,RECEIVER_SLOTS,HEADWAYS,LANE_B_SHARES):
            c=DualConfig(base=replace(base,pocket_length_m=pocket),
                through_B_share=split,receiver_slots=slots,receiver_headway_s=head)
            r=run(c,stream)
            if r["generated"]!=r["network_out_S"]+r["network_out_L"]+r["remaining"]:
                raise AssertionError("network conservation")
            rows.append({"turn_share":share,"seed":seed,"stream_sha":sha,
                "pocket_m":pocket,"receiver_slots":slots,"receiver_headway_s":head,
                "B_share":split,"generated":r["generated"],"stopline_S":r["exit_S"],
                "stopline_L":r["exit_L"],"network_S":r["network_out_S"],
                "network_L":r["network_out_L"],"receiver_final":r["receiver_final"],
                "receiver_full_denied_s":r["receiver_full_denied_s"]})
    return rows

def summarize(rows):
    output=[]
    for share,pocket,slots,head,split in product(LEFT_SHARES,POCKETS,RECEIVER_SLOTS,HEADWAYS,LANE_B_SHARES):
        group=[r for r in rows if (r["turn_share"],r["pocket_m"],r["receiver_slots"],
            r["receiver_headway_s"],r["B_share"])==(share,pocket,slots,head,split)]
        if len(group)!=8:raise AssertionError("missing seed")
        output.append({"turn_share":share,"pocket_m":pocket,"receiver_slots":slots,
            "receiver_headway_s":head,"B_share":split,
            "mean_stopline_S":mean(r["stopline_S"] for r in group),
            "mean_network_S":mean(r["network_S"] for r in group),
            "mean_stopline_L":mean(r["stopline_L"] for r in group),
            "mean_receiver_full_denied_s":mean(r["receiver_full_denied_s"] for r in group)})
    return output

if __name__=="__main__":
    dest=Path(__file__).resolve().parent/"results"
    dest.mkdir(exist_ok=True)
    rows=evaluate()
    with (dest/"receiver_1152_v13.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (dest/"receiver_summary_v13.json").write_text(json.dumps(summarize(rows),indent=2)+"\n")
    print("synthetic runs",len(rows))
