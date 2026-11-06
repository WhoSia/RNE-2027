"""Off-line policy COURT; no traffic-infrastructure control connector. Synthetic only."""
from __future__ import annotations
from statistics import mean
from micro_world import Road, FixedSignal, run
from od_and_policy import make_od_demand
from actuated import Actuated

ROADS={'A':Road('A',24,1,8,('S',)),'C':Road('C',24,1,8,('S',)),'S':Road('S',25,1,8)}

def assess(vs, output, horizon):
    total=len(vs); finished=len(output.finishes)
    # Completion-only mean is invalid for comparison when any cohort is censored.
    durations=[output.finishes[v.identity]-v.depart_s for v in vs if v.identity in output.finishes]
    by={k:[output.finishes[v.identity]-v.depart_s for v in vs if v.route[0]==k and v.identity in output.finishes] for k in ('A','C')}
    # Lower bound for horizon-censored cases, not an estimate of final travel time.
    bound=mean((output.finishes.get(v.identity,horizon)-v.depart_s) for v in vs)
    return {'completed':finished,'total':total,'uncompleted':total-finished,
            'mean_s':mean(durations) if finished==total else None,
            'censored_elapsed_lower_bound_s':bound,
            'queue_max':output.max_queue,'disparity_s':abs(mean(by['A'])-mean(by['C'])) if all(by.values()) and finished==total else None,
            'collisions':output.collision_violations}

def compare(seeds=(101,103,107,109),holdout=(211,223), horizon=260, n=28,headway=2):
    if set(seeds)&set(holdout):raise ValueError('train/holdout leakage')
    rows=[]; traces={}
    for cohort,ss in (('train',seeds),('holdout',holdout)):
        for seed in ss:
            vs=make_od_demand({'east':('A','S'),'north':('C','S')},n,seed,headway_s=headway,bus_every=7)
            for label,green in [('fixed6',6),('fixed10',10),('fixed14',14),('actuated',None)]:
                controller=Actuated(min_green=6,max_green=15,clearance=2,threshold=2) if label=='actuated' else None
                signals=None if controller else {'A':FixedSignal(24,green,0),'C':FixedSignal(24,20-green,green+2)}
                out=run(ROADS,vs,horizon_s=horizon,signals=signals,controller=controller)
                row={'cohort':cohort,'seed':seed,'policy':label,**assess(vs,out,horizon)}
                rows.append(row)
                if controller:
                    traces[f'{cohort}:{seed}']=controller.log
    return rows,traces

def controller_at(log,t,road):
    state=log[0][1]
    for moment,name in log:
        if moment>t:break
        state=name
    return state==road

def aggregate(rows):
    groups={}
    for row in rows:groups.setdefault((row['cohort'],row['policy']),[]).append(row)
    return [{'cohort':cohort,'policy':policy,'seeds':len(group),
             'censored_scenarios':sum(r['uncompleted']>0 for r in group),
             'mean_s':mean(r['mean_s'] for r in group) if all(r['mean_s'] is not None for r in group) else None,
             'censored_elapsed_lower_bound_s':mean(r['censored_elapsed_lower_bound_s'] for r in group),
             'approach_gap_s':mean(r['disparity_s'] for r in group) if all(r['disparity_s'] is not None for r in group) else None,
             'mean_max_source_queue':mean(r['queue_max'] for r in group)}
            for (cohort,policy),group in sorted(groups.items())]
