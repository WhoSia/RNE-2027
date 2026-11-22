"""P31: fresh-seed, route-preserving uniform and four-platoon arrivals (synthetic)."""
from collections import Counter,defaultdict
from dataclasses import replace
from itertools import product
from pathlib import Path
import hashlib,json,pickle

from dual_lane_v11 import run
from spatial_v10 import arrivals
from p19_receiver_service_opportunity import build_config,tape_hash
from p25_p26_physical_followups import action
from p30_unique_vehicle_event_audit import audit_trace

SEED_DEMAND=((124,1650,.50),(125,1650,.50),(126,1800,.45),(127,1800,.45))
FAMILIES=("uniform","platoon4")
PLATOON_ANCHORS=(20,80,140,200)
PLATOON_SPAN=15

def clock(base,family):
    original=arrivals(base)
    route=[v for t,v in original]
    n=len(route);length=base.duration_s
    if n==0:raise ValueError("empty synthetic tape")
    if family=="uniform":
        times=[min(length-1,(2*i+1)*length//(2*n)) for i in range(n)]
    elif family=="platoon4":
        bins=[[i for i in range(n) if (4*i)//n==p] for p in range(4)]
        if any(not b for b in bins):raise ValueError("cohort too small for platoon")
        times=[None]*n
        for p,indices in enumerate(bins):
            for j,i in enumerate(indices):
                times[i]=PLATOON_ANCHORS[p]+(2*j+1)*PLATOON_SPAN//(2*len(indices))
        if max(times)>=length:raise ValueError("platoon outside horizon")
    else:raise ValueError("unknown clock family")
    if times!=sorted(times):raise AssertionError("unsorted tape")
    tape=tuple(zip(times,route))
    if len(tape)!=len(original) or tuple(v for _,v in tape)!=tuple(v for _,v in original):
        raise AssertionError("route labels or counts modified")
    return tape

def experiment():
    rows=[]
    for seed,demand,turn in SEED_DEMAND:
        for family in FAMILIES:
            for cap,offset,pocket,bshare in product((2,4),(0,15),(14.,28.),(0.,.5)):
                cfg=replace(build_config(seed,demand,turn,pocket,cap,bshare),
                            downstream_offset_s=offset)
                tape=clock(cfg.base,family)
                cp=run(cfg,tape,checkpoint_at=84,trace=True)
                frozen=pickle.dumps(cp,protocol=4)
                baseline=run(cfg,tape,resume_from=cp,trace=True)
                branches={}
                for dur in (6,10):
                    result=run(cfg,tape,resume_from=cp,trace=True,phase_overrides=action(dur))
                    if result["generated"]!=len(tape):raise AssertionError("arrival demand mismatch")
                    branches[str(dur)]=audit_trace(result,tape)
                if pickle.dumps(cp,protocol=4)!=frozen:raise AssertionError("checkpoint changed")
                rows.append({"seed":seed,"family":family,"demand_vph":demand,
                  "left_fraction":turn,"receiver_capacity":cap,
                  "downstream_offset_s":offset,"pocket_m":pocket,"b_share":bshare,
                  "tape_sha256":tape_hash(tape),
                  "checkpoint_sha256":hashlib.sha256(frozen).hexdigest(),
                  "six":branches["6"],"ten":branches["10"],
                  "baseline_score":baseline["remaining"]})
    if len(rows)!=128 or len({r["tape_sha256"] for r in rows})!=8:
        raise AssertionError("incomplete fresh-family cohort")
    byfamily=[]
    for family in FAMILIES:
        cohort=[r for r in rows if r["family"]==family]
        effects=Counter()
        for r in cohort:
            a,b=r["six"],r["ten"]
            effects["same_score"]+=a["score"]==b["score"]
            effects["different_score"]+=a["score"]!=b["score"]
            effects["denials_4_more"]+=b["attempts"]-a["attempts"]==4
            effects["denials_other"]+=b["attempts"]-a["attempts"]!=4
            effects["unique_more"]+=b["distinct_rejected_vehicles"]>a["distinct_rejected_vehicles"]
            effects["unique_less"]+=b["distinct_rejected_vehicles"]<a["distinct_rejected_vehicles"]
            effects["same_total_crossings"]+=b["observed_crossing_count"]==a["observed_crossing_count"]
            effects["same_remaining"]+=b["remaining"]==a["remaining"]
        byfamily.append({"family":family,"worlds":len(cohort),**dict(effects)})
    family_tapes={}
    for seed,_,_ in SEED_DEMAND:
        family_tapes[str(seed)]={f:next(r["tape_sha256"] for r in rows if r["seed"]==seed and r["family"]==f) for f in FAMILIES}
    return {"protocol":"P31_NEW_ARRIVAL_FAMILY_STRESS","status":"SYNTHETIC_ONLY",
            "worlds":len(rows),"unique_arrival_tapes":8,"seeds":[s for s,_,_ in SEED_DEMAND],
            "tapes_by_seed":family_tapes,"by_family":byfamily,"records":rows,
            "limitation":"family changes the entire predecision arrival process, not an action at the checkpoint"}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("output",type=Path)
    args=p.parse_args()
    args.output.write_text(json.dumps(experiment(),indent=2,sort_keys=True)+"\n",encoding="utf8")
