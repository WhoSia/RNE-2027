"""P115 pre-registered receiver capacity 2..64 red-start comparison, full clearing."""
import json
from dataclasses import replace
from itertools import product
from pathlib import Path
from unittest.mock import patch
from receiving_cells_v15 import ReceivingCells
from p85_signal_coordination import build_config,p31,run,score,phases

CAPS=(2,3,4,5,6,8,12,16,64)
HERE=Path(__file__).resolve().parent

def one(cfg,tape,checkpoint,period):
    def green(receiver,tick):
        assert tick>=84
        return ((tick-84)%period)>=period//2
    with patch.object(ReceivingCells,'green',green):
        r=run(cfg,tape,resume_from=checkpoint,phase_overrides=phases(6,'left_first'))
    assert r['generated']==len(tape)==60
    assert r['remaining']==0 and r['network_out_L']+r['network_out_S']==len(tape)
    return {'cost':score(r,0),'denied':r['receiver_denied_seconds'],'out_L':r['network_out_L'],'out_S':r['network_out_S']}

def main():
    rows=[]
    for capacity in CAPS:
        for seed,family in product((86001,86002),('uniform','platoon4')):
            cfg=build_config(seed,900,.75,7,capacity,.5)
            tape=p31.clock(cfg.base,family)
            cfg=replace(cfg,base=replace(cfg.base,duration_s=4800))
            cp=run(cfg,tape,checkpoint_at=84)
            a,b=one(cfg,tape,cp,30),one(cfg,tape,cp,60)
            delta_cost=a['cost']-b['cost'];delta_denied=a['denied']-b['denied']
            rows.append({'receiver_slots':capacity,'seed':seed,'family':family,
                         'short':a,'long':b,'delta_cost':delta_cost,'delta_denied':delta_denied,
                         'paradox':delta_cost>0>delta_denied})
        print('CAPACITY',capacity, 'cost+',sum(r['delta_cost']>0 for r in rows if r['receiver_slots']==capacity),
              'paradox',sum(r['paradox'] for r in rows if r['receiver_slots']==capacity),flush=True)
    by={str(c):{'paradox':sum(r['paradox'] for r in rows if r['receiver_slots']==c),
                 'cost_30_worse':sum(r['delta_cost']>0 for r in rows if r['receiver_slots']==c),
                 'cost_delta_sum':sum(r['delta_cost'] for r in rows if r['receiver_slots']==c),
                 'denial_delta_sum':sum(r['delta_denied'] for r in rows if r['receiver_slots']==c)} for c in CAPS}
    result={'status':'P115_72_ARMS_COMPLETE_CONDITIONAL_T2','prereg':'P115_RECEIVER_FRONTIER_PREREG.md',
            'seed_blocks':2,'label_tapes':4,'capacity_levels':list(CAPS),'paired_comparisons':36,'simulator_arms':72,
            'all_complete':True,'summary':by,'rows':rows,
            'capacity_16_vs_4_gate':by['16']['paradox']<by['4']['paradox'],
            'caveat':'Not a physical network; changing receiver cell count changes pre-t84 checkpoint states across capacities. Matched within each capacity only.'}
    (HERE/'P115_RESULT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print('RESULT',json.dumps({'gate':result['capacity_16_vs_4_gate'],'summary':by},ensure_ascii=False))
if __name__=='__main__':main()
