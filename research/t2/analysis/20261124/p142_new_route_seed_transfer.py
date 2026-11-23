"""P142: frozen pre-decision upstream queue guard and fresh temporal holdout.

Registered before seeds 88901/88902 were run. Synthetic T2 only.
"""
from __future__ import annotations
import hashlib
import json
from collections import defaultdict
from itertools import product
from pathlib import Path
import p130_split_shared_outflow as topology
from dual_lane_separate_receivers_p130 import checkpoint_observation
from p85_signal_coordination import build_config
from p118_temporal_arrival_holdout import tape_with_random_times
from p136_offset_diversified_proxy_regret import arm, SHARES, FAMILIES, OFFSETS

HERE = Path(__file__).resolve().parent
LABEL_SEEDS = (86101, 86102)
TIME_SEEDS = (89101, 89102)
CALENDAR = {(0,30):60, (15,0):30, (7,15):60, (23,45):30}
TARGET = (7,15)
Q_THRESHOLD = 14
assert set(CALENDAR) == set(OFFSETS)
KEYS = ('outside_A','outside_B','approach_A','approach_B','pocket_vehicles','receiver_vehicles')

def observe(cp):
    o = checkpoint_observation(cp)
    assert o['decision_tick'] == 84
    state = {k:o[k] for k in KEYS}
    assert all(isinstance(x,int) and x>=0 for x in state.values())
    assert state['receiver_vehicles'] <= 4
    return state

def q_upstream(state):
    return sum(state[k] for k in KEYS if k != 'receiver_vehicles')

def choose(offset,state,share):
    baseline = CALENDAR[offset]
    return 30 if offset==TARGET and share<=.5 and q_upstream(state)>=Q_THRESHOLD else baseline

def regret(r,policy):
    costs=r['arms']
    return costs[str(policy)]['cost']-min(costs['30']['cost'],costs['60']['cost'])

def summary(rows):
    s = {'n':len(rows)}
    for name in ('calendar','guard','fixed30','fixed60'):
        s[name]={'correct':sum(regret(r,r['choices'][name])==0 for r in rows),
                 'total_regret':sum(regret(r,r['choices'][name]) for r in rows)}
    s['triggered']=sum(r['choices']['calendar']!=r['choices']['guard'] for r in rows)
    s['helpful']=sum(regret(r,r['choices']['guard'])<regret(r,r['choices']['calendar']) for r in rows)
    s['harmful']=sum(regret(r,r['choices']['guard'])>regret(r,r['choices']['calendar']) for r in rows)
    return s

def main():
    rows=[]
    tape_ids=set()
    hashes={str(x):set() for x in SHARES}
    for share,labelseed,timeseed,family in product(SHARES,LABEL_SEEDS,TIME_SEEDS,FAMILIES):
        cfg=topology.config(labelseed,share)
        tape=tape_with_random_times(build_config(labelseed,900,share,7,2,.5),labelseed,timeseed,family)
        assert len(tape)==60
        tag=(share,labelseed,timeseed,family)
        assert tag not in tape_ids
        tape_ids.add(tag)
        sh=hashlib.sha256(json.dumps(tape).encode()).hexdigest()
        assert sh not in hashes[str(share)]
        hashes[str(share)].add(sh)
        cp=topology.run(cfg,tape,checkpoint_at=84,trace=True)
        state=observe(cp)
        for phi30,phi60 in OFFSETS:
            offset=(phi30,phi60)
            a=arm(cfg,tape,cp,30,phi30)
            assert observe(cp)==state, 'checkpoint mutated by 30s'
            b=arm(cfg,tape,cp,60,phi60)
            assert observe(cp)==state, 'checkpoint mutated by 60s'
            choices={'calendar':CALENDAR[offset],
                     'guard':choose(offset,state,share),
                     'fixed30':30,'fixed60':60}
            rows.append({'share':share,'label_seed':labelseed,'time_seed':timeseed,
                         'family':family,'time_sha256':sh,
                         'phi30':phi30,'phi60':phi60,
                         'prestate':dict(state),'q_upstream':q_upstream(state),
                         'arms':{'30':a,'60':b},
                         'delta_cost':a['cost']-b['cost'],
                         'choices':choices})
        print('FINISHED',share,labelseed,timeseed,family,flush=True)
    assert len(rows)==64 and len(tape_ids)==16 and all(len(x)==8 for x in hashes.values())
    assert all(sum((r['share'],r['label_seed'],r['time_seed'],r['family'])==k for r in rows)==4 for k in tape_ids)
    pooled=summary(rows)
    by_offset={f'{a},{b}':summary([r for r in rows if (r['phi30'],r['phi60'])==(a,b)]) for a,b in OFFSETS}
    by_share={str(s):summary([r for r in rows if r['share']==s]) for s in SHARES}
    by_family={f:summary([r for r in rows if r['family']==f]) for f in FAMILIES}
    group=defaultdict(list)
    for r in rows:
        group[(r['share'],r['label_seed'],r['time_seed'],r['family'])].append(r)
    tie={'calendar_better':0,'guard_better':0,'equal':0}
    for entries in group.values():
        base=sum(regret(r,r['choices']['calendar']) for r in entries)
        new=sum(regret(r,r['choices']['guard']) for r in entries)
        tie['calendar_better' if base<new else 'guard_better' if new<base else 'equal']+=1
    if pooled['triggered']==0:
        status='P142_UNINFORMATIVE_NO_TRIGGERS'
    else:
        cal=pooled['calendar']['total_regret'];g=pooled['guard']['total_regret']
        global_pass=(g==0 if cal==0 else g<=.9*cal)
        strata_pass=all(by_share[s]['guard']['total_regret']<=by_share[s]['calendar']['total_regret'] for s in by_share)
        status='P142_PREDECLARED_PASS' if global_pass and strata_pass and pooled['harmful']*4<=pooled['triggered'] else 'P142_PREDECLARED_FAIL'
    out={'status':status,'prereg':'P142_NEW_ROUTE_SEED_TRANSFER_PREREG.md',
         'simulator_arms':128,'matched_pairs':64,'distinct_demand_tapes':16,
         'time_seeds':list(TIME_SEEDS),'all_cleared':True,'event_logs_crosschecked':True,
         'receiver_topology':'movement_separate_shared_exit','checkpoint_time':84,
         'calibration':'threshold 14 and share<=.5 selected after P140 outcomes; P142 new time seeds',
         'pooled':pooled,'by_offset':by_offset,'by_share':by_share,'by_family':by_family,
         'within_tape_paired_regret':tie,'rows':rows,
         'limitations':'Synthetic same T2 engine; route label seed reuse across shares; 4 offsets per 16 arrival tapes; no physical detector validation; no independent SUMO parity.'}
    (HERE/'P142_RESULT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print('RESULT',json.dumps({k:out[k] for k in ('status','pooled','by_offset','within_tape_paired_regret')},ensure_ascii=False),flush=True)
    return out

if __name__=='__main__':main()
