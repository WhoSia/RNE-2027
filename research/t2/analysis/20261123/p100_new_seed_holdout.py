"""P100: pre-registered 32 fresh seeds under P87 common-checkpoint cycle comparison."""
from collections import Counter,defaultdict
from dataclasses import replace
from itertools import product
from pathlib import Path
import json
from p85_signal_coordination import build_config,p31,run
from p87_half_green import measure

HERE=Path(__file__).resolve().parent
SEEDS=range(86001,86033)


def experiment():
    output=[];summary=defaultdict(Counter)
    for seed,share,clock in product(SEEDS,(.25,.5,.75),p31.FAMILIES):
        cfg=build_config(seed,900,share,7,4,.5)
        tape=p31.clock(cfg.base,clock)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=1440),downstream_offset_s=0)
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        delta_by={}
        for onset in ('green','red'):
            a=measure(cfg,tape,cp,30,onset=='green')
            b=measure(cfg,tape,cp,60,onset=='green')
            d={k:a[k]-b[k] for k in a}
            delta_by[onset]=d
            group=f'{onset}/{share}/{clock}'
            summary[group]['n']+=1
            summary[group]['paradox']+=d['denied']<0<d['cost']
            summary[group]['cost_better']+=d['cost']<0
            summary[group]['cost_worse']+=d['cost']>0
            summary[group]['denied_better']+=d['denied']<0
            summary[group]['cost_delta_sum']+=d['cost']
            output.append(dict(seed=seed,share=share,clock=clock,onset=onset,delta=d))
        both=(delta_by['green']['denied']<0<delta_by['green']['cost'] and
              delta_by['red']['denied']<0<delta_by['red']['cost'])
        summary['paired']['both_onsets_paradox']+=both
        summary['paired']['n']+=1
    assert len(output)==384 and summary['paired']['n']==192
    hi=sum(r['delta']['denied']<0<r['delta']['cost'] for r in output if r['share']==.75 and r['onset']=='red')
    low=sum(r['delta']['denied']<0<r['delta']['cost'] for r in output if r['share']==.25 and r['onset']=='green')
    return dict(prereg='P100_HOLDOUT_PREREG.md',source='p87_half_green.py',
                source_status='SYNTHETIC_UNCALIBRATED',seed_range=[86001,86032],
                unique_tapes=192,pairs=384,simulator_runs=768,
                target_high_share_red_paradox=dict(observed=hi,total=64,target=52,passed=hi>=52),
                exploratory_low_share_green_paradox=dict(observed=low,total=64,target=20,passed=low>=20),
                summary={k:dict(v) for k,v in sorted(summary.items())},rows=output)

if __name__=='__main__':
    print(json.dumps(experiment(),indent=2))
