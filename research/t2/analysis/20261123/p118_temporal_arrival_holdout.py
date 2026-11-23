"""P118 preregistered timestamp-stochastic holdout (within original deterministic T2 engine)."""
import hashlib,json,random
from dataclasses import replace
from collections import Counter,defaultdict
from itertools import product
from pathlib import Path
from unittest.mock import patch
from p85_signal_coordination import build_config,p31,run,score,phases
from receiving_cells_v15 import ReceivingCells

HERE=Path(__file__).resolve().parent


def tape_with_random_times(cfg,label_seed,time_seed,family):
    original=p31.clock(cfg.base,'uniform')
    labels=[movement for _,movement in original]
    assert len(labels)==60
    rng=random.Random(1000003*time_seed+7919*label_seed+(11 if family=='stochastic_uniform' else 97))
    if family=='stochastic_uniform':
        times=sorted(rng.randint(0,239) for _ in range(60))
    elif family=='stochastic_platoon4':
        times=[t for anchor in (20,80,140,200) for t in sorted(anchor+rng.randint(0,14) for _ in range(15))]
    else:raise ValueError(family)
    assert len(times)==60 and times==sorted(times) and all(0<=t<240 for t in times)
    return tuple(zip(times,labels))


def arm(cfg,tape,cp,period):
    def green(self,t):
        assert t>=84
        return ((t-84)%period)>=period//2
    with patch.object(ReceivingCells,'green',green):
        r=run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'))
    assert r['generated']==len(tape)==60 and r['remaining']==0
    assert r['network_out_S']+r['network_out_L']==60
    return {'cost':score(r,0),'denied':r['receiver_denied_seconds']}


def main():
    rows=[];timing_hashes=set()
    for label_seed,timing_seed,family in product((86001,86002),range(88001,88009),('stochastic_uniform','stochastic_platoon4')):
        initial_cfg=build_config(label_seed,900,.75,7,4,.5)
        tape=tape_with_random_times(initial_cfg,label_seed,timing_seed,family)
        stamp=hashlib.sha256(json.dumps([t for t,_ in tape],separators=(',',':')).encode()).hexdigest()
        assert stamp not in timing_hashes, 'temporal realization reused!'
        timing_hashes.add(stamp)
        for capacity in (4,8):
            cfg=build_config(label_seed,900,.75,7,capacity,.5)
            cfg=replace(cfg,base=replace(cfg.base,duration_s=4800))
            cp=run(cfg,tape,checkpoint_at=84)
            s=arm(cfg,tape,cp,30);l=arm(cfg,tape,cp,60)
            dc=s['cost']-l['cost'];dd=s['denied']-l['denied']
            rows.append({'label_seed':label_seed,'time_seed':timing_seed,'family':family,'arrival_hash':stamp,
                         'capacity':capacity,'short':s,'long':l,'delta_cost':dc,'delta_denied':dd,
                         'paradox':dd<0<dc})
        print('FINISHED',label_seed,timing_seed,family,flush=True)
    assert len(rows)==64 and len(timing_hashes)==32
    summary={str(c):{'matched':len([r for r in rows if r['capacity']==c]),
                     'paradox':sum(r['paradox'] for r in rows if r['capacity']==c),
                     'cost_30_worse':sum(r['delta_cost']>0 for r in rows if r['capacity']==c),
                     'sum_cost_delta':sum(r['delta_cost'] for r in rows if r['capacity']==c),
                     'sum_denied_delta':sum(r['delta_denied'] for r in rows if r['capacity']==c)} for c in (4,8)}
    pass_gate=summary['4']['paradox']>=24 and summary['8']['paradox']<=16
    result={'status':'P118_NEW_TEMPORAL_REALIZATIONS_128_ARMS_COMPLETE','prereg':'P118_RANDOM_TIME_HOLDOUT_PREREG.md',
            'route_label_seeds':2,'time_seeds':8,'timing_families':2,'distinct_time_vectors':len(timing_hashes),
            'unique_tapes':32,'matched_comparisons':64,'simulator_arms':128,'all_cleared':True,
            'primary_gate_pass':pass_gate,'summary':summary,'rows':rows,
            'limitation':'New stochastic arrival vectors within same T2 engine; not an independent physical model or representative field demand sample.'}
    (HERE/'P118_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({'pass_gate':pass_gate,'summary':summary}))
if __name__=='__main__':main()
