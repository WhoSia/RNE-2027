"""Predeclared breadth-first test of C7/C8 frontier across left-turn shares."""
import hashlib,json
from itertools import product
from dataclasses import replace
from pathlib import Path
from collections import defaultdict
from p85_signal_coordination import build_config,run
from p118_temporal_arrival_holdout import tape_with_random_times,arm

HERE=Path(__file__).resolve().parent
SHARES=(.25,.50,.75);CAPS=(4,7,8)

def main():
    rows=[];hashes={share:set() for share in SHARES}
    for share,seed,tseed,family in product(SHARES,(86001,86002),(88301,88302),('stochastic_uniform','stochastic_platoon4')):
        proto=build_config(seed,900,share,7,4,.5)
        tape=tape_with_random_times(proto,seed,tseed,family)
        stamp=hashlib.sha256(json.dumps([t for t,_ in tape],separators=(',',':')).encode()).hexdigest()
        assert stamp not in hashes[share];hashes[share].add(stamp)
        for cap in CAPS:
            cfg=build_config(seed,900,share,7,cap,.5)
            cfg=replace(cfg,base=replace(cfg.base,duration_s=4800))
            cp=run(cfg,tape,checkpoint_at=84)
            short=arm(cfg,tape,cp,30);long=arm(cfg,tape,cp,60)
            dc=short['cost']-long['cost'];dd=short['denied']-long['denied']
            rows.append({'share':share,'capacity':cap,'label_seed':seed,'time_seed':tseed,'family':family,
                         'time_sha256':stamp,'left_labels':sum(m=='L' for _,m in tape),
                         'cost30':short['cost'],'cost60':long['cost'],'denied30':short['denied'],
                         'denied60':long['denied'],'delta_cost':dc,'delta_denied':dd,'paradox':dd<0<dc})
        print('FINISHED',share,seed,tseed,family,flush=True)
    assert all(len(hashes[s])==8 for s in SHARES) and len(rows)==72
    summary={}
    for share in SHARES:
        summary[str(share)]={}
        for cap in CAPS:
            cases=[r for r in rows if r['share']==share and r['capacity']==cap]
            assert len(cases)==8
            summary[str(share)][str(cap)]={'matched':8,'paradox':sum(x['paradox'] for x in cases),
                'cost30_worse':sum(x['delta_cost']>0 for x in cases),
                'mean_delta_cost':sum(x['delta_cost'] for x in cases)/8,
                'sum_delta_denied':sum(x['delta_denied'] for x in cases),
                'min_delta_cost':min(x['delta_cost'] for x in cases),'max_delta_cost':max(x['delta_cost'] for x in cases)}
    result={'status':'P127_144_ARMS_MOVEMENT_SCOPE_COMPLETE','prereg':'P127_MOVEMENT_MIX_SCOPE_PREREG.md',
        'simulator_arms':144,'matched_comparisons':72,'tapes':24,'time_hashes_per_share':{str(s):len(hashes[s]) for s in SHARES},
        'all_clear':True,'summary':summary,'rows':rows,
        'broad_frontier_falsifier':any(r['paradox'] for r in rows if r['capacity']==8 and r['share']!=.75) or any(not r['paradox'] for r in rows if r['capacity']==7 and r['share']==.75),
        'limitation':'Same synthetic T2 engine; timestamps deliberately share random roots across turn-share strata. Fixed 900vph, 2 label seeds, 2 timing seeds per family; no field claim.'}
    (HERE/'P127_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',json.dumps({'summary':summary,'falsifier':result['broad_frontier_falsifier']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
