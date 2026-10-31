"""Paired spatial congestion signature factorial, for after-tick snapshots.

4 pocket lengths × 3 receiving lengths × 4 offsets × 8 seeds = 384.
This uses fixed per-seed arrivals and preserves raw network counters.
Frame occupancy is an association, not a proven denial cause.
"""
from dataclasses import replace
from itertools import product
from collections import defaultdict
from statistics import mean
from pathlib import Path
import csv,json
from spatial_v10 import Config,arrivals
from dual_lane_v11 import DualConfig,run
from diagnose_spillback_v16 import diagnose

POCKETS=(14.,28.,42.,70.)
LINKS=(2,4,8)
OFFSETS=(0,15,30,45)
SEEDS=range(8)

def evaluate():
    rows=[]
    for seed in SEEDS:
        base=Config(duration_s=720,seed=seed,demand_vph=1500,left_fraction=.3)
        stream=arrivals(base)
        for pocket,link,offset in product(POCKETS,LINKS,OFFSETS):
            c=DualConfig(base=replace(base,pocket_length_m=pocket),
                through_B_share=.5,receiver_mode="cells",receiver_slots=link,
                downstream_offset_s=offset,downstream_green_s=30)
            x=run(c,stream,trace=True)
            diag=diagnose(x)
            if x["generated"]!=x["network_out_S"]+x["network_out_L"]+x["remaining"]:
                raise AssertionError("mass conservation")
            sig=diag["signatures"]
            rows.append({"seed":seed,"pocket_m":pocket,"link_cells":link,
                "offset_s":offset,"network_S":x["network_out_S"],
                "network_L":x["network_out_L"],
                "network_total":x["network_out_S"]+x["network_out_L"],
                "receiver_denied_attempts":x["receiver_full_denied_s"],
                "pocket_denied_attempts":x["pocket_block_seconds"],
                "receiver_entry_occupied_frames":sig.get("receiver_entry_cell_occupied_frames",0),
                "receiver_and_stopline_frames":sig.get("receiver_occupied_and_stopline_waiting_frames",0),
                "fork_signature_frames":sig.get("pocket_entry_block_signature_frames",0),
                "stopped_vehicle_seconds":diag["stopped_vehicle_seconds_total"]})
    if len(rows)!=384:raise AssertionError("incomplete experiment")
    return rows

def summarize(rows):
    groups=defaultdict(list)
    for row in rows:
        groups[(row["pocket_m"],row["link_cells"],row["offset_s"])].append(row)
    output=[]
    for key,group in sorted(groups.items()):
        if len(group)!=8:raise ValueError("missing seed")
        summary={"pocket_m":key[0],"link_cells":key[1],"offset_s":key[2]}
        summary.update({"mean_"+name:mean(r[name] for r in group)
            for name in group[0] if name not in ("seed","pocket_m","link_cells","offset_s")})
        output.append(summary)
    return output

if __name__=="__main__":
    root=Path(__file__).resolve().parent/"results"
    root.mkdir(exist_ok=True)
    rows=evaluate()
    with (root/"trace_384_v16.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    (root/"trace_summary_v16.json").write_text(json.dumps(summarize(rows),indent=2)+"\n")
    print("runs",len(rows))
