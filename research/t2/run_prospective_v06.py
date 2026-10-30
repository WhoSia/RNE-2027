"""Run frozen v0.6 challenge against spatial_v05 (NOT a new physical model).

Invoke explicitly, not during discovery:
 python research/t2/run_prospective_v06.py --output /tmp/t2-v06.json
This runner has not been used to select hypotheses or tune thresholds.
"""
from __future__ import annotations
import argparse, json
from dataclasses import asdict, replace
from pathlib import Path
from prospective_court_v06 import (
    EXPLORATION_SEEDS, HOLDOUT_SEEDS, FORKS, CAPS, MODES, UPDATES,
    interaction, negative_control_no_left, sign_court, validate_split)
from spatial_v05 import Config, build_arrivals, simulate


def four_cells(config: Config, arrivals=None) -> dict[tuple[int,int],int]:
    if arrivals is None:
        arrivals=build_arrivals(config)
    return {(f,k):simulate(replace(config,fork_cells=f,bay_limit=k),
                            arrivals,audit=True)['stats']['exits']
            for f in FORKS for k in CAPS}


def execute() -> dict:
    validate_split()
    output={'status':'COMPUTED_IN_TOY_MODEL',
            'model':'spatial_v05','seeds_exploration':list(EXPLORATION_SEEDS),
            'seeds_holdout':list(HOLDOUT_SEEDS),'factorial_interactions':{},
            'placebo_no_left':{},'limitations':[
                'Holdout seeds are NOT independent field sites or different model classes.',
                'Gate K is virtual admission cap, not actual bay length.',
                'Arrival stream is fixed per paired geometry and capacity contrast.',
                'A sign pass cannot validate transport to physical roads or SUMO.']}
    for mode in MODES:
        for update in UPDATES:
            discovery=[]
            holdout=[]
            for seed in EXPLORATION_SEEDS+HOLDOUT_SEEDS:
                c=Config(seed=seed,signal_mode=mode,update_mode=update,clearance_s=3)
                contrast=interaction(four_cells(c))
                (discovery if seed in EXPLORATION_SEEDS else holdout).append(contrast)
            key=f'{mode}|{update}'
            verdict=sign_court(tuple(discovery),tuple(holdout))
            output['factorial_interactions'][key]={
                'discovery':discovery,'holdout':holdout,
                'verdict':asdict(verdict)}
            # Exact negative control: same fork and all-straight arrival stream.
            placebo=Config(duration=600,seed=100,left_fraction=0.0,
                           signal_mode=mode,update_mode=update,clearance_s=3)
            pc=negative_control_no_left(four_cells(placebo))
            output['placebo_no_left'][key]=asdict(pc)
    return output


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    result=execute()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    summary={k:v['verdict']['status'] for k,v in result['factorial_interactions'].items()}
    print(json.dumps({'sign_verdicts':summary,
                      'placebos':{k:v['status'] for k,v in result['placebo_no_left'].items()}},indent=2))


if __name__=='__main__':
    main()
