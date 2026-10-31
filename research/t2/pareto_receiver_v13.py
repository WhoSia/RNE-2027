"""Movement-specific Pareto frontier for fixed site/demand assumptions.

Only compare strategies with identical turn ratio, receiver configuration,
lane allocation, signal and seed design. This is conditional model analysis,
not a recommended civil-engineering decision.
"""
from collections import defaultdict
from pathlib import Path
import json

def nondominated(points):
    for p in points:
        if not all(k in p for k in ("pocket_m","mean_network_S","mean_network_L")):
            raise ValueError("missing network-completed movement outputs")
    return sorted([p for i,p in enumerate(points) if not any(
        j!=i and q["mean_network_S"]>=p["mean_network_S"] and
        q["mean_network_L"]>=p["mean_network_L"] and
        (q["mean_network_S"]>p["mean_network_S"] or
         q["mean_network_L"]>p["mean_network_L"])
        for j,q in enumerate(points))],key=lambda x:x["pocket_m"])

def assess(rows):
    groups=defaultdict(list)
    for r in rows:
        key=(r["turn_share"],r["receiver_slots"],r["receiver_headway_s"],r["B_share"])
        groups[key].append(r)
    out=[]
    for key,items in sorted(groups.items()):
        if len(items)!=4 or len({r["pocket_m"] for r in items})!=4:
            raise ValueError("incomplete paired design")
        front=nondominated(items)
        out.append({"turn_share":key[0],"receiver_slots":key[1],
            "receiver_headway_s":key[2],"B_share":key[3],
            "pareto_pocket_lengths_m":[p["pocket_m"] for p in front],
            "front":[{"pocket_m":p["pocket_m"],
                      "network_S":p["mean_network_S"],"network_L":p["mean_network_L"]}
                      for p in front]})
    return out

if __name__=="__main__":
    root=Path(__file__).resolve().parent/"results"
    rows=json.loads((root/"receiver_summary_v13.json").read_text())
    result=assess(rows)
    (root/"pareto_receiver_v13.json").write_text(json.dumps(result,indent=2)+"\n")
    print("independent scenario strata",len(result))
