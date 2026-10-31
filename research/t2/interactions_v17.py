"""T2 v1.7 paired two-factor scouting: lane mix × outages; turn pulse × phase."""
from dataclasses import replace
from itertools import product
from pathlib import Path
from statistics import mean
import csv,json
from spatial_v10 import Config
from dual_lane_v11 import DualConfig,run
from scoping_v17 import stream,case,CLOSURES

STUDIES={
  "lane_x_closure":((.2,.5,.8),("none","two_15s","two_30s")),
  "turn_x_phase":(("steady","alternating","frontloaded"),("leading","lagging")),
}
def evaluate():
    rows=[]
    for study,(aa,bb) in STUDIES.items():
        for a,b,seed,pocket in product(aa,bb,range(8),(14.,70.)):
            if study=="lane_x_closure":
                c=replace(case(seed,"through_B_share",a,pocket),receiver_closures=CLOSURES[b])
                arrivals=stream(seed,"rate_timing","steady")
            else:
                c=case(seed,"turn_timing",a,pocket)
                c=replace(c,base=replace(c.base,phase_order=b))
                arrivals=stream(seed,"turn_timing",a)
            x=run(c,arrivals)
            if x["generated"]!=x["network_out_S"]+x["network_out_L"]+x["remaining"]:
                raise AssertionError("vehicle conservation")
            rows.append({"study":study,"a":str(a),"b":str(b),"seed":seed,
                "pocket_m":pocket,"through":x["network_out_S"],
                "left":x["network_out_L"],
                "total":x["network_out_S"]+x["network_out_L"]})
    return rows

def summarize(rows):
    idx={(r["study"],r["a"],r["b"],r["seed"],r["pocket_m"]):r for r in rows}
    if len(idx)!=len(rows):raise ValueError("duplicate intervention")
    output=[]
    for study,(aa,bb) in STUDIES.items():
        for a,b in product(aa,bb):
            delta=[idx[study,str(a),str(b),i,70.]["total"]-
                   idx[study,str(a),str(b),i,14.]["total"] for i in range(8)]
            output.append({"study":study,"a":str(a),"b":str(b),
                "mean_long_pocket_gain":mean(delta),
                "per_seed_differences":delta})
    return output

if __name__=="__main__":
    root=Path(__file__).resolve().parent/"results";root.mkdir(exist_ok=True)
    raw=evaluate()
    with (root/"interactions_240_v17.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(raw[0]))
        w.writeheader();w.writerows(raw)
    (root/"interactions_summary_v17.json").write_text(json.dumps(summarize(raw),indent=2)+"\n")
    print("synthetic paired interaction runs:",len(raw))
