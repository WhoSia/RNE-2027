"""P133 preregistered three-metric denial sensitivity under exit tie priority."""
from dataclasses import replace
from collections import defaultdict
from itertools import product
from pathlib import Path
from unittest.mock import patch
import json
from p85_signal_coordination import build_config,score,phases
from p118_temporal_arrival_holdout import tape_with_random_times
import p130_split_shared_outflow as p130
import p131_exit_tie_precedence as p131
from receiving_cells_v15 import ReceivingCells

HERE=Path(__file__).resolve().parent
METRICS=('receiver_denied_seconds','receiver_denied_attempts','ever_denied_unique_ids')


def replay(module,cfg,tape,cp,period):
    def green(self,t):
        assert t>=84
        return (t-84)%period>=period//2
    with patch.object(ReceivingCells,'green',green):
        r=module.run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'),trace=True)
    assert r['generated']==r['network_out_L']+r['network_out_S']==60 and r['remaining']==0
    refuses=[e for e in r['service_events'] if e['reason'] in ('receiver_entry_cell_busy','receiver_capacity_full')]
    assert len(refuses)==r['receiver_denied_attempts'],(len(refuses),r['receiver_denied_attempts'])
    assert r['receiver_denied_seconds']<=len(refuses)
    assert all(e['vehicle_id'] in range(60) and e['movement'] in ('S','L') for e in refuses)
    assert r['exit_L']+r['exit_S']==60
    return {'cost':score(r,0),'receiver_denied_seconds':r['receiver_denied_seconds'],
            'receiver_denied_attempts':len(refuses),
            'ever_denied_unique_ids':len({e['vehicle_id'] for e in refuses}),
            'total_distinct_refused_event_ticks':len({e['t'] for e in refuses}),
            'refusal_events_by_movement':{m:sum(e['movement']==m for e in refuses) for m in ('L','S')}}


def main():
    references={who:json.loads((HERE/f'P{number}_RESULT.json').read_text()) for who,number in (('S_first',130),('L_first',131))}
    ref_by_key={who:{(r['share'],r['label_seed'],r['time_seed'],r['family']):r for r in dataset['rows']} for who,dataset in references.items()}
    rows=[]
    for share,label_seed,time_seed,family in product((.5,.75),(86001,86002),(88301,88302),('stochastic_uniform','stochastic_platoon4')):
        proto=build_config(label_seed,900,share,7,2,.5)
        tape=tape_with_random_times(proto,label_seed,time_seed,family)
        for prio,mod in (('S_first',p130),('L_first',p131)):
            cfg=mod.config(label_seed,share)
            cp=mod.run(cfg,tape,checkpoint_at=84,trace=True)
            a=replay(mod,cfg,tape,cp,30)
            b=replay(mod,cfg,tape,cp,60)
            ref=ref_by_key[prio][(share,label_seed,time_seed,family)]
            assert a['cost']==ref['short']['cost'] and b['cost']==ref['long']['cost']
            assert a['receiver_denied_seconds']==ref['short']['denied'] and b['receiver_denied_seconds']==ref['long']['denied']
            assert a['total_distinct_refused_event_ticks']==a['receiver_denied_seconds']
            assert b['total_distinct_refused_event_ticks']==b['receiver_denied_seconds']
            dcost=a['cost']-b['cost']
            delta={m:a[m]-b[m] for m in METRICS}
            labels={m:delta[m]<0<dcost for m in METRICS}
            assert labels['receiver_denied_seconds']==ref['paradox']
            rows.append({'share':share,'label_seed':label_seed,'time_seed':time_seed,'family':family,'priority':prio,
                         'delta_cost':dcost,'metric_delta':delta,'paradox_by_metric':labels,'arms':{'30':a,'60':b}})
        print('FINISHED',share,label_seed,time_seed,family,flush=True)
    assert len(rows)==32
    grouped={}
    for share in (.5,.75):
        grouped[str(share)]={}
        for priority in ('S_first','L_first'):
            r=[x for x in rows if x['share']==share and x['priority']==priority]
            assert len(r)==8
            grouped[str(share)][priority]={metric:sum(v['paradox_by_metric'][metric] for v in r) for metric in METRICS}
    index={(r['share'],r['label_seed'],r['time_seed'],r['family'],r['priority']):r for r in rows}
    flips={};same_cost_flips={};which=[]
    for metric in METRICS:
        flip=0;same=0
        for share,labelseed,tseed,family in product((.5,.75),(86001,86002),(88301,88302),('stochastic_uniform','stochastic_platoon4')):
            s=index[(share,labelseed,tseed,family,'S_first')]
            l=index[(share,labelseed,tseed,family,'L_first')]
            if s['paradox_by_metric'][metric]!=l['paradox_by_metric'][metric]:
                flip+=1
                same+=(s['delta_cost']==l['delta_cost'])
                which.append({'metric':metric,'share':share,'label_seed':labelseed,'time_seed':tseed,'family':family,
                              'sfirst_delta':s['metric_delta'][metric],'lfirst_delta':l['metric_delta'][metric],
                              'cost_sfirst':s['delta_cost'],'cost_lfirst':l['delta_cost']})
        flips[metric]=flip;same_cost_flips[metric]=same
    assert flips['receiver_denied_seconds']==3 and same_cost_flips['receiver_denied_seconds']==2
    result={'status':'P133_DENIAL_METRICS_64_ARMS_REPLAY_COMPLETE',
            'prereg':'P133_DENIAL_METRIC_SENSITIVITY_PREREG.md','new_simulator_arms':64,
            'matched_period_pairs':32,'unique_demand_tapes':16,'all_id_complete':True,
            'original_p130_p131_exact_regression':True,'metrics':list(METRICS),'by_share_priority':grouped,
            'paradox_label_flips_under_priority':flips,
            'paradox_label_flips_with_identical_cost_delta':same_cost_flips,
            'changed_labels':which,'rows':rows,
            'interpretation_limits':'Only local measure definitions differ, and each can depend on lane competition. Attempts, denied seconds and unique IDs are not direct vehicle waiting time. T2 same source; per-tape policy comparisons share traffic identities and routes. No field/SUMO.'}
    (HERE/'P133_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({'by_share':grouped,'flips':flips,'same_cost_flips':same_cost_flips},ensure_ascii=False),flush=True)
    return result

if __name__=='__main__':main()
