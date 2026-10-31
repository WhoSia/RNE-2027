"""Predeclared 576-run temporal coordination design.

2 rate profiles x 2 turn profiles x 2 upstream platoon offsets x
3 signal offsets x 4 pocket lengths x 6 seeds. Reuse exact same
arrival stream across signal and pocket interventions per seed.
Synthetic comparisons only; not field calibration.
"""
from dataclasses import replace
from itertools import product
from collections import defaultdict
from statistics import mean
from pathlib import Path
import hashlib,csv,json
from spatial_v10 import Config
from dual_lane_v11 import DualConfig,run
from arrival_design_v14 import ArrivalProfile,make_arrivals

RATES={'steady':(1500,),'surge':(900,2100)}
TURNS={'steady':(.3,),'shift':(.1,.5)}
AOFF=(0,30)
SOFF=(0,20,40)
LENGTHS=(14.,28.,42.,70.)
SEEDS=range(6)

def evaluate():
    rows=[]
    for rate,turn,aoff,seed in product(RATES,TURNS,AOFF,SEEDS):
        stream=make_arrivals(ArrivalProfile(seed=seed,arrival_offset_s=aoff,
            rates_vph=RATES[rate],left_shares=TURNS[turn]))
        digest=hashlib.sha256(repr(stream).encode()).hexdigest()
        for soff,length in product(SOFF,LENGTHS):
            base=Config(duration_s=720,seed=seed,signal_offset_s=soff,
                pocket_length_m=length,demand_vph=1500)
            config=DualConfig(base=base,through_B_share=.5,
                receiver_slots=2,receiver_headway_s=4)
            x=run(config,stream)
            if x['generated']!=x['network_out_S']+x['network_out_L']+x['remaining']:
                raise AssertionError('network vehicle conservation')
            rows.append({'rate':rate,'turn':turn,'arrival_offset':aoff,'seed':seed,
                'signal_offset':soff,'pocket_m':length,'arrival_sha':digest,
                'generated':x['generated'],'network_S':x['network_out_S'],
                'network_L':x['network_out_L'],
                'network_total':x['network_out_S']+x['network_out_L'],
                'stopline_S':x['exit_S'],'stopline_L':x['exit_L'],
                'outside':x['outside'],'receiver_final':x['receiver_final'],
                'receiver_full_denied_s':x['receiver_full_denied_s']})
    if len(rows)!=576:raise AssertionError('factorial incomplete')
    return rows

def summarize(rows):
    groups=defaultdict(list)
    for r in rows:
        k=(r['rate'],r['turn'],r['arrival_offset'],r['signal_offset'],r['pocket_m'])
        groups[k].append(r)
    out=[]
    for k,group in sorted(groups.items()):
        if len(group)!=6:raise AssertionError('missing seeds')
        x=dict(zip(('rate','turn','arrival_offset','signal_offset','pocket_m'),k))
        x.update({'mean_network_S':mean(r['network_S'] for r in group),
            'mean_network_L':mean(r['network_L'] for r in group),
            'mean_total':mean(r['network_total'] for r in group),
            'mean_outside':mean(r['outside'] for r in group)})
        out.append(x)
    return out

if __name__=='__main__':
    root=Path(__file__).resolve().parent/'results'
    root.mkdir(exist_ok=True)
    rows=evaluate()
    with (root/'temporal_576_v14.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    (root/'temporal_summary_v14.json').write_text(json.dumps(summarize(rows),indent=2)+'\n')
    print('runs',len(rows))
