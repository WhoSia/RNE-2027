"""Exploratory AFTER P22 preregistration: alternative terminal penalties in P19.

Requires exact research/t2 main engine and analysis/20261122 scripts on PYTHONPATH.
"""
from collections import defaultdict
from dataclasses import replace
from itertools import product
from pathlib import Path
import json


def execute(reference_path):
    from p19_receiver_service_opportunity import (REGIMES, SEEDS, RECEIVERS, OFFSETS,
        POCKETS, B_SHARES, ACTION, build_config, arrival_clock_pair)
    from dual_lane_v11 import run
    from physical_transfer_screen import score
    reference=json.loads(Path(reference_path).read_text(encoding='utf-8'))
    frozen={ (r['demand_vph'],r['left_fraction'],r['seed'],r['receiver_capacity'],
        r['downstream_offset_s'],r['pocket_m'],r['b_share']):r['model_delta'] for r in reference['records'] }
    if len(frozen)!=256:raise ValueError('P19 frozen reference rows missing or duplicate')
    rows=[]
    for (demand,turn),seed,cap,off,pocket,bshare in product(REGIMES,SEEDS,RECEIVERS,OFFSETS,POCKETS,B_SHARES):
        cfg=replace(build_config(seed,demand,turn,pocket,cap,bshare),downstream_offset_s=off)
        _,tape=arrival_clock_pair(cfg.base)
        checkpoint=run(cfg,tape,checkpoint_at=84)
        control=run(cfg,tape,resume_from=checkpoint)
        treatment=run(cfg,tape,resume_from=checkpoint,phase_overrides=ACTION)
        key=(demand,turn,seed,cap,off,pocket,bshare)
        deltas={str(p):score(treatment,p)-score(control,p) for p in (0,60,120)}
        if deltas['60']!=frozen[key]:raise AssertionError('existing P19 cost changed')
        rows.append({'offset':off,'seed':seed,'cap':cap,'delta':deltas})
    return aggregate(rows)


def aggregate(rows):
    if len(rows)!=256:raise ValueError('not a full P19 cohort')
    result={}
    for off,p in product((0,15),(0,60,120)):
        subset=[r['delta'][str(p)] for r in rows if r['offset']==off]
        if len(subset)!=128:raise ValueError('missing offset cohort')
        result[f'offset_{off}_penalty_{p}']={
            'harmful':sum(d>0 for d in subset),
            'helpful':sum(d<0 for d in subset),
            'ties':sum(d==0 for d in subset),
            'sum_delta':sum(subset),
        }
    return {'scope':'EXPLORATORY_POSTPREREG_SYNTHETIC_OBJECTIVE_SENSITIVITY',
        'canonical_p19_delta60_verified':len(rows),'summary':result,
        'interpretation':'Stability across three model terminal penalties is not external reality or legal action feasibility.'}

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser()
    a.add_argument('frozen_p19_json',type=Path)
    a.add_argument('output_json',type=Path)
    x=a.parse_args()
    x.output_json.write_text(json.dumps(execute(x.frozen_p19_json),sort_keys=True,indent=2)+'\n',encoding='utf-8')
