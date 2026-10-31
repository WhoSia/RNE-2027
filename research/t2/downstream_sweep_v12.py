"""Shared-exit model falsification: 768 paired synthetic runs.

A virtual common discharge headway is not a real receiving-link model.
Data: 3 left ratios x 8 seeds x 4 shared-gap settings x
2 through lane allocations x 4 pocket lengths.
"""
from dataclasses import replace
from itertools import product
from statistics import mean
from pathlib import Path
import csv,json,hashlib
from dual_lane_v11 import DualConfig,run
from spatial_v10 import Config,arrivals

GAPS=(0,4,12,40)
POCKETS=(0.,14.,28.,70.)
SHARES=(.15,.30,.50)
B_SPLITS=(.5,1.)
SEEDS=range(8)

def evaluate():
    rows=[]
    for share,seed in product(SHARES,SEEDS):
        base=Config(duration_s=720,demand_vph=1500,left_fraction=share,seed=seed)
        events=arrivals(base)
        digest=hashlib.sha256(repr(events).encode()).hexdigest()
        for gap,bsplit,pocket in product(GAPS,B_SPLITS,POCKETS):
            setup=DualConfig(base=replace(base,pocket_length_m=pocket),
                through_B_share=bsplit,downstream_conflict_gap_s=gap)
            r=run(setup,events)
            rows.append({'left_fraction':share,'seed':seed,'gap_s':gap,
                'B_share':bsplit,'pocket_m':pocket,'stream_hash':digest,
                'generated':r['generated'],'exit_S':r['exit_S'],
                'exit_L':r['exit_L'],'remaining':r['remaining'],
                'common_denied_s':r['common_exit_denied_s']})
    return rows

def summarize(rows):
    output=[]
    for share,gap,bsplit,pocket in product(SHARES,GAPS,B_SPLITS,POCKETS):
        group=[r for r in rows if (r['left_fraction'],r['gap_s'],r['B_share'],r['pocket_m'])==
              (share,gap,bsplit,pocket)]
        if len(group)!=8:raise AssertionError("missing seed")
        output.append({'left_fraction':share,'gap_s':gap,'B_share':bsplit,
            'pocket_m':pocket,'mean_exit_S':mean(r['exit_S'] for r in group),
            'mean_exit_L':mean(r['exit_L'] for r in group),
            'mean_common_denied_s':mean(r['common_denied_s'] for r in group)})
    return output

if __name__=='__main__':
    dest=Path(__file__).resolve().parent/'results'
    dest.mkdir(exist_ok=True)
    rows=evaluate()
    with (dest/'downstream_768_v12.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    (dest/'downstream_summary_v12.json').write_text(json.dumps(summarize(rows),indent=2)+'\n')
    print("synthetic runs",len(rows))
