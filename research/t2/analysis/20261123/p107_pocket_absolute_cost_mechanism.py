"""P107 post-hoc audit: compare absolute cost, maximum pocket occupancy, block events.

P106 result is known before this exploratory mechanism diagnostic. Do not claim
this was preregistered or independent field validation. Run with PYTHONPATH.
"""
from collections import Counter, defaultdict
from dataclasses import replace
from itertools import product
from pathlib import Path
from unittest.mock import patch
import json

from p85_signal_coordination import build_config,p31,run,phases,score
from receiving_cells_v15 import ReceivingCells

HERE=Path(__file__).resolve().parent


def one_arm(cfg,tape,cp,period):
    def green(link,t):
        assert t>=84 and not link.config.closure_windows
        return ((t-84)%period)>=period//2
    with patch.object(ReceivingCells,'green',green):
        r=run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'),trace=True)
    assert r['remaining']==0
    occupancy=max((len(f['pocket']) for f in r['frames'] if f['t']>=84),default=0)
    return dict(cost=score(r,0),pocket_max_occupied=occupancy,
                pocket_block_seconds=r['pocket_block_seconds'],
                network_out_S=r['network_out_S'],network_out_L=r['network_out_L'])


def experiment():
    ref=json.loads((HERE/'P106_RESULT.json').read_text())
    lookup={(r['seed'],r['clock'],r['pocket_slots']):r for r in ref['rows']}
    rows=[];by=defaultdict(Counter)
    for seed,clock in product(range(87001,87009),p31.FAMILIES):
        family={}
        for pocket_m in (7,14,28,56):
            k=pocket_m//7
            cfg=build_config(seed,900,.75,pocket_m,4,.5)
            tape=p31.clock(cfg.base,clock)
            cfg=replace(cfg,base=replace(cfg.base,duration_s=1440),downstream_offset_s=0)
            cp=run(cfg,tape,checkpoint_at=84,trace=True)
            short=one_arm(cfg,tape,cp,30)
            long=one_arm(cfg,tape,cp,60)
            expected=lookup[seed,clock,k]['delta_30_minus_60']['cost']
            assert short['cost']-long['cost']==expected
            for period,arm in ((30,short),(60,long)):
                assert arm['pocket_max_occupied']<=k
                assert arm['network_out_S']+arm['network_out_L']==len(tape)
                by[str(k)]['n_arms']+=1
                by[str(k)]['pocket_max_sum']+=arm['pocket_max_occupied']
                by[str(k)]['pocket_block_seconds_sum']+=arm['pocket_block_seconds']
                by[str(k)]['pocket_max_gt_1']+=arm['pocket_max_occupied']>1
            family[k]=dict(short=short,long=long)
            rows.append(dict(seed=seed,clock=clock,pocket_m=pocket_m,pocket_slots=k,short=short,long=long,cost_delta=expected))
        for k in (2,4,8):
            by[str(k)]['short_absolute_same_as_k1']+=family[k]['short']['cost']==family[1]['short']['cost']
            by[str(k)]['long_absolute_same_as_k1']+=family[k]['long']['cost']==family[1]['long']['cost']
            by[str(k)]['both_absolute_same_as_k1']+=(family[k]['short']['cost']==family[1]['short']['cost'] and family[k]['long']['cost']==family[1]['long']['cost'])
        by['overall']['all_four_both_absolute_identical']+=all(family[k]['short']['cost']==family[1]['short']['cost'] and family[k]['long']['cost']==family[1]['long']['cost'] for k in (2,4,8))
    assert len(rows)==64
    return dict(source='P106_RESULT.json',method='exploratory post-hoc actual run, trace=True',
                n_tapes=16,n_pairs=64,n_arms=128,by_capacity={k:dict(v) for k,v in by.items()},rows=rows)


if __name__=='__main__':
    print(json.dumps(experiment(),ensure_ascii=False,indent=2))
