"""RF15: reserve-free evaluation with legacy RF05 classifier.
Synthetic contract only; no physical measurement or blind custody claim.
"""
from rf_pilot_evaluator import validate, MODELS, fit_predict, summarize
from rf14_blind_contract import active_plan, exact

def evaluate_active(plan, rows):
    active=active_plan(plan)
    data=exact(active, rows)
    validate(list(data.values()))
    for k,r in data.items():
        if any(r[f]!=active[k][f] for f in ("session_id","placement_id")):
            raise ValueError("cell mismatch")
    train=[r for r in data.values() if (r["session_id"],r["placement_id"]) in (("S1","P1"),("S2","P1"))]
    test=[r for r in data.values() if (r["session_id"],r["placement_id"]) not in (("S1","P1"),("S2","P1"))]
    if not train or not test: raise ValueError("empty split")
    out={}
    for name, fields in MODELS.items():
        pred, fit=fit_predict(train,test,fields)
        if len(pred)!=len(test): raise ValueError("prediction denominator mismatch")
        out[name]={**summarize(test,pred),**fit}
    return {"status":"OFFLINE_LABELLED_DIAGNOSTIC_NOT_BLIND",
            "train_n":len(train),"test_n":len(test),"models":out,
            "session_quality":{s:sum(r["quality"]=="ok" for r in data.values() if r["session_id"]==s)/sum(r["session_id"]==s for r in data.values()) for s in sorted({r["session_id"] for r in data.values()})}}
