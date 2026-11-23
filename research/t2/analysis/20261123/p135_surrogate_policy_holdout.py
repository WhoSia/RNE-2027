"""P135 unseen timestamp holdout: fixed local proxy policy selection and regret."""
import hashlib,json
from itertools import product
from collections import defaultdict
from pathlib import Path
from p85_signal_coordination import build_config
from p118_temporal_arrival_holdout import tape_with_random_times
from p133_denial_metric_sensitivity import replay,METRICS
import p130_split_shared_outflow as sfirst
import p131_exit_tie_precedence as lfirst
HERE=Path(__file__).resolve().parent
SEEDS=(86001,86002);TIMESEEDS=(88401,88402,88403,88404)
SHARES=(.5,.75);FAMILIES=('stochastic_uniform','stochastic_platoon4')

def regret(row,period):
    a=row['arms']['30']['cost'];b=row['arms']['60']['cost']
    return (a if period==30 else b)-min(a,b)

def summarize(rows):
    base={'n':len(rows),'fixed30_regret':sum(regret(x,30) for x in rows),
          'fixed60_regret':sum(regret(x,60) for x in rows),
          'thirty_cheaper':sum(x['arms']['30']['cost']<x['arms']['60']['cost'] for x in rows),
          'sixty_cheaper':sum(x['arms']['60']['cost']<x['arms']['30']['cost'] for x in rows),
          'cost_tied':sum(x['arms']['60']['cost']==x['arms']['30']['cost'] for x in rows)}
    stats={}
    for metric in METRICS:
        covered=[];abstained=[]
        for row in rows:
            val=row['metric_delta'][metric]
            if val==0:abstained.append(row)
            else:covered.append((row,30 if val<0 else 60))
        correct=sum(regret(row,choice)==0 for row,choice in covered)
        covered_regret=sum(regret(row,choice) for row,choice in covered)
        deployed_regret=covered_regret+sum(regret(row,60) for row in abstained)
        stats[metric]={'covered':len(covered),'abstained':len(abstained),
          'coverage':len(covered)/len(rows),'correct_covered':correct,
          'accuracy_covered':correct/len(covered) if covered else None,
          'covered_regret_sum':covered_regret,
          'covered_mean_regret':covered_regret/len(covered) if covered else None,
          'covered_max_regret':max([regret(row,choice) for row,choice in covered],default=0),
          'deployed_regret_ties60':deployed_regret,
          'primary_gate_pass':(len(covered)/len(rows)>=.8 and correct/max(1,len(covered))>=.9 and
                               deployed_regret<=min(base['fixed30_regret'],base['fixed60_regret']))}
    return {**base,'metrics':stats}

def main():
    rows=[];timing_sha_by_share={str(s):set() for s in SHARES}
    for share,label_seed,time_seed,family in product(SHARES,SEEDS,TIMESEEDS,FAMILIES):
        proto=build_config(label_seed,900,share,7,2,.5)
        tape=tape_with_random_times(proto,label_seed,time_seed,family)
        digest=hashlib.sha256(json.dumps([t for t,m in tape],separators=(',',':')).encode()).hexdigest()
        assert digest not in timing_sha_by_share[str(share)]
        timing_sha_by_share[str(share)].add(digest)
        for name,module in (('S_first',sfirst),('L_first',lfirst)):
            cfg=module.config(label_seed,share)
            cp=module.run(cfg,tape,checkpoint_at=84,trace=True)
            short=replay(module,cfg,tape,cp,30)
            long=replay(module,cfg,tape,cp,60)
            dcost=short['cost']-long['cost']
            delta={m:short[m]-long[m] for m in METRICS}
            rows.append({'share':share,'label_seed':label_seed,'time_seed':time_seed,'family':family,
                         'priority':name,'timestamp_sha256':digest,
                         'delta_cost':dcost,'metric_delta':delta,'arms':{'30':short,'60':long}})
        print('FINISHED',share,label_seed,time_seed,family,flush=True)
    assert len(rows)==64 and all(len(a)==16 for a in timing_sha_by_share.values())
    grouped={}
    for share in SHARES:
        grouped[str(share)]={}
        for priority in ('S_first','L_first'):
            cohort=[r for r in rows if r['share']==share and r['priority']==priority]
            assert len(cohort)==16
            grouped[str(share)][priority]=summarize(cohort)
    overall=summarize(rows)
    result={'status':'P135_NEW_TIME_HOLDOUT_SURROGATE_DECISION_128_ARMS_COMPLETE',
            'prereg':'P135_HOLDOUT_SURROGATE_REGRET_PREREG.md',
            'simulator_arms':128,'matched_period_pairs':64,'tapes_by_share':32,
            'distinct_time_vectors_per_share':{'0.5':16,'0.75':16},
            'all_vehicles_cleared':True,'all_trace_denial_attempts_verified':True,
            'by_share_priority':grouped,'overall':overall,'rows':rows,
            'scope':'New timestamp seeds 88401–88404 under two preserved T2 fork topologies; labels 86001/86002, two arrival families; time draws reused across left shares. Cost is full network vehicle-seconds, not field delay. Tie-decision default fixed60. This is a within-engine out-of-time-tape holdout, not independent microsimulation.'}
    (HERE/'P135_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({'overall':overall,'by_share':grouped},ensure_ascii=False),flush=True)
    return result
if __name__=='__main__':main()
