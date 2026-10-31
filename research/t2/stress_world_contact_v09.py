"""T2 v0.9 factorial stress suite. No field-data claims.

Run: python research/t2/stress_world_contact_v09.py [output.json]
All geometry/policy counterfactuals use exactly the same time-stamped
arrival stream within each seed and arrival-pattern condition.
"""
from __future__ import annotations
from dataclasses import replace
from statistics import mean
from pathlib import Path
import json,sys,hashlib
from world_contact_v09 import Params,demand,run

def execute():
    rows=[]
    for pattern in ("uniform","platoon"):
        for seed in range(8):
            base=Params(seed=seed,arrival_pattern=pattern)
            events=demand(base)
            digest=hashlib.sha256(repr(events).encode()).hexdigest()
            for mode in ("fifo","bypass"):
                for length in (14,28,42,70):
                    for storage in (28,56,112):
                        c=replace(base,feeder_policy=mode,bay_length_m=length,
                                  straight_storage_m=storage)
                        y=run(c,events)
                        rows.append({"pattern":pattern,"seed":seed,
                            "policy":mode,"bay_m":length,"straight_m":storage,
                            "arrival_sha256":digest,"generated":y["generated"],
                            "admitted":y["admitted"],"exits_S":y["exits_S"],
                            "exits_L":y["exits_L"],"outside":y["still_outside"],
                            "left_block_s":y["blocked_L_seconds"],
                            "insertion_delay_s":y["insertion_delay_affected_seconds"]})
    # One JSON file: all raw runs and explicit descriptive summaries.
    summary=[]
    for pattern in ("uniform","platoon"):
        for policy in ("fifo","bypass"):
            for straight in (28,56,112):
                for length in (14,28,42,70):
                    z=[r for r in rows if (r["pattern"],r["policy"],r["straight_m"],r["bay_m"])==
                       (pattern,policy,straight,length)]
                    summary.append({"pattern":pattern,"policy":policy,
                        "straight_m":straight,"bay_m":length,"n_seeds":len(z),
                        "mean_S":mean(r["exits_S"] for r in z),
                        "mean_L":mean(r["exits_L"] for r in z),
                        "mean_outside":mean(r["outside"] for r in z),
                        "mean_block_s":mean(r["left_block_s"] for r in z)})
    return {"status":"SYNTHETIC_UNCALIBRATED","runs":rows,"summary":summary,
            "caution":"Factorial changes include a policy ablation, not measured driver behavior."}

if __name__=="__main__":
    o=Path(sys.argv[1] if len(sys.argv)>1 else "research/t2/results/world_contact_v09.json")
    o.parent.mkdir(exist_ok=True,parents=True)
    data=execute()
    o.write_text(json.dumps(data,indent=2)+"\n")
    print("runs",len(data["runs"]),"summaries",len(data["summary"]))
