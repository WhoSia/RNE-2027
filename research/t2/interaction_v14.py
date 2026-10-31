"""Matched finite-difference interaction: signal phase offset x pocket length.

For each seed compare pocket 70 vs 14 under signal offset 40 vs 0,
holding the full upstream timestamp/route stream fixed. The result
is model-conditional, NOT measured or real-world causal inference.
"""
from collections import defaultdict
from statistics import mean
from pathlib import Path
import csv,json

def analyze(rows):
    index={}
    for r in rows:
        k=(r['rate'],r['turn'],int(r['arrival_offset']),int(r['seed']),
            int(r['signal_offset']),float(r['pocket_m']))
        if k in index:raise ValueError('duplicate design cell')
        index[k]=r
    out=[]
    for rate in ('steady','surge'):
        for turn in ('steady','shift'):
            for aoff in (0,30):
                gains={}
                for soff in (0,20,40):
                    values=[]
                    for seed in range(6):
                        key=(rate,turn,aoff,seed,soff)
                        lo=index[key+(14.,)]
                        hi=index[key+(70.,)]
                        values.append(int(hi['network_total'])-int(lo['network_total']))
                    gains[soff]=values
                diffs=[gains[40][i]-gains[0][i] for i in range(6)]
                out.append({'rate':rate,'turn':turn,'arrival_offset':aoff,
                    'long_minus_short_at_signal0':mean(gains[0]),
                    'long_minus_short_at_signal40':mean(gains[40]),
                    'interaction_signal40_vs_0':mean(diffs),
                    'per_seed_interaction':diffs})
    return out

if __name__=='__main__':
    path=Path(__file__).resolve().parent/'results'
    with (path/'temporal_576_v14.csv').open(newline='') as f:
        rows=list(csv.DictReader(f))
    z=analyze(rows)
    (path/'temporal_interactions_v14.json').write_text(json.dumps(z,indent=2)+'\n')
    print('strata',len(z))
