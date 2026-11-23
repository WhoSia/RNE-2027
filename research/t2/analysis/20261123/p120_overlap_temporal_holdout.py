"""P120 predeclared 4-new-temporal-scenario offset-grid heuristic holdout."""
import json,hashlib
from collections import Counter
from dataclasses import replace
from itertools import product
from pathlib import Path
from p85_signal_coordination import build_config,p31,run
from p118_temporal_arrival_holdout import tape_with_random_times
from p114_offset_adjudication import arm

HERE=Path(__file__).resolve().parent

def sign(x):return (x>0)-(x<0)

def main():
    allcounts=Counter();timing_hashes=set();rows=[]
    for t_seed,family in product((88101,88102),('stochastic_uniform','stochastic_platoon4')):
        cfg=build_config(86001,900,.75,7,4,.5)
        tape=tape_with_random_times(cfg,86001,t_seed,family)
        sig=hashlib.sha256(json.dumps([t for t,_ in tape]).encode()).hexdigest()
        assert sig not in timing_hashes
        timing_hashes.add(sig)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=4800))
        cp=run(cfg,tape,checkpoint_at=84)
        by={}
        for period in (30,60):
            by[period]=[arm(cfg,tape,cp,period,offset) for offset in range(period)]
            assert all(x['remaining']==0 for x in by[period])
        c=Counter()
        for s in by[30]:
            for l in by[60]:
                observed=sign(s['cost']-l['cost'])
                prediction=sign(l['left_green_overlap_t84_400']-s['left_green_overlap_t84_400'])
                c['n']+=1;c['abstain']+=prediction==0
                c['strict_n']+=prediction!=0
                c['strict_correct']+=prediction!=0 and prediction==observed
                c['true_tie']+=observed==0
                c['baseline_30_better_correct']+=observed==-1
        for key,value in c.items():allcounts[key]+=value
        rows.append({'time_seed':t_seed,'family':family,'arrival_time_sha256':sig,'counts':dict(c),
                     'strict_accuracy':c['strict_correct']/c['strict_n']})
        print('FINISHED',t_seed,family, 'accuracy',rows[-1]['strict_accuracy'],flush=True)
    accuracy=allcounts['strict_correct']/allcounts['strict_n'];baseline=allcounts['baseline_30_better_correct']/allcounts['n']
    passed=accuracy>0.75 and (accuracy-baseline)>0.15
    result={'status':'P120_360_NEW_TIME_ARM_HOLDOUT_COMPLETE','prereg':'P120_OVERLAP_HOLDOUT_PREREG.md',
            'unique_time_vectors':len(timing_hashes),'unique_tapes':4,'arms':360,
            'offset_pairs':allcounts['n'],'coverage':allcounts['strict_n']/allcounts['n'],
            'strict_accuracy':accuracy,'always_30_better_baseline':baseline,'absolute_accuracy_lift':accuracy-baseline,
            'gate_pass':passed,'pooled':dict(allcounts),'rows':rows,
            'limitations':['7200 comparisons arise from four time vectors, not 7200 independent trials',
                           'same T2 software only, despite independently randomized timestamps','prediction is not a causal explanation and not independent-engine validation']}
    (HERE/'P120_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({'gate':passed,'strict_accuracy':accuracy,'baseline':baseline,'coverage':result['coverage'],'arms':360}))
if __name__=='__main__':main()
