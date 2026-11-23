"""P97: whether *absolute* full-network costs are monotone in startup blanking.

Unlike P89's only 30s-minus-60s delta, this retains both per-policy costs.
Run: python p97_loss_monotonicity_audit.py > P97_RESULT.json
"""
from collections import Counter
from dataclasses import replace
from itertools import product
from pathlib import Path
import json
from p85_signal_coordination import build_config, p31, run
from p89_startup_loss import trial, PERIODS, LOSSES, START

HERE=Path(__file__).resolve().parent


def experiment():
    reference={(r['seed'],r['share'],r['clock'],r['onset'],r['lost_seconds_per_green']):r
        for r in json.loads((HERE/'P89_RESULT.json').read_text())['rows']}
    assert len(reference)==768
    rows=[]; summary=Counter(); examples=[]
    for seed,share,clock in product(range(85001,85017),(.25,.5,.75),p31.FAMILIES):
        cfg=build_config(seed,900,share,7,4,.5);tape=p31.clock(cfg.base,clock)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=1440),downstream_offset_s=0)
        cp=run(cfg,tape,checkpoint_at=START)
        for onset in ('green','red'):
            costs={str(p):[] for p in PERIODS}; denials={str(p):[] for p in PERIODS}
            for loss in LOSSES:
                for p in PERIODS:
                    arm=trial(cfg,tape,cp,p,onset,loss)
                    costs[str(p)].append(arm['cost'])
                    denials[str(p)].append(arm['denied'])
                d=costs['30'][-1]-costs['60'][-1]
                expected=reference[seed,share,clock,onset,loss]['delta_30_minus_60']
                assert d==expected['cost'] and denials['30'][-1]-denials['60'][-1]==expected['denied']
            deviations={str(p):[costs[str(p)][i+1]-costs[str(p)][i] for i in range(3)] for p in PERIODS}
            for p in PERIODS:
                for step,d in enumerate(deviations[str(p)]):
                    summary[f'{onset}/{p}/step_{step}_cost_lower']+=d<0
                    summary[f'{onset}/{p}/step_{step}_cost_equal']+=d==0
                    summary[f'{onset}/{p}/step_{step}_cost_higher']+=d>0
            if any(x<0 for v in deviations.values() for x in v) and len(examples)<8:
                examples.append(dict(seed=seed,share=share,clock=clock,onset=onset,costs=costs,changes=deviations))
            rows.append(dict(seed=seed,share=share,clock=clock,onset=onset,cost_by_period=costs,
                             denied_by_period=denials,stepwise_loss_cost_change=deviations))
    assert len(rows)==192
    return dict(source='P89_RESULT.json',description='absolute full-network costs under each startup loss; 0,1,2,3 seconds',
                caveat='synthetic finite receiver; monotone signal service does not force monotone network cost if vehicle order changes',
                summary=dict(summary),rows=rows,counterexamples=examples)

if __name__=='__main__':
    print(json.dumps(experiment(),indent=2))
