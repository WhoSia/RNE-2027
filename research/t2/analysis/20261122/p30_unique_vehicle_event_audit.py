"""T2 P30: source-locked, per-vehicle receiver denial audit (synthetic only)."""
from collections import Counter,defaultdict
from pathlib import Path
import hashlib,json,pickle

from dual_lane_v11 import run
from physical_transfer_screen import score
from p25_p26_physical_followups import worlds,action,tape_hash

REF_SHA="640ec195830abae2ab99d202d43d92aaf3cbbc5f875a0ddc6765fe82f20c19e4"
DENIAL_REASONS={"receiver_capacity_full","receiver_entry_cell_busy"}
MOVES={"S","L"}
END_TICK=240


def audit_trace(result,tape):
    """Classify ID-bearing *observed* stopline events; censor unmatched waits."""
    events=result["service_events"]
    denial=defaultdict(list)
    crossed={}
    for e in events:
        vid=e["vehicle_id"]
        if not isinstance(vid,int) or not 0<=vid<len(tape):
            raise AssertionError(("invalid vehicle ID",vid))
        t=e["t"];reason=e["reason"]
        if e["movement"]!=tape[vid][1] or t<tape[vid][0]:
            raise AssertionError(("wrong route or premature event",e))
        if reason in DENIAL_REASONS:
            if vid in crossed:raise AssertionError(("denial after crossing",vid))
            denial[vid].append(t)
        elif reason=="stopline_cross":
            if vid in crossed:raise AssertionError(("duplicate stopline crossing",vid))
            crossed[vid]=t
        else:
            raise AssertionError(("unrecognized service event",reason))
    attempts=sum(map(len,denial.values()))
    if attempts!=result["receiver_denied_attempts"]:
        raise AssertionError(("denial trace mismatch",attempts,result["receiver_denied_attempts"]))
    if len(crossed)!=result["exit_L"]+result["exit_S"]:
        raise AssertionError("crossing trace mismatch")
    if any(ts!=sorted(ts) or len(ts)!=len(set(ts)) for ts in denial.values()):
        raise AssertionError("misordered or duplicate denial ticks")
    episodes=sum(1+sum(y>x+1 for x,y in zip(ts,ts[1:])) for ts in denial.values())
    completed=[];censored=[]
    for vid,ts in denial.items():
        t0=ts[0]
        if vid in crossed:
            if crossed[vid]<=ts[-1]:raise AssertionError(("cross before final denial",vid))
            completed.append(crossed[vid]-t0)
        else:
            censored.append(END_TICK-t0)
    # Interval is first denial to eventual stopline crossing, NOT downstream exit.
    result_summary={
        "attempts":attempts,"distinct_rejected_vehicles":len(denial),
        "repeat_attempts":attempts-len(denial),
        "contiguous_refusal_episodes":episodes,
        "max_attempts_per_vehicle":max(map(len,denial.values()),default=0),
        "rejected_then_crossed":len(completed),
        "rejected_censored_at_240":len(censored),
        "first_denial_to_crossing_sum_s":sum(completed),
        "first_denial_to_crossing_max_s":max(completed,default=None),
        "first_denial_right_censored_followup_sum_s":sum(censored),
        "observed_crossing_count":len(crossed),
        "left_crossings":sum(tape[v][1]=="L" for v in crossed),
        "right_censor_policy":"t=240; censored time never imputed as observed wait",
        "score":score(result,60),
        "remaining":result["remaining"],
        "receiver_vehicle_seconds":result["receiver_vehicle_seconds"],
    }
    return result_summary


def analyse(p26_reference):
    records=p26_reference["P26"]["records"]
    if len(records)!=64:raise ValueError("incomplete P26 result")
    bykey={tuple(r["key"]):r for r in records}
    if len(bykey)!=64:raise ValueError("duplicate frozen reference key")
    out=[]
    for k,cfg,tape in worlds():
        ref=bykey[k]
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        frozen=pickle.dumps(cp,protocol=4)
        baseline=run(cfg,tape,resume_from=cp,trace=True)
        treatments={}
        for dur in (6,10):
            sim=run(cfg,tape,resume_from=cp,phase_overrides=action(dur),trace=True)
            if (score(sim,60)-score(baseline,60)!=ref["deltas"][str(dur)]
                or sim["receiver_denied_attempts"]!=ref["treated"][str(dur)]["receiver_denied_attempts"]
                or sim["remaining"]!=ref["treated"][str(dur)]["remaining"]):
                raise AssertionError(("P26 prior result drift",k,dur))
            treatments[str(dur)]=audit_trace(sim,tape)
        if pickle.dumps(cp,protocol=4)!=frozen:raise AssertionError("checkpoint mutation")
        if tape_hash(tape)!=ref["tape_sha256"]:raise AssertionError("tape mismatch")
        if (score(baseline,60),baseline["receiver_denied_attempts"])!=(
            score(run(cfg,tape,trace=True),60),ref["baseline"]["receiver_denied_attempts"]):
            raise AssertionError("baseline full rerun drift")
        out.append({"key":list(k),"tape_sha256":ref["tape_sha256"],
                    "checkpoint_sha256":hashlib.sha256(frozen).hexdigest(),
                    "six":treatments["6"],"ten":treatments["10"]})
    if len(out)!=64:raise AssertionError("incomplete P30")
    fields=("attempts","distinct_rejected_vehicles","repeat_attempts",
            "contiguous_refusal_episodes","max_attempts_per_vehicle",
            "rejected_then_crossed","rejected_censored_at_240",
            "first_denial_to_crossing_sum_s","observed_crossing_count",
            "left_crossings","score","remaining")
    hist={field:dict(sorted(Counter(r["ten"][field]-r["six"][field] for r in out).items()))
          for field in fields}
    return {
        "protocol":"P30_PAIRED_PER_ID_RECEIVER_DENIAL_AUDIT",
        "preregistered_exploratory":True,"status":"SYNTHETIC_ONLY",
        "unique_full_arrival_tapes":len({r["tape_sha256"] for r in out}),
        "worlds":len(out),"same_score_worlds":sum(r["six"]["score"]==r["ten"]["score"] for r in out),
        "difference_histogram_10_minus_6":hist,
        "mean_first_denial_to_crossing_censored":"NOT_ESTIMATED",
        "cannot_measure_from_current_service_events":["per_ID_downstream_network_exit_time",
            "unique common_exit_gap-denied vehicles"],
        "records":out,
    }


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("frozen_p25p26",type=Path);p.add_argument("output",type=Path)
    a=p.parse_args();raw=a.frozen_p25p26.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=REF_SHA:raise ValueError("P26 reference SHA drift")
    a.output.write_text(json.dumps(analyse(json.loads(raw)),sort_keys=True,indent=2)+"\n",encoding="utf8")
