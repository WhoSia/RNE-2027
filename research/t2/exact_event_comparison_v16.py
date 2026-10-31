"""Compare exact receiving-link service refusals to end-of-tick occupancy.

4 bay lengths × eight paired seeds, 4 receiving cells, signal offset 0.
Do not equate denied attempts, unique denied vehicle IDs, and occupied
frames. They measure different units and different temporal events.
"""
from dataclasses import replace
from statistics import mean
from collections import Counter
from pathlib import Path
import json
from spatial_v10 import Config,arrivals
from dual_lane_v11 import DualConfig,run
from diagnose_spillback_v16 import diagnose

def evaluate():
    rows=[]
    for seed in range(8):
        base=Config(duration_s=720,demand_vph=1500,left_fraction=.3,seed=seed)
        stream=arrivals(base)
        for pocket in (14.,28.,42.,70.):
            c=DualConfig(base=replace(base,pocket_length_m=pocket),
                through_B_share=.5,receiver_mode="cells",receiver_slots=4,
                downstream_offset_s=0,downstream_green_s=30)
            y=run(c,stream,trace=True)
            d=diagnose(y)
            refused=[e for e in y["service_events"] if e["reason"] in
                     ("receiver_entry_cell_busy","receiver_capacity_full")]
            if len(refused)!=y["receiver_full_denied_s"]:
                raise AssertionError("event count differs from core counter")
            rows.append({"seed":seed,"pocket_m":pocket,
                "network_total":y["network_out_S"]+y["network_out_L"],
                "exact_refusal_attempts":len(refused),
                "unique_refused_vehicle_ids":len({e["vehicle_id"] for e in refused}),
                "receiver_entry_occupied_frames":d["signatures"].get(
                    "receiver_entry_cell_occupied_frames",0),
                "fork_joint_occupancy_frames":d["signatures"].get(
                    "pocket_entry_block_signature_frames",0)})
    return rows

def summary(rows):
    out=[]
    for pocket in (14.,28.,42.,70.):
        group=[r for r in rows if r["pocket_m"]==pocket]
        if len(group)!=8:raise ValueError("missing paired seeds")
        out.append({"pocket_m":pocket,"n":8,**{
            "mean_"+key:mean(r[key] for r in group)
            for key in ("network_total","exact_refusal_attempts",
                        "unique_refused_vehicle_ids",
                        "receiver_entry_occupied_frames",
                        "fork_joint_occupancy_frames")}})
    return out

if __name__=="__main__":
    dest=Path(__file__).resolve().parent/"results"
    dest.mkdir(exist_ok=True)
    rows=evaluate()
    (dest/"exact_events_v16.json").write_text(json.dumps(
        {"rows":rows,"summary":summary(rows),
         "source_status":"SYNTHETIC_NOT_FIELD_CALIBRATED"},indent=2)+"\n")
    print("runs",len(rows))
