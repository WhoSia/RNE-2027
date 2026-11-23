"""P123: preregistered full-ID crossing/exiting exact delay closure."""
import json
from collections import Counter
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
from receiving_cells_v15 import ReceivingCells
from p85_signal_coordination import build_config, p31, run, score, phases
from p114_offset_adjudication import overlap

HERE=Path(__file__).resolve().parent
CASES=[(86001,'uniform',30,0,60,28),
       (86001,'uniform',30,10,60,22),
       (86002,'platoon4',30,10,60,57),
       (86001,'uniform',30,0,30,1)]

def trajectory(cfg,tape,cp,period,phi):
    def green(receiver,t):
        assert t>=84
        return (t-84-phi)%period<period//2
    with patch.object(ReceivingCells,'green',green):
        res=run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'),trace=True)
    assert res['generated']==len(tape)==60 and res['remaining']==0
    crossing={}
    for e in res['service_events']:
        if e['reason']=='stopline_cross':
            vid=e['vehicle_id']
            assert vid not in crossing
            crossing[vid]=e['t']
    # Precheckpoint crossings are in checkpoint's original event log; run resumes
    # by copying checkpoint state and preserving historical trace entries.
    assert len(crossing)==60, ('crossing incompleteness',period,phi,len(crossing))
    exits={e[1]:e[0] for e in cp['state']['receiver'].exits}
    assert len(exits)==len(cp['state']['receiver'].exits)
    previous={item[1] for item in cp['state']['receiver'].snapshot()}
    count=0
    for f in res['frames']:
        if f['t']<84: continue
        current={item[1] for item in f['receiver']}
        departing=previous-current
        assert len(departing)<=1
        for vid in departing:
            assert vid not in exits
            exits[vid]=f['t'];count+=1
        previous=current
    assert len(exits)==60 and count==res['network_out_L']+res['network_out_S']-len(cp['state']['receiver'].exits)
    assert set(exits)==set(crossing)==set(range(60))
    by={}
    for i,(arrival,move) in enumerate(tape):
        assert arrival<=crossing[i]<=exits[i],(i,arrival,crossing[i],exits[i])
        by[i]={'id':i,'movement':move,'arrival':arrival,'crossing':crossing[i],'exit':exits[i],
               'pre_stopline_s':crossing[i]-arrival,'post_stopline_s':exits[i]-crossing[i]}
    # tick-based score can have same-period common constant but paired score should
    # always agree with completed departure times: vehicles stay counted until tick before exit.
    return {'cost':score(res,0),'receiver_denied':res['receiver_denied_seconds'],
            'overlap':overlap(cfg,period,phi),'vehicle':by}

def experiment():
    rows=[]
    for seed,family,pa,phia,pb,phib in CASES:
        cfg=build_config(seed,900,.75,7,4,.5)
        tape=p31.clock(cfg.base,family)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=4800),downstream_offset_s=0)
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        a=trajectory(cfg,tape,cp,pa,phia)
        b=trajectory(cfg,tape,cp,pb,phib)
        assert a['overlap']==b['overlap'],(seed,family,pa,phia,pb,phib,a['overlap'],b['overlap'])
        deltas=[]
        for i in range(60):
            v=a['vehicle'][i];w=b['vehicle'][i]
            dc=v['exit']-w['exit']
            up=v['pre_stopline_s']-w['pre_stopline_s']
            down=v['post_stopline_s']-w['post_stopline_s']
            assert dc==up+down
            deltas.append({'id':i,'movement':v['movement'],'arrival':v['arrival'],
                           'exit_a':v['exit'],'exit_b':w['exit'],'cross_a':v['crossing'],'cross_b':w['crossing'],
                           'total':dc,'pre_stopline':up,'post_stopline':down})
        observed=a['cost']-b['cost']
        assert sum(v['total'] for v in deltas)==observed,(seed,family,observed,sum(v['total'] for v in deltas))
        assert sum(v['pre_stopline']+v['post_stopline'] for v in deltas)==observed
        bymove={m:{'total':sum(v['total'] for v in deltas if v['movement']==m),
                   'pre_stopline':sum(v['pre_stopline'] for v in deltas if v['movement']==m),
                   'post_stopline':sum(v['post_stopline'] for v in deltas if v['movement']==m)} for m in ('L','S')}
        totals=Counter({'positive_ids':sum(v['total']>0 for v in deltas),
                        'negative_ids':sum(v['total']<0 for v in deltas),
                        'equal_ids':sum(v['total']==0 for v in deltas),
                        'pre_stopline':sum(v['pre_stopline'] for v in deltas),
                        'post_stopline':sum(v['post_stopline'] for v in deltas),
                        'abs_total':sum(abs(v['total']) for v in deltas)})
        rows.append({'seed':seed,'family':family,'policy_a':{'period':pa,'phi':phia,'cost':a['cost'],
                     'denied':a['receiver_denied']},'policy_b':{'period':pb,'phi':phib,'cost':b['cost'],
                     'denied':b['receiver_denied']},'same_left_overlap_seconds':a['overlap'],
                     'cost_a_minus_b':observed,'by_movement':bymove,'sums':dict(totals),
                     'top_positive_delay_ids':sorted(deltas,key=lambda v:-v['total'])[:8],
                     'top_negative_delay_ids':sorted(deltas,key=lambda v:v['total'])[:8],
                     'vehicle_deltas':deltas})
        print('FINISHED',seed,family,pa,phia,pb,phib,'delta',observed,'pre',totals['pre_stopline'],'post',totals['post_stopline'],flush=True)
    assert len(rows)==4
    result={'status':'P123_EXACT_VEHICLE_DELAY_DECOMPOSITION','prereg':'P123_VEHICLE_CAUSAL_DECOMPOSITION_PREREG.md',
            'cases':len(rows),'all_vehicles_cleared_and_id_matched':True,'all_cost_closures_exact':True,'rows':rows,
            'limits':'Post hoc case selection from P122; exact vehicle identity accounting, not independent engine, causal mediation theorem or field confirmation.'}
    (HERE/'P123_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

if __name__=='__main__':
    experiment()
