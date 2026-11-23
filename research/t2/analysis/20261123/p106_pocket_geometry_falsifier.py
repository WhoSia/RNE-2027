"""P106: preregistered 1/2/4/8-cell pocket-length falsification.

PRE-EXISTING prereg commit: cab02b203aad8312698ca6313993821472a32455.
Only new seeds 87001..87008, red onset, 75% left demand, 30 vs 60 sec.
Run with PYTHONPATH including research/t2 and analysis/20261122.
"""
from collections import Counter
from dataclasses import replace
from itertools import product
import json
from pathlib import Path
from p85_signal_coordination import build_config,p31,run
from p87_half_green import measure
from spatial_v10 import validate

HERE=Path(__file__).resolve().parent
LENGTHS=(7,14,28,56)
SEEDS=range(87001,87009)


def experiment():
    rows=[]; totals={}
    for pocket_m in LENGTHS:
        block=Counter()
        for seed,clock in product(SEEDS,p31.FAMILIES):
            cfg=build_config(seed,900,.75,pocket_m,4,.5)
            n,k=validate(cfg.base)
            assert n==20 and k==pocket_m//7 and cfg.receiver_slots==4
            tape=p31.clock(cfg.base,clock)
            cfg=replace(cfg,base=replace(cfg.base,duration_s=1440),downstream_offset_s=0)
            cp=run(cfg,tape,checkpoint_at=84,trace=True)
            assert cp['state']['count']['network_out_S']>=0
            small=measure(cfg,tape,cp,30,False)
            large=measure(cfg,tape,cp,60,False)
            delta={key:small[key]-large[key] for key in small}
            flag=delta['denied']<0<delta['cost']
            block['n']+=1
            block['paradox']+=flag
            block['30_cost_worse']+=delta['cost']>0
            block['30_cost_better']+=delta['cost']<0
            block['cost_sum']+=delta['cost']
            block['denied_sum']+=delta['denied']
            rows.append(dict(seed=seed,clock=clock,share=.75,onset='red',
                             pocket_length_m=pocket_m,pocket_slots=k,
                             generated=len(tape),delta_30_minus_60=delta,paradox=flag))
        assert block['n']==16
        block['cost_mean']=block['cost_sum']/16
        block['preregistered_geometry_robustness_pass']=block['paradox']>=14 if pocket_m>7 else None
        totals[str(pocket_m)]=dict(block)
    assert len(rows)==64
    return dict(prereg='P106_POCKET_GEOMETRY_PREREG.md',status='FULL_REPLAY_COMPLETE',
                source='same T2 model; new seeds 87001..87008; not independent engine',
                physical_correction='pocket_length_m=7 and cell_m=7 imply ONE pocket slot',
                pocket_length_m_to_slots={'7':1,'14':2,'28':4,'56':8},
                unique_seed_blocks=8,unique_demand_tapes=16,
                paired_comparisons=64,simulator_arms=128,
                summary=totals,rows=rows)


if __name__=='__main__':
    print(json.dumps(experiment(),ensure_ascii=False,indent=2))
