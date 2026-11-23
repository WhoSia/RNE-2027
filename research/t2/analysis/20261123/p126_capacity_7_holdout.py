"""P126 predeclared new timestamp realizations at 6/7/8 shared receiving cells."""
import hashlib
import json
from collections import defaultdict
from dataclasses import replace
from itertools import product
from pathlib import Path
from p85_signal_coordination import build_config, run
from p118_temporal_arrival_holdout import tape_with_random_times, arm

HERE=Path(__file__).resolve().parent
CAPS=(6,7,8)
LABEL_SEEDS=(86001,86002)
TIME_SEEDS=(88201,88202,88203,88204)
FAMILIES=('stochastic_uniform','stochastic_platoon4')

def main():
    results=[]; hashes=set()
    for label_seed,time_seed,family in product(LABEL_SEEDS,TIME_SEEDS,FAMILIES):
        prototype=build_config(label_seed,900,.75,7,4,.5)
        tape=tape_with_random_times(prototype,label_seed,time_seed,family)
        digest=hashlib.sha256(json.dumps([t for t,_ in tape],separators=(',',':')).encode()).hexdigest()
        assert digest not in hashes
        hashes.add(digest)
        for c in CAPS:
            cfg=build_config(label_seed,900,.75,7,c,.5)
            cfg=replace(cfg,base=replace(cfg.base,duration_s=4800))
            cp=run(cfg,tape,checkpoint_at=84)
            s=arm(cfg,tape,cp,30)
            l=arm(cfg,tape,cp,60)
            dc=s['cost']-l['cost'];dd=s['denied']-l['denied']
            results.append(dict(label_seed=label_seed,time_seed=time_seed,family=family,arrival_sha256=digest,
                                receiver_capacity=c,short=s,long=l,delta_cost=dc,delta_denied=dd,
                                paradox=(dc>0 and dd<0)))
        print('FINISHED',label_seed,time_seed,family,flush=True)
    assert len(hashes)==16 and len(results)==48
    summary={}
    for cap in CAPS:
        r=[x for x in results if x['receiver_capacity']==cap]
        summary[str(cap)]={'matched':len(r),'paradox':sum(x['paradox'] for x in r),
            'cost_30_worse':sum(x['delta_cost']>0 for x in r),
            'sum_delta_cost':sum(x['delta_cost'] for x in r),
            'mean_delta_cost':sum(x['delta_cost'] for x in r)/len(r),
            'sum_delta_denied':sum(x['delta_denied'] for x in r),
            'min_delta_cost':min(x['delta_cost'] for x in r),'max_delta_cost':max(x['delta_cost'] for x in r)}
    groups=defaultdict(dict)
    for x in results:groups[(x['label_seed'],x['time_seed'],x['family'])][x['receiver_capacity']]=x
    switches={'6_true_7_false':0,'7_true_8_false':0,'6_true_8_false':0,'cost_sign_nonmonotonic':0}
    for trio in groups.values():
        assert set(trio)==set(CAPS)
        switches['6_true_7_false']+=trio[6]['paradox'] and not trio[7]['paradox']
        switches['7_true_8_false']+=trio[7]['paradox'] and not trio[8]['paradox']
        switches['6_true_8_false']+=trio[6]['paradox'] and not trio[8]['paradox']
        dc=[trio[c]['delta_cost'] for c in CAPS]
        switches['cost_sign_nonmonotonic']+=not(dc[0]>=dc[1]>=dc[2])
    result={'status':'P126_96_ARM_BOUNDARY_HOLDOUT_COMPLETE','prereg':'P126_CAPACITY_7_HOLDOUT_PREREG.md',
        'label_seeds':list(LABEL_SEEDS),'timing_seeds':list(TIME_SEEDS),'families':list(FAMILIES),
        'timestamp_vectors':len(hashes),'matched_comparisons':len(results),'simulator_arms':len(results)*2,
        'all_cleared':True,'capacities':list(CAPS),'summary':summary,'switches':switches,'rows':results,
        'limitation':'Same T2 engine; only 16 randomized timestamp vectors across two label choices and two families. Cell capacity changes simulated travel time and storage; not evidence of a universal physical threshold.'}
    (HERE/'P126_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({'summary':summary,'switches':switches},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
