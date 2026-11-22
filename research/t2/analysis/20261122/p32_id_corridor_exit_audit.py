"""P32: ID-conserving corridor exit reconstruction and policy equivalence audit.

Synthetic uncalibrated trace reconstruction; it does NOT independently validate
the receiver's physical dynamics or real-world signal timings.
"""
from collections import Counter,defaultdict
from dataclasses import replace
from itertools import product
from pathlib import Path
import hashlib,json,pickle

from dual_lane_v11 import run
from physical_transfer_screen import score
from p19_receiver_service_opportunity import build_config,tape_hash
from p25_p26_physical_followups import worlds,action
from p31_two_arrival_families import SEED_DEMAND,FAMILIES,clock
from p30_unique_vehicle_event_audit import audit_trace

SHA_P30="6fc5d2e02192f8dd4ad97f420bbb8961bb0339d2c7ca01bc3a7ac16c3a43763f"
SHA_P31="ff0452b4b37174b17bf91228722209de0f26ac60730ef9ef673b08d50c0f4915"
HORIZON=240


def corridor_ledger(result,tape):
    """Observe receiver set disappearance after each tick; cross-check all flow counts."""
    if result["config"]["receiver_mode"]!="cells" or result["config"]["receiver_slots"]<=0:
        raise AssertionError("ID ledger requires a cellular receiver")
    if len(result["frames"])!=HORIZON or [f["t"] for f in result["frames"]]!=list(range(HORIZON)):
        raise AssertionError("incomplete or unordered trace")
    audit_trace(result,tape) # independent source's event validity checks
    crossing={}
    for ev in result["service_events"]:
        if ev["reason"]=="stopline_cross":
            vid=ev["vehicle_id"]
            if vid in crossing:raise AssertionError(("duplicate crossing",vid))
            crossing[vid]=ev["t"]
    departures={}
    previously={}
    seen=set()
    for f in result["frames"]:
        t=f["t"]
        current={}
        positions=[]
        for cell,vid,movement in f["receiver"]:
            if (not isinstance(vid,int) or not 0<=vid<len(tape) or
                vid in current or movement!=tape[vid][1] or
                not isinstance(cell,int) or not 0<=cell<result["config"]["receiver_slots"]):
                raise AssertionError(("invalid receiver frame",t,cell,vid))
            current[vid]=movement;positions.append(cell)
        if len(positions)!=len(set(positions)):
            raise AssertionError(("two vehicles in same cell",t))
        exiting=set(previously)-set(current)
        entering=set(current)-set(previously)
        # tick() runs before stopline admissions; departures must be older IDs.
        for vid in exiting:
            if vid in departures or vid not in crossing or crossing[vid]>=t:
                raise AssertionError(("invalid downstream discharge",vid,t))
            departures[vid]=t
        for vid in entering:
            if vid in seen or crossing.get(vid)!=t:
                raise AssertionError(("unexplained receiver entry",vid,t))
        seen.update(current)
        previously=current
    if set(crossing)!=seen or set(departures)&set(previously):
        raise AssertionError("unmatched crossing or reappearance")
    for movement in ("L","S"):
        n=sum(tape[vid][1]==movement for vid in departures)
        if n!=result["network_out_"+movement]:
            raise AssertionError(("exit count disagreement",movement,n,result["network_out_"+movement]))
    if len(previously)!=result["receiver_final"]:
        raise AssertionError("final receiver state mismatch")
    if len(departures)+result["remaining"]!=result["generated"]:
        raise AssertionError("whole-network ID conservation mismatch")
    return crossing,departures


def comparison(a,b,tape):
    ac,ae=corridor_ledger(a,tape)
    bc,be=corridor_ledger(b,tape)
    common_cross=set(ac)&set(bc)
    common_exit=set(ae)&set(be)
    only_cross=set(ac)^set(bc);only_exit=set(ae)^set(be)
    cross_shift=[bc[x]-ac[x] for x in common_cross]
    exit_shift=[be[x]-ae[x] for x in common_exit]
    return {
       "score_delta":score(b,60)-score(a,60),
       "crossing_count_delta":len(bc)-len(ac),
       "network_out_delta":len(be)-len(ae),
       "remaining_delta":b["remaining"]-a["remaining"],
       "crossing_id_symmetric_difference":len(only_cross),
       "exit_id_symmetric_difference":len(only_exit),
       "crossing_time_changed_common_ids":sum(x!=0 for x in cross_shift),
       "exit_time_changed_common_ids":sum(x!=0 for x in exit_shift),
       "crossing_time_delta_sum_common_s":sum(cross_shift),
       "exit_time_delta_sum_common_s":sum(exit_shift),
       "common_completed_corridor_ids":len(common_exit),
       "completed_full_trip_shift_sum_common_s":sum(exit_shift),
       "exit_time_advanced_ids":sum(x<0 for x in exit_shift),
       "exit_time_delayed_ids":sum(x>0 for x in exit_shift),
       "crossing_time_advanced_ids":sum(x<0 for x in cross_shift),
       "crossing_time_delayed_ids":sum(x>0 for x in cross_shift),
       "observed_crossing_and_exit_events_identical":ac==bc and ae==be,
       "fully_matching_aggregate":all((score(a,60)==score(b,60),
         a["remaining"]==b["remaining"],
         a["exit_S"]==b["exit_S"],a["exit_L"]==b["exit_L"],
         a["network_out_S"]==b["network_out_S"],
         a["network_out_L"]==b["network_out_L"])),
       "censoring":"Non-exited ID end-to-end times are RIGHT-censored at t=240; not imputed",
    }


def cases():
    for key,cfg,tape in worlds():
        yield "P30",tuple(key),cfg,tape
    for seed,demand,turn in SEED_DEMAND:
        for family in FAMILIES:
            for cap,off,pocket,bshare in product((2,4),(0,15),(14.,28.),(0.,.5)):
                cfg=replace(build_config(seed,demand,turn,pocket,cap,bshare),downstream_offset_s=off)
                tape=clock(cfg.base,family)
                yield "P31",(seed,family,cap,off,pocket,bshare),cfg,tape


def analyse(p30,p31):
    p30_rows={tuple(r["key"]):r for r in p30["records"]}
    p31_rows={(r["seed"],r["family"],r["receiver_capacity"],
        r["downstream_offset_s"],r["pocket_m"],r["b_share"]):r for r in p31["records"]}
    if len(p30_rows)!=64 or len(p31_rows)!=128:
        raise ValueError("duplicate or incomplete archived reference")
    rows=[];mislabel=0
    for cohort,key,cfg,tape in cases():
        archived=(p30_rows if cohort=="P30" else p31_rows)[key]
        if tape_hash(tape)!=archived["tape_sha256"]:
            raise AssertionError(("arrival source drift",cohort,key))
        checkpoint=run(cfg,tape,trace=True,checkpoint_at=84)
        cpbytes=pickle.dumps(checkpoint,protocol=4)
        if hashlib.sha256(cpbytes).hexdigest()!=archived["checkpoint_sha256"]:
            raise AssertionError(("checkpoint source drift",cohort,key))
        baseline=run(cfg,tape,resume_from=checkpoint,trace=True)
        a=run(cfg,tape,resume_from=checkpoint,trace=True,phase_overrides=action(6))
        b=run(cfg,tape,resume_from=checkpoint,trace=True,phase_overrides=action(10))
        if pickle.dumps(checkpoint,protocol=4)!=cpbytes:
            raise AssertionError("checkpoint mutated")
        for k,result in (("six",a),("ten",b)):
            old=archived[k]
            if (score(result,60)!=old["score"] or
                result["receiver_denied_attempts"]!=old["attempts"] or
                result["remaining"]!=old["remaining"]):
                raise AssertionError(("prior experimental result drift",cohort,key,k))
        if cohort=="P31":
            # Acknowledged schema error: an incorrectly named field in an immutable prior result.
            if archived["baseline_score"]!=baseline["remaining"]:
                raise AssertionError("unexpected previous P31 baseline_score implementation")
            mislabel+=archived["baseline_score"]!=score(baseline,60)
        metrics=comparison(a,b,tape)
        rows.append({"cohort":cohort,"key":list(key),"tape_sha256":tape_hash(tape),
                     "baseline_true_score":score(baseline,60),
                     "baseline_remaining":baseline["remaining"],
                     "metrics":metrics})
    if len(rows)!=192 or len({r["tape_sha256"] for r in rows})!=12:
        raise AssertionError("P32 cohort size mismatch")
    groups=[]
    for cohort in ("P30","P31"):
        group=[r for r in rows if r["cohort"]==cohort]
        m=[r["metrics"] for r in group]
        groups.append({"cohort":cohort,"worlds":len(group),
         "score_equal":sum(z["score_delta"]==0 for z in m),
         "score_equal_but_crossing_or_exit_history_changed":
             sum(z["score_delta"]==0 and not z["observed_crossing_and_exit_events_identical"] for z in m),
         "aggregate_exact_but_individual_history_changed":
             sum(z["fully_matching_aggregate"] and not z["observed_crossing_and_exit_events_identical"] for z in m),
         "different_stopline_crossing_ID_sets":sum(z["crossing_id_symmetric_difference"]>0 for z in m),
         "different_network_exit_ID_sets":sum(z["exit_id_symmetric_difference"]>0 for z in m),
         "changed_network_exit_timestamps":sum(z["exit_time_changed_common_ids"]>0 for z in m),
         "identical_crossing_and_downstream_exit_histories":sum(z["observed_crossing_and_exit_events_identical"] for z in m),
         "all_valid_corridor_ledger":True})
    return {"protocol":"P32_ID_CORRIDOR_EXIT_EQUIVALENCE",
       "status":"SYNTHETIC_ONLY",
       "worlds":len(rows),"unique_arrival_tapes":12,
       "archived_P31_baseline_score_wrong_label_rows":mislabel,
       "archived_P31_baseline_score_semantics":"baseline.remaining, NOT physical_transfer_screen.score",
       "by_cohort":groups,"records":rows}


def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("p30",type=Path);p.add_argument("p31",type=Path);p.add_argument("output",type=Path)
    args=p.parse_args()
    b30=args.p30.read_bytes();b31=args.p31.read_bytes()
    if hashlib.sha256(b30).hexdigest()!=SHA_P30 or hashlib.sha256(b31).hexdigest()!=SHA_P31:
        raise ValueError("frozen input SHA mismatch")
    args.output.write_text(json.dumps(analyse(json.loads(b30),json.loads(b31)),
        sort_keys=True,indent=2)+"\n",encoding="utf8")


if __name__=="__main__":
    main()
