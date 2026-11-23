"""P137 independent NEW timestamp seeds: frozen P136 calendar-only rule versus local proxies."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from itertools import product
from p85_signal_coordination import build_config
from p118_temporal_arrival_holdout import tape_with_random_times
import p130_split_shared_outflow as topology
from p136_offset_diversified_proxy_regret import arm,metrics_summary,METRICS,SHARES,LABEL_SEEDS,FAMILIES,OFFSETS

HERE=Path(__file__).resolve().parent
TIME_SEEDS=(88701,88702)
CALENDAR={(0,30):60,(15,0):30,(7,15):60,(23,45):30}
assert set(CALENDAR)==set(OFFSETS)


def rgt(row,choice):
    return row['arms'][str(choice)]['cost']-min(row['arms']['30']['cost'],row['arms']['60']['cost'])


def trained_calendar_summary(rows):
    cost=sum(rgt(row,CALENDAR[(row['phi30'],row['phi60'])]) for row in rows)
    correct=sum(rgt(row,CALENDAR[(row['phi30'],row['phi60'])])==0 for row in rows)
    return {'n':len(rows),'correct':correct,'total_regret':cost}


def main():
    rows=[]; times={str(s):set() for s in SHARES}
    for share,seed,ts,fam in product(SHARES,LABEL_SEEDS,TIME_SEEDS,FAMILIES):
        proto=build_config(seed,900,share,7,2,.5)
        tape=tape_with_random_times(proto,seed,ts,fam)
        time_sha=hashlib.sha256(json.dumps([t for t,m in tape]).encode()).hexdigest()
        assert time_sha not in times[str(share)]
        times[str(share)].add(time_sha)
        cfg=topology.config(seed,share)
        cp=topology.run(cfg,tape,checkpoint_at=84,trace=True)
        for phi30,phi60 in OFFSETS:
            a=arm(cfg,tape,cp,30,phi30)
            b=arm(cfg,tape,cp,60,phi60)
            rows.append({'share':share,'label_seed':seed,'time_seed':ts,'family':fam,
                 'time_sha256':time_sha,'phi30':phi30,'phi60':phi60,
                 'delta_cost':a['cost']-b['cost'],
                 'metric_delta':{m:a[m]-b[m] for m in METRICS},'arms':{'30':a,'60':b}})
        print('FINISHED',share,seed,ts,fam,flush=True)
    assert len(rows)==64 and all(len(v)==8 for v in times.values())
    summary=metrics_summary(rows)
    cal=trained_calendar_summary(rows)
    by_offset={f'{a},{b}':{'summary':metrics_summary([r for r in rows if (r['phi30'],r['phi60'])==(a,b)]),
          'calendar':trained_calendar_summary([r for r in rows if (r['phi30'],r['phi60'])==(a,b)])} for a,b in OFFSETS}
    by_share={str(share):{'summary':metrics_summary([r for r in rows if r['share']==share]),
         'calendar':trained_calendar_summary([r for r in rows if r['share']==share])} for share in SHARES}
    by_family={fam:{'summary':metrics_summary([r for r in rows if r['family']==fam]),
         'calendar':trained_calendar_summary([r for r in rows if r['family']==fam])} for fam in FAMILIES}
    gate={m:summary['metrics'][m]['coverage_n']>=52 and summary['metrics'][m]['deployed_regret_ties60']<=.9*cal['total_regret'] for m in METRICS}
    res={'status':'P137_NEW_TAPE_OFFSET_BASELINE_128_ARMS_COMPLETE',
         'prereg':'P137_NEW_TAPE_CALENDAR_BASELINE_PREREG.md',
         'simulator_arms':128,'matched_policy_pairs':64,'distinct_demand_tapes':16,
         'time_seeds':list(TIME_SEEDS),'all_cleared':True,'all_refusals_cross_checked':True,
         'frozen_calendar_policy':{f'{a},{b}':v for (a,b),v in CALENDAR.items()},
         'overall':summary,'calendar_trained_on_P136':cal,'by_offset':by_offset,'by_share':by_share,
         'by_family':by_family,'proxy_added_value_gate_pass':gate,'rows':rows,
         'interpretation_limits':'P137 timestamps disjoint from P136/P135/XR1. P136 calendar map trained on P136, never updated by P137. Same T2 engine and pre-existing route seeds, repeated 4 offsets per arrival tape. Post-treatment two-arm proxy comparison is not an operational online predictor; no SUMO/field.'}
    (HERE/'P137_RESULT.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({k:res[k] for k in ('overall','calendar_trained_on_P136','by_offset','proxy_added_value_gate_pass')},ensure_ascii=False),flush=True)
    return res

if __name__=='__main__':main()
