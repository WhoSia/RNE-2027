"""RF14 synthetic integration contract. No radio acquisition or physical claims."""
import hashlib
import json

def index(rows):
    result={}
    for r in rows:
        k=r["trial_id"]
        if not isinstance(k,str) or not k.strip() or k in result:
            raise ValueError("invalid or duplicate trial ID")
        result[k]=r
    return result

def exact(expected, rows):
    d=index(rows)
    if set(expected)!=set(d):
        raise ValueError("planned denominator mismatch")
    return d

def active_plan(plan):
    d=index(plan)
    allowed={("S1","P1"),("S2","P1"),("S2","P2"),("S3","P1"),("S3","P2"),("S1","P2")}
    if any((r["session_id"],r["placement_id"]) not in allowed for r in d.values()):
        raise ValueError("unknown cell")
    return {k:r for k,r in d.items() if (r["session_id"],r["placement_id"])!=("S1","P2")}

def seal_predictions(plan, predictions):
    active=active_plan(plan)
    test={k for k,r in active.items() if (r["session_id"],r["placement_id"]) not in (("S1","P1"),("S2","P1"))}
    d=exact(test,predictions)
    labels={"no_demand","free","pocket","downstream","both","abstain"}
    for r in d.values():
        if set(r)!={"trial_id","prediction"} or r["prediction"] not in labels:
            raise ValueError("invalid prediction schema")
    payload=json.dumps([d[k] for k in sorted(d)],sort_keys=True,separators=(",",":"))
    return payload,hashlib.sha256(payload.encode()).hexdigest()

def score_sealed(plan,payload,digest,truth):
    if hashlib.sha256(payload.encode()).hexdigest()!=digest:
        raise ValueError("prediction seal mismatch")
    rows=json.loads(payload)
    canonical,check=seal_predictions(plan,rows)
    if canonical!=payload or check!=digest:
        raise ValueError("noncanonical predictions")
    pred=index(rows)
    actual=exact(pred,truth)
    labels={"no_demand","free","pocket","downstream","both"}
    if any(set(r)!={"trial_id","label"} or r["label"] not in labels for r in actual.values()):
        raise ValueError("invalid truth")
    n=len(pred)
    if not n: raise ValueError("empty holdout")
    return {"n":n,"correct":sum(pred[k]["prediction"]==actual[k]["label"] for k in pred),
            "abstain":sum(r["prediction"]=="abstain" for r in pred),
            "status":"CONTRACT_ONLY_NOT_PHYSICAL_EVIDENCE"}

def availability(row):
    import math
    def valid(key):
        try: return math.isfinite(float(row[key]))
        except (KeyError,TypeError,ValueError): return False
    a=valid("rssi_1_dbm")
    b=valid("rssi_2_dbm")
    c=valid("csi_1_amp_dispersion") and valid("csi_2_amp_dispersion")
    return {"rssi_one":a,"rssi_both":a and b,"csi_both":c,"common":a and b and c}
