"""P99: align post-decision horizon to whole 60s cycles and reproduce all P89 deltas.

At t=84 fixed checkpoint, compare t=1440 (1356s) with t=1464 (1380s =23*60).
Same archived arrival tape and startup-loss masks. P99 checks ALL 768 paired contrasts
and full clearance. Nominal green exposure is now equal for 30/60 and both onsets.
"""
from collections import Counter
from dataclasses import replace
from itertools import product
import json
from pathlib import Path

from p85_signal_coordination import build_config, p31, run
from p89_startup_loss import trial, exposure, PERIODS, LOSSES, START

HERE = Path(__file__).resolve().parent
STOP = 1464

def experiment():
    ref = json.loads((HERE/'P89_RESULT.json').read_text())
    baseline = {(r['seed'],r['share'],r['clock'],r['onset'],r['lost_seconds_per_green']):r
                for r in ref['rows']}
    assert len(baseline)==768
    exposures={f'{p}/{onset}/{loss}':exposure(p,onset,loss,STOP)
               for p,onset,loss in product(PERIODS,('green','red'),LOSSES)}
    assert all(exposures[f'{p}/{onset}/0']['displayed_green_seconds']==690
               for p in PERIODS for onset in ('green','red'))
    comparisons=0;total_cost_difference=0;bad=[];rank_changed=0;by=Counter()
    for seed,share,clock in product(range(85001,85017),(.25,.5,.75),p31.FAMILIES):
        cfg=build_config(seed,900,share,7,4,.5)
        tape=p31.clock(cfg.base,clock)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=STOP),downstream_offset_s=0)
        cp=run(cfg,tape,checkpoint_at=START)
        for onset,loss in product(('green','red'),LOSSES):
            short,long=(trial(cfg,tape,cp,p,onset,loss) for p in PERIODS)
            x={k:short[k]-long[k] for k in ('cost','denied')}
            expected=baseline[seed,share,clock,onset,loss]['delta_30_minus_60']
            comparisons+=1
            total_cost_difference+=x['cost']
            by[f'{onset}/{loss}/cost_sum']+=x['cost']
            if x!=expected:
                bad.append((seed,share,clock,onset,loss,expected,x))
            rank_changed+=((x['cost']>0)-(x['cost']<0))!=((expected['cost']>0)-(expected['cost']<0))
    assert comparisons==768 and not bad and rank_changed==0
    return dict(evidence='full 1536 run repeat with integer-cycle observation window',
                reference='P89_RESULT.json',horizon_original=1440,horizon_aligned=STOP,
                postdecision_window_seconds=STOP-START,
                displayed_green_seconds_at_zero_loss=690,
                paired_comparisons=comparisons,exact_matches=comparisons-len(bad),
                changed_cost_rankings=rank_changed,all_clearance_assertions_passed=True,
                total_signed_cost_difference=sum(r['delta_30_minus_60']['cost'] for r in ref['rows']),
                source_sum_repeated=total_cost_difference,
                exposures=exposures,group_cost_sums=dict(by),
                caveat='SYNTHETIC_ONLY; matching costs removes finite-horizon counting as the driver of these comparisons, not other structural confounding')

if __name__=='__main__':
    print(json.dumps(experiment(),indent=2))
