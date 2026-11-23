"""P128 preregistered selected per-ID trace of 50% left C8 platoon family reversal."""
import json
from pathlib import Path
from dataclasses import replace
from p85_signal_coordination import build_config,run
from p118_temporal_arrival_holdout import tape_with_random_times
from p123_vehicle_delay_decomposition import trajectory
HERE=Path(__file__).resolve().parent
SELECT=((.50,'stochastic_uniform'),(.50,'stochastic_platoon4'),(.75,'stochastic_platoon4'))
SEED,TIME_SEED=86001,88301

def main():
    ref=json.loads((HERE/'P127_RESULT.json').read_text())
    rows=[]
    for share,family in SELECT:
        cfg=build_config(SEED,900,share,7,8,.5)
        tape=tape_with_random_times(cfg,SEED,TIME_SEED,family)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=4800),downstream_offset_s=0)
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        a=trajectory(cfg,tape,cp,30,15)
        b=trajectory(cfg,tape,cp,60,30)
        orig=next(x for x in ref['rows'] if x['share']==share and x['capacity']==8 and x['label_seed']==SEED and x['time_seed']==TIME_SEED and x['family']==family)
        assert a['cost']==orig['cost30'] and b['cost']==orig['cost60']
        out=[]
        for vid in range(60):
            x=a['vehicle'][vid];y=b['vehicle'][vid]
            assert x['arrival']==y['arrival'] and x['movement']==y['movement']
            total=x['exit']-y['exit'];pre=x['crossing']-y['crossing']
            post=(x['exit']-x['crossing'])-(y['exit']-y['crossing'])
            assert total==pre+post
            out.append({'id':vid,'movement':x['movement'],'exit_delta':total,'pre_stopline_delta':pre,'post_stopline_delta':post})
        dc=a['cost']-b['cost'];assert dc==sum(v['exit_delta'] for v in out)
        bymovement={m:{'total':sum(v['exit_delta'] for v in out if v['movement']==m),'pre':sum(v['pre_stopline_delta'] for v in out if v['movement']==m),'post':sum(v['post_stopline_delta'] for v in out if v['movement']==m)} for m in ('L','S')}
        totals={'total':dc,'pre':sum(v['pre_stopline_delta'] for v in out),'post':sum(v['post_stopline_delta'] for v in out)}
        assert totals['pre']+totals['post']==dc
        rows.append({'share':share,'family':family,'delta_cost':dc,'delta_denied':orig['delta_denied'],
                     'totals':totals,'bymovement':bymovement,
                     'top_positive':sorted(out,key=lambda x:-x['exit_delta'])[:5],
                     'top_negative':sorted(out,key=lambda x:x['exit_delta'])[:5]})
        print('FINISHED',share,family,totals,flush=True)
    assert rows[0]['delta_cost']==-148 and rows[1]['delta_cost']==202 and rows[2]['delta_cost']==-66
    result={'status':'P128_SELECTED_C8_PLATOON_REVERSAL_TRACE_COMPLETE',
        'prereg':'P128_PLATOON_FAMILY_REVERSAL_PREREG.md',
        'simulator_arms':6,'matched_pairs':3,'all_clear':True,'per_id_closure':True,'rows':rows,
        'limits':'Postselection from P127; same T2 engine; no independent predictive evidence.'}
    (HERE/'P128_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({'rows':[{'share':r['share'],'family':r['family'],'cost':r['delta_cost'],'total':r['totals'],'move':r['bymovement']} for r in rows]},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
