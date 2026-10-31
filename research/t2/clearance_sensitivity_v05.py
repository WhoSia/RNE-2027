"""Reproduce 3-s clearance sensitivity across both signal and movement updates."""
import csv,hashlib,json,statistics
from pathlib import Path
from dataclasses import replace
from spatial_v05 import Config,build_arrivals,simulate


def main():
    rows=[]
    for update in ('sequential','parallel'):
        for mode in ('leading','lagging'):
            for seed in range(10):
                c=Config(seed=seed,signal_mode=mode,update_mode=update,clearance_s=3)
                arrivals=build_arrivals(c)
                for f in (-21,-13):
                    for cap in (2,4):
                        r=simulate(replace(c,fork_cells=f,bay_limit=cap),arrivals)
                        rows.append({'update_mode':update,'signal_mode':mode,'seed':seed,
                            'fork_cells':f,'bay_limit':cap,'exits':r['stats']['exits']})
    summary={}
    for update in ('sequential','parallel'):
        for mode in ('leading','lagging'):
            pairs=[]
            for seed in range(10):
                q={(r['fork_cells'],r['bay_limit']):r['exits'] for r in rows
                   if r['seed']==seed and r['update_mode']==update and r['signal_mode']==mode}
                pairs.append((q[-13,4]-q[-13,2])-(q[-21,4]-q[-21,2]))
            summary[update+'|'+mode]={'mean_I':statistics.mean(pairs),
                'per_seed_I':pairs,'all_negative':all(x<0 for x in pairs)}
    out=Path(__file__).resolve().parent/'results'
    with (out/'clearance3_runs.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/'clearance3_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
