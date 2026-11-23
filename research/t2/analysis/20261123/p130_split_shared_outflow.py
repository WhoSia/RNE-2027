"""P130: shared global downstream discharge headway across separate L/S links."""
from dataclasses import replace,fields
from itertools import product
from pathlib import Path
import json,hashlib
from unittest.mock import patch
from p85_signal_coordination import build_config,score,phases
from p118_temporal_arrival_holdout import tape_with_random_times
from dual_lane_separate_receivers_p130 import DualConfig,MovementSeparateReceiver,run
from receiving_cells_v15 import ReceivingCells,LinkConfig
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent

def unit_test():
    link=MovementSeparateReceiver(LinkConfig(cells=2,downstream_cycle_s=30,downstream_green_s=30,exit_headway_s=2),shared_exit=True)
    assert link.accept((0,'L',0)) and link.accept((1,'S',0))
    link.links['L'].occupied={1:(0,'L',0)}
    link.links['S'].occupied={1:(1,'S',0)}
    x=link.tick(2)
    assert x==((1,'S',0),) and len(link)==1 and link.last_global_exit==2
    assert link.tick(3)==() and len(link)==1
    assert link.tick(4)==((0,'L',0),) and len(link)==0
    link.audit()
    return True

def config(seed,share):
    b=build_config(seed,900,share,7,2,.5)
    d={f.name:getattr(b,f.name) for f in fields(type(b))}
    return replace(DualConfig(**d,receiver_topology='movement_separate_shared_exit'),base=replace(b.base,duration_s=4800))

def arm(cfg,tape,cp,period):
    def green(self,t):
        assert t>=84
        return (t-84)%period>=period//2
    with patch.object(ReceivingCells,'green',green):
        r=run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'),trace=True)
    assert r['remaining']==0 and r['generated']==r['network_out_L']+r['network_out_S']==60
    # Every exiting ID appears once, from the exact same receiver logic.
    out=r['cycles'][-1]
    assert out['network_out_L']+out['network_out_S']==60
    cp_exits=list(cp['state']['receiver'].exits)
    after=[(frame['t'],frame['receiver']) for frame in r['frames'] if frame['t']>=84]
    # Independently reconstruct final departures from movement-tagged receiver
    # snapshots; enforce the single global exit-clock on ALL 60 vehicle IDs.
    previous={v[2] for v in cp['state']['receiver'].snapshot()}
    exited=[(t,vid) for t,vid,movement in cp_exits]
    assert len(set(vid for _,vid in exited))==len(exited)
    for t,cells in after:
        assert len({x[2] for x in cells})==len(cells)
        assert all(m==mov for m,pos,vid,mov in cells)
        current={v[2] for v in cells}
        for vid in previous-current:
            assert vid not in {v for _,v in exited}
            exited.append((t,vid))
        previous=current
    assert len(exited)==60 and {vid for _,vid in exited}==set(range(60))
    times=sorted(t for t,_ in exited)
    assert all(b-a>=2 for a,b in zip(times,times[1:])), ('shared_exit_headway',times)
    assert r['receiver_final']==0
    return {'cost':score(r,0),'denied':r['receiver_denied_seconds'],
            'exit_L':r['network_out_L'],'exit_S':r['network_out_S'],
            'max_receiver':r['max_receiver']}

def main():
    assert unit_test()
    reference=json.loads((HERE/'P129_RESULT.json').read_text())
    key={(r['share'],r['label_seed'],r['time_seed'],r['family'],r['topology']):r for r in reference['rows']}
    rows=[]
    for share,labelseed,timeseed,family in product((.5,.75),(86001,86002),(88301,88302),('stochastic_uniform','stochastic_platoon4')):
        cfg=config(labelseed,share)
        tape=tape_with_random_times(build_config(labelseed,900,share,7,2,.5),labelseed,timeseed,family)
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        short=arm(cfg,tape,cp,30);long=arm(cfg,tape,cp,60)
        dc=short['cost']-long['cost'];dd=short['denied']-long['denied']
        rows.append({'share':share,'label_seed':labelseed,'time_seed':timeseed,'family':family,
                     'delta_cost':dc,'delta_denied':dd,'paradox':dd<0<dc,'short':short,'long':long,
                     'shared4_delta':key[(share,labelseed,timeseed,family,'shared4')]['delta_cost'],
                     'separate2plus2_delta':key[(share,labelseed,timeseed,family,'separate2+2')]['delta_cost']})
        print('FINISHED',share,labelseed,timeseed,family,flush=True)
    assert len(rows)==16
    summary={}
    for share in (.5,.75):
        group=[x for x in rows if x['share']==share]
        summary[str(share)]={'n':8,'paradox':sum(x['paradox'] for x in group),
                             'short_cost_worse':sum(x['delta_cost']>0 for x in group),
                             'mean_delta_cost':sum(x['delta_cost'] for x in group)/8,
                             'mean_delta_denied':sum(x['delta_denied'] for x in group)/8,
                             'min_cost_delta':min(x['delta_cost'] for x in group),
                             'max_cost_delta':max(x['delta_cost'] for x in group)}
    result={'status':'P130_SHARED_DOWNSTREAM_HEADWAY_32_ARMS_COMPLETE',
            'prereg':'P130_SPLIT_SHARED_OUTFLOW_PREREG.md',
            'fork_source_sha256':hashlib.sha256((ROOT/'dual_lane_separate_receivers_p130.py').read_bytes()).hexdigest(),
            'simulator_arms':32,'matched_signal_pairs':16,'all_cleared':True,
            'unit_test_shared_exit_pass':True,'summary':summary,'rows':rows,
            'limits':'Same T2 fork; separate two-cell movement links + shared downstream headway; entry link per movement and lane length still different from original shared4. Fixed S-before-L simultaneous-exit precedence is a new assumption. No independent engine or field evidence.'}
    (HERE/'P130_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps(summary,ensure_ascii=False),flush=True)
    return result
if __name__=='__main__':main()
