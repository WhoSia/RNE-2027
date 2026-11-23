"""P129 pre-registered shared-vs-movement-segregated receiver replay."""
from dataclasses import replace,fields
from collections import defaultdict
from itertools import product
from pathlib import Path
import json, hashlib
from unittest.mock import patch
from p85_signal_coordination import build_config,score,phases
from p118_temporal_arrival_holdout import tape_with_random_times
from dual_lane_v11 import run as legacy_run
from dual_lane_separate_receivers_p129 import DualConfig as ForkConfig,run as fork_run
from receiving_cells_v15 import ReceivingCells

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
TOPO=(('shared4',4,'shared'),('separate2+2',2,'movement_separate'),('separate4+4',4,'movement_separate'))

def config(seed,share,slots,topology):
    baseline=build_config(seed,900,share,7,slots,.5)
    return ForkConfig(**{f.name:getattr(baseline,f.name) for f in fields(type(baseline))},receiver_topology=topology)

def arm(cfg,tape,cp,period,runner):
    def green(self,t):
        assert t>=84
        return (t-84)%period>=period//2
    with patch.object(ReceivingCells,'green',green):
        r=runner(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'))
    assert r['generated']==60 and r['remaining']==0 and r['network_out_S']+r['network_out_L']==60
    return {'cost':score(r,0),'denied':r['receiver_denied_seconds'],'network_out_L':r['network_out_L'],'network_out_S':r['network_out_S'],'receiver_occupancy':r['max_receiver'],'entrance_denied_attempts':r['receiver_denied_attempts']}

def run_experiment():
    original=json.loads((HERE/'P127_RESULT.json').read_text())
    ref={(x['share'],x['label_seed'],x['time_seed'],x['family'],x['capacity']):x for x in original['rows']}
    assert len(ref)==72
    src_sha=hashlib.sha256((ROOT/'dual_lane_v11.py').read_bytes()).hexdigest()
    fork_sha=hashlib.sha256((ROOT/'dual_lane_separate_receivers_p129.py').read_bytes()).hexdigest()
    rows=[]
    for share,label_seed,time_seed,family in product((.5,.75),(86001,86002),(88301,88302),('stochastic_uniform','stochastic_platoon4')):
        proto=build_config(label_seed,900,share,7,4,.5)
        tape=tape_with_random_times(proto,label_seed,time_seed,family)
        for name,slots,topo in TOPO:
            cfg=replace(config(label_seed,share,slots,topo),base=replace(proto.base,duration_s=4800))
            cp=fork_run(cfg,tape,checkpoint_at=84)
            short=arm(cfg,tape,cp,30,fork_run)
            long=arm(cfg,tape,cp,60,fork_run)
            if name=='shared4':
                original_cfg=replace(build_config(label_seed,900,share,7,slots,.5),base=replace(proto.base,duration_s=4800))
                old_cp=legacy_run(original_cfg,tape,checkpoint_at=84)
                orig_short=arm(original_cfg,tape,old_cp,30,legacy_run)
                orig_long=arm(original_cfg,tape,old_cp,60,legacy_run)
                assert short==orig_short and long==orig_long,(share,label_seed,time_seed,family,short,orig_short)
                rr=ref[(share,label_seed,time_seed,family,4)]
                assert short['cost']==rr['cost30'] and long['cost']==rr['cost60']
                assert short['denied']==rr['denied30'] and long['denied']==rr['denied60']
            dc=short['cost']-long['cost']; dd=short['denied']-long['denied']
            rows.append({'share':share,'label_seed':label_seed,'time_seed':time_seed,'family':family,'topology':name,
                         'cells_per_link':slots,'total_cell_storage':slots*(2 if topo=='movement_separate' else 1),
                         'short':short,'long':long,'delta_cost':dc,'delta_denied':dd,'paradox':dd<0<dc})
        print('FINISHED',share,label_seed,time_seed,family,flush=True)
    assert len(rows)==48
    summary={}
    for share in (.5,.75):
        summary[str(share)]={}
        for name,_,_ in TOPO:
            x=[r for r in rows if r['share']==share and r['topology']==name]
            assert len(x)==8
            summary[str(share)][name]={'n':len(x),'paradox':sum(v['paradox'] for v in x),
                    'short_cost_worse':sum(v['delta_cost']>0 for v in x),
                    'mean_delta_cost':sum(v['delta_cost'] for v in x)/len(x),
                    'mean_delta_denied':sum(v['delta_denied'] for v in x)/len(x),
                    'min_cost_delta':min(v['delta_cost'] for v in x),'max_cost_delta':max(v['delta_cost'] for v in x)}
    result={'status':'P129_MOVEMENT_SEGREGATED_RECEIVER_96_ARMS_COMPLETE',
            'prereg':'P129_SPLIT_RECEIVER_TOPOLOGY_PREREG.md','source_dual_lane_sha256':src_sha,'fork_sha256':fork_sha,
            'simulator_arms':96,'matched_signal_pairs':48,'original_engine_regression_arms':32,
            'all_cleared':True,'legacy_regression_exact':True,'summary':summary,'rows':rows,
            'interpretation_limit':'Three models are structurally different. separate2+2 preserves aggregate cell count but halves per-movement link length and doubles exit service opportunity. separate4+4 doubles total storage and downstream exit opportunities. Cannot isolate receiver sharing from geometry/service. No SUMO or field validation.'}
    (HERE/'P129_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps(summary,ensure_ascii=False),flush=True)
    return result

if __name__=='__main__':run_experiment()
