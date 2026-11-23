"""P136 preregistered post-midnight cross-offset local-proxy regret test."""
from __future__ import annotations
import hashlib, json
from itertools import product
from pathlib import Path
from unittest.mock import patch
from collections import Counter
from p85_signal_coordination import build_config, score, phases
from p118_temporal_arrival_holdout import tape_with_random_times
import p130_split_shared_outflow as topology
from receiving_cells_v15 import ReceivingCells

HERE = Path(__file__).resolve().parent
LABEL_SEEDS = (86001, 86002)
TIME_SEEDS = (88601, 88602)
FAMILIES = ('stochastic_uniform','stochastic_platoon4')
SHARES = (.5,.75)
OFFSETS = ((0,30),(15,0),(7,15),(23,45))
METRICS = ('receiver_denied_seconds','receiver_denied_attempts','ever_denied_unique_ids')


def arm(cfg,tape,cp,period,phi):
    def green(self,t):
        assert t >= 84
        return ((t-84+phi)%period) < period//2
    with patch.object(ReceivingCells,'green',green):
        r=topology.run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'),trace=True)
    assert r['remaining']==0 and r['generated']==r['network_out_L']+r['network_out_S']==60
    refusals=[e for e in r['service_events'] if e['reason'] in ('receiver_entry_cell_busy','receiver_capacity_full')]
    assert len(refusals)==r['receiver_denied_attempts']
    assert len({e['t'] for e in refusals}) == r['receiver_denied_seconds']
    assert all(0 <= e['vehicle_id'] <60 for e in refusals)
    assert len({e['vehicle_id'] for e in r['service_events'] if e['reason']=='stopline_cross'})==60
    assert r['receiver_final']==0
    return {'cost':score(r,0),'receiver_denied_seconds':r['receiver_denied_seconds'],
       'receiver_denied_attempts':len(refusals),'ever_denied_unique_ids':len({e['vehicle_id'] for e in refusals}),
       'network_out_L':r['network_out_L'],'network_out_S':r['network_out_S']}


def metrics_summary(rows):
    n=len(rows)
    cheap30=sum(r['delta_cost']<0 for r in rows)
    cheap60=sum(r['delta_cost']>0 for r in rows)
    ties=n-cheap30-cheap60
    def regret(r, choice):
        j=r['arms'][str(choice)]['cost']
        return j-min(r['arms']['30']['cost'],r['arms']['60']['cost'])
    fixed={str(p):{'correct':sum(regret(r,p)==0 for r in rows),'total_regret':sum(regret(r,p) for r in rows)} for p in (30,60)}
    out={}
    for m in METRICS:
        covered=[r for r in rows if r['metric_delta'][m] != 0]
        correct=sum(regret(r,30 if r['metric_delta'][m]<0 else 60)==0 for r in covered)
        total=sum(regret(r,30 if r['metric_delta'][m]<0 else 60) if r['metric_delta'][m]!=0 else regret(r,60) for r in rows)
        out[m]={'coverage_n':len(covered),'correct_covered':correct,'accuracy_covered':correct/len(covered) if covered else None,
            'deployed_regret_ties60':total,'regret_over_best_fixed':total-min(fixed['30']['total_regret'],fixed['60']['total_regret'])}
    return {'n':n,'thirty_cheaper':cheap30,'sixty_cheaper':cheap60,'tied':ties,'fixed':fixed,'metrics':out}


def main():
    rows=[]
    unique={str(s):set() for s in SHARES}
    for share,seed,ts,family in product(SHARES,LABEL_SEEDS,TIME_SEEDS,FAMILIES):
        proto=build_config(seed,900,share,7,2,.5)
        tape=tape_with_random_times(proto,seed,ts,family)
        time_hash=hashlib.sha256(json.dumps([t for t,m in tape]).encode()).hexdigest()
        assert time_hash not in unique[str(share)]
        unique[str(share)].add(time_hash)
        cfg=topology.config(seed,share)
        cp=topology.run(cfg,tape,checkpoint_at=84,trace=True)
        for phi30,phi60 in OFFSETS:
            short=arm(cfg,tape,cp,30,phi30)
            long=arm(cfg,tape,cp,60,phi60)
            rows.append({'share':share,'label_seed':seed,'time_seed':ts,'family':family,'time_sha256':time_hash,
                'phi30':phi30,'phi60':phi60,'delta_cost':short['cost']-long['cost'],
                'metric_delta':{m:short[m]-long[m] for m in METRICS},'arms':{'30':short,'60':long}})
        print('FINISHED',share,seed,ts,family,flush=True)
    assert len(rows)==64 and all(len(x)==8 for x in unique.values())
    summary=metrics_summary(rows)
    balance=summary['thirty_cheaper']>=20 and summary['sixty_cheaper']>=20
    best=min(summary['fixed']['30']['total_regret'],summary['fixed']['60']['total_regret'])
    meets={m:balance and s['coverage_n']>=int(.8*64+.9999) and s['deployed_regret_ties60']<=best*.9
         for m,s in summary['metrics'].items()}
    by_offset={f'{x},{y}':metrics_summary([r for r in rows if (r['phi30'],r['phi60'])==(x,y)]) for x,y in OFFSETS}
    by_share={str(share):metrics_summary([r for r in rows if r['share']==share]) for share in SHARES}
    report={'status':'P136_OFFSET_DIVERSIFIED_128_ARMS_COMPLETE','prereg':'P136_OFFSET_DIVERSIFIED_PROXY_REGRET_PREREG.md',
        'simulator_arms':128,'matched_policy_pairs':64,'distinct_demand_tapes':16,'time_vectors_per_share':8,
        'all_cleared':True,'all_refusals_cross_checked':True,
        'offset_pairs':OFFSETS,'overall':summary,'by_offset':by_offset,'by_share':by_share,'balance_gate_pass':balance,
        'proxy_predeclared_pass':meets,'rows':rows,
        'limitations':'Same T2 P130 fork; 16 distinct demand tapes repeated across 4 offsets. Offsets are part of policy, so period-only attribution invalid. Time-vector seeds new vs P135/XR1, but route seeds unchanged; no independent SUMO/field.'}
    (HERE/'P136_RESULT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({k:report[k] for k in ('overall','by_offset','balance_gate_pass','proxy_predeclared_pass')},ensure_ascii=False),flush=True)
    return report

if __name__=='__main__':main()
