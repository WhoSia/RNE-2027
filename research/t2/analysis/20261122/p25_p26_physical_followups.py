"""P25 discharge-headway and P26 matched-checkpoint left-stage-dose experiments.

Exact canonical T2 synthetic engine, not a traffic-controller program.
Four independent full timestamp tapes; worlds sharing tapes are not independent.
"""
from collections import Counter, defaultdict
from dataclasses import replace
from itertools import product
from pathlib import Path
import hashlib
import json
import pickle

from p19_receiver_service_opportunity import build_config,arrival_clock_pair,tape_hash
from dual_lane_v11 import run
from physical_transfer_screen import score

SEED_REGIMES=((112,1650,.50),(113,1650,.50),(116,1800,.45),(117,1800,.45))
CAPACITIES=(2,4)
OFFSETS=(0,15)
POCKETS=(14.,28.)
B_SHARES=(0.,.5)
HEADWAYS=(1,2,4)
DURATIONS=(6,8,10)
DECISION_TICK=84
EPSILON=5
TERMINAL_PENALTY=60


def action(duration):
    if duration not in DURATIONS:raise ValueError('invalid preregistered duration')
    return ((84,87,'-'),(87,87+duration,'L'),(87+duration,120,'-'))


def key(seed,demand,turn,capacity,offset,pocket,bshare):
    return (demand,turn,seed,capacity,offset,pocket,bshare)


def frozen_p19(reference):
    if reference['protocol']!='T2_P19_RECEIVER_OPPORTUNITY_PROSPECTIVE' or len(reference['records'])!=256:
        raise ValueError('not a complete frozen P19 result')
    out={}
    for r in reference['records']:
        k=key(r['seed'],r['demand_vph'],r['left_fraction'],
              r['receiver_capacity'],r['downstream_offset_s'],r['pocket_m'],r['b_share'])
        if k in out:raise ValueError('duplicate P19 frozen row')
        out[k]=(r['model_delta'],r['tape_hash'])
    if len(out)!=256:raise ValueError('incomplete frozen P19')
    return out


def worlds():
    for seed,demand,turn in SEED_REGIMES:
        for capacity,offset,pocket,bshare in product(CAPACITIES,OFFSETS,POCKETS,B_SHARES):
            cfg=replace(build_config(seed,demand,turn,pocket,capacity,bshare),
                        downstream_offset_s=offset)
            _,tape=arrival_clock_pair(cfg.base)
            yield (key(seed,demand,turn,capacity,offset,pocket,bshare),cfg,tape)


def result_metrics(result):
    return {k:result[k] for k in ('generated','remaining','network_out_S',
        'network_out_L','receiver_denied_attempts','receiver_denied_seconds',
        'receiver_vehicle_seconds','upstream_vehicle_seconds',
        'outside_vehicle_seconds')}


def replay_pair(cfg,tape,duration,*,direct_gate=False):
    cp=run(cfg,tape,checkpoint_at=DECISION_TICK)
    frozen=pickle.dumps(cp,protocol=4)
    baseline=run(cfg,tape,resume_from=cp)
    treatment=run(cfg,tape,resume_from=cp,phase_overrides=action(duration))
    if pickle.dumps(cp,protocol=4)!=frozen:raise AssertionError('checkpoint mutated')
    if direct_gate and run(cfg,tape)!=baseline:raise AssertionError('baseline resumption drift')
    if baseline['generated']!=treatment['generated']!=len(tape):
        raise AssertionError('demand tape mismatch')
    return baseline,treatment,hashlib.sha256(frozen).hexdigest()


def p25(reference):
    lookup=frozen_p19(reference)
    rows=[]
    for k,cfg,tape in worlds():
        for headway in HEADWAYS:
            c=replace(cfg,receiver_headway_s=headway)
            base,treated,cp_hash=replay_pair(c,tape,8,direct_gate=(len(rows)==0))
            delta=score(treated,TERMINAL_PENALTY)-score(base,TERMINAL_PENALTY)
            tape_sha=tape_hash(tape)
            if headway==2 and (delta,tape_sha)!=lookup[k]:
                raise AssertionError(('P19 frozen control mismatch',k))
            rows.append({'key':list(k),'receiver_headway_s':headway,
               'tape_sha256':tape_sha,'checkpoint_sha256':cp_hash,
               'delta':delta,'baseline':result_metrics(base),
               'treated':result_metrics(treated)})
    if len(rows)!=192:raise AssertionError('P25 cohort incomplete')
    strata=[]
    for h in HEADWAYS:
        group=[r for r in rows if r['receiver_headway_s']==h]
        values=[r['delta'] for r in group]
        strata.append({'headway_s':h,'worlds':len(group),
            'beneficial':sum(v<0 for v in values),'harmful':sum(v>0 for v in values),
            'ties':sum(v==0 for v in values),'delta_sum':sum(values),
            'delta_median':sorted(values)[len(values)//2-1:len(values)//2+1],
            'tape_sha_distinct':len({r['tape_sha256'] for r in group}),
            'receiver_denied_attempts_baseline':sum(r['baseline']['receiver_denied_attempts'] for r in group),
            'receiver_denied_attempts_treatment':sum(r['treated']['receiver_denied_attempts'] for r in group)})
    by=defaultdict(dict)
    for r in rows:by[tuple(r['key'])][r['receiver_headway_s']]=r
    reversals=[]
    for k,group in sorted(by.items()):
        if set(group)!=set(HEADWAYS):raise AssertionError('unmatched headways')
        a,b=group[1]['delta'],group[4]['delta']
        if (a>EPSILON and b< -EPSILON) or (a< -EPSILON and b>EPSILON):
            reversals.append({'key':list(k),'h1':a,'h4':b,'same_predecision_state':False,
                'tape_sha256':group[1]['tape_sha256']})
    return {'protocol':'P25_HEADWAY_MODERATION','status':'SYNTHETIC_ONLY',
        'worlds':len(rows),'unique_full_arrival_tapes':len({r['tape_sha256'] for r in rows}),
        'matched_headway1_vs4_groups':len(by),
        'strong_sign_reversals_eps5':len(reversals),
        'reversal_unique_tapes':len({r['tape_sha256'] for r in reversals}),
        'reversals':reversals,'strata':strata,'records':rows,
        'limitation':'headway is changed before tick84; cross-headway effects are not same-state causal contrasts'}


def p26(reference):
    lookup=frozen_p19(reference)
    rows=[]
    for k,cfg,tape in worlds():
        cp=run(cfg,tape,checkpoint_at=DECISION_TICK)
        start=pickle.dumps(cp,protocol=4)
        baseline=run(cfg,tape,resume_from=cp)
        if len(rows)==0 and baseline!=run(cfg,tape):raise AssertionError('baseline direct drift')
        values={};outputs={}
        for duration in DURATIONS:
            treated=run(cfg,tape,resume_from=cp,phase_overrides=action(duration))
            if treated['generated']!=baseline['generated']!=len(tape):
                raise AssertionError('unequal demand')
            values[str(duration)]=score(treated,TERMINAL_PENALTY)-score(baseline,TERMINAL_PENALTY)
            outputs[str(duration)]=result_metrics(treated)
        if start!=pickle.dumps(cp,protocol=4):raise AssertionError('checkpoint mutated')
        if (values['8'],tape_hash(tape))!=lookup[k]:
            raise AssertionError(('P19 fixed-8 regression',k))
        rows.append({'key':list(k),'checkpoint_sha256':hashlib.sha256(start).hexdigest(),
             'tape_sha256':tape_hash(tape),'deltas':values,
             'baseline':result_metrics(baseline),'treated':outputs})
    if len(rows)!=64:raise AssertionError('P26 cohort incomplete')
    strata=[]
    for duration in DURATIONS:
        vals=[r['deltas'][str(duration)] for r in rows]
        strata.append({'left_green_s':duration,'beneficial':sum(v<0 for v in vals),
            'harmful':sum(v>0 for v in vals),'ties':sum(v==0 for v in vals),
            'delta_sum':sum(vals)})
    winners=Counter();nonmonotonic=0;all_harm=0;all_benefit=0
    for r in rows:
        values=[r['deltas'][str(d)] for d in DURATIONS]
        candidate={'none':0,**{str(d):r['deltas'][str(d)] for d in DURATIONS}}
        best=min(candidate.values())
        # Ties are set-valued, not resolved in favor of the intervention.
        winners['|'.join(name for name,v in candidate.items() if v==best)]+=1
        if (values[1]>max(values[0],values[2]) or values[1]<min(values[0],values[2])):
            nonmonotonic+=1
        all_harm+=all(v>0 for v in values)
        all_benefit+=all(v<0 for v in values)
    return {'protocol':'P26_SAME_CHECKPOINT_DOSE','status':'SYNTHETIC_ONLY',
        'worlds':len(rows),'unique_full_arrival_tapes':len({r['tape_sha256'] for r in rows}),
        'within_world_baseline_and_3_actions':True,
        'strata':strata,'candidate_best_tie_sets':dict(sorted(winners.items())),
        'nonmonotonic_6_8_10':nonmonotonic,'all_three_harmful':all_harm,
        'all_three_beneficial':all_benefit,'records':rows,
        'limitation':'the model clearance validator is not real yellow/red/pedestrian signal feasibility'}


def experiment(frozen_path):
    data=Path(frozen_path).read_bytes()
    reference=json.loads(data)
    return {'protocol':'P25_P26_EXACT_CANONICAL_FOLLOWUPS',
        'frozen_p19_sha256':hashlib.sha256(data).hexdigest(),
        'independent_full_arrival_tapes':4,
        'P25':p25(reference),'P26':p26(reference)}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('frozen_p19',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(experiment(a.frozen_p19),sort_keys=True,indent=2)+'\n',encoding='utf8')
