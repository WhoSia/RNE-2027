"""Compare causal sign under simultaneous (parallel) vs forward-sweep updates."""
import csv, json, statistics
from pathlib import Path
from dataclasses import replace
from spatial_v05 import Config, build_arrivals, simulate


def main():
    rows=[]
    for update in ('sequential','parallel'):
        for signal_mode in ('leading','lagging'):
            for seed in range(10):
                baseline=Config(seed=seed)
                arrival=build_arrivals(baseline)
                for fork in (-21,-13):
                    for k in (2,4):
                        config=replace(baseline,signal_mode=signal_mode,
                                       fork_cells=fork,bay_limit=k,update_mode=update)
                        stats=simulate(config,arrival)['stats']
                        rows.append({'update_mode':update,'signal_mode':signal_mode,
                                     'seed':seed,'fork_cells':fork,'bay_limit':k,
                                     'exits':stats['exits'],
                                     'fork_block_cap_s':stats.get('fork_block_cap_s',0)})
    summary={}
    for update in ('sequential','parallel'):
        for mode in ('leading','lagging'):
            interactions=[]
            for seed in range(10):
                data={(r['fork_cells'],r['bay_limit']):r['exits'] for r in rows
                      if r['update_mode']==update and r['signal_mode']==mode and r['seed']==seed}
                interactions.append((data[-13,4]-data[-13,2])-(data[-21,4]-data[-21,2]))
            summary[update+'|'+mode]={'interactions':interactions,
                'mean':statistics.mean(interactions),
                'sd_sample':statistics.stdev(interactions),
                'all_negative':all(x<0 for x in interactions)}
    out=Path(__file__).resolve().parent/'results'
    out.mkdir(exist_ok=True)
    with (out/'update_sensitivity_runs.csv').open('w',newline='',encoding='utf-8') as fp:
        writer=csv.DictWriter(fp,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (out/'update_sensitivity_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
